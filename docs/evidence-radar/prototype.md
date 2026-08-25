---
title: Evidence Radar 프로토타입
description: 공개 논문 API에서 최근 한의학 인체연구 후보를 읽어 Evidence Record와 검토용 Markdown으로 변환하는 실험용 파이프라인입니다.
---
# Evidence Radar 프로토타입

156단계는 **자동발행이 아니라 읽기 전용 후보수집 프로토타입**입니다.

## 첫 테스트

```bash
python tools/evidence-radar/fetch_evidence.py --query pharmacopuncture --years 3 --limit 50
```

API 요청 필터:

`analyzed=1 + km=1 + human=1 + 최근 3년`

## 생성 결과

- `evidence-pharmacopuncture.json` — 구조화된 Evidence Record 후보
- `evidence-pharmacopuncture.md` — 사람이 검토하기 위한 PICO 보고서

## 자동 처리

`API → 최근 기간 → 한의학 → 인체연구 → 구조화 → KCD 후보 → PICO → Markdown`

## 사람이 확인

- KCD 코드가 맞는가?
- PICO가 논문 내용과 일치하는가?
- 임상적 의미를 과장하지 않았는가?
- 어느 민성 아카이브 페이지에 연결할 것인가?

검토가 끝난 자료만 기존 현대근거 카드와 참고문헌 DB에 반영합니다.

## 현재 KCD 후보 규칙

프로토타입에서는 요통·손목터널·무릎 골관절염·불면·알레르기비염·편두통·기능성소화불량·CP/CPPS 등 일부 핵심 질환만 예시 규칙으로 제공합니다.

향후 실제 결과를 본 뒤 KCD 매핑 테이블을 별도 파일로 분리합니다.
