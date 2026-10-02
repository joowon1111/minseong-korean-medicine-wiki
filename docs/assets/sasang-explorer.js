(()=>{"use strict";
const D=[
["소양인","소양상풍·표병","얕은 표병","두통·한열왕래·신체통·흉협 불편 등 표병의 비교적 얕은 방향을 살핍니다.",["배설 변화와 기력 저하가 진행하는지","망음의 복통·설사·소모가 중심으로 이동하는지","감염·호흡기·근골격 원인을 함께 구분했는지"],[["형방패독산","/sasang-formula-library/hyeongbangpaedok-san/","표병의 비교적 얕은 단계"]]],
["소양인","신열두통망음·배설 변화","신열두통망음","신열·두통·번조·구갈과 배설 변화를 함께 보며 망음 방향을 살핍니다.",["형방도적산 단계보다 열·번조가 뚜렷한지","복통·설사와 수분 소모가 중심인지","탈수·감염 등 다른 원인을 함께 확인했는지"],[["형방사백산","/sasang-formula-cards/hyeongbangsabaek-san/","신열·두통·번조·구갈의 망음 방향"],["형방도백산","/sasang-formula-library/soyangin-extended-formulas/#soyang-hyeongbangdobaek","표병·열과 배설 변화"]]],
["소양인","흉격열·리열","흉격열·리열","상부 열감·번조·구갈과 대소변 변화를 보며 흉격열과 리열의 정도를 살핍니다.",["표병의 한열·두통이 중심인지","대변 정체와 구갈의 정도","음허오열처럼 소모·허열 방향이 깊어졌는지"],[["양격산화탕","/sasang-formula-cards/yanggyeoksanhwa-tang/","흉격열·리열 방향"]]],
["소양인","음허오열·하소/허로","하소·하지무력","진액·음분의 소모와 허열, 하지 기능·소변·수면 등 전신 회복 저하를 함께 살핍니다.",["단순한 실열·구갈과 구분","체중·섭취·수분·내분비 문제 확인","하지 기능과 야간 증상·수면 변화"],[["독활지황탕","/sasang-formula-cards/dokhwaljihwang-tang/","음허오열·하소"],["숙지황고삼탕","/sasang-formula-library/soyangin-extended-formulas/#soyang-sukjihwanggosam","음허오열·습열 단서"],["화석지황탕","/sasang-formula-library/soyangin-extended-formulas/#soyang-hwaseokjihwang","음허오열·허로"]]],

["소양인","표병·결흉/흉격 불편","결흉·흉격 불편","한열·두통과 흉격 답답함, 담·기역, 대소변 변화를 함께 살핍니다.",["리열성 흉격열과 구분","신열두통망음보다 흉격·담·기역이 중심인지","배설 변화와 흉격 증상의 시간관계"],[["형방도적산","/sasang-formula-cards/hyeongbangdojeok-san/","표병·결흉 방향"]]],
["소양인","망음·설사/복통","설사·복통과 소모","복통·설사와 진액·기력 저하가 중심이 되는 망음 방향을 살핍니다.",["섭취·수분상태와 설사 뒤 회복","복통에서 열·습 단서가 큰지","급성 장염·감염·탈수 감별"],[["형방지황탕","/sasang-formula-cards/hyeongbangjihwang-tang/","망음·설사와 소모"],["활석고삼탕","/sasang-formula-library/soyangin-extended-formulas/#soyang-hwalseokgosam","망음·복통과 열·습 단서"]]],
["소양인","장관 열·이질","열성 설사·복통","설사·복통·급박감과 열증이 전면에 놓이는 장관 열 방향을 살핍니다.",["탈수·출혈 여부","감염성 장염·염증성 장질환 감별","망음의 한·소모 방향과 구분"],[["황련청장탕","/sasang-formula-library/hwangryeoncheongjang-tang/","장관 열·설사 방향"]]],
["소양인","강한 리열·이열변폐","백호계·진액손상","심한 구갈·변폐·번조와 전신 열증, 진액손상의 깊이를 살핍니다.",["고열·의식 변화·탈수는 긴급 평가 우선","양격산화탕보다 변폐·강한 전신 열증이 중심인지","만성 음허오열·소모와 구분"],[["지황백호탕","/sasang-formula-library/soyangin-extended-formulas/#soyang-jihwangbaekho","이열변폐·백호계"],["현삼백호탕","/sasang-formula-library/hyeonsambaekho-tang/","강한 열·진액손상"]]],

["태음인","표한·비위담습/조위","비위 담습","오한·발한불리, 몸의 무거움, 식후 더부룩함·부종·피로가 겹치는 표한 방향을 살핍니다.",["땀 뒤 편안함과 기력 변화","호흡기 불편·부종·대사 문제","간수열리열의 열감·구갈·건조와 구분"],[["태음조위탕","/sasang-formula-cards/taeeumjowi-tang/","표한·비위 담습"],["승지조위탕","/sasang-formula-library/taeeumin-extended-formulas/#taeeum-seungjijowi","표한·조위"]]],
["태음인","표한·승청 저하","중소·하지무력·회복 지연","식후 비만감, 하지 무력, 오래된 회복저하와 수면·심신 증상을 함께 살핍니다.",["태음조위탕 단계와의 공통점·차이","하지무력의 신경·근골격 원인","수면·심계·피로가 병증축과 일관되는지"],[["조위승청탕","/sasang-formula-cards/jowiseungcheong-tang/","승청 기능 저하와 회복축"]]],
["태음인","간열·폐조","간열·폐조","열감·구갈·발한과 대변·피부의 건조 등 리열 방향을 표한과 구분해 살핍니다.",["오한·무한·몸의 무거움이 중심인 표한과 구분","대변 정체·갈증·피부 건조의 정도","폐조·진액 소모가 심화되는지"],[["열다한소탕","/sasang-formula-cards/yeoldahanso-tang/","간열·리열 방향"]]],
["태음인","리열·양독/조열·심신","조열·심신 증후","열·건조와 함께 심번·현훈·심계·수면, 진액 보완의 비중이 커지는 방향을 살핍니다.",["단순 리열보다 폐조·진액 소모가 두드러지는지","심계·현훈의 다른 원인","수면과 대변·갈증이 함께 변하는지"],[["청심연자탕","/sasang-formula-cards/cheongsimyeonja-tang/","리열·조열·심신 증후"],["갈근해기탕","/sasang-formula-library/galgeunhaegi-tang/","리열·양독"]]],

["태음인","표한·한궐·통증","흉복통·신체통","오한·무한과 흉복통·신체통·호흡 변화가 전면인 표한 방향을 살핍니다.",["통증과 표한의 시간관계","심폐·근골격 원인 감별","맥박·수면·발한 뒤 반응"],[["마황정통탕","/sasang-formula-library/mahwangjeongtong-tang/","표한·한궐·통증"]]],
["태음인","표한·승청과 호흡","기침·담·호흡 비중","기침·담·호흡과 식후 불편·회복 지연이 함께 나타나는 승청·폐원 방향을 살핍니다.",["조위승청탕보다 호흡 비중이 큰지","급성 호흡기 위험신호","식후 불편과 활동 회복"],[["행인승청탕","/sasang-formula-library/haenginseungcheong-tang/","승청·폐원"]]],
["태음인","병후체허·폐원/회복","폐원·회복 지연","급성기 뒤 기침·호흡·식욕·활동 회복이 늦거나 건조·수면·심계가 함께 얽힌 방향을 살핍니다.",["급성 호흡기 질환과 회복기 구분","조위승청탕·행인승청탕과 비교","체중·섭취·수면·활동 회복"],[["조리폐원탕","/sasang-formula-library/joripyewon-tang/","병후체허·폐원 회복"],["경험승청탕","/sasang-formula-library/taeeumin-extended-formulas/#taeeum-gyeongheomseungcheong","승청·폐조·회복 지연"]]],
["태음인","강한 리열·승기·정체","변폐·복만·식체","번갈·변비·복만과 강한 리열, 식체·대변 정체의 비중을 살핍니다.",["급성 복증·장폐색 신호 확인","대황 관련 설사·탈수 위험","열·구갈 중심인지 식체·복만 중심인지"],[["청폐사간탕","/sasang-formula-cards/cheongpyesagan-tang/","강한 리열·정체"],["갈근승기탕","/sasang-formula-library/taeeumin-extended-formulas/#taeeum-galgeunseunggi","리열·승기"],["나복자승기탕","/sasang-formula-library/taeeumin-extended-formulas/#taeeum-nabokjaseunggi","리열·식체·정체"]]],

["소음인","태양증·울광 초기","울광 초기","오한·발열, 두통·신체통과 땀의 변화를 보며 울광의 표병 방향을 살핍니다.",["감염·체온·호흡기 증상 확인","땀 뒤 기력이 급격히 떨어지는 망양과 구분","통증 부위와 근골격 원인 확인"],[["천궁계지탕","/sasang-integrated/soeumin/#soeum-cheongung-gyeji","태양증·울광 방향"],["궁귀향소산","/sasang-formula-library/soeumin-extended-formulas/#soeum-gunggwihyangso","울광 처방군 비교"]]],
["소음인","망양초증·승양","승양·회복 지연","땀 뒤 기력저하와 표증의 지속, 회복 지연을 보며 망양 방향을 살핍니다.",["탈수·저혈압·빈혈·약물 영향","울광의 표증과 탈진의 비중 비교","어지럼·실신·심혈관 위험 신호 확인"],[["승양익기탕","/sasang-integrated/soeumin/#soeum-seungyangikgi","망양초증 방향"],["승양팔물탕","/sasang-formula-cards/seungyangpalmul-tang/","망양 처방군 비교"]]],
["소음인","태음병·한습/리한","태음병·한습","복통·설사, 식욕저하, 오심·구토와 심하부 답답함이 겹치는 리한 방향을 살핍니다.",["장염·식중독·약물 등 원인 감별","구토·심하비만의 비중","사지냉·전신 쇠약이 더 깊은 소음병과 구분"],[["곽향정기산","/sasang-formula-cards/gwakhyangjeonggi-san/","태음병의 한습·구토 방향"],["백하오이중탕","/sasang-formula-cards/baekhao-ijung-tang/","태음병의 리한 방향"]]],
["소음인","소음병·깊은 리한/장궐","소음병·리한 심화","사지냉·전신통·쇠약과 복통·설사가 깊어지는 리한 방향을 살핍니다.",["탈수·전해질·혈압·체온 확인","급성 복증과 감염 감별","부자 포함 처방의 포제·용량·병용약 안전성"],[["관계부자이중탕","/sasang-formula-cards/gwangye-buja-ijung-tang/","리한 심화 방향"]]],

["소음인","표병·기체/두통·소화","기체·두통·소화 변화","오한·두통·신체통에 흉복 답답함·식욕 변화가 함께 나타나는 울광 표병 방향을 살핍니다.",["천궁계지탕과 통증·기체 비중 비교","발한 뒤 회복과 망양 전환 여부","급성 감염·호흡기 원인 확인"],[["향소산","/sasang-formula-library/soeumin-extended-formulas/#soeum-hyangso","표병·기체·소화 변화"],["궁귀향소산","/sasang-formula-library/soeumin-extended-formulas/#soeum-gunggwihyangso","표병·두통·기체"]]],
["소음인","망양 심화·부자 배합","발한·탈진·냉감 심화","지속 발한과 탈진, 냉감·쇠약·활동 저하가 깊어지는 망양 방향을 살핍니다.",["의식·혈압·맥박·수분상태 확인","쇼크·감염·출혈 등 응급 원인 우선 배제","부자 포함 처방의 포제·용량·병용약 안전성"],[["승양익기부자탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-seungyangikgi-buja","망양 심화·부자 배합"],["인삼계지부자탕","/sasang-formula-cards/insamgyejibujatang/","망양 심화"],["인삼관계부자탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-insam-gwangye-buja","망양 심화·관계 배합"],["계지부자탕","/sasang-formula-library/gyejibujatang/","망양·발한 뒤 허탈"]]],
["소음인","태음병·구토/급성 토사","구토·정체·급성 토사","오심·구토·심하·흉부 답답함 또는 급성 구토·설사·복통·냉감이 전면인 태음병 방향을 살핍니다.",["물을 유지하기 어려운 구토·탈수 확인","급성 폐색·감염성 장염 감별","수분·전해질과 전신 쇠약 추적"],[["계지반하생강탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-gyeji-banha","태음병·구토·정체"],["궁귀총소이중탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-gunggwichongso","태음병·급성 토사"]]],
["소음인","리한·기체/흉복통·황달/음독","기체·흉복통·황색 변화","흉복부 답답함·긴장·소화저하, 흉복통·배뇨 변화, 황색 변화·부종 같은 리한의 분기들을 비교합니다.",["새 황달·진한 소변은 간담도 평가 우선","심혈관·신장·비뇨기 원인 감별","급성 표병의 향소산류와 만성 허약 구분"],[["향부자팔물탕","/sasang-formula-cards/hyangbujapalmul-tang/","리한·기체·사려상비"],["관중탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-gwanjung","리한·흉복통·배뇨 변화"],["십이미관중탕","/sasang-formula-library/soeumin-extended-formulas/#soeum-sibimi-gwanjung","태음병·황달·음독 방향"]]],

["태양인","외감요척병","해역","요척·하지의 지탱 기능 저하와 오래 서기·걷기 어려운 방향을 살핍니다.",["근력·감각·반사와 좌우 차이","뇌·척수·말초신경·근골격 질환 감별","보행·계단·낙상과 일상기능 변화"],[["오가피장척탕","/sasang-formula-cards/ogapi-jangcheok-tang/","외감요척병·해역 방향"]]],
["태양인","내촉소장병","열격·반위","연하불편·구역·구토와 섭취 감소, 체중·수분 변화를 함께 살핍니다.",["고형식·물의 차이와 걸리는 위치","흡인 신호·진행성 연하곤란 확인","위·식도 질환과 영양·탈수 평가"],[["미후등식장탕","/sasang-formula-cards/mihudeung-sikjang-tang/","내촉소장병·열격 방향"]]]
];

const AXIS_ORDER={
"소양인":["소양상풍·표병","표병·결흉/흉격 불편","신열두통망음·배설 변화","망음·설사/복통","흉격열·리열","장관 열·이질","강한 리열·이열변폐","음허오열·하소/허로"],
"태음인":["표한·한궐·통증","표한·비위담습/조위","표한·승청 저하","표한·승청과 호흡","병후체허·폐원/회복","간열·폐조","리열·양독/조열·심신","강한 리열·승기·정체"],
"소음인":["태양증·울광 초기","표병·기체/두통·소화","망양초증·승양","망양 심화·부자 배합","태음병·한습/리한","태음병·구토/급성 토사","소음병·깊은 리한/장궐","리한·기체/흉복통·황달/음독"],
"태양인":["외감요척병","내촉소장병"]
};

const LINKS={
"소양인":[["통합 허브","/sasang-integrated/soyangin/"],["병증 진행","/sasang-progression/soyangin/"],["처방 배합망","/sasang-formula-combination-network/soyangin-network/"]],
"태음인":[["통합 허브","/sasang-integrated/taeeumin/"],["표리 감별","/sasang-pattern-differential/taeeumin-exterior-vs-interior/"],["처방 배합망","/sasang-formula-combination-network/taeeumin-network/"]],
"소음인":[["통합 허브","/sasang-integrated/soeumin/"],["병증 진행","/sasang-progression/soeumin/"],["처방 배합망","/sasang-formula-combination-network/soeumin-network/"]],
"태양인":[["통합 허브","/sasang-integrated/taeyangin/"],["해역·열격 감별","/sasang-pattern-differential/taeyangin-haeyeok-vs-yeolgeok/"],["처방 배합망","/sasang-formula-combination-network/taeyangin-network/"]]
};

const $=id=>document.getElementById(id), c=$("sx-constitution"),a=$("sx-axis"),s=$("sx-stage"),r=$("sx-results"),m=$("sx-summary"),reset=$("sx-reset");
if(!c||!a||!s||!r||!m||!reset)return;
const uniq=x=>[...new Set(x)];
const opt=(v,t)=>{const o=document.createElement("option");o.value=v;o.textContent=t;return o};
function axes(){a.innerHTML="";a.append(opt("","병증군을 선택하세요"));if(!c.value){a.disabled=true;return}(AXIS_ORDER[c.value]||uniq(D.filter(x=>x[0]===c.value).map(x=>x[1]))).forEach(x=>a.append(opt(x,x)));a.disabled=false}
function stages(){s.innerHTML="";s.append(opt("","전체 단계"));if(!a.value){s.disabled=true;return}D.filter(x=>x[0]===c.value&&x[1]===a.value).forEach(x=>s.append(opt(x[2],x[2])));s.disabled=false}
function esc(x){return String(x).replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]))}
function render(){
 const rows=D.filter(x=>(!c.value||x[0]===c.value)&&(!a.value||x[1]===a.value)&&(!s.value||x[2]===s.value));
 if(!c.value){m.textContent="체질을 선택하면 해당 체질의 주요 병증군부터 단계적으로 살펴볼 수 있습니다.";r.innerHTML="";return}
 m.textContent=a.value?c.value+" · "+a.value+(s.value?" · "+s.value:" · 전체 단계")+" — 대표 처방은 추천이 아니라 관련 문서로 이동하는 학습용 연결입니다.":c.value+"의 주요 병증군을 선택하세요.";
 if(!a.value){r.innerHTML="";return}
 r.innerHTML=rows.map(x=>{const fs=x[5].map(f=>'<a class="sasang-explorer__formula" href="'+f[1]+'"><strong>'+esc(f[0])+'</strong><small>'+esc(f[2])+'</small></a>').join("");
 const ls=(LINKS[x[0]]||[]).map(z=>'<a href="'+z[1]+'">'+esc(z[0])+' →</a>').join("");
 return '<article class="sasang-explorer__card"><p class="sasang-explorer__eyebrow">'+esc(x[0])+' · '+esc(x[1])+'</p><h3>'+esc(x[2])+'</h3><p>'+esc(x[3])+'</p><h4>감별 포인트</h4><ul>'+x[4].map(d=>'<li>'+esc(d)+'</li>').join("")+'</ul><h4>연결해서 읽을 대표 처방</h4><div class="sasang-explorer__formula-grid">'+fs+'</div><h4>관련 문서</h4><div class="sasang-explorer__links">'+ls+'</div></article>'}).join("")||'<div class="sasang-explorer__empty">조건에 맞는 항목이 없습니다.</div>'
}
c.addEventListener("change",()=>{axes();s.innerHTML='<option value="">전체 단계</option>';s.disabled=true;render()});
a.addEventListener("change",()=>{stages();render()});
s.addEventListener("change",render);
reset.addEventListener("click",()=>{c.value="";a.innerHTML='<option value="">먼저 체질을 선택하세요</option>';a.disabled=true;s.innerHTML='<option value="">전체 단계</option>';s.disabled=true;render();c.focus()});
render();
})();