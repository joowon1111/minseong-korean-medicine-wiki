---
title: 통합 한의학 지식 그래프
description: 본초·방제·증상에서 고전·역사·임상근거로 이어지는 탐색 경로와 실제 연결 예시를 안내합니다.
tags: [한의학지식망, 지식그래프, AEO, GEO]
status: 검토완료
last_reviewed: 2026-08-19
---
# 통합 한의학 지식 그래프 {#_1}

**알고 있는 약재·처방·증상에서 출발해, 구성과 변증을 확인하고 고전·임상근거까지 이어 읽는 지도**입니다. 같은 약재가 여러 처방에 쓰이고, 같은 증상에서도 살펴볼 처방과 치료가 달라집니다. 아래 연결은 처방을 자동으로 선택하는 순서가 아니라 각 문서의 관계를 이해하기 위한 탐색 경로입니다.

| 지금 궁금한 것 | 시작할 지도 | 이어서 확인할 내용 |
|---|---|---|
| 이 약재는 어떤 처방에 들어가나요? | [본초→방제 역탐색](herb-to-formula-map.md) | 함께 배합되는 약재와 처방별 역할 |
| 이 처방은 어떤 상황에서 검토하나요? | [방제→질환·변증 지도](formula-to-condition-map.md) | 변증의 단서·비슷한 처방의 차이·관련 증상 |
| 내 증상은 어디서부터 읽어야 하나요? | [질환·증상→치료 임상 지도](condition-to-treatment-map.md) | 원인 감별·치료 선택·경과 관찰 |
| 고전의 설명과 연구 결과는 어떻게 연결되나요? | [고전→현대 연구 연결](classic-to-evidence-map.md) | 원문의 병증과 연구 대상·처방 구성의 차이 |

## 본초에서 시작하기 {#_2}

약재의 이름을 알고 있다면 **그 약재가 들어 있다는 사실과 처방 전체의 방향을 나누어** 봅니다. 인삼이 공통으로 들어가더라도 모든 처방이 같은 피로를 다루는 것은 아닙니다.

| 출발 본초 | 함께 읽을 방제 | 배합에서 비교할 점 |
|---|---|---|
| [인삼](../herbs/ginseng.md) | [사군자탕](../formulas/sijunzi-tang.md)·[육군자탕](../formulas/liujunzi-tang.md) | 보기·건비의 기본 골격에 반하·진피가 더해질 때의 차이 |
| [황기](../herbs/astragalus.md) | [보중익기탕](../formulas/buzhong-yiqi-tang.md)·[십전대보탕](../formulas/shi-quan-da-bu-tang.md) | 보기승양과 기혈쌍보·온보의 차이 |
| [녹용](../herbs/cervi-parvum-cornu.md) | [공진단](../formulas/gongjin-dan.md)·[소아 녹용보약의 귀룡탕 설명](../conditions/child-parent-tonic-guide.md#guiryong-tang) | 공진단의 기본 구성과 개별 상태에 따라 조정하는 탕약의 차이 |

더 많은 약재는 [본초→방제 역탐색](herb-to-formula-map.md), 처방 전체의 재료는 [처방 구성 네트워크](formula-composition-hub.md)에서 확인합니다.

## 방제에서 시작하기 {#_3}

처방명을 알고 있다면 **구성 → 중심 변증 → 비슷한 처방과의 갈림점 → 근거와 안전성**을 순서대로 살펴보면 이해하기 쉽습니다.

예를 들어 [보중익기탕](../formulas/buzhong-yiqi-tang.md)을 읽을 때는 [기허](../diagnostics/qi-deficiency.md)의 뜻을 먼저 확인하고, 식사량·피로·땀·회복 양상을 함께 봅니다. 혈허와 냉감의 비중이 궁금하면 [보중익기탕과 십전대보탕 비교](../compare/buzhong-vs-sipjeondaebo.md)로, 생활 속 상담 질문이 필요하면 [피로·기력회복 보약](../conditions/energy-recovery.md)으로 이어갈 수 있습니다.

불면과 소화불편이 함께 있을 때는 [귀비탕과 온담탕 비교](../compare/guibi-vs-wendan.md)가 다른 출발점이 됩니다. 같은 불면이라는 이름 아래에서도 기혈부족과 담음의 단서가 어떻게 다른지 비교합니다. 다른 처방군은 [방제→질환·변증 지도](formula-to-condition-map.md)에 모았습니다.

## 증상에서 시작하기 {#_4}

증상으로 들어올 때는 특정 처방이나 경혈을 먼저 고르기보다 **발생 양상과 동반 증상, 먼저 진료받아야 할 신호**를 확인합니다.

| 출발 증상 | 먼저 읽을 문서 | 다음 탐색 |
|---|---|---|
| 허리 통증과 다리 저림 | [요통](../conditions/low-back-pain.md)·[좌골신경통](../conditions/sciatica.md) | [요통 임상 지식망](low-back-pain-map.md)에서 감별·처방·침구 연결 |
| 잠을 못 자고 두근거림 | [불면](../conditions/insomnia.md)·[심계](../conditions/palpitation.md) | [불면 임상 지식망](insomnia-map.md)에서 수면·소화·정서의 관계 |
| 더부룩하고 식욕이 없음 | [소화불량](../conditions/dyspepsia.md)·[식욕저하](../conditions/poor-appetite-adult.md) | [소화불량 임상 지식망](dyspepsia-map.md)에서 허실·담음·식적 비교 |
| 쉬어도 피곤하고 회복이 더딤 | [피로](../conditions/fatigue.md)·[회복 보약](../conditions/energy-recovery.md) | [피로·회복 지식망](recovery-map.md)에서 수면·영양·보익 처방 연결 |

각 증상에서 한약과 침구를 어떤 기준으로 함께 검토하는지는 [질환·증상→치료 임상 지도](condition-to-treatment-map.md)에서 이어서 봅니다.

## 고전에서 시작하기 {#_5}

고전의 병증명은 오늘날의 질환명과 범위가 다를 수 있습니다. 원문의 증상 조합과 치법을 먼저 읽은 뒤 현대 문서와 비교합니다.

| 고전 | 연결할 주제 | 읽을 때의 질문 |
|---|---|---|
| [상한론](../classics/shanghanlun.md) | [계지탕](../formulas/guizhi-tang.md)·[마황탕](../formulas/mahuang-tang.md)·[소청룡탕](../formulas/xiaoqinglong-tang.md) | 땀·오한·수음 등 원문의 단서는 어떻게 다른가? |
| [금궤요략](../classics/jinkui-yaolue.md) | [처방군 지도](formula-family-map.md) | 잡병의 증상 조합과 허실·수기를 어떻게 구분하는가? |
| [동의보감](../classics/donguibogam.md) | [공진단 원전](../classics/donguibogam/gongjin-dan.md)·[경옥고 원전](../classics/donguibogam/gyeongok-go.md) | 허로·양생의 맥락과 현재 상담 목표는 어떻게 다른가? |

원전과 사람 대상 연구를 비교하는 읽기 순서는 [고전→현대 연구 연결](classic-to-evidence-map.md)을 참고합니다.

## 역사 축 {#_6}

[한의학 역사 타임라인](../history/index.md#timeline)으로 시대를 먼저 살핀 다음 [의가·고전·처방 계보](physician-classic-formula-lineage.md)에서 인물과 저술의 관계를 확인할 수 있습니다. 처방의 배합 변화가 궁금하면 [보기·기혈쌍보 처방 계보](tonic-formula-lineage.md)로 좁혀 읽습니다.

역사적으로 오래 사용되었다는 설명은 처방의 배경을 이해하는 자료입니다. 현재 어떤 환자에게 어느 정도 도움이 되는지는 별도의 임상근거에서 확인합니다.

## 현대 연구 축 {#_7}

[연구·근거 안내](../portal/evidence.md)에서 주제를 고르고 [참고문헌 데이터베이스](../research/references/index.md)로 원문을 찾아갈 수 있습니다. 처방 문서의 연구를 읽을 때는 다음 네 가지를 함께 확인합니다.

| 확인할 항목 | 놓치기 쉬운 차이 |
|---|---|
| 대상 | 건강인·특정 질환자·동물·세포 연구는 답할 수 있는 질문이 다름 |
| 중재 | 같은 처방명이어도 원방·가감방·추출제·복용량이 다를 수 있음 |
| 결과 | 검사 수치 변화와 실제 증상·일상 기능의 변화는 구분해야 함 |
| 한계 | 비교군·기간·규모·이상반응 보고를 함께 읽어야 함 |

연구를 읽고 돌아올 때는 해당 [방제](formula-to-condition-map.md)나 [증상](condition-to-treatment-map.md) 문서에서 자신의 상황과 연구 대상의 공통점·차이점을 다시 살펴보면 됩니다.
