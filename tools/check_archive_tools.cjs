/* Browser acceptance checks against the actual generated archive. */
const {chromium} = require('playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const base = process.env.ARCHIVE_TEST_BASE || 'http://127.0.0.1:8766';

(async () => {
  fs.mkdirSync('archive-browser-results', {recursive: true});
  const browser = await chromium.launch({headless: true});
  try {
    for (const [name, viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1440,height:1000}]]) {
      const context = await browser.newContext({viewport}); const page = await context.newPage(); const errors=[];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(base + '/herbal-integrated/formula-structure/');
      const compare = page.locator('[data-archive-compare]');
      await compare.getByRole('button',{name:'사군자탕',exact:true}).click();
      await compare.getByRole('button',{name:'육군자탕',exact:true}).click();
      await compare.getByRole('table').waitFor();
      assert.equal(await compare.locator('thead th').count(),3);
      assert.ok((await compare.locator('table').innerText()).includes('반하'));
      assert.ok(new URL(page.url()).searchParams.get('compare').includes('formula-sijunzi-tang'));
      await page.reload();
      await compare.getByRole('table').waitFor();
      await page.screenshot({path:`archive-browser-results/${name}-comparison.png`,fullPage:false});
      await compare.getByRole('button',{name:'선택 초기화',exact:true}).click();
      assert.equal(new URL(page.url()).searchParams.has('compare'),false);
      await page.goto(base + '/herbal-integrated/herb-comparisons/');
      const herb = page.locator('[data-archive-compare]');
      await herb.getByRole('searchbox').fill('인삼');
      await herb.getByRole('button',{name:/^인삼/}).first().click();
      assert.ok((await herb.locator('table').innerText()).includes('성미'));
      await page.goto(base + '/search-guide/');
      const finder = page.locator('[data-archive-finder]');
      await finder.getByRole('searchbox').fill('사군자탕');
      await finder.getByRole('button',{name:'근거 자료 찾기'}).click();
      await finder.locator('article').first().waitFor({timeout:60000});
      assert.ok((await finder.locator('article').first().innerText()).includes('사군자탕'));
      assert.ok((await finder.innerText()).includes('AI 생성 답변이 아닙니다'));
      await finder.getByText('AI에 보낼 질문과 발췌 확인').click();
      assert.ok((await finder.locator('pre').innerText()).includes('https://wiki.minseong.co.kr'));
      await page.screenshot({path:`archive-browser-results/${name}-search.png`,fullPage:false});
      await page.goto(base + '/learning/?subject=formulas');
      const room = page.locator('[data-learning-room]');
      await room.getByLabel('학습 방식').selectOption('quiz');
      await room.getByRole('button',{name:'10문제 풀기',exact:true}).click();
      await room.locator('[data-option]').first().click();
      await room.locator('.learning-feedback').waitFor();
      const attempts = await page.evaluate(() => JSON.parse(localStorage.getItem('minseong-learning-v1')).attempts);
      assert.equal(attempts,1);
      await page.reload();
      await room.getByRole('button',{name:/풀던 문제 이어하기/}).click();
      await room.locator('.learning-feedback').waitFor();
      assert.equal(await page.evaluate(() => JSON.parse(localStorage.getItem('minseong-learning-v1')).attempts),1);
      await room.getByRole('button',{name:'다음 문제 →',exact:true}).click();
      assert.ok((await room.innerText()).includes('2 / 10'));
      const downloadWait = page.waitForEvent('download');
      await room.getByRole('button',{name:'학습기록 내보내기'}).click();
      const download = await downloadWait; const backupPath=`archive-browser-results/${name}-backup.json`; await download.saveAs(backupPath);
      const backup=JSON.parse(fs.readFileSync(backupPath,'utf8')); assert.equal(backup.format,'minseong-learning'); assert.equal(backup.progress.resume.index,1);
      page.on('dialog',dialog=>dialog.accept());
      await room.getByRole('button',{name:'학습기록 초기화',exact:true}).click();
      await room.getByLabel('학습기록 파일 가져오기').setInputFiles(backupPath);
      await page.waitForFunction(()=>JSON.parse(localStorage.getItem('minseong-learning-v1')).attempts===1);
      await page.reload();
      await room.getByRole('button',{name:/풀던 문제 이어하기/}).click();
      assert.ok((await room.innerText()).includes('2 / 10'));
      await page.screenshot({path:`archive-browser-results/${name}-study.png`,fullPage:false});
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2); assert.equal(overflow,false,'page must fit viewport');
      assert.deepEqual(errors,[]); await context.close();
    }
  } finally {await browser.close();}
  console.log('Archive browser checks passed: comparison, herb search, passage search, resume, export/import; mobile and desktop.');
})().catch(error=>{console.error(error);process.exitCode=1;});
