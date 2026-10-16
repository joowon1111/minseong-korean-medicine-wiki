/* Independent classical-text reader. Imported text is rendered as text, never HTML. */
(() => {
  'use strict';
  const BASE = '/assets/donguibogam/';
  const GROUPS = {'tangaek-1':'탕액편 권1', 'tangaek-2':'탕액편 권2', 'tangaek-3':'탕액편 권3', 'naegyeong-fragments':'내경편 권1 확보된 부분'};
  const norm = value => String(value || '').normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
  const validRow = row => row && /^[a-z0-9-]+$/.test(row.id) && typeof row.title === 'string' && typeof row.text === 'string' && Array.isArray(row.aliases) && row.aliases.every(x => typeof x === 'string') && Object.hasOwn(GROUPS,row.group);
  function search(rows, raw, group='') {
    const query = norm(raw).replace(/^동의보감\s*(?:원문\s*)?/, '').trim(); const terms = query.split(' '); if (!query) return [];
    return rows.filter(row => !group || row.group === group).map(row => {
      const title = norm(row.title), aliases = row.aliases.map(norm), text = norm(row.text);
      const blob = [title,...aliases,text].join(' ');
      if (!terms.every(term => blob.includes(term))) return {row,score:0};
      const score = (title === query || aliases.includes(query) ? 1000 : 0) + (title.includes(query) ? 100 : 0) + (aliases.some(a=>a.includes(query)) ? 60 : 0) + (text.includes(query) ? 10 : 0);
      return {row,score};
    }).filter(x=>x.score).sort((a,b)=>b.score-a.score || a.row.id.localeCompare(b.row.id));
  }
  function browse(rows, group='') {
    return rows.filter(row => !group || row.group === group).map(row => ({row,score:1}));
  }
  function pageResults(hits, requested=0) {
    const pages=Math.max(1,Math.ceil(hits.length/50));
    const index=Number.isSafeInteger(requested)?Math.min(Math.max(requested,0),pages-1):0;
    return {index,pages,total:hits.length,items:hits.slice(index*50,(index+1)*50)};
  }
  const internal = url => typeof url === 'string' && /^\/(?!\/)/.test(url) && !/[\\\x00-\x20\x7f]/.test(url);
  function external(url, hosts) { try { const u = new URL(url); return u.protocol === 'https:' && hosts.includes(u.hostname) && !u.username && !u.password ? u.href : null; } catch { return null; } }
  function imageURL(scan, page) {
    if (!scan || !Number.isInteger(page) || page < 1 || page > scan.pages) return null;
    const url = external(scan.thumbnail,['thumb.wikimedia.org','upload.wikimedia.org']);
    return url && /\/page1-\d+px-/.test(url) ? url.replace(/\/page1-(\d+)px-/, `/page${page}-$1px-`) : null;
  }
  function install(root) {
    if (!root || root.dataset.dgbReady) return;
    root.dataset.dgbReady='true';
    const get = id => root.querySelector('#'+id);
    const status=get('dgb-status'), results=get('dgb-results'), passage=get('dgb-passage');
    let manifest=null, corpus=null, loading=null, generation=0, selectedScan=null,selectedPage=1;
    const make=(tag,text,parent)=>{const node=document.createElement(tag);if(text != null)node.textContent=text;if(parent)parent.appendChild(node);return node;};
    const link=(label,url,parent,isExternal=false)=>{const safe=isExternal ? external(url,['ko.wikisource.org','zh.wikisource.org','commons.wikimedia.org','upload.wikimedia.org','creativecommons.org']) : internal(url) ? url : null;if(!safe)return;const a=make('a',label,parent);a.href=safe;if(isExternal){a.target='_blank';a.rel='noopener';}return a;};
    async function fetchJSON(file) { const response=await fetch(BASE+file+'?v=2');if(!response.ok)throw new Error('download');return response.json(); }
    const manifestPromise=fetchJSON('manifest.json').then(data=>{
      if(data.schema!==1 || !Array.isArray(data.sources) || !Array.isArray(data.scans) || !data.groups)throw new Error('manifest');
      manifest=data;
      const guide=get('dgb-volume-guide');
      for(const division of ['내경편','외형편','잡병편','탕액편','침구편','목록']){
        const scans=data.scans.filter(s=>s.division===division&&imageURL(s,1)).sort((a,b)=>a.volume-b.volume);
        if(!scans.length)continue;
        const options=make('optgroup',null,get('dgb-volume'));options.label=division;
        const section=make('details',null,guide);make('summary',division+' · '+scans.length+'권',section);
        const list=make('ul',null,section);
        for(const scan of scans){
          const opt=make('option',scan.title+' · 제'+scan.number+'책 · '+scan.pages+'쪽',options);opt.value=scan.number;
          const item=make('li',null,list),button=make('button',scan.title,item);button.type='button';
          make('span',' '+scan.topics,item);
          button.addEventListener('click',()=>{get('dgb-volume').value=scan.number;showScan(scan.opening_page);get('dgb-scan').scrollIntoView({behavior:'smooth',block:'start'});});
        }
      }
      const firstScan=data.scans.find(scan=>imageURL(scan,1));if(firstScan)get('dgb-page').max=firstScan.pages;
      status.textContent='원문 검색 준비 완료. 전사 '+Object.values(data.groups).reduce((sum,g)=>sum+g.count,0)+'개 항목을 별도로 검색합니다.';
      return data;
    }).catch(()=>{status.textContent='원문 목록을 불러오지 못했습니다. 새로고침하거나 아래 출처를 이용해 주세요.';return null;});
    async function loadCorpus() {
      if(corpus)return corpus;
      if(!loading)loading=manifestPromise.then(async data=>{
        if(!data)throw new Error('manifest');
        const groups=Object.entries(data.groups);
        const lists=await Promise.all(groups.map(async ([group,entry])=>{
          if(!Object.hasOwn(GROUPS,group) || entry.file!==group+'.json')throw new Error('group');
          const list=await fetchJSON(entry.file);
          if(!Array.isArray(list) || list.length!==entry.count || !list.every(validRow))throw new Error('corpus');return list;
        }));corpus=lists.flat();return corpus;
      }).catch(error=>{loading=null;throw error;});
      return loading;
    }
    function remember(values) {const params=new URLSearchParams(values);history.replaceState(null,'',location.pathname+'?'+params.toString()+'#reader');}
    function showPassage(row) {
      passage.replaceChildren();passage.hidden=false;
      make('h3', [row.aliases.join(' · '),row.title].filter(Boolean).join(' — '),passage);
      make('p',GROUPS[row.group],passage);
      const source=manifest.sources.find(s=>s.id===row.source);
      if(source){make('p',source.title+' · '+source.quality,passage);const p=make('p',null,passage);link('사용한 수정판',source.url,p,true);make('span',' · ',p);link('전사 기여 이력',source.history,p,true);make('span',' · ',p);link('CC BY-SA 4.0',manifest.license,p,true);}
      const body=make('div',null,passage);body.className='dgb-original-text';
      // Preserve literal wording; paragraph breaks at the source's circular markers only.
      for(const text of row.text.split(/(?=○)/))if(text.trim())make('p',text.trim(),body);
      if(row.scan_page){const p=make('p',null,passage);link('전사에 대응하는 영인 페이지', 'https://ko.wikisource.org/wiki/'+encodeURIComponent(row.scan_page),p,true);}
      if(row.links?.length){const p=make('p','아카이브에서 이어 읽기: ',passage);for(const item of row.links){link(item.title,item.url,p);make('span',' ',p);}}
      remember({record:row.id});passage.scrollIntoView({behavior:'smooth',block:'start'});
    }
    async function runSearch(event, requested=0) {
      event?.preventDefault();const current=++generation;const query=get('dgb-query').value.trim(),group=get('dgb-group').value;
      status.textContent=query?'원문 전사에서 찾고 있습니다.':'수록된 원문 목록을 불러옵니다.';
      try{
        const rows=await loadCorpus();if(current!==generation || !root.isConnected)return;
        const hits=query?search(rows,query,group):browse(rows,group);
        function render(index){
          if(current!==generation||!root.isConnected)return;
          const page=pageResults(hits,index);results.replaceChildren();passage.hidden=true;
          status.textContent=(query?'검색 결과 ':'원문 목록 ')+page.total+'개 항목'+(page.total?' · '+(page.index*50+1)+'–'+Math.min((page.index+1)*50,page.total)+'번째':'');
          for(const {row} of page.items){
            const item=make('div',null,results);item.className='dgb-result';const button=make('button',[row.aliases.join(' · '),row.title].filter(Boolean).join(' — '),item);button.type='button';button.addEventListener('click',()=>showPassage(row));
            make('small',GROUPS[row.group]+(row.context_title?' · '+row.context_title+'의 부위 항목':''),item);make('p',row.text.slice(0,180)+(row.text.length>180?'…':''),item);
          }
          if(!hits.length)make('p','이 검색 결과는 현재 수록한 전사 범위에 한정됩니다. 영인본 전권의 모든 글자가 검색되는 상태는 아닙니다.',results);
          if(page.pages>1){
            const controls=make('nav',null,results);controls.className='dgb-controls';controls.setAttribute('aria-label','원문 결과 페이지');
            const prev=make('button','이전 50항목',controls);prev.type='button';prev.disabled=page.index===0;
            make('span',(page.index+1)+' / '+page.pages,controls);
            const next=make('button','다음 50항목',controls);next.type='button';next.disabled=page.index===page.pages-1;
            prev.addEventListener('click',()=>{render(page.index-1);results.scrollIntoView({behavior:'smooth',block:'start'});});
            next.addEventListener('click',()=>{render(page.index+1);results.scrollIntoView({behavior:'smooth',block:'start'});});
          }
          remember({...(query?{q:query}:{list:1}),...(group?{group}:{}),...(page.index?{offset:page.index*50}:{})});
        }
        render(requested);
      }catch{if(current===generation)status.textContent='전사를 불러오지 못했습니다. 다시 검색하거나 아래 출처를 이용해 주세요.';}
    }
    function showScan(page) {
      const scan=manifest?.scans.find(s=>s.number===Number(get('dgb-volume').value));const url=imageURL(scan,page);
      if(!url){get('dgb-scan').hidden=false;get('dgb-scan-status').textContent='책과 유효한 페이지 번호를 선택해 주세요.';return;}
      selectedScan=scan;selectedPage=page;get('dgb-page').max=scan.pages;get('dgb-page').value=page;get('dgb-scan').hidden=false;
      get('dgb-scan-status').textContent=scan.title+' · 이미지 '+page+'/'+scan.pages+'쪽';
      const img=get('dgb-scan-image');img.alt=scan.title+' 이미지 '+page+'쪽';img.src=url;get('dgb-scan-image-link').href=url;
      get('dgb-scan-source').href=external(scan.source,['commons.wikimedia.org']);get('dgb-scan-pdf').href=external(scan.pdf,['upload.wikimedia.org']);
      get('dgb-prev').disabled=page<=1;get('dgb-next').disabled=page>=scan.pages;remember({volume:scan.number,page});
    }
    get('dgb-search-form').addEventListener('submit',runSearch);
    get('dgb-browse').addEventListener('click',()=>{get('dgb-query').value='';runSearch();});
    get('dgb-scan-form').addEventListener('submit',async e=>{e.preventDefault();await manifestPromise;showScan(Number(get('dgb-page').value));});
    get('dgb-volume').addEventListener('change',()=>{selectedScan=null;get('dgb-scan').hidden=true;get('dgb-page').value=1;const scan=manifest?.scans.find(s=>s.number===Number(get('dgb-volume').value));if(scan)get('dgb-page').max=scan.pages;});
    get('dgb-prev').addEventListener('click',()=>selectedScan&&showScan(selectedPage-1));
    get('dgb-next').addEventListener('click',()=>selectedScan&&showScan(selectedPage+1));
    get('dgb-scan-image').addEventListener('error',()=>{get('dgb-scan-status').textContent='이미지 제공처에서 페이지를 불러오지 못했습니다. 아래 책 전체 PDF 또는 출처에서 확인할 수 있습니다.';});
    const params=new URLSearchParams(location.search);
    if(params.get('q')||params.get('list')){get('dgb-query').value=(params.get('q')||'').slice(0,200);get('dgb-group').value=Object.hasOwn(GROUPS,params.get('group'))?params.get('group'):'';runSearch(null,Number(params.get('offset')||0)/50);}
    else if(params.get('record'))loadCorpus().then(rows=>{const row=rows.find(r=>r.id===params.get('record'));if(row&&root.isConnected)showPassage(row);else status.textContent='해당 원문 항목을 찾지 못했습니다. 검색어로 찾아 주세요.';}).catch(()=>{status.textContent='원문을 불러오지 못했습니다. 다시 검색해 주세요.';});
    else if(params.get('volume'))manifestPromise.then(()=>{get('dgb-volume').value=params.get('volume');showScan(Number(params.get('page')||1));});
  }
  globalThis.MinseongDonguiReader={install,search,browse,pageResults,validRow,imageURL};
  if(typeof module!=='undefined'&&module.exports)module.exports=globalThis.MinseongDonguiReader;
})();
