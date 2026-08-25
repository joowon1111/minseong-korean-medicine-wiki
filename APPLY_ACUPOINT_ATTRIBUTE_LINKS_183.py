from pathlib import Path
import shutil,sys,re

p=Path("mkdocs.yml")
if not p.exists():
    print("ERROR: mkdocs.yml 없음"); sys.exit(1)

t=p.read_text(encoding="utf-8-sig")
backup=Path("_backup_mkdocs_183.yml")
shutil.copy2(p,backup)

# User decided not to expose Saam Hangyeok/Yeolgyeok.
t=t.replace("        - 사암침법 한격·열격 심화: acupuncture-specific/saam-cold-heat.md\n","")

p.write_text(t,encoding="utf-8")

cold=Path("docs/acupuncture-specific/saam-cold-heat.md")
if cold.exists():
    cold.unlink()
    print("- 사암침법 한격·열격 문서 삭제")
else:
    print("- 사암침법 한격·열격 문서 없음/이미 제거")

print("- mkdocs nav 정리 완료")
print("- 개별 경혈 특정혈 속성 문서는 ZIP 병합으로 반영")
print(f"- 백업: {backup}")
