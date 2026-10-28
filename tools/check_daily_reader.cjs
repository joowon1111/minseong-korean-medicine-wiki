/* Daily reader acceptance checks against the generated archive. */
const {chromium} = require('playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const base = process.env.ARCHIVE_TEST_BASE || 'http://127.0.0.1:8766';

(async () => {
  fs.mkdirSync('archive-browser-results', {recursive:true});
  const browser = await chromium.launch({headless:true});
  try {
    for (const [name,viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1440,height:1000}]]) {
      const context = await browser.newContext({viewport});
      const page = await context.newPage(), errors = [];
      // The home fallback is static; successful hydration must use the KST date.
      await page.clock.install({time:new Date('2026-10-13T14:59:00Z')});
      await page.goto(base+'/');
      await page.locator('[data-topic-date][datetime="2026-10-13"]').waitFor();
      await page.locator('[data-yangsheng-date][datetime="2026-10-13"]').waitFor();
      assert.equal(await page.locator('[data-km-date]').getAttribute('datetime'),'2026-10-13');
      assert.equal(await page.locator('[data-daily-data-error]').isVisible(),false);
      assert.equal(await page.locator('[data-yangsheng-error]').isVisible(),false);
      assert.equal(await page.locator('[data-topic-translation]').filter({visible:true}).filter({hasText:/^\s*아카이브 풀이\s*—\s*$/}).count(),0);
      await page.clock.setFixedTime(new Date('2026-10-13T15:01:00Z'));
      await page.reload();
      await page.locator('[data-topic-date][datetime="2026-10-14"]').waitFor();
      await page.locator('[data-yangsheng-date][datetime="2026-10-14"]').waitFor();
      assert.equal(await page.locator('[data-km-date]').getAttribute('datetime'),'2026-10-14');
      const failed = await context.newPage();
      await failed.route('**/assets/daily-korean-medicine/*.json*', route => route.abort());
      await failed.goto(base+'/');
      await failed.locator('[data-daily-data-error]').waitFor();
      await failed.locator('[data-yangsheng-error]').waitFor();
      assert.equal(await failed.locator('[data-topic-date]').innerText(),'기본 카드');
      assert.equal(await failed.locator('[data-yangsheng-date]').innerText(),'기본 카드');
      assert.match(await failed.locator('[data-daily-data-error]').innerText(),/불러오지 못했습니다/);
      assert.match(await failed.locator('[data-yangsheng-error]').innerText(),/기본 문구/);
      assert.equal(await failed.locator('[data-topic-link]').count(),4);
      for (const link of await failed.locator('[data-topic-link]').all()) assert(await link.getAttribute('href'));
      assert.equal(await failed.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),true);
      await failed.close();

      const staticContext = await browser.newContext({viewport, javaScriptEnabled:false});
      const staticPage = await staticContext.newPage();
      await staticPage.goto(base+'/');
      const homeSource = await (await staticPage.request.get(base+'/')).text();
      assert(!homeSource.includes('불러오지 못했습니다'));
      assert(!homeSource.includes('불러오지 못해'));
      assert.equal(await staticPage.locator('[data-topic-link][href]').count(),4);
      await staticPage.goto(base+'/conditions/insomnia/');
      assert.equal(await staticPage.locator('[data-copy-citation]:visible').count(),0);
      assert.equal(await staticPage.locator('[data-archive-citation] a').filter({hasText:'문서 고정 주소'}).isVisible(),true);
      await staticContext.close();

      const shared = await context.newPage();
      await shared.addInitScript(() => {
        Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{
          writeText:async text => { window.copiedArticle = text; }
        }});
      });
      await shared.goto(base+'/conditions/insomnia/?utm_source=test#_1');
      assert.match(await shared.title(),/^불면증·수면장애: 원인/);
      await shared.locator('[data-copy-citation="citation"]').click();
      await shared.locator('[data-citation-status]').filter({hasText:'복사했습니다.'}).waitFor();
      assert.equal(await shared.evaluate(() => window.copiedArticle),
        '불면증·수면장애: 원인, 한약·침 치료와 생활관리 — 민성 한의학 아카이브\nhttps://wiki.minseong.co.kr/conditions/insomnia/');
      await shared.evaluate(() => { navigator.clipboard.writeText = async () => { throw new Error('denied'); }; });
      await shared.locator('[data-copy-citation="url"]').click();
      await shared.locator('[data-citation-fallback]').waitFor();
      assert.equal(await shared.locator('[data-citation-fallback]').inputValue(),'https://wiki.minseong.co.kr/conditions/insomnia/');
      assert.equal(await shared.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),true);
      await shared.screenshot({path:`archive-browser-results/${name}-article-sharing.png`,fullPage:false});
      await shared.close();

      page.on('pageerror',error => errors.push(error.message));
      await page.goto(base+'/daily-korean-medicine/?card=points-15');
      const preview = page.locator('[data-daily-preview]');
      await preview.locator('[data-topic-title]').filter({hasText:'합곡'}).waitFor();
      const answer = preview.locator('[data-topic-answer-box]');
      assert.equal(await answer.isVisible(),true);
      assert.equal(await answer.locator('[data-topic-answer]').isVisible(),false);
      assert.match(await preview.locator('[data-topic-review]').innerText(),/합곡.*태충/);
      await answer.locator('summary').focus();
      await page.keyboard.press('Enter');
      assert.equal(await answer.locator('[data-topic-answer]').isVisible(),true);
      assert.match(await answer.locator('[data-topic-answer]').innerText(),/사관혈/);
      assert(await preview.locator('[data-topic-related] a').count() > 0);
      await page.screenshot({path:`archive-browser-results/${name}-daily-review.png`,fullPage:false});
      await page.locator('[data-daily-next-card]').click();
      assert.equal(await answer.isVisible(),false,'switching to a card without a review must remove the previous answer');
      await page.goto(base+'/daily-korean-medicine/?card=herbs-3');
      await preview.locator('[data-topic-title]').filter({hasText:'부자'}).waitFor();
      assert.equal(await answer.getAttribute('open'),null,'new review must be collapsed');
      assert.match(await preview.locator('[data-topic-explanation]').innerText(),/법제/);
      await page.goto(base+'/daily-korean-medicine/?date=2026-10-11');
      await page.locator('[data-daily-km] [data-km-count]').filter({hasText:'/ 21'}).waitFor();
      await page.goto(base+'/daily-korean-medicine/?date=2026-10-12');
      await page.locator('[data-daily-km] [data-km-count]').filter({hasText:'/ 33'}).waitFor();

      await page.goto(base+'/daily-korean-medicine/?almanac=spring-37');
      const library=page.locator('[data-almanac-library]');
      await library.locator('[data-almanac-title]').filter({hasText:'산책의 출발점'}).waitFor();
      assert.equal(await library.locator('[data-almanac-topic] option').count(),7);
      await library.locator('[data-almanac-season]').selectOption('winter');
      await library.locator('[data-almanac-topic]').selectOption('senses');
      const results=library.locator('[data-almanac-results] button');
      assert(await results.count() > 0);
      for (const text of await results.allTextContents()) assert(text.includes('겨울'));
      await results.first().click();
      assert(new URL(page.url()).searchParams.get('almanac').startsWith('winter-'));
      await page.locator('[data-yangsheng-find]').click();
      assert.equal(await library.locator('[data-almanac-season]').inputValue(),'all');
      assert.equal(await library.locator('[data-almanac-topic]').inputValue(),'all');
      await library.locator('[data-almanac-topic]').selectOption('sleep');
      await library.locator('[data-almanac-query]').fill('missing-no-such-phrase');
      assert.equal(await results.count(),0);
      assert.match(await library.locator('[data-almanac-status]').innerText(),/일치하는 문구가 없습니다/);
      await library.locator('[data-almanac-query]').fill('');
      await results.first().click();
      assert.equal(await page.locator('#__search').isChecked(),false);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),true);
      await page.screenshot({path:`archive-browser-results/${name}-daily-almanac.png`,fullPage:false});
      await page.goto(base+'/daily-korean-medicine/?almanac=autumn-57');
      const life = page.locator('[data-almanac-preview]');
      await life.locator('[data-almanac-title]').filter({hasText:'한로'}).waitFor();
      assert.match(await life.locator('[data-yangsheng-story]').innerText(),/생강과 대추/);
      assert.equal(await life.locator('.daily-km-almanac-source').isVisible(),false);
      assert.equal(await life.locator('[data-yangsheng-related-link]').getAttribute('href'),'/herbs/fresh-ginger/');
      await page.evaluate(() => { Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.copiedAlmanac=text;}}}); });
      await page.locator('[data-almanac-copy]').click();
      assert.match(await page.evaluate(()=>window.copiedAlmanac),/생강과 대추/);
      assert(!(await page.evaluate(()=>window.copiedAlmanac)).includes('고전 원문 —'));
      await page.locator('[data-almanac-query]').fill('천금요방');
      await page.locator('[data-almanac-season]').selectOption('all');
      await page.locator('[data-almanac-results] button').first().click();
      assert.equal(await life.locator('.daily-km-almanac-source').isVisible(),true);
      assert.match(await life.locator('[data-yangsheng-original]').innerText(),/安身/);
      await page.locator('[data-almanac-copy]').click();
      assert.match(await page.evaluate(()=>window.copiedAlmanac),/고전 원문 —/);
      await page.goto(base+'/daily-korean-medicine/');
      await page.locator('#daily-solar-terms > summary').click();
      assert.equal(await page.locator('#daily-solar-terms table a').count(),24);
      await page.locator('#daily-solar-terms a').filter({hasText:'입춘'}).click();
      await page.locator('[data-almanac-title]').filter({hasText:'입춘'}).waitFor();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),true);
      await page.screenshot({path:`archive-browser-results/${name}-daily-life-terms.png`,fullPage:false});
      await page.goto(base+'/daily-korean-medicine/?date=2026-11-07');
      const daily=page.locator('[data-daily-yangsheng]');
      await daily.locator('[data-yangsheng-term-day]').filter({hasText:'오늘은 입동(立冬)'}).waitFor();
      assert.match(await daily.locator('[data-term-meaning]').innerText(),/겨울/);
      assert.match(await daily.locator('[data-term-medicine]').innerText(),/보온/);
      await page.locator('[data-yangsheng-find]').click();
      assert.match(await page.locator('[data-almanac-title]').innerText(),/입동/);
      assert.equal(new URL(page.url()).searchParams.get('almanac'),'autumn-59');
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      await daily.screenshot({path:`archive-browser-results/${name}-daily-actual-term.png`});
      const picker=page.locator('[data-km-day-picker]');
      await picker.fill('2027-11-08'); await picker.dispatchEvent('change');
      await daily.locator('[data-yangsheng-term-day]').filter({hasText:'2027년 11월 8일 · 오늘은 입동'}).waitFor();
      await picker.fill('2027-11-07'); await picker.dispatchEvent('change');
      await daily.locator('[data-yangsheng-date][datetime="2027-11-07"]').waitFor();
      assert(!(await daily.locator('[data-yangsheng-term-day]').innerText()).includes('오늘은 입동'));
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      assert.deepEqual(errors,[]);
      await context.close();
    }
    console.log('Daily reader mobile/desktop checks passed: review reveal/reset, permalinks, combined filters, empty results and layout.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error);process.exit(1);});
