#!/usr/bin/env python3
"""
169 — Electroacupuncture definition refinement

Input:
  evidence-radar-work/electroacupuncture/electroacupuncture-clinical.json

Goal:
- keep true needle-based electroacupuncture
- separate TEAS/TENS/NMES/FES/peripheral electrical stimulation
- separate auricular electrical stimulation when no needle-based EA is clear
- mark combination electrical interventions as mixed-electrical
- prevent one study from being mapped to unrelated conditions only because keywords mention them
- completed A/B evidence and protocols remain separated
- internal output only; never writes docs/
"""
import argparse, json, re
from pathlib import Path
from collections import defaultdict, Counter

EA_NEEDLE=[
    "electroacupuncture","electro-acupuncture","electro acupuncture",
    "electroacupuncture needle","electro-acupuncture needle",
    "전침","電鍼"
]

NON_NEEDLE=[
    "transcutaneous electrical acupoint stimulation","teas",
    "transcutaneous electrical nerve stimulation","tens",
    "neuromuscular electrical stimulation","nmes",
    "functional electrical stimulation","fes",
    "peripheral electrical stimulation",
    "acupoint electrical stimulation",
    "electrical acupoint stimulation",
    "low-frequency acupoint electrical stimulation",
    "electrical stimulation"
]

AURICULAR_ELECTRICAL=[
    "auricular electroacupuncture",
    "auricular electrical stimulation",
    "ear electroacupuncture"
]

def content(r):
    # journal deliberately excluded
    return (" ".join([
        str(r.get("title","")),
        " ".join(map(str,r.get("keywords",[])))
    ])).lower()

def title(r):
    return str(r.get("title","")).lower()

def has_any(txt, terms):
    return any(x.lower() in txt for x in terms)

def classify_modality(r):
    t=content(r); ti=title(r)
    needle=has_any(t,EA_NEEDLE)
    nonneedle=has_any(t,NON_NEEDLE)
    auricular=has_any(t,AURICULAR_ELECTRICAL)

    # strongest signal: title explicitly says electroacupuncture
    explicit_title_ea=has_any(ti,["electroacupuncture","electro-acupuncture","electro acupuncture","전침","電鍼"])

    # If title is only generic electrical stimulation and never explicitly says EA,
    # do not call it electroacupuncture.
    generic_title=has_any(ti,NON_NEEDLE) and not explicit_title_ea

    if generic_title:
        primary="non-needle-electrical"
    elif explicit_title_ea and nonneedle:
        primary="mixed-electrical"
    elif explicit_title_ea and auricular and "auricular electroacupuncture" in ti:
        primary="auricular-electroacupuncture"
    elif explicit_title_ea:
        primary="needle-electroacupuncture"
    elif needle and nonneedle:
        primary="mixed-electrical"
    elif needle:
        primary="needle-electroacupuncture"
    elif auricular:
        primary="auricular-electroacupuncture"
    elif nonneedle:
        primary="non-needle-electrical"
    else:
        primary="unclear"

    return {
        "primary":primary,
        "needle_electroacupuncture":needle,
        "non_needle_electrical":nonneedle,
        "auricular_electrical":auricular
    }

def normalize_condition_mapping(r):
    """
    Reduce obvious over-mapping. Keep mapped conditions that appear in title.
    If none survive, retain original mapping but mark it uncertain.
    """
    ti=title(r)
    kept=[]
    for k in r.get("kcd_candidates",[]):
        label=str(k.get("label","")).lower()
        code=str(k.get("code",""))
        aliases={
          "불면":["insomnia","sleep"],
          "우울증":["depression","depressive"],
          "불안장애":["anxiety"],
          "뇌졸중/뇌경색":["stroke","post-stroke","poststroke"],
          "요통":["low back pain","lumbar pain"],
          "다낭성난소증후군":["polycystic","pcos"],
          "긴장형두통":["tension-type headache","tension headache"],
          "섬유근육통":["fibromyalgia"]
        }
        terms=aliases.get(k.get("label"),[])
        if not terms or any(x in ti for x in terms):
            kept.append(k)
    if kept:
        r["kcd_candidates_refined"]=kept
        r["kcd_mapping_status"]="title-supported"
    else:
        r["kcd_candidates_refined"]=r.get("kcd_candidates",[])
        r["kcd_mapping_status"]="needs-review"
    return r

def completed_ab(r):
    return r.get("evidence_level") in {"A","B"} and r.get("study_type") not in {"RCT protocol","SR/MA protocol"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir",default="evidence-radar-work/electroacupuncture-refined")
    args=ap.parse_args()

    rows=json.loads(Path(args.input).read_text(encoding="utf-8"))
    needle=[]; mixed=[]; nonneedle=[]; unclear=[]

    for r in rows:
        r["electrical_modality_final"]=classify_modality(r)
        r=normalize_condition_mapping(r)
        p=r["electrical_modality_final"]["primary"]
        if p in {"needle-electroacupuncture","auricular-electroacupuncture"}:
            needle.append(r)
        elif p=="mixed-electrical":
            mixed.append(r)
        elif p=="non-needle-electrical":
            nonneedle.append(r)
        else:
            unclear.append(r)

    completed=[r for r in needle if completed_ab(r)]
    protocols=[r for r in needle if r.get("evidence_level")=="P"]
    groups=defaultdict(list)
    for r in completed:
        for k in r.get("kcd_candidates_refined",[]):
            groups[k.get("label","미분류")].append(r)

    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    (out/"electroacupuncture-refined.json").write_text(json.dumps(needle,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"electroacupuncture-mixed-electrical.json").write_text(json.dumps(mixed,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"electroacupuncture-non-needle-electrical.json").write_text(json.dumps(nonneedle,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"electroacupuncture-unclear.json").write_text(json.dumps(unclear,ensure_ascii=False,indent=2),encoding="utf-8")

    md=["# Electroacupuncture Evidence Radar — Refined Definition","",
        f"- 입력: {len(rows)}건",
        f"- 진짜 전침/이침전기자극 후보: {len(needle)}건",
        f"- mixed-electrical: {len(mixed)}건",
        f"- 비침습 전기자극 분리: {len(nonneedle)}건",
        f"- 불명확: {len(unclear)}건",
        f"- 완료 A/B 전침 근거: {len(completed)}건",
        f"- protocol 추적: {len(protocols)}건","",
        "> 내부 검토용입니다. docs/ 자동 게시 없음.","",
        "## 정의","",
        "- needle-electroacupuncture: 침을 삽입한 상태에서 전기자극을 가하는 전침",
        "- auricular-electroacupuncture: 이침 기반 전기자극",
        "- mixed-electrical: 전침과 TEAS/TENS/기타 전기자극이 함께 포함",
        "- non-needle-electrical: TEAS/TENS/NMES/FES/단순 경혈 전기자극 등",
        "",
        "## 질환별 완료 A/B 전침 근거",""]
    for label,recs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            ident=("PMID "+str(r.get("pmid"))) if r.get("pmid") else ("DOI "+str(r.get("doi")) if r.get("doi") else "-")
            md.append(f"- [{r.get('evidence_level')}/{r['electrical_modality_final']['primary']}] {r.get('title')} — {ident}")
        md.append("")

    md += ["## mixed-electrical 검토 큐",""]
    for r in mixed:
        md.append(f"- [{r.get('evidence_level')}] {r.get('title')} — {r.get('doi') or r.get('pmid') or '-'}")

    (out/"electroacupuncture-refined-review.md").write_text("\n".join(md),encoding="utf-8")

    counts=Counter(r["electrical_modality_final"]["primary"] for r in rows)
    print("modality counts:",dict(counts))
    print(f"completed A/B true-EA: {len(completed)}; protocols: {len(protocols)}")
    print(f"internal output -> {out}")

if __name__=="__main__":
    main()
