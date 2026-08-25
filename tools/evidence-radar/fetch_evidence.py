#!/usr/bin/env python3
"""
Minseong Evidence Radar prototype
Read-only client for med.symbolicinfo.com public GET API.

Example:
python fetch_evidence.py --query pharmacopuncture --years 3 --limit 50
python fetch_evidence.py --query acupuncture --years 1 --limit 100 --out acupuncture.md
"""
import argparse, json, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

BASE="https://med.symbolicinfo.com"

def get_json(path, params):
    url=BASE+path+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":"Minseong-Evidence-Radar/0.1"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def pick(obj,*keys,default=""):
    for k in keys:
        v=obj.get(k)
        if v not in (None,"",[],{}): return v
    return default

def classify_kcd(text):
    t=text.lower()
    rules=[
      (["carpal tunnel"],"G56.0","손목터널증후군"),
      (["low back pain","lumbar pain"],"M54","요통"),
      (["knee osteoarthritis"],"M17","무릎 골관절염"),
      (["insomnia"],"G47","불면"),
      (["allergic rhinitis"],"J30","알레르기비염"),
      (["migraine"],"G43","편두통"),
      (["functional dyspepsia"],"K30","기능성소화불량"),
      (["prostatitis","chronic pelvic pain syndrome"],"N41","만성전립선염/CPPS"),
    ]
    return [{"code":c,"label":l,"status":"candidate"} for terms,c,l in rules if any(x in t for x in terms)]

def normalize(a):
    title=str(pick(a,"title","article_title"))
    analysis=a.get("analysis") or a.get("article_analysis") or {}
    if not isinstance(analysis,dict): analysis={}
    blob=" ".join([title,str(a),str(analysis)])
    pico=pick(analysis,"pico",default={})
    if not isinstance(pico,dict): pico={}
    return {
      "title":title,
      "published_date":pick(a,"published_date","publication_date","pub_date"),
      "journal":pick(a,"journal","journal_name"),
      "pmid":pick(a,"pmid"),
      "doi":pick(a,"doi"),
      "study_type":pick(analysis,"category","study_type","research_type"),
      "korean_medicine":pick(analysis,"is_korean_medicine","korean_medicine"),
      "human_study":pick(analysis,"is_human","human_study"),
      "kcd_candidates":classify_kcd(blob),
      "pico":{
        "population":pick(pico,"population","P"),
        "intervention":pick(pico,"intervention","I"),
        "comparator":pick(pico,"comparator","C"),
        "outcomes":pick(pico,"outcome","outcomes","O",default=[]),
      },
      "clinical_summary":pick(analysis,"clinical_summary","summary","clinical_meaning"),
      "keywords":pick(a,"keywords",default=[]),
      "source":"med.symbolicinfo.com",
      "human_reviewed":False,
    }

def markdown(records,query,start,end):
    out=[f"# Evidence Radar — {query}","",
         f"- 기간: {start} ~ {end}",
         "- 필터: analyzed=1, km=1, human=1",
         f"- 후보 논문: {len(records)}건","",
         "> 자동 생성된 검토 후보입니다. KCD, PICO와 임상적 의미는 게시 전 사람이 확인합니다.",""]
    for i,r in enumerate(records,1):
        out += [f"## {i}. {r['title']}","",
                f"- 날짜: {r['published_date'] or '-'}",
                f"- 저널: {r['journal'] or '-'}",
                f"- 연구유형: {r['study_type'] or '-'}",
                f"- PMID: {r['pmid'] or '-'}",
                f"- DOI: {r['doi'] or '-'}"]
        if r["kcd_candidates"]:
            out.append("- KCD 후보: "+", ".join(x["code"]+" "+x["label"] for x in r["kcd_candidates"]))
        p=r["pico"]
        out += ["", "**PICO 초안**",
                f"- P: {p['population'] or '-'}",
                f"- I: {p['intervention'] or '-'}",
                f"- C: {p['comparator'] or '-'}",
                f"- O: {p['outcomes'] or '-'}"]
        if r["clinical_summary"]:
            out += ["",f"**API 임상요약:** {r['clinical_summary']}"]
        out += ["","**검토:** ☐ KCD ☐ PICO ☐ 임상적 의미 ☐ 기존 아카이브 링크",""]
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--query",default="pharmacopuncture")
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=50)
    ap.add_argument("--out",default="")
    args=ap.parse_args()
    end=date.today()
    start=end-timedelta(days=365*args.years)
    params={"q":args.query,"page":1,"per_page":min(args.limit,10000),
            "analyzed":1,"km":1,"human":1,
            "pub_from":start.isoformat(),"pub_to":end.isoformat()}
    raw=get_json("/search",params)
    if isinstance(raw,list): rows=raw
    elif isinstance(raw,dict):
        rows=pick(raw,"items","results","articles","data",default=[])
    else: rows=[]
    records=[normalize(x) for x in rows[:args.limit] if isinstance(x,dict)]
    out=Path(args.out or f"evidence-{args.query.replace(' ','-')}.md")
    out.write_text(markdown(records,args.query,start,end),encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"saved {len(records)} candidates -> {out}")

if __name__=="__main__":
    main()
