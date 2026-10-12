const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base='docs/assets/acupoint-3d';
const data=JSON.parse(fs.readFileSync(base+'/points.json','utf8'));
const archive=JSON.parse(fs.readFileSync('docs/assets/acupoint-atlas/discovery.json','utf8')).entries.filter(e=>e.kind==='standard');
const daily=JSON.parse(fs.readFileSync('docs/assets/daily-korean-medicine/data.json','utf8')).points;
test('all standard points have real archive destinations and the same daily identifier',()=>{
  assert.equal(data.points.length,361);assert.equal(new Set(data.points.map(p=>p.code)).size,361);
  for(const point of data.points){
    const entry=archive.find(e=>e.code===point.code);assert(entry,point.code);
    assert.equal(point.loc,entry.location);assert.equal(point.href,entry.href);
    const index=Number(new URL(point.dailyHref,'https://wiki.minseong.co.kr').searchParams.get('card').replace('points-',''))-1;
    assert.equal(daily[index].code,point.code);
    for(const href of [point.href,point.route]){const p='docs'+href.replace(/\/$/,'');assert(fs.existsSync(p+'.md')||fs.existsSync(p+'/index.md'),href);}
    for(const row of point.rows) if(row.source) assert(/^https?:\/\//.test(row.source),row.source);
  }
});
test('display coordinates cover each point once or twice without detached or invalid mesh references',()=>{
  assert.equal(data.positions.length,670);
  const counts=new Map();
  for(const marker of data.positions){
    assert(Number.isInteger(marker[0])&&marker[0]>=0&&marker[0]<361);
    assert(marker.slice(1,8).every(Number.isFinite));
    const length=Math.hypot(...marker.slice(5,8));assert(length>0.9&&length<1.1);
    counts.set(marker[0],(counts.get(marker[0])||0)+1);
  }
  data.points.forEach((point,i)=>assert.equal(counts.get(i),['CV','GV'].includes(point.mer)?1:2,point.code));
});
test('packed anatomy layers have complete buffers and triangle indices within their own vertices',()=>{
  const model=JSON.parse(fs.readFileSync(base+'/model.json','utf8')),pad=n=>(n+3)&~3;
  for(const layer of ['skin','face','bones','muscle','organs','hair']){
    assert(Array.isArray(model[layer])&&model[layer].length);
    for(const b of model[layer]){
      const raw=Buffer.from(b.d,'base64'),offset=pad(b.n*6)+pad(b.n*3)+(b.col?pad(b.n*3):0);
      assert.equal(raw.length,offset+b.m*6);assert(b.lo.every(Number.isFinite)&&b.rng.every(Number.isFinite));
      for(let k=0;k<b.m*3;k++)assert(raw.readUInt16LE(offset+k*2)<b.n,layer);
    }
  }
});
