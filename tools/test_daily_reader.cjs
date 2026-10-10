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
          const path = 'docs' + decodeURIComponent(url.pathname).replace(/\/$/, '');
          assert(fs.existsSync(path + '.md') || fs.existsSync(path + '/index.md'), link.href);
        }
      }
    }
  }
  assert(reader.search(data, 'herbs', '사역산').length === 0);
  assert(reader.search(data, 'herbs', '삼령백출산').some(hit => /길경/.test(hit.title)));
});


test('chapter filters follow source documents and compose with text and topic', () => {
  const counts = {"taiyang-upper":30,"taiyang-middle":97,"taiyang-lower":51,yangming:84,shaoyang:10,taiyin:8,shaoyin:45,jueyin:56,huoluan:10,recovery:7};
  for (const [key, count] of Object.entries(counts)) {
    assert.equal(reader.search(data, 'shanghan', '', 'all', key).length, count, key);
  }
  assert(reader.search(data, 'shanghan', '五苓散', 'all', 'huoluan').some(hit => hit.index === 385));
  assert.equal(reader.search(data, 'shanghan', '竹葉石膏湯', 'all', 'taiyang-upper').length, 0);
  assert.equal(reader.search(data, 'herbs', '', 'all', 'huoluan').length, data.herbs.length);
  assert.equal(reader.chapterFor({href:'/other/yangming/'}), null);
});

test('exact clause numbers reject misleading prefixes and retain original 398-card order', () => {
  for (let number = 1; number <= 398; number++) {
    assert.deepEqual(reader.clauseFrom(String(number), data), {topic:'shanghan',index:number-1});
  }
  for (const value of ['0','399','01','1.0','1e2','+1','12조','-1','',null]) assert.equal(reader.clauseFrom(value, data), null);
  assert.deepEqual(reader.clauseFrom(' 163 ', data), {topic:'shanghan',index:162});
});

test('saved cards accept only existing canonical identifiers, deduplicate and bound stored lists', () => {
  for (const raw of ['broken', '{}', 'null', '42', '"points-1"', null]) assert.deepEqual(reader.savedCards(raw, data), []);
  assert.deepEqual(reader.savedCards(JSON.stringify(['points-1','points-01','points-1','herbs-999',null,{},'sasang-120','shanghan-398']), data), ['points-1','sasang-120','shanghan-398']);
  const many = data.points.map((_,i) => 'points-' + (i+1));
  assert.equal(reader.savedCards(JSON.stringify(many), data).length, 200);
});

test('seasonal almanac follows Korean month boundaries and stays continuous across winter New Year', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  const examples = {'2026-02-28':'winter','2026-03-01':'spring','2026-05-31':'spring','2026-06-01':'summer','2026-08-31':'summer','2026-09-01':'autumn','2026-11-30':'autumn','2026-12-01':'winter','2024-02-29':'winter'};
  for (const [date,season] of Object.entries(examples)) assert.equal(reader.seasonalCard(reader.parseDate(date),almanac).season, season);
  const last = reader.seasonalCard(reader.parseDate('2026-12-31'),almanac);
  const first = reader.seasonalCard(reader.parseDate('2027-01-01'),almanac);
  assert.equal(first.index, (last.index+1)%last.count);
  assert.equal(reader.seasonalCard(new Date(NaN),almanac),null);
  assert.equal(reader.seasonalCard(reader.parseDate('2026-03-01'),{cards:[]}),null);
  assert.equal(almanac.cards.length,48);
  assert.equal(new Set(almanac.cards.map(c=>c.line)).size,48);
  for (const season of ['spring','summer','autumn','winter']) {
    const cards=almanac.cards.filter(c=>c.season===season);
    assert.equal(cards.length,12);
    for (const card of cards) {
      assert(card.line && card.theme && almanac.sources[card.source]);
      if(card.modern) assert(almanac.modern[card.modern]);
    }
  }
});
