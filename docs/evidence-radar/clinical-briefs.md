---
title: Evidence Radar 임상 근거 브리프
description: 약침 등 최신 연구 후보에서 교육·정책·검색동향을 분리하고 질환별 임상근거 브리프를 자동 생성하는 단계입니다.
---
# Evidence Radar 임상 근거 브리프

158은 157의 검색 결과를 **실제 아카이브 현대근거 업데이트에 가까운 형태**로 재구성합니다.

## 처리 흐름

`v2 결과 → 임상 Evidence 필터 → KCD 확대 → 질환군 → 근거층 → 질환별 Evidence Brief`

## 근거층

- **A** — Systematic review & meta-analysis
- **B** — RCT / Scoping review
- **C** — 기타 인체연구
- **D** — Case report
- **P** — Protocol

이 표시는 공식 GRADE 등급이 아니라 **아카이브 검토 순서를 위한 내부 분류**입니다.

## 실행

```bash
python tools/evidence-radar/build_clinical_briefs.py evidence-pharmacopuncture-v2.json
```

생성:
- `evidence-pharmacopuncture-clinical.json`
- `evidence-pharmacopuncture-clinical.md`
- `evidence-briefs/spine-low-back.md`
- `evidence-briefs/cervical-neck.md`
- `evidence-briefs/shoulder.md`
- `evidence-briefs/elbow.md`
- `evidence-briefs/knee.md`
- `evidence-briefs/peripheral-nerve.md`
- `evidence-briefs/ultrasound-guided.md`
- 기타 실제 데이터에 해당하는 질환군

## 중요

Evidence Brief는 자동 게시물이 아닙니다.  
상위 연구부터 원문·PICO·KCD·기존 링크를 검토한 뒤 기존 질환별 현대근거 카드에 반영합니다.
