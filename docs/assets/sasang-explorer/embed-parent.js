(() => {
  'use strict';
  const iframe=document.getElementById('sasang-explorer-frame');
  if(!iframe || iframe.dataset.connected) return;
  iframe.dataset.connected='true';
  const isState=hash=>/^#(?:c=|s=)/.test(hash) && hash.length<2000;
  const sync=()=>{
    if(!iframe.contentWindow) return;
    const hash=isState(location.hash)?location.hash:'';
    if(iframe.contentWindow.location.hash!==hash) iframe.contentWindow.location.hash=hash;
  };
  iframe.addEventListener('load',sync);
  window.addEventListener('hashchange',sync);
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin || event.source!==iframe.contentWindow) return;
    const data=event.data;
    if(!data || data.source!=='minseong-sasang') return;
    if(data.type==='ready') sync();
    if(data.type==='resize' && Number.isFinite(data.height)) iframe.style.height=Math.max(600,Math.min(30000,data.height))+'px';
    if(data.type==='state' && typeof data.hash==='string' && isState(data.hash) && data.hash!==location.hash) history.replaceState(null,'',location.pathname+location.search+data.hash);
    if(data.type==='scroll' && Number.isFinite(data.top)) window.scrollTo({top:Math.max(0,iframe.getBoundingClientRect().top+window.scrollY+data.top-85),behavior:'auto'});
  });
})();
