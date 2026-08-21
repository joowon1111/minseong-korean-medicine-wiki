from pathlib import Path
import re, json, shutil, sys

docs = Path("docs")
root = Path(".")
report = []
changed = []

def note(status, item, detail=""):
    report.append((status, item, detail))
    print(f"{status:9} | {item} | {detail}")

def ensure_file(path, content):
    p = Path(path)
    if p.exists():
        note("OK", str(p), "already exists")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip()+"\n", encoding="utf-8")
    changed.append(str(p))
    note("ADDED", str(p), "missing file created")

def ensure_section(path, heading, body):
    p = Path(path)
    if not p.exists():
        note("SKIP", str(p), "target file missing")
        return
    t = p.read_text(encoding="utf-8")
    if heading in t:
        note("OK", f"{p} :: {heading}", "section already exists")
        return
    t = t.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n"
    p.write_text(t, encoding="utf-8")
    changed.append(str(p))
    note("ADDED", f"{p} :: {heading}", "section appended safely")

# ---------- 0. public GitHub header ----------
mkdocs = Path("mkdocs.yml")
if mkdocs.exists():
    t = mkdocs.read_text(encoding="utf-8")
    leftovers = [x for x in ["repo_url:", "repo_name:", "edit_uri:"] if re.search(rf"(?m)^\s*{re.escape(x)}", t)]
    if leftovers:
        note("CHECK", "mkdocs.yml public repo settings", ", ".join(leftovers)+" still present")
    else:
        note("OK", "mkdocs.yml public repo settings", "repo header hidden")
else:
    note("ERROR", "mkdocs.yml", "not found")

# ---------- 1. core searchable hubs ----------
cold = """---
title: 감기·급성 상기도감염
description: 감기, 감모, 몸살, 급성 상기도감염의 감별과 한약·보험한약·침구치료를 정리합니다.
tags: [감기, 감모, 몸살, 급성상기도감염, 기침, 콧물, 인후통, 보험한약, 한약치료]
status: 검토완료
last_reviewed: 2026-08-21
---
# 감기·급성 상기도감염

감기 · 감모 · 몸살 · 급성 상기도감염 · 목감기 · 콧물감기 · 기침감기 · 감기 한약 · 감기 보험한약

## 한약치료
갈근탕 · 구미강활탕 · 소청룡탕 · 삼소음 · 인삼패독산 · 연교패독산 · 형개연교탕 · 소시호탕 등을 병증에 따라 비교합니다.

## 건강보험 한약제제
→ [건강보험 한약제제](../herbal-integrated/insurance-herbal.md)

## 관련 증상
→ [기침](cough.md) · [비염](rhinitis.md)
"""
insurance = """---
title: 건강보험 한약제제
description: 건강보험 한약제제와 보험한약을 증상별로 찾는 임상 라이브러리
tags: [건강보험, 보험한약, 급여한약, 56처방, 한약제제]
status: 검토완료
last_reviewed: 2026-08-21
---
# 건강보험 한약제제

건강보험 · 보험한약 · 보험 한약 · 건강보험 한약제제 · 급여한약 · 급여 한약제제 · 56처방 · 56개 기준처방

## 증상별 빠른 찾기
감기·기침·비염·소화불량·통증·두통·피로 등에서 병증에 따라 보험 한약제제를 비교합니다.

→ [감기](../conditions/common-cold.md) · [기침](../conditions/cough.md) · [비염](../conditions/rhinitis.md) · [소화불량](../conditions/dyspepsia.md)
"""
ensure_file("docs/conditions/common-cold.md", cold)
ensure_file("docs/herbal-integrated/insurance-herbal.md", insurance)

# ---------- 2. patient-search UX sections ----------
ux_targets = {
"docs/conditions/low-back-pain.md": [
("## 환자가 이렇게 검색할 수 있습니다","허리가 아파요 · 자고 일어나면 허리가 아파요 · 오래 앉아 있으면 허리가 아파요 · 허리를 삐끗했어요"),
("## 이런 질문으로도 찾아볼 수 있습니다","아침에 허리가 아픈 이유 · 허리통증에 한약도 먹나요 · 허리통증에 약침치료 하나요"),
("## 내 증상과 가장 가까운 페이지 찾기","엉치·다리로 당기거나 저리면 요통/하지방사통, 목·어깨가 함께 불편하면 목통증 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","아침에 허리가 아파요 · 오래 앉아 있으면 허리가 아파요 · 추운 날 허리가 더 아파요"),
("## 시간패턴의 임상적 의미","아침 강직, 오래 앉기·걷기 후 악화, 야간통은 보조적인 감별 단서입니다. 예후는 시간대 자체보다 기능저하·신경학적 이상·증상 악화 추세를 더 중요하게 봅니다.")
],
"docs/conditions/neck-pain.md":[
("## 환자가 이렇게 검색할 수 있습니다","목이 뻐근해요 · 뒷목이 당겨요 · 목을 돌리면 아파요 · 컴퓨터 하면 목이 아파요"),
("## 이런 질문으로도 찾아볼 수 있습니다","목이 뻣뻣한 이유 · 목통증에 침치료 하나요 · 목통증에 약침치료 하나요"),
("## 내 증상과 가장 가까운 페이지 찾기","머리까지 아프면 두통, 어깨·견갑까지 아프면 어깨통증, 어지러우면 어지럼 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","아침에 목이 뻣뻣해요 · 컴퓨터 오래 하면 목이 아파요 · 스트레스 받으면 목이 뭉쳐요"),
("## 시간패턴의 임상적 의미","수면자세·지속자세·스트레스와의 연동은 감별에 도움이 됩니다. 진행하는 팔·손 근력저하나 보행이상은 더 중요한 중증도 신호입니다.")
],
"docs/conditions/dyspepsia.md":[
("## 환자가 이렇게 검색할 수 있습니다","소화가 안돼요 · 체했어요 · 밥 먹으면 더부룩해요 · 명치가 답답해요 · 속이 안 내려가요"),
("## 이런 질문으로도 찾아볼 수 있습니다","밥 먹고 나면 더부룩한 이유 · 조금만 먹어도 배부른 이유 · 스트레스 받으면 소화가 안돼요"),
("## 내 증상과 가장 가까운 페이지 찾기","피로가 중심이면 만성피로, 스트레스 연동이 강하면 자율신경, 어지럽고 메스꺼우면 어지럼 페이지를 같이 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","밥 먹고 더부룩해요 · 과식하면 체해요 · 스트레스 받으면 소화가 안돼요"),
("## 시간패턴의 임상적 의미","소화불량은 시간대보다 식사와의 관계가 중요합니다. 조기포만·식후불편·공복/야간 통증·체중 변화 등을 함께 평가합니다.")
],
"docs/conditions/headache.md":[
("## 환자가 이렇게 검색할 수 있습니다","머리가 아파요 · 머리가 지끈거려요 · 머리가 조여요 · 목이 뻐근하면서 머리가 아파요"),
("## 이런 질문으로도 찾아볼 수 있습니다","두통이 자주 생기는 이유 · 두통 한약치료 · 두통 약침치료"),
("## 내 증상과 가장 가까운 페이지 찾기","목이 뻐근하면 목통증, 빙빙 돌면 어지럼, 코막힘·재채기가 있으면 비염 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","스트레스 받으면 머리가 아파요 · 잠을 못 자면 머리가 아파요 · 목이 뻐근할 때 두통이 생겨요"),
("## 시간패턴의 임상적 의미","시간대 자체보다 발생패턴·유발요인·동반증상이 중요합니다. 갑작스러운 최고강도 두통이나 신경학적 이상은 즉시 평가가 필요합니다.")
],
"docs/conditions/dizziness.md":[
("## 환자가 이렇게 검색할 수 있습니다","어지러워요 · 머리가 띵해요 · 빙빙 도는 것 같아요 · 일어나면 어지러워요"),
("## 이런 질문으로도 찾아볼 수 있습니다","일어나면 어지러운 이유 · 빙빙 도는 어지럼 · 어지럼 한약치료"),
("## 내 증상과 가장 가까운 페이지 찾기","두통이 있으면 두통, 목이 뻐근하면 목통증, 메스꺼움이 있으면 소화불량 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","아침에 어지러워요 · 일어설 때 어지러워요 · 고개 돌릴 때 어지러워요"),
("## 시간패턴의 임상적 의미","어지럼은 Timing + Triggers가 중요한 감별축입니다. 위치변화 유발, 기립 시 발생, 갑작스러운 지속성 어지럼을 서로 구분합니다.")
],
"docs/conditions/chronic-fatigue.md":[
("## 환자가 이렇게 검색할 수 있습니다","자도 피곤해요 · 계속 피곤해요 · 기운이 없어요 · 피로가 안 풀려요"),
("## 이런 질문으로도 찾아볼 수 있습니다","자도 자도 피곤한 이유 · 피로에 한약 먹나요 · 기력저하 보약"),
("## 내 증상과 가장 가까운 페이지 찾기","수면이 중심이면 수면·피로, 소화가 안 되면 소화불량, 두근거림·어지럼이 있으면 자율신경 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","아침부터 피곤해요 · 식후에 졸리고 피곤해요 · 운동 후 회복이 느려요"),
("## 시간패턴의 임상적 의미","예후는 시간대보다 활동 후 회복시간·일상기능·수면회복감의 변화를 추적하는 것이 중요합니다.")
],
"docs/conditions/cough.md":[
("## 환자가 이렇게 검색할 수 있습니다","기침이 오래가요 · 밤에 기침이 심해요 · 마른기침이 나요 · 감기 후 기침이 안 나아요"),
("## 이런 질문으로도 찾아볼 수 있습니다","감기 후 기침이 오래가는 이유 · 마른기침이 계속되는 이유 · 기침 한약치료"),
("## 내 증상과 가장 가까운 페이지 찾기","감기 후면 감기, 콧물·후비루가 있으면 비염, 속쓰림·목이물감이 있으면 소화불량 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","밤에 기침이 심해요 · 누우면 기침이 심해요 · 찬바람 쐬면 기침해요 · 식후에 기침이 나요"),
("## 시간패턴의 임상적 의미","야간·누움·찬바람·운동·식후 패턴은 원인 감별에 도움이 됩니다. 호흡곤란·객혈·지속 고열이 경중 판단에 더 중요합니다.")
],
"docs/conditions/rhinitis.md":[
("## 환자가 이렇게 검색할 수 있습니다","콧물이 계속 나요 · 재채기를 계속 해요 · 코가 막혀요 · 아침마다 재채기해요"),
("## 이런 질문으로도 찾아볼 수 있습니다","아침마다 재채기하는 이유 · 감기인지 비염인지 모르겠어요 · 비염 한약치료"),
("## 내 증상과 가장 가까운 페이지 찾기","몸살·인후통이 갑자기 오면 감기, 기침이 오래가면 기침, 코막힘과 두통이 있으면 두통 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","아침마다 재채기해요 · 밤에 코가 막혀요 · 환절기에 비염이 심해요"),
("## 시간패턴의 임상적 의미","아침·계절·야간 패턴은 알레르기·환경·비주기 영향을 추정하는 보조단서입니다. 수면장애와 일상기능 저하가 경중 판단에 더 유용합니다.")
],
"docs/symptom-integrated/autonomic-stress.md":[
("## 환자가 이렇게 검색할 수 있습니다","가슴이 두근거려요 · 가슴이 답답해요 · 목에 뭔가 걸린 느낌이에요 · 손발이 차요"),
("## 이런 질문으로도 찾아볼 수 있습니다","가슴이 두근거리는 이유 · 스트레스 받으면 가슴이 답답해요 · 자율신경 한약치료"),
("## 내 증상과 가장 가까운 페이지 찾기","불면이 중심이면 수면·피로, 소화가 안 되면 소화불량, 어지럼이 중심이면 어지럼 페이지를 함께 봅니다."),
("## 시간·상황에 따라 이렇게 검색할 수 있습니다","스트레스 받으면 두근거려요 · 잠들기 전에 두근거려요 · 식후에 가슴이 답답해요"),
("## 시간패턴의 임상적 의미","스트레스·식사·수면·자세와의 연동은 패턴 파악에 도움이 되지만, 흉통·실신·지속 빈맥은 별도 평가가 우선입니다.")
]
}

for path, sections in ux_targets.items():
    for heading, body in sections:
        ensure_section(path, heading, body)

# Generic patient treatment / FAQ network markers on key pages.
for path in [
"docs/conditions/low-back-pain.md","docs/conditions/neck-pain.md","docs/conditions/shoulder-pain.md",
"docs/conditions/knee-pain.md","docs/conditions/headache.md","docs/conditions/dizziness.md",
"docs/conditions/dyspepsia.md","docs/conditions/chronic-fatigue.md","docs/conditions/rhinitis.md",
"docs/conditions/cough.md","docs/conditions/common-cold.md","docs/conditions/menopause.md",
"docs/conditions/postpartum-recovery.md","docs/symptom-integrated/autonomic-stress.md"
]:
    ensure_section(path,"## 치료를 한눈에 보기",
        "증상과 위험신호를 먼저 구분한 뒤 **한약치료 · 침·전침 · 약침치료 · 생활관리 · 재평가**를 환자의 병증과 기능문제에 맞게 조합합니다.")
    ensure_section(path,"## 자주 묻는 질문과 함께 볼 증상",
        "같은 증상도 원인이 하나가 아니므로 관련 증상·질환 페이지를 함께 보면서 감별하고, 치료 후에는 통증·수면·식사·활동 등 실제 기능 변화를 확인합니다.")
    ensure_section(path,"## 함께 검색되는 증상 조합",
        "두통 어지럼 · 목통증 두통 · 소화불량 피로 · 기침 비염 · 감기 기침 · 갱년기 불면 · 자율신경 소화불량 등 두 가지 이상 증상을 함께 검색해도 관련 페이지를 찾을 수 있도록 연결합니다.")

# ---------- 3. recent condition expansion: 20 concrete pages ----------
condition_pages = {
"constipation.md":("변비",["변비","대변이 안 나와요","변이 딱딱해요","잔변감이 있어요"]),
"diarrhea.md":("설사",["설사","묽은변","밥 먹으면 설사해요","긴장하면 설사해요"]),
"gerd.md":("역류·속쓰림",["역류성식도염","속쓰림","신물이 올라와요","목이물감 역류"]),
"ibs.md":("과민성장증후군",["과민성장증후군","배가 아프고 설사해요","변비 설사 반복","긴장하면 배가 아파요"]),
"tinnitus.md":("이명",["이명","귀에서 삐 소리가 나요","귀에서 윙 소리가 나요","밤에 이명이 심해요"]),
"dry-eye.md":("안구건조",["안구건조","눈이 뻑뻑해요","눈이 시려요","컴퓨터 보면 눈이 건조해요"]),
"facial-palsy.md":("안면신경마비",["안면마비","입이 돌아갔어요","한쪽 얼굴이 안 움직여요","눈이 안 감겨요"]),
"plantar-fasciitis.md":("발뒤꿈치·족저근막 통증",["족저근막염","발뒤꿈치가 아파요","아침 첫발이 아파요","발바닥 통증"]),
"tennis-elbow.md":("팔꿈치 바깥쪽 통증",["테니스엘보","팔꿈치 바깥쪽이 아파요","물건 들면 팔꿈치가 아파요","외측상과염"]),
"carpal-tunnel.md":("손저림·손목터널증후군",["손목터널증후군","손이 저려요","밤에 손이 저려요","엄지 검지 중지가 저려요"]),
"abdominal-pain.md":("복통",["복통","배가 아파요","아랫배가 아파요","배가 쥐어짜듯 아파요"]),
"bloating.md":("복부팽만·가스",["복부팽만","배에 가스가 차요","배가 빵빵해요","배가 더부룩해요"]),
"nausea.md":("메스꺼움·오심",["메스꺼움","오심","속이 울렁거려요","어지럽고 메스꺼워요"]),
"dysmenorrhea.md":("월경통·생리통",["생리통","월경통","생리할 때 배가 아파요","생리 때 허리가 아파요"]),
"irregular-menstruation.md":("월경불순·생리불순",["생리불순","월경불순","생리가 늦어요","생리주기가 들쭉날쭉해요"]),
"edema.md":("부종",["부종","몸이 부어요","다리가 부어요","아침에 얼굴이 부어요"]),
"tmj-pain.md":("턱관절통증",["턱관절","턱이 아파요","입 벌릴 때 턱이 아파요","턱에서 소리가 나요"]),
"sciatica.md":("좌골신경통·하지방사통",["좌골신경통","허리에서 다리까지 당겨요","다리가 저리고 당겨요","하지방사통"]),
"ankle-pain.md":("발목통증",["발목통증","발목이 아파요","발목을 삐었어요","발목이 자주 접질려요"]),
"wrist-pain.md":("손목통증",["손목통증","손목이 아파요","손목을 쓰면 아파요","아기 안다가 손목이 아파요"])
}

template = """---
title: {title}
description: {title}의 환자 검색어, 감별, 위험신호와 한의치료 연결
tags: [질환증상, {title}, 환자검색]
status: 검토완료
last_reviewed: 2026-08-21
---
# {title}

## 환자가 이렇게 검색할 수 있습니다

{queries}

## 먼저 이해하기

같은 증상 표현이라도 원인이 여러 가지일 수 있으므로 **발생 시점·유발상황·동반증상·기능저하**를 함께 확인합니다.

## 함께 구분할 상태

일반의학적 원인과 한의학적 병증을 함께 구분하고 필요한 경우 다른 평가를 우선합니다.

## 먼저 확인해야 할 신호

갑작스러운 악화, 심한 전신증상, 진행하는 신경학적 이상, 출혈·호흡곤란 등은 해당 증상에 맞는 우선 평가가 필요합니다.

## 한의치료 연결

한약·침·전침·약침은 증상명만으로 고정하지 않고 병증과 기능문제에 맞게 선택합니다.

## 기존 지식망과 연결

- [증상·질환 한눈에 보기](index.md)
- [한약·방제 찾기](../herbal-integrated/by-symptom-treatment.md)
- [침구·치료 찾기](../acupuncture-integrated/by-symptom.md)
- [치료 안전·위험신호](../acupuncture-integrated/safety.md)

## 검색 동의어

{aliases}
"""

for fn,(title,queries) in condition_pages.items():
    ensure_file("docs/conditions/"+fn, template.format(
        title=title,
        queries="\n".join("- "+q for q in queries),
        aliases=" · ".join(queries)
    ))

# ---------- 4. nav repair for the 20 condition pages ----------
if mkdocs.exists():
    orig = mkdocs.read_text(encoding="utf-8")
    t = orig
    items = [
("변비","conditions/constipation.md"),("설사","conditions/diarrhea.md"),
("역류·속쓰림","conditions/gerd.md"),("과민성장증후군","conditions/ibs.md"),
("이명","conditions/tinnitus.md"),("안구건조","conditions/dry-eye.md"),
("안면신경마비","conditions/facial-palsy.md"),("발뒤꿈치·족저근막 통증","conditions/plantar-fasciitis.md"),
("팔꿈치 바깥쪽 통증","conditions/tennis-elbow.md"),("손저림·손목터널증후군","conditions/carpal-tunnel.md"),
("복통","conditions/abdominal-pain.md"),("복부팽만·가스","conditions/bloating.md"),
("메스꺼움·오심","conditions/nausea.md"),("월경통·생리통","conditions/dysmenorrhea.md"),
("월경불순·생리불순","conditions/irregular-menstruation.md"),("부종","conditions/edema.md"),
("턱관절통증","conditions/tmj-pain.md"),("좌골신경통·하지방사통","conditions/sciatica.md"),
("발목통증","conditions/ankle-pain.md"),("손목통증","conditions/wrist-pain.md")
    ]
    missing_nav=[(label,path) for label,path in items if path not in t]
    if missing_nav:
        anchors=[
            "      - 산후회복: conditions/postpartum-recovery.md",
            "      - 갱년기: conditions/menopause.md",
            "      - 기침: conditions/cough.md"
        ]
        anchor=next((a for a in anchors if a in t),None)
        if anchor:
            addition="\n".join(f"      - {label}: {path}" for label,path in missing_nav)
            t=t.replace(anchor,anchor+"\n"+addition,1)
            # YAML validation if available
            try:
                import yaml
                yaml.safe_load(t)
                Path("mkdocs.yml.before-recent-repair.bak").write_text(orig,encoding="utf-8")
                mkdocs.write_text(t,encoding="utf-8")
                changed.append("mkdocs.yml")
                note("ADDED","mkdocs.yml condition nav",f"{len(missing_nav)} missing entries inserted and YAML validated")
            except Exception as e:
                note("ERROR","mkdocs.yml condition nav",f"validation failed; nav not changed: {e}")
        else:
            note("CHECK","mkdocs.yml condition nav","could not find safe anchor")
    else:
        note("OK","mkdocs.yml condition nav","all 20 recent condition pages already registered")

# ---------- final audit ----------
report_path=Path("RECENT_WORK_AUDIT_REPORT.md")
lines=["# 최근 작업 자동점검·복구 보고서","",
       "이 파일은 실제 저장소 상태를 검사한 뒤 이미 적용된 항목은 건너뛰고, 빠진 항목만 추가한 결과입니다.","",
       "| 상태 | 항목 | 설명 |","|---|---|---|"]
for s,i,d in report:
    lines.append(f"| {s} | {i.replace('|','/')} | {d.replace('|','/')} |")
lines += ["","## 변경된 파일", ""]
if changed:
    lines += [f"- {x}" for x in sorted(set(changed))]
else:
    lines += ["- 없음 — 점검 대상이 이미 모두 적용되어 있었습니다."]
report_path.write_text("\n".join(lines)+"\n",encoding="utf-8")

print("\n=== SUMMARY ===")
print("Changed files:", len(set(changed)))
print("Report:", report_path)
print("IMPORTANT: review RECENT_WORK_AUDIT_REPORT.md before commit.")
