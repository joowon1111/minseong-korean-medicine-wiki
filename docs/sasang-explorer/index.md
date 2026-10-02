---
title: 사상체질·병증 처방 탐색기
description: 사상체질과 주요 병증을 선택해 병증 단계, 감별 포인트, 대표 처방과 민성 한의학 아카이브 관련 문서를 단계적으로 탐색하는 학습용 도구입니다.
tags: [사상의학, 사상체질, 병증, 처방, 학습도구]
status: 시험운영
last_reviewed: '2026-10-02'
---

# 사상체질·병증 처방 탐색기

<div class="sasang-explorer-notice" role="note">
<strong>학습·문서 탐색용 도구입니다.</strong>
이 탐색기는 사상체질이나 질병을 진단하거나 개인별 처방을 추천하지 않습니다.
이미 학습하려는 체질·병증을 선택하면 아카이브 안의 병증 단계, 감별 포인트, 대표 처방 문서로 이어주는 색인입니다.
실제 진료·처방은 병력, 진찰, 검사, 안전성, 전문가의 종합 판단이 필요합니다.
</div>

<div id="sasang-explorer" class="sasang-explorer">
  <div class="sasang-explorer__steps" aria-label="탐색 순서">
    <span class="is-active">1 체질</span><span>2 병증축</span><span>3 단계</span><span>4 문서</span>
  </div>
  <div class="sasang-explorer__controls">
    <label><span>1. 사상체질</span><select id="sx-constitution">
      <option value="">체질을 선택하세요</option>
      <option value="소양인">소양인</option><option value="태음인">태음인</option>
      <option value="소음인">소음인</option><option value="태양인">태양인</option>
    </select></label>
    <label><span>2. 주요 병증축</span><select id="sx-axis" disabled><option value="">먼저 체질을 선택하세요</option></select></label>
    <label><span>3. 병증 단계</span><select id="sx-stage" disabled><option value="">전체 단계</option></select></label>
    <button type="button" id="sx-reset" class="sasang-explorer__reset">초기화</button>
  </div>
  <div id="sx-summary" class="sasang-explorer__summary" aria-live="polite">체질을 선택하면 해당 체질의 주요 병증축부터 단계적으로 살펴볼 수 있습니다.</div>
  <div id="sx-results" class="sasang-explorer__results"></div>
</div>

<link rel="stylesheet" href="/assets/sasang-explorer.css">
<script src="/assets/sasang-explorer.js" defer></script>

## 탐색기를 읽는 순서

1. **체질**은 이 도구가 판정하지 않습니다. 공부하려는 체질을 직접 선택합니다.
2. **병증축**에서 표리·주요 병증 방향을 좁힙니다.
3. **병증 단계**를 선택하면 해당 단계에서 아카이브가 정리한 핵심 모습과 감별 포인트를 확인합니다.
4. **대표 처방**은 추천 결과가 아니라 그 병증 단계와 연결해 읽을 처방 문서입니다.
5. 처방 카드와 체질 통합 허브, 병증 감별 문서를 함께 열어 원문 맥락을 확인합니다.

→ [사상의학 통합 허브](../sasang-integrated/) · [사상체질 대표처방](../sasang-integrated/formulas.md) · [체질별 병증 감별](../sasang-pattern-differential/) · [처방 배합망](../sasang-formula-combination-network/)
