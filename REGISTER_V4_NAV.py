from pathlib import Path
import yaml
p=Path("mkdocs.yml")
if not p.exists():
    raise SystemExit("mkdocs.yml이 있는 저장소 최상위에서 실행하세요.")
cfg=yaml.safe_load(p.read_text(encoding="utf-8-sig"))

entries=[
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

found=False
for top in cfg["nav"]:
    if isinstance(top,dict) and "사상의학" in top:
        for item in top["사상의학"]:
            if isinstance(item,dict) and "상세 자료실" in item:
                detail=item["상세 자료실"]
                detail[:]=[x for x in detail if not (isinstance(x,dict) and "사상처방 라이브러리 V4 추가" in x)]
                detail.append({"사상처방 라이브러리 V4 추가":[{a:b} for a,b in entries]})
                found=True
                break
if not found:
    raise SystemExit("사상의학 > 상세 자료실을 찾지 못했습니다.")

rendered=yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False,width=1000)
yaml.safe_load(rendered)
p.write_text(rendered,encoding="utf-8")
print("V4 처방 12개 nav 등록: OK")
