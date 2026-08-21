from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('발이 차고 시려요·말초냉감', 'conditions/cold-feet-circulation.md'), ('다리가 무겁고 피곤해요', 'conditions/leg-heaviness.md'), ('저녁 다리부종·발목붓기', 'conditions/leg-swelling-evening.md'), ('일어설 때 어지럼·기립성 증상', 'conditions/orthostatic-dizziness.md'), ('저혈압 느낌·기운없고 어지럼', 'conditions/low-blood-pressure-symptoms.md'), ('혈압이 높아요·건강검진 고혈압', 'conditions/high-blood-pressure-checkup.md'), ('혈액순환이 안 되는 느낌', 'conditions/poor-circulation-sensation.md'), ('멍이 잘 들어요', 'conditions/easy-bruising.md'), ('추우면 몸이 쑤셔요·냉통', 'conditions/cold-weather-body-ache.md'), ('손발은 찬데 땀이 나요', 'conditions/cold-sweaty-hands.md')]
anchors=[
"      - 미각변화·맛이 이상해요: conditions/taste-change.md",
"      - 손발냉증: conditions/cold-hands-feet.md",
"      - 부종: conditions/edema.md",
"      - 어지럼: conditions/dizziness.md"
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
    Path("mkdocs.yml.before-circulation-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
