from pathlib import Path

root=Path("docs/symptom-integrated")
blocks={
"pain.md":"""## 한약치료

통증은 침·전침·약침 같은 국소·기능 치료와 함께 **한열·허실·어혈·담습·기혈·간신허 등 전신 병증**을 평가해 한약치료를 병행할 수 있습니다.

| 증상/병증축 | 대표적으로 비교할 처방 |
|---|---|
| 급성 한습·복합 실증성 요통 | 오적산 |
| 오래된 비증 + 간신기혈허 | 독활기생탕 |
| 고정통·자통·어혈 | 혈부축어탕 등 어혈방 |
| 기허 + 통락장애·저림 | 보양환오탕 |
| 두통·풍증 | 천궁다조산·청상견통탕 |
| 현훈·담습 동반 두통 | 반하백출천마탕 |
| 간양상항성 두통 | 천마구등음 |

한약은 통증 부위만 보고 선택하지 않고 **소화·수면·냉열·피로·대소변·병기**를 같이 봅니다.

→ [일반 방제 임상 지도](../herbal-integrated/general-formulary.md)
""",
"sleep-fatigue.md":"""## 한약치료

수면·피로 증상은 침·전침·약침과 함께 **심비양허·음혈부족·담울·기허·기음양허** 등의 병증에 따라 한약치료를 연결합니다.

| 증상/병증축 | 대표 처방 |
|---|---|
| 불면 + 심계·건망·피로 | 귀비탕 |
| 음혈부족·심신불안 | 천왕보심단 |
| 허번성 불면 | 산조인탕 |
| 담울 + 심번·경계 | 가미온담탕 |
| 비위기허·무력 | 보중익기탕 |
| 과로 후 기혈손상 | 쌍화탕 |
| 전반적 기혈양허 | 십전대보탕 |
| 기음양허·자한·구갈 | 생맥산 |

→ [일반 방제 임상 지도](../herbal-integrated/general-formulary.md)
""",
"digestive.md":"""## 한약치료

소화기 증상은 한약치료가 중요한 축입니다. 기능성소화불량 한의표준임상진료지침에서도 한약치료가 별도 치료영역으로 다뤄지며, 병증에 따라 처방을 구분합니다.

| 병증축 | 대표 처방 |
|---|---|
| 습체·창만 | 평위산 |
| 비기허 + 담습·기체 | 향사육군자탕 |
| 비위허한 | 향사양위탕 |
| 식적 | 보화환 |
| 한열착잡·심하비 | 반하사심탕 |
| 간울기체 | 소요산·시호소간산 |
| 담습·오심 | 이진탕 |
| 설사·수습 | 위령탕 등 병증별 비교 |

**체했다 = 한 처방**이 아니라 식사와의 관계·대변·한열·피로·스트레스·체중변화를 같이 봅니다.

→ [증상·치법으로 방제 찾기](../herbal-integrated/by-symptom-treatment.md)
""",
"respiratory-rhinitis.md":"""## 한약치료

비염·인후·기침·가래는 침·전침·약침과 함께 **풍한·풍열·폐열·담습·담열·폐기허·기음허**를 구분해 한약치료를 연결합니다.

| 증상/병증축 | 대표 처방 |
|---|---|
| 코막힘·비규 증상 | 창이자산 |
| 풍열·인후·비부 | 형개연교탕 |
| 풍열 초기·인후통 | 은교산 |
| 풍열성 기침 | 상국음 |
| 폐열·천해 | 마행감석탕 |
| 담열·천급 | 정천탕 |
| 상실하허·기역 | 소자강기탕 |
| 만성 폐기허성 기침 | 보폐탕 |
| 기음양허·진액손상 | 생맥산 |

호흡곤란·객혈·고열 등 위험신호가 있으면 한약 선택보다 필요한 평가가 우선입니다.

→ [일반 방제 임상 지도](../herbal-integrated/general-formulary.md)
""",
"autonomic-stress.md":"""## 한약치료

자율신경·스트레스 증상은 국소 치료만으로 설명되지 않는 경우가 많아 **간울·기체·담울·심비양허·울열·수습·양허** 등 전신 병증에 따른 한약치료를 함께 봅니다.

| 증상/병증축 | 대표 처방 |
|---|---|
| 간울 + 혈허·비허 | 소요산 |
| 간울 + 울열 | 가미소요산 |
| 간기울결·흉협만 | 시호소간산 |
| 칠정기울·흉복비체 | 분심기음 |
| 목 이물감·담기울결 | 반하후박탕 |
| 담울 + 불면·심계 | 가미온담탕 |
| 비허담습성 현훈 | 반하백출천마탕 |
| 간양상항성 현훈 | 천마구등음 |
| 수습 | 오령산·저령탕 |
| 양허수기·냉증부종 | 진무탕 |

→ [일반 방제 임상 지도](../herbal-integrated/general-formulary.md)
"""
}

for fn,block in blocks.items():
    p=root/fn
    if not p.exists():
        print("SKIP:",p); continue
    t=p.read_text(encoding="utf-8")
    marker="## 한약치료"
    if marker in t:
        # Keep everything before the old herbal section, replace only that section to avoid duplicates.
        t=t.split(marker)[0].rstrip()+"\n\n"+block.strip()+"\n"
    else:
        t=t.rstrip()+"\n\n"+block.strip()+"\n"
    p.write_text(t,encoding="utf-8")
    print("UPDATED:",p)

# Treatment-evidence gets one integration statement.
p=root/"treatment-evidence.md"
if p.exists():
    t=p.read_text(encoding="utf-8")
    marker="## 주요 증상의 한약치료를 함께 보기"
    block="""## 주요 증상의 한약치료를 함께 보기

주요 증상 페이지에서는 침·전침·약침뿐 아니라 **한약치료를 동일한 핵심 치료축**으로 표시합니다.

`증상 → 감별 → 한의 병증 → 한약 + 침/전침/약침 → 생활관리 → 재평가`

한약은 전신 병증을, 침구·약침은 경락·기능·국소 치료목표를 상대적으로 더 구체적으로 다룰 수 있으므로 환자 상태에 따라 단독 또는 병행합니다.

→ [통증](pain.md#한약치료) · [수면·피로](sleep-fatigue.md#한약치료) · [소화](digestive.md#한약치료) · [호흡·비염](respiratory-rhinitis.md#한약치료) · [자율신경·스트레스](autonomic-stress.md#한약치료)
"""
    if marker not in t:
        p.write_text(t.rstrip()+"\n\n"+block.strip()+"\n",encoding="utf-8")
        print("UPDATED:",p)
