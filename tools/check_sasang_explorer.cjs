/* Verify the integrated explorer with the same browser used by archive CI. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.ARCHIVE_TEST_BASE||'http://127.0.0.1:8766';
(async()=>{
 fs.mkdirSync('archive-browser-results',{recursive:true});
 const browser=await chromium.launch({headless:true});
 try{
  for(const [name,viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1440,height:1000}]]){
   const page=await browser.newPage({viewport}),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/sasang-explorer/');
   const frame=page.frameLocator('#sasang-explorer-frame');
   await frame.locator('[data-c="소양인"]').waitFor();
   assert(!(await frame.locator('body').innerText()).includes('民成'));
   await page.screenshot({path:`archive-browser-results/${name}-sasang-start.png`});
   for(const c of ['소양인','태음인','소음인','태양인']){
    await frame.locator('[data-c="'+c+'"]').click();
    const count=await frame.locator('[data-axis]').count();
    assert.equal(count,c==='태양인'?2:8);
    await frame.locator('#search').fill('no-matching-pattern-xyz');
    assert.equal(await frame.locator('[data-axis]').count(),0);
    await frame.locator('#search').fill('');
    await frame.locator('[data-axis]').first().click();
    assert.match(await frame.locator('#content').innerText(),/감별 포인트/);
    await frame.locator('[data-next]').click();
    assert(await frame.locator('#content .formula').count()>0);
    for(const tab of ['constitution','patterns','formulas','food','living','clinic']){
     await frame.locator('[data-tab="'+tab+'"]').click();
     assert(await frame.locator('.profile-body').isVisible());
     assert(await frame.locator('body').evaluate(e=>e.scrollWidth<=window.innerWidth+1));
    }
    assert.match(await frame.locator('.profile-body').innerText(),/한약을 복용해야 하는 것은 아닙니다/);
    await frame.locator('[data-tab="food"]').click();
    await page.waitForFunction(()=>location.hash.includes('t=food'));
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    await page.screenshot({path:`archive-browser-results/${name}-sasang-${c}-food.png`});
    await page.reload();
    await frame.locator('[data-tab="food"][aria-pressed="true"]').waitFor();
    assert.match(await frame.locator('#trail').innerText(),new RegExp(c));
    await page.waitForFunction(()=>{const f=document.getElementById('sasang-explorer-frame');return f.getBoundingClientRect().height>=f.contentDocument.body.getBoundingClientRect().height-5});
    const iframeHeight=await page.locator('#sasang-explorer-frame').evaluate(e=>e.getBoundingClientRect().height);
    const bodyHeight=await frame.locator('body').evaluate(e=>e.getBoundingClientRect().height);
    assert(iframeHeight>=bodyHeight-5,'frame must fit the document');
    await frame.locator('#reset').click();
    await frame.locator('[data-c="소양인"]').waitFor();
   }
   assert.deepEqual(errors,[]);await page.close();
  }
  console.log('Sasang explorer: mobile/desktop navigation, six tabs, filtering, URL restore, frame size and overflow passed.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
