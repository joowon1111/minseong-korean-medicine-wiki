from pathlib import Path
import shutil, sys

p=Path("mkdocs.yml")
if not p.exists():
    raise SystemExit("ERROR: mkdocs.yml not found")

original=p.read_text(encoding="utf-8")
t=original

cold_line="      - 감기·급성 상기도감염: conditions/common-cold.md"
if cold_line not in t:
    anchor="      - 비염: conditions/rhinitis.md"
    if anchor not in t:
        raise SystemExit("ERROR: rhinitis nav anchor not found; mkdocs.yml unchanged")
    t=t.replace(anchor, anchor+"\n"+cold_line, 1)

insurance_line="  - 건강보험 한약제제: herbal-integrated/insurance-herbal.md"
if insurance_line not in t:
    # Insert only AFTER the entire nested '일반 방제 임상 지도' block,
    # immediately before the next same-level item that exists in the current nav.
    anchor="  - 보익·회복 핵심: herbal-integrated/tonic-recovery.md"
    if anchor not in t:
        raise SystemExit("ERROR: herbal nav anchor not found; mkdocs.yml unchanged")
    t=t.replace(anchor, insurance_line+"\n"+anchor, 1)

backup=Path("mkdocs.yml.before-search-hubs.bak")
backup.write_text(original,encoding="utf-8")
p.write_text(t,encoding="utf-8")

# Validate YAML syntax before leaving the changed file in place.
try:
    import yaml
    yaml.safe_load(t)
except Exception as e:
    p.write_text(original,encoding="utf-8")
    print("YAML validation failed. Restored original mkdocs.yml.")
    raise

print("OK: mkdocs.yml patched and YAML syntax validated")
print(" - 감기·급성 상기도감염 nav registered")
print(" - 건강보험 한약제제 nav registered after general-formulary subtree")
