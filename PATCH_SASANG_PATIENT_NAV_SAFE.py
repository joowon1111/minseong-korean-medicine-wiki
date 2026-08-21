from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('사상의학·사상체질은 무엇인가요', 'sasang/sasang-intro-patient.md'), ('사상체질과 소화·비위 증상', 'sasang/sasang-digestion.md'), ('사상체질과 피로·기력', 'sasang/sasang-fatigue.md'), ('사상체질과 땀·발한', 'sasang/sasang-sweat.md'), ('사상체질과 추위·더위·냉열', 'sasang/sasang-cold-heat.md'), ('사상체질과 불면·수면', 'sasang/sasang-sleep.md'), ('사상체질과 체중·다이어트', 'sasang/sasang-weight.md'), ('사상체질과 비염·감기', 'sasang/sasang-rhinitis.md'), ('사상체질 처방은 어떻게 고르나요', 'sasang/sasang-formula-guide.md'), ("사상체질과 일반적인 '체질' 표현의 차이", 'sasang/sasang-vs-constitution.md')]
anchors=[
"      - 사상의학: sasang/index.md",
"    - 사상의학: sasang/index.md",
"  - 사상의학: sasang/index.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: sasang nav anchor not found")
indent=anchor[:len(anchor)-len(anchor.lstrip())]
child_indent=indent+"  "
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"{child_indent}- {a}: {b}" for a,b in missing)
    # Convert scalar nav item into a parent with index + children.
    label=anchor.strip()[2:].split(":",1)[0]
    replacement=f"{indent}- {label}:\n{child_indent}- 개요: sasang/index.md\n"+addition
    new=t.replace(anchor,replacement,1)
    try:
        import yaml; yaml.safe_load(new)
    except Exception as e: raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-sasang-patient-bridge.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED SASANG NAV:",len(missing))
else: print("SASANG NAV already complete")
