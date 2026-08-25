#!/usr/bin/env python3
"""
Minseong Evidence Radar v0.4
Build non-destructive wiki update candidates from clinical Evidence JSON.

- DOES NOT edit docs/conditions or other existing wiki pages.
- Generates proposed Markdown blocks under evidence-update-candidates/.
- Prioritizes A/B evidence.
- Protocols are separated from completed clinical evidence.
"""
import argparse, json, re
from pathlib import Path
from collections import defaultdict

def safe(s):
    s=re.sub(r"[^a-zA-Z0-9가-힣._-]+","-",s).strip("-")
    return s or "candidate"

def source_line(r):
    bits=[]
    if r.get("pmid"): bits.append("PMID "+str(r["pmid"]))
    if r.get("doi"): bits.append("DOI "+str(r["doi"]))
    return " · ".join(bits) or "식별자 확인 필요"

def target_paths(r):
    # Prefer condition-specific targets; generic portal links are context links, not update targets.
    out=[]
    for x in r.get("kcd_candidates",[]):
        p=x.get("archive_path")
        if p: out.append(p)
    return list(dict.fromkeys(out))

def evidence_block(r):
    p=r.get("pico",{})
    protocol=r.get("study_type")=="RCT protocol"
    heading="연구 프로토콜" if protocol else "최신 임상근거"
    lines=[
      f"### {heading} — {r.get('published_date','')}",
      "",
      f"**{r.get('title','')}**",
      "",
      f"- 연구유형: {r.get('study_type','')}",
      f"- 중재: {p.get('intervention') or ', '.join(r.get('treatment_tags',[])) or '확인 필요'}",
    ]
    if p.get("population"): lines.append(f"- 대상: {p['population']}")
    if p.get("comparator"): lines.append(f"- 비교: {p['comparator']}")
    if p.get("outcomes"): lines.append(f"- 주요 평가항목: {', '.join(map(str,p['outcomes']))}")
    lines += [
      f"- 근거 식별자: {source_line(r)}",
      "",
      "> 자동 생성된 업데이트 후보입니다. 원문을 확인한 뒤 대상·중재·비교군·결과와 임상적 의미를 보완하여 반영합니다.",
      ""
    ]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir",default="evidence-update-candidates")
    ap.add_argument("--min-level",default="B",choices=["A","B","C","D"])
    args=ap.parse_args()
    rows=json.loads(Path(args.input).read_text(encoding="utf-8"))

    allowed={"A":{"A"},"B":{"A","B"},"C":{"A","B","C"},"D":{"A","B","C","D"}}[args.min_level]
    selected=[r for r in rows if r.get("evidence_level") in allowed or r.get("evidence_level")=="P"]

    grouped=defaultdict(list)
    unmapped=[]
    for r in selected:
        targets=target_paths(r)
        if not targets:
            unmapped.append(r); continue
        for t in targets: grouped[t].append(r)

    outdir=Path(args.outdir); outdir.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for target,recs in grouped.items():
        completed=[r for r in recs if r.get("evidence_level") in allowed]
        protocols=[r for r in recs if r.get("evidence_level")=="P"]
        if not completed and not protocols: continue

        label=next((x.get("label") for r in recs for x in r.get("kcd_candidates",[])
                    if x.get("archive_path")==target),target)
        text=[
          f"# 업데이트 후보 — {label}","",
          f"- 대상 기존 페이지: `docs/{target.rstrip('/')}.md` 또는 해당 index.md 구조 확인 필요",
          "- 상태: **검토 전 / 자동 병합 금지**","",
          "## 반영 제안","",
          "기존 페이지의 `현대 임상근거`, `약침`, `침구치료` 관련 섹션을 확인한 뒤 중복되지 않는 연구만 추가합니다.",""
        ]
        if completed:
            text += ["## 완료된 임상근거 후보",""]
            for r in sorted(completed,key=lambda x:x.get("priority_score",0),reverse=True):
                text.append(evidence_block(r))
        if protocols:
            text += ["## 진행·프로토콜 자료","",
                     "프로토콜은 치료효과의 완료 근거로 표현하지 않고 향후 연구 추적용으로 분리합니다.",""]
            for r in protocols:
                text.append(evidence_block(r))

        fname=safe(target.strip("/").replace("/","__"))+".md"
        (outdir/fname).write_text("\n".join(text),encoding="utf-8")
        manifest.append({"target":target,"label":label,"file":fname,
                         "completed":len(completed),"protocols":len(protocols)})

    # unmapped high-value evidence gets a separate review queue
    uq=["# 미매핑 A/B 근거 검토 큐","",
        "질환/KCD 또는 기존 아카이브 대상 페이지가 확정되지 않은 높은 우선순위 연구입니다.",""]
    for r in unmapped:
        uq += [f"## {r.get('title')}","",
               f"- 근거층: {r.get('evidence_level')} / {r.get('study_type')}",
               f"- 치료: {', '.join(r.get('treatment_tags',[]))}",
               f"- {source_line(r)}",""]
    (outdir/"_unmapped-review.md").write_text("\n".join(uq),encoding="utf-8")
    (outdir/"_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")

    summary=["# Evidence Update Candidates","",
             f"- 입력 임상 Evidence: {len(rows)}건",
             f"- A/B + protocol 검토대상: {len(selected)}건",
             f"- 기존 질환 페이지로 매핑된 대상: {len(manifest)}개",
             f"- 미매핑 검토 연구: {len(unmapped)}건","",
             "## 대상 페이지",""]
    for m in manifest:
        summary.append(f"- {m['label']}: 완료근거 {m['completed']} / protocol {m['protocols']} → `{m['file']}`")
    (outdir/"README.md").write_text("\n".join(summary),encoding="utf-8")
    print(f"selected {len(selected)} -> mapped targets {len(manifest)} -> unmapped {len(unmapped)}")

if __name__=="__main__":
    main()
