from pathlib import Path

docs=Path("docs")

# Long-tail, question-style search intents mapped into existing pages.
groups={
"conditions/low-back-pain.md":[
"허리가 왜 자꾸 아픈가요","아침에 허리가 아픈 이유","오래 앉아 있으면 허리가 아픈 이유",
"허리를 삐끗했을 때 한의원 치료","허리통증에 한약도 먹나요","허리통증에 약침치료 하나요",
"허리에서 엉치까지 아픈 이유","허리에서 다리까지 당기는 이유"
],
"conditions/neck-pain.md":[
"목이 뻣뻣한 이유","뒷목이 자주 당기는 이유","목을 돌리면 아픈 이유",
"자고 일어났는데 목이 안 돌아가요","목통증에 침치료 하나요","목통증에 약침치료 하나요",
"목통증에 한약치료도 하나요","컴퓨터 오래 하면 목이 아파요"
],
"conditions/shoulder-pain.md":[
"팔을 올릴 때 어깨가 아픈 이유","밤에 어깨가 더 아픈 이유","어깨가 굳고 안 올라가요",
"오십견 한의원 치료","어깨통증 침치료","어깨통증 약침","어깨통증 한약",
"뒤로 손이 안 올라가는 이유"
],
"conditions/knee-pain.md":[
"계단 내려갈 때 무릎이 아픈 이유","앉았다 일어나면 무릎이 아픈 이유",
"걸을 때 무릎이 아픈 이유","무릎 안쪽 통증 한의원","무릎통증 침치료",
"무릎통증 약침","무릎통증 한약","무릎이 붓고 뻐근해요"
],
"conditions/headache.md":[
"목이 뻐근하면서 머리가 아파요","머리가 조이는 두통","한쪽 머리가 지끈거려요",
"두통이 자주 생기는 이유","두통 한의원 치료","두통 한약치료",
"두통 약침치료","두통과 어지럼이 같이 있어요"
],
"conditions/dizziness.md":[
"일어나면 어지러운 이유","빙빙 도는 어지럼","머리가 띵하고 어지러워요",
"어지럼과 메스꺼움이 같이 있어요","어지럼 한의원 치료","어지럼 한약치료",
"어지럼이 반복되는 이유","걷다가 휘청거려요"
],
"conditions/dyspepsia.md":[
"밥 먹고 나면 더부룩한 이유","조금만 먹어도 배부른 이유","명치가 답답한 이유",
"속이 안 내려가는 느낌","자주 체하는 이유","스트레스 받으면 소화가 안돼요",
"소화불량 한약치료","소화불량 침치료"
],
"conditions/chronic-fatigue.md":[
"자도 자도 피곤한 이유","아침부터 피곤한 이유","계속 기운이 없는 이유",
"피로가 안 풀리는 이유","만성피로 한의원 치료","피로에 한약 먹나요",
"기력저하 보약","소화도 안 되고 피곤해요"
],
"conditions/rhinitis.md":[
"아침마다 재채기하는 이유","맑은 콧물이 계속 나는 이유","코막힘 때문에 잠을 못 자요",
"비염 한의원 치료","비염 한약치료","비염 약침치료","감기인지 비염인지 모르겠어요",
"찬바람 맞으면 콧물이 나요"
],
"conditions/cough.md":[
"감기 후 기침이 오래가는 이유","밤에 기침이 심한 이유","마른기침이 계속 나요",
"가래기침이 오래가요","기침 한의원 치료","기침 한약치료",
"기침 보험한약","찬바람에 기침이 심해요"
],
"conditions/common-cold.md":[
"감기 한의원 치료","감기 한약치료","감기 보험한약","감기몸살 한약",
"목감기 한약","콧물감기 한약","감기와 비염 차이","감기 후 기침이 안 나아요"
],
"conditions/menopause.md":[
"얼굴에 갑자기 열이 오르는 이유","밤에 땀이 많이 나요","갱년기 불면",
"갱년기 한의원 치료","갱년기 한약치료","갱년기 보약",
"폐경 후 피로가 심해요","갱년기 두근거림"
],
"conditions/postpartum-recovery.md":[
"출산 후 기운이 없어요","출산 후 관절이 아파요","출산 후 손목통증",
"출산 후 허리통증","산후풍 한의원 치료","산후보약 언제 먹나요",
"산후회복 한약","수유 중 한약 먹어도 되나요"
],
"symptom-integrated/autonomic-stress.md":[
"가슴이 두근거리는 이유","스트레스 받으면 가슴이 답답해요","목에 뭔가 걸린 느낌이 계속돼요",
"손발이 차고 얼굴은 뜨거워요","긴장하면 어지러워요","자율신경 한의원 치료",
"자율신경 한약치료","자율신경 약침치료"
],
"symptom-integrated/sleep-fatigue.md":[
"잠들기 어려운 이유","자다가 자주 깨는 이유","새벽에 깨서 다시 못 자요",
"꿈을 많이 꾸고 피곤해요","자도 개운하지 않아요","불면 한의원 치료",
"불면 한약치료","불면 침치료"
],
"herbal-integrated/insurance-herbal.md":[
"보험되는 한약 종류","건강보험 한약 종류","감기에 보험한약 있나요",
"기침에 보험한약 있나요","비염에 보험한약 있나요","소화불량 보험한약",
"통증 보험한약","보험한약 56처방"
],
"acupuncture-integrated/modalities.md":[
"약침치료는 어떤 경우에 하나요","약침은 침과 뭐가 다른가요","허리통증 약침치료",
"목통증 약침치료","어깨통증 약침치료","무릎통증 약침치료",
"두통 약침치료","자율신경 약침치료","비염 약침치료","소화기 약침치료"
]
}

marker="## 이런 질문으로도 찾아볼 수 있습니다"
updated=[]; missing=[]; audit=["# 환자 검색 의도 점검",""]

for rel,phrases in groups.items():
    p=docs/rel
    if not p.exists():
        missing.append(rel)
        for q in phrases:
            audit.append(f"- MISSING FILE | {q} | {rel}")
        continue
    t=p.read_text(encoding="utf-8")
    block=marker+"\n\n"+"\n".join(f"- {q}" for q in phrases)+"""

이 질문들은 검색 진입을 돕기 위한 표현입니다. 실제 진료에서는 증상의 기간·악화요인·동반증상·위험신호를 확인한 뒤 원인과 병증을 구분합니다.
"""
    if marker in t:
        t=t.split(marker,1)[0].rstrip()+"\n\n"+block.strip()+"\n"
    else:
        t=t.rstrip()+"\n\n"+block.strip()+"\n"
    p.write_text(t,encoding="utf-8")
    updated.append(rel)
    for q in phrases:
        audit.append(f"- OK | {q} | {rel}")

Path("PATIENT_SEARCH_INTENT_AUDIT.md").write_text("\n".join(audit)+"\n",encoding="utf-8")

print("UPDATED:",len(updated))
if missing:
    print("MISSING TARGET FILES:")
    for x in missing: print(" -",x)
else:
    print("ALL TARGET FILES FOUND")
print("AUDIT: PATIENT_SEARCH_INTENT_AUDIT.md")
