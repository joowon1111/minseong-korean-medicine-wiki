/* Same-origin archive integration: fit the document and preserve its selection URL. */
(() => {
  'use strict';
  if (window.parent === window) return;
  const send = (type, extra = {}) => window.parent.postMessage({source:'minseong-sasang',type,...extra}, location.origin);
  let frame = 0;
  const resize = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => send('resize',{height:Math.ceil(document.body.getBoundingClientRect().height)+2}));
  };
  const state = () => {send('state',{hash:location.hash});resize();};
  new ResizeObserver(resize).observe(document.body);
  window.addEventListener('sasang-state-change',state);
  window.addEventListener('hashchange',state);
  window.addEventListener('load',resize);
  document.addEventListener('click', event => {
    const button=event.target.closest('button');
    if(!button) return;
    let target=null;
    if(button.hasAttribute('data-profile-jump') || button.hasAttribute('data-tab')) target=document.getElementById('profile');
    else if(button.hasAttribute('data-c') || button.hasAttribute('data-axis') || button.hasAttribute('data-next') || button.hasAttribute('data-back') || button.hasAttribute('data-step') || button.hasAttribute('data-other') || button.hasAttribute('data-explore') || button.id==='reset') target=document.getElementById('explorer');
    if(target) requestAnimationFrame(()=>send('scroll',{top:target.getBoundingClientRect().top+window.scrollY}));
  });
  send('ready');resize();
})();
