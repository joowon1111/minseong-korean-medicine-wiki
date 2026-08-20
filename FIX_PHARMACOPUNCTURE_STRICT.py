from pathlib import Path
import re

docs=Path("docs")
pharm=docs/"acupuncture-integrated"/"pharmacopuncture.md"
modal=docs/"acupuncture-integrated"/"modalities.md"

if not pharm.exists():
    raise SystemExit("ERROR: docs/acupuncture-integrated/pharmacopuncture.md not found")
if not modal.exists():
    raise SystemExit("ERROR: docs/acupuncture-integrated/modalities.md not found")

ph=pharm.read_text(encoding="utf-8")
# Remove YAML front matter and title so it becomes a section of the existing page.
ph=re.sub(r"\A---\n.*?\n---\n", "", ph, flags=re.S)
ph=ph.lstrip()
ph=re.sub(r"\A# 약침치료\s*\n", "## 약침치료\n", ph, count=1)

mt=modal.read_text(encoding="utf-8")
marker="## 약침치료"
if marker in mt:
    mt=mt.split(marker)[0].rstrip()+"\n\n"+ph.rstrip()+"\n"
else:
    mt=mt.rstrip()+"\n\n"+ph.rstrip()+"\n"
modal.write_text(mt,encoding="utf-8")

# Rewrite every markdown link in docs that pointed to the standalone page.
for p in docs.rglob("*.md"):
    t=p.read_text(encoding="utf-8")
    old=t
    # same-folder and relative references
    t=t.replace("(pharmacopuncture.md)", "(modalities.md#약침치료)")
    t=t.replace("(pharmacopuncture.md#", "(modalities.md#")
    t=t.replace("(../acupuncture-integrated/pharmacopuncture.md)", "(../acupuncture-integrated/modalities.md#약침치료)")
    t=t.replace("(../acupuncture-integrated/pharmacopuncture.md#", "(../acupuncture-integrated/modalities.md#")
    if t != old:
        p.write_text(t,encoding="utf-8")

# Remove standalone page so strict nav cannot complain that it is outside nav.
pharm.unlink()

print("DONE")
print("- pharmacopuncture.md merged into existing modalities.md")
print("- all pharmacopuncture links rewritten")
print("- standalone pharmacopuncture.md removed")
print("- mkdocs.yml unchanged")
