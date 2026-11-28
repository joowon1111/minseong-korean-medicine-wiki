---
title: AI·검색엔진용 사이트 구조
description: 민성 한의학 아카이브의 AI 탐색 안내. 페이지 색인·본문 JSON·한의학 온톨로지의 역할과 실제 관계 탐색, 출처 앵커·문서 버전·임상근거를 확인하는 방법을 설명합니다.
tags: [AI검색, AEO, GEO, SEO, 사이트구조, 내부링크, 지식망, 한의학 온톨로지, JSON-LD]
last_reviewed: '2026-08-23'
---

# AI·검색엔진용 사이트 구조 {#ai}

민성 한의학 아카이브는 개별 문서를 나열하는 방식보다 **환자의 자연어 질문에서 출발해 전문 한의학 지식과 현대 임상근거까지 이어지는 계층형·관계형 구조**를 사용합니다.

## AI·검색도구 빠른 시작 {#machine-quickstart}

민성 한의학 아카이브(Minseong Korean Medicine Archive)는 민성한의원이 운영하는 공개 한의학 지식 아카이브입니다. **본문을 찾을 때는 페이지 색인, 개념 사이의 관계를 물을 때는 온톨로지, 답변의 출처를 제시할 때는 대표 HTML의 해당 절**을 사용합니다.

| 하려는 일 | 먼저 읽을 자료 | 다음에 확인할 항목 |
|---|---|---|
| 사이트의 주제와 대표 자료 파악 | [llms.txt](../llms.txt) · [핵심 색인](../ai-index.md) | 질문에 맞는 임상·본초·방제·경혈·사상의학 허브 |
| 특정 문서의 본문 읽기 | [페이지 색인](https://wiki.minseong.co.kr/assets/ai/page-index.json) | `pages`에서 `title`·`url` 확인 → 해당 `document`의 본문 JSON |
| 소제목 단위로 답과 출전 찾기 | 선택한 문서 JSON의 `sections` | 절의 `text`·`links`와 인용할 HTML 앵커 `url` |
| 처방의 구성·경혈 소속 등 관계 확인 | [온톨로지 JSON-LD](../assets/ai/ontology.jsonld) | 개념 ID → 관계 진술 → 본문 출처·적용 조건 |
| 관련 문서로 탐색 범위 확장 | [문서 지식 그래프](../assets/ai/knowledge-graph.json) | 문서 분류·별칭·내부 탐색 연결 |
| 데이터 범위와 파일 무결성 확인 | [매니페스트](../assets/ai/knowledge-manifest.json) | 현재 건수·파일 경로·각 데이터에 지정된 해시 |

한 주제의 질문에는 필요한 본문 JSON부터 읽고, 구성·소속·동명 이방을 비교할 때 온톨로지를 함께 확인합니다. [실제 관계 탐색 예시](#ontology-query-examples)와 [본문 JSON 필드](#page-json-fields)에서 구체적인 이용 방법을 볼 수 있습니다.

## 의서 편찬의 지혜를 잇는 지식 설계 {#classical-knowledge-design}

**민성 한의학 아카이브는 고전과 현대의 한의학 지식을 출처와 임상 맥락에 따라 연결하여, 환자와 한의사가 필요한 답을 정확하게 찾도록 돕는 지식 체계를 구축합니다.**

조선의 관찬의서와 이를 계승·발전시킨 주요 의서는 의학 지식을 모으고, 분류하고, 진료에 활용하기 쉽게 정리해 왔습니다. 아카이브는 이러한 편찬의 지혜를 오늘의 온톨로지와 AI 지식 설계에 적용합니다. 아래 표는 각 의서에서 착안한 현대적 설계 관점과 앞으로 지켜 갈 구축 원칙입니다.

| 의서에서 착안한 관점 | 아카이브에 반영할 설계 원칙 |
|---|---|
| 향약집성방 — 지역 지식의 표준화 | 본초·병증의 한글명·한자명·이명·현대 검색어를 연결하고, 원래 명칭과 출처를 보존합니다. |
| 의방유취 — 지식의 집대성 | 고전별 설명을 출전과 함께 연결하고, 같은 개념의 공통점과 차이를 탐색할 수 있도록 구성합니다. |
| 동의보감 — 인간·임상 중심의 재편 | 환자의 질문에서 증상·변증·치법·처방·본초·경혈로 이어지는 탐색 경로를 마련합니다. |
| 침구경험방 — 중재 지식의 체계화 | 경혈 위치·취혈·수기·적용 맥락을 구분해 연결하고, 각 설명의 근거를 표시합니다. |
| 제중신편·방약합편 — 실용적 압축 | 상세 문서 위에 핵심 비교표와 짧은 진료·학습 안내를 제공하여 필요한 설명부터 찾게 합니다. |
| 동의수세보원 — 개인의 차이 반영 | 체질·소증·현증·병증·처방의 관계를 세분화하여 처방 선택의 맥락을 설명합니다. |

의서의 편찬과 전승은 [한국 의서의 흐름](../history/classics-flow.md)에서, 원문과 편목은 [고전 원문·해석](../classics-reader/index.md)에서 확인할 수 있습니다. 향약의 수집·분류와 조선 전기 의서 편찬의 배경은 [국사편찬위원회 우리역사넷](https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_30&levelId=kc_r300775)을 참고합니다.

### 출처와 적용 조건까지 연결합니다 {#contextual-knowledge-design}

처방과 본초의 구성 관계에는 **원방·가감방·수록본·약량·포제·제법**을 함께 기록합니다. 병증과 처방의 관계에는 동반 증상과 변증 조건을 담고, 사상의학은 체질별 소증·현재 병증·치료 경과의 맥락을 유지합니다. 고전의 기록, 아카이브의 해설, 현대 연구, 의료기관의 진료 안내는 각각의 출처와 자료 성격을 표시해 연결합니다.

구축 성과는 개념·관계 수와 함께 **실제 질문에 맞는 설명과 근거를 얼마나 정확하게 찾을 수 있는가**로 살핍니다. ‘인삼이 들어간 처방은 무엇인가’, ‘같은 산조인탕의 구성은 왜 다른가’, ‘평소 소화 상태와 현재 불면을 어떻게 함께 살피는가’처럼 구체적인 질문에서 출발해 출처·조건·답변의 일치 여부를 확인합니다. 현재 제공하는 데이터와 이용 방법은 아래 [온톨로지 탐색 안내](#ontology-retrieval)와 [실제 관계 탐색 예시](#ontology-query-examples)에서 확인할 수 있습니다.

## 아카이브 대표 자료와 역할 {#featured-resources}

아래 자료는 아카이브가 중점적으로 연결하는 출발점입니다. 질문에 맞는 본문과 출처를 확인해 이용합니다.

| 자료 | 제공하는 내용과 다음 경로 |
|---|---|
| [361경혈 임상 아틀라스](../acupoint-network/standard-atlas.md) · [3D 경혈 지도](../acupoint-network/3d-map.md) | 표준 경혈 검색과 부위별 비교, 입체 위치 관계에서 혈자리 상세·해부학·고전 기록으로 연결. 3D 모형의 표시는 위치 학습을 위한 근사치입니다. |
| [민성의담](../classical-stories/index.md) | 고전과 실록의 인물·사건, 본초·처방·돌봄을 원출전과 함께 읽는 자체 해설 연재 |
| [고전 원문·해석](../classics-reader/index.md) · [동의보감 집례](../classics/donguibogam.md#jiprye) | 원문·판본·자체 풀이를 확인하고 병증·처방 및 현대 자료로 이어 읽는 경로 |
| [사상의학 통합 안내](../sasang-integrated/index.md) · [탐색기](../sasang-explorer/index.md) | 평소 소증과 현재 병증을 비교하고 체질병증·원전·처방을 탐색 |
| [핵심 처방 100선](../herbal-integrated/general-formulary.md#core-formulas-100) · [본초·방제](../herbal-integrated/index.md) | 처방의 출전·구성과 약재의 배합을 확인하고 관련 문서를 비교 |
| [연구·근거 안내](../portal/evidence.md) | 진료지침·임상연구의 대상·중재·비교군·결과·안전성과 원출처를 확인 |
| [증상·질환](../conditions/index.md) | 불면·소화불량·비염·통증 등에서 평가·한의학적 접근·근거로 연결 |
| [오늘의 한의학](../daily-korean-medicine/index.md) · [24절기 이야기](../daily-korean-medicine/solar-terms.md#stories) | 날짜별 학습 카드와 절기의 풍속·음식·본초·고전 이야기, 연도별 절입 시각 계산 |

각 자료의 역할에 맞춰 고전 기록·자체 풀이·현대 임상연구를 구분하고, 본문의 원출처와 적용 범위를 확인합니다.

## 핵심 탐색 흐름 {#_1}

`자연어 질문 → 증상·질환 → 위험신호·감별 → 한의학적 변증 → 본초·방제·침구치료 → 현대 임상근거 → PMID·DOI`

모든 문서를 이 순서대로 읽을 필요는 없습니다. 증상·처방·경혈·연구 중 알고 있는 정보에서 시작해 관련 문서로 이동합니다. R-code 등 분류 코드는 필요한 문서의 보조 정보이며, 코드나 내부 링크의 연결만으로 진단·처방의 적합성을 확정하지 않습니다.

### 질문에 따라 시작점을 고릅니다 {#choose-entry}

| 지금 찾는 것 | 먼저 읽을 자료 | 이어서 확인할 내용 |
|---|---|---|
| 증상은 알지만 진단명은 모름 | [증상으로 찾기](../symptom-integrated/index.md) | 관련 질환·감별·위험신호 |
| 특정 질환의 치료 연구 | [질환별 근거 안내](../authority/conditions/index.md) | 질환 본문의 연구 절 또는 고유한 근거 자료에서 대상·중재·비교군·결과 확인 |
| 같은 이름의 처방이 서로 다른 이유 | [처방 출전·구성](../herbal-integrated/general-formulary.md) | 수록본·약량·제형·가감과 비교 문서 |
| 비슷한 약재·처방의 차이 | [본초 비교](../herbal-integrated/herb-comparisons.md#interactive-comparison) · [처방 비교](../herbal-integrated/formula-structure.md#interactive-comparison) | 약용 부위·배합·출전·약량과 유사 처방의 감별 |
| 경혈의 위치와 혈자리별 상세 정보 | [3D 경혈 지도](../acupoint-network/3d-map.md) · [361경혈 임상 아틀라스](../acupoint-network/standard-atlas.md) | 입체 위치·경락 → 혈명·표준 위치·해부학·상세 문서 |
| 고전의 한 구절과 해석 | [고전 원문·해석](../classics-reader/index.md) | 서명·편목·조문·판본과 전후 문맥 |
| 사람과 사건으로 고전을 읽기 | [민성의담](../classical-stories/index.md) | 왕실 진료·돌봄·본초와 처방 이야기에서 실제 기록과 관련 문서 확인 |
| 매일 읽고 복습하기 | [오늘의 한의학](../daily-korean-medicine/index.md) · [학습실](../learning/index.md) | 날짜별 카드·생활 실천·원문 풀이와 과목별 복습 |
| 24절기 이야기와 절입 시각 | [24절기 이야기](../daily-korean-medicine/solar-terms.md#stories) · [절입 시각 계산](../daily-korean-medicine/solar-terms.md#solar-calculator) | 풍속·음식·본초·고전의 맥락과 연도별 한국 표준시 |
| 아카이브 전체 탐색 | [전체 둘러보기](../portal/maps.md) | 주제별 허브·고전·학습 도구·안내 |
| 한 문서를 도구에서 읽기 | [페이지 색인](https://wiki.minseong.co.kr/assets/ai/page-index.json) | 대표 주소와 페이지별 JSON |

예를 들어 ‘허리가 아플 때 침 연구’를 찾으면 [요통 문서](../conditions/low-back-pain.md)에서 증상의 범위를 확인하고, [같은 문서의 요통 연구 절](../conditions/low-back-pain.md#back-research)에서 해당 연구의 대상과 치료 조건을 읽습니다. 질환 설명과 연구 절을 함께 읽고, 탐색 링크의 연결과 개별 연구의 결론은 구분해 정리합니다.

## 1. 환자 언어와 증상 {#1}

- [증상으로 찾기](../symptom-integrated/index.md)
- [증상·질환](../conditions/index.md)
- [증상 기반 한약 탐색](../symptom-herbal-guide/index.md)
- [질문형 답변 가이드](../answer-guides/index.md)

질환명을 모르는 사용자도 “속이 더부룩해요”, “잠이 안 와요”, “허리가 오래 아파요”, “기침이 계속돼요” 같은 표현에서 시작하도록 설계합니다. 증상 안내에서 [진료 분야별 핵심 허브](../ai-index.md#clinical-hubs)와 대표 질환 본문으로 이어지며, 통합된 짧은 안내의 기존 주소는 해당 본문이나 관련 절로 연결합니다. 예를 들어 무릎의 동작별 통증은 [무릎통증](../conditions/knee-pain.md)에서 평가·치료·경과와 함께 읽습니다.

## 2. 질환과 현대 임상근거 {#2}

- [연구·근거 통합 안내](../portal/evidence.md)
- [출처·근거 카드 허브](../authority/index.md)
- [질환별 현대 근거 카드](../authority/conditions/index.md)
- [근거 가이드](../evidence-guide/index.md)
- [참고문헌 데이터베이스](../research/references/index.md)

**질환의 평가·변증·치료와 해당 임상근거를 함께 읽는 구조**를 우선합니다. 같은 질환을 반복 설명하던 확장·근거 카드는 기존 질환 본문의 연구 절로 통합하고, 기존 주소와 유입 링크는 대표 문서·해당 절로 이어지도록 유지합니다. 고유한 연구 질문을 다루는 자료와 여러 질환을 잇는 근거 허브는 관련 본문으로 연결합니다.

| 질문 | 현재 대표 경로 |
|---|---|
| 허리·목·어깨·무릎 통증의 평가와 치료 연구 | [요통 연구](../conditions/low-back-pain.md#back-research) · [목통증](../conditions/neck-pain.md) · [어깨통증 연구](../conditions/shoulder-pain.md#pain-research) · [무릎통증 연구](../conditions/knee-pain.md#_9) |
| 잠들기 어렵거나 식후 더부룩할 때의 치료 연구 | [불면 연구](../conditions/insomnia.md#sleep-research) · [기능성소화불량 연구](../conditions/functional-dyspepsia.md#pds-acupuncture-results) |
| 국내 한의치료·일본 Kampo·국제 지침을 함께 찾기 | [연구·근거 통합 안내](../portal/evidence.md) → 실제 대상·제제·치료·비교군·기간·결과·원 논문 |

연구를 인용할 때는 현재 도착한 대표 문서의 해당 절을 확인합니다. CPG·체계적 문헌고찰·무작위시험·관찰연구·기전연구는 서로 다른 질문에 답하는 자료이며, 원방·가감방·시험제제의 차이도 함께 표시합니다.

## 3. 본초와 방제 {#3}

- [본초학](../herbs/index.md)
- [방제학](../formulas/index.md)
- [임상 핵심 처방 100선: 출전·구성·용량](../herbal-integrated/general-formulary.md)
- [본초 비교·감별](../herbal-integrated/herb-comparisons.md#interactive-comparison) · [처방 구조·비교](../herbal-integrated/formula-structure.md#interactive-comparison)
- [대표 본초 근거 카드](../authority/herbs/index.md)
- [한약 처방 임상근거](../research/formulas/index.md)

본초와 방제는 효능·치법·임상영역별 분류와 질환별 근거를 연결합니다. 약재에서 처방으로, 증상에서 변증·처방으로 찾아가는 상세 경로는 [본초·방제 지식축](#herbal-formula-axis)에서 확인할 수 있습니다.

## 4. 경혈·침구치료 {#4}

- [침구·치료 통합 허브](../acupuncture-integrated/index.md)
- [WHO 표준 361경혈 임상 아틀라스](../acupoint-network/standard-atlas.md)
- [3D 경혈 지도](../acupoint-network/3d-map.md)
- [침 치료 근거 카드](../authority/acupuncture.md)

경혈은 한글명과 WHO 국제 표준 코드를 함께 사용해 국내 검색과 국제 논문 탐색을 동시에 지원합니다. [경혈·침법 통합 탐색](../acupoint-network/standard-atlas.md#clinical-explorer)에서 경혈명·증상·근육·신경을 검색하고 경락·부위로 좁혀 표준경혈·사암침·동씨기혈의 기존 상세 문서로 이동합니다. [부위별 비교 학습](../acupoint-network/standard-atlas.md#regional-learning)과 [3D 경혈 지도](../acupoint-network/3d-map.md)는 위치 이해를 돕고, 상세 본문은 위치·주치 출처·해부학·임상근거를 구분해 제공합니다. 혈자리 이름과 고전 기록을 풀어낸 이야기가 있는 상세 문서에서는 이야기의 출전과 해설을 함께 확인할 수 있습니다. [경혈·침구 포털](../portal/acupuncture.md)에서도 아틀라스와 3D 지도로 이동합니다.

## 5. 지식그래프 {#5}

[통합 한의학 지식 그래프](../network/index.md)에서는 본초·방제·증상·고전·연구 사이를 오가며 읽을 수 있습니다. 각 분야의 세부 관계는 다음 세 지식축으로 연결합니다.

| 지식축 | 중심 관계 |
|---|---|
| [본초·방제](#herbal-formula-axis) | 증상·변증·치법, 구성 본초·배합, 처방 비교와 근거 |
| [침구·신경·초음파](#_4) | 증상 위치·신경·근육, 경혈·침구와 임상해부학 |
| [사상의학](#_6) | 소증·현재 병증, 체질병증·처방과 원전 |

### 본초·방제 지식축 {#herbal-formula-axis}

본초·방제 영역은 **증상과 변증에서 처방을 찾아가는 경로**와 **약재의 구성·배합에서 처방을 비교하는 경로**를 함께 제공합니다. 보기·보혈·이기·화담·청열·이수 등 본초의 효능별 분류를 처방의 전체 치법과 연결하고, 고전의 수록 맥락과 현대 임상근거까지 이어 읽도록 구성합니다.

#### 핵심 허브 {#herbal-formula-hubs}

| 찾는 내용 | 연결할 자료 |
|---|---|
| 본초·방제의 전체 흐름 | [본초·방제 한눈에 보기](../herbal-integrated/index.md) |
| 효능별 약재와 임상영역별 처방 | [본초 찾기](../herbal-integrated/herbs.md)·[방제 찾기](../herbal-integrated/formulas.md) |
| 약재의 역할과 처방 전체의 배합 | [본초→방제 역탐색](../network/herb-to-formula-map.md)·[방제 구조](../formula-architecture/index.md) |
| 증상·변증에서 처방 비교 | [방제→질환·변증 지도](../network/formula-to-condition-map.md)·[질환→치료 지도](../network/condition-to-treatment-map.md) |
| 고전·의가와 처방의 관계 | [의가·고전·처방 계보](../network/physician-classic-formula-lineage.md) |
| 본초와 복합 처방의 현대 연구 | [본초 근거](../authority/herbs/index.md)·[한약·처방 임상근거](../authority/formulas/herbal-formula-evidence-hub.md) |

#### AEO 질문 의도 {#herbal-formula-aeo}

사용자가 실제로 묻는 비교·선택 질문을 해당 설명으로 연결합니다.

- [같은 인삼이 들어가도 처방의 역할은 왜 다른가요?](../network/herb-to-formula-map.md#_2)
- [피로할 때 보중익기탕과 십전대보탕은 무엇이 다른가요?](../compare/buzhong-vs-sipjeondaebo.md)
- [소화가 약할 때 사군자탕과 육군자탕은 어떻게 구분하나요?](../compare/sijunzi-vs-liujunzi.md)
- [불면과 두근거림에서 귀비탕과 온담탕은 어떻게 다른가요?](../compare/guibi-vs-wendan.md)
- [녹용보약은 어떤 점을 확인하고 상담하나요?](../conditions/deer-antler-tonic-guide.md)
- [한약 복용 뒤 무엇이 달라졌는지 어떻게 기록하나요?](../conditions/herbal-followup.md)

#### GEO 관계 {#herbal-formula-geo}

| 출발점 | 명확히 연결할 관계 |
|---|---|
| 증상·질환 | 감별과 변증의 단서, 치법, 비교할 처방과 경과 관찰 |
| 본초 | 기원·약용부위·포제, 효능, 함께 배합되는 약재와 처방 안의 역할 |
| 방제 | 구성·배합·가감, 유사 처방의 차이, 고전 출전과 수록본 |
| 연구 | 실제 사용한 처방·제형·대상·결과와 원문 출처 |

같은 본초를 포함한다고 처방 전체의 역할이 같지는 않습니다. 단일 성분·약재 연구와 복합 처방 연구, 원방과 가감방의 결과를 구분해 읽으며, 증상과 처방의 연결은 개인에게 맞는 치료를 자동으로 확정하는 관계가 아닙니다.

### 침구·신경·초음파 지식축 {#_4}

침구 영역은 증상 위치와 신경·근육·경혈의 관계를 현대 임상해부학과 연결합니다.

`환자 자연어 질문 → 증상·저림 위치 → 신경근 → 말초신경 → 근육 → 포착부위 → 초음파 → 경혈 → 침구치료 → 현대 임상근거`

#### 핵심 허브 {#_5}
- [침구·치료 포털](../portal/acupuncture.md)
- [신경포착증후군](../nerve-entrapment/index.md)
- [근육·말초신경 임상해부학](../clinical-anatomy/index.md)
- [침의 과학적 접근](../acupuncture-science/index.md)
- [근골격계 초음파](../musculoskeletal-ultrasound/index.md)

#### AEO 질문 의도 {#aeo}

- 손가락 저림은 어느 신경과 관련되는가?
- 손목터널 초음파에서 정중신경은 어떻게 평가하는가?
- L5 신경근병증과 총비골신경 포착은 어떻게 연결되는가?
- 침은 말초신경·척수·뇌에 어떻게 작용하는가?
- 전침의 주파수와 자극 강도는 어떤 의미인가?
- 초음파 유도 침구치료는 어떤 해부학적 구조를 확인하는가?

#### GEO 관계 {#geo}

전통 경혈 지식과 현대 임상해부학을 동일시하지 않고 다음처럼 연결합니다.

`WHO 경혈 → 주변 해부층 → 근육 → 말초신경·혈관 → 척수 분절 → 자침 → 질환별 임상근거`

### 사상의학 지식축 {#_6}

사상의학 영역은 체질 이름을 단순한 성격·체형 분류로 제공하지 않고 다음 관계로 구조화합니다.

`사상의학 → 사상인 → 장부 기능의 상대적 균형 → 소증 → 현재 병증 → 표리병증 → 증상 → 처방 → 원전 → 현대근거`

#### 핵심 허브 {#_7}
- [사상의학 한눈에 보기](../sasang-integrated/index.md)
- [소양인](../sasang-integrated/soyangin.md)
- [소음인](../sasang-integrated/soeumin.md)
- [태음인](../sasang-integrated/taeeumin.md)
- [태양인](../sasang-integrated/taeyangin.md)
- [증상으로 사상체질 이해하기](../sasang-symptoms/index.md)
- [사상체질·병증 처방 탐색기](../sasang-explorer/index.md) · [사상체질 임상 감별](../sasang-pattern-differential/index.md)

탐색기에서는 체질 → 소증·현재 병증 → 원문·유사 병증 감별 → 대표 처방으로 이동하고, 체질별 음식·양생·운동 자료를 함께 읽습니다. [소증 9항목](../sasang-original-symptoms/index.md)은 식욕·소화부터 성정·정서까지 평소 상태를 원문과 함께 살피는 입구입니다.

#### AEO 질문 의도 {#aeo_1}
- 사상의학이란 무엇인가?
- 사상인이란 무엇인가?
- 소양인·소음인·태음인·태양인의 차이는 무엇인가?
- 비대신소·신대비소·간대폐소·폐대간소는 무엇인가?
- 소증은 왜 중요한가?
- 같은 불면·소화불량·피로라도 체질별로 어떻게 다르게 보는가?

#### GEO 관계 {#geo_1}
전통적인 장부 대소는 실제 장기 크기와 동일시하지 않고 **사상의학적 기능의 상대적 균형**이라는 원전·이론적 맥락에서 제공합니다.

현대 질환명과 사상체질 병증을 자동으로 1:1 대응시키지 않고, 소증·현재 병증·원전·현대 연구를 구분해 연결합니다.

#### 사상체질 음식 탐색 {#_8}

사상의학의 생활관리 영역에서는 체질식 정보를 다음 관계로 제공합니다.

`사상인 → 평소 소증 → 현재 병증 → 소화상태 → 음식 선택 → 섭취 후 반응`

- [사상체질별 음식 가이드](../sasang-food/index.md)

체질별 음식은 절대적인 금기표로 구조화하지 않고, 개인의 현재 상태와 실제 반응을 함께 해석하도록 연결합니다.

## 6. AI용 핵심 색인 {#6-ai}

[AI 핵심 색인](../ai-index.md)에서 주요 주제와 대표 문서로 이동할 수 있습니다. 인용할 때는 **해당 문서의 주소와 제목 옆 `¶` 링크**를 사용하고, 연구 결과는 연결된 원문 출처까지 함께 확인합니다.

| 찾는 내용 | 대표 입구 |
|---|---|
| 증상과 진료 분야별 평가·치료 | [AI 색인의 임상 허브 지도](../ai-index.md#clinical-hubs) · [핵심 주제 허브](../pillar/index.md) |
| 호흡기와 별도 순환기·심혈관 자료 | [호흡·인후·성대](../pillar/respiratory-rhinitis-immune.md) · [혈압·심장·혈관](../pillar/circulation-cardiovascular.md) |
| 수면·정서·신경과 기능 경과 | [수면 허브](../pillar/sleep-neuro.md) · [브레인포그](../answer-guides/brain-fog-focus-guide.md) |
| 고전 원문·임상 연결 | [고전 원문·해석](../classics-reader/index.md) · [AI 색인의 읽기·복습 지도](../ai-index.md#classics-learning-daily) |
| 인물·왕실 진료·본초·처방 이야기 | [민성의담](../classical-stories/index.md) |
| 날짜별 지식·생활 카드와 24절기 | [오늘의 한의학](../daily-korean-medicine/index.md) · [24절기 생활 일력](../daily-korean-medicine/index.md#daily-solar-terms) · [절기 이야기·절입 시각](../daily-korean-medicine/solar-terms.md#stories) |
| 전체 주제와 안내 찾아보기 | [전체 둘러보기](../portal/maps.md) · [아카이브 안내](../guide/index.md) |
| 일곱 과목 학습·오답 복습 | [기초 한의학 퀴즈 & 학습실](../learning/index.md) |
| 영어로 한의학을 처음 이해하기 | [Korean Medicine Guide](../korean-medicine-guide/index.md) |

관련 문서의 연결은 주제를 더 살펴보기 위한 안내입니다. 개별 환자에게 맞는 진단·치료 여부는 본문의 적용 맥락과 함께 판단합니다.

### 고전·이야기·생활 카드에서 본문으로 이어 읽기 {#classics-stories-daily}

상단 메뉴는 **홈 → 한의학 기초 → 고전 원문·해석 → 본초·방제 → 침구·치료 → 증상·질환 → 사상의학 → 연구·근거 → 민성의담 → 전체 둘러보기**로 구성합니다. 전체 둘러보기에서는 지식망·학습실·안내를 찾고, 용어사전은 진단·변증 하위에서, 온병학 지식망은 한의학 고전 하위에서 탐색합니다.

| 자료 | 읽고 확인할 내용 | 다음 문서 |
|---|---|---|
| 고전 원문·해석 | 상한론·금궤요략·동의보감·동의수세보원의 조문·편목·판본, 원문과 한국어 풀이 | [원문을 깊이 읽는 관점](../classics-reader/index.md#close-reading) → 병증·치법·본초·처방과 현대 임상 자료 |
| 민성의담 | 일반 칼럼과 사상의학 이야기의 별도 회차, 최신순 목록, 실제 인물·사건·기록과 해석 | [민성의담 목록](../classical-stories/index.md) → 각 이야기의 원출전과 관련 본문 |
| 오늘의 한의학 | 날짜별 경혈·본초·상한론·사상의학, 원문 풀이·복습 문답 | [날짜별 카드](../daily-korean-medicine/index.md) → 경혈·본초·조문·사상병증 상세 문서 |
| 양생·24절기 생활 일력 | 240개 생활 카드의 해설·작은 실천, 절기별 풍속·음식·본초·고전 이야기 | [양생 카드 검색](../daily-korean-medicine/index.md#daily-yangsheng-library) · [24절기 이야기](../daily-korean-medicine/solar-terms.md#stories) → 고전 원문과 현대 생활 자료 |
| 연도별 절입 시각 | 1900–2100년 절입 시각을 한국 표준시(KST)로 표시 | [절입 시각 계산기와 자료·계산 근거](../daily-korean-medicine/solar-terms.md#solar-calculator) → 절기별 이야기와 공식 월력요항 |

하루 카드의 날짜는 한국 시간을 기준으로 하며, 절기 당일에는 해당 절기 안내를 우선 표시합니다. 다른 날짜에 순환해서 읽는 절기 카드와 당일 안내를 구분합니다. 일력의 절기 당일 표시는 날짜 전체에 적용되고, 계산기는 절입 시각을 별도로 보여줍니다. 고전 원문·아카이브의 풀이·현대 생활 제안의 역할을 나누어 읽고, 역사적 치료 기록을 현대 치료의 효과 입증으로 바꾸어 인용하지 않습니다.

### 페이지별 본문과 지식 그래프를 구분해 사용합니다 {#page-json-navigation}

[page-index.json](https://wiki.minseong.co.kr/assets/ai/page-index.json)은 각 페이지의 제목·대표 HTML 주소(`url`)·JSON 주소(`document`)를 제공합니다. 한 주제의 본문을 읽을 때는 해당 `document`를 선택하거나 HTML의 JSON 대체 링크를 사용합니다. 페이지별 JSON에는 렌더링한 본문, 실제 제목 앵커, 출처·관련 링크가 담깁니다.

#### 본문 JSON의 필드 {#page-json-fields}

| 필드 | 실제 형식과 용도 |
|---|---|
| `url` · `title` · `language` · `description` | 대표 HTML 주소·제목·언어·문서 설명 |
| `text` | 공개 본문의 전체 텍스트. 도입부와 절 사이의 문맥 확인 |
| `headings` | `level`·`title`·`url`을 가진 제목 목록. 실제 HTML 앵커로 이동 |
| `sections` | `title`·`level`·`url`·`text`·`links`를 가진 H2/H3 절 목록 |
| `links` · `sections[].links` | 각각 본문 전체·해당 절의 HTTP(S) 주소 문자열 목록. 내부 탐색·외부 원출처가 함께 포함됨 |
| `related_reading` | 문서에 명시한 관련 읽기 자료. 항목이 있으면 다음 탐색에 활용 |
| `ontology` | 등록된 개념·관계가 연결된 문서에서 제공. `document`는 문서별 JSON-LD, `concept_ids`는 본문에서 설명하는 개념, `statement_ids`는 관련 관계 진술 |
| `provenance` | 제공된 문서 식별번호·본문 및 소스 지문·빌드 기준 Git 커밋. [버전 대조 방법](#version-and-citation) 참고 |

색인의 `document` 주소와 제목의 `url`을 그대로 따라가면 현재 공개 파일과 실제 절을 찾을 수 있습니다. [페이지 색인](https://wiki.minseong.co.kr/assets/ai/page-index.json)의 `pages`에는 `url`·`title`·`document`가 들어 있습니다. 온톨로지 관계가 연결된 문서에는 `ontology_document`도 있어 문서별 JSON-LD로 바로 이동할 수 있습니다.

#### 본문 절에서 근거까지 확인하기 {#section-retrieval}

페이지별 JSON의 `sections`는 실제 앵커가 있는 H2·H3 제목 단위의 **제목·앵커 주소·해당 절의 본문·링크**를 제공합니다. 다음 H2·H3가 나오기 전까지의 연속된 본문이 한 절에 담기며, H3 하위 절을 H2 본문에 다시 복사하지 않습니다. 첫 소제목 앞의 도입부나 앵커가 없는 HTML 제목의 내용은 전체 `text`에서 읽습니다. 이는 같은 공개 HTML을 다른 형식으로 제공하는 기능이며, 검색 노출을 위한 별도 요약문이나 새 의학적 판단을 생성하지 않습니다.

| 단계 | 확인할 내용 |
|---|---|
| 대표 문서 선택 | 색인의 제목과 `url`이 질문에 해당하는지 확인 |
| 해당 절 읽기 | `sections`의 제목·본문에서 답과 적용 조건을 함께 확인 |
| 앞뒤 문맥 비교 | 전체 `text`와 HTML에서 정의·감별·안전 정보 확인 |
| 출전 확인 | 절 안의 링크를 열어 원전 위치 또는 실제 연구 대상·중재·결과 확인 |
| 인용 | 해당 절의 HTML 앵커 주소와 필요한 원출처를 함께 제시 |

절의 `links`는 그 위치에 나타나는 링크 목록입니다. 참고문헌·내부 탐색 링크가 함께 들어갈 수 있으므로, 링크의 존재를 그 절의 모든 주장이 검증되었다는 뜻으로 해석하지 않습니다. 본문의 문헌명·판본·조문, 원방·가감방, 연구 제제와 적용 범위는 인용 과정에서도 유지합니다. [자료 차이의 처리](../guide/editorial-policy.md#source-differences) · [문서 상태 해석](../guide/status-policy.md#reading-status)

#### 필드가 없거나 답이 충분하지 않을 때 {#retrieval-gaps}

| 읽다가 만난 상황 | 다음 확인 |
|---|---|
| 제목은 비슷하지만 다른 병증·처방을 설명함 | 문서 첫 문단과 출전을 비교해 질문에 맞는 대표 문서를 다시 선택 |
| 절에 원출처 링크가 없음 | 전체 본문의 참고문헌 절과 관련 근거 카드를 확인하고, 원출처 확인 여부를 밝혀 설명 |
| JSON에 원하는 소제목이 없음 | HTML의 실제 제목·표·도구 안내를 확인하고 전체 `text`와 비교 |
| 날짜·검토자·식별자가 없음 | 작성일·감수자·PMID·DOI를 추정해서 채우지 않고 확인 가능한 범위만 사용 |
| HTML과 저장해 둔 JSON의 내용이 다름 | 현재 대표 HTML과 그 페이지가 연결한 JSON을 다시 확인하고 이전 수집본과 섞지 않음 |
| 검색해도 질문에 답할 자료가 없음 | 찾지 못한 범위를 명시하고, 인접 문서의 설명을 해당 질문의 확정 답으로 바꾸지 않음 |

제목·본문의 일치 여부는 검색 결과의 순서보다 먼저 확인합니다. [출처 확인 범위](../guide/citation-policy.md#source-access)와 [결과 수치 해석](../guide/citation-policy.md#outcome-interpretation)을 함께 적용하면 요약 과정에서 근거의 범위를 유지할 수 있습니다. 페이지별 JSON은 공개 본문의 읽기 자료이며, 검색 질의를 실행하는 API나 진단·처방을 반환하는 서비스로 제공하는 것은 아닙니다.

[지식 그래프](https://wiki.minseong.co.kr/assets/ai/knowledge-graph.json)는 문서 개체·동의어·분류·내부 연결을 탐색하는 자료이고, [매니페스트](https://wiki.minseong.co.kr/assets/ai/knowledge-manifest.json)는 해당 빌드의 문서·관계 수와 무결성을 확인하는 자료입니다. 개별 주장을 인용할 때는 JSON 주소보다 원문 HTML의 해당 절과 연구 출처를 표시합니다. [데이터별 안내](../ai-index.md#_17) · [llms.txt](https://wiki.minseong.co.kr/llms.txt)

### 한의학 온톨로지에서 관계 확인하기 {#ontology-retrieval}

[온톨로지 JSON-LD](../assets/ai/ontology.jsonld)는 기존 본문에서 선별한 **본초·처방 수록형·변증·치법·경혈·경맥·고전 조문**을 개념으로 구분합니다. 문서 링크를 모은 `knowledge-graph.json`과 함께 사용하되, 출전별 구성이나 소속 관계를 묻는 질문은 [관계 정의](../network/index.md#ontology-data)와 연결된 본문을 확인합니다.

| 항목 | 확인 방법 |
|---|---|
| 개념 식별자 `@id` | `ontology.jsonld#` 뒤의 고유 이름으로 개념을 구별. 문서 주소와 개념 식별자는 역할을 나눔 |
| `skos:prefLabel` · `skos:altLabel` | 대표 이름과 별칭으로 후보 검색. 같은 별칭이 여러 수록형에 있을 수 있으므로 출전을 비교 |
| `@type` · `foaf:page` | 개념의 종류와 내용을 확인할 대표 본문·해당 절 |
| `rdf:Statement` | `rdf:subject`·`rdf:predicate`·`rdf:object`를 한 관계로 읽음 |
| `dcterms:source` · `skos:scopeNote` | 관계를 확인한 본문과 수록본·법제·동반 증후 등의 조건 |
| `dcterms:description` | 해당 출처 절에서 그대로 가져온 근거 문장·표 행. 발췌와 앞뒤 문맥을 함께 확인 |
| 매니페스트의 `ontology` | 현재 제공하는 개념·관계·관계 유형 수와 파일 SHA-256 |

#### 이름에서 개념 ID 고르기 {#ontology-name-resolution}

대표 이름과 별칭은 검색 후보를 찾는 단서입니다. 관계를 조회할 때는 **개념의 종류·정의·출전과 원문 약명**을 비교해 대상 ID를 고릅니다. 하나의 문서 주소를 공유하는 개념도 각각의 ID와 구성 관계를 유지합니다.

| 입력한 이름·질문 | 구분할 개념 ID | 다음 확인 |
|---|---|---|
| 복령 계열의 약명이 들어간 처방 | `poria` · `white-poria` · `red-poria` · `poria-spirit` | 원하는 약명별로 `containsHerb`의 대상을 선택하고, 결과에 원문 약명과 해당 ID를 함께 표시. [약명별 비교](../network/index.md#ontology-name-resolution) |
| 생강인가, 건강인가? | `fresh-ginger` · `dried-ginger` | 각 구성 진술의 `skos:scopeNote`에서 기본 약미·전탕 추가·가공 조건 확인 |
| 반하와 반하곡의 구성 기록 | `pinellia` · `pinellia-ferment` | 반하 문서를 함께 참조하더라도 각각의 ID로 조회하고, 곽향정기산 국방형의 半夏曲 발췌 확인 |
| 계지·육계·계심의 원문 약명 | `cinnamon-twig` · `cinnamon-bark` · `cinnamon-heart` | `skos:definition`과 해당 처방의 근거 발췌에서 명칭·원료·포제 확인 |
| 작약과 백작약의 기록 | `shaoyao-source-name` · `white-peony` | 芍藥과 백작약 명시 여부를 수록형별로 대조 |
| 산조인탕에 인삼이 들어가는가? | `suanzaoren-jinkui` · `suanzaoren-donguibogam` | 두 수록형을 선택한 뒤 각각의 `containsHerb`에서 `ginseng` 조회. [구성 원문 비교](../formulas/suanzaoren-tang.md#formula-variant-comparison) |

구성 탐색의 응답에는 **처방 수록형 ID·본초 ID·원문 약명·관계명·출처 절·적용 조건·근거 발췌**를 함께 보존합니다. 예를 들어 ‘복령 계열 전체’를 비교할 때는 위 네 ID를 각각 조회하고 결과를 약명별로 묶습니다. ‘복신이 들어간 처방’을 물으면 `poria-spirit`을 대상으로 선택합니다. 등록 범위 밖의 구성은 실제 처방 본문에서 추가로 확인합니다.

#### 한 문서에서 관련 관계만 읽기 {#page-ontology}

인삼·사군자탕·산조인탕·족삼리처럼 온톨로지에 등록된 개념을 설명하는 페이지는 본문 JSON의 `ontology.document`와 HTML의 `link rel="describedby" type="application/ld+json"`에서 **그 문서와 관련된 관계만 담은 JSON-LD**로 이어집니다. 전체 온톨로지를 받지 않고도 해당 개념의 구성·소속·출처 관계를 확인할 수 있습니다.

`concept_ids`는 현재 본문에서 직접 설명하는 개념이고, `statement_ids`는 그 개념을 주체·대상으로 삼거나 현재 본문을 출처로 기록한 관계입니다. 비교 문서처럼 관계의 출처 역할을 하는 페이지에는 `concept_ids`가 비어 있고 관련 진술만 연결될 수 있습니다. JSON-LD의 `@graph`에는 관계 양끝의 개념과 관계 정의를 함께 담아 이름과 의미를 확인할 수 있게 했습니다.

문서별 데이터에서도 **전역 개념 ID와 관계 ID, 출처·조건·근거 발췌**를 유지합니다. 예를 들어 인삼 문서에서 사군자탕·육군자탕·동의보감 산조인탕의 구성 관계를 찾고, 각 진술의 출처 절에서 법제·약미·제법을 비교합니다. 산조인탕 페이지에서는 두 수록형의 식별자를 따로 확인합니다. 인용에는 연결된 대표 HTML의 해당 절을 사용합니다.

#### 실제 관계 탐색 예시 {#ontology-query-examples}

아래 ID는 `https://wiki.minseong.co.kr/assets/ai/ontology.jsonld#` 뒤에 붙는 개념 식별자입니다. JSON-LD의 `@context`에서 `km` 접두어가 이 주소를 가리킵니다. 파일을 읽는 도구는 `@graph` 안의 개념과 관계 진술을 선택해 아래처럼 탐색할 수 있습니다.

| 질문 | 데이터에서 선택할 관계 | 본문에서 확인할 내용 |
|---|---|---|
| 인삼이 들어간 처방은? | `rdf:predicate`가 `km:containsHerb`, `rdf:object`가 `ginseng`인 진술에서 주체 선택 | 현재 구조화한 `sijunzi-guofang`·`liujunzi-yixuexinwu`·`suanzaoren-donguibogam`의 출전·법제·전체 약미. 더 넓은 처방 목록은 [인삼 역탐색](../network/herb-to-formula-map.md#_2) |
| 산조인탕에 인삼이 들어가는가? | `suanzaoren-jinkui`·`suanzaoren-donguibogam`을 구별하고 `km:sharesNameWith` 진술 확인 | [금궤요략 5미형](../formulas/suanzaoren-tang.md#source-dose-original)과 [동의보감 몽문 수록형](../formulas/suanzaoren-tang.md#donguibogam-version)의 약미 대조 |
| 기허·비허담습의 치료 방향은? | `qi-deficiency` 또는 `spleen-qi-deficiency-with-phlegm`에서 `km:hasTraditionalTreatmentPrinciple`의 대상 확인. 육군자탕은 `km:hasTraditionalPatternContext`로 변증에 연결 | [기허의 보기·건비](../pattern-treatment/qi-deficiency.md#treatment-principle), [비허담습의 익기건비·화담](../pattern-treatment/phlegm-fluid.md#spleen-qi-phlegm-care)과 동반 증후·배합 조건 |
| 혈허·기혈양허의 치법과 처방 맥락은? | `blood-deficiency`·`qi-blood-deficiency`에서 `km:hasTraditionalTreatmentPrinciple`을 조회하고, 해당 변증을 대상으로 하는 `km:hasTraditionalPatternContext`의 주체를 확인 | [보혈·기혈쌍보](../pattern-treatment/blood-deficiency.md#treatment-principle), 사물탕 국방형·팔진탕 만병회춘형·십전대보탕 국방형의 출처·구성 및 냉감·소화 조건. 혈허의 증상 조합과 빈혈 검사 진단을 구분 |
| 불면·소화불편에서 귀비탕과 온담탕의 변증·치법은? | `guibi-jisheng`·`guibi-donguibogam` → `heart-spleen-deficiency` → `tonify-qi-nourish-blood-calm-spirit`, `wendan-sanyin` → `gallbladder-stomach-disharmony` → `regulate-qi-transform-phlegm-harmonize-stomach`를 두 종류의 관계로 각각 조회 | [심비양허의 보기양혈·안신](../pattern-treatment/heart-spleen-deficiency.md#treatment-principle)과 [담위불화의 이기화담·화위이담](../pattern-treatment/phlegm-fluid.md#phlegm-stomach-care). 귀비탕 8미·10미와 전탕 추가, 삼인방 권9 허번 온담탕 6미·생강 대조의 제법, 후대 해설의 적용 조건 확인 |
| 반하후박탕·육군자탕·온담탕은 어떤 맥락으로 구분하나요? | 각 수록형의 `hasTraditionalPatternContext`를 조회한 뒤 해당 변증의 `hasTraditionalTreatmentPrinciple`을 선택. `banxia-houpo-jinkui` → `phlegm-qi-binding` → `move-qi-dissipate-binding-transform-phlegm`, `liujunzi-yixuexinwu` → `spleen-qi-deficiency-with-phlegm`, `wendan-sanyin` → `gallbladder-stomach-disharmony`의 경로를 각각 유지 | [세 변증의 갈림점](../pattern-treatment/phlegm-fluid.md#phlegm-qi-binding-care)에서 목 이물감·긴장, 비위허약, 오심·수면불편의 중심을 비교. 각 관계의 출처·조건과 원문 약명·약량을 확인하고 공통 본초와 개별 처방의 맥락을 함께 보존 |
| 피로·식욕저하에서 사군자탕·보중익기탕·십전대보탕을 어떻게 구분하나요? | `sijunzi-guofang` → `qi-deficiency` → `tonify-qi`, `buzhong-piwei` → `sinking-middle-qi` → `tonify-qi-raise-yang`, `shiquan-guofang` → `qi-blood-deficiency` → `tonify-qi-and-blood`의 두 관계를 각각 조회 | [세 보익 처방의 선택 맥락](../compare/buzhong-vs-sipjeondaebo.md#three-tonic-contexts)과 각 진술의 출처·조건 확인. 비위론의 원문 승양 설명과 현대 변증 해설, 원문 약량과 전탕 재료를 구분 |
| 족삼리는 어느 경맥에 속하는가? | 주체 `st36`, 관계 `km:belongsToMeridian`인 진술에서 대상 `stomach-meridian` 확인 | [족양명위경의 소속 경혈표](../meridian-network/stomach-meridian.md#_3)와 [족삼리의 위치·해부학](../acupuncture/points/st36-zusanli.md) |
| 황기가 들어간 처방은? | 관계 `km:containsHerb`, 대상 `astragalus`인 진술의 주체를 조회 | 보중익기탕·당귀보혈탕·십전대보탕·쌍화탕·귀비탕의 수록형과 각 포제·약량 |
| 귀비탕에는 당귀·원지가 들어가는가? | `guibi-jisheng`과 `guibi-donguibogam`을 각각 선택 | 제생방 기본 8미와 동의보감의 당귀·원지 포함 10미·생강 대추 추가형 |
| 경옥고의 복령량은 같은가? | `gyeongok-hongshi`·`gyeongok-donguibogam-ipmun`·`gyeongok-donguibogam-wisaeng`을 구분 | 복령 49량·48량과 위생방 별기 24량 및 전체 제조 비율 |
| 같은 이름의 처방은 무엇을 비교할까요? | 명시된 `km:sharesNameWith`의 두 대상을 선택한 뒤 각 수록형의 `km:containsHerb`를 개념 ID로 비교 | 공통·한쪽에만 등록된 본초와 각 진술의 원문 약명·약량·포제·제법. [수록형 비교 보기](../network/index.md#ontology-formula-variants) |
| 소건중탕의 두 수록형은 어떻게 다른가? | `xiaojianzhong-shanghan`·`xiaojianzhong-jinkui`를 따로 조회 | 감초 2량·대조 20매와 감초 3량·대조 12매, 교이의 용화 제법 |
| 상한론 100조의 처방과 구성은? | 주체 `shanghan-100`, 관계 `km:recordsFormula`인 진술을 고른 뒤 각 대상의 `km:containsHerb`를 조회 | 먼저 소건중탕, 불차 시 소시호탕이라는 조문의 순서·조건과 각 구성표. [조문→처방→본초](../network/index.md#ontology-classical-formulas) |
| 심포경의 전체 경혈은? | 관계 `km:belongsToMeridian`, 대상 `pericardium-meridian`인 모든 진술의 주체를 선택하고 `skos:notation`의 번호순으로 정렬 | PC1–PC9의 9혈과 각 진술의 출처·근거 발췌. [경맥별 전체 소속 경혈](../network/index.md#ontology-meridian-members) |
| 비경·임맥·독맥의 전체 경혈은? | 대상을 각각 `spleen-meridian`·`conception-vessel`·`governing-vessel`로 선택 | SP1–SP21의 21혈, CV1–CV24의 24혈, GV1–GV28의 28혈 |

각 결과는 `dcterms:source`·`skos:scopeNote`·`dcterms:description`의 출처·조건·근거 발췌와 함께 읽고, 해당 개념의 `foaf:page`로 본문에 돌아갑니다. 산조인탕은 금궤요략 5미형과 동의보감 몽문의 7미·생강 추가 구성을 각각 연결했습니다. 동의보감형의 적복령·계심도 별도의 개념과 출처를 확인할 수 있습니다. **수록되지 않은 관계는 아직 구조화하지 않은 정보**로 처리하고 실제 포함 여부는 해당 원문에서 확인합니다.

관계는 조건과 출처를 보존하는 RDF 재구체화 방식으로 제공하므로, 도구는 `rdf:Statement`의 주체·관계·대상·출처·조건과 근거 발췌를 함께 읽습니다. 근거 발췌가 인용한 절에서 사라지거나 숨김 주석·코드 예제에만 남으면 빌드를 중단하여 출처를 다시 확인하도록 합니다. 별칭의 일치, 공통 본초, 경맥 소속을 서로 같은 개념이나 동일한 치료효과라는 관계로 확장하지 않습니다. 약량·제형·연구 제제가 필요한 질문은 대표 본문과 실제 연구까지 확인합니다. [SKOS 표준](https://www.w3.org/TR/skos-reference/) · [RDF 관계 진술 표현](https://www.w3.org/TR/rdf11-mt/#reification)

## 문서 주소와 출처 {#_2}

- 문서의 대표 주소와 제목 링크로 내용을 공유할 수 있습니다.
- 질환 페이지는 환자 증상·감별·변증·치료·경과와 통합된 임상근거를 설명합니다.
- 통합 전 주소로 들어왔으면 최종 도착한 대표 문서의 제목·해당 절을 확인해 인용합니다.
- 고유한 근거 페이지와 근거 허브에서는 연구 요약·대상·치료 조건·원출처를 확인합니다.
- 고전·민성의담은 서명·편목·판본 또는 날짜가 확인되는 기록을, 하루 카드는 해당 날짜·카드의 공유 링크와 연결 출처를 함께 확인합니다.
- 참고문헌 DB는 PMID·DOI 추적의 기준 허브로 사용합니다.
- 전통적 활용과 현대 임상근거를 구분합니다.

### 문서 버전과 인용 정보 대조 {#version-and-citation}

페이지별 JSON에 `provenance`가 있으면 `document_id`로 같은 대표 주소의 문서를 식별하고, `text_sha256`·`source_sha256`로 본문과 소스의 버전을 대조합니다. `commit`은 해당 공개 자료를 만든 빌드의 기준 Git 커밋입니다. 이를 이용해 수집해 둔 자료와 현재 본문을 비교하며, 의학적 검토 시점과 검토자는 문서에 별도로 명시된 정보를 확인합니다.

온톨로지 파일의 SHA-256은 매니페스트의 `ontology.sha256`과 비교합니다. 문서 탐색 그래프는 같은 파일의 `content_sha256`을 사용합니다. 각 해시는 대상으로 지정된 파일에 적용하며, 페이지 본문 지문과 구별합니다. [문서·도표 출처 기록](../guide/content-use.md#provenance)

인용에는 문서 제목과 대표 HTML의 해당 절을 표시하고, 연구 결과를 설명할 때는 원논문의 PMID·DOI와 실제 대상·제제·비교군·기간을 함께 남깁니다. 예를 들어 사군자탕의 국방 구성을 설명할 때에는 [사군자탕의 출전 원문·약량 절](../formulas/sijunzi-tang.md#source-dose-original)을 출처로 연결합니다. 개념 ID와 JSON 주소는 도구의 검색·대조에 사용합니다.

<span id="robotstxt"></span>

### 검색·수집 도구가 찾는 공개 경로 {#crawler-discovery}

[robots.txt](../robots.txt)는 공개 경로의 수집 설정과 [sitemap.xml](https://wiki.minseong.co.kr/sitemap.xml) 주소를 제공합니다. [llms.txt](../llms.txt)는 주제별 대표 자료와 기계 판독용 파일의 역할을 안내하며, 본문 HTML의 JSON 대체 링크와 온톨로지 설명 링크를 통해 실제 자료로 이어집니다. 출처 표기와 자료 활용 범위는 [콘텐츠 이용 안내](../guide/content-use.md)에서 확인할 수 있습니다.

## 최종 구조 {#_3}

**사람에게는 탐색하기 쉬운 임상 지식망, 검색엔진에는 주제가 명확한 내부링크 구조, AI에는 증상·질환·치료·근거 관계가 명시적인 아카이브**를 목표로 합니다.

