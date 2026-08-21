from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('스트레스성 피로·번아웃 느낌', 'conditions/stress-fatigue.md'), ('머리가 멍해요·브레인포그', 'conditions/brain-fog.md'), ('아침피로·자고 일어나도 피곤', 'conditions/morning-fatigue.md'), ('새벽각성·새벽에 자꾸 깨요', 'conditions/early-awakening.md'), ('숙면이 안돼요·수면회복감 저하', 'conditions/nonrestorative-sleep.md'), ('긴장하면 몸이 불편해요·신체화 증상', 'conditions/anxiety-somatic.md'), ('과호흡·숨이 답답하고 손발저림', 'conditions/hyperventilation.md'), ('스트레스성 목·어깨 뭉침', 'conditions/stress-neck-shoulder.md'), ('두근거림 + 소화불량·스트레스', 'conditions/stress-palpitations-digestion.md'), ('주말에 늘어지는 피로·회복부족', 'conditions/weekend-fatigue.md')]
anchors=[
"      - 아이 보약·소아 한약 언제 먹나요: conditions/child-parent-tonic-guide.md",
"      - 불면증·수면장애: conditions/insomnia.md",
"      - 두근거림·심계: conditions/palpitation.md",
"      - 만성피로: conditions/chronic-fatigue.md"
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
    Path("mkdocs.yml.before-stress-sleep-autonomic-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
