from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('오래 앉으면 허리가 아파요', 'conditions/low-back-pain-sitting.md'), ('운전하면 목·허리가 아파요', 'conditions/driving-neck-back-pain.md'), ('컴퓨터 하면 목·어깨가 뭉쳐요', 'conditions/computer-neck-shoulder.md'), ('스마트폰 보면 목이 아파요', 'conditions/smartphone-neck-pain.md'), ('오래 서 있으면 허리·다리가 아파요', 'conditions/standing-leg-back-pain.md'), ('계단 오르내릴 때 무릎이 아파요', 'conditions/stairs-knee-pain.md'), ('쪼그려 앉을 때 무릎이 아파요', 'conditions/squatting-knee-pain.md'), ('팔을 위로 들면 어깨가 아파요', 'conditions/overhead-shoulder-pain.md'), ('자다가 팔·손이 저려요', 'conditions/night-arm-numbness.md'), ('아침 첫발이 아파요', 'conditions/morning-first-step-foot-pain.md')]
anchors=[
"      - 경혈은 왜 여러 곳을 함께 쓰나요: acupuncture-integrated/how-acupoints-combine.md",
"      - 뒤꿈치 통증·걸을 때 발뒤꿈치 아픔: conditions/heel-pain.md",
"      - 요통: conditions/low-back-pain.md"
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
    Path("mkdocs.yml.before-daily-activity-pain-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
