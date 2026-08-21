from pathlib import Path
p=Path("mkdocs.yml")
if not p.exists(): raise SystemExit("ERROR: mkdocs.yml not found")
orig=p.read_text(encoding="utf-8")
target="ai/search-priority-map.md"
if target in orig:
    print("NAV already contains search priority map")
    raise SystemExit(0)
anchors=[
"      - 근거와 출처를 따라가는 방법: ai/evidence-map.md",
"      - 환자 질문에서 시작하는 한의학 검색 지도: ai/patient-search-map.md",
"      - AI 검색엔진용 사이트 구조: ai-index.md"
]
anchor=next((x for x in anchors if x in orig),None)
if not anchor:
    print("NOTE: nav anchor not found; page still exists and can be linked internally.")
    raise SystemExit(0)
indent=anchor[:len(anchor)-len(anchor.lstrip())]
line=f"{indent}- 검색 우선순위와 핵심 허브: {target}"
new=orig.replace(anchor,anchor+"\n"+line,1)
try:
    import yaml; yaml.safe_load(new)
except Exception as e:
    raise SystemExit(f"ERROR: YAML validation failed; mkdocs.yml unchanged: {e}")
Path("mkdocs.yml.before-search-priority-nav.bak").write_text(orig,encoding="utf-8")
p.write_text(new,encoding="utf-8")
print("NAV ADDED")
