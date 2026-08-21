from pathlib import Path
import re, shutil, sys

candidates = [
    Path("docs/index.md"),
    Path("docs/home.md"),
    Path("docs/portal/index.md"),
]

target = next((p for p in candidates if p.exists()), None)
if not target:
    raise SystemExit("ERROR: 홈 문서(docs/index.md 등)를 찾지 못했습니다.")

orig = target.read_text(encoding="utf-8")
text = orig

# Work only near the "많이 찾는 주제" section to avoid replacing other rhinitis references.
m = re.search(r"(많이\s*찾는\s*주제)", text)
if not m:
    raise SystemExit("ERROR: '많이 찾는 주제' 섹션을 찾지 못했습니다. 파일은 변경하지 않았습니다.")

start = m.start()
end = min(len(text), start + 3000)
section = text[start:end]
before = section

# Common Markdown link forms
patterns = [
    (r"\[비염\]\((?:\.\./)?conditions/rhinitis\.md\)", "[소화](symptom-integrated/digestive.md)"),
    (r"\[비염\]\((?:\.\./)?conditions/rhinitis/\)", "[소화](symptom-integrated/digestive.md)"),
    (r"\[비염\]\((?:\.\./)?symptom-integrated/respiratory-rhinitis\.md\)", "[소화](symptom-integrated/digestive.md)"),
]

for pat, repl in patterns:
    section, n = re.subn(pat, repl, section, count=1)
    if n:
        break
else:
    # HTML button/anchor variants: replace only the first anchor containing exact visible text 비염.
    html_pat = re.compile(
        r'(<a\b[^>]*href=["\'])([^"\']*)(["\'][^>]*>\s*)비염(\s*</a>)',
        re.I
    )
    section, n = html_pat.subn(
        lambda mm: mm.group(1) + "/symptom-integrated/digestive/" + mm.group(3) + "소화" + mm.group(4),
        section,
        count=1
    )

    if not n:
        # Last safe fallback: replace an isolated "비염" token within the section only,
        # but only if "소화" is not already present in the same topic row.
        if re.search(r"(?<![가-힣])비염(?![가-힣])", section) and "소화" not in section[:1200]:
            section = re.sub(r"(?<![가-힣])비염(?![가-힣])", "소화", section, count=1)
            n = 1
        else:
            raise SystemExit("ERROR: '비염' 버튼 형태를 안전하게 특정하지 못했습니다. 파일은 변경하지 않았습니다.")

# If the fallback changed only text and did not change a link target, try to update nearby rhinitis URL.
section = re.sub(
    r'(["\'])(?:/)?conditions/rhinitis/?\1',
    r'\1/symptom-integrated/digestive/\1',
    section,
    count=1
)

if section == before:
    raise SystemExit("ERROR: 변경 사항이 없습니다.")

backup = target.with_suffix(target.suffix + ".before-popular-topic-digestive.bak")
backup.write_text(orig, encoding="utf-8")
text = text[:start] + section + text[end:]
target.write_text(text, encoding="utf-8")

print("OK:", target)
print("변경: 많이 찾는 주제 '비염' → '소화'")
print("링크: /symptom-integrated/digestive/")
print("나머지 많이 찾는 주제는 변경하지 않았습니다.")
