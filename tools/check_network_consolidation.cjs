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
   for(const hash of ['',legacy?'#'+encodeURIComponent(legacy):'']) {
    const expected=targetParts(route.anchors[decodeURIComponent(hash.slice(1))]||route.target);
    await page.goto(base+pathname(source)+hash,{waitUntil:'networkidle'});
    await page.waitForURL(url=>url.pathname===expected.path && url.hash===expected.hash);
    assert(await page.locator('.md-content h1').isVisible(),source+' must reach readable content');
    if(expected.hash) assert.equal(await page.locator('[id]').evaluateAll((nodes,id)=>nodes.filter(n=>n.id===id).length,decodeURIComponent(expected.hash.slice(1))),1,source+' section must exist');
    checked++;
   }
  }
  for(const width of [320,1440]) {
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/network/condition-expansion-map/#_4',{waitUntil:'networkidle'});
   assert.match(await page.locator('#_4').textContent(),/호흡기/);
   assert(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'No page overflow at '+width);
   const links=await page.locator('.md-nav--primary a[href]').evaluateAll(nodes=>nodes.map(n=>new URL(n.href).pathname));
   for(const old of Object.keys(routes)) assert(!links.includes(pathname(old)),old+' removed from menu');
   for(const current of ['condition-expansion-map','formula-composition-hub','herb-to-formula-map','recovery-map']) assert(links.includes('/network/'+current+'/'),current+' remains discoverable');
   await page.screenshot({path:`archive-browser-results/network-consolidation-${width}.png`});
  }
  console.log(`Network consolidation: ${checked} legacy URL/anchor navigations; 320/1440px content and menus passed.`);
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
