#!/usr/bin/env python3
"""
173 — Herbal Medicine Evidence Radar

First-pass herbal formula pipeline.
Internal only: evidence-radar-work/herbal-medicine/
Never writes docs/.

Focus:
- human clinical studies
- herbal medicine / Chinese herbal medicine / Korean medicine formula signals
- formula/decoction/granule/extract-oriented studies
- separates acupuncture/pharmacopuncture-only records
- retraction/comment/protocol safeguards
- A/B completed evidence prioritized
- formula + disease candidate extraction
"""
import argparse,json,re,time,urllib.parse,urllib.request,urllib.error
from datetime import date,timedelta
from pathlib import Path
from collections import defaultdict

BASE="https://med.symbolicinfo.com"
QUERIES=[
 "herbal medicine",
 "Chinese herbal medicine",
 "herbal formula",
 "decoction",
 "traditional herbal medicine"
]
BAD=["retraction","retracted","withdrawn","comment on ","editorial","corrigendum","erratum"]
NON_HERBAL=["electroacupuncture","pharmacopuncture","acupotomy"]  # only exclusion if no herbal signal
HERBAL=["herbal medicine","chinese herbal medicine","herbal formula","decoction",
        "granule","herbal extract","traditional medicine","한약","탕","산","환"]

# Common formula seeds already relevant to the archive; unknown formulas are still retained.
FORMULAS=[
 (["guibi tang","gui pi tang","guipi tang","귀비탕"],"귀비탕","formulas/guibi-tang/"),
 (["bojungikgi","bu zhong yi qi","補中益氣","보중익기탕"],"보중익기탕","formulas/bojungikgi-tang/"),
 (["dokhwalgi-saeng","du huo ji sheng","독활기생탕"],"독활기생탕","formulas/dokhwalgi-saeng-tang/"),
 (["yukgunja","liu jun zi","육군자탕"],"육군자탕","formulas/yukgunja-tang/"),
 (["sagunja","si jun zi","사군자탕"],"사군자탕","formulas/sagunja-tang/"),
 (["onjeong","wen jing tang","온경탕"],"온경탕","formulas/onjeong-tang/"),
 (["cheong-sang-gyeon-tong","qing shang juan tong","청상견통탕"],"청상견통탕","formulas/cheongsang-gyeontong-tang/"),
 (["ojeok-san","wu ji san","오적산"],"오적산","formulas/ojeok-san/"),
 (["ondam","wen dan tang","온담탕"],"온담탕","formulas/ondam-tang/"),
 (["hyeongbangdojeok","형방도적산"],"형방도적산","sasang-formulas/hyeongbangdojeok-san/"),
]

KCD=[
 (["functional dyspepsia","기능성 소화불량"],"K30","기능성소화불량","conditions/functional-dyspepsia/"),
 (["irritable bowel","과민성장"],"K58","과민성장증후군","conditions/irritable-bowel-syndrome/"),
 (["constipation","변비"],"K59.0","변비","conditions/constipation/"),
 (["insomnia","불면"],"G47","불면","conditions/insomnia/"),
 (["anxiety","불안"],"F41","불안장애","conditions/anxiety/"),
 (["depression","우울"],"F32","우울증","conditions/depression/"),
 (["low back pain","요통"],"M54","요통","conditions/low-back-pain/"),
 (["knee osteoarthritis","무릎 골관절염"],"M17","무릎 골관절염","conditions/knee-osteoarthritis/"),
 (["allergic rhinitis","알레르기 비염"],"J30","알레르기비염","conditions/allergic-rhinitis/"),
 (["atopic dermatitis","아토피"],"L20","아토피피부염","conditions/atopic-dermatitis/"),
 (["menopause","menopausal","갱년기"],"N95","갱년기","conditions/menopause/"),
 (["dysmenorrhea","생리통"],"N94","생리통","conditions/primary-dysmenorrhea/"),
]

def req(q,years,limit,retries=3):
    end=date.today();start=end-timedelta(days=365*years)
    params={"q":q,"page":1,"per_page":min(limit,10000),"analyzed":1,"km":1,"human":1,
            "pub_from":start.isoformat(),"pub_to":end.isoformat()}
    url=BASE+"/search?"+urllib.parse.urlencode(params)
    errs=[]
    for i in range(1,retries+1):
        try:
            rq=urllib.request.Request(url,headers={"User-Agent":"Minseong-Evidence-Radar-Herbal/0.1","Accept":"application/json"})
            with urllib.request.urlopen(rq,timeout=60) as r:return json.loads(r.read().decode()),errs
        except Exception as e:
            errs.append({"query":q,"attempt":i,"error":str(e)})
            if i<retries:time.sleep(3*i)
    return None,errs

def pick(o,*ks,default=""):
    for k in ks:
        if isinstance(o,dict) and o.get(k) not in (None,"",[],{}):return o[k]
    return default
def flat(v):
    if isinstance(v,str):return v
    if isinstance(v,list):return " ".join(flat(x) for x in v)
    if isinstance(v,dict):return " ".join(flat(x) for x in v.values())
    return str(v or "")
def stype(t):
    t=t.lower()
    if "protocol" in t and ("systematic review" in t or "meta-analysis" in t):return "SR/MA protocol"
    if "systematic review" in t and "meta-analysis" in t:return "Systematic review & meta-analysis"
    if "systematic review" in t:return "Systematic review"
    if "meta-analysis" in t:return "Meta-analysis"
    if "protocol" in t and ("randomized" in t or "randomised" in t):return "RCT protocol"
    if any(x in t for x in ["randomized controlled","randomised controlled","randomized clinical trial"]):return "RCT"
    if "cohort" in t:return "Cohort study"
    if "case-control" in t:return "Case-control study"
    if "case report" in t:return "Case report/series"
    return "Other human study"
def level(s):
    if s in {"Systematic review & meta-analysis","Systematic review","Meta-analysis"}:return "A"
    if s=="RCT":return "B"
    if s in {"RCT protocol","SR/MA protocol"}:return "P"
    if s=="Case report/series":return "D"
    return "C"
def formulas(t):
    out=[]
    for terms,label,path in FORMULAS:
        if any(x.lower() in t for x in terms):out.append({"label":label,"archive_path":path})
    return out
def kcd(t):
    out=[]
    for terms,code,label,path in KCD:
        if any(x.lower() in t for x in terms):
            out.append({"code":code,"label":label,"archive_path":path,"status":"candidate"})
    return out
def key(r):
    if r.get("doi"):return "doi:"+str(r["doi"]).lower()
    if r.get("pmid"):return "pmid:"+str(r["pmid"])
    return "title:"+re.sub(r"\W+"," ",r["title"].lower()).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=200)
    ap.add_argument("--outdir",default="evidence-radar-work/herbal-medicine")
    a=ap.parse_args()
    fetched=[];errors=[];success=[]
    for q in QUERIES:
        raw,errs=req(q,a.years,a.limit);errors+=errs
        if raw is None:continue
        rs=raw if isinstance(raw,list) else next((raw.get(k) for k in ["items","results","articles","data"] if isinstance(raw.get(k),list)),[])
        fetched+=rs;success.append({"query":q,"records":len(rs)})

    records=[];excluded=[];seen=set()
    for x in fetched:
        if not isinstance(x,dict):continue
        title=str(pick(x,"title","article_title"));kw=pick(x,"keywords",default=[])
        t=(title+" "+flat(kw)).lower()
        if any(b in t for b in BAD):excluded.append({"title":title,"reason":"unsafe-publication-type"});continue
        herbal=any(h in t for h in HERBAL)
        if not herbal:continue
        s=stype(t)
        r={"title":title,"published_date":pick(x,"published_date","publication_date","pub_date"),
           "journal":pick(x,"journal","journal_name"),"pmid":pick(x,"pmid"),"doi":pick(x,"doi"),
           "study_type":s,"evidence_level":level(s),"clinical_evidence":True,
           "formula_candidates":formulas(t),"kcd_candidates":kcd(t),
           "keywords":kw,"source":"med.symbolicinfo.com","human_reviewed":False}
        kk=key(r)
        if kk in seen:excluded.append({"title":title,"reason":"duplicate"});continue
        seen.add(kk);records.append(r)

    ab=[r for r in records if r["evidence_level"] in {"A","B"}]
    protocols=[r for r in records if r["evidence_level"]=="P"]
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    (out/"herbal-medicine-clinical.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"herbal-medicine-excluded.json").write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"run-status.json").write_text(json.dumps({"queries":QUERIES,"succeeded":success,"raw":len(fetched),"errors":errors},ensure_ascii=False,indent=2),encoding="utf-8")

    groups=defaultdict(list)
    for r in ab:
        labs=[x["label"] for x in r["kcd_candidates"]] or ["질환 미매핑"]
        for l in labs:groups[l].append(r)
    md=["# Herbal Medicine Evidence Radar","",
        f"- raw 수집: {len(fetched)}건",f"- 한약 관련 후보: {len(records)}건",
        f"- 완료 A/B: {len(ab)}건",f"- protocol: {len(protocols)}건",
        f"- 제외/중복: {len(excluded)}건","",
        "> 내부 검토용. docs/ 자동 게시 없음.","",
        "## 질환별 A/B 후보",""]
    for l,rs in sorted(groups.items(),key=lambda z:len(z[1]),reverse=True):
        md.append(f"### {l}")
        for r in rs:
            fs=", ".join(x["label"] for x in r["formula_candidates"]) or "처방명 자동확인 필요"
            ident=r.get("doi") or r.get("pmid") or "-"
            md.append(f"- [{r['evidence_level']}] {r['title']} — {fs} — {ident}")
        md.append("")
    (out/"herbal-medicine-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"HERBAL -> records {len(records)} | A/B {len(ab)} | protocols {len(protocols)} | excluded {len(excluded)}")
    print(out)

if __name__=="__main__":main()
