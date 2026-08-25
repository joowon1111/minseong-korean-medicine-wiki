#!/usr/bin/env python3
"""
174 — Evidence Radar Autopilot v2
Adds refined herbal medicine to pharmacopuncture/acupuncture/electroacupuncture.
Internal only. Does not write docs/.
"""
import argparse,json,re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

SOURCES=[
 ("pharmacopuncture",["evidence-pharmacopuncture-clinical.json","evidence-radar-work/pharmacopuncture/evidence-pharmacopuncture-clinical.json"]),
 ("acupuncture",["evidence-radar-work/acupuncture-final/acupuncture-final.json"]),
 ("electroacupuncture",["evidence-radar-work/electroacupuncture-refined/electroacupuncture-refined.json"]),
 ("herbal-medicine",["evidence-radar-work/herbal-medicine-refined/herbal-medicine-refined.json"])
]
BAD=["retraction","retracted","withdrawn","comment on ","editorial","corrigendum","erratum"]

def first(paths):
    for x in paths:
        p=Path(x)
        if p.exists():
            try:return json.loads(p.read_text(encoding="utf-8")),str(p)
            except:return [],str(p)
    return [],None
def nt(s):return re.sub(r"[^a-z0-9가-힣]+"," ",str(s).lower()).strip()
def ident(r):
    if r.get("doi"):return "doi:"+str(r["doi"]).lower()
    if r.get("pmid"):return "pmid:"+str(r["pmid"])
    return "title:"+nt(r.get("title"))
def ids(r):return [x for x in [str(r.get("doi") or "").lower().strip(),str(r.get("pmid") or "").strip()] if x]
def resolve(root,path):
    if not path:return None
    rel=path.strip("/")
    for p in [Path(root)/(rel+".md"),Path(root)/rel/"index.md",Path(root)/"authority"/(rel+".md"),Path(root)/"authority"/rel/"index.md"]:
        if p.exists():return p
    base=Path(rel).name
    hits=list(Path(root).rglob(base+".md"))
    return hits[0] if len(hits)==1 else None
def mappings(kind,r):
    if kind=="herbal-medicine":
        return r.get("kcd_candidates",[])
    return r.get("kcd_candidates_refined") or r.get("kcd_candidates") or []
def modality_ok(kind,r):
    if kind=="acupuncture":return r.get("modality_final",{}).get("primary","manual")=="manual"
    if kind=="electroacupuncture":return r.get("electrical_modality_final",{}).get("primary")=="needle-electroacupuncture"
    if kind=="pharmacopuncture":
        t=(str(r.get("title",""))+" "+" ".join(map(str,r.get("keywords",[])))).lower()
        return "pharmacopuncture" in t or "pharmacoacupuncture" in t or "약침" in t
    if kind=="herbal-medicine":
        return not bool(r.get("refine_reasons"))
    return False
def reasons(kind,r,target):
    t=str(r.get("title","")).lower(); rs=[]
    if any(x in t for x in BAD):rs.append("unsafe-publication-type")
    if r.get("study_type") in {"RCT protocol","SR/MA protocol"} or r.get("evidence_level")=="P":rs.append("protocol")
    if r.get("evidence_level") not in {"A","B"}:rs.append("not-A/B")
    if not modality_ok(kind,r):rs.append("modality-or-refine-hold")
    if not target:rs.append("target-missing")
    if str(r.get("doi") or "").lower().startswith(("10.21203/","10.1101/")):rs.append("preprint")
    return list(dict.fromkeys(rs))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--docs",default="docs");ap.add_argument("--outdir",default="evidence-radar-work/autopilot")
    a=ap.parse_args();docs=Path(a.docs)
    alltext="\n".join(p.read_text(encoding="utf-8-sig",errors="ignore").lower() for p in docs.rglob("*.md"))
    seen=set(); cand=[]; hold=[]; existing=[]; status=[]
    for kind,paths in SOURCES:
        rows,used=first(paths);status.append({"kind":kind,"path":used,"records":len(rows)})
        for r in rows:
            k=ident(r)
            if k in seen:continue
            seen.add(k)
            if ids(r) and any(x in alltext for x in ids(r)):
                existing.append({"kind":kind,**r});continue
            target=None
            for m in mappings(kind,r):
                p=resolve(docs,m.get("archive_path"))
                if p:target=str(p.relative_to(docs)).replace("\\","/");break
            rs=reasons(kind,r,target)
            item={"kind":kind,"target":target,"reasons":rs,"approved":False,**r}
            (hold if rs else cand).append(item)
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    for n,data in [("high-confidence-candidates",cand),("hold-queue",hold),("already-existing",existing),("source-status",status)]:
        (out/f"{n}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"AUTOPILOT-SUMMARY.md").write_text(
        "# Evidence Radar Autopilot v2\n\n"+
        f"- 실행: {datetime.now().isoformat(timespec='seconds')}\n"+
        f"- 고신뢰 신규 후보: {len(cand)}건\n- 내부 보류: {len(hold)}건\n- 기존 근거: {len(existing)}건\n\n"+
        "\n".join(f"- {s['kind']}: {s['records']}건 ({s['path'] or 'not found'})" for s in status),
        encoding="utf-8")
    print(f"AUTOPILOT v2 -> candidates {len(cand)} | hold {len(hold)} | existing {len(existing)}")
if __name__=="__main__":main()
