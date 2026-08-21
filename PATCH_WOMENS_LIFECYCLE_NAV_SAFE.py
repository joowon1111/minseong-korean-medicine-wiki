from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('생리양이 많아요·과다월경', 'conditions/heavy-menstruation.md'), ('생리양이 적어요·과소월경', 'conditions/scanty-menstruation.md'), ('무월경·생리가 안 나와요', 'conditions/amenorrhea.md'), ('다낭성난소증후군·PCOS', 'conditions/pcos.md'), ('배란통·배란기 아랫배통증', 'conditions/ovulation-pain.md'), ('임신준비 중 피로·냉증·소화저하', 'conditions/fertility-fatigue.md'), ('산후 땀·식은땀·냉증', 'conditions/postpartum-sweating.md'), ('산후 손목통증·육아 손목', 'conditions/postpartum-wrist-pain.md'), ('폐경이행기·생리주기 변화', 'conditions/perimenopause.md'), ('갱년기 관절통·몸이 쑤셔요', 'conditions/menopause-joint-pain.md')]
anchors=[
"      - 성인 잦은 감기·반복 감기: conditions/frequent-colds-adult.md",
"      - 여성한약·여성 건강: conditions/womens-herbal.md",
"      - 갱년기 한약·여성 갱년기: conditions/menopause-herbal.md",
"      - 산후회복: conditions/postpartum-recovery.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e: raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-womens-lifecycle-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
