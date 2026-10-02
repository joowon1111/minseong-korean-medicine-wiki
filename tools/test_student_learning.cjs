const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const study = require('../docs/assets/learning/learning.js');
const deck = JSON.parse(fs.readFileSync('docs/assets/learning/acupoints.json', 'utf8'));

test('saved, again and known records survive reload and malformed storage', () => {
  let raw; const storage = {getItem: () => raw, setItem: (_, value) => raw = value};
  const progress = study.emptyProgress(), id = deck.cards[0].id;
  study.markCard(progress, id, false); progress.saved.push(id);
  assert.ok(study.writeProgress(storage, progress));
  assert.deepEqual(study.readProgress(storage), progress);
  study.markCard(progress, id, true);
  assert.deepEqual(progress.again, []); assert.deepEqual(progress.known, [id]);
  study.markCard(progress, id, true); assert.equal(progress.known.length, 1);
  raw = '{broken'; assert.deepEqual(study.readProgress(storage), study.emptyProgress());
  raw = JSON.stringify({known: [id, id, 7], wrong: 'bad', attempts: -1, correct: 8});
  assert.deepEqual(study.readProgress(storage).known, [id]);
  assert.equal(study.readProgress(storage).correct, 0);
  assert.equal(study.writeProgress(null, progress), false);
});
test('search intersects category and card review filters', () => {
  const p = study.emptyProgress(), first = deck.cards[0];
  p.saved = [first.id]; study.markCard(p, first.id, false);
  assert.equal(study.filteredCards(deck, p, first.category, first.title, 'saved').length, 1);
  assert.equal(study.filteredCards(deck, p, 'unknown', first.title, 'saved').length, 0);
  assert.equal(study.filteredCards(deck, p, '', '', 'review').length, 1);
  assert.equal(study.filteredCards(deck, p, '', 'no-such-entry', 'cards').length, 0);
  assert.ok(study.matches(first, '', 'lu1 폐경'));
  assert.equal(study.filteredQuestions(deck, p, '', '', false, 'diagram').length, 361);
  assert.equal(study.filteredQuestions(deck, p, '', '', false, 'unknown').length, 0);
});
test('incorrect questions are removed only when that question is answered correctly', () => {
  const p = study.emptyProgress(), q = deck.questions[0];
  assert.equal(study.recordAnswer(p, q, (q.answer + 1) % 4), false);
  assert.equal(study.filteredQuestions(deck, p, '', '', true).length, 1);
  assert.equal(study.recordAnswer(p, q, q.answer), true);
  assert.equal(p.wrong.length, 0); assert.equal(p.attempts, 2); assert.equal(p.correct, 1);
  assert.deepEqual(p.known, []); // Quiz score is not card understanding.
});
test('an exact point code selects that point instead of other location cross references', () => {
  const p = study.emptyProgress();
  for (const code of ['LU9', 'BL1', 'BL10']) {
    const result = study.filteredCards(deck, p, '', code.toLowerCase(), 'cards');
    assert.deepEqual(result.map(c => c.code), [code]);
    const questions = study.filteredQuestions(deck, p, '', code, false);
    assert.ok(questions.length > 0 && questions.every(q => q.cardId === 'point-' + code));
  }
  const herbs = JSON.parse(fs.readFileSync('docs/assets/learning/herbs.json', 'utf8'));
  assert.equal(study.filteredCards(herbs, p, '', '인삼', 'cards')[0].id, 'herb-ginseng');
  assert.ok(study.filteredCards(herbs, p, '', '청열', 'cards').length > 10);
});
test('daily practice is deterministic, contains no repeated IDs and changes with the date', () => {
  const a = study.dailyQuestions(deck.questions, '2026-10-2');
  assert.deepEqual(a, study.dailyQuestions(deck.questions, '2026-10-2'));
  assert.notDeepEqual(a, study.dailyQuestions(deck.questions, '2026-10-3'));
  assert.equal(new Set(a.map(q => q.id)).size, 10);
  assert.equal(study.dailyQuestions(deck.questions.slice(0, 3), 'date').length, 3);
  const copy = study.shuffle(deck.questions); assert.equal(copy.length, deck.questions.length);
  assert.equal(new Set(copy.map(q => q.id)).size, copy.length);
  assert.equal(study.safeURL('javascript:alert(1)'), '#');
  assert.equal(study.safeURL('//evil.example'), '#');
});

// Exercise the real controller with user events, including racing lazy loads.
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.events = {}; this.textContent = ''; this.value = ''; this.isConnected = true; }
  setAttribute(k, v) { this.attrs[k] = v; if(k === 'value') this.value = v; if(k.startsWith('data-')) this.dataset[k.slice(5)] = v; }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(k, f) { this.events[k] = f; }
  append(...els) { this.children.push(...els); }
  replaceChildren(...els) { this.children = els; }
  focus() { this.focused = true; }
  querySelector(s) { return all(this).find(e => s === 'h3' ? e.tagName === 'h3' : (e.attrs.class || '').split(' ').includes(s.slice(1))); }
}
function all(e) { return e.children.flatMap(c => [c, ...all(c)]); }
function harness() {
  const root = new Element('div'); const loads = [];
  const doc = {readyState: 'complete', createElement: tag => new Element(tag), querySelector: () => root};
  const context = {document: doc, location: {search: ''}, URLSearchParams, Date, Math, Map, Set, JSON,
    confirm: () => true, localStorage: {getItem: () => '{}', setItem: () => {}},
    fetch: url => new Promise((resolve, reject) => loads.push({url, resolve, reject}))};
  context.window = context;
  vm.runInNewContext(fs.readFileSync('docs/assets/learning/learning.js', 'utf8'), context);
  const button = label => all(root).find(e => e.tagName === 'button' && e.textContent === label);
  const select = label => all(root).find(e => e.attrs['aria-label'] === label);
  const settle = async () => { for(let i=0;i<8;i++) await Promise.resolve(); };
  return {root, loads, context, button, select, settle};
}
test('subject switches ignore stale responses and a failed fetch can be retried', async () => {
  const h = harness(); h.button('본초학').events.click();
  assert.equal(h.loads.length, 2);
  h.loads[0].resolve({ok: true, json: async () => deck}); await h.settle();
  assert.equal(h.button('카드 뒤집기 · 답 확인'), undefined);
  h.loads[1].reject(new Error('offline')); await h.settle();
  assert.ok(h.button('다시 불러오기'));
  h.button('다시 불러오기').events.click();
  const herbs = JSON.parse(fs.readFileSync('docs/assets/learning/herbs.json', 'utf8'));
  h.loads[2].resolve({ok: true, json: async () => herbs}); await h.settle();
  h.button('카드 뒤집기 · 답 확인').events.click();
  assert.ok(all(h.root).some(e => e.textContent === herbs.cards[0].title));
});
test('real quiz interaction locks the answer, records it once and advances only on next', async () => {
  const h = harness(); h.loads[0].resolve({ok: true, json: async () => deck}); await h.settle();
  h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
  h.button('10문제 풀기').events.click();
  const options = all(h.root).filter(e => e.attrs['data-option'] !== undefined);
  options[0].events.click(); options[0].events.click();
  assert.equal(all(h.root).filter(e => e.attrs.class === 'learning-feedback').length, 1);
  assert.ok(all(h.root).filter(e => e.attrs['data-option'] !== undefined).every(e => e.attrs.disabled === ''));
  assert.ok(h.button('다음 문제 →')); h.button('다음 문제 →').events.click();
  assert.equal(all(h.root).filter(e => e.attrs.class === 'learning-feedback').length, 0);
  assert.ok(all(h.root).some(e => e.textContent.includes('2 / 10')));
});
test('understood review card removal does not skip the following card', async () => {
  const h = harness(); h.loads[0].resolve({ok:true, json:async() => deck}); await h.settle();
  for(let i=0; i<3; i++) { h.button('카드 뒤집기 · 답 확인').events.click(); h.button('다시 볼게요').events.click(); }
  h.select('학습 방식').value = 'review'; h.select('학습 방식').events.change();
  h.button('카드 뒤집기 · 답 확인').events.click(); h.button('이해했어요').events.click();
  h.button('카드 뒤집기 · 답 확인').events.click();
  assert.ok(all(h.root).some(e => e.textContent === deck.cards[1].title));
});
test('a small selected range offers one quiz length without duplicate buttons', async () => {
  const h = harness(); h.loads[0].resolve({ok:true, json:async() => ({...deck, cards:deck.cards.slice(0,1), questions:deck.questions.slice(0,1)})}); await h.settle();
  h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
  assert.equal(all(h.root).filter(e => e.tagName === 'button' && e.textContent === '1문제 풀기').length, 1);
});
