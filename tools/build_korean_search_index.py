#!/usr/bin/env python3
from pathlib import Path
import re,json,yaml,html
docs=Path("docs")
aliases={
"비염":["비염","알레르기비염","코막힘","콧물","재채기"],
"불면":["불면","불면증","수면","잠","잠이 안 와요","자주 깨요"],
"요통":["요통","허리통증","허리가 아파요"],
"소화불량":["소화불량","더부룩함","체했어요","명치 답답함"],
"녹용":["녹용","녹용보약"],
"귀비탕":["귀비탕"],
"족삼리":["족삼리","ST36"],
}
out=[]
for p in docs.rglob("*.md"):
    if any(x in p.parts for x in ["templates"]): continue
    txt=p.read_text(encoding="utf-8-sig",errors="ignore")
    fm={}
    body=txt
    if txt.startswith("---"):
        parts=txt.split("---",2)
        if len(parts)>=3:
            try: fm=yaml.safe_load(parts[1]) or {}
            except: fm={}
            body=parts[2]
    title=str(fm.get("title") or "")
    if not title:
        m=re.search(r"^#\s+(.+)$",body,re.M); title=m.group(1).strip() if m else p.stem
    plain=re.sub(r"`[^`]*`"," ",body)
    plain=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",plain)
    plain=re.sub(r"[#>*_|~-]+"," ",plain)
    plain=re.sub(r"\s+"," ",plain).strip()
    keys=set(map(str,fm.get("tags",[]) if isinstance(fm.get("tags"),list) else []))
    blob=(title+" "+plain).lower()
    for canonical,vals in aliases.items():
        if canonical.lower() in blob or any(v.lower() in blob for v in vals):
            keys.update(vals)
    rel=p.relative_to(docs).as_posix()
    if rel=="index.md": url="./"
    elif rel.endswith("/index.md"): url="./"+rel[:-8]
    else: url="./"+rel[:-3]+"/"
    out.append({"title":title,"url":url,"keywords":sorted(keys),"text":plain[:1800],
                "snippet":plain[:180]})
asset=docs/"assets";asset.mkdir(exist_ok=True)
(asset/"korean-search-index.json").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print("Korean fallback index:",len(out),"documents")
