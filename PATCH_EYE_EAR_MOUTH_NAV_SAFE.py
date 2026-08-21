from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8"); t=orig
items=[('눈피로·안구피로', 'conditions/eye-fatigue.md'), ('눈떨림·눈꺼풀떨림', 'conditions/eye-twitching.md'), ('귀먹먹함·귀가 막힌 느낌', 'conditions/ear-fullness.md'), ('청력저하·소리가 잘 안 들려요', 'conditions/hearing-loss.md'), ('구내염·입안이 헐어요', 'conditions/mouth-ulcer.md'), ('입이 써요·쓴맛이 나요', 'conditions/bitter-taste.md'), ('입냄새·구취', 'conditions/bad-breath.md'), ('혀가 화끈거려요·구강작열감', 'conditions/tongue-burning.md'), ('목건조·목이 자꾸 말라요', 'conditions/dry-throat.md'), ('미각변화·맛이 이상해요', 'conditions/taste-change.md')]
anchors=[
"      - 소변 후 찔끔·배뇨후 요점적: conditions/post-void-dribble.md",
"      - 안구건조: conditions/dry-eye.md",
"      - 이명: conditions/tinnitus.md",
"      - 노인 입마름·구강건조: conditions/elderly-dry-mouth.md"
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
    Path("mkdocs.yml.before-eye-ear-mouth-expansion.bak").write_text(orig,encoding="utf-8")
    p.write_text(new,encoding="utf-8")
    print("ADDED NAV:",len(missing))
else: print("NAV already complete")
