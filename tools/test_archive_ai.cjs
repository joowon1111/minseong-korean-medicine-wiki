const test=require('node:test');
const assert=require('node:assert/strict');
const client=require('../docs/assets/archive-tools/ai-client.js');
const worker=import('../services/archive-ai/worker.mjs');
const rows=[
  {title:'사군자탕',heading:'구성',kind:'formula',url:'/formulas/sijunzi-tang/',text:'사군자탕은 인삼 백출 복령 감초로 구성된다.'},
  {title:'육군자탕',heading:'구성',kind:'formula',url:'/formulas/liujunzi-tang/',text:'육군자탕은 사군자탕에 반하와 진피를 더한 처방이다.'},
  {title:'불면 연구',heading:'결과',kind:'evidence',url:'/research/sleep/',text:'불면 환자의 수면 결과를 비교한 연구이며 자료에 한계가 있다.'},
];
const good={sufficient:true,paragraphs:[{text:'사군자탕의 구성은 인삼·백출·복령·감초입니다.',source_ids:['S1']}],quotes:[{source_id:'S1',quote:rows[0].text}],limitations:'발췌에 없는 용량은 확인할 수 없습니다.'};
const request=(payload={question:'사군자탕 구성',kind:''},headers={})=>new Request('https://server.example/answer',{method:'POST',headers:{Origin:'https://wiki.minseong.co.kr','Content-Type':'application/json','CF-Connecting-IP':'192.0.2.1',...headers},body:JSON.stringify(payload)});
const modelResponse=value=>Response.json({status:'completed',output:[{type:'message',content:[{type:'output_text',text:JSON.stringify(value)}]}]});
function fixture(options={}) {
  const calls=[], limiter=[];
  const env={OPENAI_API_KEY:'fixture-only',AI_RATE_LIMITER:{limit:async ({key})=>{limiter.push(key);return {success:options.allowed!==false};}}};
  const fetcher=async (url,init)=>{
    calls.push({url,init});
    if (url.includes('passages.json')) return options.archiveError ? new Response('',{status:502}) : Response.json({schema:1,passages:options.rows||rows});
    const payload=JSON.parse(init.body);
    if (payload.text.format.name==='archive_queries') return options.expansionError ? new Response('private diagnostic',{status:502}) : modelResponse({queries:options.queries||['사군자탕']});
    return options.providerError ? new Response('private diagnostic',{status:401}) : modelResponse(options.answer||good);
  };
  return {env,fetcher,calls,limiter};
}
test('retrieval keeps named formulas, supplements aliases, scopes kind and bounds sources',async()=>{
  const {retrieve}=await worker;
  const found=retrieve(rows,'사군자탕과 육군자탕의 차이',['불면'],'formula');
  assert.ok(found.some(r=>r.title==='사군자탕')); assert.ok(found.some(r=>r.title==='육군자탕'));
  assert.ok(found.every(r=>r.kind==='formula')); assert.ok(found.length<=10);
  assert.deepEqual(retrieve(rows,'존재하지않음',[],''),[]);
});
test('valid answers require actual supporting quotations for every cited source',async()=>{
  const {validateAnswer}=await worker, sources=rows.map((r,i)=>({...r,id:'S'+(i+1)}));
  const answer=validateAnswer(good,sources); assert.equal(client.validAnswer(answer),true); assert.equal(answer.sources.length,1);
  for (const mutated of [
    {...good,paragraphs:[{text:'invented',source_ids:['S999']}]},
    {...good,quotes:[{source_id:'S1',quote:'자료에 없는 발췌를 창작한 문구'}]},
    {...good,quotes:[]},
    {...good,paragraphs:[{text:'unsupported',source_ids:[]}]},
    {...good,sufficient:true,paragraphs:[]},
  ]) assert.throws(()=>validateAnswer(mutated,sources));
  assert.equal(client.validAnswer({...answer,sources:[{...answer.sources[0],url:'javascript:alert(1)'}]}),false);
  assert.equal(client.validAnswer({...answer,sources:[{...answer.sources[0],url:'/\\external.com'}]}),false);
  assert.equal(client.validAnswer({...answer,quotes:[{source_id:'S1',quote:'가짜 발췌를 만든 경우'}]}),false);
});
test('server retrieves trusted data, ignores no browser sources and returns source links',async()=>{
  const {createWorker}=await worker, f=fixture(), service=createWorker(f);
  const response=await service.fetch(request(),f.env), answer=await response.json();
  assert.equal(response.status,200); assert.equal(answer.sources[0].url,rows[0].url);
  assert.equal(client.validAnswer(answer),true); assert.equal(response.headers.get('Cache-Control'),'no-store');
  assert.equal(response.headers.get('Access-Control-Allow-Origin'),'https://wiki.minseong.co.kr');
  assert.deepEqual(f.limiter,['ip:192.0.2.1']);
  const models=f.calls.filter(c=>c.url.includes('/responses')).map(c=>JSON.parse(c.init.body));
  assert.equal(models.length,2); assert.ok(models.every(p=>p.store===false && p.text.format.strict===true));
  const sent=JSON.parse(models[1].input); assert.equal(sent.sources[0].id,'S1'); assert.equal(sent.sources[0].url,rows[0].url);
  await service.fetch(request(),f.env); assert.equal(f.calls.filter(c=>c.url.includes('passages.json')).length,1);
});
test('server rejects untrusted origins, browser-provided sources, malformed/large input before model calls',async()=>{
  const {createWorker}=await worker, f=fixture(), service=createWorker(f);
  for (const [req,expected] of [[request({}, {Origin:'https://evil.example'}),403],[request({question:'test',sources:rows}),400],[request({question:'x'.repeat(501)}),400],[request({question:'test',kind:'not-a-kind'}),400],[request({question:'x'.repeat(4000)}),413],[request({}, {'Content-Type':'text/plain'}),400]]) assert.equal((await service.fetch(req,f.env)).status,expected);
  assert.equal(f.calls.length,0);
  const preflight=await service.fetch(new Request('https://server.example/answer',{method:'OPTIONS',headers:{Origin:'https://wiki.minseong.co.kr'}}),f.env);
  assert.equal(preflight.status,204);
});
test('unconfigured server, throttling, provider failure and citation failure fail closed',async()=>{
  const {createWorker}=await worker;
  for (const [options,error,status] of [[{allowed:false},'rate_limited',429],[{providerError:true},'provider_unavailable',503],[{archiveError:true},'archive_unavailable',503],[{answer:{...good,quotes:[]}},'invalid_citation',503]]) {
    const f=fixture(options), r=await createWorker(f).fetch(request(),f.env); assert.equal(r.status,status); assert.deepEqual(await r.json(),{error});
  }
  const f=fixture(); const service=createWorker(f); const r=await service.fetch(request(),{});
  assert.deepEqual(await r.json(),{error:'not_configured'}); assert.equal(f.calls.length,0);
  const health=await service.fetch(new Request('https://server.example/health'),{}); assert.equal((await health.json()).ready,false);
});
test('no matches produce an explicit insufficiency; expansion failures retain exact retrieval',async()=>{
  const {createWorker}=await worker;
  const missing=fixture({queries:[]}); const r=await createWorker(missing).fetch(request({question:'아무자료없음'}),missing.env);
  const d=await r.json(); assert.equal(d.sufficient,false); assert.deepEqual(d.sources,[]); assert.equal(client.validAnswer(d),true);
  assert.equal(missing.calls.filter(c=>c.url.includes('/responses')).length,1);
  const fallback=fixture({expansionError:true}); assert.equal((await createWorker(fallback).fetch(request(),fallback.env)).status,200);
});
test('endpoint config permits only HTTPS bases without credentials or URL decorations',()=>{
  assert.equal(client.endpoint('https://server.example/'),'https://server.example');
  for (const url of ['http://server.example','https://user:pass@server.example','https://server.example?q=1','javascript:alert(1)','https://server.example/#key','https://server.example:8080']) assert.equal(client.endpoint(url),null);
});
