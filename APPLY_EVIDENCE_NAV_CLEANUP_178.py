from pathlib import Path
import shutil, re, sys
from datetime import datetime

p=Path("mkdocs.yml")
if not p.exists():
    print("ERROR: 저장소 최상위 mkdocs.yml을 찾지 못했습니다.")
    print("GitHub Desktop 저장소 최상위 폴더에서 실행하세요.")
    sys.exit(1)

text=p.read_text(encoding="utf-8-sig")
original=text

# Find the "상세 자료실:" nav section and only edit that subsection.
lines=text.splitlines()
start=None
for i,line in enumerate(lines):
    if re.match(r"^(\s*)-\s*상세 자료실\s*:\s*$",line) or re.match(r"^(\s*)상세 자료실\s*:\s*$",line):
        start=i
        break

if start is None:
    print("ERROR: mkdocs.yml에서 '상세 자료실:' 구역을 찾지 못했습니다.")
    print("파일을 자동 수정하지 않았습니다.")
    sys.exit(2)

base_indent=len(lines[start])-len(lines[start].lstrip())
end=len(lines)
for i in range(start+1,len(lines)):
    if not lines[i].strip():
        continue
    ind=len(lines[i])-len(lines[i].lstrip())
    if ind<=base_indent:
        end=i
        break

block=lines[start:end]

# 1) 연구·근거 -> 연구·근거 포털 (상세 자료실 안에서만)
for i,line in enumerate(block):
    if re.match(r"^(\s*)-\s*연구·근거\s*:",line):
        block[i]=re.sub(r"연구·근거\s*:", "연구·근거 포털:", line, count=1)

# 2) 연구·근거 임상 해석 심화 -> 임상근거 해석 심화
for i,line in enumerate(block):
    if "연구·근거 임상 해석 심화:" in line:
        block[i]=line.replace("연구·근거 임상 해석 심화:","임상근거 해석 심화:",1)

# 3) 상세 자료실의 '근거 읽는 법' 항목과 그 하위 nav만 제거.
#    문서 파일은 삭제하지 않으며 상단 '근거 수준 읽기'도 건드리지 않음.
newblock=[]
i=0
removed=False
while i<len(block):
    line=block[i]
    if re.match(r"^(\s*)-\s*근거 읽는 법\s*:\s*$",line):
        item_indent=len(line)-len(line.lstrip())
        removed=True
        i+=1
        while i<len(block):
            nxt=block[i]
            if not nxt.strip():
                i+=1
                continue
            ind=len(nxt)-len(nxt.lstrip())
            if ind<=item_indent:
                break
            i+=1
        continue
    newblock.append(line)
    i+=1

lines[start:end]=newblock
new="\n".join(lines)+"\n"

if new==original and not removed:
    print("변경할 항목이 없었습니다. 파일을 수정하지 않았습니다.")
    sys.exit(0)

backup=Path(f"_backup_mkdocs_178_{datetime.now().strftime('%Y%m%d-%H%M%S')}.yml")
shutil.copy2(p,backup)
p.write_text(new,encoding="utf-8")

print("178 연구·근거 좌측 메뉴 정리 완료")
print("- 상세 자료실: '연구·근거' → '연구·근거 포털'")
print("- 상세 자료실: '근거 읽는 법' 좌측 nav 제거 (문서 자체는 유지)")
print("- '연구·근거 임상 해석 심화' → '임상근거 해석 심화'")
print("- 출처·근거 허브 / 현대 연구 유지")
print(f"- 백업: {backup}")
