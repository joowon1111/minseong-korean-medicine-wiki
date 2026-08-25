#!/usr/bin/env python3
"""
172 — Evidence Radar Autopilot
Unifies reviewed pharmacopuncture/acupuncture/electroacupuncture outputs.

Purpose:
- no more manual stage-by-stage filtering
- compare against current docs
- high-confidence direct evidence -> proposed patches
- ambiguous evidence -> internal hold queue
- NEVER edits docs automatically by default
- optional --apply-reviewed only applies candidates marked approved=true
"""
import argparse,json,re,hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

SOURCES=[
 ("pharmacopuncture",[
   "evidence-pharmacopuncture-clinical.json",
   "evidence-radar-work/pharmacopuncture/evidence-pharmacopuncture-clinical.json"
 ]),
 ("acupuncture",[
   "evidence-radar-work/acupuncture-final/acupuncture-final.json"
 ]),
 ("electroacupuncture",[
   "evidence-radar-work/electroacupuncture-refined/electroacupuncture-refined.json"
 ])
]

BAD_TITLE=["retraction","retracted","withdrawn","comment on ","editorial","corrigendum","erratum"]
PROTOCOL={"RCT protocol","SR/MA protocol"}
DIRECT_LEVEL={"A","B"}

def read_first(paths):
    for x in paths:
        p=Path(x)
        if p.exists():
            try:return json.loads(p.read_text(encoding="utf-8")),str(p)
            except Exception:return [],str(p)
    return [],None

def norm_title(s):return re.sub(r"[^a-z0-9가-힣]+"," ",str(s).lower()).strip()
def ident(r):
    d=str(r.get("doi") or "").strip().lower()
    if d:return "doi:"+d
    p=str(r.get("pmid") or "").strip()
    if p:return "pmid:"+p
    return "title:"+norm_title(r.get("title"))

def ids(r):
    return [x for x in [str(r.get("doi") or "").lower().strip(),str(r.get("pmid") or "").strip()] if x]

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

def mappings(r):
    return r.get("kcd_candidates_refined") or r.get("kcd_candidates") or []

def modality_ok(kind,r):
    title=str(r.get("title","")).lower()
    if kind=="acupuncture":
        return r.get("modality_final",{}).get("primary","manual")=="manual"
    if kind=="electroacupuncture":
        return r.get("electrical_modality_final",{}).get("primary")=="needle-electroacupuncture"
    if kind=="pharmacopuncture":
        return "pharmacopuncture" in title or "약침" in " ".join(map(str,r.get("keywords",[]))) or "pharmacoacupuncture" in title
    return False

def quality_reasons(kind,r,target):
    reasons=[]
    title=str(r.get("title","")).lower()
    if any(x in title for x in BAD_TITLE):reasons.append("unsafe-publication-type")
    if r.get("study_type") in PROTOCOL or r.get("evidence_level")=="P":reasons.append("protocol")
    if r.get("evidence_level") not in DIRECT_LEVEL:reasons.append("not-A/B")
    if not modality_ok(kind,r):reasons.append("modality-not-direct")
    if not target:reasons.append("target-missing")
    if r.get("kcd_mapping_status") and r.get("kcd_mapping_status")!="title-supported":
        reasons.append("condition-mapping-review")
    if any(x in title for x in [
        "different methods","different acupuncture","network meta-analysis",
        "different interventions","nonpharmacological methods","physical stimulation",
        "combined with","combining ","adjuvant therapy","versus battle field"
    ]):reasons.append("indirect-or-combination")
    if str(r.get("doi") or "").lower().startswith("10.21203/"):reasons.append("preprint")
    return reasons

def block(kind,r):
    label={"pharmacopuncture":"약침","acupuncture":"침","electroacupuncture":"전침"}[kind]
    st=r.get("study_type","임상연구")
    date=r.get("published_date","")
    idtxt=" · ".join(([f"PMID `{r['pmid']}`"] if r.get("pmid") else [])+
                     ([f"DOI `{r['doi']}`"] if r.get("doi") else []))
    return f"""### {label} 최신 임상근거

- **{r.get('title','')}** — {date} {st}. {label} 치료와 해당 질환의 임상적 연관성을 평가한 최근 연구입니다. {idtxt}

> Evidence Radar 자동 후보입니다. 원문 결과값을 임의로 추정하지 않으며, 공개 반영 전 식별자·대상 질환·중재의 직접성을 확인합니다.
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--docs",default="docs")
    ap.add_argument("--outdir",default="evidence-radar-work/autopilot")
    args=ap.parse_args()

    docs=Path(args.docs)
    md=list(docs.rglob("*.md"))
    alltext="\n".join(p.read_text(encoding="utf-8-sig",errors="ignore").lower() for p in md)
    seen=set(); candidates=[]; holds=[]; existing=[]; source_status=[]

    for kind,paths in SOURCES:
        rows,used=read_first(paths)
        source_status.append({"kind":kind,"path":used,"records":len(rows)})
        for r in rows:
            k=ident(r)
            if k in seen:continue
            seen.add(k)
            if ids(r) and any(x in alltext for x in ids(r)):
                existing.append({"kind":kind,**r});continue
            target=None
            for m in mappings(r):
                p=resolve(docs,m.get("archive_path"))
                if p:
                    target=str(p.relative_to(docs)).replace("\\","/");break
            reasons=quality_reasons(kind,r,target)
            item={"kind":kind,"target":target,"reasons":reasons,
                  "approved":False,**r}
            if reasons:holds.append(item)
            else:candidates.append(item)

    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    for n,data in [("high-confidence-candidates",candidates),("hold-queue",holds),
                   ("already-existing",existing),("source-status",source_status)]:
        (out/f"{n}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")

    # proposed patches are internal, not docs
    patchdir=out/"proposed-patches";patchdir.mkdir(exist_ok=True)
    grouped=defaultdict(list)
    for r in candidates:grouped[(r["kind"],r["target"])].append(r)
    for (kind,target),rs in grouped.items():
        name=target.replace("/","__")+".md"
        txt=[f"# Proposed patch → {target}","",
             "> 내부 검토용. 이 파일 자체는 공개 docs가 아닙니다.",""]
        for r in rs:txt.append(block(kind,r))
        (patchdir/name).write_text("\n".join(txt),encoding="utf-8")

    summary=["# Evidence Radar Autopilot","",
             f"- 실행: {datetime.now().isoformat(timespec='seconds')}",
             f"- 고신뢰 신규 후보: {len(candidates)}건",
             f"- 내부 보류: {len(holds)}건",
             f"- 기존 식별자 발견: {len(existing)}건","",
             "## 소스 상태",""]
    for s in source_status:summary.append(f"- {s['kind']}: {s['records']}건 ({s['path'] or 'not found'})")
    summary += ["","## 운영 원칙","",
                "- 사용자가 논문을 한 건씩 분류하지 않음",
                "- A/B + 직접 modality + 기존 질환페이지 + 신규 식별자를 우선 후보화",
                "- protocol/preprint/복합중재/간접근거/불확실 매핑은 자동 보류",
                "- 후보 패치는 내부에만 생성",
                "- 실제 docs 반영은 검토된 batch에서만 수행"]
    (out/"AUTOPILOT-SUMMARY.md").write_text("\n".join(summary),encoding="utf-8")
    print(f"AUTOPILOT -> candidates {len(candidates)} | hold {len(holds)} | existing {len(existing)}")
    print(out)

if __name__=="__main__":main()
