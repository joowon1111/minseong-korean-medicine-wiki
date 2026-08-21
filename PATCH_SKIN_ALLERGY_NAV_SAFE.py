from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[
("두드러기·반복되는 가려움","conditions/urticaria.md"),
("아토피피부염·만성 가려움","conditions/atopic-dermatitis.md"),
("여드름·성인여드름","conditions/acne.md"),
("지루성피부염·두피 가려움","conditions/seborrheic-dermatitis.md"),
("손습진·주부습진","conditions/eczema-hands.md"),
("한포진·손발 물집","conditions/dyshidrotic-eczema.md"),
("피부 가려움·원인 모를 소양감","conditions/pruritus.md"),
("알레르기 피부반응·민감성 피부","conditions/allergic-skin.md"),
("건조피부·피부 당김","conditions/dry-skin.md"),
("대상포진·띠 모양 통증과 수포","conditions/shingles.md"),
]
anchors=[
"      - 건강검진은 정상인데 피곤해요: conditions/normal-checkup-fatigue.md",
"      - 습진·가려움: conditions/eczema.md",
"      - 비염: conditions/rhinitis.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-skin-allergy-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
