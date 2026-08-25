#!/usr/bin/env python3
"""
Minseong Evidence Radar — Acupuncture refinement (163)

Input:
  evidence-radar-work/acupuncture/acupuncture-clinical.json

Output (internal only):
  evidence-radar-work/acupuncture-refined/acupuncture-refined.json
  evidence-radar-work/acupuncture-refined/acupuncture-refined-review.md

Refinements:
- remove RETRACTION / withdrawn / corrigendum-like records
- remove comments/editorials/letters
- exclude electroacupuncture/pharmacopuncture/acupotomy-only studies from manual acupuncture radar
- deduplicate DOI/title
- correct known KCD false positives
- expand KCD mapping for useful acupuncture conditions
- keep protocols separate from completed A/B evidence
- no docs/ output, no automatic publishing
"""
import argparse, json, re
from pathlib import Path
from collections import defaultdict

RETRACTION_TERMS=["retraction","retracted","withdrawn","withdrawal notice"]
COMMENT_TERMS=["comment on ","editorial","letter to the editor","commentary","corrigendum","erratum"]

EA_TERMS=["electroacupuncture","electro-acupuncture","electrical acupuncture","전침","電鍼"]
PA_TERMS=["pharmacopuncture","pharmacoacupuncture","약침","봉침","bee venom injection"]
ACUPOTOMY_TERMS=["acupotomy","needle knife","acupotome","도침","침도","鍼刀"]

MANUAL_TERMS=["manual acupuncture","body acupuncture","acupuncture therapy","acupuncture treatment","침 치료","침치료","鍼治療"]

KCD_RULES=[
 (["de quervain","드퀘르벵"],"M65.4","드퀘르벵 건초염","conditions/de-quervain-tenosynovitis/"),
 (["dry eye","안구건조"],"H04.1","안구건조","conditions/dry-eye/"),
 (["crohn","크론병"],"K50","크론병","conditions/crohns-disease/"),
 (["mild cognitive impairment","경도인지장애"],"R41.8","경도인지장애","conditions/mild-cognitive-impairment/"),
 (["anxiety disorder","generalized anxiety","불안 장애","범불안"],"F41","불안장애","conditions/anxiety/"),
 (["stroke","뇌졸중"],"I63","뇌졸중/뇌경색","conditions/stroke/"),
 (["bell's palsy","bell’s palsy","안면마비"],"G51.0","벨마비","conditions/bell-palsy/"),
 (["sudden sensorineural hearing loss","돌발성 난청"],"H91.2","돌발성 감각신경성 난청","conditions/sudden-sensorineural-hearing-loss/"),
 (["primary dysmenorrhea","원발성 생리통"],"N94.4","원발성 생리통","conditions/primary-dysmenorrhea/"),
 (["fibromyalgia","섬유근육통"],"M79.7","섬유근육통","conditions/fibromyalgia/"),
 (["gastroesophageal reflux","gerd","위식도역류"],"K21","위식도역류질환","conditions/gastroesophageal-reflux-disease/"),
 (["stress urinary incontinence","복압성 요실금"],"N39.3","복압성 요실금","conditions/stress-urinary-incontinence/"),
 (["diabetic peripheral neuropathy","당뇨병성 말초신경병증"],"G63.2","당뇨병성 말초신경병증","conditions/diabetic-polyneuropathy/"),
 (["restless legs","하지불안"],"G25.81","하지불안증후군","conditions/restless-legs-syndrome/"),
 (["rheumatoid arthritis","류마티스 관절염"],"M06.9","류마티스관절염","conditions/rheumatoid-arthritis/"),
 (["hyperhidrosis","다한증"],"R61","다한증","conditions/hyperhidrosis/"),
 (["myofascial pain","근막통증"],"M79.1","근막통증증후군","conditions/myofascial-pain-syndrome/"),
 (["cervical radiculopathy","경추 신경근증"],"M54.12","경추 신경근병증","conditions/cervical-radiculopathy/"),
]

def text(r):
    return " ".join([
        str(r.get("title","")),
        " ".join(map(str,r.get("keywords",[]))),
        str(r.get("journal",""))
    ]).lower()

def is_retracted(r):
    t=text(r)
    return any(x in t for x in RETRACTION_TERMS)

def is_comment(r):
    title=str(r.get("title","")).lower().strip()
    return any(x in title for x in COMMENT_TERMS)

def modality_flags(r):
    t=text(r)
    return {
      "electroacupuncture": any(x.lower() in t for x in EA_TERMS),
      "pharmacopuncture": any(x.lower() in t for x in PA_TERMS),
      "acupotomy": any(x.lower() in t for x in ACUPOTOMY_TERMS),
      "manual_acupuncture": any(x.lower() in t for x in MANUAL_TERMS) or "acupuncture" in str(r.get("title","")).lower()
    }

def manual_keep(r):
    flags=modality_flags(r)
    title=str(r.get("title","")).lower()
    # Mixed modality reviews remain only when manual/body acupuncture is explicitly part of the question.
    if flags["pharmacopuncture"] and "acupuncture" not in title.replace("pharmacopuncture",""):
        return False,"pharmacopuncture-only"
    if flags["acupotomy"] and "acupuncture" not in title.replace("acupotomy",""):
        return False,"acupotomy-only"
    if flags["electroacupuncture"]:
        manual_explicit=any(x in title for x in ["manual acupuncture","body acupuncture","acupuncture and","acupuncture versus","different acupuncture"])
        if not manual_explicit:
            return False,"electroacupuncture-only"
    return True,""

def correct_kcd(r):
    t=text(r)
    # Remove known false-positive neck-pain mapping in De Quervain paper.
    if "de quervain" in t or "드퀘르벵" in t:
        r["kcd_candidates"]=[x for x in r.get("kcd_candidates",[]) if x.get("code")!="M54.2"]
    # RLS should not be classified as insomnia just because insomnia is mentioned as a symptom.
    if "restless legs" in t or "하지불안" in t:
        r["kcd_candidates"]=[x for x in r.get("kcd_candidates",[]) if x.get("code")!="G47"]

    existing={(x.get("code"),x.get("label")) for x in r.get("kcd_candidates",[])}
    for terms,code,label,path in KCD_RULES:
        if any(term.lower() in t for term in terms) and (code,label) not in existing:
            r.setdefault("kcd_candidates",[]).append({
              "code":code,"label":label,"status":"candidate","archive_path":path
            })
    return r

def completed_ab(r):
    return r.get("evidence_level") in {"A","B"} and r.get("study_type") not in {"RCT protocol","SR/MA protocol"}

def key_for(r):
    doi=str(r.get("doi") or "").strip().lower()
    if doi: return "doi:"+doi
    title=re.sub(r"\W+"," ",str(r.get("title","")).lower()).strip()
    return "title:"+title

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir",default="evidence-radar-work/acupuncture-refined")
    args=ap.parse_args()
    rows=json.loads(Path(args.input).read_text(encoding="utf-8"))

    kept=[]; excluded=[]; seen=set()
    for r in rows:
        reason=""
        if is_retracted(r): reason="retracted/withdrawn"
        elif is_comment(r): reason="comment/editorial"
        else:
            ok,reason2=manual_keep(r)
            if not ok: reason=reason2
        if reason:
            r["refine_exclusion_reason"]=reason
            excluded.append(r); continue

        k=key_for(r)
        if k in seen:
            r["refine_exclusion_reason"]="duplicate"
            excluded.append(r); continue
        seen.add(k)

        r=correct_kcd(r)
        r["modality_flags"]=modality_flags(r)
        kept.append(r)

    completed=[r for r in kept if completed_ab(r)]
    protocols=[r for r in kept if r.get("evidence_level")=="P"]
    groups=defaultdict(list)
    for r in completed:
        for x in r.get("kcd_candidates",[]):
            groups[x.get("label","미분류")].append(r)

    outdir=Path(args.outdir); outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"acupuncture-refined.json").write_text(json.dumps(kept,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"acupuncture-excluded.json").write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Acupuncture Evidence Radar — Refined","",
        f"- 입력: {len(rows)}건",
        f"- 정밀필터 통과: {len(kept)}건",
        f"- 제외: {len(excluded)}건",
        f"- 완료 A/B 근거: {len(completed)}건",
        f"- protocol 추적: {len(protocols)}건","",
        "> 내부 검토용입니다. docs/에는 자동 게시하지 않습니다.","",
        "## 질환별 완료 A/B 근거",""]
    for label,recs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            ident=("PMID "+str(r.get("pmid"))) if r.get("pmid") else ("DOI "+str(r.get("doi")) if r.get("doi") else "식별자 확인 필요")
            md.append(f"- [{r.get('evidence_level')}] {r.get('title')} — {ident}")
        md.append("")
    md += ["## 제외 사유 요약",""]
    counts=defaultdict(int)
    for r in excluded: counts[r.get("refine_exclusion_reason","")]+=1
    for k,v in sorted(counts.items(),key=lambda x:x[1],reverse=True):
        md.append(f"- {k}: {v}건")

    (outdir/"acupuncture-refined-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"input {len(rows)} -> kept {len(kept)} -> excluded {len(excluded)} -> completed A/B {len(completed)} -> protocols {len(protocols)}")

if __name__=="__main__":
    main()
