(function(global) {
  'use strict';
  const messages={not_configured:'AI 서버 연결을 준비 중입니다. 근거 자료 검색과 질문·출처 복사를 이용해 주세요.',rate_limited:'요청이 많습니다. 1분 뒤 다시 시도하세요.',provider_busy:'AI 제공 서버가 혼잡합니다. 잠시 뒤 다시 시도하세요.',invalid_citation:'답변의 인용을 검증하지 못했습니다. 원문을 확인하거나 다시 질문하세요.',answer_refused:'이 질문에 대한 AI 답변을 제공할 수 없습니다.',archive_unavailable:'아카이브 자료에 연결하지 못했습니다. 잠시 뒤 다시 시도하세요.'};
  function endpoint(value) {
    try {const u=new URL(value); return u.protocol==='https:' && !u.username && !u.password && !u.search && !u.hash && (!u.port || u.port==='443') ? u.href.replace(/\/$/,'') : null;} catch {return null;}
  }
  function validAnswer(d) {
    if (!d || d.schema!==1 || typeof d.sufficient!=='boolean' || !Array.isArray(d.paragraphs) || !Array.isArray(d.sources) || !Array.isArray(d.quotes) || typeof d.limitations!=='string') return false;
    if (d.paragraphs.length>8 || d.sources.length>10 || d.quotes.length>20 || d.limitations.length>1200) return false;
    const ids=new Set();
    for (const s of d.sources) {if (!s || !/^S\d+$/.test(s.id) || ids.has(s.id) || typeof s.title!=='string' || typeof s.heading!=='string' || typeof s.text!=='string' || !/^\/(?!\/)[^\s<>\\]*$/.test(s.url)) return false; ids.add(s.id);}
    const quoted=new Set();
    const norm=s=>s.normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
    for (const q of d.quotes) {if (!q) return false; const s=d.sources.find(s=>s.id===q.source_id); if (!s || typeof q.quote!=='string' || q.quote.trim().length<8 || q.quote.length>600 || !norm(s.text).includes(norm(q.quote))) return false; quoted.add(q.source_id);}
    return (!d.sufficient || d.paragraphs.length>0) && d.paragraphs.every(p=>p && typeof p.text==='string' && p.text.trim() && p.text.length<=1800 && Array.isArray(p.source_ids) && p.source_ids.length>0 && p.source_ids.length<=10 && p.source_ids.every(id=>ids.has(id) && quoted.has(id)));
  }
  const api={endpoint,validAnswer}; if (typeof module!=='undefined' && module.exports) module.exports=api;
  if (!global.document) return;
  const make=(tag,text,attrs={})=>{const e=global.document.createElement(tag); if (text!==undefined) e.textContent=text; for (const [key,value] of Object.entries(attrs)) e.setAttribute(key,value); return e;};
  let configuration;
  function config() {
    if (!configuration) {
      configuration=global.fetch('/assets/archive-tools/ai-config.json',{cache:'no-store'}).then(async r=>{if (!r.ok) return null; const d=await r.json(); return d.schema===1 ? endpoint(d.endpoint) : null;});
      configuration.catch(()=>{configuration=undefined;});
    }
    return configuration;
  }
  api.mount=function(root,question,kind) {
    const section=make('section',undefined,{class:'archive-ai','aria-label':'아카이브 AI 답변'}), title=make('h3','아카이브 AI 답변'), status=make('p','AI 서버 연결을 확인하고 있습니다.',{role:'status'}), output=make('div'), generate=make('button','출처 기반 AI 답변 생성',{type:'button',disabled:''}), cancel=make('button','생성 취소',{type:'button',hidden:''}), controls=make('div',undefined,{class:'archive-controls'});
    const disclosure=make('p','생성을 누르면 질문과 아카이브 발췌가 AI 서버와 OpenAI에 전송됩니다. 이름·연락처·환자 개인정보는 입력하지 마세요. 답변의 근거 문단을 함께 확인할 수 있습니다.');
    controls.append(generate,cancel); section.append(title,status,disclosure,controls,output); section.hidden=true;
    let server=null, controller=null, sequence=0;
    config().then(async value=>{
      if (!value) return;
      const response=await global.fetch(value+'/health',{signal:AbortSignal.timeout(8000)}); const health=await response.json();
      if (response.ok && health.schema===1 && health.ready===true && health.provider==='OpenAI' && health.archive==='https://wiki.minseong.co.kr') server=value;
    }).catch(()=>{}).finally(()=>{if (sequence!==0 || !root.isConnected || !server) return; root.prepend(section); section.hidden=false; generate.disabled=false; status.textContent=server ? '검색한 질문을 바탕으로 아카이브 자료를 다시 찾아 답변을 생성합니다.' : messages.not_configured; disclosure.hidden=!server;});
    cancel.addEventListener('click',()=>{sequence++; controller?.abort(); controller=null; generate.disabled=!server; cancel.hidden=true; status.textContent='답변 생성을 취소했습니다.'; section.removeAttribute('aria-busy');});
    generate.addEventListener('click',async()=>{
      if (!server || controller) return;
      const ticket=++sequence; controller=new AbortController(); const activeController=controller; const timer=global.setTimeout(()=>activeController.abort(),75000);
      generate.disabled=true; cancel.hidden=false; output.replaceChildren(); section.setAttribute('aria-busy','true'); status.textContent='관련 문서 검색과 인용 검증을 진행하고 있습니다…';
      try {
        const response=await global.fetch(server+'/answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,kind}),signal:controller.signal});
        const d=await response.json(); if (ticket!==sequence || !section.isConnected) return;
        if (!response.ok) {status.textContent=messages[d.error] || 'AI 답변을 생성하지 못했습니다. 잠시 뒤 다시 시도하세요. 근거 검색 결과는 계속 이용할 수 있습니다.'; return;}
        if (!validAnswer(d)) {status.textContent=messages.invalid_citation; return;}
        status.textContent=d.sufficient ? 'AI 생성 답변 · 각 문단의 출처와 실제 발췌를 확인하세요.' : '자료가 부족해 질문 전체에 답할 수 없습니다.';
        for (const p of d.paragraphs) {
          const paragraph=make('p',p.text), refs=make('span',undefined,{class:'archive-ai-refs'});
          for (const id of [...new Set(p.source_ids)]) {const source=d.sources.find(s=>s.id===id); refs.append(make('a','['+id+']',{href:source.url,title:source.title+' / '+source.heading}));}
          paragraph.append(refs); output.append(paragraph);
        }
        if (d.limitations) output.append(make('p',d.limitations,{class:'archive-ai-limitations'}));
        if (d.sources.length) output.append(make('h4','답변에 사용한 근거'));
        for (const s of d.sources) {const detail=make('details'); detail.append(make('summary','['+s.id+'] '+s.title+' / '+s.heading)); for (const q of d.quotes.filter(q=>q.source_id===s.id)) detail.append(make('blockquote',q.quote)); detail.append(make('a','본문과 출처 확인',{href:s.url})); output.append(detail);}
      } catch (error) {if (ticket===sequence && section.isConnected) status.textContent=error.name==='AbortError' ? '응답 대기 시간이 지났습니다. 다시 시도하세요.' : 'AI 서버에 연결하지 못했습니다. 잠시 뒤 다시 시도하세요.';}
      finally {global.clearTimeout(timer); if (ticket===sequence) {controller=null; generate.disabled=!server; cancel.hidden=true; section.removeAttribute('aria-busy');}}
    });
    return ()=>{sequence++; controller?.abort();};
  };
  global.MinseongArchiveAI=api;
})(typeof window==='undefined' ? globalThis : window);
