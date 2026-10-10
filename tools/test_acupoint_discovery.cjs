const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {normalize,tokens,matches,rank,safeURL,init}=require('../docs/assets/acupoint-atlas/discovery.js');
const entries=JSON.parse(fs.readFileSync(path.join(__dirname,'../docs/assets/acupoint-atlas/discovery.json'),'utf8')).entries;
const state=query=>({query,kind:'',meridian:'',region:''});
test('names, codes, neural annotations and prescription contents are searchable',()=>{
  for(const [q,id] of [['합곡','LI4'],['ＬＩ－４','LI4'],['li 4','LI4'],['정중신경','PC6'],['심비골신경','ST36'],['폐정격','saam-lu-tonify']]){
    assert.ok(entries.filter(e=>matches(e,state(q))).some(e=>e.id===id),q);
  }
  assert.deepEqual(tokens('LI 4 손'),['li4','손']);
  assert.equal(normalize(' ＬＩ－４ '),'li4');
});
test('multiple terms and simultaneous meridian and region filters narrow the results',()=>{
  const e=entries.find(e=>e.id==='PC6');
  assert.ok(matches(e,{query:'정중신경 내관',kind:'standard',meridian:'PC',region:e.region}));
  assert.ok(!matches(e,{...state('정중신경'),kind:'tung'}));
  assert.ok(!matches(e,{...state('정중신경'),meridian:'LI'}));
  assert.ok(!matches(e,state('정중신경 없는검색어')));
});
test('same-name records remain distinct and exact matches precede descriptive mentions',()=>{
  const shaohai=entries.filter(e=>matches(e,state('소해'))&&e.name==='소해');
  assert.equal(shaohai.length,2);
  assert.equal(new Set(shaohai.map(e=>e.id)).size,2);
  const hegu=entries.find(e=>e.id==='LI4');
  const ranked=entries.filter(e=>matches(e,state('합곡'))).sort((a,b)=>rank(b,'합곡')-rank(a,'합곡'));
  assert.equal(ranked[0].id,hegu.id);
  const linggu=entries.find(e=>e.kind==='tung'&&e.name==='영골');
  assert.ok(matches(linggu,{...state('영골'),kind:'tung'}));
});
test('unsafe URL schemes are rejected and query markup is never executed',()=>{
  for(const value of ['javascript:alert(1)','//example.org','data:text/html,x','/bad\\path','https://example.org/ x'])assert.equal(safeURL(value),'');
  assert.equal(safeURL('/assets/a.svg#LI4'),'/assets/a.svg#LI4');
  assert.ok(!entries.some(e=>matches(e,state('<script>alert(1)</script>'))));
  assert.doesNotThrow(()=>init({getElementById:()=>null}));
});
