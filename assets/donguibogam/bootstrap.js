/* Load the reader only on its own page, including Material instant navigation. */
(() => {
  let loading;
  function install() {
    const root=document.getElementById('dgb-reader');
    if(!root || root.dataset.dgbReady)return;
    if(globalThis.MinseongDonguiReader){globalThis.MinseongDonguiReader.install(root);return;}
    if(!loading)loading=new Promise((resolve,reject)=>{
      const script=document.createElement('script');script.src='/assets/donguibogam/reader.js';
      script.onload=resolve;script.onerror=()=>{script.remove();reject(new Error('reader'));};document.head.appendChild(script);
    }).then(()=>{const current=document.getElementById('dgb-reader');if(current)globalThis.MinseongDonguiReader.install(current);}).catch(()=>{loading=null;const status=document.getElementById('dgb-status');if(status)status.textContent='열람기를 불러오지 못했습니다. 새로고침하거나 아래 출처를 이용해 주세요.';});
  }
  install();if(typeof document$!=='undefined')document$.subscribe(install);
})();
