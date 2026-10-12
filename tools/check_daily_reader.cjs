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
      page.on('pageerror',error => errors.push(error.message));
      await page.goto(base+'/daily-korean-medicine/?card=points-15');
      const preview = page.locator('[data-daily-preview]');
      await preview.locator('[data-topic-title]').filter({hasText:'합곡'}).waitFor();
      const answer = preview.locator('[data-topic-answer-box]');
      assert.equal(await answer.isVisible(),true);
      assert.equal(await answer.locator('[data-topic-answer]').isVisible(),false);
      assert.match(await preview.locator('[data-topic-review]').innerText(),/사관/);
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
      assert.deepEqual(errors,[]);
      await context.close();
    }
    console.log('Daily reader mobile/desktop checks passed: review reveal/reset, permalinks, combined filters, empty results and layout.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error);process.exit(1);});
