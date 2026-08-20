from pathlib import Path
import re

repo=Path.cwd()
docs=repo/"docs"
if not (repo/"mkdocs.yml").exists() or not docs.exists():
    raise SystemExit("저장소 최상위(mkdocs.yml이 있는 곳)에서 실행하세요.")

formula_dirs=[
    docs/"sasang-formula-cards",
    docs/"sasang-formula-cards-2",
    docs/"sasang-formula-library",
]
herb_dir=docs/"herbs"
if not herb_dir.exists():
    raise SystemExit("docs/herbs 폴더가 없습니다.")

# Build herb target map from links already present in formula tables.
# This avoids inventing herb paths.
herb_to_formulas={}
formula_title={}

def get_title(text, fallback):
    m=re.search(r'(?m)^title:\s*(.+?)\s*$',text)
    if m: return m.group(1).strip().strip("'\"")
    m=re.search(r'(?m)^#\s+(.+?)\s*$',text)
    return m.group(1).strip() if m else fallback

for fd in formula_dirs:
    if not fd.exists(): continue
    for f in fd.glob("*.md"):
        if f.name=="index.md": continue
        txt=f.read_text(encoding="utf-8-sig")
        title=get_title(txt,f.stem)
        formula_title[f.resolve()]=title
        # Match linked herb names in table cells.
        for name, rel in re.findall(r'\[([^\]]+)\]\((\.\./herbs/[^)]+\.md)\)',txt):
            target=(f.parent/rel).resolve()
            if target.exists():
                herb_to_formulas.setdefault(target,[]).append((title,f.resolve()))

# Update each herb page with an auto-generated reverse-link section.
start="<!-- BEGIN AUTO SASANG FORMULA LINKS -->"
end="<!-- END AUTO SASANG FORMULA LINKS -->"
changed=0
for herb_file, formulas in herb_to_formulas.items():
    txt=herb_file.read_text(encoding="utf-8-sig")
    # remove old generated block
    txt=re.sub(r'(?ms)\n?'+re.escape(start)+r'.*?'+re.escape(end)+r'\n?', '\n', txt)
    unique=[]
    seen=set()
    for title,fp in formulas:
        if fp in seen: continue
        seen.add(fp)
        rel=Path(fp).relative_to(docs)
        # herb page is docs/herbs/*.md, so ../ reaches docs root.
        unique.append((title,"../"+rel.as_posix()))
    unique.sort(key=lambda x:x[0])
    block=["",start,"## 이 본초가 들어가는 사상처방",""]
    block.append("현재 위키의 사상처방 구성표에서 이 본초가 확인되는 처방입니다.")
    block.append("")
    for title,rel in unique:
        block.append(f"- [{title}]({rel})")
    block += ["",end,""]
    herb_file.write_text(txt.rstrip()+"\n"+"\n".join(block),encoding="utf-8")
    changed+=1

# Build global herb→formula index from the verified links.
index=docs/"herbs"/"sasang-formula-reverse-index.md"
rows=[]
for herb_file, formulas in sorted(herb_to_formulas.items(),key=lambda kv: kv[0].name):
    htxt=herb_file.read_text(encoding="utf-8")
    htitle=get_title(htxt,herb_file.stem)
    hrel=herb_file.relative_to(docs).as_posix()
    fs=[]
    seen=set()
    for title,fp in sorted(formulas,key=lambda x:x[0]):
        if title in seen: continue
        seen.add(title)
        frel=Path(fp).relative_to(docs).as_posix()
        fs.append(f"[{title}](../{frel})")
    rows.append(f"| [{htitle}]({herb_file.name}) | " + " · ".join(fs) + " |")

content="""---
title: 본초→사상처방 역색인
tags: [본초, 사상처방, 지식그래프, 역색인]
status: 검토완료
last_reviewed: 2026-08-20
---
# 본초 → 사상처방 역색인

개별 본초에서 **어떤 사상처방에 실제로 들어가는지** 역방향으로 탐색하는 지식지도입니다.

| 본초 | 연결된 사상처방 |
|---|---|
"""+"\n".join(rows)+"""

```text
체질병증 → 처방 → 본초
                  ↓
             본초 상세
                  ↓
       이 본초가 들어가는 다른 처방
```

이 색인은 현재 위키의 처방 구성표에 실제 링크된 본초만 자동 수집합니다.
"""
index.write_text(content,encoding="utf-8")

# Validate all markdown relative links in generated blocks/index.
bad=[]
for f in list(herb_to_formulas.keys())+[index]:
    txt=f.read_text(encoding="utf-8")
    for rel in re.findall(r'\]\((\.\./[^)]+\.md|[^:/()]+\.md)\)',txt):
        target=(f.parent/rel).resolve()
        if not target.exists():
            bad.append((f.relative_to(repo).as_posix(),rel))
if bad:
    for x in bad: print("BROKEN",x)
    raise SystemExit("생성 링크 검증 실패")

print("역링크가 추가된 본초:",changed)
print("전체 역색인:",index.relative_to(repo))
print("링크 검증: OK")
