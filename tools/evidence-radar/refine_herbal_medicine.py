#!/usr/bin/env python3
"""
174 — Herbal Medicine refinement + Autopilot integration

Input:
  evidence-radar-work/herbal-medicine/herbal-medicine-clinical.json

Goals:
- focus on East Asian oral herbal formula evidence
- exclude acupuncture-only / non-herbal false positives
- separate external, injection, nasal irrigation, foot bath, mouthwash, nebulized routes
- separate non-East-Asian traditional herbal systems
- hold combination/intervention-mixed evidence
- prioritize formula-specific A/B clinical evidence
- map known archive formulas and diseases
- write only internal outputs
- no automatic docs publishing

Also produces a normalized herbal source file that 172 Autopilot can consume.
"""
import argparse,json,re
from pathlib import Path
from collections import defaultdict,Counter

EAST_ASIAN=[
 "chinese herbal","traditional chinese medicine","east asian herbal","korean medicine",
 "kampo","decoction","granule","formula","탕","산","환","한약"
]
NON_EAST_ASIAN=[
 "thai herbal","persian medicine","indian herbal","ayurvedic","ethiopia",
 "sub-saharan africa","saudi herbal","traditional persian"
]
EXTERNAL_ROUTE=[
 "foot bath","bath therapy","nasal irrigation","mouthwash","nebulised","nebulized",
 "topical","external chinese herbal","external application","injection","injectable"
]
OTHER_MODALITY=[
 "acupuncture combined","acupuncture and herbal","acupuncture plus","needle knife",
 "acupotomy","moxibustion and","manual therapy","stem cell"
]
MECHANISTIC_ONLY=[
 "network pharmacology","molecular docking","data mining","bibliometric",
 "evidence map","meta-epidemiological","reporting quality","risk of bias",
 "umbrella review","overview of systematic reviews","prevalence and utilization",
 "mechanism of","pharmacological mechanisms"
]
COMBINATION=[
 "combined with western medicine","combined with chemical drugs","combined with donepezil",
 "combined with antihistamines","combined with opioids","combined with chemotherapy",
 "combined with adjuvant chemotherapy","plus conventional therapy","adjunctive therapy",
 "combined with negative pressure","combined with calcipotriol","combined with mesalazine",
 "combined with antithyroid","combined with interferon","combined with auricular acupressure"
]
PREPRINT=["10.21203/","10.1101/","preprint"]

KNOWN_FORMULAS=[
 (["sijunzi","si jun zi","四君子","사군자"],"사군자탕","formulas/sagunja-tang/"),
 (["xiangsha liujunzi","xiangsha liujun","향사육군자","香砂六君子"],"향사육군자탕","formulas/xiangsha-liujunzi-tang/"),
 (["liujunzi","liu jun zi","六君子","육군자"],"육군자탕","formulas/yukgunja-tang/"),
 (["guipi","gui pi","歸脾","귀비"],"귀비탕","formulas/guibi-tang/"),
 (["buzhongyiqi","bu zhong yi qi","補中益氣","보중익기"],"보중익기탕","formulas/bojungikgi-tang/"),
 (["duhuo-jisheng","du huo ji sheng","獨活寄生","독활기생"],"독활기생탕","formulas/dokhwalgi-saeng-tang/"),
 (["wendan","wen dan","溫膽","온담"],"온담탕","formulas/ondam-tang/"),
 (["wujisan","wu ji san","五積散","오적산"],"오적산","formulas/ojeok-san/"),
 (["xuefu zhuyu","혈부축어","血府逐瘀"],"혈부축어탕","formulas/xuefu-zhuyu-tang/"),
 (["xiaoyao san","xiao-yao-san","소요산","逍遙散"],"소요산","formulas/xiaoyao-san/"),
 (["banxia shumi","반하서미"],"반하서미탕","formulas/banxia-shumi-tang/"),
 (["tongxie yaofang","痛瀉要方","통사요방"],"통사요방","formulas/tongxie-yaofang/"),
 (["huoxiang zhengqi","藿香正氣","곽향정기"],"곽향정기산","formulas/huoxiang-zhengqi-san/"),
]

def norm(s): return re.sub(r"\s+"," ",str(s or "")).strip()
def title(r): return norm(r.get("title")).lower()
def blob(r): return (title(r)+" "+" ".join(map(str,r.get("keywords",[])))).lower()
def ids(r): return [x for x in [str(r.get("doi") or "").lower().strip(),str(r.get("pmid") or "").strip()] if x]
def dedupe_key(r):
    return ("doi:"+str(r.get("doi")).lower()) if r.get("doi") else ("pmid:"+str(r.get("pmid"))) if r.get("pmid") else "title:"+re.sub(r"\W+"," ",title(r))

def formula_candidates(r):
    t=blob(r); out=[]
    for terms,label,path in KNOWN_FORMULAS:
        if any(x.lower() in t for x in terms):
            out.append({"label":label,"archive_path":path})
    # preserve earlier parser results too
    for x in r.get("formula_candidates",[]):
        if x.get("label") and not any(y["label"]==x["label"] for y in out):
            out.append(x)
    return out

def reasons(r):
    t=blob(r); rs=[]
    if r.get("study_type") in {"RCT protocol","SR/MA protocol"} or r.get("evidence_level")=="P":
        rs.append("protocol")
    if r.get("evidence_level") not in {"A","B"}:
        rs.append("not-A/B")
    if any(x in t for x in NON_EAST_ASIAN):
        rs.append("non-east-asian-herbal-system")
    if any(x in t for x in EXTERNAL_ROUTE):
        rs.append("non-oral-or-external-route")
    if any(x in t for x in OTHER_MODALITY):
        rs.append("other-modality-mixed")
    if any(x in t for x in MECHANISTIC_ONLY):
        rs.append("mechanistic-or-methodology-heavy")
    if any(x in t for x in COMBINATION):
        rs.append("western-or-combination-therapy")
    if any(x in str(r.get("doi") or "").lower() for x in PREPRINT) or "preprint" in t:
        rs.append("preprint")
    if not any(x in t for x in EAST_ASIAN):
        rs.append("east-asian-herbal-signal-weak")
    return list(dict.fromkeys(rs))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir",default="evidence-radar-work/herbal-medicine-refined")
    a=ap.parse_args()

    rows=json.loads(Path(a.input).read_text(encoding="utf-8"))
    clean=[]; hold=[]; seen=set()
    for r in rows:
        k=dedupe_key(r)
        if k in seen: continue
        seen.add(k)
        r["formula_candidates_refined"]=formula_candidates(r)
        rs=reasons(r)
        item={**r,"refine_reasons":rs}
        if rs:
            hold.append(item)
        else:
            clean.append(item)

    # prioritize formula-specific items; disease-only items are still retained
    formula_specific=[r for r in clean if r.get("formula_candidates_refined")]
    disease_only=[r for r in clean if not r.get("formula_candidates_refined")]

    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    (out/"herbal-medicine-refined.json").write_text(json.dumps(clean,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"herbal-medicine-formula-specific.json").write_text(json.dumps(formula_specific,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"herbal-medicine-disease-only.json").write_text(json.dumps(disease_only,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"herbal-medicine-hold.json").write_text(json.dumps(hold,ensure_ascii=False,indent=2),encoding="utf-8")

    groups=defaultdict(list)
    for r in clean:
        labs=[x.get("label") for x in r.get("kcd_candidates",[]) if x.get("label")] or ["질환 미매핑"]
        for l in labs: groups[l].append(r)

    md=["# Herbal Medicine Evidence Radar — Refined","",
        f"- 입력: {len(rows)}건",
        f"- 고신뢰 A/B 경구 동아시아 한약 후보: {len(clean)}건",
        f"- 그중 기존 방제명 직접 연결: {len(formula_specific)}건",
        f"- 질환 중심·처방명 추가확인: {len(disease_only)}건",
        f"- 내부 보류: {len(hold)}건","",
        "> 내부 검토용입니다. docs/ 자동 게시 없음.","",
        "## 질환별 고신뢰 후보",""]
    for label,rs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in rs:
            fs=", ".join(x["label"] for x in r.get("formula_candidates_refined",[])) or "처방명 자동확인 필요"
            ident=r.get("doi") or r.get("pmid") or "-"
            md.append(f"- [{r.get('evidence_level')}] {r.get('title')} — {fs} — {ident}")
        md.append("")
    md += ["## 자동 보류 사유 요약",""]
    c=Counter(x for r in hold for x in r["refine_reasons"])
    for k,v in c.most_common(): md.append(f"- {k}: {v}건")
    (out/"herbal-medicine-refined-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"HERBAL REFINE -> clean {len(clean)} | formula-specific {len(formula_specific)} | hold {len(hold)}")
    print(out)

if __name__=="__main__": main()
