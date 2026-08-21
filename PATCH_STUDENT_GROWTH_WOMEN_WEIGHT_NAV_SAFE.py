from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("수험생 집중력·학습피로","conditions/student-concentration.md"),
("수험생 체력·기력회복","conditions/student-stamina.md"),
("성장기·아이 키 성장","conditions/child-growth.md"),
("소아 코피·반복 코피","conditions/child-nosebleed.md"),
("소아 비염·아이 비염","conditions/child-rhinitis.md"),
("임신준비 한약·가임기 건강","conditions/preconception-herbal.md"),
("출산 후 한약·산후보약","conditions/postpartum-herbal.md"),
("갱년기 한약·여성 갱년기","conditions/menopause-herbal.md"),
("여성한약·여성 건강","conditions/womens-herbal.md"),
("다이어트 한약·체중관리","conditions/weight-management-herbal.md"),
]
anchors=[
"      - 암 치료 후 회복·기력저하: conditions/cancer-treatment-recovery.md",
"      - 노인보약·어르신보약: conditions/elderly-tonic.md",
"      - 산후회복: conditions/postpartum-recovery.md",
"      - 갱년기: conditions/menopause.md"
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
    Path("mkdocs.yml.before-student-growth-women-weight.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
