/* Enhance existing HTML links; no remote requests or duplicate point database. */
(function () {
  'use strict';
  function normalize(value) {
    return String(value || '').normalize('NFKC').toLocaleLowerCase('ko').replace(/[\s-]+/g, '');
  }
  function matches(label, code, selected, query) {
    return (!selected || code === selected) && normalize(label).includes(normalize(query));
  }
  function loadRegion(region) {
    if (!region.open) return;
    region.querySelectorAll('object[data-src]').forEach(object => {
      object.setAttribute('data', object.dataset.src);
      object.removeAttribute('data-src');
    });
  }
  function initRegions(doc) {
    doc.querySelectorAll('.acupoint-region').forEach(region => {
      if (!region.dataset.ready) {
        region.addEventListener('toggle', () => loadRegion(region));
        region.dataset.ready = 'true';
      }
      loadRegion(region);
    });
    revealRegion(doc);
  }
  function revealRegion(doc) {
    const hash = doc.defaultView && doc.defaultView.location.hash;
    if (!hash || !/^#visual-[a-z0-9-]+$/.test(hash)) return;
    const anchor = doc.getElementById(hash.slice(1));
    // Markdown wraps a standalone span anchor in a paragraph.
    const container = anchor && anchor.parentElement && anchor.parentElement.tagName === 'P' ? anchor.parentElement : anchor;
    const region = container && container.nextElementSibling;
    if (region && region.matches('details.acupoint-region')) {
      region.open = true;
      loadRegion(region);
    }
  }
  function init(doc) {
    const controls = doc.getElementById('acupoint-controls');
    if (!controls || controls.dataset.ready) return;
    const query = doc.getElementById('acupoint-query');
    const select = doc.getElementById('acupoint-meridian');
    const reset = doc.getElementById('acupoint-reset');
    const count = doc.getElementById('acupoint-count');
    const empty = doc.getElementById('acupoint-empty');
    if (!query || !select || !reset || !count || !empty) return;
    const groups = Array.from(doc.querySelectorAll('.acupoint-group')).map(group => ({
      element: group, code: group.dataset.meridian,
      links: Array.from(group.querySelectorAll('.acupoint-links a')).map(link => ({
        element: link, label: link.textContent
      }))
    }));
    if (!groups.length) return;
    groups.forEach(group => {
      const option = doc.createElement('option');
      option.value = group.code;
      option.textContent = group.element.dataset.label + ' ' + group.code;
      select.appendChild(option);
    });
    const total = groups.reduce((sum, group) => sum + group.links.length, 0);
    function update() {
      let visible = 0;
      groups.forEach(group => {
        let groupCount = 0;
        group.links.forEach(link => {
          const show = matches(link.label, group.code, select.value, query.value);
          link.element.hidden = !show;
          if (show) groupCount++;
        });
        group.element.hidden = groupCount === 0;
        visible += groupCount;
      });
      count.textContent = visible + ' / ' + total + '경혈';
      empty.hidden = visible !== 0;
    }
    query.addEventListener('input', update);
    select.addEventListener('change', update);
    reset.addEventListener('click', () => {
      query.value = ''; select.value = ''; update(); query.focus();
    });
    controls.dataset.ready = 'true'; controls.hidden = false; update();
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {normalize, matches, init, initRegions, revealRegion};
  if (typeof document !== 'undefined') {
    const setup = () => { init(document); initRegions(document); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, {once: true});
    else setup();
    window.addEventListener('hashchange', () => revealRegion(document));
    if (typeof document$ !== 'undefined') document$.subscribe(setup);
  }
}());
