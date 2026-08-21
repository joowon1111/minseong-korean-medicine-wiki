from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[
("기능성소화불량","conditions/functional-dyspepsia.md"),
("위염·속쓰림·명치통증","conditions/gastritis-symptoms.md"),
("트림·잦은 트림","conditions/belching.md"),
("속쓰림·가슴쓰림","conditions/heartburn.md"),
("장내가스·방귀가 많아요","conditions/abdominal-gas.md"),
("묽은변·무른변","conditions/loose-stool.md"),
("딱딱한변·배변곤란","conditions/constipation-hard-stool.md"),
("스트레스성 위장증상","conditions/stress-gut.md"),
("아침설사·식후설사","conditions/morning-diarrhea.md"),
("체기·소화불량과 두통","conditions/indigestion-headache.md"),
]
anchors=[
"      - 대상포진 후 신경통: conditions/postherpetic-neuralgia.md",
"      - 복통: conditions/abdominal-pain.md",
"      - 소화불량: conditions/dyspepsia.md"
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
    Path("mkdocs.yml.before-digestive-expansion-10.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
