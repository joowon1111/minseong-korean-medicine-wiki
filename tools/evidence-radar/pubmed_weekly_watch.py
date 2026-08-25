#!/usr/bin/env python3
"""
176 — Minseong Evidence Radar: PubMed Weekly Watch

Directly checks PubMed for newly indexed studies and creates an internal batch:
PubMed -> modality classification -> safety filter -> study type -> DOI/PMID dedupe
-> archive target mapping -> high-confidence candidate / hold queue.

IMPORTANT:
- Does NOT edit docs/.
- Does NOT auto-commit public medical content.
- Output stays under evidence-radar-work/pubmed-watch/ and is uploaded as a
  GitHub Actions artifact.
"""

import argparse, json, re, time, urllib.parse, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from datetime import date, timedelta, datetime
from pathlib import Path
from collections import defaultdict

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

QUERIES = {
    "pharmacopuncture": (
        '("pharmacopuncture"[Title/Abstract] OR "pharmacoacupuncture"[Title/Abstract] '
        'OR "bee venom acupuncture"[Title/Abstract])'
    ),
    "acupuncture": (
        '("acupuncture"[Title/Abstract] OR "manual acupuncture"[Title/Abstract])'
    ),
    "electroacupuncture": (
        '("electroacupuncture"[Title/Abstract] OR "electro-acupuncture"[Title/Abstract] '
        'OR "electro acupuncture"[Title/Abstract])'
    ),
    "herbal-medicine": (
        '("herbal medicine"[Title/Abstract] OR "Chinese herbal medicine"[Title/Abstract] '
        'OR "East Asian herbal medicine"[Title/Abstract] OR decoction[Title/Abstract] '
        'OR "herbal formula"[Title/Abstract])'
    ),
}

BAD = [
    "retraction of", "retracted:", "withdrawn", "withdrawal notice",
    "comment on", "editorial", "corrigendum", "erratum"
]
PROTOCOL = ["protocol", "study protocol"]

EA = ["electroacupuncture", "electro-acupuncture", "electro acupuncture"]
PA = ["pharmacopuncture", "pharmacoacupuncture", "bee venom acupuncture"]
ACUPOTOMY = ["acupotomy", "needle knife", "acupotome"]
NON_NEEDLE_ELECTRICAL = [
    "transcutaneous electrical acupoint stimulation", "teas",
    "transcutaneous electrical nerve stimulation", "tens",
    "neuromuscular electrical stimulation", "nmes",
    "functional electrical stimulation", "fes",
    "peripheral electrical stimulation"
]

HERBAL_EAST_ASIAN = [
    "chinese herbal medicine", "east asian herbal medicine", "traditional chinese medicine",
    "decoction", "herbal formula", "granule", "kampo", "korean medicine"
]
HERBAL_HOLD = [
    "foot bath", "bath therapy", "nasal irrigation", "mouthwash", "nebulized",
    "nebulised", "topical", "injection", "injectable", "network pharmacology",
    "molecular docking", "bibliometric", "evidence map", "prevalence",
    "traditional persian", "thai herbal", "ayurvedic", "indian herbal"
]

# Conservative disease map. More can be added later without changing the workflow.
CONDITIONS = [
    (["low back pain", "chronic low back pain"], "M54", "요통", "conditions/low-back-pain/"),
    (["knee osteoarthritis"], "M17", "무릎 골관절염", "conditions/knee-osteoarthritis/"),
    (["frozen shoulder", "adhesive capsulitis"], "M75.0", "유착성 관절낭염", "conditions/frozen-shoulder/"),
    (["rotator cuff"], "M75.1", "회전근개 질환", "conditions/rotator-cuff-disease/"),
    (["migraine"], "G43", "편두통", "conditions/migraine/"),
    (["tension-type headache", "tension headache"], "G44.2", "긴장형두통", "conditions/tension-type-headache/"),
    (["insomnia"], "G47", "불면", "conditions/insomnia/"),
    (["anxiety disorder", "generalized anxiety"], "F41", "불안장애", "conditions/anxiety/"),
    (["depression", "major depressive disorder"], "F32", "우울증", "conditions/depression/"),
    (["functional dyspepsia"], "K30", "기능성소화불량", "conditions/functional-dyspepsia/"),
    (["irritable bowel syndrome", "ibs-d"], "K58", "과민성장증후군", "conditions/irritable-bowel-syndrome/"),
    (["constipation"], "K59.0", "변비", "conditions/constipation/"),
    (["atopic dermatitis"], "L20", "아토피피부염", "conditions/atopic-dermatitis/"),
    (["allergic rhinitis"], "J30", "알레르기비염", "conditions/allergic-rhinitis/"),
    (["primary dysmenorrhea"], "N94", "원발성 생리통", "conditions/primary-dysmenorrhea/"),
    (["polycystic ovary syndrome", "pcos"], "E28.2", "다낭성난소증후군", "conditions/polycystic-ovary-syndrome/"),
    (["stroke", "post-stroke", "poststroke"], "I63", "뇌졸중/뇌경색", "conditions/stroke/"),
    (["bell's palsy", "bell palsy"], "G51.0", "벨마비", "conditions/bell-palsy/"),
]

FORMULAS = [
    (["guipi decoction", "gui pi tang", "guipi tang"], "귀비탕", "formulas/guibi-tang/"),
    (["buzhong yiqi", "bu zhong yi qi"], "보중익기탕", "formulas/bojungikgi-tang/"),
    (["duhuo jisheng", "du huo ji sheng", "duhuo-jisheng"], "독활기생탕", "formulas/dokhwalgi-saeng-tang/"),
    (["sijunzi", "si jun zi"], "사군자탕", "formulas/sagunja-tang/"),
    (["liujunzi", "liu jun zi"], "육군자탕", "formulas/yukgunja-tang/"),
    (["xiangsha liujunzi", "xiangsha liujun"], "향사육군자탕", "formulas/xiangsha-liujunzi-tang/"),
    (["wendan decoction", "wen dan tang"], "온담탕", "formulas/ondam-tang/"),
    (["tongxie yaofang"], "통사요방", "formulas/tongxie-yaofang/"),
    (["huoxiang zhengqi"], "곽향정기산", "formulas/huoxiang-zhengqi-san/"),
    (["xuefu zhuyu"], "혈부축어탕", "formulas/xuefu-zhuyu-tang/"),
    (["banxia shumi"], "반하서미탕", "formulas/banxia-shumi-tang/"),
]

def request(url, params, retries=4):
    full = url + "?" + urllib.parse.urlencode(params)
    errors = []
    for i in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                full,
                headers={"User-Agent": "Minseong-Evidence-Radar-PubMed-Watch/1.0"}
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), errors
        except Exception as e:
            errors.append({"attempt": i, "error": str(e), "url": full})
            if i < retries:
                time.sleep(3 * i)
    return None, errors

def text_of(node):
    if node is None:
        return ""
    return "".join(node.itertext()).strip()

def study_type(title, abstract, pubtypes):
    t = (title + " " + abstract + " " + " ".join(pubtypes)).lower()
    if "protocol" in t and ("systematic review" in t or "meta-analysis" in t):
        return "SR/MA protocol"
    if "systematic review" in t and "meta-analysis" in t:
        return "Systematic review & meta-analysis"
    if "systematic review" in t:
        return "Systematic review"
    if "meta-analysis" in t:
        return "Meta-analysis"
    if "protocol" in t and ("randomized" in t or "randomised" in t):
        return "RCT protocol"
    if ("randomized controlled trial" in t or "randomised controlled trial" in t
            or "randomized clinical trial" in t):
        return "RCT"
    if "clinical trial" in t:
        return "Clinical trial"
    if "cohort" in t:
        return "Cohort study"
    if "case-control" in t:
        return "Case-control study"
    return "Other human study"

def evidence_level(st):
    if st in {"Systematic review & meta-analysis", "Systematic review", "Meta-analysis"}:
        return "A"
    if st in {"RCT", "Clinical trial"}:
        return "B"
    if st in {"RCT protocol", "SR/MA protocol"}:
        return "P"
    return "C"

def map_conditions(t):
    out = []
    for terms, code, label, path in CONDITIONS:
        if any(x in t for x in terms):
            out.append({"code": code, "label": label, "archive_path": path})
    return out

def map_formulas(t):
    out = []
    for terms, label, path in FORMULAS:
        if any(x in t for x in terms):
            out.append({"label": label, "archive_path": path})
    return out

def resolve_target(docs, mappings):
    for m in mappings:
        rel = m.get("archive_path", "").strip("/")
        for p in [
            docs / (rel + ".md"),
            docs / rel / "index.md",
            docs / "authority" / (rel + ".md"),
            docs / "authority" / rel / "index.md"
        ]:
            if p.exists():
                return str(p.relative_to(docs)).replace("\\", "/")
    return None

def modality_reasons(kind, t):
    rs = []
    if kind == "pharmacopuncture":
        if not any(x in t for x in PA):
            rs.append("pharmacopuncture-not-direct")
    elif kind == "acupuncture":
        if any(x in t for x in PA + EA + ACUPOTOMY):
            rs.append("acupuncture-mixed-or-other-modality")
    elif kind == "electroacupuncture":
        if not any(x in t for x in EA):
            rs.append("electroacupuncture-not-direct")
        if any(x in t for x in NON_NEEDLE_ELECTRICAL) and not any(x in t for x in EA):
            rs.append("non-needle-electrical")
    elif kind == "herbal-medicine":
        if not any(x in t for x in HERBAL_EAST_ASIAN):
            rs.append("east-asian-herbal-signal-weak")
        if any(x in t for x in HERBAL_HOLD):
            rs.append("herbal-route-or-methodology-hold")
        if "acupuncture" in t and ("combined" in t or "plus" in t):
            rs.append("herbal-other-modality-combination")
    return rs

def fetch_kind(kind, query, mindate, maxdate, retmax):
    term = f'({query}) AND ("{mindate}"[Date - Publication] : "{maxdate}"[Date - Publication])'
    raw, errors = request(EUTILS + "/esearch.fcgi", {
        "db": "pubmed", "term": term, "retmode": "json", "retmax": retmax,
        "sort": "pub date"
    })
    if raw is None:
        return [], errors
    data = json.loads(raw.decode("utf-8"))
    pmids = data.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return [], errors

    fetched, errs2 = request(EUTILS + "/efetch.fcgi", {
        "db": "pubmed", "id": ",".join(pmids), "retmode": "xml"
    })
    errors += errs2
    if fetched is None:
        return [], errors

    root = ET.fromstring(fetched)
    rows = []
    for a in root.findall(".//PubmedArticle"):
        med = a.find("MedlineCitation")
        art = med.find("Article") if med is not None else None
        if med is None or art is None:
            continue
        pmid = text_of(med.find("PMID"))
        title = text_of(art.find("ArticleTitle"))
        abstract = " ".join(text_of(x) for x in art.findall("Abstract/AbstractText"))
        journal = text_of(art.find("Journal/Title"))
        pubtypes = [text_of(x) for x in art.findall("PublicationTypeList/PublicationType")]
        doi = ""
        for x in a.findall(".//ArticleId"):
            if x.attrib.get("IdType") == "doi":
                doi = text_of(x)
                break
        pubdate = ""
        pd = art.find("Journal/JournalIssue/PubDate")
        if pd is not None:
            pubdate = "-".join(filter(None, [
                text_of(pd.find("Year")),
                text_of(pd.find("Month")),
                text_of(pd.find("Day"))
            ]))
        rows.append({
            "kind": kind, "title": title, "abstract": abstract, "journal": journal,
            "pmid": pmid, "doi": doi, "published_date": pubdate,
            "publication_types": pubtypes
        })
    return rows, errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14,
                    help="Look back this many publication days; default 14.")
    ap.add_argument("--retmax", type=int, default=200)
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--outdir", default="evidence-radar-work/pubmed-watch")
    args = ap.parse_args()

    today = date.today()
    start = today - timedelta(days=args.days)
    mindate, maxdate = start.strftime("%Y/%m/%d"), today.strftime("%Y/%m/%d")
    docs = Path(args.docs)

    docs_text = "\n".join(
        p.read_text(encoding="utf-8-sig", errors="ignore").lower()
        for p in docs.rglob("*.md")
    ) if docs.exists() else ""

    all_rows, errors, status = [], [], []
    for kind, query in QUERIES.items():
        print(f"[PubMed] {kind} ...", flush=True)
        rows, errs = fetch_kind(kind, query, mindate, maxdate, args.retmax)
        all_rows.extend(rows)
        errors.extend([{"kind": kind, **e} for e in errs])
        status.append({"kind": kind, "records": len(rows)})
        print(f"  {len(rows)} record(s)", flush=True)

    # Cross-query dedupe while preferring the more specific modality.
    priority = {"pharmacopuncture": 4, "electroacupuncture": 3, "acupuncture": 2, "herbal-medicine": 1}
    by_id = {}
    for r in all_rows:
        key = ("pmid:" + r["pmid"]) if r["pmid"] else ("doi:" + r["doi"].lower()) if r["doi"] else "title:" + re.sub(r"\W+", " ", r["title"].lower())
        if key not in by_id or priority[r["kind"]] > priority[by_id[key]["kind"]]:
            by_id[key] = r

    candidates, holds, existing = [], [], []
    for r in by_id.values():
        t = (r["title"] + " " + r["abstract"]).lower()
        st = study_type(r["title"], r["abstract"], r["publication_types"])
        level = evidence_level(st)
        r["study_type"] = st
        r["evidence_level"] = level
        r["kcd_candidates"] = map_conditions(t)
        r["formula_candidates"] = map_formulas(t)

        identifiers = [x for x in [r["doi"].lower().strip(), r["pmid"].strip()] if x]
        if identifiers and any(x in docs_text for x in identifiers):
            existing.append(r)
            continue

        target = resolve_target(docs, r["kcd_candidates"])
        r["target"] = target
        reasons = []

        if any(x in t for x in BAD):
            reasons.append("unsafe-publication-type")
        if any(x in t for x in PROTOCOL) or level == "P":
            reasons.append("protocol")
        if level not in {"A", "B"}:
            reasons.append("not-A/B")
        reasons += modality_reasons(r["kind"], t)
        if not target:
            reasons.append("target-missing-or-unmapped")
        if not r["doi"] and not r["pmid"]:
            reasons.append("identifier-missing")

        # Broad multi-intervention reviews are useful internally but not auto-promoted.
        if any(x in t for x in [
            "network meta-analysis", "different interventions", "different therapies",
            "nonpharmacological methods", "combined with", "adjunctive therapy"
        ]):
            reasons.append("indirect-or-combination")

        r["reasons"] = list(dict.fromkeys(reasons))
        r["approved"] = False
        if r["reasons"]:
            holds.append(r)
        else:
            candidates.append(r)

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "new-pubmed-records.json").write_text(json.dumps(list(by_id.values()), ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "high-confidence-candidates.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "hold-queue.json").write_text(json.dumps(holds, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "already-existing.json").write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "request-errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = [
        "# PubMed Evidence Radar Weekly Watch", "",
        f"- 실행: {datetime.now().isoformat(timespec='seconds')}",
        f"- 검색기간: {mindate} ~ {maxdate}",
        f"- 신규 검색 고유논문: {len(by_id)}건",
        f"- 기존 아카이브 식별자: {len(existing)}건",
        f"- 고신뢰 신규 후보: {len(candidates)}건",
        f"- 내부 보류: {len(holds)}건",
        f"- API 오류 기록: {len(errors)}건", "",
        "## 분야별 수집", ""
    ]
    for s in status:
        summary.append(f"- {s['kind']}: {s['records']}건")
    summary += [
        "", "## 운영 원칙", "",
        "- PubMed를 직접 정기 조회",
        "- 공개 docs는 자동 수정하지 않음",
        "- 철회/논평/protocol/낮은 연구유형/중복/복합중재/모달리티 혼입 자동 보류",
        "- 고신뢰 후보만 batch 검토 대상으로 남김",
        "- 사용자가 논문을 한 건씩 심사하지 않음"
    ]
    (out / "WEEKLY-SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")

    print(
        f"DONE -> unique {len(by_id)} | existing {len(existing)} | "
        f"candidates {len(candidates)} | hold {len(holds)}",
        flush=True
    )

if __name__ == "__main__":
    main()
