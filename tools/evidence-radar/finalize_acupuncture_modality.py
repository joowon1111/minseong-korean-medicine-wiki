#!/usr/bin/env python3
"""
164 — Acupuncture modality final refinement

Input:
  evidence-radar-work/acupuncture-refined/acupuncture-refined.json
  evidence-radar-work/acupuncture-refined/acupuncture-excluded.json

Purpose:
- Do NOT use journal name to infer treatment modality.
- Rescue genuine acupuncture reviews incorrectly excluded merely because keywords mention electroacupuncture.
- Classify modality as manual / mixed / electro / pharmacopuncture / acupotomy / other.
- Keep completed A/B evidence separate from protocols.
- Internal output only. Never writes to docs/.
"""
import argparse, json, re
from pathlib import Path
from collections import defaultdict

EA=["electroacupuncture","electro-acupuncture","electrical acupuncture","전침","電鍼"]
PA=["pharmacopuncture","pharmacoacupuncture","약침","봉침","bee venom injection"]
AC=["acupotomy","needle knife","acupotome","도침","침도","鍼刀"]
MANUAL=["manual acupuncture","body acupuncture","acupuncture treatment","acupuncture therapy",
        "침 치료","침치료","鍼治療","intradermal acupuncture","피내침","warm acupuncture","온침"]

def content(r):
    # Deliberately excludes journal name.
    return (" ".join([str(r.get("title","")), " ".join(map(str,r.get("keywords",[])))])).lower()

def title(r): return str(r.get("title","")).lower()

def has_any(txt,terms): return any(x.lower() in txt for x in terms)

def modality(r):
    t=content(r); ti=title(r)
    ea=has_any(t,EA); pa=has_any(t,PA); ac=has_any(t,AC)
    manual=has_any(t,MANUAL) or ("acupuncture" in ti and not ti.startswith("pharmacoacupuncture"))
    # Title has highest weight for primary intervention.
    title_ea=has_any(ti,EA)
    title_pa=has_any(ti,PA)
    title_ac=has_any(ti,AC)
    title_manual=("acupuncture" in ti and not title_ea and not title_pa and not title_ac) or has_any(ti,MANUAL)

    if title_pa and not title_manual: primary="pharmacopuncture"
    elif title_ac and not title_manual: primary="acupotomy"
    elif title_ea and not title_manual: primary="electroacupuncture"
    elif title_manual and (ea or pa or ac): primary="mixed"
    elif title_manual: primary="manual"
    elif manual and (ea or pa or ac): primary="mixed"
    elif manual: primary="manual"
    elif ea: primary="electroacupuncture"
    elif pa: primary="pharmacopuncture"
    elif ac: primary="acupotomy"
    else: primary="other"
    return {"primary":primary,"manual":manual,"electroacupuncture":ea,
            "pharmacopuncture":pa,"acupotomy":ac}

def key(r):
    d=str(r.get("doi") or "").strip().lower()
    if d:return "doi:"+d
    return "title:"+re.sub(r"\W+"," ",title(r)).strip()

def is_completed_ab(r):
    return r.get("evidence_level") in {"A","B"} and r.get("study_type") not in {"RCT protocol","SR/MA protocol"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("kept")
    ap.add_argument("excluded")
    ap.add_argument("--outdir",default="evidence-radar-work/acupuncture-final")
    args=ap.parse_args()

    kept=json.loads(Path(args.kept).read_text(encoding="utf-8"))
    excluded=json.loads(Path(args.excluded).read_text(encoding="utf-8"))

    # Only reconsider modality exclusions. Retractions/comments remain permanently excluded.
    rescue_pool=[r for r in excluded if r.get("refine_exclusion_reason") in
                 {"electroacupuncture-only","pharmacopuncture-only","acupotomy-only"}]

    combined=[]; seen=set(); rescued=[]
    for r in kept + rescue_pool:
        m=modality(r); r["modality_final"]=m
        # manual and mixed are allowed in acupuncture evidence; mixed is labeled explicitly.
        if m["primary"] not in {"manual","mixed"}: continue
        k=key(r)
        if k in seen: continue
        seen.add(k)
        if r in rescue_pool: rescued.append(r)
        combined.append(r)

    completed=[r for r in combined if is_completed_ab(r)]
    protocols=[r for r in combined if r.get("evidence_level")=="P"]
    groups=defaultdict(list)
    for r in completed:
        for x in r.get("kcd_candidates",[]):
            groups[x.get("label","미분류")].append(r)

    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    (out/"acupuncture-final.json").write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"acupuncture-rescued.json").write_text(json.dumps(rescued,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Acupuncture Evidence Radar — Final Modality Review","",
        f"- 최종 침/복합침 후보: {len(combined)}건",
        f"- 163에서 복구된 연구: {len(rescued)}건",
        f"- 완료 A/B 근거: {len(completed)}건",
        f"- protocol 추적: {len(protocols)}건","",
        "> 내부 검토용. docs/ 자동 게시 없음.","",
        "## Modality 원칙","",
        "- 저널명은 modality 판정에 사용하지 않음",
        "- 제목을 가장 강하게 반영",
        "- 순수 침: manual",
        "- 침과 전침·기타 침법을 함께 비교/포함: mixed",
        "- 전침/약침/도침 단독: 각 전용 Radar에서 처리","",
        "## 질환별 완료 A/B 근거",""]
    for label,recs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            ident=("PMID "+str(r.get("pmid"))) if r.get("pmid") else ("DOI "+str(r.get("doi")) if r.get("doi") else "-")
            md.append(f"- [{r.get('evidence_level')}/{r['modality_final']['primary']}] {r.get('title')} — {ident}")
        md.append("")
    md += ["## 163에서 복구된 연구",""]
    for r in rescued:
        md.append(f"- [{r.get('evidence_level')}/{r['modality_final']['primary']}] {r.get('title')} — {r.get('doi') or r.get('pmid') or '-'}")

    (out/"acupuncture-final-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"final {len(combined)} -> rescued {len(rescued)} -> completed A/B {len(completed)} -> protocols {len(protocols)}")

if __name__=="__main__":
    main()
