#!/usr/bin/env python3
from pathlib import Path
import json
import re
import yaml

DOCS = Path("docs")
OUT = DOCS / "assets" / "korean-search-index.json"

ALIASES = {
    "비염": ["비염", "알레르기비염", "알레르기 비염", "코막힘", "코 막힘", "콧물", "재채기", "코가 막혀요"],
    "불면": ["불면", "불면증", "수면장애", "잠이 안 와요", "잠이안와요", "잠이 안와요", "자주 깨요", "새벽에 깨요"],
    "수면": ["수면", "잠", "숙면", "잠잘", "잠드는", "수면의 질"],
    "요통": ["요통", "허리통증", "허리 통증", "허리가 아파요", "허리가아파요", "허리 아픔"],
    "소화불량": ["소화불량", "소화 불량", "더부룩함", "체했어요", "명치 답답함", "속이 더부룩해요"],
    "녹용": ["녹용", "녹용보약", "녹용 보약"],
    "귀비탕": ["귀비탕"],
    "족삼리": ["족삼리", "ST36", "st36"],
}

CATEGORY_BOOSTS = {
    "conditions/": 20,
    "authority/conditions/": 18,
    "answer-guides/": 14,
    "research/": 10,
    "formulas/": 8,
    "herbs/": 8,
    "acupuncture/": 8,
    "acupoints/": 8,
}

def strip_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        return yaml.safe_load(parts[1]) or {}, parts[2]
    except Exception:
        return {}, parts[2]

def clean_markdown(body):
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"`([^`]*)`", r"\1", body)
    body = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"[#>*_|~=-]+", " ", body)
    return re.sub(r"\s+", " ", body).strip()

def title_from(fm, body, path):
    title = str(fm.get("title") or "").strip()
    if title:
        return title
    m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    return m.group(1).strip() if m else path.stem

def url_from(path):
    rel = path.relative_to(DOCS).as_posix()
    if rel == "index.md":
        return "/"
    if rel.endswith("/index.md"):
        return "/" + rel[:-8]
    return "/" + rel[:-3] + "/"

def path_boost(path):
    rel = path.relative_to(DOCS).as_posix()
    return max((score for prefix, score in CATEGORY_BOOSTS.items() if rel.startswith(prefix)), default=0)

def keyword_set(title, plain, fm):
    keys = set()
    tags = fm.get("tags", [])
    if isinstance(tags, list):
        keys.update(str(x).strip() for x in tags if str(x).strip())

    blob = f"{title} {plain}".lower()
    for canonical, vals in ALIASES.items():
        candidates = [canonical, *vals]
        if any(v.lower() in blob for v in candidates):
            keys.add(canonical)
            keys.update(vals)
    return sorted(keys)

def main():
    rows = []
    for p in DOCS.rglob("*.md"):
        if any(part in {"templates"} for part in p.parts):
            continue

        raw = p.read_text(encoding="utf-8-sig", errors="ignore")
        fm, body = strip_frontmatter(raw)
        title = title_from(fm, body, p)
        plain = clean_markdown(body)
        keys = keyword_set(title, plain, fm)

        # 검색 품질을 위해 너무 짧은 문서도 유지하되, 텍스트는 충분히 수록한다.
        rows.append({
            "title": title,
            "url": url_from(p),
            "keywords": keys,
            "text": plain[:5000],
            "snippet": plain[:260],
            "boost": path_boost(p),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(rows, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Korean search index: {len(rows)} documents -> {OUT}")

if __name__ == "__main__":
    main()
