/* Acceptance checks for actual WebGL rendering, archive navigation and graceful failure. */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
const base=process.env.ARCHIVE_TEST_BASE||'http://127.0.0.1:8766';
(async()=>{
  fs.mkdirSync('archive-browser-results',{recursive:true});
  const browser=await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try{
    for(const [name,viewport] of [['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}]]){
      const context=await browser.newContext({viewport,reducedMotion:'reduce'}),page=await context.newPage(),errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      let heavy=0;page.on('request',r=>{if(r.url().includes('/acupoint-3d/model.json'))heavy++;});
      await page.goto(base+'/acupoint-network/3d-map/');
      assert.equal(heavy,0,'geometry must not load before starting the map');
      await page.locator('[data-map-start]').click();
      const frame=page.frameLocator('[data-map-frame]');
      await frame.locator('#detail .code').filter({hasText:'ST36'}).waitFor({timeout:30000});
      const iframe=page.frames().find(f=>f.url().includes('/assets/acupoint-3d/index.html'));
      assert(await iframe.evaluate(()=>!!window.__acu));assert.equal(heavy,1);
      await frame.locator('#q').fill('合谷');
      await frame.locator('#results button').first().click();
      await frame.locator('#detail .code').filter({hasText:'LI4'}).waitFor();
      await page.waitForURL(url=>url.searchParams.get('point')==='LI4');
      assert((await frame.locator('[data-archive-link]').getAttribute('href')).includes('/li4-hegu/'));
      await frame.locator('#chips [data-m="LI"]').click();
      assert.equal(await frame.locator('#list button').count(),20);
      await frame.locator('#tBones').click();await frame.locator('#tMuscle').click();
      assert(await iframe.evaluate(()=>window.__acu.state.bones&&window.__acu.state.muscle));
      await frame.locator('#tBones').click();await frame.locator('#tMuscle').click();
      await frame.locator('#detail [data-focus]').click();
      await iframe.waitForFunction(()=>window.__acu.cam.dist<60);
      await iframe.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('unavailable'))}}));
      await frame.locator('#share-point').click();
      await frame.locator('#share-fallback').waitFor({state:'visible'});
      assert.equal(new URL(await frame.locator('#share-fallback').inputValue()).searchParams.get('point'),'LI4');
      await page.screenshot({path:`archive-browser-results/${name}-3d-point.png`});
      await frame.locator('#today-point').click();
      const expected=await iframe.evaluate(async()=>{
        const j=await (await fetch('/assets/daily-korean-medicine/data.json')).json(),now=new Date(Date.now()+9*60*60*1000);
        const day=Math.floor((Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate())-Date.UTC(now.getUTCFullYear(),0,1))/86400000);
        return j.points[day%j.points.length].code;
      });
      assert.equal(await frame.locator('#detail .code').innerText(),expected);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      assert(await iframe.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      await page.goto(base+'/acupoint-network/3d-map/?point=KI3');
      await page.frameLocator('[data-map-frame]').locator('#detail .code').filter({hasText:'KI3'}).waitFor({timeout:30000});
      await page.goto(base+'/assets/acupoint-3d/index.html?point=not-a-point');
      await page.locator('#detail .code').filter({hasText:'ST36'}).waitFor();
      const angle=await page.evaluate(()=>window.__acu.cam.theta),box=await page.locator('#gl').boundingBox();
      await page.mouse.move(box.x+box.width*.4,box.y+box.height*.4);await page.mouse.down();await page.mouse.move(box.x+box.width*.55,box.y+box.height*.4,{steps:5});await page.mouse.up();
      assert.notEqual(await page.evaluate(()=>window.__acu.cam.theta),angle);
      await page.locator('#q').fill('missing-no-such-point');assert.equal(await page.locator('#results button').count(),0);
      assert.deepEqual(errors,[]);
      await context.close();
    }
    const page=await browser.newPage();
    await page.route('**/acupoint-3d/model.json',route=>route.abort());
    await page.goto(base+'/assets/acupoint-3d/index.html');
    await page.locator('#loading a').filter({hasText:'2D 경혈 아틀라스'}).waitFor();
    assert.equal(await page.locator('#loading a').getAttribute('href'),'/acupoint-network/standard-atlas/');
    console.log('3D map: mobile/desktop WebGL, lazy assets, search, filters, layers, permalinks, daily point, layout and fallback passed.');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
