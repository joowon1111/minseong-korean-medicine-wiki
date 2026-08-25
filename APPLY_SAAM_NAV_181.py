from pathlib import Path
import shutil,sys
p=Path("mkdocs.yml")
if not p.exists(): print("ERROR: mkdocs.yml 없음"); sys.exit(1)
t=p.read_text(encoding="utf-8-sig")
line="        - 사암침법 12경맥 정격·승격: acupuncture-specific/saam-12-meridians.md\n"
if line.strip() in t: print("이미 181 적용됨"); sys.exit()
needle="        - 사암침법 기초 지식망: acupuncture-specific/saam-acupuncture.md\n"
if needle not in t: print("ERROR: 179 nav 먼저 적용 필요"); sys.exit(2)
shutil.copy2(p,"_backup_mkdocs_181.yml")
p.write_text(t.replace(needle,needle+line,1),encoding="utf-8")
print("181 nav 적용 완료")
