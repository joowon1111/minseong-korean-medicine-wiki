from pathlib import Path
import shutil,sys
from datetime import datetime
p=Path("mkdocs.yml")
if not p.exists(): print("ERROR: mkdocs.yml 없음"); sys.exit(1)
t=p.read_text(encoding="utf-8-sig")
if "특정혈·배혈 임상 지식망:" in t: print("이미 nav에 있음"); sys.exit(0)
needle="      - WHO 표준 361경혈 아틀라스: acupoint-network/standard-atlas.md\n"
insert=needle+'''      - 특정혈·배혈 임상 지식망:
        - acupuncture-specific/index.md
        - 오수혈·오행 통합표: acupuncture-specific/five-shu.md
        - 특정혈 분류와 배혈 원리: acupuncture-specific/pairing-principles.md
        - 사암침법 기초 지식망: acupuncture-specific/saam-acupuncture.md
'''
if needle not in t: print("ERROR: WHO 표준 361경혈 nav 위치를 찾지 못함"); sys.exit(2)
shutil.copy2(p,Path("_backup_mkdocs_179.yml"))
p.write_text(t.replace(needle,insert,1),encoding="utf-8")
print("179 nav 추가 완료")
