// Browser-event regression checks for the independent Korean search panel.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '../docs/assets/korean-search-185.js'), 'utf8');
const rows = [
  { title: '불면', url: '/conditions/insomnia/', keywords: ['수면'], text: '불면 수면 잠', boost: 20 },
  { title: '비염', url: '/conditions/rhinitis/', keywords: ['코막힘'], text: '비염 코막힘', boost: 20 },
  { title: '족삼리 ST36', url: '/acupoints/st36/', keywords: ['ST36'], text: '족삼리', boost: 8 },
  { title: '불면 관련 연구', url: '/research/sleep/', keywords: [], text: '수면 불면', boost: 10 },
];

function browser(fetchImpl = async () => ({ ok: true, json: async () => rows })) {
  const listeners = {};
  const classes = new Set();
  const keyListeners = [];
  const subscriptions = [];
  const input = { value: '', dataset: {}, addEventListener: (name, fn) => { listeners[name] = fn; } };
  let panel;
  const requests = [];
  const document = {
    baseURI: 'https://wiki.minseong.co.kr/conditions/insomnia/',
    querySelector: (selector) => selector === '.md-search__input' ? input : { appendChild: (node) => { panel = node; } },
    getElementById: () => panel,
    createElement: () => ({ hidden: false, innerHTML: '', setAttribute() {} }),
    documentElement: { classList: { add: (name) => classes.add(name), remove: (name) => classes.delete(name) } },
    addEventListener(name, fn) { if (name === "keydown") keyListeners.push(fn); },
  };
  vm.runInNewContext(script, {
    document, setTimeout: (fn) => fn(), console: { error() {} },
    document$: { subscribe: (fn) => subscriptions.push(fn) },
    fetch: (...args) => { requests.push(args); return fetchImpl(...args); },
  });
  return {
    input, requests, classes, keyListeners, subscriptions,
    escape() { keyListeners.forEach((fn) => fn({ key: "Escape" })); },
    navigate() { input.dataset = {}; subscriptions.forEach((fn) => fn()); },
    get panel() { return panel; },
    async enter(value) { input.value = value; await listeners.input(); },
    async focus() { await listeners.focus(); },
  };
}

test('page visit and empty focus do not download the index or show a panel', async () => {
  const b = browser();
  await b.focus();
  await b.enter('   ');
  assert.equal(b.requests.length, 0);
  assert.equal(b.panel.hidden, true);
});

test('nested-page searches share one root-relative index and preserve exact-title ranking', async () => {
  const b = browser();
  await b.enter('불면');
  assert.equal(b.requests[0][0], '/assets/korean-search-index.json');
  assert.ok(b.panel.innerHTML.indexOf('/conditions/insomnia/') < b.panel.innerHTML.indexOf('/research/sleep/'));
  await b.enter('비염');
  assert.match(b.panel.innerHTML, /href="\/conditions\/rhinitis\/"/);
  assert.doesNotMatch(b.panel.innerHTML, /href="\/conditions\/insomnia\/"/);
  assert.equal(b.requests.length, 1);
});

test('patient expressions, spacing and full-width Latin characters still match', async () => {
  const b = browser();
  for (const [query, url] of [
    ['잠이 안 와요', '/conditions/insomnia/'],
    ['코가 막혀요', '/conditions/rhinitis/'],
    ['족삼리ＳＴ３６', '/acupoints/st36/'],
  ]) {
    await b.enter(query);
    assert.ok(b.panel.innerHTML.includes(`href="${url}"`), query);
  }
});

test('overlapping queries share the download and only the latest query renders', async () => {
  let finish;
  const b = browser(() => new Promise((resolve) => { finish = resolve; }));
  const first = b.enter('불면');
  const latest = b.enter('비염');
  assert.equal(b.requests.length, 1);
  finish({ ok: true, json: async () => rows });
  await Promise.all([first, latest]);
  assert.match(b.panel.innerHTML, /href="\/conditions\/rhinitis\/"/);
  assert.doesNotMatch(b.panel.innerHTML, /href="\/conditions\/insomnia\/"/);
});

test('clearing a pending query keeps its eventual results hidden', async () => {
  let finish;
  const b = browser(() => new Promise((resolve) => { finish = resolve; }));
  const pending = b.enter('불면');
  await b.enter('');
  finish({ ok: true, json: async () => rows });
  await pending;
  assert.equal(b.panel.hidden, true);
  assert.equal(b.panel.innerHTML, '');
});

test('a temporary failed download can be retried on the next search', async () => {
  let attempts = 0;
  const b = browser(async () => ++attempts === 1
    ? { ok: false, status: 503 }
    : { ok: true, json: async () => rows });
  await b.enter('불면');
  await b.focus();
  assert.equal(attempts, 2);
  assert.match(b.panel.innerHTML, /href="\/conditions\/insomnia\/"/);
});

test('unknown queries show an escaped empty result', async () => {
  const b = browser();
  await b.enter('<없는검색어>');
  assert.match(b.panel.innerHTML, /&lt;없는검색어&gt;/);
  assert.doesNotMatch(b.panel.innerHTML, /class="ms-ksearch-item"/);
});

test('escape cancels a pending render', async () => {
  let finish;
  const b = browser(() => new Promise((resolve) => { finish = resolve; }));
  const pending = b.enter('불면');
  b.escape();
  finish({ ok: true, json: async () => rows });
  await pending;
  assert.equal(b.panel.hidden, true);
  assert.equal(b.classes.has('ms-ksearch-active'), false);
});

test('instant navigation installs only one global listener and subscription', () => {
  const b = browser();
  for (let n = 0; n < 20; n++) b.navigate();
  assert.equal(b.subscriptions.length, 1);
  assert.equal(b.keyListeners.length, 1);
});

test('invalid rows and executable URLs cannot break or inject search results', async () => {
  const invalid = [null, {}, { ...rows[0], keywords: {} },
    ...['javascript:alert(1)', 'data:text/html,evil', '//evil.test/', '/\\evil.test/', '/\nevil.test/'].map(url => ({ ...rows[0], url }))];
  const b = browser(async () => ({ ok: true, json: async () => [...invalid, ...rows] }));
  await b.enter('불면');
  assert.match(b.panel.innerHTML, /href="\/conditions\/insomnia\/"/);
  assert.doesNotMatch(b.panel.innerHTML, /evil|javascript:|data:text/);
});

test('HTTP permission failures and corrupt JSON recover on next input', async () => {
  for (const response of [
    { ok: false, status: 403 },
    { ok: true, json: async () => { throw new SyntaxError('bad JSON'); } },
    { ok: true, json: async () => ({ rows: [] }) },
  ]) {
    let attempts = 0;
    const b = browser(async () => ++attempts === 1 ? response : { ok: true, json: async () => rows });
    await b.enter('불면');
    await b.focus();
    assert.equal(attempts, 2);
    assert.match(b.panel.innerHTML, /conditions\/insomnia/);
  }
});

test('empty index and HTML titles/snippets are safe', async () => {
  const empty = browser(async () => ({ ok: true, json: async () => [] }));
  await empty.enter('불면');
  assert.doesNotMatch(empty.panel.innerHTML, /class="ms-ksearch-item"/);
  const b = browser(async () => ({ ok: true, json: async () => [{ ...rows[0], title: '<img>불면', snippet: '<script>bad</script>' }] }));
  await b.enter('불면');
  assert.match(b.panel.innerHTML, /&lt;img&gt;/);
  assert.doesNotMatch(b.panel.innerHTML, /<script>|<img>/);
});
