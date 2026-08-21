from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('야간뇨·밤에 소변 때문에 깨요', 'conditions/nocturia.md'), ('소변줄기 약함·배뇨지연', 'conditions/weak-urine-stream.md'), ('잔뇨감·소변이 시원하지 않아요', 'conditions/residual-urine.md'), ('과민성방광·급하게 소변 마려움', 'conditions/overactive-bladder.md'), ('만성전립선염·만성골반통', 'conditions/chronic-prostatitis.md'), ('남성 골반저근 긴장·회음부 불편', 'conditions/pelvic-floor-tension-men.md'), ('발기력저하·남성 활력', 'conditions/erectile-difficulty.md'), ('남성 피로·기력보강 한약', 'conditions/male-fatigue-tonic.md'), ('긴장하면 소변이 자주 마려워요', 'conditions/urinary-frequency-stress.md'), ('소변 후 찔끔·배뇨후 요점적', 'conditions/post-void-dribble.md')]
anchors=[
"      - 건강한 체중관리·한방다이어트 상담: conditions/healthy-weight-management.md",
"      - 전립선·배뇨불편: conditions/prostate-urinary-symptoms.md",
"      - 남성갱년기·남성 기력저하: conditions/male-menopause.md",
"      - 빈뇨·야간뇨: conditions/frequent-urination.md"
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
    Path("mkdocs.yml.before-urology-mens-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
