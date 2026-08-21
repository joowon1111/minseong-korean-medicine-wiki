from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("변비","conditions/constipation.md"),
("설사","conditions/diarrhea.md"),
("역류·속쓰림","conditions/gerd.md"),
("과민성장증후군","conditions/ibs.md"),
("이명","conditions/tinnitus.md"),
("안구건조","conditions/dry-eye.md"),
("안면신경마비","conditions/facial-palsy.md"),
("발뒤꿈치·족저근막 통증","conditions/plantar-fasciitis.md"),
("팔꿈치 바깥쪽 통증","conditions/tennis-elbow.md"),
("손저림·손목터널증후군","conditions/carpal-tunnel.md"),
]
# Add to the existing detailed condition list, after a known existing condition.
anchor="      - 산후회복: conditions/postpartum-recovery.md"
if anchor not in t:
    # fallback: add after menopause if current nav lacks postpartum line
    anchor="      - 갱년기: conditions/menopause.md"
if anchor not in t:
    raise SystemExit("ERROR: condition nav anchor not found; mkdocs.yml unchanged")
addition="\n".join(f"      - {label}: {path}" for label,path in items)
if "conditions/constipation.md" not in t:
    t=t.replace(anchor,anchor+"\n"+addition,1)
# backup and YAML validation
Path("mkdocs.yml.before-condition-expansion.bak").write_text(orig,encoding="utf-8")
try:
    import yaml
    yaml.safe_load(t)
except Exception:
    p.write_text(orig,encoding="utf-8")
    raise
p.write_text(t,encoding="utf-8")
print("OK: 10 condition pages registered and YAML validated")
