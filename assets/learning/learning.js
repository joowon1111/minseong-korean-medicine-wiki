/* Student learning room: lazy decks, local progress, instant navigation support. */
(function (global) {
  'use strict';
  const KEY = 'minseong-learning-v1';
  const VERSION = '20261002-9';
  const SUBJECTS = {anatomy: '기초 해부학', acupoints: '경혈학', acupuncture: '침구학', herbs: '본초학', formulas: '방제학', shanghanlun: '상한론', sasang: '사상의학'};
  const emptyProgress = () => ({known: [], again: [], saved: [], wrong: [], attempts: 0, correct: 0});
  function readProgress(storage) {
    try {
      const parsed = JSON.parse(storage.getItem(KEY) || '{}');
      const result = emptyProgress();
      for (const key of ['known', 'again', 'saved', 'wrong']) {
        if (Array.isArray(parsed[key])) result[key] = [...new Set(parsed[key].filter(x => typeof x === 'string'))];
      }
      for (const key of ['attempts', 'correct']) if (Number.isSafeInteger(parsed[key]) && parsed[key] >= 0) result[key] = parsed[key];
      result.correct = Math.min(result.correct, result.attempts);
      return result;
    } catch (_) { return emptyProgress(); }
  }
  function writeProgress(storage, progress) {
    try { storage.setItem(KEY, JSON.stringify(progress)); return true; } catch (_) { return false; }
  }
  function toggle(list, id, selected) {
    const set = new Set(list);
    if (selected) set.add(id); else set.delete(id);
    return [...set];
  }
  function markCard(progress, id, known) {
    progress.known = toggle(progress.known, id, known);
    progress.again = toggle(progress.again, id, !known);
    return progress;
  }
  function recordAnswer(progress, question, answer) {
    const correct = answer === question.answer;
    progress.attempts += 1;
    if (correct) progress.correct += 1;
    progress.wrong = toggle(progress.wrong, question.id, !correct);
    return correct;
  }
  function matches(card, category, query) {
    if (category && card.category !== category) return false;
    const haystack = [card.title, card.category, ...(card.aliases || []), ...card.facts.map(f => f.label + ' ' + f.value)].join(' ').toLowerCase();
    return query.toLowerCase().trim().split(/\s+/).every(word => haystack.includes(word));
  }
  function filteredCards(deck, progress, category, query, mode) {
    const words = query.toLowerCase().trim().split(/\s+/);
    const directCode = deck.cards.find(c => c.code && c.code.toLowerCase() === query.toLowerCase().trim());
    const cards = deck.cards.filter(c => (!directCode || c.id === directCode.id) && matches(c, category, query) &&
      (mode !== 'saved' || progress.saved.includes(c.id)) &&
      (mode !== 'review' || progress.again.includes(c.id)));
    const rank = c => words.every(w => c.title.toLowerCase().includes(w)) ? 0 : 1;
    return cards.sort((a, b) => rank(a) - rank(b));
  }
  function filteredQuestions(deck, progress, category, query, wrongOnly, kind = '', difficulty = '') {
    const ids = new Set(filteredCards(deck, progress, category, query, 'cards').map(c => c.id));
    return deck.questions.filter(q => ids.has(q.cardId) && (!wrongOnly || progress.wrong.includes(q.id)) && (!kind || q.kind === kind) && (!difficulty || (q.difficulty || 'basic') === difficulty));
  }
  function shuffle(items, random = Math.random) {
    const copy = items.slice();
    for (let i = copy.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [copy[i], copy[j]] = [copy[j], copy[i]]; }
    return copy;
  }
  function dailySeed(date) {
    return [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-');
  }
  function dailyQuestions(items, seed) {
    const hash = text => { let n = 2166136261; for (const ch of text) n = Math.imul(n ^ ch.charCodeAt(0), 16777619); return n >>> 0; };
    return items.slice().sort((a, b) => hash(seed + a.id) - hash(seed + b.id)).slice(0, 10);
  }
  function safeURL(value) {
    return typeof value === 'string' && /^\/(?!\/)[^\s<>]*$/.test(value) ? value : '#';
  }
  function answerMatches(question, value) {
    const normalize = text => String(text).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
    const entered = normalize(value);
    return !!entered && (question.acceptedAnswers || []).some(alias => normalize(alias) === entered);
  }
  const api = {answerMatches, KEY, emptyProgress, readProgress, writeProgress, markCard, recordAnswer, matches,
    filteredCards, filteredQuestions, shuffle, dailySeed, dailyQuestions, safeURL};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!global.document) return;

  const cache = new Map();
  let active = null;
  function deckFor(subject) {
    if (!cache.has(subject)) {
      const request = global.fetch('/assets/learning/' + subject + '.json?v=' + VERSION)
        .then(r => { if (!r.ok) throw new Error('자료를 가져오지 못했습니다.'); return r.json(); })
        .then(d => { if (d.schema !== 1 || d.subject !== subject || !Array.isArray(d.cards) || !Array.isArray(d.questions)) throw new Error('학습자료 형식을 확인할 수 없습니다.'); return d; });
      cache.set(subject, request);
      request.catch(() => { if (cache.get(subject) === request) cache.delete(subject); });
    }
    return cache.get(subject);
  }
  function node(tag, text, attrs) {
    const el = global.document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    for (const [key, value] of Object.entries(attrs || {})) el.setAttribute(key, value);
    return el;
  }
  function revealSource() {
    if (!global.location.hash) return;
    let target;
    try { target = global.document.getElementById(decodeURIComponent(global.location.hash.slice(1))); } catch (_) { return; }
    if (!target) return;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) if (parent.tagName === 'DETAILS') parent.open = true;
  }
  function init() {
    revealSource();
    const root = global.document.querySelector('[data-learning-room]');
    if (!root || root.dataset.ready) return;
    if (active) active.alive = false;
    const view = {alive: true, seq: 0};
    active = view; root.dataset.ready = 'true';
    let storage;
    try { storage = global.localStorage; } catch (_) { storage = null; }
    let progress = readProgress(storage);
    let subject = root.dataset.subject || new URLSearchParams(global.location.search).get('subject') || 'acupoints';
    if (!SUBJECTS[subject]) subject = 'acupoints';
    let deck = null, mode = 'cards', index = 0, flipped = false, session = null, questionKind = '', difficulty = '';
    const controls = node('div', undefined, {class: 'learning-controls'});
    const tabs = node('div', undefined, {class: 'learning-subjects', 'aria-label': '학습 과목'});
    for (const [id, title] of Object.entries(SUBJECTS)) {
      const button = node('button', title, {type: 'button', 'data-subject': id});
      button.addEventListener('click', () => { subject = id; category.value = ''; query.value = ''; load(); });
      tabs.append(button);
    }
    const filters = node('div', undefined, {class: 'learning-filters'});
    const query = node('input', undefined, {type: 'search', placeholder: '구조·혈명·본초·처방·조문·병증 검색', 'aria-label': '학습자료 검색'});
    const category = node('select', undefined, {'aria-label': '학습 단원'});
    const modeSelect = node('select', undefined, {'aria-label': '학습 방식'});
    for (const [value, title] of [['cards', '학습카드'], ['quiz', '퀴즈'], ['wrong', '오답 다시 풀기'], ['review', '다시 볼 카드'], ['saved', '북마크 카드']]) {
      modeSelect.append(node('option', title, {value}));
    }
    filters.append(query, category, modeSelect);
    const stats = node('p', '', {class: 'learning-stats', 'aria-live': 'polite'});
    const storageNote = node('p', '학습기록은 이 브라우저에 저장됩니다. 회원가입 없이 사용할 수 있습니다.', {class: 'learning-note'});
    const status = node('p', '', {role: 'status', class: 'learning-status'});
    const stage = node('div', undefined, {class: 'learning-stage'});
    const toolbar = node('div', undefined, {class: 'learning-toolbar'});
    const resetFilters = node('button', '검색·단원 초기화', {type: 'button'});
    resetFilters.addEventListener('click', () => { query.value = ''; category.value = ''; restart(); });
    const clear = node('button', '학습기록 초기화', {type: 'button', class: 'learning-clear'});
    clear.addEventListener('click', () => {
      if (!global.confirm('전체 과목의 이해한 카드·북마크·오답 기록을 이 브라우저에서 지울까요?')) return;
      progress = emptyProgress(); save(); restart();
    });
    toolbar.append(resetFilters, clear);
    controls.append(tabs, filters, stats);
    root.replaceChildren(controls, status, stage, toolbar, storageNote);
    function save() {
      if (!writeProgress(storage, progress)) storageNote.textContent = '현재 브라우저에서 기록을 저장할 수 없습니다. 이번 화면에서는 학습을 계속할 수 있습니다.';
      updateStats();
    }
    function updateStats() {
      if (!deck) return;
      const cards = new Set(deck.cards.map(c => c.id)), qs = new Set(deck.questions.map(q => q.id));
      stats.textContent = SUBJECTS[subject] + ' · 카드 ' + deck.cards.length + '개 · 문제 ' + deck.questions.length + '개 · 이해한 카드 ' + progress.known.filter(x => cards.has(x)).length + '개 · 오답 ' + progress.wrong.filter(x => qs.has(x)).length + '개';
    }
    function button(text, action, attrs) {
      const el = node('button', text, Object.assign({type: 'button'}, attrs));
      el.addEventListener('click', action); return el;
    }
    function focusHeading() { const h = stage.querySelector('h3'); if (h) h.focus({preventScroll: true}); }
    function picture(source, description) {
      const object = node('object', undefined, {data: safeURL(source), type: 'image/svg+xml', class: 'learning-diagram', 'aria-label': description});
      object.append(node('a', '도해를 새 화면에서 보기', {href: safeURL(source), target: '_blank', rel: 'noopener'}));
      const wrap = node('figure'); wrap.append(object, node('figcaption', subject === 'anatomy' ? '자체 제작 교육용 개념도입니다. 실제 해부표본·현미경 사진과 함께 구조를 확인하세요.' : '학습용 개략 도해입니다. 정확한 위치는 표준 위치 설명과 원문에서 함께 확인하세요.')); return wrap;
    }
    function sourceLink(source, title) { return node('a', title || '원문에서 더 읽기 →', {href: safeURL(source), class: 'learning-source', target: '_blank', rel: 'noopener'}); }
    function restart() { index = 0; flipped = false; session = null; status.textContent = ''; render(); }
    function empty(message) {
      stage.append(node('h3', message, {tabindex: '-1'}), node('p', '다른 단원이나 검색어를 선택해 보세요.'));
      if (mode === 'wrong') stage.append(button('전체 퀴즈로 가기', () => { mode = 'quiz'; modeSelect.value = mode; restart(); }));
    }
    function renderCards() {
      const cards = filteredCards(deck, progress, category.value, query.value, mode);
      if (!cards.length) { empty(mode === 'cards' ? '조건에 맞는 카드가 없습니다.' : '이 조건으로 저장된 카드가 없습니다.'); return; }
      index = Math.min(index, cards.length - 1);
      const c = cards[index];
      stage.append(node('p', c.category + ' · ' + (index + 1) + ' / ' + cards.length, {class: 'learning-eyebrow'}));
      stage.append(node('h3', flipped ? c.title : '기억을 꺼내 보세요', {tabindex: '-1'}));
      if (!flipped) {
        stage.append(node('p', c.prompt, {class: 'learning-prompt'}));
        stage.append(button('카드 뒤집기 · 답 확인', () => { flipped = true; render(); focusHeading(); }, {class: 'learning-primary'}));
      } else {
        const dl = node('dl', undefined, {class: 'learning-facts'});
        for (const f of c.facts) dl.append(node('dt', f.label), node('dd', f.value));
        stage.append(dl);
        if (c.diagram) stage.append(picture(c.diagram, c.title + ' 위치 도해'));
        stage.append(sourceLink(c.source));
        if (c.aliases) stage.append(node('p', '다른 표기: ' + c.aliases.join(' · '), {class: 'learning-note'}));
        if (c.relatedSource) stage.append(sourceLink(c.relatedSource, '부위별 임상해부학 →'));
        if (c.overviewSource) stage.append(sourceLink(c.overviewSource, '100선 구조표 확인 →'));
        const actions = node('div', undefined, {class: 'learning-actions'});
        function advance(removed) { index = (index + (removed ? 0 : 1)) % Math.max(cards.length, 1); flipped = false; render(); focusHeading(); }
        actions.append(button('이해했어요', () => { markCard(progress, c.id, true); save(); status.textContent = c.title + ' 이해한 카드로 저장했습니다.'; advance(mode === 'review'); }, {class: 'learning-primary'}),
          button('다시 볼게요', () => { markCard(progress, c.id, false); save(); status.textContent = c.title + ' 다시 볼 카드로 저장했습니다.'; advance(); }));
        stage.append(actions);
      }
      const nav = node('div', undefined, {class: 'learning-actions'});
      nav.append(button('← 이전', () => { index = (index + cards.length - 1) % cards.length; flipped = false; render(); focusHeading(); }),
        button(progress.saved.includes(c.id) ? '북마크 해제' : '북마크', () => { progress.saved = toggle(progress.saved, c.id, !progress.saved.includes(c.id)); save(); render(); }, {'aria-pressed': String(progress.saved.includes(c.id))}),
        button('다음 →', () => { index = (index + 1) % cards.length; flipped = false; render(); focusHeading(); }));
      stage.append(nav);
    }
    function begin(items, count, daily) {
      const questions = daily ? dailyQuestions(items, dailySeed(new Date()) + subject) : shuffle(items).slice(0, count);
      session = {questions, index: 0, answered: false, correct: 0}; render(); focusHeading();
    }
    function renderQuiz() {
      const items = filteredQuestions(deck, progress, category.value, query.value, mode === 'wrong', questionKind, difficulty);
      if (!session) {
        {
          const kinds = node('select', undefined, {'aria-label': '문제 유형'});
          const types = subject === 'acupoints'
            ? [['', '전체 문제 유형'], ['name', '혈명·경맥'], ['location', '표준 위치 설명'], ['diagram', '그림으로 경혈 찾기']]
            : subject === 'anatomy' ? [['', '전체 문제 유형'], ['fact', '부착·작용·연결·특징'], ['identify', '설명으로 구조 식별'], ['diagram', '도해로 구조 식별']]
            : (subject === 'shanghanlun' || subject === 'sasang') ? [['', '전체 문제 유형'], ['original', '원문·표지어 → 우리말 풀이'], ['interpretation', '조문·병증 해석'], ['treatment', '치법·처방 연결'], ...(subject === 'sasang' ? [['formula', '주요 처방 감별']] : []), ['case', '증례·배합 → 조문·병증 찾기']]
            : [['', '전체 문제 유형'], ['fact', '이름 → 개념·특징'], ['recall', '설명 → 이름 찾기']];
          types.push(['advanced', '통합·감별 (상·극상)']);
          for (const [value, label] of types) kinds.append(node('option', label, {value}));
          kinds.value = questionKind;
          kinds.addEventListener('change', () => {
            questionKind = kinds.value;
            if (questionKind && questionKind !== 'advanced' && (difficulty === 'high' || difficulty === 'expert')) difficulty = '';
            if (questionKind === 'advanced' && difficulty === 'basic') difficulty = '';
            restart();
          });
          stage.append(kinds);
          const levels = node('select', undefined, {'aria-label': '문제 난이도'});
          for (const [value, label] of [['', '전체 난이도'], ['basic', '기본'], ['high', '상'], ['expert', '극상']]) levels.append(node('option', label, {value}));
          levels.value = difficulty;
          levels.addEventListener('change', () => {
            difficulty = levels.value;
            if (difficulty === 'high' || difficulty === 'expert') questionKind = 'advanced';
            else if (difficulty === 'basic' && questionKind === 'advanced') questionKind = '';
            restart();
          });
          stage.append(levels, node('p', '상: 여러 단서·근접 감별 · 극상: 예외·조건 변화·복수 분류·출전 판단. 출제 의도에 따른 난이도입니다.', {class: 'learning-note'}));
        }
        if (!items.length) { empty(mode === 'wrong' ? '남아 있는 오답이 없습니다.' : '조건에 맞는 문제가 없습니다.'); return; }
        stage.append(node('h3', mode === 'wrong' ? '오답을 다시 꺼내 보세요' : '배운 내용을 확인해 보세요', {tabindex: '-1'}),
          node('p', '현재 선택 범위 ' + items.length + '문제. 한 문제씩 풀고 정답과 보기별 원문을 확인합니다.'));
        const actions = node('div', undefined, {class: 'learning-actions'});
        for (const count of new Set([10, 20, 50].map(n => Math.min(n, items.length)))) actions.append(button(count + '문제 풀기', () => begin(items, count, false), {class: count === Math.min(10, items.length) ? 'learning-primary' : ''}));
        if (items.length > 50) actions.append(button('선택 범위 전체 풀기', () => begin(items, items.length, false)));
        if (mode === 'quiz') actions.append(button('오늘의 10문제', () => begin(items, 10, true)));
        stage.append(actions); return;
      }
      if (session.index >= session.questions.length) {
        stage.append(node('h3', '복습을 마쳤어요', {tabindex: '-1'}), node('p', session.questions.length + '문제 중 ' + session.correct + '문제 정답 · ' + Math.round(session.correct / session.questions.length * 100) + '%', {class: 'learning-result'}));
        stage.append(button('새 퀴즈 시작', () => { session = null; render(); focusHeading(); }, {class: 'learning-primary'}),
          button('오답 다시 풀기', () => { mode = 'wrong'; modeSelect.value = mode; session = null; render(); focusHeading(); }));
        return;
      }
      const q = session.questions[session.index];
      stage.append(node('p', ({high: '상', expert: '극상'}[q.difficulty] || '기본') + ' · ' + q.category + ' · ' + (session.index + 1) + ' / ' + session.questions.length, {class: 'learning-eyebrow'}),
        node('h3', q.prompt, {tabindex: '-1'}));
      if (q.context) stage.append(node('p', q.context, {class: 'learning-prompt'}));
      if (q.diagram) stage.append(picture(q.diagram, subject === 'anatomy' ? '강조된 해부 구조를 식별하는 도해' : '붉은 점의 경혈을 맞히는 도해'));
      const options = node('div', undefined, {class: 'learning-options', role: 'group', 'aria-label': '정답 보기'});
      q.options.forEach((option, i) => {
        options.append(button((i + 1) + '. ' + option.text, () => {
          if (session.answered) return;
          session.answered = true; session.selected = i;
          const correct = recordAnswer(progress, q, i);
          if (correct) session.correct += 1;
          save(); render();
          const answer = stage.querySelector('.learning-feedback'); if (answer) answer.focus({preventScroll: true});
        }, {'data-option': String(i), 'aria-disabled': String(session.answered),
          class: session.answered && i === q.answer ? 'is-correct' : session.answered && i === session.selected ? 'is-wrong' : '',
          ...(session.answered ? {disabled: ''} : {})}));
      });
      stage.append(options);
      if (session.answered) {
        const feedback = node('div', undefined, {class: 'learning-feedback', tabindex: '-1'});
        feedback.append(node('strong', session.selected === q.answer ? '정답이에요.' : '다시 확인해 보세요. 정답은 ' + (q.answer + 1) + '번입니다.'), node('p', q.explanation), sourceLink(q.source, q.kind === 'advanced' ? '이 문항의 전체 해설 →' : undefined));
        if (q.relatedSource) feedback.append(sourceLink(q.relatedSource, '연결 학습 원문 →'));
        const details = node('details'), summary = node('summary', q.kind === 'advanced' ? '정답 근거와 오답 감별' : '보기별 설명과 원문'); details.append(summary);
        q.options.forEach((option, i) => {
          const p = node('p', (i + 1) + '번 · ' + option.owner + ' — ' + (option.detail || option.text) + ' ');
          p.append(sourceLink(option.source, q.kind === 'advanced' ? '문항 해설 →' : '해당 원문 →')); details.append(p);
        });
        feedback.append(details); stage.append(feedback);
        stage.append(button(session.index + 1 === session.questions.length ? '결과 보기' : '다음 문제 →', () => { session.index += 1; session.answered = false; session.selected = undefined; render(); focusHeading(); }, {class: 'learning-primary'}));
      }
      stage.append(button('퀴즈 선택으로 돌아가기', () => { session = null; render(); focusHeading(); }));
    }
    function renderIdentify() {
      const items = filteredQuestions(deck, progress, category.value, query.value, false).filter(q => q.acceptedAnswers);
      if (!session) {
        if (!items.length) { empty('조건에 맞는 구조 식별 문제가 없습니다.'); return; }
        stage.append(node('h3', '구조 이름을 직접 떠올려 보세요', {tabindex: '-1'}),
          node('p', '설명이나 이름을 가린 도해를 보고 구조 이름을 입력합니다. 한글의 다른 표기와 영문명도 정답으로 인정합니다.'));
        stage.append(button(Math.min(10, items.length) + '문제 시작', () => begin(items, 10, false), {class: 'learning-primary'})); return;
      }
      if (session.index >= session.questions.length) {
        stage.append(node('h3', '구조 식별을 마쳤어요', {tabindex: '-1'}), node('p', session.questions.length + '문제 중 ' + session.correct + '문제 정답', {class: 'learning-result'}));
        stage.append(button('다시 시작', restart, {class: 'learning-primary'})); return;
      }
      const q = session.questions[session.index];
      stage.append(node('p', q.category + ' · ' + (session.index + 1) + ' / ' + session.questions.length, {class: 'learning-eyebrow'}), node('h3', q.prompt, {tabindex: '-1'}));
      if (q.context) stage.append(node('p', q.context, {class: 'learning-prompt'}));
      if (q.diagram) stage.append(picture(q.diagram, '강조된 해부 구조를 식별하는 도해'));
      function submit(value) {
        if (session.answered) return;
        session.answered = true;
        session.selected = answerMatches(q, value) ? q.answer : -1;
        if (recordAnswer(progress, q, session.selected)) session.correct += 1;
        save(); render();
        const feedback = stage.querySelector('.learning-feedback'); if (feedback) feedback.focus({preventScroll: true});
      }
      if (!session.answered) {
        const form = node('form', undefined, {class: 'learning-answer-form'});
        const label = node('label', '구조 이름', {for: 'learning-structure-answer'});
        const input = node('input', undefined, {id: 'learning-structure-answer', type: 'text', autocomplete: 'off', placeholder: '한글 또는 영문명'});
        form.append(label, input, node('button', '답 확인', {type: 'submit', class: 'learning-primary'}));
        form.addEventListener('submit', event => { event.preventDefault(); submit(input.value); });
        stage.append(form, button('모르겠어요 · 정답 보기', () => submit('')));
      } else {
        const feedback = node('div', undefined, {class: 'learning-feedback', tabindex: '-1'});
        feedback.append(node('strong', session.selected === q.answer ? '정답이에요.' : '구조 이름을 다시 확인해 보세요.'), node('p', q.explanation), node('p', '인정하는 표기: ' + q.acceptedAnswers.join(' · ')), sourceLink(q.source));
        stage.append(feedback, button(session.index + 1 === session.questions.length ? '결과 보기' : '다음 문제 →', () => { session.index += 1; session.answered = false; render(); focusHeading(); }, {class: 'learning-primary'}));
      }
      stage.append(button('구조 식별 선택으로 돌아가기', restart));
    }
    function render() {
      stage.replaceChildren();
      if (!deck) return;
      updateStats();
      if (mode === 'identify') renderIdentify(); else if (mode === 'quiz' || mode === 'wrong') renderQuiz(); else renderCards();
    }
    async function load() {
      const seq = ++view.seq;
      deck = null; session = null; index = 0; flipped = false; questionKind = ''; difficulty = '';
      stage.replaceChildren(); status.textContent = SUBJECTS[subject] + ' 자료를 불러오고 있습니다…';
      filters.setAttribute('inert', ''); stats.textContent = '';
      for (const b of tabs.children) b.setAttribute('aria-pressed', String(b.dataset.subject === subject));
      try {
        const loaded = await deckFor(subject);
        if (!view.alive || seq !== view.seq || !root.isConnected) return;
        deck = loaded;
        modeSelect.replaceChildren();
        const modes = [['cards', '학습카드'], ['quiz', '퀴즈'], ['wrong', '오답 다시 풀기'], ['review', '다시 볼 카드'], ['saved', '북마크 카드']];
        if (subject === 'anatomy') modes.splice(2, 0, ['identify', '구조 이름 직접 입력']);
        if (subject !== 'anatomy' && mode === 'identify') mode = 'cards';
        for (const [value, title] of modes) modeSelect.append(node('option', title, {value}));
        modeSelect.value = mode;
        category.replaceChildren(node('option', '전체 단원', {value: ''}));
        for (const c of new Set(deck.cards.map(c => c.category))) category.append(node('option', c, {value: c}));
        filters.removeAttribute('inert'); status.textContent = ''; render();
      } catch (_) {
        if (!view.alive || seq !== view.seq || !root.isConnected) return;
        status.textContent = '학습자료를 불러오지 못했습니다. 연결 상태를 확인하고 다시 시도해 주세요.';
        stage.append(button('다시 불러오기', load, {class: 'learning-primary'}));
      }
    }
    query.addEventListener('input', restart);
    category.addEventListener('change', restart);
    modeSelect.addEventListener('change', () => { mode = modeSelect.value; restart(); });
    load();
  }
  global.addEventListener?.('hashchange', revealSource);
  if (global.document$ && global.document$.subscribe) global.document$.subscribe(init);
  else if (global.document.readyState === 'loading') global.document.addEventListener('DOMContentLoaded', init);
  else init();
})(typeof window === 'undefined' ? globalThis : window);
