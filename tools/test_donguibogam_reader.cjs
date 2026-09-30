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
