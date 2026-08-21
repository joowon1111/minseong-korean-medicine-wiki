from pathlib import Path

docs=Path("docs")

pages={
"conditions/low-back-pain.md":{
"faq":[
("허리가 아프면 무조건 디스크인가요?","아닙니다. 근육·근막, 관절, 인대, 디스크, 신경 자극 등 여러 원인이 있을 수 있습니다."),
("침만 맞으면 되나요?","급성 국소통은 침·전침·약침 중심으로 볼 수 있지만, 냉증·피로·수면저하·허증이 동반되면 한약을 함께 고려할 수 있습니다."),
("엉치나 다리까지 당기면 어떻게 하나요?","하지 방사통·저림·근력저하가 있는지 확인하고 신경학적 평가를 함께 봅니다.")
],
"related":[("엉치통증","low-back-pain.md"),("무릎통증","knee-pain.md"),("만성피로","chronic-fatigue.md"),("어지럼","dizziness.md")]
},
"conditions/neck-pain.md":{
"faq":[
("목이 뻐근하면 목디스크인가요?","근육긴장·관절·디스크·신경근 자극 등 원인이 다양합니다."),
("두통도 목 때문에 생길 수 있나요?","경항부 긴장과 경추 문제가 두통과 연동되는 경우가 있어 두통 양상과 목 움직임을 함께 봅니다."),
("팔저림이 같이 있으면요?","감각분포·근력·신경학적 이상을 확인한 뒤 치료범위를 정합니다.")
],
"related":[("두통","headache.md"),("어깨통증","shoulder-pain.md"),("어지럼","dizziness.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md")]
},
"conditions/shoulder-pain.md":{
"faq":[
("오십견인가요?","팔이 안 올라간다고 모두 오십견은 아닙니다. 능동·수동 ROM, 회전근개, 경추 영향을 구분합니다."),
("밤에 더 아픈 이유는 뭔가요?","관절·건·근육 문제에서 야간통이 나타날 수 있어 통증 패턴을 함께 봅니다."),
("약침도 하나요?","국소 연부조직·MPS·아시혈 등 실제 치료표적과 상태에 따라 약침을 검토할 수 있습니다.")
],
"related":[("목통증","neck-pain.md"),("두통","headache.md"),("만성피로","chronic-fatigue.md")]
},
"conditions/knee-pain.md":{
"faq":[
("무릎이 아프면 퇴행성관절염인가요?","연령·영상소견뿐 아니라 근육·인대·반월상연골·부종·보행기능을 함께 봐야 합니다."),
("계단에서만 아파도 치료하나요?","계단·앉았다 일어나기 같은 기능성 통증도 중요한 평가대상입니다."),
("한약은 언제 같이 보나요?","만성 통증에 냉증·허약·부종·회복저하가 동반되면 병증에 따라 한약을 함께 고려합니다.")
],
"related":[("요통","low-back-pain.md"),("만성피로","chronic-fatigue.md"),("산후회복","postpartum-recovery.md")]
},
"conditions/dyspepsia.md":{
"faq":[
("체한 것과 소화불량은 같은가요?","일시적인 식적과 반복되는 기능성소화불량은 경과와 원인이 다를 수 있습니다."),
("스트레스 받으면 더 심해질 수 있나요?","기체·간위불화나 자율신경 변화와 함께 증상이 심해지는 경우가 있습니다."),
("한약만 먹나요?","병증에 따라 한약을 중심으로 침·전침·약침·식사관리 등을 조합할 수 있습니다.")
],
"related":[("만성피로","chronic-fatigue.md"),("어지럼","dizziness.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),("기침","cough.md")]
},
"conditions/chronic-fatigue.md":{
"faq":[
("자도 피곤하면 보약을 먹어야 하나요?","수면·빈혈·내분비·대사·감염 등 원인을 먼저 확인하고 병증에 맞는 한약을 선택합니다."),
("소화가 안 되면서 피곤할 수도 있나요?","비위기허·담습 등에서 소화저하와 피로가 함께 나타날 수 있습니다."),
("불면이 원인일 수도 있나요?","수면의 질 저하는 피로의 중요한 원인 중 하나입니다.")
],
"related":[("소화불량","dyspepsia.md"),("갱년기","menopause.md"),("산후회복","postpartum-recovery.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md")]
},
"conditions/headache.md":{
"faq":[
("두통이 자주 생기면 한의원에서 치료하나요?","두통 유형과 위험신호를 확인한 뒤 한약·침·전침·약침을 병증과 기능에 맞게 연결합니다."),
("목이 뻐근하면서 두통이 생기는 건 왜 그런가요?","경항부 근긴장·MPS·경추성 요소가 두통과 연동될 수 있습니다."),
("어지럼이 같이 있으면요?","편두통 연관 어지럼, 담습, 간양상항 등 여러 가능성을 함께 봅니다.")
],
"related":[("목통증","neck-pain.md"),("어지럼","dizziness.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),("비염","rhinitis.md")]
},
"conditions/dizziness.md":{
"faq":[
("어지럼은 빈혈 때문인가요?","빈혈 외에도 전정기관·혈압·편두통·약물·수면·담습·기혈허 등 다양한 원인이 있습니다."),
("목이 뻐근해도 어지러울 수 있나요?","경항부 긴장이 동반될 수 있지만 다른 원인 감별이 먼저입니다."),
("메스꺼움이 같이 있으면요?","현훈·위기상역·담습 등의 관점과 함께 일반의학적 원인을 구분합니다.")
],
"related":[("두통","headache.md"),("소화불량","dyspepsia.md"),("목통증","neck-pain.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md")]
},
"conditions/rhinitis.md":{
"faq":[
("감기인지 비염인지 어떻게 구분하나요?","감기는 급성 경과와 인후통·몸살 등이 흔하고, 비염은 반복되는 재채기·맑은 콧물·코막힘이 특징적일 수 있습니다."),
("비염에 한약도 쓰나요?","풍한·풍열·폐기허·비기허·담습 등을 구분해 한약을 비교합니다."),
("코막힘 때문에 잠을 못 자면요?","수면영향까지 치료지표로 보고 비강증상과 함께 관리합니다.")
],
"related":[("감기","common-cold.md"),("기침","cough.md"),("두통","headache.md"),("만성피로","chronic-fatigue.md")]
},
"conditions/cough.md":{
"faq":[
("감기 후 기침은 얼마나 가나요?","감기 후 기침이 오래 남을 수 있지만 지속·악화되면 다른 원인을 확인해야 합니다."),
("마른기침과 가래기침은 처방이 다른가요?","기침 성상·가래·한열·체력에 따라 병증과 처방 후보가 달라집니다."),
("비염 때문에 기침할 수도 있나요?","후비루·비염이 기침과 연동되는 경우가 있습니다.")
],
"related":[("감기","common-cold.md"),("비염","rhinitis.md"),("소화불량","dyspepsia.md"),("만성피로","chronic-fatigue.md")]
},
"conditions/common-cold.md":{
"faq":[
("감기에도 보험한약이 있나요?","건강보험 한약제제 중 감기·기침 증상에 비교할 수 있는 처방들이 있습니다. 실제 급여제품은 최신 목록을 확인합니다."),
("감기와 비염은 어떻게 다른가요?","감기는 급성 경과·몸살·인후통이 흔하고 비염은 반복적인 재채기·맑은 콧물·코막힘이 두드러질 수 있습니다."),
("감기 후 기침이 계속되면요?","기침 페이지에서 감기 후 기침·담습·폐기허·기음허 등을 다시 구분합니다.")
],
"related":[("기침","cough.md"),("비염","rhinitis.md"),("건강보험 한약제제","../herbal-integrated/insurance-herbal.md")]
},
"conditions/menopause.md":{
"faq":[
("얼굴에 열이 오르면 모두 갱년기인가요?","갱년기 외에도 갑상선·감염·약물·자율신경 등 다른 원인이 있을 수 있습니다."),
("불면과 두근거림도 같이 올 수 있나요?","안면홍조·발한·수면장애·심계·피로가 함께 나타날 수 있습니다."),
("한약은 어떤 기준으로 고르나요?","신음허·신양허·간울·심비양허·어혈 등 병증을 구분합니다.")
],
"related":[("만성피로","chronic-fatigue.md"),("자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),("어지럼","dizziness.md")]
},
"conditions/postpartum-recovery.md":{
"faq":[
("산후보약은 누구나 같은 처방인가요?","기혈허·혈허·어혈·양허·산후신통·소화상태 등을 구분해 처방합니다."),
("출산 후 관절통도 한의치료를 하나요?","통증 위치·기능·회복상태를 보고 한약·침·약침 등을 조합할 수 있습니다."),
("수유 중에도 한약을 먹을 수 있나요?","수유 여부와 처방구성을 확인해 안전성을 함께 검토합니다.")
],
"related":[("만성피로","chronic-fatigue.md"),("요통","low-back-pain.md"),("무릎통증","knee-pain.md")]
}
}

marker="## 자주 묻는 질문과 함께 볼 증상"

for rel,d in pages.items():
    p=docs/rel
    if not p.exists():
        print("SKIP:",rel)
        continue
    t=p.read_text(encoding="utf-8")
    block=[marker,"","### 자주 묻는 질문",""]
    for q,a in d["faq"]:
        block += [f"**{q}**", "", a, ""]
    block += ["### 함께 볼 증상·질환",""]
    for label,href in d["related"]:
        block.append(f"- [{label}]({href})")
    block += ["", "관련 페이지를 함께 보면 한 가지 증상을 **통증·소화·수면·자율신경·호흡·회복** 등 여러 축에서 연결해서 이해할 수 있습니다.", ""]
    b="\n".join(block)
    if marker in t:
        t=t.split(marker,1)[0].rstrip()+"\n\n"+b
    else:
        t=t.rstrip()+"\n\n"+b
    p.write_text(t,encoding="utf-8")
    print("UPDATED:",rel)

audit=["# FAQ·관련증상 네트워크 점검",""]
for rel in pages:
    p=docs/rel
    ok=p.exists() and marker in p.read_text(encoding="utf-8")
    audit.append(f"- {'OK' if ok else 'MISSING'} | {rel}")
Path("PATIENT_FAQ_RELATED_NETWORK_AUDIT.md").write_text("\n".join(audit)+"\n",encoding="utf-8")
print("AUDIT: PATIENT_FAQ_RELATED_NETWORK_AUDIT.md")
