---
title: 동의보감 원문 열람·검색
description: 동의보감의 공개 원문 전사와 전권 영인본을 임상 문서 검색과 분리하여 읽고 찾습니다.
search:
  exclude: true
---
# 동의보감 원문 열람·검색

한문 원문은 아래 **원문 검색**에서 찾고, 책의 모습을 그대로 확인하려면 **전권 영인본**을 엽니다. 일반 아카이브 검색은 기존 질환·본초·방제·경혈 문서를 중심으로 유지합니다.

## 수록 범위와 읽는 방법 {#coverage}

| 자료 | 이 화면에서 할 수 있는 일 | 현재 범위 |
|---|---|---|
| 원문 전사 | 한글 약재명·한자명·원문 구절로 검색하고 본문 읽기 | 탕액편 3권의 전사와 내경편 권1 신형·정의 확보된 부분 |
| 전권 영인본 | 책과 페이지를 선택하여 원전 이미지 열람 | 국립중앙도서관 자료 `CNTS-00047980284`의 목판본 23권 25책 |
| 임상 해설 | 원문에서 기존 본초·방제 문서로 이동 | 연결이 확인된 본초·방제부터 안내 |

**전사 전체의 교감과 전권의 검색 가능한 텍스트화는 완료되지 않았습니다.** 위키문헌 전사에는 오자·누락이 있을 수 있어 정확한 글자·용량·포제는 출처의 영인 페이지와 대조합니다. 탕액편 전사에 대응하는 영인본과 전권 열람용 목판본은 별도 자료이며, 같은 판본으로 합쳐 표시하지 않습니다. 출처가 명시한 간행연도가 없는 전권 영인본에 1613년 초간본이라는 이름을 붙이지 않습니다.

원문은 역사적 의학 기록입니다. 고전의 `無毒`이나 용량·주치가 오늘의 안전성·효과·복용법을 보증하지는 않습니다. 실제 활용의 기원종·제형·금기·병용약은 [본초 문서](../../herbs/index.md)와 [한약 안전성](../../herbal-integrated/safety.md)을 함께 읽습니다.

## 원문 검색과 열람 {#reader}

<div id="dgb-reader">
<p id="dgb-status" role="status">원문 열람기를 준비합니다.</p>
<form id="dgb-search-form" role="search">
<label for="dgb-query">한글·한자 약재명 또는 원문 구절</label>
<input id="dgb-query" type="search" maxlength="200" placeholder="당귀 · 當歸 · 경옥고 · 黃連" autocomplete="off">
<label for="dgb-group">검색할 범위</label>
<select id="dgb-group"><option value="">수록 전사 전체</option><option value="tangaek-1">탕액편 권1</option><option value="tangaek-2">탕액편 권2</option><option value="tangaek-3">탕액편 권3</option><option value="naegyeong-fragments">내경편 권1 확보된 부분</option></select>
<button type="submit">원문 검색</button>
</form>
<div id="dgb-results" aria-live="polite"></div>
<article id="dgb-passage" hidden></article>
<h3 id="facsimile">전권 영인본</h3>
<p>이미지는 Wikimedia Commons에서 선택한 한 페이지씩 불러옵니다. 아카이브 안에서 읽을 수 있으며, 이미지 제공처의 연결 상태에 따라 열람이 제한될 수 있습니다. 전사 파일은 아카이브 자체에 수록되어 있습니다.</p>
<form id="dgb-scan-form">
<label for="dgb-volume">책</label><select id="dgb-volume"></select>
<label for="dgb-page">이미지 페이지</label><input id="dgb-page" type="number" min="1" value="1">
<button type="submit">영인본 열기</button>
</form>
<div id="dgb-scan" hidden>
<p id="dgb-scan-status" role="status"></p>
<div class="dgb-controls"><button id="dgb-prev" type="button">이전 페이지</button><button id="dgb-next" type="button">다음 페이지</button></div>
<a id="dgb-scan-image-link" target="_blank" rel="noopener"><img id="dgb-scan-image" alt="선택한 동의보감 원전 페이지" loading="lazy" decoding="async" referrerpolicy="no-referrer"></a>
<p><a id="dgb-scan-source" target="_blank" rel="noopener">영인본 출처·이용조건</a> · <a id="dgb-scan-pdf" target="_blank" rel="noopener">책 전체 PDF</a></p>
</div>
</div>

<noscript>원문 검색과 페이지 열람에는 JavaScript가 필요합니다. 아래 출처에서 공개 원문과 영인본을 직접 열람할 수 있습니다.</noscript>

## 출처·전사·이용조건 {#sources}

한의학고전DB의 본문·번역·교감 자료를 가져오지 않았습니다. 해당 DB는 [이용조건](https://info.mediclassics.kr/document/guide/license)에 따라 외부 참고 링크로만 안내합니다.

- **전사 출처:** [한국어 위키문헌 동의보감 탕액편](https://ko.wikisource.org/wiki/동의보감/탕액편), [중국어 위키문헌 내경편 권1](https://zh.wikisource.org/wiki/東醫寶鑒/內景篇一). 저자 허준, 전사·편집 기여자 위키문헌 사용자들. 각 검색 결과에서 사용한 수정판의 고정 링크와 기여 이력을 제공합니다.
- **전사 이용조건:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ko). 이 화면의 가져온 전사와 이를 정리한 전사 데이터는 동일한 이용조건을 따릅니다. 원문 내용에 현대 번역을 덧붙이지 않았으며, 위키 문법·배치를 텍스트 항목으로 정리하고 검색용 한글명과 아카이브 연결을 추가했습니다. 정본·완역본이라는 의미가 아닙니다.
- **전권 영인본:** [Wikimedia Commons 공개 파일과 서지](https://commons.wikimedia.org/wiki/File:CNTS-00047980284_1_東醫寶鑑.pdf). 국립중앙도서관 디지털 자료를 바탕으로 제공된 목판본 25책이며, 파일 설명의 `PD-scan / PD-South Korea` 표시를 확인했습니다. 이미지와 PDF는 제공처에서 불러옵니다.
- **자체 설명:** 아카이브의 해설과 임상 문서는 [콘텐츠 이용 안내](../../guide/content-use.md)를 따릅니다. 공개 전사·영인본의 이용조건과 자체 해설의 이용조건을 구분합니다.

→ [동의보감 개요](../donguibogam.md) · [동의보감 임상 탐색 네트워크](../../donguibogam-network/index.md) · [탕액편 임상 지도](../donguibogam-tangaek.md) · [사이트 검색 안내](../../search-guide.md)
