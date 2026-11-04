/* Shared reading aids stay small while page-specific study tools load on demand. */
(() => {
  "use strict";
  function revealAnchor() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = id && document.getElementById(id);
    if (!target) return;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === "DETAILS") parent.open = true;
    }
  }

  function updateTable(wrap) {
    const overflowing = wrap.scrollWidth > wrap.clientWidth + 1;
    if (overflowing) {
      wrap.tabIndex = 0;
      wrap.setAttribute("role", "region");
      const caption = wrap.querySelector("caption");
      wrap.setAttribute("aria-label", caption?.textContent.trim() || "가로로 스크롤하는 표");
    } else {
      wrap.removeAttribute("tabindex");
      wrap.removeAttribute("role");
      wrap.removeAttribute("aria-label");
    }
  }

  // Insert only line breaks: links, emphasis, original text and event handlers stay intact.
  const protectedContent = 'table, pre, code, kbd, samp, sup, math, mjx-container, .katex, .arithmatex, nav, form, button, textarea, [role="status"], [contenteditable="true"], [data-sentence-breaks="off"]';
  const segmenter = typeof Intl.Segmenter === "function" ? new Intl.Segmenter("ko", {granularity: "sentence"}) : null;
  const hangul = /[가-힣]/;
  const proseSelector = 'p, li';
  function sentenceStarts(text) {
    if (!hangul.test(text)) return [];
    const starts = [];
    if (segmenter) {
      let previous = "";
      for (const part of segmenter.segment(text)) {
        if (part.index && hangul.test(previous) && /[.!?。！？][”’」』〉》"')\]]*\s*$/.test(previous)) starts.push(part.index);
        previous = part.segment;
      }
    } else {
      // Korean sentence endings only; decimals, URLs and Latin abbreviations stay together.
      const endings = /[가-힣][.!?。！？][”’」』〉》"')\]]*\s+(?=\S)/gu;
      for (const match of text.matchAll(endings)) starts.push(match.index + match[0].length);
    }
    return starts;
  }
  function formatParagraph(paragraph) {
    if (paragraph.closest(protectedContent) || paragraph.querySelector('input, select, textarea, button') || paragraph.matches(':lang(en)')) return;
    if (paragraph.tagName === 'LI' && paragraph.querySelector('p, ul, ol, table')) return;
    paragraph.querySelectorAll('br.ms-sentence-break').forEach(br => br.remove());
    const text = paragraph.textContent;
    const starts = sentenceStarts(text);
    if (!starts.length) return;
    const walker = document.createTreeWalker(paragraph, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    const nodes = [], manualBreaks = [];
    let offset = 0;
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeType === Node.TEXT_NODE) {
        nodes.push({node, start: offset, end: offset + node.length});
        offset += node.length;
      } else if (node.tagName === 'BR') manualBreaks.push(offset);
    }
    // Reverse order keeps the original text offsets valid while inserting breaks.
    for (const start of starts.reverse()) {
      if (manualBreaks.some(at => at <= start && !text.slice(at, start).trim())) continue;
      const entry = nodes.find(item => item.start <= start && item.end > start);
      if (!entry || entry.node.parentElement.closest(protectedContent)) continue;
      const range = document.createRange();
      range.setStart(entry.node, start - entry.start);
      range.collapse(true);
      const br = document.createElement('br');
      br.className = 'ms-sentence-break';
      range.insertNode(br);
    }
  }

  let observer, sentenceObserver, readingRoot;
  const pending = new Set();
  let scheduled = false;
  function flushParagraphs() {
    scheduled = false;
    sentenceObserver?.disconnect();
    pending.forEach(paragraph => { if (paragraph.isConnected) formatParagraph(paragraph); });
    pending.clear();
    if (readingRoot) sentenceObserver.observe(readingRoot, {subtree: true, childList: true, characterData: true});
  }
  function queueParagraphs(node) {
    const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    if (!element) return;
    const paragraph = element.closest(proseSelector);
    if (paragraph && readingRoot.contains(paragraph)) pending.add(paragraph);
    element.querySelectorAll(proseSelector).forEach(p => pending.add(p));
  }
  function init() {
    revealAnchor();
    observer?.disconnect();
    sentenceObserver?.disconnect();
    pending.clear();
    readingRoot = document.querySelector('.md-content__inner');
    if (readingRoot) {
      readingRoot.querySelectorAll(proseSelector).forEach(formatParagraph);
      sentenceObserver = new MutationObserver(records => {
        records.forEach(record => {
          queueParagraphs(record.target);
          record.addedNodes.forEach(queueParagraphs);
        });
        if (pending.size && !scheduled) { scheduled = true; queueMicrotask(flushParagraphs); }
      });
      sentenceObserver.observe(readingRoot, {subtree: true, childList: true, characterData: true});
    }
    const tables = document.querySelectorAll(".md-typeset__scrollwrap");
    if (typeof ResizeObserver !== "undefined") {
      observer = new ResizeObserver(entries => entries.forEach(entry => updateTable(entry.target)));
      tables.forEach(wrap => observer.observe(wrap));
    }
    tables.forEach(updateTable);
  }

  window.addEventListener("hashchange", revealAnchor);
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, {once: true});
  else init();
})();
