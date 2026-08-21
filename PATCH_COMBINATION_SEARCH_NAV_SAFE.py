from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[
("피로 + 소화불량","symptom-integrated/fatigue-digestion.md"),
("두통 + 어지럼","symptom-integrated/headache-dizziness.md"),
("비염 + 기침·후비루","symptom-integrated/rhinitis-cough.md"),
("불면 + 두근거림","symptom-integrated/insomnia-palpitations.md"),
("손발냉증 + 상열감","symptom-integrated/cold-hands-hot-flush.md"),
("목통증 + 두통","symptom-integrated/neck-headache.md"),
("허리통증 + 다리저림","symptom-integrated/lowback-leg-numbness.md"),
("갱년기 + 불면·상열감","symptom-integrated/menopause-insomnia.md"),
("산후피로 + 관절·허리통증","symptom-integrated/postpartum-fatigue-pain.md"),
("어르신 식욕저하 + 기력저하","symptom-integrated/elderly-appetite-fatigue.md"),
]
# Find an existing symptom-integrated nav item; only insert siblings at same indentation.
anchors=[
"      - 치료 근거 한눈에 보기: symptom-integrated/treatment-evidence.md",
"      - 수면·피로: symptom-integrated/sleep-fatigue.md",
"      - 자율신경·스트레스: symptom-integrated/autonomic-stress.md",
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe symptom-integrated nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-combination-search-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
