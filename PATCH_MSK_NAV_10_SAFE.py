from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("오십견·어깨가 안 올라가요","conditions/frozen-shoulder.md"),
("회전근개 통증·팔 올릴 때 어깨통증","conditions/rotator-cuff-pain.md"),
("골프엘보·팔꿈치 안쪽 통증","conditions/golfer-elbow.md"),
("방아쇠수지·손가락 걸림","conditions/trigger-finger.md"),
("드퀘르벵·엄지쪽 손목통증","conditions/dequervain.md"),
("고관절·엉덩관절 통증","conditions/hip-pain.md"),
("엉치·둔부 통증","conditions/buttock-pain.md"),
("이상근증후군·엉치에서 다리저림","conditions/piriformis-syndrome.md"),
("종아리 쥐·다리경련","conditions/calf-cramp.md"),
("발저림·발바닥 저림","conditions/foot-numbness.md"),
]
anchors=[
"      - 운동 후 피로·회복지연: conditions/poor-recovery-after-exercise.md",
"      - 전립선·배뇨불편: conditions/prostate-urinary-symptoms.md",
"      - 손목통증: conditions/wrist-pain.md",
"      - 어깨통증: conditions/shoulder-pain.md"
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
    Path("mkdocs.yml.before-musculoskeletal-expansion-10.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
