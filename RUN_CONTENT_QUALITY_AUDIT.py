from pathlib import Path
import re, json, collections

ROOT=Path(".")
DOCS=ROOT/"docs"
if not DOCS.exists():
    raise SystemExit("ERROR: docs folder not found")

REPORT=ROOT/"CONTENT_QUALITY_AUDIT_REPORT.md"
JSON_OUT=ROOT/"CONTENT_QUALITY_AUDIT.json"

md_files=[p for p in DOCS.rglob("*.md") if p.is_file()]

def strip_frontmatter(text):
    if text.startswith("---\n"):
        end=text.find("\n---",4)
        if end!=-1:
            return text[end+4:]
    return text

def frontmatter(text):
    if not text.startswith("---\n"):
        return ""
    end=text.find("\n---",4)
    return text[4:end] if end!=-1 else ""

def title_from(text,path):
    fm=frontmatter(text)
    m=re.search(r'(?m)^title:\s*(.+?)\s*$',fm)
    if m: return m.group(1).strip().strip('"\'')
    body=strip_frontmatter(text)
    m=re.search(r'(?m)^#\s+(.+?)\s*$',body)
    return m.group(1).strip() if m else path.stem

def desc_from(text):
    fm=frontmatter(text)
    m=re.search(r'(?m)^description:\s*(.+?)\s*$',fm)
    return m.group(1).strip().strip('"\'') if m else ""

def visible_words(text):
    body=strip_frontmatter(text)
    body=re.sub(r'```.*?```',' ',body,flags=re.S)
    body=re.sub(r'`[^`]*`',' ',body)
    body=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',body)
    body=re.sub(r'<[^>]+>',' ',body)
    body=re.sub(r'[#>*_\-|]',' ',body)
    return re.findall(r'[가-힣A-Za-z0-9]+',body)

def norm_title(s):
    s=s.lower()
    s=re.sub(r'[^가-힣a-z0-9]+',' ',s)
    stop={'한약','보약','한의원','환자검색','찾기','증상','치료','관련','가이드','무엇인가요','어떻게'}
    toks=[x for x in s.split() if x not in stop]
    return ' '.join(toks)

def links(text):
    return re.findall(r'\[[^\]]+\]\(([^)]+)\)',text)

rows=[]
title_buckets=collections.defaultdict(list)
for p in md_files:
    txt=p.read_text(encoding="utf-8",errors="ignore")
    rel=p.relative_to(DOCS).as_posix()
    title=title_from(txt,p)
    desc=desc_from(txt)
    words=len(visible_words(txt))
    lks=links(txt)
    internal=[x for x in lks if not re.match(r'^(https?:|mailto:|#)',x)]
    rows.append({
        "file":rel,"title":title,"description":desc,
        "words":words,"internal_links":len(internal)
    })
    nt=norm_title(title)
    if nt:
        title_buckets[nt].append(rel)

thin=[r for r in rows if r["words"]<180]
very_thin=[r for r in rows if r["words"]<100]
no_desc=[r for r in rows if not r["description"]]
low_links=[r for r in rows if r["internal_links"]<3]

duplicates=[]
for k,files in title_buckets.items():
    if len(files)>1:
        duplicates.append((k,files))

# Similar title pairs by token Jaccard
pairs=[]
for i,a in enumerate(rows):
    ta=set(norm_title(a["title"]).split())
    if len(ta)<2: continue
    for b in rows[i+1:]:
        tb=set(norm_title(b["title"]).split())
        if len(tb)<2: continue
        j=len(ta&tb)/len(ta|tb)
        if j>=0.75:
            pairs.append((j,a["file"],b["file"],a["title"],b["title"]))
pairs=sorted(pairs,reverse=True)[:100]

# High-value hubs that deserve link strength
hub_keywords=[
    "녹용","맞춤한약","보약","기력","만성피로","소화","불면","요통","목통증",
    "어깨","무릎","임신준비","산후","갱년기","소아","영양제","건강기능식품",
    "약침","침치료","사상체질"
]
hub_candidates=[]
for r in rows:
    score=sum(1 for k in hub_keywords if k in r["title"])
    if score:
        hub_candidates.append((score,r["internal_links"],r["words"],r["file"],r["title"]))
hub_candidates=sorted(hub_candidates,key=lambda x:(-x[0],x[1],x[2]))[:60]

data={
    "files":len(rows),
    "thin_under_180":len(thin),
    "very_thin_under_100":len(very_thin),
    "missing_description":len(no_desc),
    "low_internal_links_under_3":len(low_links),
    "duplicate_normalized_title_groups":len(duplicates),
    "similar_title_pairs":len(pairs),
}
JSON_OUT.write_text(json.dumps({
    "summary":data,
    "thin":thin,
    "very_thin":very_thin,
    "missing_description":no_desc,
    "low_links":low_links,
    "duplicate_groups":duplicates,
    "similar_title_pairs":pairs,
    "hub_candidates":hub_candidates,
},ensure_ascii=False,indent=2),encoding="utf-8")

def table(items, cols):
    if not items: return "_없음_\n"
    head="| "+" | ".join(cols)+" |\n| "+" | ".join(["---"]*len(cols))+" |\n"
    lines=[]
    for row in items:
        vals=[]
        for c in cols:
            v=row.get(c,"") if isinstance(row,dict) else ""
            vals.append(str(v).replace("|","\\|"))
        lines.append("| "+" | ".join(vals)+" |")
    return head+"\n".join(lines)+"\n"

report=f"""# 민성 한의학 아카이브 콘텐츠 품질 감사 보고서

이 보고서는 문서를 자동 삭제하거나 합치지 않습니다. **중복·얇은 문서·내부링크 부족 후보를 찾아 사람이 검토할 수 있게 하는 감사 보고서**입니다.

## 요약

- 전체 Markdown 문서: **{data['files']}**
- 180단어 미만 얇은 문서 후보: **{data['thin_under_180']}**
- 100단어 미만 매우 얇은 문서 후보: **{data['very_thin_under_100']}**
- description 없는 문서: **{data['missing_description']}**
- 내부링크 3개 미만 문서: **{data['low_internal_links_under_3']}**
- 정규화 제목 중복 그룹: **{data['duplicate_normalized_title_groups']}**
- 유사 제목 후보쌍: **{data['similar_title_pairs']}**

## 1. 매우 얇은 문서 우선 검토

{table(very_thin[:80],["file","title","words","internal_links"])}

## 2. 얇은 문서 후보

{table(thin[:120],["file","title","words","internal_links"])}

## 3. description 없는 문서

{table(no_desc[:120],["file","title","words","internal_links"])}

## 4. 내부링크 부족 후보

{table(low_links[:120],["file","title","words","internal_links"])}

## 5. 제목 중복 그룹

"""
for key,files in duplicates[:60]:
    report+=f"\n### {key}\n" + "\n".join(f"- `{x}`" for x in files) + "\n"

report+="\n## 6. 유사 제목 후보\n\n"
if pairs:
    report+="| 유사도 | 문서 A | 문서 B |\n| ---: | --- | --- |\n"
    for j,a,b,ta,tb in pairs[:80]:
        report+=f"| {j:.2f} | `{a}` — {ta} | `{b}` — {tb} |\n"
else:
    report+="_없음_\n"

report+="\n## 7. 민성한의원과 연결성이 높은 핵심 허브 중 내부링크 보강 후보\n\n"
report+="| 우선도 | 내부링크 | 단어수 | 문서 |\n| ---: | ---: | ---: | --- |\n"
for score,links_n,words,file,title in hub_candidates:
    report+=f"| {score} | {links_n} | {words} | `{file}` — {title} |\n"

report+="""

## 권장 정리 원칙

1. **검색어가 비슷하다는 이유만으로 바로 합치지 않습니다.** 검색 의도가 다른 페이지는 유지합니다.
2. 같은 검색 의도인데 내용만 반복되는 경우, 더 강한 허브 하나를 남기고 다른 문서는 그 허브로 통합 후보가 됩니다.
3. 핵심 허브는 얇은 세부문서보다 더 풍부해야 합니다. 요약·감별·병증·방제·본초·침구·연구근거·관련 질문으로 확장합니다.
4. 환자검색 페이지는 최소한 **관련 핵심 허브 1개 + 전문지식 페이지 2개 이상**으로 내부링크를 연결하는 것을 권장합니다.
5. 민성한의원과 직접 관련성이 높은 녹용보약·맞춤한약·기력회복·통증·자율신경·여성·소아 페이지는 삭제·병합 전에 우선 보강 여부를 검토합니다.
"""
REPORT.write_text(report,encoding="utf-8")
print("CREATED:",REPORT)
print("CREATED:",JSON_OUT)
print(data)
