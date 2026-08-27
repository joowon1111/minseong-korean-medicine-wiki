/* Minseong Korean search fallback.
   MkDocs Material remains primary. If it returns no results, this searches
   a compact Korean keyword index generated at build time. */
(function(){
  let idx=null;
  async function loadIndex(){
    if(idx) return idx;
    try{
      const base=(document.querySelector('meta[name="site_url"]')||{}).content||'/';
      const r=await fetch((new URL('assets/korean-search-index.json', document.baseURI)).href);
      idx=await r.json(); return idx;
    }catch(e){ return []; }
  }
  function norm(s){ return (s||'').toLowerCase().replace(/\s+/g,' ').trim(); }
  function score(doc,q){
    let s=0, t=norm(doc.title), k=norm((doc.keywords||[]).join(' ')), x=norm(doc.text);
    if(t===q) s+=100; if(t.includes(q)) s+=50;
    if(k.includes(q)) s+=30; if(x.includes(q)) s+=10;
    return s;
  }
  async function fallback(q){
    q=norm(q); if(!q) return [];
    const data=await loadIndex();
    return data.map(d=>[score(d,q),d]).filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,12).map(x=>x[1]);
  }
  function render(q,docs){
    const container=document.querySelector('.md-search-result__list');
    const meta=document.querySelector('.md-search-result__meta');
    if(!container || !docs.length) return;
    if(meta) meta.textContent='아카이브 보조 검색 결과';
    container.innerHTML='';
    docs.forEach(d=>{
      const a=document.createElement('a');
      a.className='md-search-result__link';
      a.href=d.url;
      a.innerHTML='<article class="md-search-result__article md-typeset"><h1>'+d.title+'</h1><p>'+d.snippet+'</p></article>';
      const li=document.createElement('li'); li.className='md-search-result__item'; li.appendChild(a); container.appendChild(li);
    });
  }
  document.addEventListener('input', async e=>{
    if(!e.target.matches('[data-md-component="search-query"] input, .md-search__input')) return;
    const q=e.target.value;
    if(q.trim().length<1) return;
    setTimeout(async()=>{
      const list=document.querySelector('.md-search-result__list');
      const primaryCount=list ? list.querySelectorAll('.md-search-result__item').length : 0;
      if(primaryCount===0){
        const docs=await fallback(q); render(q,docs);
      }
    },450);
  });
})();