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
test('UAMS aliases, regional filters and direct recall work for the expanded muscles', () => {
  const anatomy = JSON.parse(fs.readFileSync('docs/assets/learning/anatomy.json', 'utf8'));
  const p = study.emptyProgress();
  for (const [name, id] of [['sphenomeniscus', 'anatomy-sphenomeniscus'], ['Peroneus tertius', 'anatomy-fibularis-tertius'], ['pupillae, dilator', 'anatomy-dilator-pupillae'], ['detruser of bladder', 'anatomy-detrusor']]) {
    const cards = study.filteredCards(anatomy, p, '', name, 'cards');
    assert.ok(cards.some(c => c.id === id), name);
    const qs = study.filteredQuestions(anatomy, p, '', name, false, 'identify').filter(q => q.cardId === id);
    assert.ok(qs.length > 0, name);
    assert.ok(study.answerMatches(qs[0], name), name);
  }
  const eye = study.filteredCards(anatomy, p, '근육 · 눈·눈꺼풀', '', 'cards');
  assert.equal(eye.length, 10);
  assert.ok(eye.every(c => c.anatomyKind === 'muscle'));
  assert.equal(study.filteredCards(anatomy, p, '근육 · 골반·회음', '등자근', 'cards').length, 0);
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
test('all seven subjects select advanced levels, explain answers and recover when switching to basic kinds', async () => {
  for (const [subject, title, basicKind] of [
    ['anatomy', '기초 해부학', 'fact'], ['acupoints', '경혈학', 'name'],
    ['acupuncture', '침구학', 'fact'], ['herbs', '본초학', 'fact'],
    ['formulas', '방제학', 'fact'], ['shanghanlun', '상한론', 'original'],
    ['sasang', '사상의학', 'original']
  ]) {
    const d = JSON.parse(fs.readFileSync('docs/assets/learning/' + subject + '.json', 'utf8'));
    const h = harness(); h.button(title).events.click();
    h.loads.at(-1).resolve({ok: true, json: async () => d}); await h.settle();
    h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
    assert.deepEqual(all(h.select('문제 난이도')).filter(e => e.tagName === 'option').map(e => e.textContent),
      ['전체 난이도', '하', '중', '상']);
    for (const level of ['high', 'expert']) {
      const levels = h.select('문제 난이도'); levels.value = level; levels.events.change();
      assert.ok(all(h.root).some(e => e.textContent.includes('현재 선택 범위 17문제')));
    }
    h.button('10문제 풀기').events.click();
    const clue = all(h.root).find(e => e.attrs.class === 'learning-prompt').textContent;
    const q = d.questions.find(q => q.context === clue && q.difficulty === 'expert');
    assert.ok(q, subject);
    assert.ok(!all(h.root).some(e => e.textContent.includes(q.discriminator)));
    all(h.root).find(e => e.attrs['data-option'] === String((q.answer + 1) % 4)).events.click();
    assert.ok(all(h.root).some(e => e.textContent === '결정적 감별 단서: ' + q.discriminator));
    assert.ok(all(h.root).some(e => e.textContent === '가장 가까운 오답: ' + (q.nearestWrong + 1) + '번 — ' + q.options[q.nearestWrong].detail));
    assert.ok(all(h.root).some(e => e.textContent === '정답 근거와 오답 감별'));
    assert.ok(all(h.root).some(e => e.tagName === 'a' && e.attrs.href === q.relatedSource));
    h.select('학습 방식').value = 'wrong'; h.select('학습 방식').events.change();
    assert.ok(all(h.root).some(e => e.textContent.includes('현재 선택 범위 1문제')));
    h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
    const kinds = h.select('문제 유형'); kinds.value = basicKind; kinds.events.change();
    assert.equal(h.select('문제 난이도').value, '');
    assert.ok(h.button('10문제 풀기'));
  }
});
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
const anatomy = JSON.parse(fs.readFileSync('docs/assets/learning/anatomy.json', 'utf8'));
test('anatomy accepts exact Korean aliases and English but rejects nearby structures', () => {
  const q = anatomy.questions.find(q => q.cardId === 'anatomy-muscle-gluteus-medius' && q.acceptedAnswers);
  assert.ok(study.answerMatches(q, '중간 볼기근'));
  assert.ok(study.answerMatches(q, 'GLUTEUS MEDIUS'));
  assert.ok(study.answerMatches(q, 'ｇｌｕｔｅｕｓ ｍｅｄｉｕｓ'));
  for (const answer of ['', '둔근', '대둔근', 'gluteus', 'gluteus minimus', '모르겠습니다']) assert.equal(study.answerMatches(q, answer), false);
  assert.ok(study.filteredCards(anatomy, study.emptyProgress(), '', '중간볼기근', 'cards').some(c => c.id === q.cardId));
});
test('typed identification shares wrong answers, locks submissions and switches subjects safely', async () => {
  const h = harness(); h.button('기초 해부학').events.click();
  h.loads[1].resolve({ok: true, json: async () => anatomy}); await h.settle();
  assert.ok(h.select('학습 방식').children.some(e => e.value === 'identify'));
  h.select('학습 방식').value = 'identify'; h.select('학습 방식').events.change();
  h.button('10문제 시작').events.click();
  assert.equal(all(h.root).filter(e => e.attrs['data-option'] !== undefined).length, 0);
  const skip = h.button('모르겠어요 · 정답 보기'); skip.events.click(); skip.events.click();
  assert.ok(all(h.root).some(e => e.textContent.includes('오답 1개')));
  h.button('다음 문제 →').events.click();
  const prompt = all(h.root).find(e => e.tagName === 'h3').textContent;
  const object = all(h.root).find(e => e.tagName === 'object');
  const clue = all(h.root).find(e => e.attrs.class === 'learning-prompt');
  const q = anatomy.questions.find(q => q.acceptedAnswers && q.prompt === prompt && (object ? q.diagram === object.attrs.data : q.context === clue.textContent));
  const form = all(h.root).find(e => e.tagName === 'form');
  form.children.find(e => e.tagName === 'input').value = q.acceptedAnswers[0];
  form.events.submit({preventDefault(){}});
  assert.ok(all(h.root).some(e => e.textContent === '정답이에요.'));
  h.button('경혈학').events.click(); h.loads[0].resolve({ok:true,json:async()=>deck}); await h.settle();
  assert.equal(h.select('학습 방식').value, 'cards');
  assert.equal(h.select('학습 방식').children.some(e => e.value === 'identify'), false);
  assert.ok(h.button('카드 뒤집기 · 답 확인'));
});

test('hand and foot structures with similar Korean names remain distinct', () => {
  const hand = anatomy.questions.find(q => q.cardId === 'anatomy-bone-scaphoid' && q.acceptedAnswers);
  const foot = anatomy.questions.find(q => q.cardId === 'anatomy-bone-navicular-foot' && q.acceptedAnswers);
  assert.ok(study.answerMatches(hand, 'scaphoid'));
  assert.ok(study.answerMatches(foot, '발배뼈'));
  assert.equal(study.answerMatches(foot, '주상골'), false);
  assert.equal(study.answerMatches(hand, 'navicular'), false);
  const toe = anatomy.questions.find(q => q.cardId === 'anatomy-extensor-hallucis-longus' && q.acceptedAnswers);
  assert.ok(study.answerMatches(toe, 'EHL'));
  assert.equal(study.answerMatches(toe, 'EPL'), false);
  assert.equal(study.answerMatches(toe, '긴엄지폄근'), false);
  const adductorToe = anatomy.questions.find(q => q.cardId === 'anatomy-adductor-hallucis' && q.acceptedAnswers);
  assert.ok(study.answerMatches(adductorToe, '발의 무지내전근'));
  assert.equal(study.answerMatches(adductorToe, '무지내전근'), false);
});

for (const [subject, title] of [['shanghanlun', '상한론'], ['sasang', '사상의학']]) {
  test(title + ' subject loads, filters question types and reveals source comparisons', async () => {
    const classic = JSON.parse(fs.readFileSync('docs/assets/learning/' + subject + '.json', 'utf8'));
    const h = harness(); h.button(title).events.click();
    h.loads[1].resolve({ok: true, json: async () => classic}); await h.settle();
    assert.ok(h.button('카드 뒤집기 · 답 확인'));
    h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
    const kinds = h.select('문제 유형');
    assert.ok(kinds.children.some(e => e.value === 'original'));
    assert.ok(kinds.children.some(e => e.value === 'interpretation'));
    kinds.value = 'original'; kinds.events.change();
    h.button('10문제 풀기').events.click();
    const context = all(h.root).find(e => e.attrs.class === 'learning-prompt').textContent;
    assert.ok(classic.questions.some(q => q.kind === 'original' && q.context === context));
    all(h.root).find(e => e.attrs['data-option'] === '0').events.click();
    assert.ok(all(h.root).some(e => e.textContent === '보기별 설명과 원문'));
    const sources = all(h.root).filter(e => e.tagName === 'a' && (e.attrs.href || '').startsWith('/learning/' + subject + '/#'));
    assert.equal(sources.length, 5);
    const p = study.emptyProgress();
    assert.equal(study.filteredQuestions(classic, p, '', '', false, 'original').length, classic.cards.length);
    const q = classic.questions[0]; study.recordAnswer(p, q, (q.answer + 1) % 4);
    assert.equal(study.filteredQuestions(classic, p, '', '', true).length, 1);
    study.recordAnswer(p, q, q.answer);
    assert.equal(study.filteredQuestions(classic, p, '', '', true).length, 0);
  });
  test(title + ' authored case mode selects only cases and keeps answer sources', async () => {
    const classic = JSON.parse(fs.readFileSync('docs/assets/learning/' + subject + '.json', 'utf8'));
    const h = harness(); h.button(title).events.click();
    h.loads[1].resolve({ok: true, json: async () => classic}); await h.settle();
    h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
    const kinds = h.select('문제 유형');
    assert.ok(kinds.children.some(e => e.value === 'case'));
    kinds.value = 'case'; kinds.events.change();
    h.button('10문제 풀기').events.click();
    const context = all(h.root).find(e => e.attrs.class === 'learning-prompt').textContent;
    const q = classic.questions.find(q => q.kind === 'case' && q.context === context);
    assert.ok(q);
    assert.deepEqual(all(h.root).filter(e => e.attrs['data-option'] !== undefined).map(e => e.textContent), q.options.map((o, i) => (i + 1) + '. ' + o.text));
    all(h.root).find(e => e.attrs['data-option'] === String(q.answer)).events.click();
    assert.ok(all(h.root).some(e => e.textContent.includes(q.explanation)));
    const cases = study.filteredQuestions(classic, study.emptyProgress(), '', '', false, 'case');
    assert.equal(cases.length, subject === 'shanghanlun' ? 36 : 24);
    assert.ok(cases.every(q => q.kind === 'case'));
    assert.ok(all(h.root).some(e => e.tagName === 'a' && e.attrs.href === q.source));
  });
}

test('five-option cases retain level filters, structured observations and wrong-answer progress', async () => {
  for (const [subject, title] of Object.entries({anatomy:'기초 해부학',acupoints:'경혈학',acupuncture:'침구학',herbs:'본초학',formulas:'방제학',shanghanlun:'상한론',sasang:'사상의학'})) {
    const d = JSON.parse(fs.readFileSync('docs/assets/learning/' + subject + '.json', 'utf8'));
    const cases = d.questions.filter(q => q.kind === 'clinical');
    assert.equal(cases.length, 28);
    assert.equal(study.filteredQuestions(d, study.emptyProgress(), '', '', false, 'clinical', 'expert').length, 14);
    const h = harness(); h.button(title).events.click();
    h.loads.at(-1).resolve({ok:true,json:async()=>d}); await h.settle();
    h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
    h.select('문제 유형').value = 'clinical'; h.select('문제 유형').events.change();
    h.select('문제 난이도').value = 'expert'; h.select('문제 난이도').events.change();
    assert.equal(h.select('문제 유형').value, 'clinical');
    assert.ok(h.button('10문제 풀기')); h.button('10문제 풀기').events.click();
    const clue = all(h.root).find(e => e.attrs.class === 'learning-prompt').textContent;
    const q = cases.find(q => q.context === clue);
    assert.ok(q);
    assert.equal(all(h.root).filter(e => e.attrs['data-option'] !== undefined).length, 5);
    assert.ok(!all(h.root).some(e => e.textContent.includes(q.discriminator)));
    if(q.table) {
      assert.ok(all(h.root).some(e => e.tagName === 'caption' && e.textContent === q.table.caption));
      assert.equal(all(h.root).filter(e => e.tagName === 'tr').length, q.table.rows.length + 1);
    }
    const wrong = (q.answer + 1) % 5;
    all(h.root).find(e => e.attrs['data-option'] === String(wrong)).events.click();
    assert.ok(all(h.root).some(e => e.textContent === '결정적 감별 단서: ' + q.discriminator));
    assert.ok(all(h.root).filter(e => e.attrs['data-option'] !== undefined).every(e => e.attrs.disabled === ''));
    h.select('학습 방식').value = 'wrong'; h.select('학습 방식').events.change();
    assert.ok(h.button('1문제 풀기')); h.button('1문제 풀기').events.click();
    all(h.root).find(e => e.attrs['data-option'] === String(q.answer)).events.click();
    assert.ok(all(h.root).some(e => e.textContent.includes('오답 0개')));
  }
});

test('case tables display every observation, including the fifth choice', async () => {
  const herbs = JSON.parse(fs.readFileSync('docs/assets/learning/herbs.json', 'utf8'));
  const q = herbs.questions.find(q => q.kind === 'clinical' && q.table);
  const h = harness(); h.button('본초학').events.click();
  h.loads.at(-1).resolve({ok:true,json:async()=>({...herbs,questions:[q]})}); await h.settle();
  h.select('학습 방식').value = 'quiz'; h.select('학습 방식').events.change();
  h.select('문제 유형').value = 'clinical'; h.select('문제 유형').events.change();
  h.button('1문제 풀기').events.click();
  assert.ok(all(h.root).some(e => e.attrs['data-option'] === '4'));
  for(const row of q.table.rows) for(const value of row) assert.ok(all(h.root).some(e => e.textContent === value));
  for(const label of q.table.headers) assert.ok(all(h.root).some(e => e.tagName === 'th' && e.attrs.scope === 'col' && e.textContent === label));
});
