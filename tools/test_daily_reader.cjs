const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const reader = require('../docs/assets/daily-korean-medicine/reader-core.js');
const data = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/data.json', 'utf8'));

test('shared dates reject rolled-over and malformed calendar values', () => {
  for (const value of ['2026-02-29', '2026-04-31', '2026-13-01', '2026-00-10', '2026-10-00', '2026-1-1', '0100-01-01', '', null]) {
    assert.equal(reader.parseDate(value), null, String(value));
  }
  assert.equal(reader.parseDate('2024-02-29').toISOString().slice(0, 10), '2024-02-29');
});

test('Korean midnight and leap-year date links round-trip independently of device timezone', () => {
  assert.equal(reader.today(new Date('2026-10-09T14:59:59Z')).toISOString().slice(0, 10), '2026-10-09');
  const now = new Date('2026-10-09T15:00:00Z');
  assert.equal(reader.today(now).toISOString().slice(0, 10), '2026-10-10');
  for (const value of ['2024-02-29', '2026-01-01', '2026-12-31', '2027-01-01']) {
    assert.equal(reader.dateFor(reader.offsetFor(value, now), now).toISOString().slice(0, 10), value);
  }
  for (const offset of [Infinity, NaN, 0.5]) assert.equal(reader.dateFor(offset, now), null);
});

test('card search covers all four streams and matches code, Hanja and explanation', () => {
  assert.equal(reader.search(data, 'all', '').length, 1036);
  const hegu = reader.search(data, 'points', '합곡 li4');
  assert.equal(hegu.length, 1);
  assert.match(hegu[0].title, /合谷/);
  assert(reader.search(data, 'points', '合谷').some(hit => hit.index === hegu[0].index));
  assert(reader.search(data, 'sasang', '갑오 구본').length > 0);
  assert(reader.search(data, 'shanghan', '桂枝湯').length > 0);
  assert.equal(reader.search(data, 'herbs', '합곡 li4').length, 0);
  assert.equal(reader.search(data, 'all', '<script>missing-card</script>').length, 0);
});

test('card permalinks respect topic boundaries and one-based indexes', () => {
  assert.deepEqual(reader.cardFrom('sasang-120', data), {topic: 'sasang', index: 119});
  assert.deepEqual(reader.cardFrom('points-361', data), {topic: 'points', index: 360});
  for (const value of ['sasang-121', 'points-362', 'sasang-0', 'sasang-01', 'unknown-1', 'sasang-1x', null]) {
    assert.equal(reader.cardFrom(value, data), null);
  }
});

test('meridian filters compose with point codes and never leak into other topics', () => {
  assert.equal(reader.search(data, 'points', '', '수양명대장경').length, 20);
  assert.equal(reader.search(data, 'points', 'li4', '수양명대장경').length, 1);
  assert.equal(reader.search(data, 'points', 'li4', '수태음폐경').length, 0);
  assert.equal(reader.search(data, 'points', '', '임맥').length, 24);
  assert.equal(reader.search(data, 'herbs', '', '수양명대장경').length, data.herbs.length);
});

test('daily clause prose has no imported document markup and related links resolve', () => {
  for (const [topic, items] of Object.entries(data)) {
    if (!Array.isArray(items)) continue;
    for (const item of items) {
      if (topic === 'shanghan') assert.doesNotMatch(item.translation, /\?\?\?|\]\(|\*\*/);
      for (const link of item.related || []) {
        assert(link.label && link.href.startsWith('/') && !link.href.startsWith('//'));
        const url = new URL(link.href, 'https://wiki.minseong.co.kr');
        if (url.pathname === '/daily-korean-medicine/') {
          assert(reader.cardFrom(url.searchParams.get('card'), data), link.href);
        } else {
          const path = 'docs' + url.pathname.replace(/\/$/, '');
          assert(fs.existsSync(path + '.md') || fs.existsSync(path + '/index.md'), link.href);
        }
      }
    }
  }
  assert(reader.search(data, 'herbs', '사역산').length === 0);
  assert(reader.search(data, 'herbs', '삼령백출산').some(hit => /길경/.test(hit.title)));
});
