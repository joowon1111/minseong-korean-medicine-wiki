from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('아침에 몸이 뻣뻣해요·아침강직', 'conditions/morning-stiffness.md'), ('온몸이 쑤셔요·전신근육통', 'conditions/whole-body-ache.md'), ('근육이 뭉치고 딱딱해요', 'conditions/muscle-tightness.md'), ('등이 뻐근하고 결려요', 'conditions/back-stiffness.md'), ('날개뼈·견갑골 안쪽 통증', 'conditions/scapular-pain.md'), ('허벅지 통증·당김', 'conditions/thigh-pain.md'), ('햄스트링 당김·뒤허벅지 뻣뻣함', 'conditions/hamstring-tightness.md'), ('아킬레스건 통증·뒤꿈치 위 통증', 'conditions/achilles-pain.md'), ('발목이 자주 접질려요·만성 발목불안정', 'conditions/ankle-instability.md'), ('뒤꿈치 통증·걸을 때 발뒤꿈치 아픔', 'conditions/heel-pain.md')]
anchors=[
"      - 손발은 찬데 땀이 나요: conditions/cold-sweaty-hands.md",
"      - 오십견·어깨가 안 올라가요: conditions/frozen-shoulder.md",
"      - 발저림·발바닥 저림: conditions/foot-numbness.md",
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
    Path("mkdocs.yml.before-muscle-stiffness-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
