---
title: 한의학 지식망 — 증상·처방·경혈·고전 연결
description: 한의학 온톨로지의 개념·속성·관계를 실제 사례로 설명합니다. 증상·변증·본초·처방·경혈·고전·연구와 사상의학을 연결하고, 구성·배혈·출전·임상근거를 비교하는 경로를 안내합니다.
---
# 한의학 지식망 {#_1}

한의학 지식망은 **증상·변증·본초·처방·경혈·고전·연구를 관계와 출처에 따라 연결한 안내**입니다. 지금 알고 있는 증상이나 약재 이름에서 시작해 처방의 구성, 치료의 선택 이유, 고전 기록과 현대 연구까지 확인할 수 있습니다. 질환별 감별·치료는 해당 본문에서, 여러 문서를 함께 비교해야 하는 배합·배혈·출전의 관계는 이 지식망에서 살펴봅니다.

## 한의학 온톨로지의 기반 {#ontology}

온톨로지(Ontology)는 한 분야의 개념과 속성, 개념 사이의 관계를 명확하게 정의하여 지식을 공유하고 컴퓨터도 해석할 수 있도록 표현하는 체계입니다. 한의학에서는 ‘인삼’, ‘사군자탕’, ‘기허’, ‘족삼리’를 각각 어떤 종류의 개념으로 다루고, 무엇으로 연결하는지 설명하는 일이 그 출발점입니다. [온톨로지 개념 참고: W3C OWL 2 개요](https://www.w3.org/TR/owl2-overview/)

민성 한의학 아카이브는 **용어의 뜻과 식별 정보, 구성·소속·적용 맥락, 확인할 수 있는 출처**를 정리하며 한의학 온톨로지 구축의 기반을 쌓습니다. 이 페이지는 그 관계를 실제 문서로 확인하는 출발점입니다.

| 지식을 정리하는 요소 | 한의학에서의 예 | 확인할 자료 |
|---|---|---|
| 개념과 종류 | 인삼은 본초, 사군자탕은 처방, 기허는 변증 개념, 족삼리는 경혈 | [인삼](../herbs/ginseng.md) · [사군자탕](../formulas/sijunzi-tang.md) · [기허](../diagnostics/qi-deficiency.md) · [족삼리](../acupuncture/points/st36-zusanli.md) |
| 개념의 속성 | 본초의 기원·약용 부위, 처방의 제형·용량, 경혈의 표준 코드·위치 | [본초 비교](../herbal-integrated/herb-comparisons.md#interactive-comparison) · [원료·비율·제형](formula-composition-hub.md) · [경혈 아틀라스](../acupoint-network/standard-atlas.md) |
| 개념 사이의 관계 | 처방이 본초를 포함함, 경혈이 경맥에 속함, 문헌이 처방을 수록함 | 아래 [관계의 실제 사례](#relation-examples) |
| 관계의 출처와 조건 | 수록 판본·조문, 가감·제법, 연구 대상·비교군·기간 | [원전과 현대 연구 대조](classic-to-evidence-map.md) · [출처·인용 원칙](../guide/citation-policy.md) |

## 관계를 실제 사례로 이해하기 {#relation-examples}

**‘무엇이 무엇과 연결되는가’에 더해 ‘어떤 관계인가’를 확인하면** 같은 문서를 서로 다른 질문에 활용할 수 있습니다. 구성·소속·수록형 관계 가운데 본문에서 확인한 항목은 아래 [온톨로지 데이터](#ontology-data)에도 출처와 조건을 함께 제공합니다.

| 관계 | 실제 사례 | 관계를 확인하며 비교할 점 |
|---|---|---|
| 구성 | [사군자탕](../formulas/sijunzi-tang.md)은 인삼·백출·복령·감초를 기본 골격으로 함 | [본초에서 처방 찾기](herb-to-formula-map.md#_2)에서 인삼이 들어가는 다른 처방과 배합 역할 비교 |
| 기본방과 확장 | [육군자탕](../formulas/liujunzi-tang.md)은 사군자탕 골격에 반하·진피를 더함 | [사군자탕·육군자탕 비교](../compare/sijunzi-vs-liujunzi.md#comparison)에서 비위기허와 함께 담습·오심을 살피는 이유 확인 |
| 소속 | [족삼리 ST36](../acupuncture/points/st36-zusanli.md)는 [족양명위경](../meridian-network/stomach-meridian.md)에 속함 | 경맥의 유주, 족삼리의 표준 위치, 주변 근육·신경을 각각 확인 |
| 변증과 치료 방향 | [귀비탕](../formulas/guibi-tang.md)은 심비양허의 맥락에서 식욕·기력과 수면·심계를 함께 살핌 | [귀비탕·온담탕 비교](../compare/guibi-vs-wendan.md)에서 동반 증상과 배합의 차이 확인 |
| 문헌 수록 | 《금궤요략》은 [허로허번불면 조문](../classics/jinkui-yaolue/chapters/blood-bi-deficiency.md#clause-06-017)에 산조인탕을 제시함 | [산조인탕](../formulas/suanzaoren-tang.md)에서 원문과 구성을 확인하고, [동의보감 수록 동명방](../formulas/suanzaoren-tang.md#donguibogam-version)의 약미·제법을 따로 비교 |
| 연구의 평가 대상 | [산조인탕 임상근거](../authority/formulas/suanzaoren-tang.md#szrd-results)는 실제 시험 처방과 수면 결과를 연결함 | 원방·가감방, 단독·병용, 비교군과 평가 지표를 확인 |

예를 들어 ‘인삼이 들어간 처방’을 찾는 질문은 **구성 관계**로 답하고, ‘식욕저하와 오심이 함께 있을 때 처방의 차이’를 묻는 질문은 **증후·배합 관계**로 살핍니다. ‘그 처방을 사용한 연구 결과’는 **해당 연구의 대상과 치료 조건**까지 확인합니다.

## 출처를 함께 담은 온톨로지 데이터 {#ontology-data}

[온톨로지 JSON-LD](../assets/ai/ontology.jsonld)는 **개념의 이름·종류·대표 문서와 관계의 출처·적용 범위**를 함께 제공합니다. 사군자탕·육군자탕의 구성, 산조인탕의 동명 이방, 기허의 처방 맥락, 족삼리의 경맥 소속, 《금궤요략》의 조문·처방 관계를 먼저 정리했습니다. 전체 문서의 탐색 연결은 기존 [지식 그래프](../assets/ai/knowledge-graph.json)에서 확인할 수 있습니다.

| 관계 이름 | 뜻 | 출처와 함께 확인하는 조건 |
|---|---|---|
| `containsHerb` | 특정 처방 수록형에 포함된 본초 | 수록본·법제·기본 약미와 달일 때 더하는 재료 |
| `sharesFormulaStructureWith` | 두 처방이 공유하는 기본 약미 골격 | 수록본마다 다른 약량·제법과 추가 약재 |
| `sharesNameWith` | 이름이 같은 서로 다른 구성 | 산조인탕 금궤요략 5미형과 동의보감 몽문 7미형·생강 추가 |
| `hasTraditionalPatternContext` | 처방을 설명하는 전통 변증의 맥락 | 기허 가운데 식욕·기력·비위허약을 함께 보는 조건 |
| `belongsToMeridian` | 경혈의 소속 경맥 | 족삼리 ST36–족양명위경, 신문 HT7–수소음심경의 분류 관계 |
| `recordsFormula` | 고전 조문에 명시된 처방 수록형 | 서명·편목·조문과 해당 구성 |

**이름이 같아도 수록형의 식별자는 각각 유지합니다.** 《금궤요략》 산조인탕과 《동의보감》 산조인탕은 같은 문서 안에서도 서로 다른 개념으로 연결됩니다. 인삼·감초 같은 본초 개념과 처방 안에서의 거로·자(炙) 등 가공 조건도 나누어 기록합니다. 이렇게 하면 ‘어떤 산조인탕에 인삼이 들어가는가’, ‘육군자탕에서 생강·대조는 어떻게 기록되는가’처럼 출전과 구성을 함께 묻는 질문을 구체화할 수 있습니다.

개념 이름과 별칭은 [W3C SKOS](https://www.w3.org/TR/skos-reference/)로 표현합니다. 각 관계는 주체·관계명·대상과 함께 **본문 출처 주소와 적용 조건**을 가진 `rdf:Statement`로 제공합니다. 각 관계에는 본문에서 발췌한 근거 문장·표 행도 함께 제공합니다. 관계의 조건과 근거 발췌를 함께 확인하고, 인용은 연결된 본문의 해당 절과 원출처로 표시합니다. 최신 개념·관계 수와 파일 무결성은 [매니페스트](../assets/ai/knowledge-manifest.json)의 `ontology`에서 확인합니다. [AI·검색도구의 이용 순서](../ai/site-structure.md#ontology-retrieval)

## 어디에서 시작할까요? {#starting-points}

| 알고 있는 것 | 대표 경로 | 확인할 내용 |
|---|---|---|
| 아픈 부위·불편한 증상 | [증상별 감별·치료 지도](condition-to-treatment-map.md) | 통증·수면·소화·호흡기·여성건강의 원인과 치료 목표 |
| 피로와 회복 지연 | [피로·보익·회복](recovery-map.md) | 수면·섭취·활동과 보익 처방, 회복 단계 |
| 약재 이름 | [본초에서 처방 찾기](herb-to-formula-map.md) | 같은 약재가 처방마다 맡는 역할 |
| 처방 이름 | [처방에서 변증 찾기](formula-to-condition-map.md) | 구성·동반 증후·유사 처방과의 차이 |
| 경혈 이름·코드 | [배혈과 치료 설계](acupuncture-clinical-map.md) | 위치·해부학·국소와 원위 배혈·자극법 |
| 고전·의가 | [의가·저술·처방의 전승](physician-classic-formula-lineage.md) | 저술·편찬·의안·후대 정리의 구분 |
| 체질과 평소 몸 상태 | [사상의학 통합 안내](../sasang-integrated/index.md) | 소증과 현재 병증, 표리·순역·중증도와 처방 |
| 연구 논문 | [원전과 현대 연구 대조](classic-to-evidence-map.md) | 대상·실제 제제·비교치료·평가 결과 |

## 증상에서 치료와 경과로 {#_2}

[불면](../conditions/insomnia.md), [소화불량](../conditions/dyspepsia.md), [요통](../conditions/low-back-pain.md)은 각 본문에서 원인·변증·한약·침구·연구·생활관리를 이어 읽을 수 있습니다. 증상이 여럿 겹치면 [증상별 감별·치료 지도](condition-to-treatment-map.md)에서 어느 평가를 먼저 할지 살펴봅니다.

예를 들어 ‘허리가 아프고 다리가 저리다’는 표현에서는 [요통의 유형](../conditions/low-back-pain.md#_3)을 먼저 보고 [허리디스크](../conditions/lumbar-disc-herniation.md)·[협착증](../conditions/lumbar-spinal-stenosis.md)의 차이를 확인합니다. 이어 [요통 배혈](low-back-pain-acupoints.md#point-combinations)과 [운동의 방향](../conditions/low-back-pain.md#mckenzie-extension), [치료 후 기능](../conditions/low-back-pain.md#_12)을 연결합니다.

## 본초·방제를 비교하며 읽기 {#_3}

| 비교하는 단위 | 대표 문서 | 그 문서가 답하는 질문 |
|---|---|---|
| 한 약재와 여러 처방 | [본초→방제](herb-to-formula-map.md) | 인삼·황기·당귀 등이 배합에 따라 어떤 역할을 맡는가? |
| 두 약재의 관계 | [약대와 배합](herb-pair-combinations.md) | 반하·진피처럼 함께 쓰는 약재는 무엇을 보완하는가? |
| 처방군 | [처방군별 차이](formula-family-map.md) | 보기·화담·해표·이수·거풍습의 갈림점은 무엇인가? |
| 기본방과 변형 | [보익 처방의 구조·비교](tonic-formula-compare.md#formula-structure) | 사군자탕·육군자탕·팔물탕·십전대보탕은 어떻게 다른가? |
| 실제 조제 내용 | [원료·비율·제형](formula-composition-hub.md) | 같은 처방명이라도 생즙·분말·탕·환·고는 무엇이 다른가? |

인삼에서 출발했다면 [인삼 본초](../herbs/ginseng.md) → [사군자탕과 육군자탕](../compare/sijunzi-vs-liujunzi.md) → [소화불량의 처방 비교](../conditions/dyspepsia.md#formula-comparison) 순서로 읽어 보세요. 공통 약재를 확인한 뒤 반하·진피가 더해진 이유와 실제 증후를 비교할 수 있습니다.

## 경혈에서 배혈·해부학으로 {#_4}

[침구 임상 지식망](acupuncture-clinical-map.md)은 경혈 선택의 이유와 일반침·전침·약침의 차이, 한약과 병행할 때의 목표를 설명합니다. 상세 자료는 [불면](insomnia-acupoints.md)·[소화불량](dyspepsia-acupoints.md)·[요통](low-back-pain-acupoints.md)·[피로](fatigue-acupoints.md)로 나누어 경혈별 위치·배혈·해부학·연구를 확인합니다.

경혈의 위치는 [표준 아틀라스](../acupoint-network/standard-atlas.md), 유주는 [경락·경맥](../meridian-network/index.md), 실제 근육·신경과의 관계는 [임상 해부학](../clinical-anatomy/index.md)에서 읽습니다. 경혈 문서에서는 표준 위치를, 경맥 문서에서는 유주와 소속을, 해부학 문서에서는 실제 근육·신경과의 위치 관계를 확인합니다.

## 고전에서 구성과 연구로 {#_5}

[상한론 조문별 탐색](shanghan-taiyang-map.md)은 같은 처방이 등장하는 앞뒤 맥증과 치료 경과를 연결합니다. [고전→현대 연구](classic-to-evidence-map.md)는 그 질문을 현재의 질환·연구와 대조합니다. [예방·기능 회복 연구](../research/prevention-function.md)는 일상 기능과 생활 복귀를 중심으로 읽는 경로입니다.

예를 들어 《금궤요략》의 [허로허번불면](../classics/jinkui-yaolue/chapters/blood-bi-deficiency.md#clause-06-017)에서 시작해 [산조인탕의 구성](../formulas/suanzaoren-tang.md), [불면의 변증과 동반 증상](../conditions/insomnia.md#classical-clinical-reading), [산조인탕 임상연구](../authority/formulas/suanzaoren-tang.md#szrd-results)를 차례로 확인합니다. 고전의 병증과 현대 시험의 모집 기준, 원방과 시험 제제의 구성은 각각 확인합니다.

## 사상의학: 소증에서 병증·처방으로 {#sasang-network}

사상의학은 **평소의 소증과 현재의 변화를 비교하고, 체질별 병증 체계 안에서 치료 방향을 살피는 경로**로 연결합니다. 식욕·소화·수면·대변·땀의 평소 상태를 기준으로 현재 어떤 변화가 생겼는지 확인합니다.

| 확인할 질문 | 연결할 자료 | 이어서 살필 내용 |
|---|---|---|
| 평소 몸 상태를 어떻게 정리할까요? | [사상의학 소증으로 찾기](../sasang-symptoms/index.md) | 식사·배변·수면·발한 등 평소 소증과 발병 뒤 변화 |
| 현재 병증은 어디에 속하나요? | [체질·병증 탐색기](../sasang-explorer/index.md) · [체질별 병증 상세](../sasang-clinical-detail/index.md) | 체질별 표리·순역·단계, 유사 병증의 감별 |
| 어떤 원문과 지침에 근거하나요? | [원전·CPG 병증 근거지도](../sasang-clinical-detail/pattern-source-map.md) | 《동의수세보원》의 편명·조문과 지침의 분류·권고 |
| 처방의 구성과 차이는 무엇인가요? | [사상처방 비교](../sasang-formula-cards/comparison-map.md) · [건강→악화→회복 지도](../sasang-progression/index.md) | 병증에 따른 구성 차이와 치료 후 소증·생활기능의 변화 |

일반 변증의 기허·담음과 사상체질의 병증은 각각의 정의와 분류 안에서 확인합니다. 현대 질환명은 진단·검사·임상연구를 연결하는 축으로 함께 살피고, 체질병증은 해당 원전과 진료지침의 맥락을 유지합니다.

## 연결 자료를 읽는 기준 {#choose-network}

- **구성과 배합:** 포함된 본초와 함께 약미 전체·비율·법제·제형을 확인해 처방의 역할을 이해합니다.
- **문헌과 전승:** 수록·인용·가감·저술 관계를 나누고, 판본·편목·조문으로 기록의 위치를 확인합니다.
- **치료와 경과:** 배혈·자극법·병행치료의 목표를 확인하고, 치료 전후의 증상과 생활기능을 같은 기준으로 비교합니다.
- **연구와 적용 범위:** 세포·동물·건강인·환자 연구가 답하는 질문을 구분하고, 실제 제제·기간·비교군·결과·안전성을 함께 확인합니다.

검증할 원자료가 필요하면 [참고문헌 데이터베이스](../research/references/index.md), 개념이 낯설면 [진단·변증](../diagnostics/index.md), 사람과 약재의 이야기를 읽고 싶다면 [민성의담](../classical-stories/index.md)으로 이어갈 수 있습니다.


### 검색·AI 자료로 이어지는 연결 {#knowledge-reuse}

같은 개념의 한글명·한자명·경혈 코드와 대표 문서 주소를 함께 정리하면 여러 표현으로 같은 자료를 찾고 출처를 확인하기 쉬워집니다. 아카이브의 [AI·검색엔진용 사이트 구조](../ai/site-structure.md)에는 문서·동의어·분류·내부 연결을 제공하는 지식 그래프와 페이지별 자료의 이용 방법을 안내합니다. 기계가 읽는 자료는 문서 탐색에 활용하고, 개별 구성·치료·연구 관계를 인용할 때는 해당 본문의 설명과 원출처를 함께 확인합니다.
