from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('두통·머리통증과 경혈 찾기', 'acupuncture-integrated/points-for-headache.md'), ('목·어깨 뭉침과 경혈 찾기', 'acupuncture-integrated/points-for-neck-shoulder.md'), ('허리통증·요통과 경혈 찾기', 'acupuncture-integrated/points-for-low-back.md'), ('소화불량·체기와 경혈 찾기', 'acupuncture-integrated/points-for-digestion.md'), ('불면·수면장애와 경혈 찾기', 'acupuncture-integrated/points-for-insomnia.md'), ('비염·코막힘과 경혈 찾기', 'acupuncture-integrated/points-for-rhinitis.md'), ('스트레스·자율신경 증상과 경혈 찾기', 'acupuncture-integrated/points-for-stress-autonomic.md'), ('여성·월경·갱년기와 경혈 찾기', 'acupuncture-integrated/points-for-womens-health.md'), ('빈뇨·야간뇨·배뇨불편과 경혈 찾기', 'acupuncture-integrated/points-for-urinary.md'), ('경혈은 왜 여러 곳을 함께 쓰나요', 'acupuncture-integrated/how-acupoints-combine.md')]
anchors=[
"      - 경혈·경락 찾기: acupuncture-integrated/points-meridians.md",
"      - 통증·증상으로 찾기: acupuncture-integrated/by-symptom.md",
"      - 근골격 통증 핵심: acupuncture-integrated/musculoskeletal.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe acupuncture-integrated nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e: raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-acupoint-bridge-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
