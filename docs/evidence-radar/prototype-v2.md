---
title: Evidence Radar 프로토타입 v2
description: 실제 50건 테스트 결과를 바탕으로 검색 관련성, 연구유형, 치료법, KCD 후보, PICO fallback, 아카이브 연결과 우선순위를 개선한 Evidence Radar입니다.
---
# Evidence Radar 프로토타입 v2

156 실제 테스트에서 API 수집 자체는 성공했지만 다음 문제가 확인되었습니다.

1. `pharmacopuncture` 검색 시 **Journal of Pharmacopuncture 저널명만 일치하는 비관련 논문**이 많이 포함됨
2. API에서 받은 키워드는 풍부하지만 `study_type` 필드가 비어 있었음
3. PICO와 임상요약 필드가 현재 클라이언트에서는 비어 있었음
4. KCD 후보 규칙이 너무 적었음
5. 기존 아카이브 페이지 연결이 자동화되지 않았음

157은 이 문제를 보완합니다.

## 개선된 흐름

`API 원후보 → 검색어 실제 관련성 → 연구유형 → 치료태그 → 질환/KCD → PICO 초안 → 아카이브 링크 후보 → 우선순위`

## 약침 다시 테스트

```bash
python tools/evidence-radar/fetch_evidence_v2.py --query pharmacopuncture --years 3 --limit 100
```

생성:

- `evidence-pharmacopuncture-v2.md`
- `evidence-pharmacopuncture-v2.json`

## 관련성 필터

저널명이 `Journal of Pharmacopuncture`라는 이유만으로 포함되는 논문은 제외하고,
제목·키워드·치료태그에서 실제 약침 관련성이 확인되는 논문을 우선합니다.

## 연구유형

제목과 키워드에서 다음을 자동 추론합니다.

- Systematic review & meta-analysis
- Scoping review
- RCT
- RCT protocol
- Case report
- Cross-sectional study
- Survey
- Pilot study

## PICO fallback

API의 PICO 필드를 못 읽는 경우에도 제목과 키워드에서
Population / Intervention / Comparator / Outcome의 최소 초안을 생성합니다.

이는 최종 PICO가 아니라 **사람 검토를 위한 초안**입니다.

## 우선순위

Systematic review/meta-analysis와 RCT에 높은 점수를 주고,
KCD 매핑 및 초음파 유도·약침 관련성에 추가 점수를 줍니다.

점수가 높은 연구부터 먼저 검토하면 됩니다.
