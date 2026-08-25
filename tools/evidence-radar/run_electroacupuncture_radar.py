#!/usr/bin/env python3
"""
167 — Minseong Evidence Radar: Electroacupuncture

Independent electroacupuncture pipeline based on the validated
pharmacopuncture/acupuncture workflow.

Internal outputs only:
  evidence-radar-work/electroacupuncture/

Nothing is written to docs/.
"""
import argparse, json, re, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path
from collections import defaultdict

BASE="https://med.symbolicinfo.com"

EA=["electroacupuncture","electro-acupuncture","electrical acupuncture",
    "electro acupuncture","전침","電鍼"]
EXCLUDE_PRIMARY={
 "pharmacopuncture":["pharmacopuncture","pharmacoacupuncture","약침","봉침"],
 "acupotomy":["acupotomy","needle knife","acupotome","도침","침도","鍼刀"]
}
BAD=["retraction","retracted","withdrawn","withdrawal notice",
     "comment on ","editorial","letter to the editor","commentary","corrigendum","erratum"]

KCD=[
 (["low back pain","chronic low back pain","요통"],"M54","요통","conditions/low-back-pain/"),
 (["lumbar spinal stenosis","요추 척추관 협착"],"M48.06","요추 척추관협착증","conditions/lumbar-spinal-stenosis/"),
 (["lumbar disc herniation","요추 추간판 탈출"],"M51.1","요추 추간판탈출증","conditions/lumbar-disc-herniation/"),
 (["cervical radiculopathy","경추 신경근"],"M54.12","경추 신경근병증","conditions/cervical-radiculopathy/"),
 (["neck pain","목 통증"],"M54.2","경부통","conditions/neck-pain/"),
 (["knee osteoarthritis","무릎 골관절염"],"M17","무릎 골관절염","conditions/knee-osteoarthritis/"),
 (["frozen shoulder","adhesive capsulitis","오십견"],"M75.0","유착성관절낭염","conditions/frozen-shoulder/"),
 (["rotator cuff","회전근개"],"M75.1","회전근개 질환","conditions/rotator-cuff-disease/"),
 (["migraine","편두통"],"G43","편두통","conditions/migraine/"),
 (["tension-type headache","긴장형두통"],"G44.2","긴장형두통","conditions/tension-type-headache/"),
 (["insomnia","불면"],"G47","불면","conditions/insomnia/"),
 (["stroke","post-stroke","poststroke","뇌졸중"],"I63","뇌졸중/뇌경색","conditions/stroke/"),
 (["parkinson","파킨슨"],"G20","파킨슨병","conditions/parkinsons-disease/"),
 (["diabetic peripheral neuropathy","당뇨병성 말초신경"],"G63.2","당뇨병성 말초신경병증","conditions/diabetic-polyneuropathy/"),
 (["functional dyspepsia","기능성 소화불량"],"K30","기능성소화불량","conditions/functional-dyspepsia/"),
 (["irritable bowel","과민성장"],"K58","과민성장증후군","conditions/irritable-bowel-syndrome/"),
 (["constipation","변비"],"K59.0","변비","conditions/constipation/"),
 (["stress urinary incontinence","복압성 요실금"],"N39.3","복압성 요실금","conditions/stress-urinary-incontinence/"),
 (["primary dysmenorrhea","원발성 생리통"],"N94.4","원발성 생리통","conditions/primary-dysmenorrhea/"),
 (["polycystic ovary","pcos","다낭성"],"E28.2","다낭성난소증후군","conditions/polycystic-ovary-syndrome/"),
 (["depression","우울"],"F32","우울증","conditions/depression/"),
 (["anxiety","불안"],"F41","불안장애","conditions/anxiety/"),
 (["fibromyalgia","섬유근육통"],"M79.7","섬유근육통","conditions/fibromyalgia/"),
]

def get_json(path,params):
    url=BASE+path+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":"Minseong-Evidence-Radar-Electroacupuncture/0.1"})
    with urllib.request.urlopen(req,timeout=45) as r:
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

def blob(a,include_journal=False):
    parts=[str(pick(a,"title","article_title")),flat(pick(a,"keywords",default=[]))]
    if include_journal: parts.append(str(pick(a,"journal","journal_name")))
    return " ".join(parts).lower()

def study_type(title,keywords):
    t=(title+" "+flat(keywords)).lower()
    if "protocol" in t and ("systematic review" in t or "meta-analysis" in t): return "SR/MA protocol"
    if "systematic review" in t and "meta-analysis" in t: return "Systematic review & meta-analysis"
    if "systematic review" in t: return "Systematic review"
    if "meta-analysis" in t: return "Meta-analysis"
    if "protocol" in t and ("randomized" in t or "randomised" in t): return "RCT protocol"
    if any(x in t for x in ["randomized controlled","randomised controlled","randomized clinical trial","randomised clinical trial"]): return "RCT"
    if "cohort" in t:return "Cohort study"
    if "case-control" in t:return "Case-control study"
    if "cross-sectional" in t:return "Cross-sectional study"
    if "case report" in t or "case series" in t:return "Case report/series"
    return "Other human study"

def level(st):
    if st in {"Systematic review & meta-analysis","Systematic review","Meta-analysis"}:return "A"
    if st=="RCT":return "B"
    if st in {"Cohort study","Case-control study","Cross-sectional study","Other human study"}:return "C"
    if st=="Case report/series":return "D"
    return "P"

def classify(t):
    out=[]
    for terms,code,label,path in KCD:
        if any(x.lower() in t for x in terms):
            out.append({"code":code,"label":label,"status":"candidate","archive_path":path})
    return out

def primary_modality(t):
    ea=any(x.lower() in t for x in EA)
    pa=any(x.lower() in t for x in EXCLUDE_PRIMARY["pharmacopuncture"])
    ac=any(x.lower() in t for x in EXCLUDE_PRIMARY["acupotomy"])
    manual=("manual acupuncture" in t or "body acupuncture" in t or
            ("acupuncture" in t and not ea and not pa and not ac))
    if ea and (manual or pa or ac): return "mixed"
    if ea:return "electroacupuncture"
    if pa:return "pharmacopuncture"
    if ac:return "acupotomy"
    return "manual" if manual else "other"

def pico(t):
    outcomes=[]
    for label,terms in [
      ("통증",["pain","통증"]),("기능",["function","functional","기능"]),
      ("수면",["sleep","insomnia","수면"]),("안전성",["safety","adverse","안전성"]),
      ("삶의 질",["quality of life","qol","삶의 질"]),("신경기능",["nerve conduction","neurological"])
    ]:
        if any(x in t for x in terms): outcomes.append(label)
    comp=""
    if "sham electroacupuncture" in t or "sham" in t:comp="sham"
    elif "manual acupuncture" in t:comp="manual acupuncture"
    elif "usual care" in t:comp="usual care"
    return {"population":"","intervention":"electroacupuncture","comparator":comp,"outcomes":list(dict.fromkeys(outcomes))}

def dedupe_key(r):
    d=str(r.get("doi") or "").strip().lower()
    if d:return "doi:"+d
    return "title:"+re.sub(r"\W+"," ",str(r.get("title","")).lower()).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=250)
    ap.add_argument("--outdir",default="evidence-radar-work/electroacupuncture")
    args=ap.parse_args()

    end=date.today(); start=end-timedelta(days=365*args.years)
    # Two queries catch spelling variants; dedupe afterward.
    fetched=[]
    for q in ["electroacupuncture","electro-acupuncture"]:
        raw=get_json("/search",{"q":q,"page":1,"per_page":min(args.limit,10000),
                                "analyzed":1,"km":1,"human":1,
                                "pub_from":start.isoformat(),"pub_to":end.isoformat()})
        rs=raw if isinstance(raw,list) else pick(raw,"items","results","articles","data",default=[])
        fetched.extend(rs)

    records=[]; excluded=[]; seen=set()
    for a in fetched:
        if not isinstance(a,dict):continue
        title=str(pick(a,"title","article_title")); keywords=pick(a,"keywords",default=[])
        t=(title+" "+flat(keywords)).lower() # journal deliberately excluded
        if not any(x.lower() in t for x in EA):continue
        if any(x in t for x in BAD):
            excluded.append({"title":title,"reason":"retraction/comment/editorial"});continue

        modality=primary_modality(t)
        if modality in {"pharmacopuncture","acupotomy","other"}:
            excluded.append({"title":title,"reason":"non-electroacupuncture-primary"});continue

        st=study_type(title,keywords)
        r={
          "title":title,
          "published_date":pick(a,"published_date","publication_date","pub_date"),
          "journal":pick(a,"journal","journal_name"),
          "pmid":pick(a,"pmid"),"doi":pick(a,"doi"),
          "study_type":st,"evidence_level":level(st),
          "modality":modality,
          "clinical_evidence":True,
          "kcd_candidates":classify(t),
          "pico":pico(t),
          "keywords":keywords,
          "source":"med.symbolicinfo.com",
          "human_reviewed":False
        }
        k=dedupe_key(r)
        if k in seen:
            excluded.append({"title":title,"reason":"duplicate"});continue
        seen.add(k);records.append(r)

    completed=[r for r in records if r["evidence_level"] in {"A","B"} and r["study_type"] not in {"RCT protocol","SR/MA protocol"}]
    protocols=[r for r in records if r["evidence_level"]=="P"]
    groups=defaultdict(list)
    for r in completed:
        for x in r["kcd_candidates"]:groups[x["label"]].append(r)

    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    (out/"electroacupuncture-clinical.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"electroacupuncture-excluded.json").write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Electroacupuncture Evidence Radar","",
        f"- 기간: {start} ~ {end}",
        f"- 전침/복합전침 후보: {len(records)}건",
        f"- 완료 A/B 근거: {len(completed)}건",
        f"- protocol 추적: {len(protocols)}건",
        f"- 제외/중복: {len(excluded)}건","",
        "> 내부 검토용입니다. docs/ 자동 게시 없음.","",
        "## 질환별 완료 A/B 근거",""]
    for label,recs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            ident=("PMID "+str(r["pmid"])) if r["pmid"] else ("DOI "+str(r["doi"]) if r["doi"] else "-")
            md.append(f"- [{r['evidence_level']}/{r['modality']}] {r['title']} — {ident}")
        md.append("")
    (out/"electroacupuncture-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"EA candidates {len(records)} -> completed A/B {len(completed)} -> protocols {len(protocols)} -> excluded {len(excluded)}")
    print(f"internal output -> {out}")

if __name__=="__main__":
    main()
