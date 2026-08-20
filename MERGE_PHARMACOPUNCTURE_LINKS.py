from pathlib import Path

def append_once(path, marker, block):
    p=Path(path)
    if not p.exists():
        print("SKIP:", path)
        return
    t=p.read_text(encoding="utf-8")
    if marker in t:
        print("OK:", path)
        return
    p.write_text(t.rstrip()+"\n\n"+block.strip()+"\n", encoding="utf-8")
    print("UPDATED:", path)

append_once(
    "docs/acupuncture-integrated/index.md",
    "## 약침치료",
    """## 약침치료

통증·근골격계뿐 아니라 두통·자율신경·소화기·알레르기·피부 등에서 활용되는 약침을 독립적인 임상치료축으로 정리합니다.

→ [약침치료](pharmacopuncture.md)
"""
)

append_once(
    "docs/acupuncture-integrated/modalities.md",
    "## 약침",
    """## 약침

약침은 일반침과 달리 **약침액의 선택·주입·약물성 이상반응·품질관리**가 추가되는 침습적 치료입니다.

→ [약침치료 상세](pharmacopuncture.md)
"""
)

symptoms = {
    "docs/symptom-integrated/pain.md":
    """## 약침치료 연결

통증의 구조·MPS·경근·어혈·염증·허증을 구분한 뒤 약침을 치료축으로 검토합니다.

→ [약침치료](../acupuncture-integrated/pharmacopuncture.md#3-통증근골격계-약침)
""",
    "docs/symptom-integrated/autonomic-stress.md":
    """## 약침치료 연결

두근거림·흉민·상열감·긴장·어지럼 등은 위험신호를 먼저 감별하고 약침을 한약·체침·생활관리와 함께 검토합니다.

→ [약침치료](../acupuncture-integrated/pharmacopuncture.md#6-자율신경스트레스-관련-약침)
""",
    "docs/symptom-integrated/digestive.md":
    """## 약침치료 연결

소화기 증상에서는 기능성/구조적 감별 후 복부·비위·자율신경 치료축에서 약침을 검토합니다.

→ [약침치료](../acupuncture-integrated/pharmacopuncture.md#7-소화기-약침)
""",
    "docs/symptom-integrated/respiratory-rhinitis.md":
    """## 약침치료 연결

알레르기비염·호흡기 증상에서는 질환별 진단과 염증·알레르기 상태를 먼저 확인하고 약침을 보조치료축으로 봅니다.

→ [약침치료](../acupuncture-integrated/pharmacopuncture.md#8-면역알레르기호흡기-약침)
"""
}

for path, block in symptoms.items():
    append_once(path, "## 약침치료 연결", block)
