/* Browser acceptance: serve site/ first, then BASE_URL=http://127.0.0.1:8767 node tools/check_solar_terms.cjs. */
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://127.0.0.1:8767';
const launch=process.env.PLAYWRIGHT_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_EXECUTABLE_PATH}:{};
(async()=>{
 const browser=await chromium.launch({headless:true,...launch});
 try{
  for(const [device,viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1440,height:1000}]]){
   const page=await browser.newPage({viewport}),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.clock.setFixedTime(new Date('2026-11-01T00:00:00Z'));
   await page.goto(base+'/daily-korean-medicine/solar-terms/#solar-calculator');
   const widget=page.locator('[data-solar-term-calculator]');
   const status=widget.locator('[data-solar-status]'),input=widget.locator('[data-solar-year]');
   const yearReady=async year=>{await status.filter({hasText:year+'년 절기 24개를 계산했습니다.'}).waitFor();assert.equal(await widget.locator('tbody tr').count(),24);};
   const run=async year=>{await input.fill(String(year));await widget.locator('[type=submit]').click();await yearReady(year);};
   const ipdong=widget.locator('tbody tr').filter({hasText:'입동('});
   await yearReady(2027);assert.equal(await input.inputValue(),'2027');
   assert.match(await ipdong.innerText(),/2027-11-08\s+00:39\s+225°/);
   await widget.locator('[data-solar-seconds]').check();assert.match(await ipdong.innerText(),/00:38:34/);
   await widget.locator('[data-solar-seconds]').uncheck();
   await run(2026);assert.match(await ipdong.innerText(),/2026-11-07\s+18:52/);
   await widget.locator('[data-solar-step="1"]').click();await yearReady(2027);
   assert.equal(new URL(page.url()).searchParams.get('solarYear'),'2027');
   await widget.locator('[data-solar-step="-1"]').click();await yearReady(2026);
   await widget.locator('[data-solar-next-year]').click();await yearReady(2027);
   await run(1900);assert(await widget.locator('[data-solar-step="-1"]').isDisabled());
   await run(2100);assert(await widget.locator('[data-solar-step="1"]').isDisabled());
   await input.fill('2101');await widget.locator('[type=submit]').click();assert(await input.evaluate(el=>el.validity.rangeOverflow));
   assert.match(await widget.locator('caption').innerText(),/2100년/);
   await run(2027);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'page horizontal overflow');
   await page.locator('#solar-calculator').scrollIntoViewIfNeeded();
   if(process.env.SOLAR_SCREENSHOT_DIR)await page.screenshot({path:process.env.SOLAR_SCREENSHOT_DIR+'/solar-calculator-'+device+'.png'});
   await ipdong.locator('a').click();assert.equal(new URL(page.url()).hash,'#ipdong');await page.locator('#ipdong').waitFor();
   await page.goto(base+'/daily-korean-medicine/solar-terms/?solarYear=2028#solar-calculator');await yearReady(2028);
   assert.match(await ipdong.innerText(),/2028-11-07\s+06:27/);
   await page.goto(base+'/daily-korean-medicine/');
   assert.equal(await page.locator('script[src*="solar-terms/calculator"]').count(),0,'assets leaked into other article');
   assert.deepEqual(errors,[]);await page.close();console.log(device+': year controls, seconds, bounds, query, story links and overflow PASS');
  }
  // A failed data request must offer the requested official year, and retry successfully.
  const page=await browser.newPage();let fail=true;
  await page.route('**/de440/2030.json*',route=>fail?route.abort():route.continue());
  await page.goto(base+'/daily-korean-medicine/solar-terms/?solarYear=2031#solar-calculator');
  const widget=page.locator('[data-solar-term-calculator]');
  await widget.locator('[data-solar-status]').filter({hasText:'계산 자료를 확인할 수 없습니다.'}).waitFor();
  assert.match(await widget.locator('[data-solar-official]').getAttribute('href'),/search_year=2031$/);
  fail=false;await widget.locator('[type=submit]').click();
  await widget.locator('[data-solar-status]').filter({hasText:'2031년 절기 24개를 계산했습니다.'}).waitFor();
  assert.equal(await widget.locator('tbody tr').count(),24);await page.close();
  console.log('failed request: year-matched official fallback and retry PASS');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
