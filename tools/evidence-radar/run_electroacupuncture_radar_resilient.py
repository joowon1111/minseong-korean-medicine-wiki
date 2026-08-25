#!/usr/bin/env python3
"""
168 — Electroacupuncture Evidence Radar resilient runner

Fix for 167:
- HTTP 500/502/503/504 automatic retry
- one failed query does not abort the whole run
- query fallback variants
- always writes request-errors.json and run-status.json
- writes evidence files whenever at least one query succeeds
- internal only; never writes docs/
"""
import argparse, json, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
import importlib.util

BASE="https://med.symbolicinfo.com"

def request_json(q, years, limit, retries=3):
    from datetime import date, timedelta
    end=date.today(); start=end-timedelta(days=365*years)
    params={"q":q,"page":1,"per_page":min(limit,10000),"analyzed":1,
            "km":1,"human":1,"pub_from":start.isoformat(),"pub_to":end.isoformat()}
    url=BASE+"/search?"+urllib.parse.urlencode(params)
    errors=[]
    for attempt in range(1,retries+1):
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":"Minseong-Evidence-Radar-Electroacupuncture/0.2",
                "Accept":"application/json"
            })
            with urllib.request.urlopen(req,timeout=60) as r:
                return json.loads(r.read().decode("utf-8")), errors
        except urllib.error.HTTPError as e:
            errors.append({"query":q,"attempt":attempt,"type":"HTTPError","code":e.code,"message":str(e)})
            if e.code not in {429,500,502,503,504}: break
        except Exception as e:
            errors.append({"query":q,"attempt":attempt,"type":type(e).__name__,"message":str(e)})
        if attempt < retries:
            time.sleep(3*attempt)
    return None, errors

def load_167(path):
    spec=importlib.util.spec_from_file_location("ea167",path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--years",type=int,default=3)
    ap.add_argument("--limit",type=int,default=250)
    ap.add_argument("--retries",type=int,default=3)
    ap.add_argument("--outdir",default="evidence-radar-work/electroacupuncture")
    args=ap.parse_args()

    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True)
    queries=["electroacupuncture","electro-acupuncture","electrical acupuncture"]
    fetched=[]; all_errors=[]; succeeded=[]

    for q in queries:
        print(f"[query] {q}")
        raw,errs=request_json(q,args.years,args.limit,args.retries)
        all_errors.extend(errs)
        if raw is None:
            print(f"  failed after {args.retries} attempt(s); continuing...")
            continue
        rows=raw if isinstance(raw,list) else next(
            (raw.get(k) for k in ["items","results","articles","data"] if isinstance(raw.get(k),list)),[])
        fetched.extend(rows)
        succeeded.append({"query":q,"records":len(rows)})
        print(f"  success: {len(rows)} record(s)")

    (out/"request-errors.json").write_text(json.dumps(all_errors,ensure_ascii=False,indent=2),encoding="utf-8")
    status={"queries":queries,"succeeded":succeeded,"raw_records":len(fetched),
            "errors":len(all_errors),"all_queries_failed":not bool(succeeded)}
    (out/"run-status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding="utf-8")

    if not succeeded:
        (out/"README-FAILED.txt").write_text(
            "모든 API 검색어가 실패했습니다.\nrequest-errors.json을 확인하세요.\n"
            "Python/PowerShell 설치 문제가 아니라 원격 API 응답 실패일 가능성이 큽니다.\n",
            encoding="utf-8-sig")
        print("All API queries failed. Diagnostic files were still created.")
        return 2

    # Reuse 167's classification/filter logic, but process already fetched data locally.
    mod=load_167(Path(__file__).with_name("run_electroacupuncture_radar.py"))
    records=[]; excluded=[]; seen=set()
    for a in fetched:
        if not isinstance(a,dict): continue
        title=str(mod.pick(a,"title","article_title")); keywords=mod.pick(a,"keywords",default=[])
        t=(title+" "+mod.flat(keywords)).lower()
        if not any(x.lower() in t for x in mod.EA): continue
        if any(x in t for x in mod.BAD):
            excluded.append({"title":title,"reason":"retraction/comment/editorial"}); continue
        modality=mod.primary_modality(t)
        if modality in {"pharmacopuncture","acupotomy","other"}:
            excluded.append({"title":title,"reason":"non-electroacupuncture-primary"}); continue
        st=mod.study_type(title,keywords)
        r={"title":title,
           "published_date":mod.pick(a,"published_date","publication_date","pub_date"),
           "journal":mod.pick(a,"journal","journal_name"),
           "pmid":mod.pick(a,"pmid"),"doi":mod.pick(a,"doi"),
           "study_type":st,"evidence_level":mod.level(st),"modality":modality,
           "clinical_evidence":True,"kcd_candidates":mod.classify(t),
           "pico":mod.pico(t),"keywords":keywords,
           "source":"med.symbolicinfo.com","human_reviewed":False}
        k=mod.dedupe_key(r)
        if k in seen:
            excluded.append({"title":title,"reason":"duplicate"}); continue
        seen.add(k); records.append(r)

    completed=[r for r in records if r["evidence_level"] in {"A","B"} and r["study_type"] not in {"RCT protocol","SR/MA protocol"}]
    protocols=[r for r in records if r["evidence_level"]=="P"]

    (out/"electroacupuncture-clinical.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"electroacupuncture-excluded.json").write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding="utf-8")

    from collections import defaultdict
    groups=defaultdict(list)
    for r in completed:
        for x in r["kcd_candidates"]: groups[x["label"]].append(r)
    md=["# Electroacupuncture Evidence Radar — resilient run","",
        f"- 성공 검색어: {len(succeeded)}/{len(queries)}",
        f"- 수집 raw: {len(fetched)}건",
        f"- 전침/복합전침 후보: {len(records)}건",
        f"- 완료 A/B 근거: {len(completed)}건",
        f"- protocol 추적: {len(protocols)}건",
        f"- 제외/중복: {len(excluded)}건","",
        "> 내부 검토용입니다. docs/ 자동 게시 없음.","",
        "## 질환별 완료 A/B 근거",""]
    for label,recs in sorted(groups.items(),key=lambda x:len(x[1]),reverse=True):
        md.append(f"### {label}")
        for r in recs:
            ident=("PMID "+str(r["pmid"])) if r["pmid"] else ("DOI "+str(r["doi"]) if r["doi"] else "-")
            md.append(f"- [{r['evidence_level']}/{r['modality']}] {r['title']} — {ident}")
        md.append("")
    (out/"electroacupuncture-review.md").write_text("\n".join(md),encoding="utf-8")
    print(f"DONE: candidates {len(records)} -> A/B {len(completed)} -> protocols {len(protocols)}")
    print(f"Output: {out}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
