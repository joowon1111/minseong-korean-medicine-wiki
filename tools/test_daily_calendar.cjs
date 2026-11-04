const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const calendar=require('../docs/assets/daily-korean-medicine/calendar-core.js');
const terms=require('../docs/assets/solar-terms/calculator.js');
const dir='docs/assets/solar-terms/de440/';
const metadata=JSON.parse(fs.readFileSync(dir+'metadata.json'));
const yearEvents=year=>terms.calculateYear(year,JSON.parse(fs.readFileSync(dir+Math.floor(year/10)*10+'.json')).years[String(year)],metadata);
// Independent KASI monthly reference table: https://astro.kasi.re.kr/kor/life/post/calendarData?search_year=2026
test('Korean lunar dates match KASI month starts, including the Korean/Chinese date difference',()=>{
  const starts=[[2,17,1],[3,19,2],[4,17,3],[5,17,4],[6,15,5],[7,14,6],[8,13,7],[9,11,8],[10,11,9],[11,9,10],[12,9,11]];
  for(const[m,d,lunarMonth]of starts)assert.deepEqual(calendar.lunarFor(new Date(Date.UTC(2026,m-1,d))),{year:2026,month:lunarMonth,day:1,intercalation:false});
  assert.deepEqual(calendar.lunarFor(new Date('2026-11-04')),{year:2026,month:9,day:25,intercalation:false});
  assert.equal(calendar.lunarFor(new Date('2026-10-10')).month,8);
  assert.equal(calendar.lunarFor(new Date('2026-10-10')).day,30);
});
test('leap months and lunar New Year do not inherit the solar month/year',()=>{
  assert.deepEqual(calendar.lunarFor(new Date('2025-07-25')),{year:2025,month:6,day:1,intercalation:true});
  assert.deepEqual(calendar.lunarFor(new Date('2026-02-16')),{year:2025,month:12,day:29,intercalation:false});
  for(const value of ['1899-12-31','2051-01-01'])assert.equal(calendar.lunarFor(new Date(value)),null);
  assert.equal(calendar.lunarFor(new Date(NaN)),null);
});
test('daily ganji uses KST midnight, and month/year pillars use exact DE440 jie boundaries',()=>{
  const events=yearEvents(2026);
  assert.deepEqual(calendar.pillarsAt(new Date('2026-11-04T03:00:00Z'),events),{year:'병오년',month:'무술월',day:'임오일'});
  assert.equal(calendar.pillarsAt(new Date('2026-11-04T14:59:59Z'),events).day,'임오일');
  assert.equal(calendar.pillarsAt(new Date('2026-11-04T15:00:00Z'),events).day,'계미일');
  const ipdong=events.find(e=>e.termIndex===15).milliseconds;
  assert.equal(calendar.pillarsAt(new Date(ipdong-1),events).month,'무술월');
  assert.equal(calendar.pillarsAt(new Date(ipdong+1),events).month,'기해월');
  const ipchun=events.find(e=>e.termIndex===21).milliseconds;
  assert.deepEqual(calendar.pillarsAt(new Date(ipchun-1),events),{year:'을사년',month:'기축월',day:calendar.pillarsAt(new Date(ipchun+1),events).day});
  assert.equal(calendar.pillarsAt(new Date(ipchun+1),events).year,'병오년');
  assert.equal(calendar.pillarsAt(new Date(ipchun+1),events).month,'경인월');
  for(let year=1900;year<=2100;year++){
    const list=yearEvents(year);
    for(const e of list.filter(x=>x.termIndex%2))assert.notEqual(calendar.pillarsAt(new Date(e.milliseconds-1),list).month,calendar.pillarsAt(new Date(e.milliseconds+1),list).month);
  }
});
// USNO primary-phase instants, UT: https://aa.usno.navy.mil/calculated/moon/phases?year=2026
test('moon illumination agrees with independent new/quarter/full phase references',()=>{
  for(const [instant,phase]of [['2026-11-09T07:02:00Z',0],['2026-11-17T11:48:00Z',.25],['2026-11-24T14:53:00Z',.5],['2026-12-01T06:08:00Z',.75]]){
    const moon=calendar.moonAt(new Date(instant));
    assert(Math.min(Math.abs(moon.phase-phase),1-Math.abs(moon.phase-phase))<.001,instant);
    if(phase===0)assert(moon.fraction<.005);
    else if(phase===.5)assert(moon.fraction>.995);
    else assert(Math.abs(moon.fraction-.5)<.03);
  }
  const moon=calendar.moonFor(new Date('2026-11-04'));assert.equal(moon.emoji,'🌘');assert.equal(moon.label,'그믐달');
  assert.equal(calendar.moonAt(new Date(NaN)),null);
});
