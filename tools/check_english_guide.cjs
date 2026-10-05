// Run against a built site served at GUIDE_BASE_URL. Browser dependency is CI-only.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require('playwright');
const base = process.env.GUIDE_BASE_URL || 'http://127.0.0.1:8766';

(async () => {
  const browser = await chromium.launch();
  try {
    fs.mkdirSync('guide-browser-results', { recursive: true });
    for (const width of [390, 1440]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.goto(base + '/', { waitUntil: 'networkidle' });
      const entry = page.locator('article .km-guide-entry a');
      assert(await entry.isVisible(), 'Home English entrance must be visible');
      await entry.click();
      await page.waitForURL('**/korean-medicine-guide/');
      assert.equal(await page.locator('article h1').innerText(), 'Korean Medicine Guide');
      assert.equal(await page.locator('html').getAttribute('lang'), 'en');
      assert.equal(await page.locator('article').getAttribute('lang'), 'en');
      assert.equal(await page.locator('.km-guide-nav a').count(), 8);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
      assert(!overflow, `Page overflow at ${width}px`);
      await page.screenshot({ path: `guide-browser-results/guide-${width}.png` });
      await page.locator('.km-guide-nav a[href="#sasang-medicine"]').click();
      assert.equal(new URL(page.url()).hash, '#sasang-medicine');
      assert(await page.locator('#sasang-medicine').isVisible());
      const question = page.locator('article details').filter({ hasText: 'Can I find my Sasang constitution' });
      await question.locator('summary').click();
      assert(await question.evaluate(el => el.open), 'FAQ must expand');
      assert((await question.innerText()).includes('A personality result is insufficient'));
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), 'Expanded FAQ overflow');
      await page.screenshot({ path: `guide-browser-results/faq-${width}.png` });
      await page.goto(base + '/');
      const search = page.locator('.md-search__input');
      if (!(await search.isVisible())) await page.locator('label[for="__search"]').first().click();
      await search.fill('Korean Medicine');
      await page.locator('a[href="/korean-medicine-guide/"]').filter({ hasText: 'Korean Medicine Guide' }).first().waitFor({ state: 'visible' });
      console.log(`PASS ${width}px: home entrance, English language, eight sections, no horizontal overflow, Sasang anchor, expandable FAQ, English search`);
      await page.close();
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
