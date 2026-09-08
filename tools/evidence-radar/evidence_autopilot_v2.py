#!/usr/bin/env python3
"""
174 — Evidence Radar Autopilot v2
Adds refined herbal medicine to pharmacopuncture/acupuncture/electroacupuncture.
Internal only. Does not write docs/.
"""
import argparse,json,re
from pathlib import Path
import logging
from functools import lru_cache
from datetime import datetime

SOURCES=[
 ("pharmacopuncture",["evidence-pharmacopuncture-clinical.json","evidence-radar-work/pharmacopuncture/evidence-pharmacopuncture-clinical.json"]),
 ("acupuncture",["evidence-radar-work/acupuncture-final/acupuncture-final.json"]),
 ("electroacupuncture",["evidence-radar-work/electroacupuncture-refined/electroacupuncture-refined.json"]),
 ("herbal-medicine",["evidence-radar-work/herbal-medicine-refined/herbal-medicine-refined.json"])
]
BAD=["retraction","retracted","withdrawn","comment on ","editorial","corrigendum","erratum"]

def first(paths):
    for value in paths:
        path = Path(value)
        if not path.exists():
            continue
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(rows, list):
                raise ValueError("expected record list")
            scalar_fields = ("title", "doi", "pmid", "study_type", "evidence_level", "kcd_mapping_status")
            valid = [row for row in rows if isinstance(row, dict)
                     and all(row.get(key) is None or isinstance(row.get(key), (str, int, float)) for key in scalar_fields)
                     and (row.get("keywords") is None or isinstance(row.get("keywords"), list))
                     and all(row.get(key) is None or isinstance(row.get(key), dict)
                             for key in ("modality_final", "electrical_modality_final"))]
            if len(valid) != len(rows):
                logging.warning("Invalid Evidence Radar records skipped: %s", path.name)
            return valid, str(path)
        except (OSError, ValueError) as error:
            logging.warning("Evidence Radar source unavailable: %s [%s]", path.name, type(error).__name__)
            return [], str(path)
    return [], None

def nt(s):return re.sub(r"[^a-z0-9가-힣]+"," ",str(s).lower()).strip()
def ident(r):
    if r.get("doi"):return "doi:"+str(r["doi"]).lower()
    if r.get("pmid"):return "pmid:"+str(r["pmid"])
    return "title:"+nt(r.get("title"))
def ids(r):return [x for x in [str(r.get("doi") or "").lower().strip(),str(r.get("pmid") or "").strip()] if x]
def resolve(root, path):
    if not isinstance(path, str) or not path:
        return None
    rel = path.strip("/")
    if any(part == ".." for part in rel.split("/")) or any(c in rel for c in "\\:*?[]\x00"):
        return None
    root = Path(root)
    candidates = [root / (rel + ".md"), root / rel / "index.md",
                  root / "authority" / (rel + ".md"), root / "authority" / rel / "index.md"]
    for candidate in candidates:
        if candidate.resolve().is_relative_to(root.resolve()) and candidate.is_file():
            return candidate
    hits = [p for p in root.rglob(Path(rel).name + ".md")
            if p.resolve().is_relative_to(root.resolve()) and p.is_file()]
    return hits[0] if len(hits) == 1 else None

def mappings(kind,r):
    if kind=="herbal-medicine":
        return r.get("kcd_candidates") if isinstance(r.get("kcd_candidates"), list) else []
    value = r.get("kcd_candidates_refined") or r.get("kcd_candidates") or []
    return value if isinstance(value, list) else []
def modality_ok(kind,r):
    if kind=="acupuncture":return (r.get("modality_final") if isinstance(r.get("modality_final"), dict) else {}).get("primary","manual")=="manual"
    if kind=="electroacupuncture":return (r.get("electrical_modality_final") if isinstance(r.get("electrical_modality_final"), dict) else {}).get("primary")=="needle-electroacupuncture"
    if kind=="pharmacopuncture":
        t=(str(r.get("title",""))+" "+" ".join(map(str,(r.get("keywords") or [])))).lower()
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
    if not docs.is_dir(): ap.error("docs directory does not exist")
    resolve_cached = lru_cache(maxsize=4096)(lambda path: resolve(docs, path))
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
                p=resolve_cached(m.get("archive_path")) if isinstance(m, dict) and isinstance(m.get("archive_path"), str) else None
                if p:target=str(p.relative_to(docs)).replace("\\","/");break
            rs=reasons(kind,r,target)
            item={**r,"kind":kind,"target":target,"reasons":rs,"approved":False}
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
