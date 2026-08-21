from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("복통","conditions/abdominal-pain.md"),
("복부팽만·가스","conditions/bloating.md"),
("메스꺼움·오심","conditions/nausea.md"),
("월경통·생리통","conditions/dysmenorrhea.md"),
("월경불순·생리불순","conditions/irregular-menstruation.md"),
("부종","conditions/edema.md"),
("턱관절통증","conditions/tmj-pain.md"),
("좌골신경통·하지방사통","conditions/sciatica.md"),
("발목통증","conditions/ankle-pain.md"),
("손목통증","conditions/wrist-pain.md"),
]
# Prefer previously-added carpal tunnel as anchor, then fallback to postpartum/menopause.
anchors=[
"      - 손저림·손목터널증후군: conditions/carpal-tunnel.md",
"      - 산후회복: conditions/postpartum-recovery.md",
"      - 갱년기: conditions/menopause.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor:
    raise SystemExit("ERROR: condition nav anchor not found; mkdocs.yml unchanged")
addition="\n".join(f"      - {label}: {path}" for label,path in items)
if "conditions/abdominal-pain.md" not in t:
    t=t.replace(anchor,anchor+"\n"+addition,1)

Path("mkdocs.yml.before-condition-expansion-10b.bak").write_text(orig,encoding="utf-8")
try:
    import yaml
    yaml.safe_load(t)
except Exception:
    p.write_text(orig,encoding="utf-8")
    raise
p.write_text(t,encoding="utf-8")
print("OK: second 10 condition pages registered and YAML validated")
