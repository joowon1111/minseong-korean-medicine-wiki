from pathlib import Path
p=Path("docs/acupuncture-integrated/modalities.md")
marker="## 시술 전 공통 안전 체크"
block="""## 시술 전 공통 안전 체크

침·전침·부항·온열 등 치료수단을 정하기 전에:
- 해부학적 위험구조
- 출혈경향·항응고제
- 피부상태
- 임신
- 쇠약·실신경향
- 감각저하
- 전기자극 관련 상황
을 확인합니다.

→ [경혈별 해부학적 안전](points-meridians.md#경혈-위치와-해부학적-안전을-함께-보기)
"""
if p.exists():
    t=p.read_text(encoding="utf-8")
    if marker not in t:
        p.write_text(t.rstrip()+"\n\n"+block+"\n",encoding="utf-8")
        print("UPDATED:",p)
    else:
        print("OK:",p)
else:
    print("SKIP:",p)
