from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('간수치가 높아요', 'conditions/elevated-liver-enzymes.md'), ('지방간·건강검진 지방간', 'conditions/fatty-liver.md'), ('공복혈당·당화혈색소 경계', 'conditions/prediabetes.md'), ('콜레스테롤·중성지방이 높아요', 'conditions/dyslipidemia.md'), ('건강검진 빈혈·헤모글로빈 저하', 'conditions/anemia-lab.md'), ('갑상선 수치 이상·TSH', 'conditions/thyroid-lab.md'), ('골밀도 저하·골감소증', 'conditions/low-bone-density.md'), ('염증수치·CRP·ESR 상승', 'conditions/inflammation-markers.md'), ('건강검진 위염·위내시경 소견', 'conditions/checkup-gastritis.md'), ('건강검진은 정상인데 피곤해요', 'conditions/normal-checkup-fatigue.md')]
anchors=[
"      - 보약·영양제 무엇을 선택할까: conditions/tonic-supplement-choice.md",
"      - 영양제·건강기능식품과 한약: conditions/supplements-herbal-medicine.md",
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
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; unchanged: {e}")
    Path("mkdocs.yml.before-health-checkup-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
