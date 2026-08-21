from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("노인 입마름·구강건조","conditions/elderly-dry-mouth.md"),
("노인보약·어르신보약","conditions/elderly-tonic.md"),
("면역력저하·잦은 감기","conditions/low-immunity-recurrent-illness.md"),
("수술 후 회복·기력저하","conditions/postoperative-recovery.md"),
("기력회복·허약","conditions/energy-recovery.md"),
("암 치료 후 회복·기력저하","conditions/cancer-treatment-recovery.md"),
]
anchors=[
"      - 후비루·목뒤로 넘어가는 콧물: conditions/postnasal-drip.md",
"      - 손목통증: conditions/wrist-pain.md",
"      - 산후회복: conditions/postpartum-recovery.md",
"      - 만성피로: conditions/chronic-fatigue.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe nav anchor not found")
missing=[(a,b) for a,b in items if b not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml
        yaml.safe_load(new)
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; mkdocs.yml unchanged: {e}")
    Path("mkdocs.yml.before-elderly-recovery-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
