from pathlib import Path
import re, sys

repo = Path.cwd()
docs = repo / "docs"
if not (repo / "mkdocs.yml").exists() or not docs.exists():
    raise SystemExit("저장소 최상위(mkdocs.yml이 있는 곳)에서 실행하세요.")

# Only link herbs whose current paths are confirmed in the actual mkdocs.yml.
herbs = {
    "녹용":"herbs/cervi-parvum-cornu.md",
    "인삼":"herbs/ginseng.md",
    "황기":"herbs/astragalus.md",
    "당귀":"herbs/angelica.md",
    "숙지황":"herbs/prepared-rehmannia.md",
    "백출":"herbs/atractylodes.md",
    "복령":"herbs/poria.md",
    "백복령":"herbs/poria.md",
    "적복령":"herbs/poria.md",
    "산수유":"herbs/cornus-fruit.md",
    "산조인":"herbs/ziziphus-seed.md",
    "오미자":"herbs/schisandra.md",
    "반하":"herbs/pinellia.md",
    "진피":"herbs/citrus-peel.md",
    "택사":"herbs/alisma.md",
    "생지황":"herbs/fresh-rehmannia.md",
    "맥문동":"herbs/ophiopogon.md",
    "천궁":"herbs/chuanxiong.md",
    "백작약":"herbs/white-peony.md",
    "육계":"herbs/cinnamon-bark.md",
    "계피":"herbs/cinnamon-bark.md",
    "감초":"herbs/licorice.md",
    "자감초":"herbs/licorice.md",
}

targets = []
for folder in ["sasang-formula-cards","sasang-formula-cards-2","sasang-formula-library"]:
    p=docs/folder
    if p.exists():
        targets += list(p.glob("*.md"))

changed=[]
links_added=0

for f in targets:
    text=f.read_text(encoding="utf-8-sig")
    original=text
    # Link herb names only in markdown table first column: | 숙지황 | ...
    for name,path in sorted(herbs.items(), key=lambda x: -len(x[0])):
        # Do not touch already-linked names.
        pattern = rf'(?m)^(\|\s*){re.escape(name)}(\s*\|)'
        repl = rf'\1[{name}](../{path})\2'
        text,n = re.subn(pattern,repl,text)
        links_added += n

    if text != original:
        f.write_text(text,encoding="utf-8")
        changed.append(str(f.relative_to(repo)))

print(f"수정 문서: {len(changed)}개")
print(f"추가 링크: {links_added}개")
for x in changed: print(" -",x)

# Validate every generated relative target.
bad=[]
link_re=re.compile(r'\]\((\.\./herbs/[^)]+\.md)\)')
for f in targets:
    txt=f.read_text(encoding="utf-8")
    for rel in link_re.findall(txt):
        target=(f.parent/rel).resolve()
        if not target.exists():
            bad.append((str(f.relative_to(repo)),rel))
if bad:
    print("깨진 링크 발견:")
    for x in bad: print(x)
    raise SystemExit(2)
print("본초 내부링크 대상 검증: OK")
