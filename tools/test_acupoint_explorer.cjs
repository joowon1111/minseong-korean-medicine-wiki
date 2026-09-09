const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {normalize, matches, init} = require('../docs/assets/acupoint-atlas/explorer.js');
test('search accepts Korean, spaced codes, case and full-width text', () => {
  assert.equal(normalize(' ＬＩ－４ '), 'li4');
  assert.ok(matches('합곡 LI4', 'LI', '', 'li 4'));
  assert.ok(matches('합곡 LI4', 'LI', 'LI', '합곡'));
  assert.ok(!matches('합곡 LI4', 'LI', 'PC', '합곡'));
  assert.ok(!matches('합곡 LI4', 'LI', '', '<script>'));
  assert.ok(matches('합곡 LI4', 'LI', '', null));
});
test('unrelated pages and incomplete controls remain usable', () => {
  assert.doesNotThrow(() => init({getElementById: () => null}));
  assert.doesNotThrow(() => init({getElementById: id => id === 'acupoint-controls' ? {dataset:{}} : null}));
});
test('all 361 unique point links are preserved in 14 searchable groups', () => {
  const doc = fs.readFileSync(path.join(__dirname, '../docs/acupoint-network/standard-atlas.md'), 'utf8');
  const groups = [...doc.matchAll(/data-meridian="([A-Z]+)"/g)];
  assert.equal(groups.length, 14);
  const links = [...doc.matchAll(/\]\((\.\.\/acupuncture\/points\/[^)]+\.md)\)/g)];
  assert.equal(links.length, 361);
  assert.equal(new Set(links.map(x=>x[1])).size, 361);
  for (const [, link] of links) assert.ok(fs.existsSync(path.resolve(__dirname, '../docs/acupoint-network', link)), link);
});
test('diagram destinations are existing point pages without scripts or remote assets', () => {
  for (const file of ['hand-dorsal.svg','wrist-palmar.svg']) {
    const svg = fs.readFileSync(path.join(__dirname, '../docs/assets/acupoint-atlas', file), 'utf8');
    assert.ok(!/<script|onload=|onclick=|<image/i.test(svg));
    const links = [...svg.matchAll(/href="(\/acupuncture\/points\/[^"#]+)"/g)];
    assert.ok(links.length > 0);
    for (const [, link] of links) assert.ok(fs.existsSync(path.join(__dirname, '../docs', link.slice(1,-1)+'.md')), link);
  }
});
