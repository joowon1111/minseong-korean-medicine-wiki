from pathlib import Path

docs=Path("docs")

# Combined symptom searches are common in real users:
# "두통 어지럼", "목통증 두통", "소화불량 피로", etc.
# We add these exact combinations to existing pages rather than create new pages.
groups={
"conditions/headache.md":[
"두통 어지럼","두통 목통증","두통 뒷목통증","두통 메스꺼움","두통 비염",
"두통 불면","두통 스트레스","두통 자율신경","편두통 어지럼","머리아픔 어지럼"
],
"conditions/dizziness.md":[
"어지럼 두통","어지럼 메스꺼움","어지럼 목통증","어지럼 피로","어지럼 소화불량",
"어지럼 두근거림","어지럼 자율신경","현훈 두통","현훈 메스꺼움"
],
"conditions/neck-pain.md":[
"목통증 두통","목통증 어깨통증","목통증 팔저림","목통증 어지럼","뒷목통증 두통",
"목 어깨 뻐근","경항통 두통","목디스크 두통","목디스크 팔저림"
],
"conditions/shoulder-pain.md":[
"어깨통증 목통증","어깨통증 팔저림","어깨통증 야간통","어깨통증 두통",
"오십견 목통증","어깨 뭉침 두통","어깨통증 팔올리기"
],
"conditions/low-back-pain.md":[
"허리통증 엉치통증","허리통증 다리저림","허리통증 골반통증","허리통증 무릎통증",
"요통 하지방사통","허리 아픔 다리 당김","허리통증 피로","허리통증 수면"
],
"conditions/knee-pain.md":[
"무릎통증 허리통증","무릎통증 부종","무릎통증 계단","무릎통증 걸을때",
"무릎통증 냉증","무릎통증 산후","무릎통증 피로"
],
"conditions/dyspepsia.md":[
"소화불량 피로","소화불량 어지럼","소화불량 두근거림","소화불량 스트레스",
"소화불량 불면","더부룩함 메스꺼움","명치답답 가슴답답","체기 두통","체기 어지럼"
],
"conditions/chronic-fatigue.md":[
"만성피로 소화불량","만성피로 불면","만성피로 어지럼","만성피로 두근거림",
"피로 소화안됨","피로 수면장애","피로 갱년기","피로 산후","기력저하 소화불량"
],
"conditions/rhinitis.md":[
"비염 두통","비염 기침","비염 불면","비염 피로","비염 코막힘 두통",
"비염 후비루 기침","콧물 기침","코막힘 수면"
],
"conditions/cough.md":[
"기침 비염","기침 감기","기침 가래","기침 목이물감","기침 소화불량",
"기침 역류","기침 불면","기침 피로","감기후 기침","후비루 기침"
],
"conditions/common-cold.md":[
"감기 기침","감기 비염","감기 몸살","감기 두통","감기 목통증",
"감기 피로","감기 후 기침","감기 콧물 기침","목감기 기침"
],
"conditions/menopause.md":[
"갱년기 불면","갱년기 두근거림","갱년기 피로","갱년기 어지럼",
"갱년기 상열감","갱년기 식은땀","갱년기 자율신경","폐경 불면"
],
"conditions/postpartum-recovery.md":[
"산후 피로","산후 허리통증","산후 무릎통증","산후 손목통증",
"산후 불면","산후 냉증","산후 관절통","산후 기력저하"
],
"symptom-integrated/autonomic-stress.md":[
"두근거림 가슴답답","두근거림 어지럼","두근거림 불면","자율신경 소화불량",
"자율신경 어지럼","자율신경 두통","자율신경 불면","상열감 손발냉증",
"목이물감 스트레스","매핵기 소화불량"
],
"symptom-integrated/sleep-fatigue.md":[
"불면 피로","불면 두근거림","불면 두통","불면 소화불량","수면장애 피로",
"자다가 자주깸 피로","새벽각성 피로","잠이안옴 두근거림"
]
}

marker="## 함께 검색되는 증상 조합"

updated=[]
missing=[]
for rel,phrases in groups.items():
    p=docs/rel
    if not p.exists():
        missing.append(rel)
        continue
    t=p.read_text(encoding="utf-8")
    block=marker+"\n\n"+ " · ".join(phrases) + "\n\n"
    block += "이 조합들은 환자가 **두 가지 이상 증상을 한 번에 검색할 때** 관련 페이지에 도달하도록 돕는 검색어입니다. 증상 조합이 같아도 원인이 다를 수 있으므로 감별과 위험신호를 먼저 확인합니다.\n"
    if marker in t:
        t=t.split(marker,1)[0].rstrip()+"\n\n"+block
    else:
        t=t.rstrip()+"\n\n"+block
    p.write_text(t,encoding="utf-8")
    updated.append(rel)
    print("UPDATED:",rel)

audit=["# 증상 조합 검색 점검",""]
for rel,phrases in groups.items():
    p=docs/rel
    if not p.exists():
        for phrase in phrases:
            audit.append(f"- MISSING FILE | {phrase} | {rel}")
    else:
        text=p.read_text(encoding="utf-8")
        for phrase in phrases:
            audit.append(f"- {'OK' if phrase in text else 'MISSING'} | {phrase} | {rel}")
Path("COMBINED_SYMPTOM_SEARCH_AUDIT.md").write_text("\n".join(audit)+"\n",encoding="utf-8")

print("UPDATED COUNT:",len(updated))
print("MISSING TARGET FILES:", missing if missing else "none")
print("AUDIT: COMBINED_SYMPTOM_SEARCH_AUDIT.md")
