/* Progressive enhancement: the complete selected text remains readable without JS. */
(() => {
  'use strict';
  const normalize = text => text.normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim();
  function revealAnchor() {
    const root = document.getElementById('dsb-reader');
    if (!root) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const passage = target.closest('.dsb-passage');
    if (passage && passage.hidden) root.querySelector('#dsb-reset')?.click();
    const scan = target.closest('.dsb-scan');
    if (scan) scan.open = true;
  }
  function install() {
    const root = document.getElementById('dsb-reader');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = 'true';
    const query = root.querySelector('#dsb-query');
    const category = root.querySelector('#dsb-category');
    const count = root.querySelector('#dsb-count');
    const rows = [...root.querySelectorAll('.dsb-passage')].map(node => ({node, text: normalize(node.textContent)}));
    function filter() {
      const words = normalize(query.value).split(' ').filter(Boolean);
      let found = 0;
      for (const {node, text} of rows) {
        node.hidden = Boolean(category.value && node.dataset.category !== category.value) || !words.every(word => text.includes(word));
        if (!node.hidden) found++;
      }
      count.textContent = found ? `${rows.length}개 대목 중 ${found}개 표시` : '일치하는 대목이 없습니다. 검색어를 줄이거나 전체 보기를 누르세요.';
    }
    query.addEventListener('input', filter);
    category.addEventListener('change', filter);
    root.querySelector('#dsb-reset').addEventListener('click', () => { query.value = ''; category.value = ''; filter(); });
    root.querySelector('.dsb-controls').hidden = false;
    filter();
    revealAnchor();
    document.querySelectorAll('.dsb-scan img').forEach(img => {
      img.addEventListener('error', () => {
        if (img.parentNode.querySelector('.dsb-image-error')) return;
        const message = document.createElement('p');
        message.className = 'dsb-image-error';
        message.textContent = '책 이미지를 불러오지 못했습니다. 위의 원문·풀이는 계속 읽을 수 있으며, 이미지 링크나 출처의 PDF에서 대조할 수 있습니다.';
        img.after(message);
      });
    });
  }
  window.addEventListener('hashchange', revealAnchor);
  install();
  if (typeof document$ !== 'undefined') document$.subscribe(install);
})();
