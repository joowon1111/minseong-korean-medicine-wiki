from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("교통사고 후유증","conditions/traffic-accident-sequelae.md"),
("인후통·목감기","conditions/sore-throat.md"),
("부비동염·축농증","conditions/sinusitis.md"),
("소아 식욕부진","conditions/child-poor-appetite.md"),
("소아 잦은 감기·허약","conditions/child-recurrent-colds.md"),
("성장통·아이 다리통증","conditions/growing-pains.md"),
("생리전증후군·PMS","conditions/pms.md"),
("냉증·아랫배냉증","conditions/cold-sensitivity.md"),
("남성갱년기·남성 기력저하","conditions/male-menopause.md"),
("전립선·배뇨불편","conditions/prostate-urinary-symptoms.md"),
]
anchors=[
"      - 다이어트 한약·체중관리: conditions/weight-management-herbal.md",
"      - 암 치료 후 회복·기력저하: conditions/cancer-treatment-recovery.md",
"      - 산후회복: conditions/postpartum-recovery.md",
"      - 만성피로: conditions/chronic-fatigue.md"
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
    Path("mkdocs.yml.before-condition-expansion-10d.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
