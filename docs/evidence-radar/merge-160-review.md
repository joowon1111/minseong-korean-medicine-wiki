---
title: Evidence Radar 160 병합 검토 기록
description: 159 후보를 최신 docs 구조와 대조해 실제 존재 페이지, 중복 DOI, 프로토콜 여부를 검토한 기록입니다.
---
# Evidence Radar 160 병합 검토

## 이번에 실제 병합한 영역

- 유착성관절낭염(오십견)
- 회전근개 질환
- 턱관절장애
- 긴장형 두통
- 만성 요통
- 무릎통증

## 자동 병합하지 않은 후보

### 요추 척추관협착증
Evidence Radar에는 약침 RCT와 protocol이 있으나 최신 `docs/conditions/`에 대응하는 확정 페이지 경로가 없어 이번에는 새 질환 페이지를 임의 생성하지 않았습니다.

### 경추 추간판탈출증
약침 RCT 후보가 있으나 최신 `docs/conditions/`에 정확한 대응 페이지가 없어 보류했습니다.

### 요추 추간판탈출증
Evidence 후보는 유용하지만 현재 최신 docs의 기존 구조와 연결 위치를 추가 검토한 뒤 반영합니다.

### 근막통증증후군
현재 후보 중 protocol 비중이 있어 완료 임상근거와 분리해 추적합니다.

## 프로토콜 오분류 교정

`Pharmacoacupuncture for the Treatment of Frozen Shoulder: protocol for a systematic review and meta-analysis`

이 문헌은 제목상 **systematic review/meta-analysis protocol**입니다. 완료된 SR/MA 근거로 취급하지 않고 연구 추적 자료로 분리했습니다.

## 원칙

이번 병합은 논문의 제목·연구유형·키워드·PMID/DOI로 확인 가능한 범위만 반영했습니다. API에서 실제 결과값이 비어 있는 연구는 효과크기나 통계적 유의성을 임의로 작성하지 않았습니다.
