from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[
("영양제·건강기능식품과 한약","conditions/supplements-herbal-medicine.md"),
("천연제품·천연성분과 한약","conditions/natural-products-herbal.md"),
("홍삼·인삼과 한약","conditions/red-ginseng-herbal.md"),
("비타민·미네랄과 한약","conditions/vitamins-herbal.md"),
("오메가3·혈행 건기식과 한약","conditions/omega3-herbal.md"),
("유산균·프로바이오틱스와 한약","conditions/probiotics-herbal.md"),
("밀크시슬·간 영양제와 한약","conditions/liver-supplements-herbal.md"),
("허브·식물추출물·농축액과 한약","conditions/herbal-extract-products.md"),
("영양제 여러 개 복용·중복성분 점검","conditions/multi-supplement-review.md"),
("보약·영양제 무엇을 선택할까","conditions/tonic-supplement-choice.md"),
]
anchors=[
"      - 체기·소화불량과 두통: conditions/indigestion-headache.md",
"      - 운동 후 피로·회복지연: conditions/poor-recovery-after-exercise.md",
"      - 노인보약·어르신보약: conditions/elderly-tonic.md",
"      - 만성피로: conditions/chronic-fatigue.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe nav anchor not found")
missing=[x for x in items if x[1] not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml
        yaml.safe_load(new)
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; mkdocs.yml unchanged: {e}")
    Path("mkdocs.yml.before-supplement-natural-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
