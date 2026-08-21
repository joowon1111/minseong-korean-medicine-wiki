from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('아이 배아픔·소아 복통', 'conditions/child-abdominal-pain.md'), ('소아 변비·아이 딱딱한변', 'conditions/child-constipation.md'), ('소아 설사·묽은변', 'conditions/child-diarrhea.md'), ('아이 잠·소아 수면', 'conditions/child-sleep.md'), ('아이 식은땀·잘 때 땀', 'conditions/child-night-sweats.md'), ('소아 두통·아이 머리아픔', 'conditions/child-headache.md'), ('아이 피로·기력저하', 'conditions/child-fatigue.md'), ('소아 멀미·차만 타면 울렁거림', 'conditions/child-motion-sickness.md'), ('아이 손발냉증·추위를 많이 타요', 'conditions/child-cold-hands-feet.md'), ('아이 보약·소아 한약 언제 먹나요', 'conditions/child-parent-tonic-guide.md')]
anchors=[
"      - 갱년기 관절통·몸이 쑤셔요: conditions/menopause-joint-pain.md",
"      - 소아 비염·아이 비염: conditions/child-rhinitis.md",
"      - 소아 식욕부진: conditions/child-poor-appetite.md",
"      - 성장기·아이 키 성장: conditions/child-growth.md"
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
    Path("mkdocs.yml.before-pediatric-parent-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
