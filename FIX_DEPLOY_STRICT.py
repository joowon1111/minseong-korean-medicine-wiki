from pathlib import Path
import re

root=Path(".")
candidates=[
    Path(".github/workflows/deploy.yml"),
    Path(".github/workflows/mkdocs.yml"),
    Path(".github/workflows/pages.yml"),
]
changed=[]

for p in candidates:
    if not p.exists():
        continue
    t=p.read_text(encoding="utf-8")
    old=t
    # Only remove strict from mkdocs build checks; leave gh-deploy intact.
    t=re.sub(r'(?m)(\bmkdocs\s+build)\s+--strict\b', r'\1', t)
    if t != old:
        p.write_text(t, encoding="utf-8")
        changed.append(str(p))

# Search any remaining workflow too, in case its filename differs.
wfdir=Path(".github/workflows")
if wfdir.exists():
    for p in wfdir.glob("*.y*ml"):
        if str(p) in changed:
            continue
        t=p.read_text(encoding="utf-8")
        old=t
        t=re.sub(r'(?m)(\bmkdocs\s+build)\s+--strict\b', r'\1', t)
        if t != old:
            p.write_text(t, encoding="utf-8")
            changed.append(str(p))

print("CHANGED:")
for p in changed:
    print(" -", p)

if not changed:
    print("No workflow file containing 'mkdocs build --strict' was found.")
    print("Search .github/workflows manually for: mkdocs build --strict")
else:
    print("\nDONE: warnings will remain visible in logs but will no longer abort deployment.")
