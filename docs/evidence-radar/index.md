---
title: 민성 Evidence Radar
description: 최신 한의학 인체연구를 질환·KCD, 치료법, 연구유형, PICO와 기존 민성 한의학 아카이브 지식망에 연결하기 위한 근거 업데이트 설계입니다.
tags: [EvidenceRadar, 최신논문, PubMed, KCD, PICO, RCT, 메타분석, AEO, GEO]
last_reviewed: '2026-08-25'
---

# 민성 Evidence Radar

Evidence Radar는 최신 연구를 무작정 쌓는 페이지가 아니라 **새 연구를 기존 민성 한의학 아카이브의 지식망에 연결하는 근거 업데이트 계층**입니다.

## 핵심 구조

`최신 논문 → 한의학 여부 → 인체연구 → 질환·KCD → 치료법 → 연구유형 → PICO → 임상적 의미 → 기존 아카이브 페이지`

## 최신 근거 레이더

관찰 기간은 **최근 30일 / 90일 / 1년 / 3년**으로 나눕니다.

우선순위는 다음과 같이 둡니다.

1. Systematic review / Meta-analysis
2. RCT
3. 기타 인체 임상연구
4. 관찰연구
5. 기전·전임상 연구

## 질환·KCD 중심 분류

가능한 경우 논문을 KCD와 기존 질환 페이지에 연결합니다.

예:

`M54 요통 → 침 → 전침 → 약침 → 한약 → SR/MA → RCT → 관련 경혈·방제`

`G56.0 손목터널증후군 → 정중신경 → 초음파 → 침 → 약침 → 임상근거`

KCD 자동분류는 확정값이 아니라 **검토할 후보값**으로 취급합니다.

## 치료법 분류

침 · 전침 · 약침 · 도침 · 뜸 · 부항 · 한약·탕약 · 본초 · 사상의학 · 복합 한의치료

## PICO 논문 카드

**P — Population**  
대상 질환 · 진단기준 · 환자 수

**I — Intervention**  
치료법 · 경혈/처방 · 용량·빈도 · 치료기간

**C — Comparator**  
sham · usual care · medication · 다른 치료

**O — Outcome**  
통증 · 기능 · 삶의 질 · 수면 · 검사수치 · adverse events

**Clinical meaning**  
이 연구가 실제 어떤 임상 질문에 답하는지 정리합니다.

**Source**  
PMID · DOI · 저널 · 연도

## 기존 지식망 연결

- [증상·질환](../conditions/index.md)
- [질환별 현대 근거 카드](../authority/conditions/index.md)
- [본초](../herbs/index.md)
- [방제](../formulas/index.md)
- [침구·치료](../portal/acupuncture.md)
- [신경포착증후군](../nerve-entrapment/index.md)
- [근골격계 초음파](../musculoskeletal-ultrasound/index.md)
- [사상의학](../sasang-integrated/index.md)
- [참고문헌 데이터베이스](../research/references/index.md)

## 업데이트 우선순위

높은 우선순위는 **최신 SR/MA, 대규모 RCT, 기존 핵심 페이지를 직접 보강하는 연구, 근거가 부족한 영역의 인체연구**입니다.

기전·동물·세포 연구는 임상근거와 섞지 않고 별도 기전층으로 둡니다.

## AI·AEO·GEO

`환자 질문 → 증상 → 질환/KCD → 치료법 → 연구유형 → PICO → 결과 → 임상적 의미 → PMID/DOI`

질문 예:
- 최근 요통 침 연구는 무엇인가요?
- 불면 한약 RCT는 최근에 어떤 것이 나왔나요?
- 손목터널증후군 침 치료 최신 systematic review는?
- 약침 인체연구만 볼 수 있나요?
- 최근 3년 한의학 임상시험을 질환별로 볼 수 있나요?

## 자동화 원칙

자동화에 적합:
`수집 → 중복제거 → 날짜필터 → 인체연구필터 → 연구유형 → PICO 초안 → 질환 후보분류`

사람이 검토:
`KCD 확정 → 임상적 의미 → 기존 페이지 연결 → 과도한 결론 방지 → 최종 게시`

## 시스템 역할 분리

**외부 논문 검색·분석 시스템** → 최신 연구 후보 탐색  
**민성 Evidence Pipeline** → 분류·검토·기존 지식망 연결  
**민성 한의학 아카이브** → 최종 지식 제공

처음부터 자동발행하지 않고 **자동수집·자동초안 → 사람 검토 → 게시** 구조로 시작합니다.

→ [Evidence Record 데이터 스키마](data-schema.md)  
→ [Evidence Pipeline 운영 흐름](pipeline.md)
