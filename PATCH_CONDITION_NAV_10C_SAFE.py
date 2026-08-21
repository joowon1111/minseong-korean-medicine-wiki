from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
t=orig
items=[
("불면증·수면장애","conditions/insomnia.md"),
("두근거림·심계","conditions/palpitation.md"),
("손발냉증","conditions/cold-hands-feet.md"),
("상열감·안면홍조","conditions/hot-flush.md"),
("목이물감·매핵기","conditions/globus.md"),
("가슴답답함","conditions/chest-tightness.md"),
("빈뇨·야간뇨","conditions/frequent-urination.md"),
("골반·회음부 통증","conditions/pelvic-pain.md"),
("습진·가려움","conditions/eczema.md"),
("후비루·목뒤로 넘어가는 콧물","conditions/postnasal-drip.md"),
]
anchors=[
"      - 손목통증: conditions/wrist-pain.md",
"      - 손저림·손목터널증후군: conditions/carpal-tunnel.md",
"      - 산후회복: conditions/postpartum-recovery.md",
"      - 갱년기: conditions/menopause.md"
]
anchor=next((a for a in anchors if a in t),None)
if not anchor: raise SystemExit("ERROR: safe condition nav anchor not found")
missing=[(a,b) for a,b in items if b not in t]
if missing:
    addition="\n".join(f"      - {a}: {b}" for a,b in missing)
    new=t.replace(anchor,anchor+"\n"+addition,1)
    try:
        import yaml
        yaml.safe_load(new)
    except Exception as e:
        raise SystemExit(f"ERROR: YAML validation failed; mkdocs.yml unchanged: {e}")
    Path("mkdocs.yml.before-condition-expansion-10c.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else:
    print("NAV already complete")
