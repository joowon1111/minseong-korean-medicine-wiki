from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("성인 식욕저하·입맛저하","conditions/poor-appetite-adult.md"),
("체중감소·살이 빠져요","conditions/unintentional-weight-loss.md"),
("노쇠·근감소·근력저하","conditions/frailty-sarcopenia.md"),
("감기·바이러스 감염 후 피로","conditions/post-viral-fatigue.md"),
("폐렴 후 회복·기력저하","conditions/pneumonia-recovery.md"),
("골절 후 회복·뼈 회복","conditions/fracture-recovery.md"),
("퇴원 후 회복·장기입원 후 기력저하","conditions/post-hospitalization-recovery.md"),
("빈혈·어지럼·피로","conditions/anemia-fatigue.md"),
("노인 불면·새벽각성","conditions/poor-sleep-elderly.md"),
("운동 후 피로·회복지연","conditions/poor-recovery-after-exercise.md"),
]
anchors=[
"      - 전립선·배뇨불편: conditions/prostate-urinary-symptoms.md",
"      - 다이어트 한약·체중관리: conditions/weight-management-herbal.md",
"      - 암 치료 후 회복·기력저하: conditions/cancer-treatment-recovery.md",
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
    Path("mkdocs.yml.before-condition-expansion-10e.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
