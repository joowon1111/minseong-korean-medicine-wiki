/* Start the large 3D assets only on the requested map, preserving instant navigation. */
(function () {
  'use strict';
  const ready = new WeakSet();
  const listeners = new Map();
  const limits = {LU:11,LI:20,ST:45,SP:21,HT:9,SI:19,BL:67,KI:27,PC:9,TE:23,GB:44,LR:14,GV:28,CV:24};
  function validCode(value) {
    const match = /^(LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR|GV|CV)([1-9][0-9]?)$/.exec(value || '');
    return match && Number(match[2]) <= limits[match[1]] ? value : null;
  }
  function init() {
    for (const [root,handler] of listeners) if (!root.isConnected) { window.removeEventListener('message',handler); listeners.delete(root); }
    document.querySelectorAll('[data-acupoint-3d]').forEach(root => {
      if (ready.has(root)) return;
      ready.add(root);
      const frame=root.querySelector('[data-map-frame]'), start=root.querySelector('[data-map-start]');
      const fullscreen=root.querySelector('[data-map-fullscreen]'), direct=root.querySelector('[data-map-direct]');
      const status=root.querySelector('[data-map-status]');
      let code=validCode(new URL(location.href).searchParams.get('point'));
      function target() { const url=new URL('/assets/acupoint-3d/index.html?v=20261012-style',location.origin); if(code) url.searchParams.set('point',code); return url; }
      function open() {
        if (frame.hasAttribute('src')) return;
        frame.src=target().href; frame.hidden=false; start.hidden=true; fullscreen.hidden=false;
        status.textContent='모형을 불러오는 중입니다. 화면 안의 경혈 이름이나 검색창으로 선택하세요.';
      }
      direct.href=target().href;
      start.addEventListener('click',open);
      frame.addEventListener('load',()=>{status.textContent='경혈 점을 선택하거나 이름·코드로 검색하세요. 상세 문서는 지도의 설명 패널에서 열 수 있습니다.';});
      fullscreen.addEventListener('click',async()=>{try {if(root.requestFullscreen) await root.requestFullscreen();else window.open(target().href,'_blank','noopener');}catch(_){status.textContent='전체 화면을 열 수 없습니다. ‘넓은 화면으로 열기’를 이용하세요.';}});
      const onMessage=event=>{
        if(!root.isConnected) {window.removeEventListener('message',onMessage);listeners.delete(root);return;}
        if(event.origin!==location.origin || event.source!==frame.contentWindow || event.data?.type!=='minseong-acupoint-select') return;
        const next=validCode(event.data.code); if(!next) return;
        code=next; const url=new URL(location.href); url.searchParams.set('point',code); history.replaceState(null,'',url);
        direct.href=target().href;
      };
      window.addEventListener('message',onMessage);
      listeners.set(root,onMessage);
      if(code) open();
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
  if(typeof document$!=='undefined') document$.subscribe(init);
})();
