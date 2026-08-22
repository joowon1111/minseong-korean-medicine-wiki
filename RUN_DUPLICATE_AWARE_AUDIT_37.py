from pathlib import Path
import re, csv
ROOT=Path(__file__).resolve().parent
DOCS=ROOT/"docs"
OUT=ROOT/"_quality_audit_37"
OUT.mkdir(exist_ok=True)
rows=[]
for f in DOCS.rglob("*.md"):
    rel=f.relative_to(DOCS).as_posix()
    txt=f.read_text(encoding="utf-8",errors="ignore")
    body=re.sub(r'(?s)^---\s*.*?\s*---\s*','',txt)
    chars=len(re.sub(r'\s+','',body))
    heads=len(re.findall(r'(?m)^#{1,6}\s+',body))
    links=len(re.findall(r'\[[^\]]+\]\((?!https?://|#)([^)]+)\)',body))
    kind="content"
    if rel.startswith("templates/"): kind="template"
    elif rel.endswith("/references.md") or rel=="references.md": kind="references"
    elif re.search(r'(?m)^status\s*:\s*canonical-bridge\s*$',txt): kind="bridge"
    score=0; reasons=[]
    if kind=="content":
        if chars<500: score+=5;reasons.append("very short")
        elif chars<900: score+=3;reasons.append("short")
        if heads<3: score+=2;reasons.append("few sections")
        if links<2: score+=2;reasons.append("few links")
    rows.append((score,kind,rel,chars,heads,links,"; ".join(reasons)))
rows.sort(key=lambda x:(-x[0],x[2]))
with (OUT/"AUDIT_RANKING_37.tsv").open("w",encoding="utf-8-sig",newline="") as o:
    w=csv.writer(o,delimiter="\t");w.writerow(["score","kind","path","body_chars","headings","internal_links","reasons"]);w.writerows(rows)
priority=[x for x in rows if x[0]>=5 and x[1]=="content"]
report=["# Quality Audit 37 — duplicate-aware","",f"- Markdown: **{len(rows)}**",f"- True content priority candidates: **{len(priority)}**",f"- Bridge/template/reference pages excluded from ordinary length scoring: **{sum(1 for x in rows if x[1]!='content')}**","","## Top true-content candidates",""]
for x in priority[:100]: report.append(f"- `{x[2]}` — score {x[0]}, {x[3]} chars, {x[6]}")
(OUT/"AUDIT_REPORT_37.md").write_text("\n".join(report),encoding="utf-8-sig")
print("DUPLICATE-AWARE QUALITY AUDIT 37 COMPLETE")
print("Report: _quality_audit_37/AUDIT_REPORT_37.md")
print("Ranking: _quality_audit_37/AUDIT_RANKING_37.tsv")
input("Press Enter to close")
