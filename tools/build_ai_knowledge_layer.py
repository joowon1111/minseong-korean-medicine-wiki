#!/usr/bin/env python3
"""Build a deterministic, machine-readable knowledge layer from MkDocs pages.

Only explicit document metadata and internal links are exported. Diagnostic
codes are never inferred from prose: they are included only when a document
front matter explicitly provides them.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import hashlib
import json
import re
import sys

import yaml


DOCS = Path("docs")
OUT_DIR = DOCS / "assets" / "ai"
SCHEMA_SOURCE = Path("tools/ai-knowledge/schema-v1.json")
BASE_URL = "https://wiki.minseong.co.kr"
SCHEMA_VERSION = "1.0"

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"""href\s*=\s*["']([^"'#]+(?:#[^"']*)?)["']""", re.I)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
PMID_RE = re.compile(
    r"(?:PMID\s*[:：]?\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d{6,9})",
    re.I,
)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.I)
CODE_FIELDS = {
    "kcd": "kcd",
    "mesh": "mesh",
    "icd11": "icd11",
    "icd-11": "icd11",
    "who_code": "who",
    "who_codes": "who",
    "acupoint_code": "who_acupoint",
}
SAFETY_TERMS = (
    "위험신호",
    "안전",
    "주의",
    "금기",
    "복용 전",
    "이상반응",
    "부작용",
    "응급",
    "먼저 확인",
)
RED_FLAG_TERMS = ("위험신호", "응급", "즉시", "먼저 확인")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        data = {}
    return (data if isinstance(data, dict) else {}), parts[2]


def as_strings(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        values = value
    else:
        values = [value]
    result = []
    for item in values:
        text = str(item).strip()
        if text:
            result.append(text)
    return result


def unique(values: list[str], *, limit: int | None = None) -> list[str]:
    seen = set()
    result = []
    for value in values:
        normalized = re.sub(r"\s+", " ", value).strip()
        key = normalized.casefold()
        if not normalized or key in seen:
            continue
        seen.add(key)
        result.append(normalized)
        if limit and len(result) >= limit:
            break
    return result


def canonical_url(path: Path) -> str:
    rel = path.relative_to(DOCS).as_posix()
    if rel == "index.md":
        return f"{BASE_URL}/"
    if rel.endswith("/index.md"):
        return f"{BASE_URL}/{rel[:-8]}"
    return f"{BASE_URL}/{rel[:-3]}/"


def entity_id(path: Path) -> str:
    rel = path.relative_to(DOCS).as_posix()
    if rel == "index.md":
        return "km:home"
    slug = rel[:-3]
    if slug.endswith("/index"):
        slug = slug[:-6]
    return f"km:{slug.strip('/')}"


def entity_type(path: Path) -> str:
    rel = path.relative_to(DOCS).as_posix()
    rules = (
        ("authority/conditions/", "condition_evidence"),
        ("authority/herbs/", "herb_evidence"),
        ("authority/formulas/", "formula_evidence"),
        ("research/formulas/", "formula_evidence"),
        ("research/", "research"),
        ("conditions/", "condition"),
        ("symptoms/", "symptom"),
        ("symptom-", "symptom_guide"),
        ("herbs/", "herb"),
        ("formulas/", "formula"),
        ("acupuncture/points/", "acupoint"),
        ("acupoints/", "acupoint"),
        ("acupuncture/extra-points/", "acupoint"),
        ("acupuncture/meridians/", "meridian"),
        ("sasang-formula", "sasang_formula"),
        ("diagnostics/patterns/", "pattern"),
        ("pattern-treatment/", "pattern"),
        ("answer-guides/", "question_guide"),
        ("classics/", "classical_source"),
        ("guide/", "guide"),
        ("portal/", "portal"),
        ("pillar/", "topic_hub"),
        ("network/", "knowledge_map"),
        ("evidence-", "evidence_guide"),
        ("sasang", "sasang_medicine"),
        ("acupuncture", "acupuncture"),
    )
    for prefix, kind in rules:
        if rel.startswith(prefix):
            return kind
    if "-integrated/" in rel or "-network/" in rel:
        return "knowledge_hub"
    return "article"


def extract_search_aliases(body: str) -> list[str]:
    match = re.search(
        r"^##\s+검색\s*동의어\s*$\n(.*?)(?=^##\s+|\Z)",
        body,
        flags=re.M | re.S,
    )
    if not match:
        return []
    block = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", match.group(1))
    block = re.sub(r"[*_>#]", " ", block)
    return unique(re.split(r"[·,;|\n]+", block), limit=40)


def extract_codes(frontmatter: dict, title: str, path: Path) -> dict[str, list[str]]:
    codes: dict[str, list[str]] = {}
    for source_key, output_key in CODE_FIELDS.items():
        values = unique(as_strings(frontmatter.get(source_key)))
        if values:
            codes[output_key] = values

    if entity_type(path) == "acupoint":
        match = re.search(r"\b(?:EX-[A-Z]{2}|[A-Z]{2})\d+\b", title, re.I)
        if match:
            codes.setdefault("who_acupoint", []).append(match.group(0).upper())
    return {key: unique(values) for key, values in sorted(codes.items())}


def extract_evidence_ids(text: str) -> dict[str, list[str]]:
    pmids = sorted(set(PMID_RE.findall(text)), key=int)
    dois = {
        value.rstrip(".,;:)]}").lower()
        for value in DOI_RE.findall(text)
    }
    result = {}
    if pmids:
        result["pmid"] = pmids
    if dois:
        result["doi"] = sorted(dois)
    return result


def page_title(frontmatter: dict, body: str, path: Path) -> str:
    title = str(frontmatter.get("title") or "").strip()
    if title:
        return title
    match = H1_RE.search(body)
    return match.group(1).strip() if match else path.stem


def build_entity(path: Path, text: str, frontmatter: dict, body: str) -> dict:
    title = page_title(frontmatter, body, path)
    tags = unique(as_strings(frontmatter.get("tags")))
    keywords = unique(as_strings(frontmatter.get("keywords")))
    aliases = unique(
        as_strings(frontmatter.get("aliases"))
        + as_strings(frontmatter.get("synonyms"))
        + extract_search_aliases(body),
        limit=50,
    )
    aliases = [alias for alias in aliases if alias.casefold() != title.casefold()]

    sections = unique(
        [re.sub(r"\s*\{#[^}]+\}\s*$", "", item).strip() for item in H2_RE.findall(body)],
        limit=60,
    )
    safety_sections = [
        section
        for section in sections
        if any(term in section for term in SAFETY_TERMS)
    ]
    entity = {
        "id": entity_id(path),
        "type": entity_type(path),
        "name": title,
        "description": str(frontmatter.get("description") or "").strip(),
        "url": canonical_url(path),
        "source_path": path.relative_to(DOCS).as_posix(),
        "language": "ko-KR",
        "aliases": aliases,
        "keywords": keywords,
        "tags": tags,
        "codes": extract_codes(frontmatter, title, path),
        "evidence_ids": extract_evidence_ids(text),
        "sections": sections,
        "safety": {
            "has_safety_section": bool(safety_sections),
            "has_red_flag_section": any(
                term in section
                for section in safety_sections
                for term in RED_FLAG_TERMS
            ),
            "sections": safety_sections,
        },
    }
    status = str(frontmatter.get("status") or "").strip()
    reviewed = str(frontmatter.get("last_reviewed") or "").strip()
    if status:
        entity["status"] = status
    if reviewed:
        entity["last_reviewed"] = reviewed
    return entity


def resolve_target(source: Path, raw_target: str, by_url: dict[str, Path]) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    parts = urlsplit(target)
    if parts.scheme in {"http", "https"}:
        if parts.netloc not in {"wiki.minseong.co.kr", "www.wiki.minseong.co.kr"}:
            return None
        key = parts.path or "/"
        return by_url.get(key.rstrip("/") or "/")

    clean = unquote(parts.path)
    if not clean:
        return None
    if clean.startswith("/"):
        return by_url.get(clean.rstrip("/") or "/")

    candidate = source.parent / clean
    if candidate.suffix == ".md":
        resolved = candidate
    elif candidate.suffix:
        return None
    elif (candidate / "index.md").exists():
        resolved = candidate / "index.md"
    else:
        resolved = candidate.with_suffix(".md")
    try:
        resolved = resolved.resolve().relative_to(DOCS.resolve())
    except (ValueError, OSError):
        return None
    final = DOCS / resolved
    return final if final.exists() else None


def relation_name(target_type: str) -> str:
    if target_type in {"condition", "condition_evidence"}:
        return "links_to_condition"
    if target_type in {"formula", "sasang_formula", "formula_evidence"}:
        return "links_to_formula"
    if target_type in {"herb", "herb_evidence"}:
        return "links_to_herb"
    if target_type == "acupoint":
        return "links_to_acupoint"
    if target_type == "pattern":
        return "links_to_pattern"
    if target_type in {"research", "evidence_guide"}:
        return "links_to_evidence"
    return "links_to"


def document_paths() -> list[Path]:
    return sorted(
        path
        for path in DOCS.rglob("*.md")
        if "templates" not in path.parts
    )


def build() -> tuple[list[dict], list[dict]]:
    paths = document_paths()
    parsed = {}
    entities = []
    for path in paths:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        frontmatter, body = parse_frontmatter(text)
        parsed[path] = (text, body)
        entities.append(build_entity(path, text, frontmatter, body))

    entity_by_path = {DOCS / item["source_path"]: item for item in entities}
    by_url = {}
    for path in paths:
        relative_url = canonical_url(path).removeprefix(BASE_URL)
        by_url[relative_url.rstrip("/") or "/"] = path

    relations = set()
    for source, (_, body) in parsed.items():
        source_entity = entity_by_path[source]
        targets = MARKDOWN_LINK_RE.findall(body) + HTML_LINK_RE.findall(body)
        for raw_target in targets:
            target_path = resolve_target(source, raw_target, by_url)
            if not target_path or target_path == source or target_path not in entity_by_path:
                continue
            target_entity = entity_by_path[target_path]
            relations.add(
                (
                    source_entity["id"],
                    relation_name(target_entity["type"]),
                    target_entity["id"],
                )
            )

    relation_rows = [
        {"source": source, "relation": relation, "target": target}
        for source, relation, target in sorted(relations)
    ]
    return sorted(entities, key=lambda item: item["id"]), relation_rows


def validate(entities: list[dict], relations: list[dict]) -> None:
    for field in ("id", "url", "source_path"):
        values = [item[field] for item in entities]
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate entity {field}: {duplicates[:10]}")

    known_ids = {item["id"] for item in entities}
    dangling = [
        relation
        for relation in relations
        if relation["source"] not in known_ids or relation["target"] not in known_ids
    ]
    if dangling:
        raise ValueError(f"Dangling relations: {dangling[:10]}")

    duplicate_relations = len(relations) - len(
        {
            (item["source"], item["relation"], item["target"])
            for item in relations
        }
    )
    if duplicate_relations:
        raise ValueError(f"Duplicate relations: {duplicate_relations}")


def json_bytes(value, *, pretty: bool = False) -> bytes:
    if pretty:
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    else:
        text = json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return text.encode("utf-8")


def write_if_changed(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when committed AI knowledge files are stale.",
    )
    args = parser.parse_args()

    entities, relations = build()
    validate(entities, relations)
    entity_types = Counter(item["type"] for item in entities)
    relation_types = Counter(item["relation"] for item in relations)
    safety_count = sum(item["safety"]["has_safety_section"] for item in entities)
    red_flag_count = sum(item["safety"]["has_red_flag_section"] for item in entities)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "entities": entities,
        "relations": relations,
    }
    payload_bytes = json_bytes(payload)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "base_url": BASE_URL,
        "language": "ko-KR",
        "entity_count": len(entities),
        "relation_count": len(relations),
        "entity_types": dict(sorted(entity_types.items())),
        "relation_types": dict(sorted(relation_types.items())),
        "safety_section_entities": safety_count,
        "red_flag_section_entities": red_flag_count,
        "content_sha256": hashlib.sha256(payload_bytes).hexdigest(),
        "files": {
            "knowledge_graph": "/assets/ai/knowledge-graph.json",
            "schema": "/assets/ai/knowledge-schema.json"
        },
        "code_policy": "explicit_metadata_only",
        "contains_patient_data": False
    }

    expected = {
        OUT_DIR / "knowledge-graph.json": payload_bytes,
        OUT_DIR / "knowledge-manifest.json": json_bytes(manifest, pretty=True),
        OUT_DIR / "knowledge-schema.json": SCHEMA_SOURCE.read_bytes()
    }

    stale = [
        str(path)
        for path, content in expected.items()
        if not path.exists() or path.read_bytes() != content
    ]
    if args.check:
        if stale:
            print("Stale AI knowledge files:")
            for path in stale:
                print(f"- {path}")
            return 1
    else:
        for path, content in expected.items():
            write_if_changed(path, content)

    print(
        f"AI knowledge layer: {len(entities)} entities, "
        f"{len(relations)} relations -> {OUT_DIR}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
