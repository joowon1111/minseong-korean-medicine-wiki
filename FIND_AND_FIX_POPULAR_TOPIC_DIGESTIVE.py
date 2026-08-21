from pathlib import Path
import re

ROOT=Path(".")
TEXT_EXT={".md",".html",".htm",".yml",".yaml",".css",".js",".json",".py"}
matches=[]

for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
        continue
    # skip git/build/cache directories
    parts=set(p.parts)
    if ".git" in parts or "site" in parts or "__pycache__" in parts:
        continue
    try:
        t=p.read_text(encoding="utf-8")
    except Exception:
        continue
    if "많이 찾는 주제" in t or "비염" in t:
        # prioritize files that contain both
        score=(2 if "많이 찾는 주제" in t else 0)+(1 if "비염" in t else 0)
        matches.append((score,p,t))

matches.sort(key=lambda x:(-x[0],str(x[1])))

report=["# 많이 찾는 주제 위치 검색 결과",""]
for score,p,t in matches:
    if "많이 찾는 주제" in t or score>=3:
        idx=t.find("많이 찾는 주제")
        if idx<0: idx=t.find("비염")
        snippet=t[max(0,idx-500):min(len(t),idx+1800)]
        report.append(f"## {p}")
        report.append("```")
        report.append(snippet)
        report.append("```")
        report.append("")

Path("POPULAR_TOPIC_LOCATION_REPORT.md").write_text("\n".join(report),encoding="utf-8")

# Find the actual home rendering source: require both phrase and '비염' in a local window.
target=None
for score,p,t in matches:
    if "많이 찾는 주제" not in t:
        continue
    idx=t.find("많이 찾는 주제")
    window=t[idx:idx+3500]
    if "비염" in window:
        target=(p,t,idx,window)
        break

if not target:
    print("ERROR: '많이 찾는 주제'와 '비염'이 함께 있는 원본 파일을 찾지 못했습니다.")
    print("POPULAR_TOPIC_LOCATION_REPORT.md를 확인하세요.")
    raise SystemExit(1)

p,t,idx,window=target
orig=t
w=window
changed=False

# Replace visible label + target for Markdown, HTML, or raw data object patterns.
# 1) markdown [비염](...)
m=re.search(r'\[비염\]\(([^)]+)\)',w)
if m:
    w=w[:m.start()]+f"[소화](symptom-integrated/digestive.md)"+w[m.end():]
    changed=True

# 2) html <a ...>비염</a>
if not changed:
    m=re.search(r'(<a\b[^>]*href=["\'])([^"\']*)(["\'][^>]*>\s*)비염(\s*</a>)',w,re.I)
    if m:
        repl=m.group(1)+"/symptom-integrated/digestive/"+m.group(3)+"소화"+m.group(4)
        w=w[:m.start()]+repl+w[m.end():]
        changed=True

# 3) common JS/HTML data object: label/title/text + url/href
if not changed:
    # Replace first isolated label within this exact section and then first nearby rhinitis path.
    m=re.search(r'(?<![가-힣])비염(?![가-힣])',w)
    if m:
        w=w[:m.start()]+"소화"+w[m.end():]
        # try replacing a nearby rhinitis link
        w=re.sub(r'(?:(?:\.\./)?conditions/rhinitis\.md|/conditions/rhinitis/?|conditions/rhinitis/?|(?:\.\./)?symptom-integrated/respiratory-rhinitis\.md)',
                 'symptom-integrated/digestive.md',w,count=1)
        changed=True

if not changed:
    print("ERROR: 원본 파일은 찾았지만 비염 버튼 형태를 안전하게 교체하지 못했습니다.")
    print("대상:",p)
    raise SystemExit(1)

backup=p.with_suffix(p.suffix+".before-digestive-topic-fix.bak")
backup.write_text(orig,encoding="utf-8")
new=orig[:idx]+w+orig[idx+len(window):]
p.write_text(new,encoding="utf-8")

print("FIXED FILE:",p)
print("BACKUP:",backup)
print("변경: 많이 찾는 주제 '비염' → '소화'")
print("POPULAR_TOPIC_LOCATION_REPORT.md도 생성했습니다.")
