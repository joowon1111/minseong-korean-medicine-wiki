from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('피로·기력저하에 쓰는 한약 처방 찾기', 'herbal-integrated/formula-for-fatigue.md'), ('소화불량·더부룩함 한약 처방 찾기', 'herbal-integrated/formula-for-digestion.md'), ('감기·기침 한약 처방 찾기', 'herbal-integrated/formula-for-cold-cough.md'), ('불면·두근거림 한약 처방 찾기', 'herbal-integrated/formula-for-insomnia.md'), ('두통·어지럼 한약 처방 찾기', 'herbal-integrated/formula-for-headache.md'), ('여성·월경·산후 한약 처방 찾기', 'herbal-integrated/formula-for-women.md'), ('근골격 통증 한약 처방 찾기', 'herbal-integrated/formula-for-pain.md'), ('비염·코막힘 한약 처방 찾기', 'herbal-integrated/formula-for-rhinitis.md'), ('갱년기·상열감 한약 처방 찾기', 'herbal-integrated/formula-for-menopause.md'), ('같은 증상인데 한약 처방이 다른 이유', 'herbal-integrated/formula-selection-guide.md')]
anchors=[
"      - 건강보험 한약제제: herbal-integrated/insurance-herbal.md",
"      - 증상·치료로 찾기: herbal-integrated/by-symptom-treatment.md",
"      - 보익·회복 핵심: herbal-integrated/tonic-recovery.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe herbal-integrated nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e: raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-herbal-formula-language-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
