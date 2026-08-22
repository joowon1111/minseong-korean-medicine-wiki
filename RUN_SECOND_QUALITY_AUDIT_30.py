from pathlib import Path
import re, json, sys, datetime

ROOT=Path(__file__).resolve().parent
DOCS=ROOT/"docs"
OUT=ROOT/"_quality_audit_30"
OUT.mkdir(exist_ok=True)

if not DOCS.exists():
    print("ERROR: docs folder not found")
    input("Press Enter to close")
    sys.exit(1)

SKIP_PARTS={"_quality_audit","_quality_audit_30","assets","stylesheets","javascripts"}
priority_prefixes=("conditions/","herbs/","formulas/","pillar/","network/","formula-architecture/",
                   "sasang/","classics/","meridian-network/","acupoint-network/","clinical-core/",
                   "diagnostics/","research/","evidence-integrated/")

rows=[]
broken=[]
append_hits=[]
legacy_hits=[]
files=list(DOCS.rglob("*.md"))

link_re=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
heading_re=re.compile(r'(?m)^#{1,6}\s+(.+)$')
front_re=re.compile(r'^---\s*\n(.*?)\n---\s*\n',re.S)
legacy_words=[
    "대표 처방 몇 가지","대표 본초 몇 가지","간단히 정리","추후 보강","추가 예정",
    "확장 예정","TODO","TBD","placeholder","초안"
]
append_markers=[
    "EXPANSION_","_START -->","ACUPOINT_ATLAS_","MERIDIAN_EXPANSION_",
    "추가 확장","확장 보강"
]

for f in files:
    rel=f.relative_to(DOCS).as_posix()
    if any(x in f.parts for x in SKIP_PARTS): continue
    txt=f.read_text(encoding="utf-8",errors="ignore")
    fm=front_re.match(txt)
    body=txt[fm.end():] if fm else txt
    body_no_code=re.sub(r'```.*?```','',body,flags=re.S)
    words=len(re.findall(r'[가-힣A-Za-z0-9]+',body_no_code))
    chars=len(re.sub(r'\s+','',body_no_code))
    heads=len(heading_re.findall(body))
    links=link_re.findall(body)
    internal=0
    for href in links:
        href=href.strip()
        if href.startswith(("http://","https://","#","mailto:","tel:")): continue
        internal+=1
        target=href.split("#",1)[0].split("?",1)[0]
        if not target: continue
        dest=(f.parent/target).resolve()
        candidates=[dest]
        if dest.suffix=="":
            candidates += [Path(str(dest)+".md"),dest/"index.md"]
        elif dest.suffix==".md":
            pass
        if not any(x.exists() for x in candidates):
            broken.append((rel,href))
    fm_text=fm.group(1) if fm else ""
    has_title=bool(re.search(r'(?m)^title\s*:',fm_text))
    has_desc=bool(re.search(r'(?m)^description\s*:',fm_text))
    pri=rel.startswith(priority_prefixes)
    score=0
    reasons=[]
    if chars<500: score+=5; reasons.append("본문 매우 짧음")
    elif chars<900: score+=3; reasons.append("본문 짧음")
    elif chars<1400: score+=1; reasons.append("본문 보강 후보")
    if heads<3: score+=2; reasons.append("섹션 부족")
    if internal<2: score+=2; reasons.append("내부링크 부족")
    if not has_desc: score+=1; reasons.append("description 없음")
    if pri: score+=1
    lh=[w for w in legacy_words if w.lower() in txt.lower()]
    ah=[w for w in append_markers if w.lower() in txt.lower()]
    if lh:
        score+=3; reasons.append("초기/미완성 표현")
        legacy_hits.append((rel,", ".join(lh)))
    if ah:
        score+=2; reasons.append("과거 append 흔적")
        append_hits.append((rel,", ".join(ah)))
    rows.append((score,rel,chars,heads,internal,has_title,has_desc,"; ".join(reasons)))

rows.sort(key=lambda x:(-x[0],x[2],x[1]))
broken=sorted(set(broken))

def esc(s): return str(s).replace("|","\\|").replace("\n"," ")

report=[]
report.append("# 민성 한의학 아카이브 2차 전체 품질감사\n")
report.append(f"- 실행일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"- 검사 Markdown: **{len(rows)}개**")
report.append(f"- 깨진 상대링크 후보: **{len(broken)}개**")
report.append(f"- 현대화 우선후보(score ≥ 5): **{sum(1 for r in rows if r[0]>=5)}개**\n")
report.append("## 이번 감사의 기준\n")
report.append("초창기 문서와 최신 문서의 괴리감을 찾기 위해 **본문 충실도, 섹션 구조, 내부링크, 메타데이터, 미완성 표현, 과거 append 흔적**을 함께 봅니다. 단순히 짧다는 이유만으로 자동 수정하지 않고, 우선순위를 정한 뒤 기존 문서의 좋은 내용을 보존하면서 통합 재작성하는 것을 전제로 합니다.\n")
report.append("## A. 최우선 현대화 후보\n")
report.append("|순위|문서|점수|본문문자|섹션|내부링크|이유|")
report.append("|---:|---|---:|---:|---:|---:|---|")
for i,r in enumerate([x for x in rows if x[0]>=5][:80],1):
    score,rel,chars,heads,internal,ht,hd,reason=r
    report.append(f"|{i}|`{esc(rel)}`|{score}|{chars}|{heads}|{internal}|{esc(reason)}|")

report.append("\n## B. 중간 우선순위 후보\n")
report.append("|문서|점수|본문문자|섹션|내부링크|")
report.append("|---|---:|---:|---:|---:|")
for r in [x for x in rows if 3<=x[0]<5][:100]:
    report.append(f"|`{esc(r[1])}`|{r[0]}|{r[2]}|{r[3]}|{r[4]}|")

report.append("\n## C. 깨진 상대링크 후보\n")
if broken:
    for rel,href in broken[:200]: report.append(f"- `{esc(rel)}` → `{esc(href)}`")
else:
    report.append("- 발견되지 않음")

report.append("\n## D. 과거 append/확장 흔적\n")
if append_hits:
    for rel,hit in append_hits[:100]: report.append(f"- `{esc(rel)}` — {esc(hit)}")
else: report.append("- 발견되지 않음")

report.append("\n## E. 초기·미완성 표현 후보\n")
if legacy_hits:
    for rel,hit in legacy_hits[:100]: report.append(f"- `{esc(rel)}` — {esc(hit)}")
else: report.append("- 발견되지 않음")

report.append("\n## F. 다음 작업 원칙\n")
report.append("1. 점수가 높은 문서를 무조건 덮어쓰지 않고 실제 내용을 먼저 읽습니다.")
report.append("2. 기존 좋은 문단·출전·연구·링크를 보존합니다.")
report.append("3. 새 섹션을 맨 아래에 덧붙이는 방식 대신 기존 흐름 안에 통합합니다.")
report.append("4. 환자 진입 문서는 위험신호→감별→변증→치료→관련 본초·방제·경혈→현대근거 순서를 우선합니다.")
report.append("5. 전문 문서는 출전·구성·용량·전체 경혈/유주·연구 등 해당 분야에 필요한 깊이를 충분히 확보합니다.")
report.append("6. 한 번에 너무 많은 문서를 자동 교체하지 않고, 우선순위 묶음별로 실제 원문을 확인한 뒤 현대화합니다.\n")

(OUT/"AUDIT_REPORT_30.md").write_text("\n".join(report),encoding="utf-8-sig")
(OUT/"AUDIT_PROGRESS.txt").write_text(
    f"COMPLETE\nMarkdown files: {len(rows)}\nPriority candidates: {sum(1 for r in rows if r[0]>=5)}\nBroken links: {len(broken)}\n",
    encoding="utf-8-sig")
with (OUT/"AUDIT_RANKING.tsv").open("w",encoding="utf-8-sig") as o:
    o.write("score\tpath\tbody_chars\theadings\tinternal_links\thas_title\thas_description\treasons\n")
    for r in rows: o.write("\t".join(map(str,r))+"\n")

print("SECOND QUALITY AUDIT 30 COMPLETE")
print("Report: _quality_audit_30/AUDIT_REPORT_30.md")
print("Ranking: _quality_audit_30/AUDIT_RANKING.tsv")
print("Progress: _quality_audit_30/AUDIT_PROGRESS.txt")
print("Priority candidates:",sum(1 for r in rows if r[0]>=5))
print("Broken relative links:",len(broken))
input("Press Enter to close")
