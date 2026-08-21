from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('한약 식전·식후 언제 먹나요', 'conditions/herbal-before-after-meals.md'), ('한약 먹을 때 커피·카페인', 'conditions/herbal-with-coffee.md'), ('한약 먹을 때 음식·식이관리', 'conditions/herbal-with-food.md'), ('한약 보관방법·파우치 보관', 'conditions/herbal-storage.md'), ('한약 복용을 깜빡했어요', 'conditions/herbal-missed-dose.md'), ('한약 장기복용·꾸준히 먹어도 되나요', 'conditions/herbal-long-term.md'), ('한약 먹고 언제 효과를 평가하나요', 'conditions/herbal-followup.md'), ('한약 먹다가 증상이 바뀌면 처방도 바꾸나요', 'conditions/herbal-customization.md'), ('탕약·환약·농축제형 차이', 'conditions/herbal-pills-decoction.md'), ('한약 상담 전 무엇을 준비하나요', 'conditions/herbal-consultation-prep.md')]
anchors=[
"      - 보약·건기식·영양제 함께 선택하기: conditions/tonic-vs-health-supplement.md",
"      - 맞춤한약·체질과 증상에 맞춘 처방: conditions/custom-herbal-medicine.md",
"      - 보약 복용기간·한약 얼마나 먹나요: conditions/tonic-duration.md",
"      - 노인보약·어르신보약: conditions/elderly-tonic.md"
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
    Path("mkdocs.yml.before-herbal-question-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
