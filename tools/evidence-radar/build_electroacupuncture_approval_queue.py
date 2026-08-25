#!/usr/bin/env python3
"""
170 — Electroacupuncture evidence approval queue
Internal only; does not modify docs.
"""
import argparse,json,re
from pathlib import Path
from collections import defaultdict

def ids(r):
    return [x for x in [str(r.get("doi") or "").lower().strip(),str(r.get("pmid") or "").strip()] if x]

def norm(s): return re.sub(r"[^a-z0-9가-힣]+"," ",str(s).lower()).strip()

def resolve(root,path):
    if not path:return None
    rel=path.strip("/")
    cs=[Path(root)/(rel+".md"),Path(root)/rel/"index.md",
        Path(root)/"authority"/(rel+".md"),Path(root)/"authority"/rel/"index.md"]
    for p in cs:
        if p.exists():return p
    base=Path(rel).name
    hits=list(Path(root).rglob(base+".md"))
    return hits[0] if len(hits)==1 else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("evidence"); ap.add_argument("docs")
    ap.add_argument("--outdir",default="evidence-radar-work/electroacupuncture-approval")
    a=ap.parse_args()
    rows=json.loads(Path(a.evidence).read_text(encoding="utf-8"))
    files=list(Path(a.docs).rglob("*.md"))
    texts={}
    for p in files:
        texts[p]=p.read_text(encoding="utf-8-sig",errors="ignore").lower()
    alltext="\n".join(texts.values())

    ab=[r for r in rows if r.get("evidence_level") in {"A","B"} and r.get("study_type") not in {"RCT protocol","SR/MA protocol"}]
    protocols=[r for r in rows if r.get("evidence_level")=="P"]
    title_counts=defaultdict(int)
    for r in ab:title_counts[norm(r.get("title"))]+=1

    buckets=defaultdict(list)
    for r in ab:
        if ids(r) and any(i in alltext for i in ids(r)):
            buckets["existing"].append(r);continue
        targets=[]
        for k in r.get("kcd_candidates_refined",r.get("kcd_candidates",[])):
            p=resolve(a.docs,k.get("archive_path"))
            if p:targets.append(str(p.relative_to(a.docs)).replace("\\","/"))
        targets=list(dict.fromkeys(targets)); r["resolved_targets"]=targets

        reasons=[]
        if not targets:reasons.append("target-missing-or-unmapped")
        if r.get("kcd_mapping_status")!="title-supported":reasons.append("condition-mapping-review")
        ti=str(r.get("title","")).lower()
        # indirect/multi-intervention evidence should not be presented as pure EA efficacy
        if any(x in ti for x in ["different physical stimulation","different acupuncture methods",
                                  "nonpharmacological methods","different interventions",
                                  "acupuncture in patients","acupuncture for women",
                                  "rehabilitation therapies"]):
            reasons.append("indirect-or-multimodal-evidence")
        if "combined with" in ti or " and exercise" in ti:
            reasons.append("combination-intervention")
        if r.get("electrical_modality_final",{}).get("primary")=="auricular-electroacupuncture":
            reasons.append("auricular-ea-subtype")
        if title_counts[norm(r.get("title"))]>1:reasons.append("duplicate-title")
        if str(r.get("doi") or "").lower().startswith("10.21203/"):reasons.append("preprint")

        r["approval_reasons"]=reasons
        buckets["review" if reasons else "approve"].append(r)

    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    for n in ["existing","approve","review"]:
        (out/f"{n}.json").write_text(json.dumps(buckets[n],ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"protocol.json").write_text(json.dumps(protocols,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Electroacupuncture Evidence Approval Queue","",
        f"- 완료 A/B 입력: {len(ab)}건",
        f"- 기존 docs에 이미 존재: {len(buckets['existing'])}건",
        f"- 신규 반영 승인 후보: {len(buckets['approve'])}건",
        f"- 사람 검토 필요: {len(buckets['review'])}건",
        f"- protocol 추적: {len(protocols)}건","",
        "> 내부 작업자료입니다. 자동 병합·자동 공개하지 않습니다.","",
        "## 신규 반영 승인 후보",""]
    for r in buckets["approve"]:
        md.append(f"- [{r.get('evidence_level')}] {r.get('title')} → {', '.join(r.get('resolved_targets',[]))} — {r.get('doi') or r.get('pmid') or '-'}")
    md += ["","## 사람 검토 필요",""]
    for r in buckets["review"]:
        md.append(f"- [{r.get('evidence_level')}] {r.get('title')} — {', '.join(r.get('approval_reasons',[]))} — {r.get('doi') or r.get('pmid') or '-'}")
    (out/"approval-queue.md").write_text("\n".join(md),encoding="utf-8")
    print(f"A/B {len(ab)} -> existing {len(buckets['existing'])} -> approve {len(buckets['approve'])} -> review {len(buckets['review'])} -> protocols {len(protocols)}")

if __name__=="__main__":main()
