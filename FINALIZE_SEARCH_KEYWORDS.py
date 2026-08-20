from pathlib import Path

docs = Path("docs")

keyword_map = {
    "conditions/common-cold.md": [
        "감기","감모","몸살","급성 상기도감염","상기도감염","감기몸살",
        "목감기","콧물감기","기침감기","인후통","감기 한약","감기 보험한약"
    ],
    "herbal-integrated/insurance-herbal.md": [
        "건강보험","건강보험 한약제제","보험한약","보험 한약","급여 한약제제",
        "급여한약","56처방","56개 기준처방","단미엑스혼합제"
    ],
    "conditions/cough.md": [
        "기침","급성기침","만성기침","마른기침","가래기침","감기기침",
        "기침 한약","기침 보험한약","급성기관지염","가래"
    ],
    "conditions/rhinitis.md": [
        "비염","알레르기비염","알레르기 비염","콧물","코막힘","재채기",
        "비염 한약","비염 보험한약"
    ],
    "acupuncture-integrated/modalities.md": [
        "약침","약침치료","pharmacopuncture","봉약침","봉독약침","Bee Venom",
        "Sweet BV","중성어혈약침","황련해독탕약침","자하거약침","홍화약침",
        "홍화녹용약침","산삼약침","산양산삼약침","통증 약침","두통 약침",
        "자율신경 약침","소화기 약침","면역 약침","피부 약침"
    ],
    "acupuncture-integrated/points-meridians.md": [
        "경혈","혈자리","침자리","경락","12경맥","십이경맥","경맥 유주","표리관계",
        "오수혈","정형수경합","원혈","락혈","극혈","배수혈","모혈","팔회혈","하합혈",
        "팔맥교회혈","12경근","십이경근","경근","락맥","15락맥","경별","12경별",
        "기경팔맥","독맥","임맥","충맥","대맥","음교맥","양교맥","음유맥","양유맥",
        "골도분촌","동신촌","취혈","취혈법","경혈 위치","해부학적 안전",
        "MPS","근막통증증후군","Myofascial Pain Syndrome","Trigger point","트리거포인트",
        "통증유발점","아시혈","태극침법","태극침","이침","이침치료","이혈","이혈치료"
    ],
    "conditions/dyspepsia.md": ["소화불량","체기","체함","더부룩함","복부팽만","소화 한약","소화 보험한약"],
    "conditions/chronic-fatigue.md": ["만성피로","피로","기력저하","기운없음","허약","보약","피로 한약"],
    "conditions/low-back-pain.md": ["요통","허리통증","허리 아픔","만성요통","요통 한약","허리 약침"],
    "conditions/neck-pain.md": ["목통증","경항통","뒷목통증","경추통","목 한약","목 약침"],
    "conditions/shoulder-pain.md": ["어깨통증","견비통","오십견","어깨 한약","어깨 약침"],
    "conditions/knee-pain.md": ["무릎통증","슬통","무릎관절통","무릎 한약","무릎 약침"],
    "conditions/headache.md": ["두통","편두통","긴장성두통","긴장형두통","두통 한약","두통 약침"],
    "conditions/dizziness.md": ["어지럼","어지럼증","현훈","머리가 띵함","빙빙 도는 느낌","현훈 한약"],
    "conditions/menopause.md": ["갱년기","폐경","안면홍조","상열감","갱년기 한약"],
    "conditions/postpartum-recovery.md": ["산후회복","산후조리","산후보약","산후 한약","산후풍"],
    "symptom-integrated/autonomic-stress.md": [
        "자율신경","자율신경실조","스트레스","두근거림","가슴답답","상열감",
        "매핵기","자율신경 한약","자율신경 약침"
    ],
}

marker = "## 검색 동의어"

updated = []
missing_files = []

for rel, kws in keyword_map.items():
    p = docs / rel
    if not p.exists():
        missing_files.append(rel)
        continue
    t = p.read_text(encoding="utf-8")
    block = marker + "\n\n" + " · ".join(dict.fromkeys(kws)) + \
        "\n\n> 같은 임상 주제를 환자 표현·한의학 용어·영문 용어로도 검색할 수 있도록 연결한 검색 동의어입니다.\n"
    if marker in t:
        before = t.split(marker, 1)[0].rstrip()
        t = before + "\n\n" + block
    else:
        t = t.rstrip() + "\n\n" + block
    p.write_text(t, encoding="utf-8")
    updated.append(rel)

# Audit all required major terms across docs after patch.
required = [
    "감기","감모","몸살","급성 상기도감염","기침","비염",
    "건강보험","보험한약","건강보험 한약제제","56처방",
    "한약","한약치료","약침","약침치료","봉약침","Sweet BV",
    "중성어혈약침","황련해독탕약침","자하거약침",
    "MPS","근막통증증후군","Trigger point","태극침법","이침","이혈치료",
    "경혈","경락","12경맥","오수혈","원혈","락혈","극혈","배수혈","모혈",
    "팔회혈","하합혈","팔맥교회혈","12경근","경별","기경팔맥",
    "골도분촌","취혈","해부학적 안전",
    "소화불량","만성피로","요통","목통증","어깨통증","무릎통증",
    "두통","어지럼","갱년기","산후회복","자율신경"
]

all_docs = []
for p in docs.rglob("*.md"):
    try:
        all_docs.append((p, p.read_text(encoding="utf-8")))
    except Exception:
        pass

audit = ["# 핵심 검색어 최종 점검", ""]
missing_terms = []
for kw in required:
    hits = [str(p.relative_to(docs)) for p, text in all_docs if kw.lower() in text.lower()]
    status = "OK" if hits else "MISSING"
    if not hits:
        missing_terms.append(kw)
    audit.append(f"- {status} | {kw} | {', '.join(hits[:6])}")

Path("SEARCH_KEYWORD_FINAL_AUDIT.md").write_text("\n".join(audit) + "\n", encoding="utf-8")

print(f"UPDATED: {len(updated)} pages")
if missing_files:
    print("MISSING FILES (non-fatal):")
    for x in missing_files:
        print(" -", x)
if missing_terms:
    print("MISSING TERMS:")
    for x in missing_terms:
        print(" -", x)
else:
    print("ALL REQUIRED KEYWORDS FOUND IN DOCS")
print("AUDIT: SEARCH_KEYWORD_FINAL_AUDIT.md")
