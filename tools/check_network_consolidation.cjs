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
   const fragments=source.startsWith('autonomic/')||source.startsWith('sasang/')||source.includes('facial-palsy')||source.includes('bell-palsy-acute-acupuncture')||['authority/conditions/functional-dyspepsia.md','authority/conditions/anxiety.md','authority/conditions/insomnia.md','conditions/anxiety-somatic.md','conditions/stress-palpitations-digestion.md','tonic-masterpieces/deer-antler/quality-parts.md'].includes(source)
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
   await page.waitForURL(url=>url.pathname==='/network/condition-to-treatment-map/'&&url.hash==='#respiratory');
   assert.match(await page.locator('#respiratory').textContent(),/호흡기/);
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'No page overflow at '+width);
   const links=await page.locator('.md-nav--primary a[href]').evaluateAll(nodes=>nodes.map(n=>new URL(n.href).pathname));
   for(const old of Object.keys(routes)) assert(!links.includes(pathname(old)),old+' removed from menu');
   assert(links.includes('/network/condition-to-treatment-map/'),'Current clinical map remains in its active menu branch');
   await page.evaluate(()=>document.fonts.ready);
   await page.screenshot({path:`archive-browser-results/network-consolidation-${width}.png`});
   // Material prunes inactive menu branches. Exercise the actual entry links,
   // then verify each destination's own active branch instead of assuming it is open.
   for(const current of ['formula-composition-hub','herb-to-formula-map','recovery-map']) {
    await page.goto(base+'/network/',{waitUntil:'domcontentloaded'});
    const link=page.locator(`.md-content a[href*='${current}/']`).first();
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
   await page.goto(base+'/classical-stories/',{waitUntil:'domcontentloaded'});
   const labels=await page.locator('.md-nav--primary > .md-nav__list > .md-nav__item').evaluateAll(nodes=>nodes.map(n=>n.textContent.trim()));
   assert(labels[0].startsWith('홈')&&labels[1].startsWith('민성의담'),'Uidam must be independent immediately after Home');
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'Uidam fits '+width);
   await page.screenshot({path:`archive-browser-results/uidam-navigation-${width}.png`});
   await page.goto(base+'/conditions/facial-palsy/',{waitUntil:'domcontentloaded'});
   for(const id of ['acute-treatment','eye-protection','facial-pattern-treatment','facial-acute-acupuncture-2025','facial-ea-2026','facial-synkinesis','_6','_7','_8'])
    assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,id),1,'Facial palsy section '+id);
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'Facial palsy fits at '+width);
   await page.screenshot({path:`archive-browser-results/facial-palsy-${width}.png`});
  }
  for(const width of [320,1440]) {
   await page.setViewportSize({width,height:900});
   for(const [name,entry,legacy] of [['sweating','sweat-patterns','taeeumin-sweat'],['cold-heat','cold-heat-patterns','soyangin-heat-cold']]) {
    await page.goto(base+'/sasang/',{waitUntil:'domcontentloaded'});
    await page.locator(`.md-content a[href*="sasang-original-symptoms/${name}/#${entry}"]`).first().click();
    await page.waitForURL(url=>url.pathname===`/sasang-original-symptoms/${name}/`&&url.hash==='#'+entry);
    for(const id of [entry,legacy,'_1','_2','related-reading'])
     assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,id),1,name+' retained anchor '+id);
    assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),name+' fits at '+width);
    await page.screenshot({path:`archive-browser-results/sasang-${name}-${width}.png`});
   }
  }
  for(const width of [320,1440]) {
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/autonomic/#five-core-symptoms',{waitUntil:'domcontentloaded'});
   const core=[['chronic-fatigue','stress-recovery'],['functional-dyspepsia','stress-five-core'],['palpitation','stress-five-core'],['headache','stress-five-core'],['insomnia','stress-five-core']];
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'Autonomic core table fits '+width);
   await page.screenshot({path:`archive-browser-results/autonomic-five-core-${width}.png`});
   for(const [name,id] of core) {
    await page.goto(base+'/autonomic/#five-core-symptoms',{waitUntil:'domcontentloaded'});
    await page.locator(`.md-content a[href*="conditions/${name}/#${id}"]`).first().click();
    await page.waitForURL(url=>url.pathname===`/conditions/${name}/`&&url.hash==='#'+id);
    assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,id),1,name+' core anchor');
    assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),name+' fits '+width);
   }
  }
  console.log(`Network consolidation: ${checked} legacy URL/anchor navigations; 320/1440px content and menus passed.`);
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
