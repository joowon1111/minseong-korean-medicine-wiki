const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.ARCHIVE_TEST_BASE||'http://127.0.0.1:8766';
const source={id:'S1',title:'사군자탕',heading:'구성',url:'/formulas/sijunzi-tang/',text:'사군자탕은 인삼 백출 복령 감초로 구성된다.'};
const answer={schema:1,sufficient:true,paragraphs:[{text:'사군자탕은 인삼·백출·복령·감초로 구성됩니다. <img src=x onerror=alert(1)>',source_ids:['S1']}],quotes:[{source_id:'S1',quote:source.text}],limitations:'발췌에 없는 용량은 확인할 수 없습니다.',sources:[source]};

(async()=>{
  fs.mkdirSync('archive-browser-results',{recursive:true}); const browser=await chromium.launch({headless:true});
  try {for (const [name,viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1440,height:1000}]]) {
    const context=await browser.newContext({viewport}), page=await context.newPage(), errors=[], calls=[]; let mode='success', pending;
    page.on('pageerror',e=>errors.push(e.message));
    await page.route('**/assets/archive-tools/ai-config.json',route=>route.fulfill({json:{schema:1,endpoint:'https://archive-ai.example'}}));
    await page.route('https://archive-ai.example/**',async route=>{
      const req=route.request(); if (req.method()==='OPTIONS') return route.fulfill({status:204,headers:{'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'POST, GET, OPTIONS','Access-Control-Allow-Headers':'Content-Type'}});
      const headers={'Access-Control-Allow-Origin':'*'};
      if (req.url().endsWith('/health')) return route.fulfill({headers,json:{schema:1,ready:true,provider:'OpenAI',archive:'https://wiki.minseong.co.kr'}});
      calls.push(req.postDataJSON());
      if (mode==='pending') {pending=route; return;}
      if (mode==='rate') return route.fulfill({status:429,headers,json:{error:'rate_limited'}});
      return route.fulfill({headers,json:mode==='invalid' ? {...answer,quotes:[]} : mode==='insufficient' ? {schema:1,sufficient:false,paragraphs:[],quotes:[],sources:[],limitations:'해당 질문을 뒷받침하는 자료가 부족합니다.'} : answer});
    });
    await page.goto(base+'/search-guide/'); const finder=page.locator('[data-archive-finder]');
    await finder.getByRole('searchbox').fill('사군자탕'); await finder.getByRole('button',{name:'근거 자료 찾기'}).click();
    const ai=finder.locator('.archive-ai'), generate=ai.getByRole('button',{name:'출처 기반 AI 답변 생성'});
    await generate.waitFor(); await page.waitForFunction(()=>!document.querySelector('.archive-ai button').disabled);
    assert.equal(calls.length,0,'search must not call AI');
    await generate.click(); await ai.getByText('AI 생성 답변 · 각 문단의 출처와 실제 발췌를 확인하세요.').waitFor();
    assert.deepEqual(calls[0],{question:'사군자탕',kind:''}); assert.equal(await ai.locator('img').count(),0);
    assert.equal(await ai.getByRole('link',{name:'[S1]',exact:true}).getAttribute('href'),source.url);
    await ai.locator('summary').click(); assert.equal(await ai.locator('blockquote').innerText(),source.text);
    await ai.scrollIntoViewIfNeeded(); await page.screenshot({path:`archive-browser-results/${name}-ai-answer.png`});
    mode='invalid'; await generate.click(); await ai.getByText(/답변의 인용을 검증하지 못했습니다/).waitFor(); assert.equal(await ai.locator('blockquote').count(),0);
    mode='rate'; await generate.click(); await ai.getByText(/1분 뒤 다시 시도하세요/).waitFor();
    mode='insufficient'; await generate.click(); await ai.getByText('자료가 부족해 질문 전체에 답할 수 없습니다.').waitFor();
    mode='pending'; await generate.click(); await ai.getByRole('button',{name:'생성 취소'}).click(); await ai.getByText('답변 생성을 취소했습니다.').waitFor();
    if (pending) {await pending.abort().catch(()=>{}); pending=null;}
    mode='success'; await generate.click(); await ai.getByText(/AI 생성 답변 ·/).waitFor();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false); assert.deepEqual(errors,[]);
    await context.close();
    const offline=await browser.newContext({viewport}), offlinePage=await offline.newPage();
    await offlinePage.route('**/assets/archive-tools/ai-config.json',r=>r.fulfill({json:{schema:1,endpoint:null}}));
    await offlinePage.goto(base+'/search-guide/?q=사군자탕'); const unavailable=offlinePage.locator('.archive-ai');
    await offlinePage.locator('[data-archive-finder] article').first().waitFor({timeout:60000});
    assert.equal(await unavailable.count(),0);
    assert.equal((await offlinePage.locator('[data-archive-finder]').innerText()).includes('AI 서버 연결을 준비'),false); await offline.close();
  }} finally {await browser.close();}
  console.log('Archive AI browser checks passed: source rendering, escaped text, no automatic submission, failures, retry, cancellation and unavailable server; mobile and desktop.');
})().catch(error=>{console.error(error);process.exitCode=1;});
