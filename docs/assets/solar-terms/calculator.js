/* DE440 apparent-longitude interpolation and solar-term root solver. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MinseongSolarTerms = api;
  if (typeof document !== 'undefined') {
    function boot() { document.querySelectorAll('[data-solar-term-calculator]').forEach(api.mount); }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
    else boot();
    if (typeof document$ !== 'undefined') document$.subscribe(boot);
  }
})(typeof window === 'undefined' ? globalThis : window, function () {
  'use strict';
  const OFFSET = 9 * 3600000, DAY = 86400000;
  const TERMS = [
    ['춘분','春分','chunbun'],['청명','淸明','cheongmyeong'],['곡우','穀雨','gogu'],
    ['입하','立夏','ipha'],['소만','小滿','soman'],['망종','芒種','mangjong'],
    ['하지','夏至','haji'],['소서','小暑','soseo'],['대서','大暑','daeseo'],
    ['입추','立秋','ipchu'],['처서','處暑','cheoseo'],['백로','白露','baengno'],
    ['추분','秋分','chubun'],['한로','寒露','hallo'],['상강','霜降','sanggang'],
    ['입동','立冬','ipdong'],['소설','小雪','soseol'],['대설','大雪','daeseol'],
    ['동지','冬至','dongji'],['소한','小寒','sohan'],['대한','大寒','daehan'],
    ['입춘','立春','ipchun'],['우수','雨水','usu'],['경칩','驚蟄','gyeongchip']
  ];
  function yearValue(value, min=1900, max=2100) {
    const text=String(value).trim();
    if (!/^\d{4}$/.test(text)) return null;
    const year=Number(text);
    return year>=min && year<=max ? year : null;
  }
  function chebyshev(coefficients, x) {
    let next=0, after=0;
    for (let i=coefficients.length-1;i>=1;i--) {
      const current=2*x*next-after+coefficients[i]; after=next; next=current;
    }
    return x*next-after+coefficients[0];
  }
  function calculateYear(year, segments, metadata) {
    if (yearValue(year,metadata.startYear,metadata.endYear)===null || metadata.schema!==1 || metadata.model!=='JPL DE440' || metadata.spanDays!==8 || metadata.degree!==14) throw new Error('계산 범위 또는 모델 형식이 맞지 않습니다.');
    const start=Date.UTC(year,0,1)-OFFSET, end=Date.UTC(year+1,0,1)-OFFSET;
    const days=(end-start)/DAY;
    if (!Array.isArray(segments) || segments.length<Math.ceil(days/8) || segments.length>96) throw new Error('해당 연도의 계산 자료가 완전하지 않습니다.');
    const events=[];
    let previousEnd=0;
    segments.forEach(function (segment,i) {
      if (!Array.isArray(segment) || segment.length!==17) throw new Error('황경 구간 형식이 맞지 않습니다.');
      const [first,last,...coefficients]=segment;
      if (Math.abs(first-previousEnd)>1e-8 || !(last>first && last-first<=8.00000001) || last>days) throw new Error('황경 구간이 연속되지 않습니다.');
      previousEnd=last;
      if (!Array.isArray(coefficients) || coefficients.length!==15 || !coefficients.every(Number.isFinite)) throw new Error('황경 자료 형식이 맞지 않습니다.');
      const left=chebyshev(coefficients,-1),right=chebyshev(coefficients,1);
      if (!(right>left && right-left<10)) throw new Error('황경의 진행 방향을 확인할 수 없습니다.');
      for (let k=Math.ceil(left/15);k*15<=right;k++) {
        const target=k*15;
        let lo=-1,hi=1;
        for (let iteration=0;iteration<48;iteration++) {
          const mid=(lo+hi)/2;
          if (chebyshev(coefficients,mid)<target) lo=mid; else hi=mid;
        }
        const milliseconds=start+(first+(last-first)*((lo+hi)/2+1)/2)*DAY;
        const termIndex=((k%24)+24)%24;
        if (milliseconds>=start && milliseconds<end && !events.some(e=>Math.abs(e.milliseconds-milliseconds)<1000)) events.push({termIndex,milliseconds});
      }
    });
    if (Math.abs(previousEnd-days)>1e-8) throw new Error('연말 황경 자료가 빠져 있습니다.');
    events.sort((a,b)=>a.milliseconds-b.milliseconds);
    if (events.length!==24 || new Set(events.map(e=>e.termIndex)).size!==24) throw new Error('24개 절기를 모두 계산하지 못했습니다.');
    return events;
  }
  function displayTime(milliseconds, seconds=false) {
    const rounded=seconds ? Math.round(milliseconds/1000)*1000 : Math.floor((milliseconds+30000)/60000)*60000;
    const iso=new Date(rounded+OFFSET).toISOString();
    return {date:iso.slice(0,10),time:iso.slice(11,seconds?19:16)};
  }
  function defaultYear(now=new Date(),min=1900,max=2100) {
    return Math.min(max,Math.max(min,new Date(now.getTime()+OFFSET).getUTCFullYear()+1));
  }
  const requests=new Map();
  function json(url) {
    if (!requests.has(url)) requests.set(url,fetch(url,{credentials:'same-origin'}).then(r=>{
      if (!r.ok) throw new Error('계산 자료를 불러오지 못했습니다.');
      return r.json();
    }).catch(error=>{requests.delete(url);throw error;}));
    return requests.get(url);
  }
  function mount(element) {
    if (element._solarCalculator) return;
    element._solarCalculator=true;
    const form=element.querySelector('form'),input=element.querySelector('[data-solar-year]');
    const status=element.querySelector('[data-solar-status]'),body=element.querySelector('tbody');
    const caption=element.querySelector('caption'),seconds=element.querySelector('[data-solar-seconds]');
    const official=element.querySelector('[data-solar-official]');
    let generation=0,currentEvents=null,currentYear=null;
    function render() {
      body.replaceChildren();
      currentEvents.forEach(function (event) {
        const term=TERMS[event.termIndex],row=document.createElement('tr'),name=document.createElement('th');
        const link=document.createElement('a');link.href='#'+term[2];link.textContent=term[0]+'('+term[1]+')';
        name.scope='row';name.append(link);row.append(name);
        const value=displayTime(event.milliseconds,seconds.checked);
        [value.date,value.time,event.termIndex*15+'°'].forEach(text=>{const cell=document.createElement('td');cell.textContent=text;row.append(cell);});
        body.append(row);
      });
      caption.textContent=currentYear+'년 24절기 · KST(UTC+9)';
      official.href='https://astro.kasi.re.kr/kor/life/post/almanac?search_year='+currentYear;
      official.textContent=currentYear+'년 월력요항 확인 ↗';
      element.querySelector('[data-solar-step="-1"]').disabled=currentYear===1900;
      element.querySelector('[data-solar-step="1"]').disabled=currentYear===2100;
    }
    async function run(updateUrl=false) {
      const token=++generation,year=yearValue(input.value);
      if (year===null) {status.textContent='1900–2100 사이의 연도를 네 자리 정수로 입력해 주세요.';return;}
      official.href='https://astro.kasi.re.kr/kor/life/post/almanac?search_year='+year;
      official.textContent=year+'년 월력요항 확인 ↗';
      status.textContent=year+'년 절입 시각을 계산하고 있습니다…';
      try {
        const [metadata,data]=await Promise.all([json('/assets/solar-terms/de440/metadata.json?v=20261101'),json('/assets/solar-terms/de440/'+Math.floor(year/10)*10+'.json?v=20261101')]);
        if (token!==generation) return;
        if (data.schema!==1) throw new Error('계산 자료의 형식이 맞지 않습니다.');
        currentEvents=calculateYear(year,data.years[String(year)],metadata);currentYear=year;render();
        status.textContent=year+'년 절기 24개를 계산했습니다. 시각은 '+(seconds.checked?'초 단위 반올림':'가까운 분으로 반올림')+'하여 표시합니다.';
        if (updateUrl) {const url=new URL(location.href);url.searchParams.set('solarYear',String(year));history.replaceState(null,'',url);}
      } catch (error) {
        if (token===generation) status.textContent='계산 자료를 확인할 수 없습니다. 잠시 후 다시 계산하거나 아래의 월력요항 링크를 이용해 주세요.';
      }
    }
    form.addEventListener('submit',event=>{event.preventDefault();run(true);});
    element.querySelectorAll('[data-solar-step]').forEach(button=>button.addEventListener('click',()=>{
      input.value=String((yearValue(input.value)||defaultYear())+Number(button.dataset.solarStep));run(true);
    }));
    element.querySelector('[data-solar-next-year]').addEventListener('click',()=>{input.value=String(defaultYear());run(true);});
    seconds.addEventListener('change',()=>{if(currentEvents){render();status.textContent=currentYear+'년 · '+(seconds.checked?'초 단위 반올림':'가까운 분으로 반올림')+' 표시입니다.';}});
    input.value=String(yearValue(new URL(location.href).searchParams.get('solarYear'))||defaultYear());run();
  }
  return {TERMS,yearValue,chebyshev,calculateYear,displayTime,defaultYear,mount};
});
