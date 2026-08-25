#!/usr/bin/env python3
"""
Minseong Evidence Radar — Acupuncture pipeline (162)

Runs the proven Evidence Radar flow for acupuncture:
API -> relevance -> clinical evidence -> KCD/condition -> evidence level
-> reviewable update candidates.

Internal-only outputs. Nothing is written under docs/.
No automatic wiki publishing.
"""
import argparse, json, re, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path
from collections import defaultdict

BASE="https://med.symbolicinfo.com"

ALIASES=[
 "acupuncture","acupuncture therapy","manual acupuncture",
 "침 치료","침치료","침술","침(鍼","鍼治療"
]
EXCLUDE_AS_PRIMARY=[
 "pharmacopuncture","pharmacoacupuncture","약침","봉침",
 "electroacupuncture","electro-acupuncture","전침",
 "acupotomy","도침","침도"
]
NONCLINICAL=[
 "education","curriculum","student","survey on the current usage",
 "utilization","search trends","data lab","bibliometric","expert opinion"
]

KCD=[
 (["low back pain","chronic low back pain","요통"],"M54","요통","conditions/low-back-pain/"),
 (["lumbar spinal stenosis","요추 척추관 협착"],"M48.06","요추 척추관협착증","conditions/lumbar-spinal-stenosis/"),
 (["lumbar disc herniation","요추 추간판 탈출"],"M51.1","요추 추간판탈출증","conditions/lumbar-disc-herniation/"),
 (["cervical disc herniation","경추 추간판 탈출"],"M50.1","경추 추간판탈출증","conditions/cervical-disc-herniation/"),
 (["neck pain","chronic neck pain","목 통증"],"M54.2","경부통","conditions/neck-pain/"),
 (["knee osteoarthritis","무릎 골관절염"],"M17","무릎 골관절염","conditions/knee-osteoarthritis/"),
 (["shoulder pain","어깨 통증"],"M25.51","어깨통증","conditions/shoulder-pain/"),
 (["frozen shoulder","adhesive capsulitis","오십견"],"M75.0","유착성관절낭염","conditions/frozen-shoulder/"),
 (["migraine","편두통"],"G43","편두통","conditions/migraine/"),
 (["tension-type headache","tension headache","긴장형두통"],"G44.2","긴장형두통","conditions/tension-type-headache/"),
 (["insomnia","불면"],"G47","불면","conditions/insomnia/"),
 (["allergic rhinitis","알레르기 비염"],"J30","알레르기비염","conditions/allergic-rhinitis/"),
 (["functional dyspepsia","기능성 소화불량"],"K30","기능성소화불량","conditions/functional-dyspepsia/"),
 (["irritable bowel","과민성장"],"K58","과민성장증후군","conditions/irritable-bowel-syndrome/"),
 (["temporomandibular","턱관절"],"K07.6","턱관절장애","conditions/temporomandibular-disorder/"),
 (["carpal tunnel","손목터널"],"G56.0","손목터널증후군","conditions/carpal-tunnel-syndrome/"),
 (["postherpetic neuralgia","대상포진 후 신경통"],"G53.0","대상포진후신경통","conditions/postherpetic-neuralgia/"),
]

def get_json(path,params):
    url=BASE+path+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":"Minseong-Evidence-Radar-Acupuncture/0.1"})
    with urllib.request.urlopen(req,timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))

def pick(o,*ks,default=""):
    if not isinstance(o,dict): return default
    for k in ks:
        v=o.get(k)
        if v not in (None,"",[],{}): return v
    return default

def flat(v):
    if isinstance(v,str): return v
    if isinstance(v,list): return " ".join(flat(x) for x in v)
    if isinstance(v,dict): return " ".join(flat(x) for x in v.values())
    return str(v or "")

def study_type(title,keywords):
    t=(title+" "+flat(keywords)).lower()
    if "protocol" in t and ("systematic review" in t or "meta-analysis" in t): return "SR/MA protocol"
    if "systematic review" in t and "meta-analysis" in t: return "Systematic review & meta-analysis"
    if "systematic review" in t: return "Systematic review"
    if "meta-analysis" in t: return "Meta-analysis"
    if "protocol" in t and ("randomized" in t or "randomised" in t): return "RCT protocol"
    if "randomized controlled" in t or "randomised controlled" in t or "randomized clinical trial" in t: return "RCT"
    if "cohort" in t: return "Cohort study"
    if "case-control" in t: return "Case-control study"
    if "cross-sectional" in t: return "Cross-sectional study"
    if "case report" in t or "case series" in t: return "Case report/series"
    return "Other human study"

def level(st):
    if st in {"Systematic review & meta-analysis","Systematic review","Meta-analysis"}: return "A"
    if st=="RCT": return "B"
    if st in {"Cohort study","Case-control study","Cross-sectional study","Other human study"}: return "C"
    if st=="Case report/series": return "D"
    return "P"

def relevance(title,journal,keywords):
    title_l=title.lower(); kw=flat(keywords).lower(); journal_l=journal.lower()
    primary=any(x.lower() in title_l or x.lower() in kw for x in ALIASES)
    excluded=any(x.lower() in title_l for x in EXCLUDE_AS_PRIMARY)
    # allow multimodal studies where acupuncture is explicitly a treatment keyword,
    # but do not let pharmacopuncture/electroacupuncture-only papers masquerade as manual acupuncture.
    manual_signal=any(x.lower() in title_l or x.lower() in kw for x in ["manual acupuncture","침 치료","침치료","acupuncture"])
    journal_only=("acupuncture" in journal_l and not primary)
    score=(6 if any(x.lower() in title_l for x in ALIASES) else 0)+(4 if any(x.lower() in kw for x in ALIASES) else 0)
    if excluded and not manual_signal: score-=8
    if journal_only: score-=5
    return score, primary and score>0 and not journal_only

def classify(text):
    t=text.lower(); out=[]
    for terms,code,label,path in KCD:
        if any(x.lower() in t for x in terms):
            out.append({"code":code,"label":label,"status":"candidate","archive_path":path})
    return out

def pico(title,keywords):
    t=(title+" "+flat(keywords)).lower()
    outcomes=[]
    for label,terms in [
      ("통증",["pain","통증"]),("기능",["function","functional","기능"]),
      ("삶의 질",["quality of life","qol","삶의 질"]),("수면",["sleep","insomnia","수면"]),
      ("안전성",["safety","adverse","안전성"]),("삶의 질/기능척도",["womac","odi","ndI".lower()])
    ]:
        if any(x in t for x in terms): outcomes.append(label)
    comp=""
    if "sham acupuncture" in t or "sham" in t: comp="sham acupuncture"
    elif "usual care" in t: comp="usual care"
    elif "physical therapy" in t or "physiotherapy" in t: comp="physical therapy"
    return {"population":"","intervention":"acupuncture","comparator":comp,"outcomes":list(dict.fromkeys(outcomes))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=200)
    ap.add_argument("--query",default="acupuncture")
    ap.add_argument("--outdir",default="evidence-radar-work/acupuncture")
    args=ap.parse_args()

    end=date.today(); start=end-timedelta(days=365*args.years)
    raw=get_json("/search",{"q":args.query,"page":1,"per_page":min(args.limit,10000),
                            "analyzed":1,"km":1,"human":1,
                            "pub_from":start.isoformat(),"pub_to":end.isoformat()})
    rows=raw if isinstance(raw,list) else pick(raw,"items","results","articles","data",default=[])
    records=[]
    for a in rows[:args.limit]:
        if not isinstance(a,dict): continue
        title=str(pick(a,"title","article_title")); journal=str(pick(a,"journal","journal_name"))
        keywords=pick(a,"keywords",default=[])
        score,keep=relevance(title,journal,keywords)
        if not keep: continue
        blob=title+" "+flat(keywords)
        st=study_type(title,keywords)
        nonclinical=any(x in blob.lower() for x in NONCLINICAL)
        rec={
          "title":title,"published_date":pick(a,"published_date","publication_date","pub_date"),
          "journal":journal,"pmid":pick(a,"pmid"),"doi":pick(a,"doi"),
          "study_type":st,"evidence_level":level(st),
          "query_relevance_score":score,"clinical_evidence":not nonclinical,
          "kcd_candidates":classify(blob),"pico":pico(title,keywords),
          "keywords":keywords,"source":"med.symbolicinfo.com","human_reviewed":False
        }
        records.append(rec)

    outdir=Path(args.outdir); outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"acupuncture-clinical.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")

    clinical=[r for r in records if r["clinical_evidence"]]
    high=[r for r in clinical if r["evidence_level"] in {"A","B"}]
    grouped=defaultdict(list)
    for r in high:
        for k in r["kcd_candidates"]: grouped[k["label"]].append(r)

    md=["# Acupuncture Evidence Radar","",
        f"- 기간: {start} ~ {end}",f"- 관련성 통과: {len(records)}건",
        f"- 임상 후보: {len(clinical)}건",f"- A/B 우선근거: {len(high)}건","",
        "> 내부 검토용 결과입니다. docs/에는 자동 게시하지 않습니다.","",
        "## 질환별 A/B 후보",""]
    for label,recs in sorted(grouped.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            src=("PMID "+str(r["pmid"])) if r["pmid"] else ("DOI "+str(r["doi"]) if r["doi"] else "식별자 확인 필요")
            md.append(f"- [{r['evidence_level']}] {r['title']} — {src}")
        md.append("")
    (outdir/"acupuncture-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"relevant {len(records)} -> clinical {len(clinical)} -> A/B {len(high)}")
    print(f"internal output -> {outdir}")

if __name__=="__main__":
    main()
