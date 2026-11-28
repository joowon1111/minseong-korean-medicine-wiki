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
      await page.goto(base+'/network/#ontology-composition-tables');
      await page.locator('#ontology-formula-compositions').waitFor();
      const ontology=JSON.parse(fs.readFileSync('docs/assets/ai/ontology.jsonld','utf8'));
      const compositions=ontology['@graph'].filter(n=>n['@type']==='rdf:Statement'&&n['rdf:predicate']['@id']==='km:containsHerb');
      const formulaIds=new Set(compositions.map(n=>n['rdf:subject']['@id']));
      const classical=ontology['@graph'].filter(n=>n['@type']==='rdf:Statement'&&n['rdf:predicate']['@id']==='km:recordsFormula');
      const inverse=new Map();
      for(const n of compositions){const herb=n['rdf:object']['@id'];if(!inverse.has(herb))inverse.set(herb,new Set());inverse.get(herb).add(n['rdf:subject']['@id']);}
      const projected=await page.evaluate(()=>{
        const after=id=>{for(let e=document.getElementById(id).nextElementSibling;e;e=e.nextElementSibling){const t=e.matches('table')?e:e.querySelector('table');if(t)return t;}throw Error('Missing composition table');};
        const formulas=after('ontology-formula-compositions'),shared=after('ontology-shared-herbs'),clauses=after('ontology-classical-formulas');
        return {formulaRows:formulas.tBodies[0].rows.length,sharedRows:shared.tBodies[0].rows.length,
          classicalRows:clauses.tBodies[0].rows.length,classicalText:clauses.innerText,
          classicalSources:[...clauses.querySelectorAll('a')].map(a=>a.href),
          text:formulas.innerText,hasSource:[...formulas.querySelectorAll('a')].some(a=>a.href.endsWith('#donguibogam-version')),
          emptyLinks:[...formulas.querySelectorAll('a')].filter(a=>!a.innerText.trim()).length,
          overflow:document.documentElement.scrollWidth>innerWidth+2};
      });
      assert.equal(projected.formulaRows,formulaIds.size);
      assert.equal(projected.sharedRows,inverse.size);
      assert.equal(projected.classicalRows,new Set(classical.map(n=>JSON.stringify([n['rdf:subject']['@id'],n['rdf:object']['@id'],n['dcterms:source']['@id']]))).size);
      assert.match(projected.classicalText,/소건중탕 — 상한론 송본 수록형/);
      assert.match(projected.classicalText,/소건중탕 — 금궤요략 수록형/);
      for(const record of classical)assert.ok(projected.classicalSources.includes(record['dcterms:source']['@id']));
      assert.match(projected.text,/산조인탕 — 금궤요략 수록형/);
      assert.match(projected.text,/산조인탕 — 동의보감 몽문 수록형/);
      assert.match(projected.text,/반하후박탕 — 금궤요략 수록형/);
      assert.equal(projected.hasSource,true); assert.equal(projected.emptyLinks,0);
      assert.equal(projected.overflow,false,'ontology tables must fit the viewport');
      const statements=ontology['@graph'].filter(n=>n['@type']==='rdf:Statement');
      const principles=statements.filter(n=>n['rdf:predicate']['@id']==='km:hasTraditionalTreatmentPrinciple');
      const routes=statements.filter(n=>n['rdf:predicate']['@id']==='km:hasTraditionalPatternContext')
        .flatMap(context=>principles.filter(p=>p['rdf:subject']['@id']===context['rdf:object']['@id']).map(treatment=>[context,treatment]));
      const routePanels=page.locator('details.ontology-treatment-route');
      assert.equal(await routePanels.count(),routes.length);
      const nodeMap=new Map(ontology['@graph'].map(n=>[n['@id'],n]));
      const expectedRows=routes.map(([c,t])=>[c['rdf:subject'],c['rdf:object'],t['rdf:object']]
        .map(ref=>nodeMap.get(ref['@id'])['skos:prefLabel']['@value']).join(' / ')).sort();
      const actualRows=await routePanels.evaluateAll(panels=>panels.map(panel=>
        [...panel.closest('tr').cells].slice(0,3).map(cell=>cell.innerText.trim()).join(' / ')).sort());
      assert.deepEqual(actualRows,expectedRows);
      for(let i=0;i<await routePanels.count();i++){
        const panel=routePanels.nth(i);
        const control=await panel.locator(':scope > summary').boundingBox();
        assert.ok(control.height<=64,'treatment evidence controls must remain compact');
        await panel.locator(':scope > summary').click();
        assert.equal(await panel.locator('blockquote').count(),2);
        assert.equal(await panel.locator('a').count(),2);
        assert.equal(await panel.locator('blockquote').first().isVisible(),true);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,'expanded treatment conditions must fit the viewport');
        await panel.locator(':scope > summary').click();
      }
      for(const [context,treatment] of routes){
        const row=routePanels.filter({hasText:context['dcterms:description']['@value']})
          .filter({hasText:treatment['dcterms:description']['@value']});
        assert.equal(await row.count(),1);
        const sources=await row.locator('a').evaluateAll(links=>links.map(a=>a.href));
        assert.ok(sources.includes(context['dcterms:source']['@id']));
        assert.ok(sources.includes(treatment['dcterms:source']['@id']));
        const text=await row.textContent();
        for(const record of [context,treatment])assert.ok(text.includes(record['skos:scopeNote']['@value']));
      }
      await page.locator('#ontology-pattern-treatment').scrollIntoViewIfNeeded();
      await page.screenshot({path:`archive-browser-results/${name}-ontology-treatment-routes.png`,fullPage:false});
      const variantPairs=new Set(ontology['@graph'].filter(n=>n['@type']==='rdf:Statement'&&n['rdf:predicate']['@id']==='km:sharesNameWith').map(n=>JSON.stringify([n['rdf:subject']['@id'],n['rdf:object']['@id']].sort())));
      const comparisons=page.locator('details.ontology-variant-comparison');
      assert.equal(await comparisons.count(),variantPairs.size);
      for(let i=0;i<await comparisons.count();i++){
        const panel=comparisons.nth(i);
        await panel.locator(':scope > summary').click();
        const notes=panel.locator('details.ontology-variant-records');
        await notes.locator(':scope > summary').click();
        assert.ok((await panel.locator('a').count())>0);
        const text=await panel.innerText();
        assert.match(text,/공통으로 등록된 본초/);
        assert.match(text,/구성 근거/);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,'expanded variant tables must fit the viewport');
        await panel.locator(':scope > summary').click();
      }
      for(const term of ['先與小建中湯','不差者，與小柴胡湯']){
        const note=page.locator('details.ontology-clause-context').filter({hasText:term});
        assert.equal(await note.count(),1);
        await note.locator(':scope > summary').click();
        assert.equal(await note.locator('p').first().isVisible(),true);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,'expanded clause conditions must fit the viewport');
        await note.locator(':scope > summary').click();
      }
      await page.locator('#ontology-formula-compositions').scrollIntoViewIfNeeded();
      await page.screenshot({path:`archive-browser-results/${name}-ontology-compositions.png`,fullPage:false});
      for(const slug of ['ginseng','poria','ziziphus-seed','cinnamon-bark','perilla-leaf','magnolia-bark','astragalus','angelica','licorice','prepared-rehmannia','atractylodes','fresh-ginger','jujube-fruit','cinnamon-twig','pinellia','moschus','cervi-parvum-cornu','cornus-fructus','dried-ginger']){
        const herbIds=new Set(ontology['@graph'].filter(n=>Array.isArray(n['@type'])&&n['@type'].includes('km:Herb')&&new URL(n['foaf:page']['@id']).pathname==='/herbs/'+slug+'/').map(n=>n['@id']));
        const records=compositions.filter(n=>herbIds.has(n['rdf:object']['@id']));
        const expectedRows=new Set(records.map(n=>JSON.stringify([n['rdf:object']['@id'],n['rdf:subject']['@id'],n['dcterms:source']['@id']])));
        await page.goto(base+'/herbs/'+slug+'/#ontology-herb-formula-sources');
        await page.locator('#ontology-herb-formula-sources').waitFor();
        const herbView=await page.evaluate(()=>{
          let table;
          for(let e=document.getElementById('ontology-herb-formula-sources').nextElementSibling;e;e=e.nextElementSibling){table=e.matches('table')?e:e.querySelector('table');if(table)break;}
          if(!table)throw Error('Missing herb source table');
          return {rows:table.tBodies[0].rows.length,names:[...table.tBodies[0].rows].map(r=>r.cells[0].innerText),links:[...table.querySelectorAll('a')].map(a=>a.href),
            conditions:[...table.querySelectorAll('details.ontology-herb-context')].map(d=>d.textContent),overflow:document.documentElement.scrollWidth>innerWidth+2};
        });
        assert.equal(herbView.rows,expectedRows.size,slug+' source row count');
        assert.equal(herbView.overflow,false,slug+' herb table must fit the viewport');
        for(const record of records)assert.ok(herbView.links.includes(record['dcterms:source']['@id']));
        assert.equal(herbView.conditions.length,expectedRows.size,slug+' condition controls');
        for(const record of records)assert.ok(herbView.conditions.some(text=>text.replace(/\s+/g,'').includes(record['skos:scopeNote']['@value'].replace(/\s+/g,''))),slug+' retains its registered source conditions');
        const herbConditions=page.locator('details.ontology-herb-context');
        for(const index of new Set([0,expectedRows.size-1])){
          const condition=herbConditions.nth(index);
          assert.equal(await condition.evaluate(el=>el.open),false);
          await condition.locator(':scope > summary').click();
          assert.equal(await condition.evaluate(el=>el.open),true);
          assert.equal(await condition.locator('p').first().isVisible(),true);
          assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,slug+' expanded conditions must fit the viewport');
          if(slug==='fresh-ginger'&&index===0)await page.screenshot({path:`archive-browser-results/${name}-ontology-herb-conditions.png`,fullPage:false});
          await condition.locator(':scope > summary').click();
          assert.equal(await condition.evaluate(el=>el.open),false);
        }
        if(slug==='poria'){
          assert.ok(herbView.names.includes('복령')); assert.ok(herbView.names.includes('적복령'));
          await page.locator('#ontology-herb-formula-sources').scrollIntoViewIfNeeded();
          await page.screenshot({path:`archive-browser-results/${name}-ontology-herb-parts.png`,fullPage:false});
        }
      }
      const catalog=JSON.parse(fs.readFileSync('docs/assets/archive-tools/comparison.json','utf8'));
      const formulaCount=catalog.cards.filter(c=>c.kind==='formula').length;
      await page.goto(base+'/herbal-integrated/formula-structure/');
      const full=page.locator('[data-archive-compare]');
      await full.getByRole('status').filter({hasText:'전체 '+formulaCount+'개 처방 자료'}).waitFor();
      assert.equal(await full.locator('.archive-choice-list button').count(),60);
      while(await full.getByRole('button',{name:/^다음 \d+개 보기$/}).isVisible()) await full.getByRole('button',{name:/^다음 \d+개 보기$/}).click();
      assert.equal(await full.locator('.archive-choice-list button').count(),formulaCount);
      await full.getByLabel('처방 체계·체질').selectOption('소양인');
      assert.equal(await full.locator('.archive-choice-list button').count(),catalog.cards.filter(c=>c.kind==='formula'&&c.system==='소양인').length);
      await full.getByRole('searchbox').fill('독활지황');
      assert.equal(await full.locator('.archive-choice-list button').filter({hasText:/^독활지황탕/}).count(),1);
      assert.match(await full.locator('.archive-choice-list button').first().innerText(),/^독활지황탕/);
      await full.getByLabel('유사 처방 묶음').selectOption('soyang-yin');
      await full.getByRole('button',{name:'이 묶음 비교하기',exact:true}).click();
      await full.getByRole('table').waitFor();
      assert.equal(await full.locator('thead th').count(),5);
      const clinical=await full.getByRole('table').innerText();
      assert.match(clinical,/독활지황탕/); assert.match(clinical,/숙지황고삼탕/); assert.match(clinical,/출전·판본/); assert.match(clinical,/구성·약량/); assert.match(clinical,/고삼/);
      await page.reload(); await full.getByRole('table').waitFor();
      assert.equal(await full.locator('thead th').count(),5);
      assert.equal(await full.getByRole('link',{name:'관련 문제 풀기',exact:true}).first().getAttribute('href').then(u=>new URL(u,base).searchParams.get('subject')),'sasang');
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      await page.screenshot({path:`archive-browser-results/${name}-expanded-sasang-comparison.png`,fullPage:false});
      await page.goto(base+'/herbal-integrated/formula-structure/?group=women#interactive-comparison');
      await full.getByRole('table').waitFor();
      assert.match(await full.getByRole('table').innerText(),/온경탕/);
      assert.equal(await full.locator('thead th').count(),5);
      await page.goto(base+'/herbal-integrated/formula-structure/?compare='+encodeURIComponent('document-formulas-liu wei dihuang wan'));
      await full.getByRole('table').waitFor();
      assert.match(await full.locator('thead').innerText(),/육미지황환/);
      assert.equal(new URL(page.url()).searchParams.get('compare').includes('document-formulas-liu'),false);
      await page.goto(base + '/herbal-integrated/formula-structure/?compare=formula-sijunzi-tang,formula-liujunzi-tang,formula-xiangsha-liujunzi-tang#interactive-comparison');
      const trio=page.locator('[data-archive-compare]');
      await trio.getByRole('table').waitFor();
      assert.equal(await trio.locator('thead th').count(),4);
      assert.match(await trio.locator('table').innerText(),/목향|사인/);
      for (const name of ['사군자탕','육군자탕','향사육군자탕']) assert((await trio.locator('thead').innerText()).includes(name));
      await trio.getByRole('button',{name:'선택 초기화',exact:true}).click();
      await page.goto(base + '/herbal-integrated/formula-structure/');
      const compare = page.locator('[data-archive-compare]');
      await compare.locator('.archive-choice-list').getByRole('button',{name:'사군자탕',exact:true}).click();
      await compare.locator('.archive-choice-list').getByRole('button',{name:'육군자탕',exact:true}).click();
      await compare.getByRole('table').waitFor();
      assert.equal(await compare.locator('thead th').count(),3);
      assert.ok((await compare.locator('table').innerText()).includes('반하'));
      assert.ok(new URL(page.url()).searchParams.get('compare').includes('formula-sijunzi-tang'));
      await page.reload();
      await compare.getByRole('table').waitFor();
      await compare.getByRole('table').scrollIntoViewIfNeeded();
      await page.screenshot({path:`archive-browser-results/${name}-comparison.png`,fullPage:false});
      const studyLink = compare.getByRole('link',{name:'관련 문제 풀기',exact:true}).first();
      const studyURL = new URL(await studyLink.getAttribute('href'), page.url());
      assert.ok(studyURL.searchParams.get('topic'));
      assert.equal(studyURL.searchParams.has('q'),false);
      await studyLink.click();
      await page.getByRole('button',{name:'카드 뒤집기 · 답 확인',exact:true}).waitFor();
      assert.equal(await page.locator('[data-learning-room]').getByRole('searchbox').inputValue(),studyURL.searchParams.get('topic'));
      assert.equal(await page.locator('#__search').isChecked(),false,'learning link must not open global search overlay');
      await page.goBack();
      await compare.getByRole('table').waitFor();
      await compare.getByRole('button',{name:'선택 초기화',exact:true}).click();
      assert.equal(new URL(page.url()).searchParams.has('compare'),false);
      await page.goto(base + '/herbal-integrated/herb-comparisons/');
      const herb = page.locator('[data-archive-compare]');
      await herb.getByRole('searchbox').fill('인삼');
      await herb.getByRole('button',{name:/^인삼/}).first().click();
      assert.ok((await herb.locator('table').innerText()).includes('전통 효능'));
      await page.goto(base + '/search-guide/');
      const finder = page.locator('[data-archive-finder]');
      await finder.getByRole('searchbox').fill('사군자탕');
      await finder.getByRole('button',{name:'근거 자료 찾기'}).click();
      await finder.locator('article').first().waitFor({timeout:60000});
      assert.ok((await finder.locator('article').first().innerText()).includes('사군자탕'));
      assert.ok((await finder.innerText()).includes('관련 본문 발췌'));
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
  console.log('Archive browser checks passed: ontology composition and herb source tables, comparison, herb search, passage search, resume, export/import; mobile and desktop.');
})().catch(error=>{console.error(error);process.exitCode=1;});
