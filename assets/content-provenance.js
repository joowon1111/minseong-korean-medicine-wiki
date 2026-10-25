/* Source attribution on ordinary article copies. No telemetry or visitor identifiers. */
(function () {
  'use strict';
  if (window.__archiveProvenanceCopyInstalled) return;
  window.__archiveProvenanceCopyInstalled = true;
  const excluded = 'input,textarea,select,[contenteditable]:not([contenteditable="false"]),pre,code,.archive-provenance,.archive-citation';
  function element(node) { return node && (node.nodeType === 1 ? node : node.parentElement); }
  document.addEventListener('copy', function (event) {
    if (event.defaultPrevented || !event.clipboardData) return;
    const target = element(event.target);
    if (target && target.closest(excluded)) return;
    const selection = document.getSelection();
    if (!selection || selection.isCollapsed || selection.rangeCount !== 1) return;
    const range = selection.getRangeAt(0), start = element(range.startContainer), end = element(range.endContainer);
    if (!start || !end || start.closest(excluded) || end.closest(excluded)) return;
    const article = start.closest('article.md-content__inner');
    if (!article || !article.contains(end)) return;
    const provenance = article.querySelector('[data-archive-provenance]');
    const selected = selection.toString();
    if (!provenance || selected.trim().length < 80) return;
    const data = provenance.dataset;
    const english = article.lang === 'en';
    const source = (english ? 'Source: ' : '출처: ') + '민성 한의학 아카이브, 「' + data.provenanceTitle + '」';
    const version = data.provenanceId + ' · ' + (english ? 'version ' : '버전 ') + data.provenanceVersion;
    const note = source + '\n' + data.provenanceUrl + '\n' + version;
    const rich = document.createElement('div');
    rich.appendChild(range.cloneContents());
    rich.querySelectorAll('script,style,iframe,object,embed,input,textarea,button,.headerlink,.archive-provenance,.archive-citation').forEach(node => node.remove());
    rich.querySelectorAll('*').forEach(node => {
      for (const attr of Array.from(node.attributes)) {
        if (/^on/i.test(attr.name) || /^(id|style|class|data-.*)$/i.test(attr.name) ||
            (/^(href|src)$/i.test(attr.name) && /^\s*javascript:/i.test(attr.value))) node.removeAttribute(attr.name);
      }
    });
    const attribution = document.createElement('p');
    attribution.append(document.createTextNode(source), document.createElement('br'));
    const link = document.createElement('a'); link.href = data.provenanceUrl; link.textContent = data.provenanceUrl;
    attribution.append(link, document.createElement('br'), document.createTextNode(version));
    rich.appendChild(attribution);
    try {
      event.clipboardData.setData('text/plain', selected + '\n\n' + note);
      event.clipboardData.setData('text/html', rich.innerHTML);
      event.preventDefault();
    } catch (_) { /* Keep the browser's normal copy behavior when unsupported. */ }
  });
})();
