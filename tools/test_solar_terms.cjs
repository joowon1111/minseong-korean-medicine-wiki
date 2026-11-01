'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const api=require('../docs/assets/solar-terms/calculator.js');
const directory=path.join(__dirname,'../docs/assets/solar-terms/de440');
const metadata=JSON.parse(fs.readFileSync(path.join(directory,'metadata.json')));
const data=year=>JSON.parse(fs.readFileSync(path.join(directory,Math.floor(year/10)*10+'.json'))).years[String(year)];
test('all supported years contain 24 different, chronological events within the KST year',()=>{
 for(let year=1900;year<=2100;year++){
  const events=api.calculateYear(year,data(year),metadata);
  assert.equal(events.length,24);assert.equal(new Set(events.map(e=>e.termIndex)).size,24);
  events.forEach((event,i)=>{
   assert.equal(api.displayTime(event.milliseconds,true).date.slice(0,4),String(year));
   if(i)assert(event.milliseconds>events[i-1].milliseconds);
  });
 }
});
test('interpolated roots agree with 192 independently searched DE440 reference events within 2 ms',()=>{
 for(const [year,references] of Object.entries(metadata.referenceEventsUtc)){
  const events=api.calculateYear(Number(year),data(Number(year)),metadata);
  references.forEach(([index,utc],i)=>{
   assert.equal(events[i].termIndex,index);
   assert(Math.abs(events[i].milliseconds-Date.parse(utc))<2,year+' '+api.TERMS[index][0]);
  });
 }
});
// Independent public minute data, KASI 1920–2100 download, as of 2026-09-01:
// https://astro.kasi.re.kr/kor/almanac/solarTerms/download
const official={"2026": [[19, "2026-01-05", "17:23"], [20, "2026-01-20", "10:45"], [21, "2026-02-04", "05:02"], [22, "2026-02-19", "00:52"], [23, "2026-03-05", "22:59"], [0, "2026-03-20", "23:46"], [1, "2026-04-05", "03:40"], [2, "2026-04-20", "10:39"], [3, "2026-05-05", "20:49"], [4, "2026-05-21", "09:37"], [5, "2026-06-06", "00:48"], [6, "2026-06-21", "17:25"], [7, "2026-07-07", "10:57"], [8, "2026-07-23", "04:13"], [9, "2026-08-07", "20:43"], [10, "2026-08-23", "11:19"], [11, "2026-09-07", "23:41"], [12, "2026-09-23", "09:05"], [13, "2026-10-08", "15:29"], [14, "2026-10-23", "18:38"], [15, "2026-11-07", "18:52"], [16, "2026-11-22", "16:23"], [17, "2026-12-07", "11:53"], [18, "2026-12-22", "05:50"]], "2027": [[19, "2027-01-05", "23:10"], [20, "2027-01-20", "16:30"], [21, "2027-02-04", "10:46"], [22, "2027-02-19", "06:33"], [23, "2027-03-06", "04:40"], [0, "2027-03-21", "05:25"], [1, "2027-04-05", "09:17"], [2, "2027-04-20", "16:18"], [3, "2027-05-06", "02:25"], [4, "2027-05-21", "15:18"], [5, "2027-06-06", "06:26"], [6, "2027-06-21", "23:11"], [7, "2027-07-07", "16:37"], [8, "2027-07-23", "10:05"], [9, "2027-08-08", "02:27"], [10, "2027-08-23", "17:14"], [11, "2027-09-08", "05:28"], [12, "2027-09-23", "15:02"], [13, "2027-10-08", "21:17"], [14, "2027-10-24", "00:33"], [15, "2027-11-08", "00:39"], [16, "2027-11-22", "22:16"], [17, "2027-12-07", "17:38"], [18, "2027-12-22", "11:42"]]};
test('2026 and 2027 minute displays match all 48 KASI public values',()=>{
 for(const [year,values] of Object.entries(official)){
  const results=api.calculateYear(Number(year),data(Number(year)),metadata);
  assert.deepEqual(results.map(e=>{const t=api.displayTime(e.milliseconds);return [e.termIndex,t.date,t.time];}),values);
 }
});
test('time rounding carries into the next KST day',()=>{
 assert.deepEqual(api.displayTime(Date.parse('2027-11-07T15:38:34Z')),{date:'2027-11-08',time:'00:39'});
 assert.deepEqual(api.displayTime(Date.parse('2026-12-31T14:59:45Z')),{date:'2027-01-01',time:'00:00'});
 assert.deepEqual(api.displayTime(Date.parse('2026-12-31T14:59:59.750Z'),true),{date:'2027-01-01',time:'00:00:00'});
});
test('year validation and next-year default use KST rather than host timezone',()=>{
 for(const input of ['',null,'2027.5','2e3','02027',1899,2101,'NaN'])assert.equal(api.yearValue(input),null,String(input));
 assert.equal(api.yearValue(' 2027 '),2027);
 assert.equal(api.defaultYear(new Date('2026-12-31T14:59:59Z')),2027);
 assert.equal(api.defaultYear(new Date('2026-12-31T15:00:00Z')),2028);
 assert.equal(api.defaultYear(new Date('2101-01-01T00:00:00Z')),2100);
});
test('damaged, incomplete or mismatched model data fails explicitly',()=>{
 const segments=data(2027),copy=()=>structuredClone(segments);
 assert.throws(()=>api.calculateYear(2027,segments.slice(0,-1),metadata));
 const broken=copy();broken[1][0]+=1;assert.throws(()=>api.calculateYear(2027,broken,metadata));
 const invalid=copy();invalid[0][2]=NaN;assert.throws(()=>api.calculateYear(2027,invalid,metadata));
 assert.throws(()=>api.calculateYear(2027,segments,{...metadata,model:'DE441'}));
 assert.throws(()=>api.calculateYear(2101,segments,metadata));
});
