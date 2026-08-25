from pathlib import Path
import shutil,sys
p=Path("mkdocs.yml")
if not p.exists(): print("ERROR: mkdocs.yml 없음"); sys.exit(1)
t=p.read_text(encoding="utf-8-sig")
needle="        - 특정혈 분류와 배혈 원리: acupuncture-specific/pairing-principles.md\n"
if "특정혈 통합 아틀라스: acupuncture-specific/special-points-atlas.md" in t: print("이미 적용됨"); sys.exit()
if needle not in t: print("ERROR: 179 nav 먼저 적용 필요"); sys.exit(2)
insert=needle+"        - 특정혈 통합 아틀라스: acupuncture-specific/special-points-atlas.md\n        - 주요 경혈 다중속성 지도: acupuncture-specific/point-attribute-map.md\n"
shutil.copy2(p,"_backup_mkdocs_180.yml"); p.write_text(t.replace(needle,insert,1),encoding="utf-8"); print("180 nav 적용 완료")
