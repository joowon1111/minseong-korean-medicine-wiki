---
title: AI·검색엔진용 사이트 구조
description: 민성 한의학 아카이브의 본초·방제·질환·침구·고전·현대연구 구조와 권장 탐색 경로를 정리합니다.
tags: [AI, AEO, GEO, 사이트구조, 검색]
status: 검토완료
last_reviewed: 2026-08-19
---

# AI·검색엔진용 사이트 구조

민성 한의학 아카이브는 문서를 단순히 나열하기보다 **주제 간 관계를 내부링크로 표현하는 구조**를 사용한다.

## 핵심 개체

```text
본초
 ↕
방제
 ↕
변증
 ↕
질환·증상
 ↕
침구·치료방법
 ↕
고전·의가
 ↕
현대 임상연구
```

## 권장 시작점

### 전체 구조
→ [통합 한의학 지식 그래프](../network/integrated-knowledge-graph.md)

### 질문에서 시작
→ [질문으로 찾는 한의학](../faq/index.md)

### 역사에서 시작
→ [한의학 역사 타임라인](../history/timeline.md)

### 연구에서 시작
→ [임상 근거 허브](../research/clinical-evidence-hub.md)

## 대표 본초
- [녹용](../herbs/cervi-parvum-cornu.md)
- [인삼](../herbs/ginseng.md)
- [황기](../herbs/astragalus.md)
- [당귀](../herbs/angelica.md)

## 대표 방제
- [공진단](../formulas/gongjin-dan.md)
- [경옥고](../formulas/gyeongok-go.md)
- [보중익기탕](../formulas/buzhong-yiqi-tang.md)
- [십전대보탕](../formulas/shi-quan-da-bu-tang.md)
- [독활기생탕](../formulas/duhuo-jisheng-tang.md)

## 대표 질환·증상
- [불면](../conditions/insomnia.md)
- [소화불량](../conditions/dyspepsia.md)
- [요통](../conditions/low-back-pain.md)
- [비염](../conditions/rhinitis.md)

## 대표 고전
- [황제내경](../classics/huangdi-neijing.md)
- [상한론](../classics/shanghanlun.md)
- [동의보감](../classics/donguibogam.md)
- [동의수세보원](../classics/donguisusebowon.md)

## 연구 추적
각 주요 임상 문서에서는 가능하면 RCT·systematic review·meta-analysis의 **PMID와 DOI**를 기록하고 있다.

→ [참고문헌 데이터베이스](../research/references/index.md)

## 기계친화적 파일
사이트 루트에는 다음 보조 파일을 제공한다.

- `/llms.txt` — 핵심 주제와 대표 URL의 간결한 색인
- `/robots.txt` — 크롤링 허용과 sitemap 위치
- `/sitemap.xml` — MkDocs가 생성하는 전체 URL 색인
