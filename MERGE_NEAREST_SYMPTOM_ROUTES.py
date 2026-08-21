from pathlib import Path

docs=Path("docs")

# Existing-page-only nearest symptom routing.
# No new site page/nav. Adds "가장 가까운 증상 찾기" to current condition/symptom pages.
routes={
"conditions/low-back-pain.md":{
"prompt":"허리통증과 함께 나타나는 증상에 따라 아래 페이지가 더 가까울 수 있습니다.",
"links":[
("엉치·다리로 당기거나 저려요","요통","low-back-pain.md"),
("목·어깨도 같이 뻐근해요","목통증","neck-pain.md"),
("걷거나 계단에서 무릎도 아파요","무릎통증","knee-pain.md"),
("통증 때문에 잠을 못 자고 피곤해요","수면·피로","../symptom-integrated/sleep-fatigue.md")
]},
"conditions/neck-pain.md":{
"prompt":"목통증이 어떤 증상과 함께 오는지에 따라 더 가까운 페이지를 선택할 수 있습니다.",
"links":[
("머리까지 아파요","두통","headache.md"),
("어깨·견갑골까지 아파요","어깨통증","shoulder-pain.md"),
("어지럽고 머리가 띵해요","어지럼","dizziness.md"),
("가슴이 답답하고 긴장돼요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md")
]},
"conditions/shoulder-pain.md":{
"prompt":"어깨통증의 중심이 어디인지에 따라 관련 페이지를 같이 보세요.",
"links":[
("목에서 어깨로 이어져 아파요","목통증","neck-pain.md"),
("팔을 올리거나 뒤로 돌리기 힘들어요","어깨통증","shoulder-pain.md"),
("두통·뒷목통증도 있어요","두통","headache.md"),
("전신 피로와 회복저하가 같이 있어요","만성피로","chronic-fatigue.md")
]},
"conditions/knee-pain.md":{
"prompt":"무릎통증이 다른 기능문제와 연결되는지 같이 확인합니다.",
"links":[
("허리·엉치도 같이 아파요","요통","low-back-pain.md"),
("다리가 무겁고 쉽게 피곤해요","만성피로","chronic-fatigue.md"),
("출산 후 무릎·관절이 아파요","산후회복","postpartum-recovery.md"),
("무릎보다 전신 통증이 더 커요","통증","../symptom-integrated/pain.md")
]},
"conditions/headache.md":{
"prompt":"두통과 함께 나타나는 증상에 따라 원인과 치료축이 달라질 수 있습니다.",
"links":[
("목이 뻐근하고 뒤통수가 아파요","목통증","neck-pain.md"),
("빙빙 돌거나 머리가 띵해요","어지럼","dizziness.md"),
("코막힘·재채기가 같이 있어요","비염","rhinitis.md"),
("두근거림·긴장·불면이 같이 있어요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md")
]},
"conditions/dizziness.md":{
"prompt":"어지럼이 어떤 증상과 같이 나타나는지에 따라 더 가까운 설명을 찾을 수 있습니다.",
"links":[
("두통이 같이 있어요","두통","headache.md"),
("목이 뻐근해요","목통증","neck-pain.md"),
("메스꺼움·더부룩함이 있어요","소화불량","dyspepsia.md"),
("긴장·두근거림·상열감이 있어요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md")
]},
"conditions/dyspepsia.md":{
"prompt":"소화불량과 함께 나타나는 증상을 고르면 관련 자료를 더 빨리 찾을 수 있습니다.",
"links":[
("자도 피곤하고 기운이 없어요","만성피로","chronic-fatigue.md"),
("스트레스 받으면 더 심해져요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),
("어지럽고 메스꺼워요","어지럼","dizziness.md"),
("기침·목이물감·역류 느낌이 있어요","기침","cough.md")
]},
"conditions/chronic-fatigue.md":{
"prompt":"피로의 중심 원인이 어디에 가까운지 관련 페이지와 함께 봅니다.",
"links":[
("잠을 자도 개운하지 않아요","수면·피로","../symptom-integrated/sleep-fatigue.md"),
("소화가 안 되고 기운이 없어요","소화불량","dyspepsia.md"),
("두근거림·긴장·어지럼이 있어요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),
("갱년기 열감·불면이 같이 있어요","갱년기","menopause.md")
]},
"conditions/rhinitis.md":{
"prompt":"비염처럼 보이는 증상이 감기·기침·두통과 연결되는지 확인합니다.",
"links":[
("몸살·인후통이 갑자기 같이 왔어요","감기","common-cold.md"),
("기침이 오래가요","기침","cough.md"),
("코막힘과 함께 머리가 아파요","두통","headache.md"),
("수면이 깨지고 피곤해요","만성피로","chronic-fatigue.md")
]},
"conditions/cough.md":{
"prompt":"기침이 어떤 증상과 연결되는지에 따라 더 가까운 페이지를 선택하세요.",
"links":[
("감기 후 기침이 남았어요","감기","common-cold.md"),
("콧물·코막힘·후비루가 있어요","비염","rhinitis.md"),
("속쓰림·더부룩함·목이물감이 있어요","소화불량","dyspepsia.md"),
("오래 기침해서 기운이 없어요","만성피로","chronic-fatigue.md")
]},
"conditions/common-cold.md":{
"prompt":"감기 증상 중 무엇이 가장 오래 남는지에 따라 다음 페이지를 같이 보세요.",
"links":[
("기침이 오래 남아요","기침","cough.md"),
("콧물·재채기·코막힘이 계속돼요","비염","rhinitis.md"),
("몸살·근육통이 심해요","통증","../symptom-integrated/pain.md"),
("보험되는 한약이 궁금해요","건강보험 한약제제","../herbal-integrated/insurance-herbal.md")
]},
"conditions/menopause.md":{
"prompt":"갱년기 증상은 열감뿐 아니라 수면·피로·자율신경 증상과 함께 나타날 수 있습니다.",
"links":[
("자도 피곤하고 기운이 없어요","만성피로","chronic-fatigue.md"),
("잠들기 어렵고 자주 깨요","수면·피로","../symptom-integrated/sleep-fatigue.md"),
("두근거림·상열감·긴장이 있어요","자율신경·스트레스","../symptom-integrated/autonomic-stress.md"),
("어지럽고 머리가 띵해요","어지럼","dizziness.md")
]},
"conditions/postpartum-recovery.md":{
"prompt":"산후회복에서 가장 불편한 증상에 가까운 페이지를 같이 보세요.",
"links":[
("기운이 없고 회복이 느려요","만성피로","chronic-fatigue.md"),
("허리가 아파요","요통","low-back-pain.md"),
("무릎·관절이 아파요","무릎통증","knee-pain.md"),
("잠을 못 자고 지쳐요","수면·피로","../symptom-integrated/sleep-fatigue.md")
]},
"symptom-integrated/autonomic-stress.md":{
"prompt":"자율신경·스트레스 증상 중 실제로 가장 불편한 증상으로 이동할 수 있습니다.",
"links":[
("가슴답답·두근거림이 중심이에요","자율신경·스트레스","autonomic-stress.md"),
("잠이 안 오고 자주 깨요","수면·피로","sleep-fatigue.md"),
("스트레스 받으면 소화가 안돼요","소화불량","../conditions/dyspepsia.md"),
("머리가 띵하고 어지러워요","어지럼","../conditions/dizziness.md")
]},
"symptom-integrated/sleep-fatigue.md":{
"prompt":"수면문제와 피로 중 어느 쪽이 중심인지 관련 페이지를 같이 확인합니다.",
"links":[
("자도 계속 피곤해요","만성피로","../conditions/chronic-fatigue.md"),
("두근거림·긴장이 같이 있어요","자율신경·스트레스","autonomic-stress.md"),
("갱년기 열감 때문에 잠을 못 자요","갱년기","../conditions/menopause.md"),
("소화가 안 되고 잠도 불편해요","소화불량","../conditions/dyspepsia.md")
]}
}

marker="## 내 증상과 가장 가까운 페이지 찾기"

updated=[]
for rel,d in routes.items():
    p=docs/rel
    if not p.exists():
        print("SKIP:",rel)
        continue
    t=p.read_text(encoding="utf-8")
    lines=[marker,"",d["prompt"],""]
    lines += ["| 지금 가장 불편한 증상 | 먼저 볼 페이지 |","|---|---|"]
    for cue,label,href in d["links"]:
        lines.append(f"| {cue} | [{label}]({href}) |")
    lines += ["","> 하나의 증상이 여러 페이지에 걸칠 수 있습니다. 가장 가까운 페이지에서 시작한 뒤 관련 증상·치료·방제·경혈 자료로 확장해서 보세요.",""]
    block="\n".join(lines)
    if marker in t:
        t=t.split(marker,1)[0].rstrip()+"\n\n"+block
    else:
        t=t.rstrip()+"\n\n"+block
    p.write_text(t,encoding="utf-8")
    updated.append(rel)
    print("UPDATED:",rel)

audit=["# 가장 가까운 증상 페이지 연결 점검",""]
for rel in routes:
    p=docs/rel
    ok=p.exists() and marker in p.read_text(encoding="utf-8")
    audit.append(f"- {'OK' if ok else 'MISSING'} | {rel}")
Path("NEAREST_SYMPTOM_PAGE_AUDIT.md").write_text("\n".join(audit)+"\n",encoding="utf-8")
print("UPDATED COUNT:",len(updated))
print("AUDIT: NEAREST_SYMPTOM_PAGE_AUDIT.md")
