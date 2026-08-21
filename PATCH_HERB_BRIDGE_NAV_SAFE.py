from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('피로·기력회복과 본초 찾기', 'herbal-integrated/herbs-for-fatigue.md'), ('소화·비위와 본초 찾기', 'herbal-integrated/herbs-for-digestion.md'), ('불면·심계와 본초 찾기', 'herbal-integrated/herbs-for-sleep.md'), ('감기·기침·비염과 본초 찾기', 'herbal-integrated/herbs-for-cold-cough.md'), ('통증·관절·근육과 본초 찾기', 'herbal-integrated/herbs-for-pain.md'), ('여성·월경·산후와 본초 찾기', 'herbal-integrated/herbs-for-women.md'), ('갱년기·냉열과 본초 찾기', 'herbal-integrated/herbs-for-menopause.md'), ('부종·수습과 본초 찾기', 'herbal-integrated/herbs-for-edema.md'), ('스트레스·기체와 본초 찾기', 'herbal-integrated/herbs-for-stress.md'), ('한약재는 왜 여러 가지를 함께 쓰나요', 'herbal-integrated/how-herbs-combine.md')]
anchors=[
"      - 같은 증상인데 한약 처방이 다른 이유: herbal-integrated/formula-selection-guide.md",
"      - 본초 찾기: herbal-integrated/herbs.md",
"      - 증상·치료로 찾기: herbal-integrated/by-symptom-treatment.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe herbal nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e: raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-herb-bridge-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
