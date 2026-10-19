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
  // Compare the searchable catalogue, not repeated links in learning examples.
  const groups = [...doc.matchAll(/<div class="acupoint-group" data-meridian="([A-Z]+)"[^>]*>([\s\S]*?)<\/div>/g)];
  const counts = {LU:11, LI:20, ST:45, SP:21, HT:9, SI:19, BL:67, KI:27, PC:9, TE:23, GB:44, LR:14, GV:28, CV:24};
  assert.equal(groups.length, 14);
  assert.equal(new Set(groups.map(group=>group[1])).size, 14);
  const links = groups.flatMap(([, meridian, content]) => {
    const found = [...content.matchAll(/\]\((\.\.\/acupuncture\/points\/[^)]+\.md)\)/g)];
    assert.equal(found.length, counts[meridian], meridian);
    return found;
  });
  assert.equal(links.length, 361);
  assert.equal(new Set(links.map(x=>x[1])).size, 361);
  // Both catalogue and additional learning links must resolve to real documents.
  const allLinks = [...doc.matchAll(/\]\((\.\.\/acupuncture\/points\/[^)]+\.md)\)/g)];
  for (const [, link] of allLinks) assert.ok(fs.existsSync(path.resolve(__dirname, '../docs/acupoint-network', link)), link);
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

test('regional SVGs load only on expansion and do not reload on repeat setup', () => {
  const {initRegions} = require('../docs/assets/acupoint-atlas/explorer.js');
  let loads = 0, bindings = 0;
  const objects = [0,1].map(i => ({dataset:{src:'/assets/acupoint-atlas/test-'+i+'.svg'},
    setAttribute(key, value) { assert.equal(key,'data'); assert.equal(value,this.dataset.src); loads++; },
    removeAttribute(key) { assert.equal(key,'data-src'); delete this.dataset.src; }}));
  const regions = objects.map((object,i) => ({open:i===0,dataset:{},
    querySelectorAll() { return object.dataset.src ? [object] : []; },
    addEventListener(event, listener) { assert.equal(event,'toggle'); bindings++; this.toggle=listener; }}));
  const doc = {querySelectorAll: () => regions};
  initRegions(doc); assert.equal(loads,1); assert.equal(bindings,2);
  initRegions(doc); assert.equal(loads,1); assert.equal(bindings,2);
  regions[1].open=true; regions[1].toggle(); assert.equal(loads,2);
  regions[1].open=false; regions[1].toggle();
  regions[1].open=true; regions[1].toggle(); assert.equal(loads,2);
});
test('regional fragment opens its own group and ignores other or malformed anchors', () => {
  const {revealRegion} = require('../docs/assets/acupoint-atlas/explorer.js');
  const region={open:false,matches:s=>s==='details.acupoint-region',querySelectorAll:()=>[]};
  const doc={defaultView:{location:{hash:'#visual-head'}},getElementById:id=>id==='visual-head'?{nextElementSibling:region}:null};
  revealRegion(doc); assert.equal(region.open,true);
  region.open=false;
  doc.getElementById=id=>id==='visual-head'?{parentElement:{tagName:'P',nextElementSibling:region}}:null;
  revealRegion(doc); assert.equal(region.open,true);
  for (const hash of ['#find-points','#%invalid','#visual-missing','']) {
    region.open=false;doc.defaultView.location.hash=hash;revealRegion(doc);assert.equal(region.open,false);
  }
});
test('all diagrams have ordinary links and image fallbacks without JavaScript', () => {
  const doc=fs.readFileSync(path.join(__dirname,'../docs/acupoint-network/standard-atlas.md'),'utf8');
  const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/acupoint_diagrams.json'),'utf8'));
  const sources=[...doc.matchAll(/<object data-src="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(sources.length,manifest.regions.length);
  assert.equal((doc.match(/<noscript><img /g)||[]).length,sources.length);
  for (const source of sources) assert.ok(doc.includes('href="'+source+'"'));
});
