const test = require('node:test');
const assert = require('node:assert/strict');
const study = require('../docs/assets/learning/learning.js');
const tools = require('../docs/assets/archive-tools/tools.js');

test('spaced repetition advances only by recorded answers and wrong answers become due', () => {
  const p = study.emptyProgress(), q = {id:'formula-test-q', answer:0, category:'보기'};
  const now = new Date(2026, 9, 9, 9).getTime();
  study.recordAnswer(p, q, 0, now, 'formulas');
  assert.equal(study.dueQuestions([q], p, now).length, 0);
  assert.equal(study.dueQuestions([q], p, now + 86400000).length, 1);
  assert.equal(p.schedule[q.id].streak, 1);
  study.recordAnswer(p, q, 1, now + 86400000, 'formulas');
  assert.equal(p.schedule[q.id].streak, 0);
  assert.equal(study.dueQuestions([q], p, now + 86400000).length, 1);
  assert.equal(study.weakQuestions([q], p).length, 1);
});
test('backup roundtrip retains legacy records, schedule and in-progress quiz', () => {
  const p = study.emptyProgress(); p.saved = ['herb-test'];
  study.recordAnswer(p, {id:'herb-test-q',answer:1,category:'본초'}, 1, 1000, 'herbs');
  p.resume = {subject:'herbs',ids:['herb-test-q'],index:0,correct:1,answered:true,selected:1,mode:'quiz'};
  assert.deepEqual(study.restore(study.backup(p)), p);
  const legacy = study.readProgress({getItem:()=>JSON.stringify({known:['old'],wrong:['old-q'],attempts:3,correct:1})});
  assert.equal(legacy.attempts,3); assert.deepEqual(legacy.known,['old']); assert.deepEqual(legacy.schedule,{});
  assert.throws(()=>study.restore('{"format":"something"}'));
  assert.throws(()=>study.restore(study.backup({...p,attempts:-1})));
  assert.equal(study.writeProgress(null,p),false);
});
test('search ranks named formula, finds aliases and filters evidence without inventing an answer', () => {
  const rows = [
    {title:'사군자탕',heading:'구성',kind:'formula',url:'/formulas/a/',text:'인삼 백출 복령 감초'},
    {title:'육군자탕',heading:'비교',kind:'formula',url:'/formulas/b/',text:'사군자탕에 반하 진피를 배합'},
    {title:'수면 연구',heading:'근거',kind:'evidence',url:'/research/sleep/',text:'불면 환자 연구의 결과와 한계'},
  ];
  assert.equal(tools.search(rows,'사군자탕')[0].title,'사군자탕');
  assert.equal(tools.search(rows,'잠이 안 와요','evidence')[0].title,'수면 연구');
  assert.deepEqual(tools.search(rows,'없는문자열'),[]);
  const prompt=tools.prompt('구성을 설명해줘',rows);
  assert.ok(prompt.includes('https://wiki.minseong.co.kr/formulas/a/'));
  assert.ok(prompt.includes('확인되지 않는 출전·구성·용량은 추정하지'));
  assert.equal(tools.safeURL('javascript:alert(1)'),'#');
  assert.equal(tools.safeURL('//external.com'),'#');
});
