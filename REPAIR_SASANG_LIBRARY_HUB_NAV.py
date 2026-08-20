from pathlib import Path
import yaml

p=Path("mkdocs.yml")
if not p.exists():
    raise SystemExit("mkdocs.yml이 있는 저장소 최상위에서 실행하세요.")

cfg=yaml.safe_load(p.read_text(encoding="utf-8-sig"))
if not isinstance(cfg,dict) or not isinstance(cfg.get("nav"),list):
    raise SystemExit("mkdocs.yml nav를 읽을 수 없습니다.")

hub_group={
    "사상처방 구성·용량 라이브러리":[
        "sasang-formula-library/index.md",
        {"소양인 처방":[
            {"망음·표병":"sasang-formula-library/soyangin-exterior.md"},
            {"흉격열·리열":"sasang-formula-library/soyangin-interior-heat.md"},
            {"음허오열·하소":"sasang-formula-library/soyangin-yin-deficiency.md"},
            {"기타 주요 처방":"sasang-formula-library/soyangin-other.md"},
        ]},
        {"태음인 처방":[
            {"위완수한표한":"sasang-formula-library/taeeumin-exterior-cold.md"},
            {"간수열리열":"sasang-formula-library/taeeumin-interior-heat.md"},
            {"기타 주요 처방":"sasang-formula-library/taeeumin-other.md"},
        ]},
        {"소음인 처방":[
            {"태음병·리한":"sasang-formula-library/soeumin-taeeum.md"},
            {"망양·표병":"sasang-formula-library/soeumin-mangyang.md"},
            {"비위·기체·기타":"sasang-formula-library/soeumin-digestive.md"},
        ]},
    ]
}

found=False
for top in cfg["nav"]:
    if isinstance(top,dict) and "사상의학" in top:
        for item in top["사상의학"]:
            if isinstance(item,dict) and "상세 자료실" in item:
                detail=item["상세 자료실"]
                # Remove older production/version labels or duplicate library blocks.
                banned={
                    "사상처방 구성·용량 라이브러리",
                    "사상처방 라이브러리 V4 추가",
                    "사상처방 라이브러리 V3",
                    "사상처방 V4 추가",
                    "사상처방 추가",
                }
                detail[:]=[x for x in detail if not (isinstance(x,dict) and any(k in x for k in banned))]
                detail.append(hub_group)
                found=True
                break
        break

if not found:
    raise SystemExit("사상의학 > 상세 자료실을 찾지 못했습니다.")

rendered=yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False,width=1000)
yaml.safe_load(rendered)
p.write_text(rendered,encoding="utf-8")

print("사상처방 통합 허브 10개 NAV 등록: OK")
print("V3/V4/추가 같은 사용자용 버전 표시는 제거: OK")
