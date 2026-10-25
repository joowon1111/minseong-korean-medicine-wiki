/* Actual copy/paste, provenance and SVG checks on desktop and mobile layouts. */
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs');
const base=process.env.ARCHIVE_TEST_BASE||'http://127.0.0.1:8766';
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  fs.mkdirSync('archive-browser-results',{recursive:true});
  for(const width of [390,1440]){
   const context=await browser.newContext({viewport:{width,height:950},permissions:['clipboard-read','clipboard-write']});
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/conditions/dry-eye/');
   const info=await page.locator('[data-archive-provenance]').evaluate(n=>({...n.dataset}));
   await page.evaluate(()=>{
    const p=Array.from(document.querySelectorAll('article p')).find(p=>p.textContent.trim().length>100&&!p.closest('aside'));
    const r=document.createRange();r.selectNodeContents(p);getSelection().removeAllRanges();getSelection().addRange(r);
   });
   const selected=await page.evaluate(()=>getSelection().toString());
   await page.keyboard.press('Control+c');
   const copied=await page.evaluate(()=>navigator.clipboard.readText());
   assert(copied.startsWith(selected));assert(copied.includes(info.provenanceUrl));assert(copied.includes(info.provenanceId));
   assert(copied.includes('출처: 민성 한의학 아카이브'));
   const rich=await page.evaluate(()=>{
    const event=new ClipboardEvent('copy',{bubbles:true,cancelable:true,clipboardData:new DataTransfer()});
    document.dispatchEvent(event);return {prevented:event.defaultPrevented,html:event.clipboardData.getData('text/html')};
   });
   assert(rich.prevented);assert(rich.html.includes(info.provenanceUrl));assert(!rich.html.includes('<script'));
   const untouched=await page.evaluate(()=>{
    const p=document.querySelector('article h1'),r=document.createRange();r.selectNodeContents(p);
    getSelection().removeAllRanges();getSelection().addRange(r);
    const short=new ClipboardEvent('copy',{bubbles:true,cancelable:true,clipboardData:new DataTransfer()});document.dispatchEvent(short);
    const input=document.createElement('textarea');input.value='사용자가 입력한 메모';document.body.appendChild(input);input.focus();input.select();
    const form=new ClipboardEvent('copy',{bubbles:true,cancelable:true,clipboardData:new DataTransfer()});input.dispatchEvent(form);input.remove();
    return {short:short.defaultPrevented,form:form.defaultPrevented};
   });
   assert.deepEqual(untouched,{short:false,form:false});
   await page.locator('.archive-provenance summary').click();
   await page.locator('.archive-provenance').scrollIntoViewIfNeeded();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.screenshot({path:`archive-browser-results/provenance-${width}.png`});
   await page.goto(base+'/conditions/eye-fatigue/');
   const next=await page.locator('[data-archive-provenance]').getAttribute('data-provenance-url');
   assert(next.endsWith('/conditions/eye-fatigue/'));assert.notEqual(next,info.provenanceUrl);
   const svg=await page.request.get(base+'/assets/acupoint-atlas/face-orbit.svg');
   assert.equal(svg.status(),200);assert((await svg.text()).includes('id="minseong-provenance-watermark"'));
   await page.goto(base+'/assets/acupoint-atlas/face-orbit.svg#BL2');
   assert(await page.locator('#BL2').count());assert(await page.locator('#minseong-provenance-watermark').count());
   await page.screenshot({path:`archive-browser-results/watermark-${width}.png`});
   assert.deepEqual(errors,[]);await context.close();
   console.log(`${width}px: real clipboard attribution, rich copy, short/form exclusions, page identity and SVG watermark passed`);
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
