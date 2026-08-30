#!/usr/bin/env python3
"""Audit MkDocs source links and generated-site links before deployment."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = ROOT / "site"

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
HTML_LINK = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
FRONT_TITLE = re.compile(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$")
H1 = re.compile(r"(?m)^#\s+(.+?)\s*$")


def local_candidates(source: Path, raw: str) -> list[Path]:
    split = urlsplit(unquote(raw.strip().strip("<>")))
    if split.scheme or split.netloc or not split.path or split.path.startswith("//"):
        return []
    path = split.path
    base = DOCS / path.lstrip("/") if path.startswith("/") else source.parent / path
    if path.endswith("/"):
        return [base / "index.md", base.with_suffix(".md"), base / "index.html"]
    if base.suffix:
        return [base]
    return [base.with_suffix(".md"), base / "index.md", base]


def audit_source() -> int:
    files = sorted(DOCS.rglob("*.md"))
    missing: list[tuple[str, int, str]] = []
    html_md: list[tuple[str, int, str]] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    url_map: dict[str, list[str]] = defaultdict(list)
    titles: dict[str, list[str]] = defaultdict(list)

    for source in files:
        rel = source.relative_to(DOCS).as_posix()
        text = source.read_text(encoding="utf-8-sig", errors="replace")
        title_match = FRONT_TITLE.search(text) or H1.search(text)
        if title_match:
            title = re.sub(r"\s+", " ", title_match.group(1).strip().strip("'\""))
            titles[title].append(rel)
        normalized = re.sub(r"(?s)^---.*?---\s*", "", text, count=1)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        if len(normalized) >= 120:
            hashes[hashlib.sha256(normalized.encode()).hexdigest()].append(rel)
        url = "/" if rel == "index.md" else "/" + (rel[:-8] if rel.endswith("/index.md") else rel[:-3] + "/")
        url_map[url].append(rel)

        for kind, regex in (("markdown", MD_LINK), ("html", HTML_LINK)):
            for match in regex.finditer(text):
                raw = match.group(1)
                line = text.count("\n", 0, match.start()) + 1
                if kind == "html" and urlsplit(raw).path.endswith(".md"):
                    html_md.append((rel, line, raw))
                candidates = local_candidates(source, raw)
                if candidates and not any(path.exists() for path in candidates):
                    missing.append((rel, line, raw))

    duplicate_content = [paths for paths in hashes.values() if len(paths) > 1]
    collisions = {url: paths for url, paths in url_map.items() if len(paths) > 1}
    duplicate_titles = {title: paths for title, paths in titles.items() if len(paths) > 1}

    print(f"source documents: {len(files)}")
    print(f"missing internal links: {len(missing)}")
    print(f"raw HTML .md links: {len(html_md)}")
    print(f"URL collisions: {len(collisions)}")
    print(f"exact duplicate contents: {len(duplicate_content)}")
    print(f"duplicate titles: {len(duplicate_titles)}")
    for rel, line, raw in missing:
        print(f"ERROR missing: {rel}:{line} -> {raw}")
    for rel, line, raw in html_md:
        print(f"ERROR raw .md: {rel}:{line} -> {raw}")
    for url, paths in collisions.items():
        print(f"ERROR URL collision: {url} <- {' | '.join(paths)}")
    for paths in duplicate_content:
        print(f"ERROR duplicate content: {' | '.join(paths)}")
    for title, paths in duplicate_titles.items():
        print(f"WARN duplicate title: {title} <- {' | '.join(paths)}")
    return len(missing) + len(html_md) + len(collisions) + len(duplicate_content)


def audit_site() -> int:
    if not SITE.exists():
        print("ERROR generated site directory does not exist; run mkdocs build first")
        return 1
    missing: set[tuple[str, str]] = set()
    for page in sorted(SITE.rglob("*.html")):
        html = page.read_text(encoding="utf-8", errors="replace")
        for match in HTML_LINK.finditer(html):
            raw = unquote(match.group(1).strip())
            split = urlsplit(raw)
            if split.scheme or split.netloc or not split.path or split.path.startswith("//"):
                continue
            path = split.path
            target = SITE / path.lstrip("/") if path.startswith("/") else page.parent / path
            candidates = [target]
            if path.endswith("/"):
                candidates.append(target / "index.html")
            elif not target.suffix:
                candidates.extend([target.with_suffix(".html"), target / "index.html"])
            if not any(candidate.exists() for candidate in candidates):
                missing.add((page.relative_to(SITE).as_posix(), raw))
    print(f"generated-site missing links: {len(missing)}")
    for page, raw in sorted(missing):
        print(f"ERROR generated link: {page} -> {raw}")
    return len(missing)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", action="store_true", help="also audit generated site HTML")
    args = parser.parse_args()
    errors = audit_source()
    if args.site:
        errors += audit_site()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

