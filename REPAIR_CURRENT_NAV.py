from pathlib import Path
import yaml

p=Path("mkdocs.yml")
if not p.exists():
    raise SystemExit("mkdocs.yml이 있는 저장소 최상위에서 실행하세요.")

cfg=yaml.safe_load(p.read_text(encoding="utf-8-sig"))
if not isinstance(cfg,dict) or not isinstance(cfg.get("nav"),list):
    raise SystemExit("mkdocs.yml nav를 읽을 수 없습니다.")

# Current screenshot: 1 herb comparison + 12 Sasang formulas exist in docs but are absent from nav.
herb_path="herbal-integrated/herb-comparisons.md"
v4=[
("황련청장탕","sasang-formula-library/hwangryeoncheongjang-tang.md"),
("갈근해기탕","sasang-formula-library/galgeunhaegi-tang.md"),
("갈근승기탕","sasang-formula-library/galgeunseunggi-tang.md"),
("승지조위탕","sasang-formula-library/seungjijowi-tang.md"),
("승양팔물탕","sasang-formula-library/seungyangpalmul-tang.md"),
("향부자팔물탕","sasang-formula-library/hyangbujapalmul-tang.md"),
("향소산","sasang-formula-library/hyangso-san.md"),
("궁귀향소산","sasang-formula-library/gunggwihyangso-san.md"),
("계지부자탕","sasang-formula-library/gyejibujatang.md"),
("인삼계지부자탕","sasang-formula-library/insamgyejibujatang.md"),
("오수유부자이중탕","sasang-formula-library/osuyubujairijung-tang.md"),
("궁귀총소이중탕","sasang-formula-library/gunggwichongsoijung-tang.md"),
]

# 1) Herb comparison: place next to 본초 찾기, no version labels.
ok=False
for top in cfg["nav"]:
    if isinstance(top,dict) and "본초·방제" in top:
        items=top["본초·방제"]
        items[:]=[x for x in items if not (isinstance(x,dict) and "주요 본초 비교·감별" in x)]
        idx=next((i for i,x in enumerate(items) if isinstance(x,dict) and "본초 찾기" in x),0)
        items.insert(idx+1,{"주요 본초 비교·감별":herb_path})
        ok=True
        break
if not ok: raise SystemExit("본초·방제 nav를 찾지 못했습니다.")

# 2) Sasang formulas: integrate semantically, never show V3/V4/추가.
ok=False
for top in cfg["nav"]:
    if isinstance(top,dict) and "사상의학" in top:
        items=top["사상의학"]
        for item in items:
            if isinstance(item,dict) and "상세 자료실" in item:
                detail=item["상세 자료실"]
                # Remove old production/version labels if present.
                detail[:]=[x for x in detail if not (
                    isinstance(x,dict) and any(k in x for k in [
                        "사상처방 라이브러리 V4 추가","사상처방 라이브러리 V3",
                        "사상처방 V4 추가","사상처방 추가"
                    ])
                )]
                # Register these pages under semantic constitution groups.
                group={"사상처방 구성·용량 라이브러리":[
                    {"소양인 처방":[{"황련청장탕":v4[0][1]}]},
                    {"태음인 처방":[{n:path} for n,path in v4[1:4]]},
                    {"소음인 처방":[{n:path} for n,path in v4[4:]]},
                ]}
                # Avoid duplicate same group created by this repair.
                detail[:]=[x for x in detail if not (isinstance(x,dict) and "사상처방 구성·용량 라이브러리" in x)]
                detail.append(group)
                ok=True
                break
        break
if not ok: raise SystemExit("사상의학 > 상세 자료실 nav를 찾지 못했습니다.")

rendered=yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False,width=1000)
yaml.safe_load(rendered)
p.write_text(rendered,encoding="utf-8")
print("현재 누락 13개 NAV 등록: OK")
print("V3/V4/추가 같은 사용자용 버전 표시는 사용하지 않음: OK")
