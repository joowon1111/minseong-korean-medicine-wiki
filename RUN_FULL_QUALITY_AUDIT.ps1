$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found. ZIP을 저장소 최상위에 풀어주세요."}
$code=@'
from pathlib import Path
import re,json
from collections import Counter,defaultdict
try:
 import yaml
except: yaml=None
D=Path("docs"); fs=list(D.rglob("*.md")); ex={p.relative_to(D).as_posix() for p in fs}
def fm(t):
 if not t.startswith("---"): return {}
 try:
  s=t.split("---",2)[1]
  return (yaml.safe_load(s) or {}) if yaml else {}
 except:return {}
incoming=Counter();broken=[];titles=defaultdict(list);descs=defaultdict(list);answers=[];thin=[];nofm=[];noh1=[];nocore=[]
texts={}
for p in fs:
 r=p.relative_to(D).as_posix();t=p.read_text(encoding="utf-8",errors="ignore");texts[r]=t;m=fm(t)
 if not m:nofm.append(r)
 if m.get("title"):titles[str(m["title"])].append(r)
 if m.get("description"):descs[str(m["description"])].append(r)
 if not re.search(r"(?m)^#\s+",t):noh1.append(r)
 if len(re.sub(r"\s+"," ",t))<650:thin.append(r)
 if r.startswith("answer-guides/"):
  answers.append(r)
  if "## 핵심 답변" not in t:nocore.append(r)
 for _,tar in re.findall(r"\[([^\]]+)\]\(([^)]+)\)",t):
  tar=tar.split("#")[0].split("?")[0].strip()
  if not tar or tar.startswith(("http://","https://","mailto:","#")):continue
  try:q=(p.parent/tar).resolve().relative_to(D.resolve()).as_posix()
  except:continue
  if q.endswith("/"):q+="index.md"
  if not q.endswith(".md"):q+=".md"
  if q in ex:incoming[q]+=1
  else:broken.append((r,tar,q))
nav=set()
if yaml and Path("mkdocs.yml").exists():
 try:
  cfg=yaml.safe_load(Path("mkdocs.yml").read_text(encoding="utf-8"))
  def walk(x):
   if isinstance(x,str) and x.endswith(".md"):nav.add(x)
   elif isinstance(x,list):
    for y in x:walk(y)
   elif isinstance(x,dict):
    for y in x.values():walk(y)
  walk(cfg.get("nav",[]))
 except:pass
orph=sorted(r for r in ex if incoming[r]==0 and r not in nav and not r.endswith("index.md"))
def tok(s):return set(re.findall(r"[가-힣A-Za-z0-9]{2,}",s.lower()))
ats={r:tok(str(fm(texts[r]).get("title",""))+" "+re.sub(r"---.*?---","",texts[r],flags=re.S)[:1600]) for r in answers}
sim=[]
for i,a in enumerate(sorted(answers)):
 for b in sorted(answers)[i+1:]:
  A,B=ats[a],ats[b]
  if A and B:
   j=len(A&B)/len(A|B)
   if j>=.48:sim.append((round(j,3),a,b))
sim.sort(reverse=True)
dupT={k:v for k,v in titles.items() if len(v)>1};dupD={k:v for k,v in descs.items() if len(v)>1}
out=Path("_quality_audit");out.mkdir(exist_ok=True)
data={"total_md":len(fs),"answer_guides":len(answers),"broken_links":broken,"not_in_nav":sorted(ex-nav),"orphans":orph,"no_frontmatter":nofm,"no_h1":noh1,"thin":thin,"no_core_answer":nocore,"duplicate_titles":dupT,"duplicate_descriptions":dupD,"similar_answer_guides":sim[:100]}
(out/"audit.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
with (out/"AUDIT_REPORT.md").open("w",encoding="utf-8") as f:
 f.write("# 민성 한의학 아카이브 전체 품질감사\n\n")
 f.write(f"- 전체 Markdown: **{len(fs)}**\n- answer-guides: **{len(answers)}**\n- 깨진 내부링크: **{len(broken)}**\n- nav 미등록: **{len(ex-nav)}**\n- 고아 페이지 후보: **{len(orph)}**\n- front matter 없음: **{len(nofm)}**\n- H1 없음: **{len(noh1)}**\n- 얇은 페이지 후보: **{len(thin)}**\n- 핵심답변 없는 answer-guide: **{len(nocore)}**\n- 유사 answer-guide 후보: **{len(sim)}**\n\n")
 def sec(h,x,limit=250):
  f.write("## "+h+"\n\n")
  if not x:f.write("- 없음\n\n");return
  for v in x[:limit]:f.write("- "+(" | ".join(map(str,v)) if isinstance(v,(list,tuple)) else str(v))+"\n")
  f.write("\n")
 sec("깨진 내부링크",broken);sec("고아 페이지 후보",orph);sec("nav 미등록 문서",sorted(ex-nav));sec("핵심답변 없는 answer-guide",nocore);sec("얇은 페이지 후보",thin);sec("유사 answer-guide 후보",sim)
 f.write("## 중복 title\n\n")
 for k,v in dupT.items():f.write(f"- **{k}**: {', '.join(v)}\n")
print("AUDIT COMPLETE",len(fs),len(answers),len(broken),len(orph),len(sim))
'@
Set-Content "_RUN_QUALITY_AUDIT.py" $code -Encoding UTF8
python "_RUN_QUALITY_AUDIT.py"
if($LASTEXITCODE -ne 0){throw "audit failed"}
Write-Host "AUDIT COMPLETE - open _quality_audit\AUDIT_REPORT.md" -ForegroundColor Green
Write-Host "Site content was NOT modified." -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
