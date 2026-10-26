/* Test retired URL navigation and the retained network menu against the build. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const routes = JSON.parse(fs.readFileSync('tools/network_consolidations.json', 'utf8'));
const base = process.env.ARCHIVE_TEST_BASE || 'http://127.0.0.1:8766';
const pathname = source => '/' + (source.endsWith('/index.md') ? source.slice(0,-8) : source.slice(0,-3) + '/');
function targetParts(target) {const [source,hash=''] = target.split('#');return {path:pathname(source),hash:hash?'#'+encodeURIComponent(hash):''};}
(async()=>{
 const browser=await chromium.launch({headless:true});
 fs.mkdirSync('archive-browser-results',{recursive:true});
 try {
  const page=await browser.newPage({viewport:{width:390,height:844}});
  page.setDefaultTimeout(15000);
  await page.route('**/*',async route=>{
   const url=new URL(route.request().url());
   if(url.origin===new URL(base).origin) return route.continue();
   if(url.origin==='https://wiki.minseong.co.kr') {
    const response=await route.fetch({url:base+url.pathname+url.search});
    return route.fulfill({response});
   }
   return route.abort();
  });
  let checked=0;
  for(const [source,route] of Object.entries(routes)) {
   const legacy=Object.keys(route.anchors).at(-1);
   const fragments=source.includes('facial-palsy')||source.includes('bell-palsy-acute-acupuncture')||['authority/conditions/functional-dyspepsia.md','authority/conditions/anxiety.md','authority/conditions/insomnia.md','conditions/anxiety-somatic.md','conditions/stress-palpitations-digestion.md','tonic-masterpieces/deer-antler/quality-parts.md'].includes(source)
    ? ['',...Object.keys(route.anchors).map(id=>'#'+encodeURIComponent(id)),'#unknown-fragment']
    : ['',legacy?'#'+encodeURIComponent(legacy):''];
   for(const hash of fragments) {
    const expected=targetParts(route.anchors[decodeURIComponent(hash.slice(1))]||route.target);
    await page.goto(base+pathname(source)+hash,{waitUntil:'domcontentloaded'});
    await page.waitForURL(url=>url.pathname===expected.path && url.hash===expected.hash,{waitUntil:'domcontentloaded'});
    await page.locator('.md-content h1').waitFor();
    assert(await page.locator('.md-content h1').isVisible(),source+' must reach readable content');
    if(expected.hash) assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,decodeURIComponent(expected.hash.slice(1))),1,source+' section must exist');
    checked++;
   }
  }
  for(const width of [320,1440]) {
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/network/condition-expansion-map/#_4',{waitUntil:'domcontentloaded'});
   assert.match(await page.locator('#_4').textContent(),/호흡기/);
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'No page overflow at '+width);
   const links=await page.locator('.md-nav--primary a[href]').evaluateAll(nodes=>nodes.map(n=>new URL(n.href).pathname));
   for(const old of Object.keys(routes)) assert(!links.includes(pathname(old)),old+' removed from menu');
   assert(links.includes('/network/condition-expansion-map/'),'Current clinical map remains in its active menu branch');
   await page.evaluate(()=>document.fonts.ready);
   await page.screenshot({path:`archive-browser-results/network-consolidation-${width}.png`});
   // Material prunes inactive menu branches. Exercise the actual entry links,
   // then verify each destination's own active branch instead of assuming it is open.
   for(const current of ['formula-composition-hub','herb-to-formula-map','recovery-map']) {
    await page.goto(base+'/network/',{waitUntil:'domcontentloaded'});
    const link=page.locator('.md-content a').filter({hasText:current==='formula-composition-hub'?'처방 구성 네트워크':current==='herb-to-formula-map'?'본초→방제 역탐색':'피로·회복'}).first();
    await link.click();
    await page.waitForURL(url=>url.pathname==='/network/'+current+'/',{waitUntil:'domcontentloaded'});
    await page.locator('.md-content h1').waitFor();
    assert(await page.locator('.md-nav--primary a[href]').evaluateAll((nodes,path)=>nodes.some(n=>new URL(n.href).pathname===path),'/network/'+current+'/'),current+' appears in its active menu');
    assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),current+' fits at '+width);
   }
   await page.screenshot({path:`archive-browser-results/network-destination-${width}.png`});
  }
  for(const width of [320,1440]) {
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/conditions/facial-palsy/',{waitUntil:'domcontentloaded'});
   for(const id of ['acute-treatment','eye-protection','facial-pattern-treatment','facial-acute-acupuncture-2025','facial-ea-2026','facial-synkinesis','_6','_7','_8'])
    assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,id),1,'Facial palsy section '+id);
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'Facial palsy fits at '+width);
   await page.screenshot({path:`archive-browser-results/facial-palsy-${width}.png`});
  }
  console.log(`Network consolidation: ${checked} legacy URL/anchor navigations; 320/1440px content and menus passed.`);
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
