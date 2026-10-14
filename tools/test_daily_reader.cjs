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
  assert.equal(almanac.cards.length,240);
  assert.equal(new Set(almanac.cards.map(c=>c.practice)).size,240);
  assert.equal(new Set(almanac.cards.map(c=>c.line)).size,240);
  for (const season of ['spring','summer','autumn','winter']) {
    const cards=almanac.cards.filter(c=>c.season===season);
    assert.equal(cards.length,60);
    for (const card of cards) {
      assert(card.line && card.theme && card.practice && (almanac.sources[card.source] || card.kind === "life" && card.story && card.relatedHref));
      if(card.modern) assert(almanac.modern[card.modern]);
    }
  }
});


test('almanac source links reach both classical archive hubs and each season includes Donguibogam', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  for(const source of Object.values(almanac.sources)) {
    assert(source.original && source.translation && source.context && source.label);
    assert(source.href.startsWith('https://'));
    const url=new URL(source.archiveHref,'https://wiki.minseong.co.kr');
    const path='docs'+url.pathname.replace(/\/$/,'');
    assert(fs.existsSync(path+'.md') || fs.existsSync(path+'/index.md'),source.archiveHref);
  }
  for(const season of ['spring','summer','autumn','winter']) {
    const books=almanac.cards.filter(c=>c.season===season && c.source).map(c=>almanac.sources[c.source].label);
    assert(books.some(label=>label.startsWith('동의보감')));
    assert(books.some(label=>label.startsWith('황제내경')));
  }
});

test('almanac identifiers remain tied to content when order changes and invalid links fail closed', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  assert.equal(new Set(almanac.cards.map(item => item.id)).size,240);
  const reversed = {...almanac,cards:[...almanac.cards].reverse()};
  for(const item of almanac.cards) {
    assert.equal(reader.almanacFrom(item.id,reversed),item);
    assert.equal(reader.almanacFrom(item.id,almanac),item);
  }
  for(const id of ['spring-00','spring-61','spring-1','autumn-01x','spring-01/','unknown-01','__proto__',null]) {
    assert.equal(reader.almanacFrom(id,almanac),null);
  }
});

test('almanac search combines season with original, gloss, practical action and book terms', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  assert.equal(reader.searchAlmanac(almanac,'all','').length,240);
  assert.equal(reader.searchAlmanac(almanac,'winter','').length,60);
  const hits=reader.searchAlmanac(almanac,'autumn','동의보감 少勞');
  assert(hits.length >= 1);
  assert(hits.every(item => item.source === 'gentle' && item.season === 'autumn'));
  assert(reader.searchAlmanac(almanac,'all','넓적다리').every(item=>item.source==='leg-movement'));
  assert.equal(reader.searchAlmanac(almanac,'all','넓적다리').length,5);
  assert.equal(reader.searchAlmanac(almanac,'all','식사 건너뛰거나')[0].season,'summer');
  assert.equal(reader.searchAlmanac(almanac,'autumn','동의보감 missing-word').length,0);
  assert.equal(reader.searchAlmanac(almanac,'all','<script>missing</script>').length,0);
  for(const source of Object.values(almanac.sources)) assert(source.words);
});

test('copied almanac prose distinguishes lifestyle suggestions from attributed original text', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  for(const item of almanac.cards) {
    const text=reader.almanacText(item,almanac),source=almanac.sources[item.source];
    assert(text.includes('생활 제안 — '+item.line));
    assert(text.includes('오늘의 작은 실천 — '+item.practice));
    if(source) {
      assert(text.includes('고전 원문 — '+source.original));
      assert(text.includes('원문 풀이 — '+source.translation));
      assert(text.includes('출처 — '+source.label));
      assert(text.includes(source.href));
    } else {
      assert.equal(item.kind,'life');
      assert(!text.includes('고전 원문 —'));
      assert(!text.includes('undefined'));
      assert(text.includes(item.story));
    }
    if(item.modern) assert(text.includes(almanac.modern[item.modern].href));
  }
});

test('short review requires a complete pair and is searchable without changing card identifiers', () => {
  assert.equal(reader.reviewFor(null), null);
  assert.equal(reader.reviewFor({reviewQuestion:'질문만'}), null);
  assert.equal(reader.reviewFor({reviewQuestion:' ',reviewAnswer:'풀이'}), null);
  assert.deepEqual(reader.reviewFor({reviewQuestion:' 질문 ',reviewAnswer:' 풀이 '}), {question:'질문',answer:'풀이'});
  for (const topic of ['points','herbs','shanghan','sasang']) {
    const enriched = data[topic].filter(item => reader.reviewFor(item));
    assert.equal(enriched.length, topic === "points" ? 24 : 36, topic);
    assert(enriched.every(item => item.related && item.related.length));
  }
  const hegu = reader.search(data,'points','합곡 사관혈');
  assert(hegu.some(hit => data.points[hit.index].code === 'LI4'));
  assert(reader.search(data,'shanghan','수증치지 현재').some(hit => hit.index === 15));
  assert.deepEqual(reader.cardFrom('herbs-157',data),{topic:'herbs',index:156});
});

test('life topic, season and free text compose without losing original almanac links', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  assert.equal(Object.keys(almanac.topics).length,6);
  for (const item of almanac.cards) assert(almanac.topics[item.topic],item.id);
  const allEyes = reader.searchAlmanac(almanac,'all','', 'senses');
  assert(allEyes.length >= 4);
  assert(allEyes.every(item => ['ear-eye','long-looking'].includes(item.source)));
  const winterEyes = reader.searchAlmanac(almanac,'winter','', 'senses');
  assert(winterEyes.length && winterEyes.every(item => item.season === 'winter'));
  assert.equal(reader.searchAlmanac(almanac,'winter','', 'unknown').length,0);
  assert(reader.searchAlmanac(almanac,'spring','산책의 출발점','movement').some(item => item.id === 'spring-37'));
  assert.equal(reader.almanacFrom('spring-01',almanac).theme,'산책');
  assert.equal(reader.almanacFrom('winter-48',almanac).season,'winter');
});

test('expansion keeps previously shared seasonal dates on their original reading cycle', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  const legacy = {...almanac,cards:almanac.cards.filter(item => !item.introducedOn)};
  for (const date of ['2024-02-29','2026-03-01','2026-07-15','2026-10-11']) {
    const old = reader.seasonalCard(reader.parseDate(date),legacy);
    const current = reader.seasonalCard(reader.parseDate(date),almanac);
    assert.equal(current.item.id,old.item.id,date);
    assert.equal(current.count,36,date);
  }
  assert.equal(reader.seasonalCard(reader.parseDate('2026-10-12'),almanac).count,48);
  for (const item of almanac.cards.filter(item => item.introducedOn)) assert(reader.parseDate(item.introducedOn));
});


test('life expansion preserves dated readings and gives every term a stable sourced card', () => {
  const almanac = JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/yangsheng.json','utf8'));
  const old = {...almanac,cards:almanac.cards.filter(c => c.introducedOn !== '2026-10-14')};
  for(const date of ['2026-10-12','2026-10-13']) {
    assert.equal(reader.seasonalCard(reader.parseDate(date),almanac).item.id,
      reader.seasonalCard(reader.parseDate(date),old).item.id);
  }
  const terms=almanac.cards.filter(c=>c.solarTerm);
  assert.equal(terms.length,24);
  assert.equal(new Set(terms.map(c=>c.solarTerm)).size,24);
  for(const item of almanac.cards.filter(c=>c.introducedOn==='2026-10-14')) {
    assert(item.story && item.relatedHref,item.id);
    const pathname=new URL(item.relatedHref,'https://wiki.minseong.co.kr').pathname.replace(/\/$/,'');
    assert(fs.existsSync('docs'+pathname+'.md') || fs.existsSync('docs'+pathname+'/index.md'),item.relatedHref);
  }
  for(const item of terms) assert(reader.searchAlmanac(almanac,'all',item.solarTerm).some(c=>c.id===item.id));
  assert(reader.searchAlmanac(almanac,'all','천금요방').length>=3);
  assert.equal(reader.seasonalCard(reader.parseDate('2026-10-14'),almanac).count,60);
});
