#!/usr/bin/env python3
"""
165 — Acupuncture evidence approval queue

Compare final A/B acupuncture evidence against current docs.
Internal output only. Does not edit docs/.

Buckets:
- existing: PMID/DOI already present
- approve: mapped target exists, identifier not present, completed A/B
- review: target missing/ambiguous, mixed modality, weak/duplicate-title concerns
- protocol: tracking only
"""
import argparse,json,re
from pathlib import Path
from collections import defaultdict

def norm_title(s):
    return re.sub(r"[^a-z0-9가-힣]+"," ",str(s).lower()).strip()

def identifiers(r):
    out=[]
    if r.get("doi"): out.append(str(r["doi"]).lower().strip())
    if r.get("pmid"): out.append(str(r["pmid"]).strip())
    return out

def docs_index(root):
    files=list(Path(root).rglob("*.md"))
    text={}
    for p in files:
        try: text[p]=p.read_text(encoding="utf-8-sig",errors="ignore").lower()
        except: pass
    return text

def resolve_target(root,archive_path):
    if not archive_path:return None
    rel=archive_path.strip("/")
    candidates=[
      Path(root)/(rel+".md"),
      Path(root)/rel/"index.md",
      Path(root)/"authority"/(rel+".md"),
      Path(root)/"authority"/rel/"index.md",
    ]
    for p in candidates:
        if p.exists(): return p
    # basename fallback, but only if unique
    base=Path(rel).name
    hits=list(Path(root).rglob(base+".md"))+list(Path(root).rglob(base+"/index.md"))
    hits=list(dict.fromkeys(hits))
    return hits[0] if len(hits)==1 else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("evidence")
    ap.add_argument("docs")
    ap.add_argument("--outdir",default="evidence-radar-work/acupuncture-approval")
    args=ap.parse_args()
    rows=json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    dindex=docs_index(args.docs)
    alltext="\n".join(dindex.values())

    ab=[r for r in rows if r.get("evidence_level") in {"A","B"} and r.get("study_type") not in {"RCT protocol","SR/MA protocol"}]
    title_counts=defaultdict(list)
    for r in ab:title_counts[norm_title(r.get("title"))].append(r)

    buckets=defaultdict(list)
    for r in ab:
        ids=identifiers(r)
        if ids and any(i in alltext for i in ids):
            buckets["existing"].append(r); continue

        targets=[]
        for k in r.get("kcd_candidates",[]):
            p=resolve_target(args.docs,k.get("archive_path"))
            if p: targets.append(str(p.relative_to(args.docs)).replace("\\","/"))
        targets=list(dict.fromkeys(targets))
        r["resolved_targets"]=targets

        reasons=[]
        if not targets: reasons.append("target-missing-or-unmapped")
        if r.get("modality_final",{}).get("primary")=="mixed": reasons.append("mixed-modality")
        if len(title_counts[norm_title(r.get("title"))])>1: reasons.append("duplicate-title")
        doi=str(r.get("doi") or "").lower()
        if "10.21203/" in doi: reasons.append("preprint")
        # Internal evidence level is not quality appraisal; flag some title patterns for human check.
        ti=str(r.get("title","")).lower()
        if "theoretical meta-analysis review" in ti: reasons.append("study-design-quality-check")
        if "mongolian" in ti or "warm acupuncture" in ti: reasons.append("modality-generalizability-check")

        if reasons:
            r["approval_reasons"]=reasons
            buckets["review"].append(r)
        else:
            buckets["approve"].append(r)

    protocols=[r for r in rows if r.get("evidence_level")=="P"]
    buckets["protocol"]=protocols

    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    for name,recs in buckets.items():
        (out/f"{name}.json").write_text(json.dumps(recs,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Acupuncture Evidence Approval Queue","",
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

if __name__=="__main__":
    main()
