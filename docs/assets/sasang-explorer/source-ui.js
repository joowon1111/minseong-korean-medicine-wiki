'use strict';
function patternSource(row){return PATTERN_SOURCES[row[0]][row[1]]}
function sourceHref(passage){
 const doc=SOURCE_DOCUMENTS[passage.document];
 return 'https://journal.kci.go.kr/JSCIM/archive/articlePdf?artiId='+doc[1]+(passage.page?'#page='+passage.page:'');
}
function passageCard(id){
 const p=SOURCE_PASSAGES[id],doc=SOURCE_DOCUMENTS[p.document];
 return `<article class="passage"><p class="passage-location">《동의수세보원》 신축본 · ${esc(p.number)}<br>${esc(SOURCE_CHAPTERS[p.chapter])}</p><blockquote lang="zh-Hant" cite="${esc(sourceHref(p))}">${esc(p.text)}</blockquote><p class="passage-translation"><b>우리말 풀이</b>${esc(p.translation)}</p><p class="passage-context">${esc(p.context)}</p><a class="source-link" href="${esc(sourceHref(p))}" target="_blank" rel="noopener">원문 인용 확인 · ${esc(doc[0])}${p.page?' · PDF '+p.page+'쪽':''} ↗</a></article>`;
}
function renderSource(row){
 const s=patternSource(row);
 return `<section class="pattern-source" aria-labelledby="source-title"><div class="source-heading"><h3 id="source-title">병증의 근거를 원문으로</h3><span class="source-kind">${esc(s.kind)}</span></div><p class="pattern-route">${esc(s.route)}</p>${passageCard(s.passages[0])}<div class="source-meaning"><h4>이 병증에서는 이렇게 읽습니다</h4><p>${esc(s.meaning)}</p></div><details class="source-details"><summary>소증·처방 연결${s.passages.length>1?'과 관련 원문':''} 더 읽기</summary>${s.passages.slice(1).map(passageCard).join('')}<h4>평소와 달라진 점</h4><p>${esc(s.ordinary)}</p><h4>처방으로 이어 읽기</h4><p>${esc(s.formula)}</p><p class="source-method">원문은 해당 편의 일부를 발췌했습니다. 조문 번호는 연결한 2014–2015 지침의 인용 체계를 따르며, 우리말 풀이와 병증 해설은 구분해 작성했습니다. 후대·학습 연결 항목은 인용문에 그대로 있는 독립 병증명이 아닙니다.</p>${link('/sasang-clinical-detail/pattern-source-map/','원전·지침 분류 대조 ↗')}</details></section>`;
}
function renderComparisons(row){
 const s=patternSource(row);
 return `<section class="pattern-comparison" aria-labelledby="comparison-title"><h3 id="comparison-title">헷갈리기 쉬운 병증과 비교</h3><p class="intro">다음 단계로 진행한다는 뜻이 아닙니다. 같은 체질 안의 다른 병증과 비교해 보세요.</p><div class="comparison-buttons">${s.compare.map(axis=>`<button data-axis="${esc(axis)}">${esc(axis)} →</button>`).join('')}</div></section>`;
}
function sourceSearchText(row){
 const s=patternSource(row);
 return [row[1],row[2],row[3],...row[4],...row[5].flatMap(f=>[f[0],f[2]]),s.route,s.kind,...s.passages.flatMap(id=>{
  const p=SOURCE_PASSAGES[id];return [p.number,p.text,p.translation,SOURCE_CHAPTERS[p.chapter]];
 })].join(' ').normalize('NFKC').toLowerCase();
}
