from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('보약은 언제 먹나요·보약이 필요한 때', 'conditions/when-to-take-tonic.md'), ('보약 복용기간·한약 얼마나 먹나요', 'conditions/tonic-duration.md'), ('봄·여름·가을·겨울 보약', 'conditions/tonic-season.md'), ('연령별 보약·가족 보약', 'conditions/tonic-age.md'), ('녹용보약이 궁금해요', 'conditions/deer-antler-tonic-guide.md'), ('공진단은 언제 찾나요', 'conditions/gongjin-dan-guide.md'), ('경옥고는 언제 찾나요', 'conditions/gyeongokgo-guide.md'), ('맞춤한약·체질과 증상에 맞춘 처방', 'conditions/custom-herbal-medicine.md'), ('건강검진 후 한약·보약 상담', 'conditions/herbal-medicine-after-checkup.md'), ('보약·건기식·영양제 함께 선택하기', 'conditions/tonic-vs-health-supplement.md')]
anchors=[
"      - 뒤꿈치 통증·걸을 때 발뒤꿈치 아픔: conditions/heel-pain.md",
"      - 노인보약·어르신보약: conditions/elderly-tonic.md",
"      - 영양제·건강기능식품과 한약: conditions/supplements-herbal-medicine.md"
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
    Path("mkdocs.yml.before-tonic-intent-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
