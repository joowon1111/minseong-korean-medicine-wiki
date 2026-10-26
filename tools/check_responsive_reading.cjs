/* Built-site checks for page-specific assets and responsive reading controls. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const base = process.env.ARCHIVE_TEST_BASE || 'http://127.0.0.1:8766';

(async () => {
  const browser = await chromium.launch({headless:true});
  fs.mkdirSync('archive-browser-results', {recursive:true});
  try {
    for (const [width, height] of [[320,640], [390,844], [768,1024], [1440,900]]) {
      const page = await browser.newPage({viewport:{width,height}});
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
      await page.goto(base + '/', {waitUntil:'networkidle'});
      await page.locator('[data-topic-title]').first().waitFor();
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), `Home overflow at ${width}`);
      const scripts = await page.locator('script[src]').evaluateAll(nodes => nodes.map(n => n.src));
      assert(!scripts.some(src => /learning\/learning|acupoint-atlas\/(explorer|discovery)|archive-tools\/tools/.test(src)), 'Home must not request unrelated widget code');
      await page.screenshot({path:`archive-browser-results/home-responsive-${width}.png`});
      const publisher = page.locator('.archive-publisher');
      assert.match(await publisher.textContent(), /목정일 · 김문정/);
      assert.equal(await publisher.locator('a[href="https://minseong.co.kr/"]').count(), 1);
      assert.equal(await publisher.locator('a[href="https://minseong.co.kr/oshineun-gil/"]').count(), 1);
      await publisher.scrollIntoViewIfNeeded();
      const columns = await publisher.locator('.archive-publisher__grid > div').all();
      const left = await columns[0].boundingBox(), right = await columns[1].boundingBox();
      assert(width <= 760 ? right.y >= left.y + left.height : right.x >= left.x + left.width, 'Publisher columns must adapt to viewport');
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), `Publisher overflow at ${width}`);
      for (const link of await publisher.locator('nav a').all()) {
        const box = await link.boundingBox();
        assert(box.height >= 44 && box.x >= 0 && box.x + box.width <= width, 'Footer links must fit and be easy to tap');
      }
      await publisher.locator('a').first().focus();
      assert(await publisher.locator('a').first().evaluate(el => el === document.activeElement), 'Footer links must accept keyboard focus');
      await publisher.screenshot({path:`archive-browser-results/publisher-${width}.png`});
      await page.evaluate(() => document.body.setAttribute('data-md-color-scheme', 'slate'));
      await publisher.screenshot({path:`archive-browser-results/publisher-dark-${width}.png`});
      await page.evaluate(() => document.body.setAttribute('data-md-color-scheme', 'default'));
      for (const [path, anchor] of [
        ['/conditions/', 'combined-care-paths'],
        ['/portal/herbs-formulas/', 'compare-formulas'],
        ['/sasang-integrated/', 'ordinary-current-record'],
        ['/classics-reader/', 'shanghan-reading-paths'],
        ['/symptom-herbal-guide/', '5'],
        ['/symptom-herbal-guide/neuro-mental/', 'clinical-route'],
        ['/symptom-herbal-guide/urogenital/', '_1'],
        ['/symptom-integrated/sleep-fatigue/', '자고-나도-피곤해요'],
        ['/symptom-integrated/respiratory-rhinitis/', '기침이-오래가요'],
        ['/symptom-integrated/treatment-evidence/', '_1'],
      ]) {
        await page.goto(base + path + '#' + anchor, {waitUntil:'networkidle'});
        await page.locator('#' + anchor).waitFor();
        assert.equal(await page.locator('article h1').count(), 1, `One article title: ${path}`);
        assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), `Hub overflow: ${path} at ${width}`);
        const hubTables = await page.locator('.md-typeset__scrollwrap').evaluateAll(nodes => nodes.map(n => ({overflow:n.scrollWidth>n.clientWidth+1,tabindex:n.getAttribute('tabindex'),role:n.getAttribute('role')})));
        hubTables.filter(table => table.overflow).forEach(table => {assert.equal(table.tabindex,'0'); assert.equal(table.role,'region');});
        await page.screenshot({path:`archive-browser-results/hub-${anchor}-${width}.png`});
      }
      await page.goto(base + '/acupuncture/points/lu2/', {waitUntil:'networkidle'});
      assert.equal(await page.locator('link[href*="acupoint-atlas/explorer.css"]').count(), 1, 'Point detail must load its navigation styles');
      const parent = page.locator('.acupoint-meridian-parent');
      assert.match(await parent.textContent(), /소속 경맥\s*수태음폐경 LU →/);
      assert.equal(await parent.getAttribute('href'), '/meridian-network/lung-meridian/');
      const parentBox = await parent.boundingBox();
      assert(parentBox.height >= 44 && parentBox.x >= 0 && parentBox.x + parentBox.width <= width, 'Parent link must fit and be easy to tap');
      if (width >= 768) {
        const title = await page.locator('.acupoint-title-row h1').boundingBox();
        assert(parentBox.x >= title.x + title.width, 'Meridian appears beside the point title on wider screens');
      }
      await page.screenshot({path:`archive-browser-results/point-meridian-${width}.png`});
      await parent.click();
      assert(new URL(page.url()).pathname.endsWith('/lung-meridian/'));
      await page.locator('a[href="../../acupuncture/points/lu2/"]').first().click();
      assert(new URL(page.url()).pathname.endsWith('/lu2/'), 'Meridian links back to the point');
      const sequence = page.locator('.acupoint-sequence');
      const previous = await sequence.locator('a[rel="prev"]').boundingBox();
      const next = await sequence.locator('a[rel="next"]').boundingBox();
      assert(previous.height >= 60 && next.height >= 60, 'Point cards must be easy to tap');
      assert(width <= 600 ? next.y >= previous.y + previous.height + 8 : next.x >= previous.x + previous.width + 8, 'Point cards must have a visible gap');
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), `Point overflow at ${width}`);
      await sequence.scrollIntoViewIfNeeded();
      await page.screenshot({path:`archive-browser-results/point-navigation-${width}.png`});
      await sequence.locator('a[rel="next"]').click();
      assert(new URL(page.url()).pathname.endsWith('/lu3/'), 'Next point link keeps its destination');
      await page.goto(base + '/conditions/low-back-pain/', {waitUntil:'networkidle'});
      assert.equal(await page.locator('script[src*="learning/learning.js"]').count(), 0);
      assert.equal(await page.locator('script[src*="daily-korean-medicine"]').count(), 0);
      assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), `Article overflow at ${width}`);
      const tables = await page.locator('.md-typeset__scrollwrap').evaluateAll(nodes => nodes.map(n => ({overflow:n.scrollWidth>n.clientWidth+1,tabindex:n.getAttribute('tabindex'),role:n.getAttribute('role')})));
      tables.filter(table => table.overflow).forEach(table => {assert.equal(table.tabindex,'0'); assert.equal(table.role,'region');});
      const input = page.locator('.md-search__input');
      if (!(await input.isVisible())) await page.locator('label[for="__search"]').first().click();
      await input.fill('전침');
      await page.locator('#ms-ksearch-panel .ms-ksearch-item').first().waitFor();
      if (width < 720) {
        await page.setViewportSize({width,height:400});
        const panel = await page.locator('#ms-ksearch-panel').boundingBox();
        assert(panel.y >= 0 && panel.y + panel.height <= 401, 'Search results must fit a shortened mobile viewport');
      }
      await page.keyboard.press('Escape');
      assert(await page.locator('#ms-ksearch-panel').isHidden(), 'Escape closes search');
      assert.deepEqual(errors, [], `Browser errors at ${width}`);
      await page.close();
      console.log(`PASS ${width}px: home, article, widget loading, tables, search and Escape`);
    }
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode=1;});
