/* Student learning room: lazy decks, local progress, instant navigation support. */
(function (global) {
  'use strict';
  const KEY = 'minseong-learning-v1';
  const VERSION = '20261004-07';
  const SUBJECTS = {anatomy: '기초 해부학', acupoints: '경혈학', acupuncture: '침구학', herbs: '본초학', formulas: '방제학', shanghanlun: '상한론', sasang: '사상의학'};
  const emptyProgress = () => ({known: [], again: [], saved: [], wrong: [], attempts: 0, correct: 0, schedule: {}, days: {}, resume: null});
  function readProgress(storage) {
    try {
      const parsed = JSON.parse(storage.getItem(KEY) || '{}');
      const result = emptyProgress();
      for (const key of ['known', 'again', 'saved', 'wrong']) {
        if (Array.isArray(parsed[key])) result[key] = [...new Set(parsed[key].filter(x => typeof x === 'string'))];
      }
      for (const key of ['attempts', 'correct']) if (Number.isSafeInteger(parsed[key]) && parsed[key] >= 0) result[key] = parsed[key];
      result.correct = Math.min(result.correct, result.attempts);
      result.schedule = cleanSchedule(parsed.schedule);
      result.days = cleanDays(parsed.days);
      result.resume = cleanResume(parsed.resume);
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
  function cleanSchedule(value) {
    const out = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) return out;
    for (const [id, row] of Object.entries(value).slice(0, 20000)) {
      if (['__proto__', 'constructor', 'prototype'].includes(id) || !/^[^\u0000-\u001f<>]{1,180}$/u.test(id) || !row || typeof row !== 'object') continue;
      if (!['attempts', 'correct', 'streak', 'due', 'last'].every(k => Number.isSafeInteger(row[k]) && row[k] >= 0)) continue;
      if (row.correct > row.attempts || row.streak > 5 || row.due > 8640000000000000) continue;
      out[id] = {attempts: row.attempts, correct: row.correct, streak: row.streak, due: row.due, last: row.last,
        subject: typeof row.subject === 'string' && SUBJECTS[row.subject] ? row.subject : '', category: String(row.category || '').slice(0, 150)};
    }
    return out;
  }
  function cleanDays(value) {
    const out = {};
    if (value && typeof value === 'object') for (const [date, row] of Object.entries(value).sort().slice(-365)) {
      if (/^\d{4}-\d{1,2}-\d{1,2}$/.test(date) && row && Number.isSafeInteger(row.attempts) && row.attempts >= 0 && Number.isSafeInteger(row.correct) && row.correct >= 0 && row.correct <= row.attempts) out[date] = {attempts: row.attempts, correct: row.correct};
    }
    return out;
  }
  function cleanResume(value) {
    if (!value || !SUBJECTS[value.subject] || !Array.isArray(value.ids) || value.ids.length > 20000 || !value.ids.every(id => typeof id === 'string' && id.length <= 180) || !Number.isSafeInteger(value.index) || value.index < 0 || value.index > value.ids.length || !Number.isSafeInteger(value.correct) || value.correct < 0 || value.correct > value.ids.length) return null;
    return {subject: value.subject, ids: value.ids, index: value.index, correct: value.correct, answered: value.answered === true,
      selected: Number.isInteger(value.selected) && value.selected >= -1 && value.selected <= 10 ? value.selected : undefined,
      mode: value.mode === 'identify' ? 'identify' : 'quiz'};
  }
  function recordAnswer(progress, question, answer, now = Date.now(), subject = '') {
    const correct = answer === question.answer;
    progress.attempts += 1;
    if (correct) progress.correct += 1;
    progress.wrong = toggle(progress.wrong, question.id, !correct);
    progress.schedule ||= {}; progress.days ||= {};
    const previous = progress.schedule[question.id] || {attempts: 0, correct: 0, streak: 0};
    const streak = correct ? Math.min(5, previous.streak + 1) : 0;
    const next = new Date(now); next.setDate(next.getDate() + [0, 1, 3, 7, 14, 30][streak]);
    progress.schedule[question.id] = {attempts: previous.attempts + 1, correct: previous.correct + Number(correct), streak,
      due: next.getTime(), last: now, subject, category: question.category || ''};
    const day = dailySeed(new Date(now)); const row = progress.days[day] || {attempts: 0, correct: 0};
    progress.days[day] = {attempts: row.attempts + 1, correct: row.correct + Number(correct)};
    progress.days = cleanDays(progress.days);
    return correct;
  }
  function dueQuestions(items, progress, now = Date.now()) {
    return items.filter(q => progress.schedule?.[q.id]?.due <= now).sort((a, b) => progress.schedule[a.id].due - progress.schedule[b.id].due);
  }
  function weakQuestions(items, progress) {
    return items.filter(q => progress.schedule?.[q.id] && progress.schedule[q.id].correct < progress.schedule[q.id].attempts)
      .sort((a, b) => progress.schedule[a.id].correct / progress.schedule[a.id].attempts - progress.schedule[b.id].correct / progress.schedule[b.id].attempts);
  }
  function backup(progress) { return JSON.stringify({format: 'minseong-learning', version: 1, exportedAt: new Date().toISOString(), progress}, null, 2); }
  function restore(text) {
    const data = JSON.parse(text);
    if (data?.format !== 'minseong-learning' || data.version !== 1 || !data.progress || !['known', 'again', 'saved', 'wrong'].every(k => Array.isArray(data.progress[k]) && data.progress[k].length <= 20000 && data.progress[k].every(x => typeof x === 'string' && !['__proto__', 'constructor', 'prototype'].includes(x) && /^[^\u0000-\u001f<>]{1,180}$/u.test(x)))) throw Error('기록 파일 형식을 확인해 주세요.');
    if (!['attempts', 'correct'].every(k => Number.isSafeInteger(data.progress[k]) && data.progress[k] >= 0) || data.progress.correct > data.progress.attempts) throw Error('학습 통계 형식을 확인해 주세요.');
    return readProgress({getItem: () => JSON.stringify(data.progress)});
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
  const api = {dueQuestions, weakQuestions, backup, restore, cleanSchedule, answerMatches, KEY, emptyProgress, readProgress, writeProgress, markCard, recordAnswer, matches,
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
    query.value = new URLSearchParams(global.location.search).get('q') || '';
    const category = node('select', undefined, {'aria-label': '학습 단원'});
    const modeSelect = node('select', undefined, {'aria-label': '학습 방식'});
    for (const [value, title] of [['cards', '학습카드'], ['quiz', '퀴즈'], ['wrong', '오답 다시 풀기'], ['due', '오늘 복습할 문제'], ['weak', '반복 오답 문제'], ['review', '다시 볼 카드'], ['saved', '북마크 카드']]) {
      modeSelect.append(node('option', title, {value}));
    }
    filters.append(query, category, modeSelect);
    const stats = node('p', '', {class: 'learning-stats', 'aria-live': 'polite'});
    const storageNote = node('p', '학습기록은 이 브라우저에 저장됩니다.', {class: 'learning-note'});
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
    const exportButton = node('button', '학습기록 내보내기', {type: 'button'});
    exportButton.addEventListener('click', () => {
      const url = global.URL.createObjectURL(new global.Blob([backup(progress)], {type: 'application/json'}));
      const a = node('a', '', {href: url, download: 'minseong-learning-' + dailySeed(new Date()) + '.json'});
      root.append(a); a.click(); a.remove(); global.setTimeout(() => global.URL.revokeObjectURL(url), 1000);
      status.textContent = '학습기록 파일을 저장했습니다. 다른 기기에서 가져올 수 있습니다.';
    });
    const importLabel = node('label', '학습기록 가져오기 ');
    const importInput = node('input', undefined, {type: 'file', accept: '.json,application/json', 'aria-label': '학습기록 파일 가져오기'});
    importInput.addEventListener('change', async () => {
      const file = importInput.files?.[0]; if (!file) return;
      try {
        if (file.size > 5000000) throw Error('5MB 이하 학습기록 파일을 선택하세요.');
        const restored = restore(await file.text());
        if (!root.isConnected) return;
        if (!global.confirm('현재 브라우저의 학습기록을 선택한 파일의 기록으로 바꿀까요?')) return;
        progress = restored; save(); restart(); status.textContent = '학습기록을 가져왔습니다.';
      } catch (error) {status.textContent = error.message || '학습기록을 가져오지 못했습니다.';}
      finally {importInput.value = '';}
    });
    importLabel.append(importInput);
    toolbar.append(resetFilters, exportButton, importLabel, clear);
    controls.append(tabs, filters, stats);
    root.replaceChildren(controls, status, stage, toolbar, storageNote);
    function save() {
      if (!writeProgress(storage, progress)) storageNote.textContent = '현재 브라우저에서 기록을 저장할 수 없습니다. 이번 화면에서는 학습을 계속할 수 있습니다.';
      updateStats();
    }
    function saveSession() {
      progress.resume = session && session.index < session.questions.length ? {subject, ids: session.questions.map(q => q.id), index: session.index, correct: session.correct, answered: session.answered, selected: session.selected, mode: mode === 'identify' ? 'identify' : 'quiz'} : null;
      writeProgress(storage, progress);
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
      const questions = daily ? dailyQuestions(items, dailySeed(new Date()) + subject) : (['due', 'weak'].includes(mode) ? items.slice(0, count) : shuffle(items).slice(0, count));
      session = {questions, index: 0, answered: false, correct: 0}; saveSession(); render(); focusHeading();
    }
    function renderQuiz() {
      const pool = filteredQuestions(deck, progress, category.value, query.value, mode === 'wrong', questionKind, difficulty);
      const items = mode === 'due' ? dueQuestions(pool, progress) : mode === 'weak' ? weakQuestions(pool, progress) : pool;
      if (!session) {
        {
          const kinds = node('select', undefined, {'aria-label': '문제 유형'});
          const types = subject === 'acupoints'
            ? [['', '전체 문제 유형'], ['name', '혈명 → 위치·표지 감별'], ['location', '위치·표지 → 혈명 감별'], ['diagram', '그림으로 경혈 찾기']]
            : subject === 'anatomy' ? [['', '전체 문제 유형'], ['fact', '부착·작용·연결·특징'], ['identify', '설명으로 구조 식별'], ['diagram', '도해로 구조 식별']]
            : (subject === 'shanghanlun' || subject === 'sasang') ? [['', '전체 문제 유형'], ['original', '원문·표지어 → 우리말 풀이'], ['interpretation', '조문·병증 해석'], ['treatment', '치법·처방 연결'], ...(subject === 'sasang' ? [['formula', '주요 처방 감별']] : []), ['case', '증례·배합 → 조문·병증 찾기']]
            : [['', '전체 문제 유형'], ['fact', '이름 → 개념·특징'], ['recall', '설명 → 이름 찾기']];
          types.push(['advanced', '통합·감별 (중·상)']);
          types.push(['clinical', '증례·배혈·본초 추론 (5지선다)']);
          for (const [value, label] of types) kinds.append(node('option', label, {value}));
          kinds.value = questionKind;
          kinds.addEventListener('change', () => {
            questionKind = kinds.value;
            if (questionKind && !['advanced', 'clinical'].includes(questionKind) && (difficulty === 'high' || difficulty === 'expert')) difficulty = '';
            if (['advanced', 'clinical'].includes(questionKind) && difficulty === 'basic') difficulty = '';
            restart();
          });
          stage.append(kinds);
          const levels = node('select', undefined, {'aria-label': '문제 난이도'});
          for (const [value, label] of [['', '전체 난이도'], ['basic', '하'], ['high', '중'], ['expert', '상']]) levels.append(node('option', label, {value}));
          levels.value = difficulty;
          levels.addEventListener('change', () => {
            difficulty = levels.value;
            if ((difficulty === 'high' || difficulty === 'expert') && questionKind !== 'clinical') questionKind = 'advanced';
            else if (difficulty === 'basic' && ['advanced', 'clinical'].includes(questionKind)) questionKind = '';
            restart();
          });
          stage.append(levels, node('p', '하: 단일 개념 회상 · 중: 유사 구조·병증 감별 · 상: 예외·조건 변화·복수 단서 판단. 출제 의도에 따른 난이도입니다.', {class: 'learning-note'}));
        }
        if (!items.length) { empty(mode === 'wrong' ? '남아 있는 오답이 없습니다.' : mode === 'due' ? '현재 범위에서 복습할 시점이 된 문제가 없습니다.' : mode === 'weak' ? '현재 범위에 기록된 반복 오답이 없습니다.' : '조건에 맞는 문제가 없습니다.'); return; }
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
      stage.append(node('p', ({high: '중', expert: '상'}[q.difficulty] || '하') + ' · ' + q.category + ' · ' + (session.index + 1) + ' / ' + session.questions.length, {class: 'learning-eyebrow'}),
        node('h3', q.prompt, {tabindex: '-1'}));
      if (q.context) stage.append(node('p', q.context, {class: 'learning-prompt'}));
      if (q.table) {
        const wrap = node('div', undefined, {class: 'learning-table-wrap', role: 'region', 'aria-label': q.table.caption, tabindex: '0'});
        const table = node('table', undefined, {class: 'learning-observations'});
        table.append(node('caption', q.table.caption));
        const head = node('thead'), header = node('tr');
        q.table.headers.forEach(label => header.append(node('th', label, {scope: 'col'})));
        head.append(header); table.append(head);
        const body = node('tbody');
        q.table.rows.forEach(values => { const row = node('tr'); values.forEach((value, i) => row.append(node(i ? 'td' : 'th', value, i ? undefined : {scope: 'row'}))); body.append(row); });
        table.append(body); wrap.append(table); stage.append(wrap);
      }
      if (q.diagram) stage.append(picture(q.diagram, subject === 'anatomy' ? '강조된 해부 구조를 식별하는 도해' : '붉은 점의 경혈을 맞히는 도해'));
      const options = node('div', undefined, {class: 'learning-options', role: 'group', 'aria-label': '정답 보기'});
      q.options.forEach((option, i) => {
        options.append(button((i + 1) + '. ' + option.text, () => {
          if (session.answered) return;
          session.answered = true; session.selected = i;
          const correct = recordAnswer(progress, q, i, Date.now(), subject);
          if (correct) session.correct += 1;
          save(); saveSession(); render();
          const answer = stage.querySelector('.learning-feedback'); if (answer) answer.focus({preventScroll: true});
        }, {'data-option': String(i), 'aria-disabled': String(session.answered),
          class: session.answered && i === q.answer ? 'is-correct' : session.answered && i === session.selected ? 'is-wrong' : '',
          ...(session.answered ? {disabled: ''} : {})}));
      });
      stage.append(options);
      if (session.answered) {
        const feedback = node('div', undefined, {class: 'learning-feedback', tabindex: '-1'});
        feedback.append(node('strong', session.selected === q.answer ? '정답이에요.' : '다시 확인해 보세요. 정답은 ' + (q.answer + 1) + '번입니다.'), node('p', q.explanation), sourceLink(q.source, ['advanced', 'clinical'].includes(q.kind) ? '이 문항의 전체 해설 →' : undefined));
        if (q.relatedSource) feedback.append(sourceLink(q.relatedSource, '연결 학습 원문 →'));
        if (q.discriminator) feedback.append(node('p', '결정적 감별 단서: ' + q.discriminator));
        if (Number.isInteger(q.nearestWrong)) feedback.append(node('p', '가장 가까운 오답: ' + (q.nearestWrong + 1) + '번 — ' + q.options[q.nearestWrong].detail));
        const details = node('details'), summary = node('summary', ['advanced', 'clinical'].includes(q.kind) ? '정답 근거와 오답 감별' : '보기별 설명과 원문'); details.append(summary);
        q.options.forEach((option, i) => {
          const p = node('p', (i + 1) + '번 · ' + option.owner + ' — ' + (option.detail || option.text) + ' ');
          p.append(sourceLink(option.source, ['advanced', 'clinical'].includes(q.kind) ? '문항 해설 →' : '해당 원문 →')); details.append(p);
        });
        feedback.append(details); stage.append(feedback);
        stage.append(button(session.index + 1 === session.questions.length ? '결과 보기' : '다음 문제 →', () => { session.index += 1; session.answered = false; session.selected = undefined; saveSession(); render(); focusHeading(); }, {class: 'learning-primary'}));
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
        if (recordAnswer(progress, q, session.selected, Date.now(), subject)) session.correct += 1;
        save(); saveSession(); render();
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
        stage.append(feedback, button(session.index + 1 === session.questions.length ? '결과 보기' : '다음 문제 →', () => { session.index += 1; session.answered = false; session.selected = undefined; saveSession(); render(); focusHeading(); }, {class: 'learning-primary'}));
      }
      stage.append(button('구조 식별 선택으로 돌아가기', restart));
    }
    function render() {
      stage.replaceChildren();
      if (!deck) return;
      updateStats();
      const personal = node('div', undefined, {class: 'learning-personal'});
      const day = progress.days[dailySeed(new Date())] || {attempts: 0, correct: 0};
      const due = dueQuestions(deck.questions, progress).length;
      personal.append(node('p', '오늘 ' + day.attempts + '회 풀이 · ' + day.correct + '회 정답 · 이 과목 복습 예정 ' + due + '문제'));
      const units = new Map();
      for (const q of deck.questions) { const r = progress.schedule[q.id]; if (!r) continue; const unit = units.get(q.category) || {attempts: 0, correct: 0}; unit.attempts += r.attempts; unit.correct += r.correct; units.set(q.category, unit); }
      const weak = [...units].filter(([, r]) => r.attempts >= 3).sort((a, b) => a[1].correct / a[1].attempts - b[1].correct / b[1].attempts).slice(0, 3);
      if (weak.length) personal.append(node('p', '복습할 단원: ' + weak.map(([name, r]) => name + ' ' + Math.round(100 * r.correct / r.attempts) + '% (' + r.attempts + '회)').join(' · ')));
      stage.append(personal);
      const prior = progress.resume;
      if (!session && prior && prior.subject === subject && prior.index < prior.ids.length) {
        const byId = new Map(deck.questions.map(q => [q.id, q]));
        if (prior.ids.every(id => byId.has(id))) {
          const resumeButton = button('풀던 문제 이어하기 (' + (prior.index + 1) + '/' + prior.ids.length + ')', () => {
            mode = prior.mode; modeSelect.value = mode; session = {questions: prior.ids.map(id => byId.get(id)), index: prior.index, correct: prior.correct, answered: prior.answered, selected: prior.selected};
            render(); focusHeading();
          }, {class: 'learning-primary'});
          stage.append(resumeButton);
        }
      }
      if (mode === 'identify') renderIdentify(); else if (['quiz', 'wrong', 'due', 'weak'].includes(mode)) renderQuiz(); else renderCards();
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
        const modes = [['cards', '학습카드'], ['quiz', '퀴즈'], ['wrong', '오답 다시 풀기'], ['due', '오늘 복습할 문제'], ['weak', '반복 오답 문제'], ['review', '다시 볼 카드'], ['saved', '북마크 카드']];
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
