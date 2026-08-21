from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('만성기침·오래가는 기침', 'conditions/chronic-cough.md'), ('마른기침·목이 간질간질한 기침', 'conditions/dry-cough.md'), ('가래·목에 가래가 걸려요', 'conditions/phlegm.md'), ('코막힘·코로 숨쉬기 불편', 'conditions/nasal-congestion.md'), ('재채기·맑은콧물', 'conditions/sneezing-runny-nose.md'), ('쉰목소리·목소리가 안 나와요', 'conditions/hoarseness.md'), ('목이 자주 붓고 아파요', 'conditions/recurrent-sore-throat.md'), ('기관지염 후 기침·회복', 'conditions/bronchitis-recovery.md'), ('숨참·숨이 차요', 'conditions/shortness-of-breath.md'), ('성인 잦은 감기·반복 감기', 'conditions/frequent-colds-adult.md')]
anchors=[
"      - 대상포진·띠 모양 통증과 수포: conditions/shingles.md",
"      - 비염: conditions/rhinitis.md",
"      - 기침: conditions/cough.md",
"      - 감기: conditions/common-cold.md"
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
    Path("mkdocs.yml.before-respiratory-ent-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
