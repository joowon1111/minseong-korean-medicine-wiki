from pathlib import Path
import re
repo=Path.cwd(); docs=repo/"docs"
mapping={'갈근': 'pueraria.md', '황금': 'scutellaria.md', '석고': 'gypsum.md', '연교': 'forsythia.md', '형개': 'schizonepeta.md', '방풍': 'saposhnikovia.md', '강활': 'notopterygium.md', '독활': 'angelica-pubescens.md', '나복자': 'raphanus-seed.md', '내복자': 'raphanus-seed.md', '길경': 'platycodon.md', '마황': 'ephedra.md', '지모': 'anemarrhena.md', '황백': 'phellodendron.md', '대황': 'rhubarb.md'}
changed=0; added=0
for folder in ["sasang-formula-cards","sasang-formula-cards-2","sasang-formula-library"]:
    p=docs/folder
    if not p.exists(): continue
    for f in p.glob("*.md"):
        text=f.read_text(encoding="utf-8-sig"); old=text
        for name,fn in sorted(mapping.items(),key=lambda x:-len(x[0])):
            # Only first-column herb names in markdown tables.
            pat=rf'(?m)^(\|\s*){re.escape(name)}(\s*\|)'
            rep=rf'\1[{name}](../herbs/{fn})\2'
            text,n=re.subn(pat,rep,text)
            added+=n
        if text!=old:
            f.write_text(text,encoding="utf-8"); changed+=1
print("수정 문서:",changed,"추가 링크:",added)
# validate new targets
for folder in ["sasang-formula-cards","sasang-formula-cards-2","sasang-formula-library"]:
    p=docs/folder
    if not p.exists(): continue
    for f in p.glob("*.md"):
        for rel in re.findall(r'\]\((\.\./herbs/[^)]+\.md)\)',f.read_text(encoding="utf-8")):
            if not (f.parent/rel).resolve().exists():
                raise SystemExit(f"깨진 링크: {f} -> {rel}")
print("새 본초 링크 검증: OK")
