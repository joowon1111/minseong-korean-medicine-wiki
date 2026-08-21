from pathlib import Path
docs=Path("docs")
groups={
"conditions/low-back-pain.md":["허리가 아파요","허리가 뻐근해요","허리를 숙이면 아파요","자고 일어나면 허리가 아파요","오래 앉아 있으면 허리가 아파요","허리를 삐끗했어요","엉치가 아파요","허리에서 다리로 당겨요"],
"conditions/neck-pain.md":["목이 뻐근해요","뒷목이 당겨요","목을 돌리면 아파요","자고 일어나니 목이 안 돌아가요","목과 어깨가 같이 아파요","컴퓨터 하면 목이 아파요"],
"conditions/shoulder-pain.md":["어깨가 아파요","팔을 올리면 어깨가 아파요","밤에 어깨가 아파요","뒤로 손이 안 올라가요","옷 입을 때 어깨가 아파요","어깨가 굳었어요"],
"conditions/knee-pain.md":["무릎이 아파요","계단 내려갈 때 무릎이 아파요","앉았다 일어나면 무릎이 아파요","무릎이 붓고 뻐근해요","걸으면 무릎이 아파요"],
"conditions/headache.md":["머리가 아파요","머리가 지끈거려요","머리가 조여요","관자놀이가 아파요","뒷머리가 아파요","목이 뻐근하면서 머리가 아파요","한쪽 머리가 아파요"],
"conditions/dizziness.md":["어지러워요","머리가 띵해요","빙빙 도는 것 같아요","일어나면 어지러워요","걸을 때 휘청거려요","어지럽고 메스꺼워요"],
"conditions/dyspepsia.md":["소화가 안돼요","체했어요","밥 먹으면 더부룩해요","조금만 먹어도 배가 불러요","명치가 답답해요","속이 꽉 찬 느낌이에요","트림이 자주 나요","속이 안 내려가요"],
"conditions/chronic-fatigue.md":["자도 피곤해요","계속 피곤해요","아침부터 피곤해요","기운이 없어요","몸이 무거워요","쉽게 지쳐요","피로가 안 풀려요"],
"conditions/rhinitis.md":["콧물이 계속 나요","재채기를 계속 해요","코가 막혀요","아침마다 재채기해요","맑은 콧물이 나요","코가 간지러워요","코막힘 때문에 잠을 못 자요"],
"conditions/cough.md":["기침이 계속 나요","기침이 오래가요","밤에 기침이 심해요","마른기침이 나요","가래가 끓어요","찬바람 쐬면 기침해요","감기 후 기침이 안 나아요","기침 때문에 잠을 못 자요"],
"conditions/common-cold.md":["감기 걸렸어요","몸살이 났어요","목감기 같아요","콧물감기 같아요","감기 몸살","오한이 나고 몸이 아파요","목이 아프고 기침해요","콧물 나고 재채기해요"],
"conditions/menopause.md":["얼굴에 열이 올라요","갑자기 더워지고 땀이 나요","갱년기 열감","밤에 땀이 나요","갱년기 때문에 잠을 못 자요","폐경 후 몸이 힘들어요"],
"conditions/postpartum-recovery.md":["출산 후 기운이 없어요","출산 후 몸이 시려요","출산 후 관절이 아파요","산후에 허리가 아파요","산후에 손목이 아파요","출산 후 회복이 안돼요"],
"symptom-integrated/autonomic-stress.md":["가슴이 두근거려요","가슴이 답답해요","숨이 잘 안 쉬어지는 느낌이에요","스트레스 받으면 속이 안 좋아요","목에 뭔가 걸린 느낌이에요","목에 이물감이 있어요","얼굴에 열이 올라요","손발이 차요","긴장하면 어지러워요","자율신경이 안 좋은 것 같아요"],
"symptom-integrated/sleep-fatigue.md":["잠이 안 와요","잠들기 어려워요","자다가 자주 깨요","새벽에 깨면 다시 못 자요","꿈을 많이 꿔요","자도 개운하지 않아요","아침에 너무 피곤해요"],
"symptom-integrated/pain.md":["온몸이 아파요","여기저기 쑤셔요","근육이 뭉쳤어요","찌릿찌릿 아파요","저리고 아파요","밤에 더 아파요","날씨가 추우면 아파요","통증이 오래가요"],
"herbal-integrated/insurance-herbal.md":["보험되는 한약","보험 한약 있나요","건강보험 되는 한약","감기 보험한약","기침 보험한약","비염 보험한약","소화 보험한약","통증 보험한약"],
"acupuncture-integrated/modalities.md":["약침이 뭐예요","약침치료","통증 약침","허리 약침","목 약침","어깨 약침","무릎 약침","두통 약침","자율신경 약침","소화기 약침","비염 약침","피부 약침"]
}
marker="## 환자가 이렇게 검색할 수 있습니다"
updated=[]; missing=[]; audit=["# 환자 생활언어 검색어 점검",""]
for rel,phrases in groups.items():
    p=docs/rel
    if not p.exists():
        missing.append(rel)
        for x in phrases:audit.append(f"- MISSING FILE | {x} | {rel}")
        continue
    t=p.read_text(encoding="utf-8")
    block=marker+"\n\n"+"\n".join("- "+x for x in phrases)+"\n\n위 표현들은 진단명이 아니라 **환자가 실제로 검색하거나 진료실에서 말할 수 있는 표현**입니다. 같은 표현도 원인이 여러 가지일 수 있으므로 위험신호·감별 → 한의학적 병증 → 치료 순으로 확인합니다.\n"
    if marker in t:t=t.split(marker,1)[0].rstrip()+"\n\n"+block
    else:t=t.rstrip()+"\n\n"+block
    p.write_text(t,encoding="utf-8");updated.append(rel)
    for x in phrases:audit.append(f"- OK | {x} | {rel}")
idx=docs/"conditions/index.md"
if idx.exists():
    t=idx.read_text(encoding="utf-8")
    if "## 환자 표현으로 찾기" not in t:
        t += "\n\n## 환자 표현으로 찾기\n\n질환명을 몰라도 괜찮습니다. 검색창에 **허리가 아파요, 밥 먹으면 더부룩해요, 기침이 오래가요, 자도 피곤해요, 가슴이 두근거려요**처럼 지금 불편한 증상을 평소 표현대로 입력해 보세요.\n"
        idx.write_text(t,encoding="utf-8")
Path("PATIENT_SEARCH_PHRASE_AUDIT.md").write_text("\n".join(audit)+"\n",encoding="utf-8")
print("UPDATED",len(updated),"pages")
print("MISSING TARGET FILES:",missing if missing else "none")
print("AUDIT: PATIENT_SEARCH_PHRASE_AUDIT.md")
