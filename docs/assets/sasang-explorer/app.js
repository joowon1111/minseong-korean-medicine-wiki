'use strict';
const root='https://wiki.minseong.co.kr';
const META={'소양인':['少陽人','비수한표한 · 위수열리열','배변·갈증·수면·진액의 변화'],'태음인':['太陰人','위완수한표한 · 간수열리열','발한·호흡·건조·회복의 변화'],'소음인':['少陰人','신수열표열 · 위수한리한','소화·땀·냉감·기력의 변화'],'태양인':['太陽人','외감요척 · 내촉소장','보행·연하·섭취·배뇨의 변화']};
const labels=['체질 선택','병증 탐색','원문·감별','대표 처방'];
let state={step:0,c:'',axis:''};
const el=id=>document.getElementById(id);
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link=(path,text,cls='')=>`<a class="${cls}" href="${root+path}" target="_blank" rel="noopener">${text}</a>`;
function selected(){return D.find(x=>x[0]===state.c&&x[1]===state.axis)}
function maxStep(){return state.axis?3:state.c?1:0}
function restore(){const q=new URLSearchParams(location.hash.slice(1));const c=q.get('c');const a=q.get('a');profileTab=PROFILE_TABS.some(x=>x[0]===q.get('t'))?q.get('t'):'constitution';state={step:0,c:META[c]?c:'',axis:''};if(D.some(x=>x[0]===state.c&&x[1]===a))state.axis=a;state.step=Math.max(0,Math.min(Math.trunc(Number(q.get('s')))||0,maxStep()));render(false)}
function save(){const q=new URLSearchParams();if(state.c)q.set('c',state.c);if(state.axis)q.set('a',state.axis);q.set('s',state.step);if(state.c)q.set('t',profileTab);history.replaceState(null,'','#'+q);window.dispatchEvent(new Event('sasang-state-change'))}
function render(focus=false){
 el('steps').innerHTML=labels.map((x,i)=>`<button data-step="${i}" ${i>maxStep()?'disabled':''} ${i===state.step?'aria-current="step"':''} class="${i===state.step?'active':''}"><span>${i+1}</span>${x}</button>`).join('');
 el('trail').innerHTML=state.c?`<strong>${esc(state.c)}</strong>${state.axis?`<strong>${esc(state.axis)}</strong>`:'<small>병증군을 선택해 주세요</small>'}`:'<small>체질 → 병증 → 감별 → 처방</small>';
 let html='';const row=selected();
 if(state.step===0){html='<p class="eyebrow">01 · CONSTITUTION</p><h2 tabindex="-1">어떤 체질을 살펴볼까요?</h2><p class="intro">나의 체질을 판정하는 검사가 아닙니다. 학습하려는 체질을 선택하세요.</p><div class="cards">'+Object.entries(META).map(([c,m])=>`<button class="card ${state.c===c?'selected':''}" data-c="${c}" aria-pressed="${state.c===c}"><span class="han" aria-hidden="true">${m[0]}</span><b>${c}</b><small>${m[1]}<br>${m[2]}</small><span class="count">${AXIS_ORDER[c].length}개 병증군 살펴보기 →</span></button>`).join('')+'</div>'}
 if(state.step===1){html=`<p class="eyebrow">02 · PATTERN</p><h2 tabindex="-1">${state.c}의 병증 흐름</h2><p class="intro">${META[state.c][1]}<br>아래 항목은 학습용 분류입니다. 증상 하나만으로 병증을 확정하지 않습니다.</p><input class="search" id="search" type="search" aria-label="병증·한자 원문·조문·처방 검색" placeholder="병증·한자·조문 번호·처방으로 검색"><div class="cards" id="axes"></div><p id="result-count" class="intro" role="status"></p>`}
 if(state.step===2){html=`<p class="eyebrow">03 · DIFFERENTIAL</p><h2 tabindex="-1">${esc(row[2])}</h2><p class="intro">${state.c} · ${esc(state.axis)}</p><div class="summary-box"><strong>핵심으로 살펴볼 모습</strong><p>${esc(row[3])}</p></div>${renderSource(row)}<h3 style="margin-top:26px">함께 확인할 감별 포인트</h3><ol class="points">${row[4].map(p=>`<li>${esc(p)}</li>`).join('')}</ol><p class="intro">평소 상태 → 발병 뒤 변화 → 회복 경과를 함께 살펴보세요. 현재 병증과 체질은 서로 다른 판단입니다.</p>${renderComparisons(row)}`}
 if(state.step===3){html=`<p class="eyebrow">04 · FORMULA & READING</p><h2 tabindex="-1">연결해서 읽을 대표 처방</h2><p class="intro">${state.c} · ${esc(row[2])}<br>이 병증과 연결된 학습 문서입니다. 개인별 복용 처방이나 용량을 제안하지 않습니다.</p><div class="cards">${row[5].map(f=>link(f[1],`<strong>${esc(f[0])} ↗</strong><span>${esc(f[2])}</span>`,'formula')).join('')}</div><div class="summary-box" style="margin-top:24px"><strong>이 병증에서 처방을 비교할 때</strong><p>${esc(patternSource(row).formula)}</p><p>이름이 같아도 문헌·체계에 따라 구성이 다를 수 있습니다. 출전, 적용 병증, 약재 구성과 감별 처방을 상세 문서에서 함께 확인하세요.</p></div><div class="links">${LINKS[state.c].map(l=>link(l[1],esc(l[0])+' ↗')).join('')}</div>`}
 el('content').innerHTML=html+(state.c?'<button class="profile-jump" data-profile-jump>소증 · 음식 · 양생 · 운동 · 한의원 진료 안내 ↓</button>':'');renderProfile();
 if(state.step===1)renderAxes('');
 el('navigation').innerHTML=(state.step>0?'<button data-back>← 이전 단계</button>':'')+(state.step<3?`<button class="next" data-next ${state.step===0&&!state.c||state.step===1&&!state.axis?'disabled':''}>${labels[state.step+1]} →</button>`:'<button class="next" data-other>다른 병증 살펴보기 →</button>');save();if(focus){el('content').querySelector('h2').focus({preventScroll:true});el('explorer').scrollIntoView({behavior:'auto',block:'start'})}}
function renderAxes(query){
 const terms=query.normalize('NFKC').trim().toLowerCase().split(/\s+/).filter(Boolean);
 const rows=AXIS_ORDER[state.c].map(a=>D.find(x=>x[0]===state.c&&x[1]===a)).filter(row=>terms.every(term=>sourceSearchText(row).includes(term)));
 el('axes').innerHTML=rows.length?rows.map(x=>`<button class="card axis ${state.axis===x[1]?'selected':''}" data-axis="${esc(x[1])}" aria-pressed="${state.axis===x[1]}"><span class="axis-route">${esc(patternSource(x).route)}</span><b>${esc(x[1])}</b><small>${esc(x[2])} · 처방 ${x[5].length}개</small><span class="axis-source">${esc(patternSource(x).kind)} · 원문·풀이</span></button>`).join(''):'<p class="empty">일치하는 항목이 없습니다. 다른 단어로 검색해 주세요.</p>';
 el('result-count').textContent=`${rows.length} / ${AXIS_ORDER[state.c].length}개 병증군`;
}
 document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||b.disabled)return;if(b.dataset.c){state.c=b.dataset.c;state.axis='';state.step=1;profileTab='constitution'}else if(b.dataset.axis){state.axis=b.dataset.axis;state.step=2}else if(b.dataset.step!==undefined){state.step=Number(b.dataset.step)}else if(b.hasAttribute('data-next')){state.step++}else if(b.hasAttribute('data-back')){state.step--}else if(b.hasAttribute('data-other')){state.step=1;state.axis=''}else if(b.id==='reset'){state={step:0,c:'',axis:''};profileTab='constitution'}else{return}render(true)});
 document.addEventListener('input',e=>{if(e.target.id==='search')renderAxes(e.target.value)});window.addEventListener('hashchange',restore);restore();
