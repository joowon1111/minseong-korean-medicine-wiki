/* Original archive discovery UI. Uses existing local records and original SVGs. */
(function () {
  'use strict';
  const kinds = {standard: '표준경혈', saam: '사암침법', tung: '동씨기혈'};
  function normalize(value) {
    return String(value || '').normalize('NFKC').toLocaleLowerCase('ko').replace(/[\s·ㆍ,－-]+/g, '');
  }
  function tokens(query) {
    // Keep international codes together even when entered as "LI 4".
    return String(query || '').normalize('NFKC').replace(/\b([a-z]{2})[\s-]+(\d+)/gi, '$1$2')
      .split(/\s+/).map(normalize).filter(Boolean);
  }
  function matches(entry, state) {
    return (!state.kind || entry.kind === state.kind) &&
      (!state.meridian || entry.meridian === state.meridian) &&
      (!state.region || entry.region === state.region) &&
      tokens(state.query).every(token => normalize(entry.search).includes(token));
  }
  function rank(entry, query) {
    const q = normalize(query);
    if (!q) return 0;
    if ([entry.name, entry.code, entry.han].some(value => normalize(value) === q)) return 3;
    if (normalize(entry.name).startsWith(q) || (entry.code && normalize(entry.code).startsWith(q))) return 2;
    return 1;
  }
  function safeURL(value) {
    return typeof value === 'string' && (/^\/(?!\/)[^\\\s]*$/.test(value) || /^https:\/\/[^\s]+$/.test(value)) ? value : '';
  }
  function init(doc) {
    const root = doc.getElementById('acupoint-discovery');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = 'true';
    const query = root.querySelector('[data-query]');
    const meridian = root.querySelector('[data-meridian-filter]');
    const region = root.querySelector('[data-region-filter]');
    const result = root.querySelector('[data-results]');
    const panel = root.querySelector('[data-detail]');
    const status = root.querySelector('[data-status]');
    const more = root.querySelector('[data-more]');
    const reset = root.querySelector('[data-reset]');
    let entries = [], kind = '', selected = '', limit = 24, visible = [];
    let lastQuery = '';
    const el = (tag, text, parent, cls) => {
      const node = doc.createElement(tag);
      if (text !== undefined) node.textContent = text;
      if (cls) node.className = cls;
      if (parent) parent.appendChild(node);
      return node;
    };
    function link(label, href, parent) {
      const node = el('a', label, parent);
      const safe = safeURL(href);
      if (safe) node.href = safe;
      return node;
    }
    function syncURL() {
      const win = doc.defaultView;
      if (!win || !win.history) return;
      const url = new URL(win.location.href);
      for (const [key, value] of Object.entries({point: selected, type: kind, q: query.value,
        meridian: meridian.value, region: region.value})) {
        if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
      }
      url.hash = 'clinical-explorer';
      win.history.replaceState(null, '', url);
    }
    function navigate(entry) {
      // A diagram or prescription may lead beyond the current search scope.
      query.value = entry.code || entry.name; setKind(entry.kind); selected = entry.id;
      choose(entry); update();
      const heading = panel.querySelector('h3');
      heading.tabIndex = -1; heading.focus({preventScroll: true});
      panel.scrollIntoView({block: 'start', behavior: 'smooth'});
    }
    function recordLink(label, entry, parent) {
      const node = link(label, entry.href, parent);
      node.addEventListener('click', event => {
        if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault(); navigate(entry);
      });
      return node;
    }
    function section(title, text) {
      if (!text) return;
      el('h4', title, panel); el('p', text, panel);
    }
    function choose(entry) {
      selected = entry.id;
      panel.replaceChildren();
      panel.hidden = false;
      el('p', kinds[entry.kind] + ' · ' + entry.region, panel, 'discovery-eyebrow');
      el('h3', entry.name + (entry.han ? ' ' + entry.han : '') + (entry.code ? ' · ' + entry.code : ''), panel);
      const actions = el('div', undefined, panel, 'discovery-actions');
      link('상세 문서', entry.href, actions);
      if (entry.route) link(entry.meridian_name + ' 유주', entry.route, actions);
      if (entry.standard_reference) link('표준경혈 DB', entry.standard_reference, actions);
      const share = el('button', '선택·검색 링크 복사', actions); share.type = 'button';
      const shareStatus = el('p', '', panel, 'discovery-source');
      shareStatus.setAttribute('role', 'status');
      share.addEventListener('click', async () => {
        syncURL();
        const url = doc.defaultView.location.href;
        try {
          await doc.defaultView.navigator.clipboard.writeText(url);
          shareStatus.textContent = '현재 선택과 검색 조건의 링크를 복사했습니다.';
        } catch (_) {
          shareStatus.replaceChildren();
          el('span', '아래 주소를 선택해 복사해 주세요. ', shareStatus);
          const field = el('input', undefined, shareStatus);
          field.type = 'text'; field.readOnly = true; field.value = url;
          field.setAttribute('aria-label', '선택과 검색 조건 공유 주소');
          field.focus(); field.select();
        }
      });
      if (entry.points) {
        const group = el('div', undefined, panel, 'discovery-points');
        for (const role of ['보', '사']) {
          const row = el('p', undefined, group);
          el('strong', role + '혈: ', row);
          entry.points.filter(p => p.role === role).forEach((p, i) => {
            if (i) row.appendChild(doc.createTextNode(' · '));
            const point = entries.find(e => e.id === p.code && e.kind === 'standard');
            if (point) recordLink(p.name + ' ' + p.code, point, row);
            else link(p.name + ' ' + p.code, p.href, row);
          });
        }
      }
      section('위치·구성', entry.location);
      if (entry.diagrams.length) {
        const views = el('div', undefined, panel, 'discovery-views');
        const figure = el('figure', undefined, panel, 'discovery-figure');
        const controls = el('div', undefined, figure, 'discovery-zoom');
        const viewport = el('div', undefined, figure, 'discovery-viewport');
        viewport.tabIndex = 0;
        viewport.setAttribute('aria-label', '경혈 도해 · 확대 후 가로·세로로 스크롤할 수 있습니다');
        const object = el('object', undefined, viewport);
        let zoom = 1;
        const zoomStatus = el('span', '100%', controls);
        zoomStatus.setAttribute('aria-live', 'polite');
        function resize() {
          const old = object.clientWidth || viewport.clientWidth;
          const centerX = (viewport.scrollLeft + viewport.clientWidth / 2) / old;
          const centerY = (viewport.scrollTop + viewport.clientHeight / 2) / (object.clientHeight || viewport.clientHeight);
          object.style.width = (zoom * 100) + '%';
          object.style.height = (viewport.clientHeight * zoom) + 'px';
          viewport.scrollLeft = centerX * object.clientWidth - viewport.clientWidth / 2;
          viewport.scrollTop = centerY * object.clientHeight - viewport.clientHeight / 2;
          zoomStatus.textContent = Math.round(zoom * 100) + '%';
          minus.disabled = zoom <= 1; plus.disabled = zoom >= 3;
        }
        function control(label, action) {
          const button = el('button', label, controls); button.type = 'button';
          button.addEventListener('click', action); return button;
        }
        const minus = control('축소', () => {zoom = Math.max(1, zoom - .5); resize();});
        const plus = control('확대', () => {zoom = Math.min(3, zoom + .5); resize();});
        control('원래 크기', () => {zoom = 1; resize();});
        const fullscreen = control('크게 보기', async () => {
          try {
            if (doc.fullscreenElement === figure) await doc.exitFullscreen();
            else if (figure.requestFullscreen) await figure.requestFullscreen();
            else figure.classList.toggle('discovery-expanded');
          } catch (_) {figure.classList.toggle('discovery-expanded');}
          fullscreen.textContent = doc.fullscreenElement === figure || figure.classList.contains('discovery-expanded') ? '크게 보기 닫기' : '크게 보기';
          resize();
        });
        figure.addEventListener('fullscreenchange', () => {
          fullscreen.textContent = doc.fullscreenElement === figure ? '크게 보기 닫기' : '크게 보기'; resize();
        });
        const wired = new WeakSet();
        object.addEventListener('load', () => {
          const svg = object.contentDocument;
          if (!svg || wired.has(svg)) return;
          wired.add(svg);
          svg.querySelectorAll('a[href]').forEach(anchor => {
            const href = anchor.getAttribute('href');
            const target = entries.find(e => e.href === href);
            if (!target) return;
            anchor.addEventListener('click', event => {
              if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
              event.preventDefault(); navigate(target);
            });
          });
        });
        object.type = 'image/svg+xml';
        const fallback = link('도해를 새 화면에서 보기', entry.diagrams[0].src, object);
        const caption = el('figcaption', undefined, figure);
        function show(src, title, button) {
          zoom = 1; resize();
          object.data = safeURL(src);
          object.setAttribute('aria-label', title);
          fallback.href = safeURL(src);
          caption.textContent = title;
          views.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
        }
        function view(label, src, title) {
          const button = el('button', label, views); button.type = 'button';
          button.setAttribute('aria-pressed', 'false');
          button.addEventListener('click', () => show(src, title, button));
          return button;
        }
        const buttons = entry.diagrams.map(d => view(d.name ? d.role + ' · ' + d.name : '경혈 위치', d.src, d.title));
        if (entry.route_diagram) view('경맥 전체', entry.route_diagram, entry.meridian_name + ' 체표 유주');
        const muscle = muscleView(entry.region);
        if (muscle) {
          view('부위 근육', '/assets/mps-atlas/' + muscle + '.svg', '해당 부위의 근육 개요 · 경혈과 근육을 일대일 대응한 그림이 아닙니다.');
          link('근육·움직임 해설', '/clinical-anatomy/mps-' + muscle + '/', actions);
        }
        show(entry.diagrams[0].src, entry.diagrams[0].title, buttons[0]);
      }
      section('해부학·주변 구조', entry.anatomy);
      if (entry.kind === 'standard') {
        const anatomyLinks = el('div', undefined, panel, 'discovery-actions');
        link('말초신경·근육 지도', '/clinical-anatomy/', anatomyLinks);
        link('경혈·근육·신경 초음파 지도', '/musculoskeletal-ultrasound/acupoint-ultrasound-map/', anatomyLinks);
        if (entry.roles && entry.roles.length) {
          el('h4', '사암침법에서의 역할', panel);
          const roles = el('p', undefined, panel);
          entry.roles.forEach((r, i) => {
            if (i) roles.appendChild(doc.createTextNode(' · '));
            const prescription = entries.find(e => e.kind === 'saam' && e.name === r.label.replace(/ [보사]혈$/, ''));
            if (prescription) recordLink(r.label, prescription, roles);
            else link(r.label, '/acupuncture-specific/saam-12-meridians/#' + r.meridian, roles);
          });
        }
      }
      for (const row of entry.rows) {
        el('h4', row.layer + ' · ' + row.label, panel); el('p', row.text, panel);
        if (row.source) {
          const source = el('p', undefined, panel, 'discovery-source');
          link('출처', row.source, source);
          if (row.locator) source.appendChild(doc.createTextNode(' · ' + row.locator));
        }
      }
      section('평가·함께 읽기', entry.assessment);
      section('그림의 범위', entry.note);
      const note = el('p', '위치 그림은 교육용 상대 위치입니다. 자침 깊이·방향을 표시하지 않습니다. 주치·전승과 비교 임상시험 결과는 상세 문서에서 구분해 읽습니다.', panel, 'discovery-source');
      link('자료와 이용조건', '/portal/acupuncture/#sources', note);
      if (entry.kind === 'standard') {
        const attribution = el('p', '위치: KM-Agent, Won-Yung Lee 외 5인, 2026. 기존 위치 자료를 탐색용으로 재구성. ', panel, 'discovery-source');
        link('원자료', 'https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv', attribution);
        attribution.appendChild(doc.createTextNode(' · '));
        link('CC BY 4.0', 'https://github.com/wonyung-lee/km-agent/blob/main/LICENSE', attribution);
      }
      result.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.entry === entry.id)));
      syncURL();
    }
    function options(select, values, empty) {
      select.replaceChildren();
      const all = el('option', empty, select); all.value = '';
      values.forEach(([value, label]) => {const option = el('option', label, select); option.value = value;});
    }
    function fillFilters() {
      const subset = entries.filter(e => !kind || e.kind === kind);
      const codes = new Map(subset.filter(e => e.meridian).map(e => [e.meridian, e.meridian_name]));
      options(meridian, [...codes].map(([c, n]) => [c, n + ' ' + c]), '전체 경락');
      meridian.disabled = !codes.size;
      options(region, [...new Set(subset.map(e => e.region))].map(r => [r, r]), '전체 부위');
    }
    function update() {
      const state = {kind, meridian: meridian.value, region: region.value, query: query.value};
      visible = entries.filter(e => matches(e, state)).sort((a, b) => rank(b, state.query) - rank(a, state.query));
      result.replaceChildren();
      visible.slice(0, limit).forEach(entry => {
        const button = el('button', undefined, result, 'discovery-result'); button.type = 'button';
        button.dataset.entry = entry.id; button.setAttribute('aria-pressed', String(selected === entry.id));
        el('strong', entry.name + (entry.code ? ' ' + entry.code : ''), button);
        el('span', kinds[entry.kind] + ' · ' + entry.region, button);
        button.addEventListener('click', () => { choose(entry); if (doc.defaultView && doc.defaultView.innerWidth < 850) panel.scrollIntoView({block:'start', behavior:'smooth'}); });
      });
      status.textContent = visible.length + '개 항목 · ' + Math.min(limit, visible.length) + '개 표시';
      more.hidden = visible.length <= limit;
      if (!visible.length) {
        selected = '';
        el('p', '일치하는 항목이 없습니다. 검색어를 줄이거나 전체 보기를 눌러 주세요.', result);
        panel.hidden = true;
      } else if (!visible.some(e => e.id === selected)) {
        choose(visible[0]);
      } else panel.hidden = false;
      syncURL();
    }
    function setKind(value) {
      kind = value; limit = 24; fillFilters();
      root.querySelectorAll('[data-kind]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.kind === kind)));
    }
    query.addEventListener('input', () => {lastQuery = query.value; limit = 24; update();});
    meridian.addEventListener('change', () => {limit = 24; update();});
    region.addEventListener('change', () => {limit = 24; update();});
    more.addEventListener('click', () => {limit += 24; update();});
    reset.addEventListener('click', () => {query.value = ''; selected = ''; setKind(''); update(); query.focus();});
    root.querySelectorAll('[data-kind]').forEach(button => button.addEventListener('click', () => {setKind(button.dataset.kind); update();}));
    root.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => {setKind(''); query.value = button.dataset.example; selected = ''; update();}));
    const win = doc.defaultView;
    const request = win && win.fetch ? win.fetch.bind(win) : null;
    if (!request) {status.textContent = '아래 경락별 목록과 부위별 도해에서 찾을 수 있습니다.'; return;}
    request('/assets/acupoint-atlas/discovery.json').then(response => {
      if (!response.ok) throw new Error('Discovery data unavailable');
      return response.json();
    }).then(data => {
      if (!Array.isArray(data.entries) || !root.isConnected) return;
      entries = data.entries;
      const params = new URL(win.location.href).searchParams;
      setKind(Object.hasOwn(kinds, params.get('type')) ? params.get('type') : '');
      if (!lastQuery) query.value = (params.get('q') || '').slice(0, 100);
      for (const [select, name] of [[meridian, 'meridian'], [region, 'region']]) {
        const value = params.get(name);
        if ([...select.options].some(option => option.value === value)) select.value = value;
      }
      const target = entries.find(e => e.id === params.get('point'));
      if (target && matches(target, {kind, query: query.value, meridian: meridian.value, region: region.value})) {
        const sorted = entries.filter(e => matches(e, {kind, query: query.value, meridian: meridian.value, region: region.value}))
          .sort((a, b) => rank(b, query.value) - rank(a, query.value));
        limit = Math.max(24, Math.ceil((sorted.indexOf(target) + 1) / 24) * 24);
        choose(target);
      } else if (target) {query.value = ''; setKind(target.kind); choose(target);}
      update();
    }).catch(() => {status.textContent = '탐색 자료를 불러오지 못했습니다. 아래 경락별 목록·부위별 도해는 계속 사용할 수 있습니다.';});
  }
  function muscleView(region) {
    const map = {'손·손가락':'forearm','손목·아래팔':'forearm','팔꿈치·위팔':'forearm',
      '무릎·종아리':'calf','발·발목':'calf','목·어깨':'neck','등·허리·엉치':'lumbar',
      '넓적다리·엉덩이':'hip'};
    return map[region] || '';
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {normalize, tokens, matches, rank, safeURL, init};
  if (typeof document !== 'undefined') {
    const setup = () => init(document);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, {once:true}); else setup();
    if (typeof document$ !== 'undefined') document$.subscribe(setup);
  }
}());
