const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const dir=path.join(__dirname,'../docs/assets/sasang-explorer');
function load(){
 const ctx=vm.createContext({});
 for(const file of ['data.js','sources.js','source-ui.js']) vm.runInContext(fs.readFileSync(path.join(dir,file),'utf8'),ctx);
 return vm.runInContext('({D,AXIS_ORDER,PATTERN_SOURCES,SOURCE_PASSAGES,SOURCE_DOCUMENTS,SOURCE_CHAPTERS,sourceSearchText})',ctx);
}
test('every selectable pattern has verified-source metadata and valid same-constitution comparisons',()=>{
 const d=load(),used=new Set();
 for(const [c,axes] of Object.entries(d.AXIS_ORDER)){
  assert.deepEqual(Object.keys(d.PATTERN_SOURCES[c]).sort(),Array.from(axes).sort());
  for(const axis of axes){
   const s=d.PATTERN_SOURCES[c][axis];
   assert.ok(s.meaning&&s.ordinary&&s.formula&&s.kind&&s.route);
   assert.ok(s.passages.length>0);
   for(const id of s.passages){
    used.add(id);const p=d.SOURCE_PASSAGES[id];
    assert.ok(p,`${c}/${axis}: missing passage ${id}`);
    assert.ok(d.SOURCE_CHAPTERS[p.chapter]&&d.SOURCE_DOCUMENTS[p.document]);
    assert.ok(p.text&&p.translation&&p.context&&Number.isInteger(p.page)&&p.page>0);
    assert.match(p.number,/^\d+-\d+$/);
   }
   assert.ok(s.compare.length>0);
   for(const target of s.compare) assert.ok(target!==axis&&axes.includes(target),`${axis} -> ${target}`);
  }
 }
 assert.equal(used.size,Object.keys(d.SOURCE_PASSAGES).length,'no orphan passages');
});
test('classical and formula search finds learning content without indexing incidental URL paths',()=>{
 const {D,sourceSearchText}=load();
 const matches=q=>D.filter(row=>sourceSearchText(row).includes(q.normalize('NFKC').toLowerCase()));
 assert.ok(matches('亡陽').some(row=>row[1]==='망양초증·승양'));
 assert.ok(matches('7-30').some(row=>row[1]==='소음병·깊은 리한/장궐'));
 assert.ok(matches('저령차전자탕').some(row=>row[1]==='신열두통망음·배설 변화'));
 assert.equal(matches('sasang-formula-library').length,0);
});
test('all explorer prescription targets and explicit anchors exist in the archive',()=>{
 const {D}=load();
 for(const [name,url] of D.flatMap(row=>Array.from(row[5]))){
  const [route,anchor]=url.split('#');
  const slug=route.replace(/^\//,'').replace(/\/$/,'');
  const candidates=[path.join(__dirname,'../docs',slug+'.md'),path.join(__dirname,'../docs',slug,'index.md')];
  const file=candidates.find(p=>fs.existsSync(p));
  assert.ok(file,`${name}: ${url}`);
  if(anchor) assert.ok(fs.readFileSync(file,'utf8').includes('{#'+anchor+'}'),`${name}: missing ${anchor}`);
 }
});
