from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('복부비만·뱃살', 'conditions/abdominal-obesity.md'), ('과식·폭식·식욕조절', 'conditions/overeating-binge.md'), ('야식·밤에 배고픔', 'conditions/night-eating.md'), ('식후 졸림·밥 먹으면 피곤', 'conditions/postmeal-sleepiness.md'), ('다이어트 정체기·체중이 안 빠져요', 'conditions/weight-plateau.md'), ('요요·다이어트 후 체중증가', 'conditions/weight-regain.md'), ('부종·붓기와 체중변화', 'conditions/edema-weight.md'), ('대사증후군·건강검진 체중관리', 'conditions/metabolic-syndrome.md'), ('중년 체중증가·나잇살', 'conditions/middle-age-weight.md'), ('건강한 체중관리·한방다이어트 상담', 'conditions/healthy-weight-management.md')]
anchors=[
"      - 주말에 늘어지는 피로·회복부족: conditions/weekend-fatigue.md",
"      - 다이어트 한약·체중관리: conditions/weight-management-herbal.md",
"      - 공복혈당·당화혈색소 경계: conditions/prediabetes.md"
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
    Path("mkdocs.yml.before-metabolic-lifestyle-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
