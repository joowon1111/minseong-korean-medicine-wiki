from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("긴장형두통·뒷목두통","conditions/tension-headache.md"),
("편두통","conditions/migraine.md"),
("경추성두통·목에서 올라오는 두통","conditions/cervicogenic-headache.md"),
("후두신경통·뒤통수 찌릿통증","conditions/occipital-neuralgia.md"),
("안면통증·얼굴통증","conditions/facial-pain.md"),
("삼차신경통·얼굴 전기통증","conditions/trigeminal-neuralgia.md"),
("이갈이·이악물기·턱근육 긴장","conditions/jaw-clenching-bruxism.md"),
("팔저림·손까지 내려가는 저림","conditions/arm-numbness.md"),
("목·어깨·팔저림과 흉곽출구 증상","conditions/thoracic-outlet-symptoms.md"),
("대상포진 후 신경통","conditions/postherpetic-neuralgia.md"),
]
anchors=[
"      - 발저림·발바닥 저림: conditions/foot-numbness.md",
"      - 운동 후 피로·회복지연: conditions/poor-recovery-after-exercise.md",
"      - 두통: conditions/headache.md",
"      - 목통증: conditions/neck-pain.md"
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
    Path("mkdocs.yml.before-head-neck-neuro-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
