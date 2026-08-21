from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('침치료 많이 아픈가요', 'conditions/acupuncture-pain-question.md'), ('침치료 얼마나 자주 받나요', 'conditions/acupuncture-frequency.md'), ('약침치료란 무엇인가요', 'conditions/pharmacopuncture-what-is.md'), ('약침은 아픈가요·치료 후 뻐근함', 'conditions/pharmacopuncture-pain.md'), ('약침치료 몇 번 받나요', 'conditions/pharmacopuncture-frequency.md'), ('전침치료란 무엇인가요', 'conditions/electroacupuncture-question.md'), ('부항치료란 무엇인가요·자국은 얼마나 가나요', 'conditions/cupping-question.md'), ('MPS·근막통증 치료란 무엇인가요', 'conditions/mps-treatment-question.md'), ('침치료와 한약을 같이 하나요', 'conditions/acupuncture-herbal-combination.md'), ('한의치료 효과는 무엇으로 확인하나요', 'conditions/treatment-response-evaluation.md')]
anchors=[
"      - 한약 상담 전 무엇을 준비하나요: conditions/herbal-consultation-prep.md",
"      - 근육이 뭉치고 딱딱해요: conditions/muscle-tightness.md",
"      - 요통: conditions/low-back-pain.md"
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
    Path("mkdocs.yml.before-acupuncture-question-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
