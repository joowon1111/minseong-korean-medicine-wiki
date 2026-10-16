const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {test}=require('node:test');
const reader=require('../docs/assets/donguibogam/reader.js');
const base=path.join(__dirname,'../docs/assets/donguibogam');
const manifest=JSON.parse(fs.readFileSync(path.join(base,'manifest.json'),'utf8'));
const rows=Object.values(manifest.groups).flatMap(g=>JSON.parse(fs.readFileSync(path.join(base,g.file),'utf8')));
test('Korean names, Hanja and literal phrases search only the independent corpus',()=>{
 for(const [query,title] of [['당귀','當歸'],['동의보감 원문 당귀','當歸'],['황련','黃連'],['녹용','鹿茸'],['경옥고','瓊玉膏'],['當歸','當歸']])assert.equal(reader.search(rows,query)[0].row.title,title);
 assert.ok(reader.search(rows,'開胃 止嘔逆').some(x=>x.row.title==='茯苓'));
 assert.ok(reader.search(rows,'당귀','tangaek-3').length);
 assert.equal(reader.search(rows,'당귀','tangaek-1').length,0);
 assert.equal(reader.search(rows,'').length,0);
 assert.equal(reader.search(rows,'없는검색어123').length,0);
});
test('all volumes have bounded page URLs and external hosts cannot be injected',()=>{
 assert.equal(manifest.scans.length,25);
 for(const scan of manifest.scans){assert.match(reader.imageURL(scan,1),/\/page1-/);assert.ok(reader.imageURL(scan,scan.pages));assert.equal(reader.imageURL(scan,0),null);assert.equal(reader.imageURL(scan,scan.pages+1),null);assert.equal(reader.imageURL(scan,1.5),null);assert.equal(reader.imageURL({...scan,thumbnail:'https://evil.test/page1-500px-x'},1),null);}
});
test('malformed imported rows cannot enter the reader',()=>{
 assert.ok(rows.every(reader.validRow));
 for(const row of [null,{}, {...rows[0],aliases:'bad'},{...rows[0],text:[]},{...rows[0],id:'<script>'},{...rows[0],group:'outside'}])assert.equal(Boolean(reader.validRow(row)),false);
});

test('ordinary pages and instant navigation never load reader or corpus assets',()=>{
 const vm=require('node:vm');let created=0;let subscription;
 const context={document:{getElementById:()=>null,createElement:()=>{created++;},head:{appendChild(){created++;}}},document$:{subscribe(fn){subscription=fn;}}};
 vm.runInNewContext(fs.readFileSync(path.join(base,'bootstrap.js'),'utf8'),context);
 for(let n=0;n<20;n++)subscription();assert.equal(created,0);
});

test('new Korean names reach their original entry and part names keep parent context',()=>{
 for(const [query,title] of [['사향','麝香'],['천마','天麻'],['대황','大黃'],['오가피','五加皮'],['현호색','玄胡索'],['연자육','蓮實'],['행인','杏核仁'],['산약','薯蕷'],['백급','白芨'],['향부자','莎草根']]){
  assert.equal(reader.search(rows,query)[0].row.title,title);
 }
 const part=reader.search(rows,'감초 마디')[0].row;
 assert.equal(part.title,'節');assert.equal(part.context_title,'甘草');
});

test('browsing and pagination can reach every original record exactly once',()=>{
 for(const group of ['',...Object.keys(manifest.groups)]){
  const hits=reader.browse(rows,group),seen=[];
  const pages=Math.ceil(hits.length/50);
  for(let n=0;n<pages;n++)seen.push(...reader.pageResults(hits,n).items.map(x=>x.row.id));
  assert.equal(seen.length,hits.length);assert.equal(new Set(seen).size,hits.length);
  assert.deepEqual(seen,rows.filter(r=>!group||r.group===group).map(r=>r.id));
 }
 assert.equal(reader.pageResults(reader.browse(rows),-1).index,0);
 assert.equal(reader.pageResults(reader.browse(rows),Infinity).index,0);
 assert.equal(reader.pageResults(reader.browse(rows),9999).index,31);
 assert.deepEqual(reader.pageResults([],0).items,[]);
});

test('the live reader browses past 50 entries and facsimile navigation stays independent',async()=>{
 const vm=require('node:vm');
 class Element {
  constructor(tag='div'){this.tag=tag;this.children=[];this.listeners={};this.dataset={};this.value='';this.textContent='';this.isConnected=true;}
  appendChild(node){this.children.push(node);return node;}
  replaceChildren(){this.children=[];}
  addEventListener(name,fn){this.listeners[name]=fn;}
  setAttribute(){} scrollIntoView(){}
 }
 const ids=['dgb-status','dgb-results','dgb-passage','dgb-volume-guide','dgb-volume','dgb-page','dgb-query','dgb-group','dgb-search-form','dgb-browse','dgb-scan-form','dgb-scan','dgb-scan-status','dgb-scan-image','dgb-scan-image-link','dgb-scan-source','dgb-scan-pdf','dgb-prev','dgb-next'];
 const elements=Object.fromEntries(ids.map(id=>[id,new Element()]));
 elements['dgb-volume'].value='1';elements['dgb-page'].value='1';
 const root=new Element();root.querySelector=selector=>elements[selector.slice(1)];
 const requests=[];let address='';
 const context={document:{createElement:tag=>new Element(tag)},URL,URLSearchParams,location:{pathname:'/classics/donguibogam/original/',search:''},history:{replaceState:(_,__,url)=>{address=url;}},fetch:async url=>{
  requests.push(url);const file=url.split('/').pop().split('?')[0];return {ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(base,file),'utf8'))};
 }};
 vm.runInNewContext(fs.readFileSync(path.join(base,'reader.js'),'utf8'),context);
 context.MinseongDonguiReader.install(root);await new Promise(resolve=>setImmediate(resolve));
 assert.equal(requests.length,1);
 const descend=node=>[node,...node.children.flatMap(descend)];
 const women=descend(elements['dgb-volume-guide']).find(el=>el.tag==='button'&&el.textContent==='잡병편 권10');
 women.listeners.click();assert.equal(requests.length,1);assert.match(address,/volume=18&page=3/);assert.match(elements['dgb-scan-status'].textContent,/잡병편 권10/);
 elements['dgb-group'].value='tangaek-3';elements['dgb-browse'].listeners.click();await new Promise(resolve=>setImmediate(resolve));
 assert.equal(elements['dgb-results'].children.filter(el=>el.className==='dgb-result').length,50);assert.match(address,/list=1&group=tangaek-3/);
 const next=()=>descend(elements['dgb-results']).find(el=>el.tag==='button'&&el.textContent==='다음 50항목');
 for(let n=0;n<8;n++)next().listeners.click();
 assert.equal(elements['dgb-results'].children.filter(el=>el.className==='dgb-result').length,38);assert.equal(next().disabled,true);assert.match(address,/offset=400/);
 elements['dgb-volume'].value='23';elements['dgb-volume'].listeners.change();assert.equal(elements['dgb-scan'].hidden,true);
 elements['dgb-page'].value='3';await elements['dgb-scan-form'].listeners.submit({preventDefault(){}});
 assert.match(elements['dgb-scan-status'].textContent,/침구편 권1/);
});
