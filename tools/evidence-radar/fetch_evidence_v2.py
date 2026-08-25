#!/usr/bin/env python3
"""
Minseong Evidence Radar v0.2

Improvements from live 156 test:
- relevance filtering so journal-title matches do not dominate results
- study type inference from title + keywords
- treatment type inference
- expanded KCD candidate mapping
- priority scoring
- archive link candidates
- better PICO fallback from title/keywords when API PICO is empty
- review Markdown grouped by priority

This remains READ-ONLY:
API fetch -> local JSON/Markdown only.
"""

import argparse, json, re, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

BASE="https://med.symbolicinfo.com"

def get_json(path, params):
    url=BASE+path+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":"Minseong-Evidence-Radar/0.2"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def pick(obj,*keys,default=""):
    if not isinstance(obj,dict):
        return default
    for k in keys:
        v=obj.get(k)
        if v not in (None,"",[],{}):
            return v
    return default

def flatten_text(v):
    if isinstance(v,str): return v
    if isinstance(v,list): return " ".join(flatten_text(x) for x in v)
    if isinstance(v,dict): return " ".join(flatten_text(x) for x in v.values())
    return str(v or "")

def norm(s):
    return re.sub(r"\s+"," ",str(s or "")).strip()

def infer_study_type(title,keywords):
    text=(title+" "+flatten_text(keywords)).lower()
    rules=[
      ("Systematic review & meta-analysis",["systematic review","meta-analysis","메타분석","체계적 문헌고찰"]),
      ("Scoping review",["scoping review","범위 검토"]),
      ("Systematic review protocol",["systematic review protocol"]),
      ("RCT protocol",["randomized controlled trial","study protocol","protocol for","무작위 대조 시험"]),
      ("RCT",["randomized controlled trial","randomised controlled trial","randomized","무작위 대조"]),
      ("Case report",["case report","case study","증례","사례 보고"]),
      ("Cross-sectional study",["cross-sectional","단면 연구"]),
      ("Survey",["survey","실태조사","panel"]),
      ("Observational review",["observational studies","prevalence"]),
      ("Pilot study",["pilot study","pilot trial"]),
    ]
    for label,terms in rules:
        if any(x in text for x in terms):
            if label=="RCT protocol" and "protocol" not in text: continue
            if label=="RCT" and "protocol" in text: continue
            return label
    return "Other human study"

def infer_treatments(title,keywords):
    text=(title+" "+flatten_text(keywords)).lower()
    out=[]
    rules=[
      ("pharmacopuncture",["pharmacopuncture","pharmacoacupuncture","약침","봉독약침","bee venom injection","봉침"]),
      ("ultrasound-guided",["ultrasound-guided","ultrasound guided","초음파 유도"]),
      ("acupuncture",["acupuncture","침(鍼","침 치료","피내침"]),
      ("electroacupuncture",["electroacupuncture","전침"]),
      ("cupping",["cupping","부항"]),
      ("herbal medicine",["herbal medicine","herbal decoction","한약","탕약","-tang","탕("]),
      ("moxibustion",["moxibustion","뜸"]),
      ("chuna/manual",["chuna","tuina","manual therapy","추나"]),
    ]
    for label,terms in rules:
        if any(x in text for x in terms): out.append(label)
    return list(dict.fromkeys(out))

def query_relevance(query,title,journal,keywords,treatments):
    q=query.lower().strip()
    text_title=title.lower()
    text_kw=flatten_text(keywords).lower()
    text_j=journal.lower()

    aliases={
      "pharmacopuncture":["pharmacopuncture","pharmacoacupuncture","약침","봉독약침","bee venom injection","봉침"],
      "acupuncture":["acupuncture","침 치료","침(鍼","전침","electroacupuncture"],
      "herbal medicine":["herbal medicine","herbal decoction","한약","탕약"],
    }
    terms=aliases.get(q,[q])
    title_hit=any(t in text_title for t in terms)
    kw_hit=any(t in text_kw for t in terms)
    treatment_hit=(q in treatments) or (q=="pharmacopuncture" and "pharmacopuncture" in treatments)
    journal_only=(any(t in text_j for t in terms) and not (title_hit or kw_hit or treatment_hit))

    score=0
    if title_hit: score+=5
    if kw_hit: score+=4
    if treatment_hit: score+=4
    if journal_only: score-=6

    return score, not journal_only and score>0

def classify_kcd(text):
    t=text.lower()
    rules=[
      (["carpal tunnel","손목터널"],"G56.0","손목터널증후군","conditions/carpal-tunnel-syndrome/"),
      (["common peroneal nerve entrapment","총비골신경 포착"],"G57.3","총비골신경 포착","nerve-entrapment/common-peroneal-entrapment/"),
      (["lumbar disc herniation","요추 추간판 탈출"],"M51.1","요추 추간판탈출증","conditions/lumbar-disc-herniation/"),
      (["low back pain","lumbar pain","요통"],"M54","요통","conditions/low-back-pain/"),
      (["lateral epicondylitis","외측 상과염"],"M77.1","외측상과염","conditions/lateral-epicondylitis/"),
      (["frozen shoulder","adhesive capsulitis","오십견"],"M75.0","유착성 관절낭염","conditions/frozen-shoulder/"),
      (["knee osteoarthritis"],"M17","무릎 골관절염","conditions/knee-osteoarthritis/"),
      (["insomnia","불면"],"G47","불면","conditions/insomnia/"),
      (["allergic rhinitis","알레르기 비염"],"J30","알레르기비염","conditions/allergic-rhinitis/"),
      (["migraine","편두통"],"G43","편두통","conditions/migraine/"),
      (["functional dyspepsia"],"K30","기능성소화불량","conditions/functional-dyspepsia/"),
      (["crohn","크론병"],"K50","크론병","conditions/crohns-disease/"),
      (["atopic dermatitis","아토피"],"L20","아토피피부염","conditions/atopic-dermatitis/"),
      (["dry eye","안구건조"],"H04.1","안구건조","conditions/dry-eye/"),
      (["alopecia areata","원형탈모"],"L63","원형탈모증","conditions/alopecia-areata/"),
      (["postherpetic neuralgia","대상포진 후 신경통"],"G53.0","대상포진후신경통","conditions/postherpetic-neuralgia/"),
      (["prostatitis","chronic pelvic pain syndrome"],"N41","만성전립선염/CPPS","conditions/chronic-prostatitis-cpps/"),
    ]
    out=[]
    for terms,c,label,url in rules:
        if any(x in t for x in terms):
            out.append({"code":c,"label":label,"status":"candidate","archive_path":url})
    return out

def infer_pico(title,keywords,study_type):
    text=title+" "+flatten_text(keywords)
    low=text.lower()

    population=""
    condition_terms=[
      ("근골격계 질환","musculoskeletal"),
      ("외측상과염","lateral epicondylitis"),
      ("요추 추간판탈출증","lumbar disc herniation"),
      ("손목터널증후군","carpal tunnel"),
      ("알레르기비염","allergic rhinitis"),
      ("불면","insomnia"),
      ("편두통","migraine"),
      ("아토피피부염","atopic dermatitis"),
      ("안구건조","dry eye"),
      ("크론병","crohn"),
      ("원형탈모증","alopecia areata"),
    ]
    for ko,en in condition_terms:
        if en in low or ko in text:
            population=ko+" 환자/대상"
            break

    treatments=infer_treatments(title,keywords)
    intervention=", ".join(treatments)

    comparator=""
    if "placebo" in low: comparator="placebo"
    elif "usual care" in low: comparator="usual care"
    elif "comparison" in low or "compared" in low: comparator="active comparator"
    elif "case report" in study_type.lower(): comparator="해당 없음"

    outcomes=[]
    out_terms=[
      ("통증","pain"),("기능","function"),("삶의 질","quality of life"),
      ("수면","sleep"),("안전성","safety"),("이상반응","adverse"),
      ("OSDI","osdi"),("Schirmer test","schirmer"),("CDAI","cdai")
    ]
    for label,key in out_terms:
        if key in low: outcomes.append(label)

    return {
      "population":population,
      "intervention":intervention,
      "comparator":comparator,
      "outcomes":outcomes
    }

def priority_score(study_type,relevance,kcd,treatments):
    s=relevance
    if "Systematic review & meta-analysis"==study_type: s+=8
    elif "Scoping review"==study_type: s+=5
    elif study_type=="RCT": s+=7
    elif study_type=="RCT protocol": s+=2
    elif study_type=="Case report": s+=1
    if kcd: s+=3
    if "ultrasound-guided" in treatments: s+=2
    if "pharmacopuncture" in treatments: s+=2
    return s

def archive_candidates(kcd,treatments):
    links=[]
    for x in kcd:
        if x.get("archive_path"): links.append("/"+x["archive_path"])
    if "pharmacopuncture" in treatments: links += ["/portal/acupuncture/"]
    if "ultrasound-guided" in treatments: links += ["/musculoskeletal-ultrasound/","/musculoskeletal-ultrasound/ultrasound-guided-treatment/"]
    if any(x["code"]=="G57.3" for x in kcd): links += ["/nerve-entrapment/common-peroneal-entrapment/"]
    return list(dict.fromkeys(links))

def normalize(a,query):
    title=norm(pick(a,"title","article_title"))
    journal=norm(pick(a,"journal","journal_name"))
    keywords=pick(a,"keywords",default=[])
    analysis=pick(a,"analysis","article_analysis",default={})
    if not isinstance(analysis,dict): analysis={}
    raw_pico=pick(analysis,"pico",default={})
    if not isinstance(raw_pico,dict): raw_pico={}
    study_type=norm(pick(analysis,"category","study_type","research_type")) or infer_study_type(title,keywords)
    treatments=infer_treatments(title,keywords)
    relevance,keep=query_relevance(query,title,journal,keywords,treatments)
    blob=" ".join([title,flatten_text(keywords),flatten_text(analysis)])
    kcd=classify_kcd(blob)

    pico={
      "population":pick(raw_pico,"population","P"),
      "intervention":pick(raw_pico,"intervention","I"),
      "comparator":pick(raw_pico,"comparator","C"),
      "outcomes":pick(raw_pico,"outcome","outcomes","O",default=[]),
    }
    if not any([pico["population"],pico["intervention"],pico["comparator"],pico["outcomes"]]):
        pico=infer_pico(title,keywords,study_type)

    score=priority_score(study_type,relevance,kcd,treatments)

    return {
      "title":title,
      "published_date":pick(a,"published_date","publication_date","pub_date"),
      "journal":journal,
      "pmid":pick(a,"pmid"),
      "doi":pick(a,"doi"),
      "study_type":study_type,
      "treatment_tags":treatments,
      "query_relevance_score":relevance,
      "keep_for_query":keep,
      "priority_score":score,
      "kcd_candidates":kcd,
      "pico":pico,
      "clinical_summary":pick(analysis,"clinical_summary","summary","clinical_meaning"),
      "keywords":keywords,
      "archive_links":archive_candidates(kcd,treatments),
      "source":"med.symbolicinfo.com",
      "human_reviewed":False,
    }

def markdown(records,query,start,end,total_raw):
    out=[f"# Evidence Radar — {query}","",
         f"- 기간: {start} ~ {end}",
         "- 필터: analyzed=1, km=1, human=1",
         f"- API 원후보: {total_raw}건",
         f"- 관련성 필터 통과: {len(records)}건","",
         "> 자동 생성 검토 후보입니다. KCD·PICO·임상적 의미와 아카이브 링크는 게시 전 사람이 확인합니다.",""]

    for i,r in enumerate(sorted(records,key=lambda x:(x["priority_score"],x["published_date"]),reverse=True),1):
        out += [f"## {i}. {r['title']}","",
                f"- 날짜: {r['published_date'] or '-'}",
                f"- 저널: {r['journal'] or '-'}",
                f"- 연구유형: {r['study_type']}",
                f"- 치료태그: {', '.join(r['treatment_tags']) or '-'}",
                f"- 우선순위 점수: {r['priority_score']}",
                f"- PMID: {r['pmid'] or '-'}",
                f"- DOI: {r['doi'] or '-'}"]
        if r["kcd_candidates"]:
            out.append("- KCD 후보: "+", ".join(x["code"]+" "+x["label"] for x in r["kcd_candidates"]))
        if r["archive_links"]:
            out.append("- 아카이브 연결 후보: "+", ".join(r["archive_links"]))
        p=r["pico"]
        out += ["","**PICO 초안**",
                f"- P: {p['population'] or '-'}",
                f"- I: {p['intervention'] or '-'}",
                f"- C: {p['comparator'] or '-'}",
                f"- O: {p['outcomes'] or '-'}"]
        if r["clinical_summary"]:
            out += ["",f"**API 임상요약:** {r['clinical_summary']}"]
        out += ["","**검토:** ☐ 관련성 ☐ KCD ☐ PICO ☐ 임상적 의미 ☐ 기존 아카이브 링크",""]
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--query",default="pharmacopuncture")
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=100)
    ap.add_argument("--out",default="")
    args=ap.parse_args()

    end=date.today()
    start=end-timedelta(days=365*args.years)
    params={"q":args.query,"page":1,"per_page":min(args.limit,10000),
            "analyzed":1,"km":1,"human":1,
            "pub_from":start.isoformat(),"pub_to":end.isoformat()}
    raw=get_json("/search",params)
    if isinstance(raw,list): rows=raw
    elif isinstance(raw,dict): rows=pick(raw,"items","results","articles","data",default=[])
    else: rows=[]

    normalized=[normalize(x,args.query) for x in rows[:args.limit] if isinstance(x,dict)]
    records=[x for x in normalized if x["keep_for_query"]]

    out=Path(args.out or f"evidence-{args.query.replace(' ','-')}-v2.md")
    out.write_text(markdown(records,args.query,start,end,len(normalized)),encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"raw {len(normalized)} -> relevant {len(records)} -> {out}")

if __name__=="__main__":
    main()
