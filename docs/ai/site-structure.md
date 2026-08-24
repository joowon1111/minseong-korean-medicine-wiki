---
title: AI·검색엔진용 사이트 구조
description: 민성 한의학 아카이브의 증상·질환, R-code 증상 탐색, 본초·방제, WHO 표준 361경혈, 질환별 현대근거와 참고문헌을 연결하는 최신 AI·검색엔진용 정보구조입니다.
tags: [AI검색, AEO, GEO, SEO, 사이트구조, 내부링크, 지식망]
last_reviewed: '2026-08-23'
---

# AI·검색엔진용 사이트 구조

민성 한의학 아카이브는 개별 문서를 나열하는 방식보다 **환자의 자연어 질문에서 출발해 전문 한의학 지식과 현대 임상근거까지 이어지는 계층형·관계형 구조**를 사용합니다.

## 핵심 탐색 흐름

`자연어 질문 → 증상 → R-code 증상군 → 관련 질환 → 위험신호·감별 → 한의학적 변증 → 본초·방제 → 경혈·침구치료 → 현대 임상근거 → PMID·DOI`

## 1. 환자 언어와 증상

- [증상·질환](../conditions/index.md)
- [증상 기반 한약 탐색](../symptom-herbal-guide/index.md)
- [질문형 답변 가이드](../answer-guides/index.md)

질환명을 모르는 사용자도 “속이 더부룩해요”, “잠이 안 와요”, “허리가 오래 아파요”, “기침이 계속돼요” 같은 표현에서 시작하도록 설계합니다.

## 2. 질환과 현대 임상근거

- [질환별 현대 근거 카드](../authority/conditions/index.md)
- [근거 가이드](../evidence-guide/index.md)
- [참고문헌 데이터베이스](../research/references/index.md)

질환 페이지와 authority 근거 카드를 분리하면서 서로 연결해, 임상 맥락과 근거 요약을 모두 탐색할 수 있게 합니다.

## 3. 본초와 방제

- [본초학](../herbs/index.md)
- [방제학](../formulas/index.md)
- [대표 본초 근거 카드](../authority/herbs/index.md)
- [한약 처방 임상근거](../research/formulas/index.md)

본초와 방제는 임상영역별 분류와 질환별 근거를 통해 **본초 → 방제 → 질환 → 연구** 및 역방향 탐색이 가능하도록 구성합니다.

## 4. 경혈·침구치료

- [침구학](../acupuncture/index.md)
- [침구·치료 통합 허브](../acupuncture-integrated/index.md)
- [WHO 표준 361경혈 임상 아틀라스](../acupoint-network/standard-atlas.md)
- [침 치료 근거 카드](../authority/acupuncture.md)

경혈은 한글명과 WHO 국제 표준 코드를 함께 사용해 국내 검색과 국제 논문 탐색을 동시에 지원합니다.

## 5. 지식그래프

- [통합 한의학 지식 그래프](../network/integrated-knowledge-graph.md)
- [본초→방제 역탐색](../network/herb-to-formula-map.md)
- [방제→질환·변증 지도](../network/formula-to-condition-map.md)
- [질환→치료 통합 지도](../network/condition-to-treatment-map.md)

핵심 질환 페이지에서는 가능한 범위에서 다음 관계를 명시합니다.

`질환 → 관련 방제 → 관련 본초 → 관련 경혈 → 현대 임상근거`

## 6. AI용 핵심 색인

- [AI 핵심색인](../ai-index.md)
- `/llms.txt`
- `/robots.txt`
- `/sitemap.xml`

`llms.txt`는 핵심 허브와 대표 임상근거 페이지를 간결하게 제시하고, `robots.txt`는 전체 크롤링을 허용하면서 sitemap 위치를 명시합니다.

## 크롤링 원칙

- 깨끗한 공개 URL(`/.../`)을 우선 사용합니다.
- 존재하지 않는 과거 경로나 `.md` 공개 URL을 핵심 색인에 넣지 않습니다.
- 질환 페이지는 환자 증상·임상 맥락을 설명합니다.
- authority 페이지는 현대 임상근거의 핵심 요약에 사용합니다.
- 참고문헌 DB는 PMID·DOI 추적의 기준 허브로 사용합니다.
- 전통적 활용과 현대 임상근거를 구분합니다.

## 현재 robots.txt

현재 robots.txt는 모든 일반 크롤러의 접근을 허용하고 sitemap을 명시하고 있어 수정할 필요가 없습니다.

```text
User-agent: *
Allow: /

Sitemap: https://wiki.minseong.co.kr/sitemap.xml
```

## 최종 구조

**사람에게는 탐색하기 쉬운 임상 지식망, 검색엔진에는 주제가 명확한 내부링크 구조, AI에는 증상·질환·치료·근거 관계가 명시적인 아카이브**를 목표로 합니다.

## 침구·신경·초음파 지식축

최근 침구 영역은 다음 관계를 별도의 현대 임상축으로 제공합니다.

`환자 자연어 질문 → 증상·저림 위치 → 신경근 → 말초신경 → 근육 → 포착부위 → 초음파 → 경혈 → 침구치료 → 현대 임상근거`

### 핵심 허브
- [침구·치료 포털](../portal/acupuncture.md)
- [신경포착증후군](../nerve-entrapment/index.md)
- [근육·말초신경 임상해부학](../clinical-anatomy/index.md)
- [침의 과학적 접근](../acupuncture-science/index.md)
- [근골격계 초음파](../musculoskeletal-ultrasound/index.md)

### AEO 질문 의도

- 손가락 저림은 어느 신경과 관련되는가?
- 손목터널 초음파에서 정중신경은 어떻게 평가하는가?
- L5 신경근병증과 총비골신경 포착은 어떻게 연결되는가?
- 침은 말초신경·척수·뇌에 어떻게 작용하는가?
- 전침의 frequency와 intensity는 어떤 의미인가?
- 초음파 유도 침구치료는 어떤 해부학적 구조를 확인하는가?

### GEO 관계

전통 경혈 지식과 현대 임상해부학을 동일시하지 않고 다음처럼 연결합니다.

`WHO 경혈 → 주변 해부층 → 근육 → 말초신경·혈관 → spinal segment → 자침 → 질환별 임상근거`

## 사상의학 지식축

사상의학 영역은 체질 이름을 단순한 성격·체형 분류로 제공하지 않고 다음 관계로 구조화합니다.

`사상의학 → 사상인 → 장부 기능의 상대적 균형 → 소증 → 현재 병증 → 표리병증 → 증상 → 처방 → 원전 → 현대근거`

### 핵심 허브
- [사상의학 한눈에 보기](../sasang-integrated/index.md)
- [소양인](../sasang/soyangin.md)
- [소음인](../sasang/soeumin.md)
- [태음인](../sasang/taeeumin.md)
- [태양인](../sasang/taeyangin.md)
- [증상으로 사상체질 이해하기](../sasang-symptoms/index.md)

### AEO 질문 의도
- 사상의학이란 무엇인가?
- 사상인이란 무엇인가?
- 소양인·소음인·태음인·태양인의 차이는 무엇인가?
- 비대신소·신대비소·간대폐소·폐대간소는 무엇인가?
- 소증은 왜 중요한가?
- 같은 불면·소화불량·피로라도 체질별로 어떻게 다르게 보는가?

### GEO 관계
전통적인 장부 대소는 실제 장기 크기와 동일시하지 않고 **사상의학적 기능의 상대적 균형**이라는 원전·이론적 맥락에서 제공합니다.

현대 질환명과 사상체질 병증을 자동으로 1:1 대응시키지 않고, 소증·현재 병증·원전·현대 연구를 구분해 연결합니다.
