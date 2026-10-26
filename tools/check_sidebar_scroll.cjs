/* Long menus must expose a clickable final item at every responsive breakpoint. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.ARCHIVE_TEST_BASE||'http://127.0.0.1:8766';
// Reduced CSS viewports + device scale model layout under display scaling;
// these are not a claim of testing Windows browser zoom UI.
const cases=[['desktop',1440,900,1],['short-desktop',1280,360,1],['desktop-edge',1220,500,1],['drawer-edge',1219,500,1],['scaled-125',1536,864,1.25],['scaled-150',1280,720,1.5],['scaled-200',960,540,2],['tablet',768,384,1],['phone',390,844,1],['landscape',844,390,1]];
(async()=>{
 fs.mkdirSync('archive-browser-results',{recursive:true});
 const browser=await chromium.launch({headless:true});
 try{
  // The clinic's five core symptoms must be reachable in the first menu group.
  for(const width of [390,1440]){
   const page=await browser.newPage({viewport:{width,height:900}});
   await page.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
   await page.goto(base+'/autonomic/',{waitUntil:'domcontentloaded'});
   if(width<1220)await page.locator('header label[for="__drawer"]').click();
   const entry=page.locator('.md-sidebar--primary').getByRole('link',{name:'자율신경·스트레스',exact:true});
   await entry.waitFor({state:'visible'});
   const position=await entry.evaluate(a=>{
    const group=a.closest('li.md-nav__item'),r=a.getBoundingClientRect();
    return {first:group===group.parentElement.firstElementChild,top:r.top,bottom:r.bottom,links:[...group.querySelectorAll('a[href]')].map(a=>new URL(a.href).pathname)};
   });
   assert(position.first,'Autonomic must be the first symptoms menu group at '+width);
   assert(position.top>=0&&position.bottom<900,'Autonomic entry must be visible without scrolling at '+width);
   for(const name of ['chronic-fatigue','functional-dyspepsia','palpitation','headache','insomnia']){
    assert(position.links.includes('/conditions/'+name+'/'),'Core symptom must be in the promoted group: '+name);
    const link=page.locator('.md-sidebar--primary').getByRole('link',{name:'자율신경·스트레스',exact:true}).locator('xpath=ancestor::li[1]').locator('a[href$="/conditions/'+name+'/"]');
    assert(await link.isVisible(),'Core symptom must be visible in the open group: '+name);
   }
   await page.screenshot({path:`archive-browser-results/autonomic-menu-priority-${width}.png`});
   await page.close();
  }
  for(const [name,width,height,deviceScaleFactor] of cases){
   const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor});
   // External font/analytics latency must not determine menu geometry tests.
   await page.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
   await page.goto(base+'/conditions/low-back-pain/',{waitUntil:'domcontentloaded'});
   await page.locator('.md-sidebar--primary').waitFor({state:'attached'});
   await page.setViewportSize({width,height});
   await page.waitForTimeout(200);
   if(width<1220)await page.locator('header label[for="__drawer"]').click();
   await page.waitForTimeout(300);
   const position=await page.evaluate(()=>{
    const sidebar=document.querySelector('.md-sidebar--primary'),r=sidebar.getBoundingClientRect();
    const x=r.left+r.width/2,y=Math.min(innerHeight-30,Math.max(r.top+160,innerHeight/2));
    let e=document.elementFromPoint(x,y);
    while(e&&!(getComputedStyle(e).overflowY==='auto'&&e.scrollHeight>e.clientHeight+2))e=e.parentElement;
    if(!e)throw Error('No visible scrolling menu at pointer');
    e.setAttribute('data-scroll-test','active');
    return{x,y};
   });
   const menu=page.locator('[data-scroll-test="active"]');
   const bodyY=await page.evaluate(()=>scrollY);
   await page.mouse.move(position.x,position.y);
   for(let i=0;i<4;i++){await page.mouse.wheel(0,6000);await page.waitForTimeout(100)}
   const last=await menu.evaluate(e=>{
    const r=e.getBoundingClientRect();
    const links=[...e.querySelectorAll('a[href]')].filter(a=>{const q=a.getBoundingClientRect();return q.width&&q.height&&q.left>=r.left-1&&q.right<=r.right+1});
    const a=links.sort((a,b)=>a.getBoundingClientRect().bottom-b.getBoundingClientRect().bottom).at(-1);
    if(!a)throw Error('No final link');
    const q=a.getBoundingClientRect(),hit=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2);
    a.setAttribute('data-scroll-test-link','last');
    return {text:a.textContent.trim(),href:a.href,top:q.top,bottom:q.bottom,edge:Math.min(r.bottom,innerHeight),atEnd:e.scrollTop+e.clientHeight>=e.scrollHeight-2,clickable:!!hit&&(hit===a||a.contains(hit))};
   });
   assert(last.atEnd,name+': wheel must reach scroll end');
   assert(last.bottom<=last.edge-10,name+': final link needs bottom breathing room');
   assert(last.top>=0&&last.clickable,name+': final link must be visible and hit-testable');
   assert.equal(await page.evaluate(()=>scrollY),bodyY,name+': wheel must not spill into article');
   // Native focus scrolling must also expose the final item after resetting the menu.
   await menu.evaluate(e=>{e.scrollTop=0});
   await page.locator('[data-scroll-test-link="last"]').focus();
   await page.waitForTimeout(100);
   assert(await page.locator('[data-scroll-test-link="last"]').evaluate(a=>{const q=a.getBoundingClientRect();return q.top>=0&&q.bottom<=innerHeight}),name+': keyboard focus must reveal final item');
   await page.screenshot({path:`archive-browser-results/sidebar-${name}.png`});
   await page.locator('[data-scroll-test-link="last"]').click();
   await page.waitForURL(last.href);
   await page.locator('article').waitFor({state:'visible'});
   console.log(name+': final menu link reachable — '+last.text);
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
