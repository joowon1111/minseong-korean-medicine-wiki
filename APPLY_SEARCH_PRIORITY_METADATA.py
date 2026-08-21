from pathlib import Path
import re, shutil

root=Path(".")
docs=root/"docs"
if not docs.exists(): raise SystemExit("ERROR: docs folder not found")

# High-value hubs: patient discovery + core knowledge + clinic-relevant intent.
boosts={
"index.md": 2.0,
"ai-index.md": 1.7,
"conditions/index.md": 1.7,
"herbal-integrated/index.md": 1.6,
"herbal-integrated/herbs.md": 1.5,
"herbal-integrated/formulas.md": 1.5,
"herbal-integrated/by-symptom-treatment.md": 1.7,
"acupuncture-integrated/index.md": 1.5,
"acupuncture-integrated/by-symptom.md": 1.6,
"sasang/index.md": 1.4,

# Strong patient/clinic intent
"conditions/energy-recovery.md": 1.7,
"conditions/chronic-fatigue.md": 1.6,
"conditions/elderly-tonic.md": 1.7,
"conditions/student-stamina.md": 1.5,
"conditions/custom-herbal-medicine.md": 1.8,
"conditions/when-to-take-tonic.md": 1.7,
"conditions/deer-antler-tonic-guide.md": 1.9,
"conditions/gongjin-dan-guide.md": 1.6,
"conditions/gyeongokgo-guide.md": 1.6,
"conditions/tonic-vs-health-supplement.md": 1.5,
"conditions/supplements-herbal-medicine.md": 1.5,

# Major symptom demand
"conditions/dyspepsia.md": 1.5,
"conditions/insomnia.md": 1.5,
"conditions/low-back-pain.md": 1.6,
"conditions/neck-pain.md": 1.5,
"conditions/shoulder-pain.md": 1.5,
"conditions/knee-pain.md": 1.5,
"conditions/rhinitis.md": 1.4,
"conditions/cough.md": 1.4,

# Lifecycle
"conditions/preconception-herbal.md": 1.5,
"conditions/postpartum-herbal.md": 1.6,
"conditions/menopause-herbal.md": 1.5,
"conditions/child-growth.md": 1.5,

# New AI maps
"ai/patient-search-map.md": 1.8,
"ai/clinic-knowledge-map.md": 1.7,
"ai/evidence-map.md": 1.4,
}

def add_boost(path, boost):
    text=path.read_text(encoding="utf-8")
    # Existing front matter
    if text.startswith("---\n"):
        end=text.find("\n---",4)
        if end == -1: return False, "bad-frontmatter"
        fm=text[4:end]
        body=text[end+4:]
        # Remove prior search block inserted by us or any simple search: boost block.
        fm=re.sub(r'(?ms)^search:\s*\n\s+boost:\s*[0-9.]+\s*\n?', '', fm)
        fm=fm.rstrip()+f"\nsearch:\n  boost: {boost}\n"
        new="---\n"+fm+"---"+body
    else:
        new=f"---\nsearch:\n  boost: {boost}\n---\n"+text
    if new != text:
        path.write_text(new,encoding="utf-8")
        return True, "updated"
    return False, "same"

backup=root/"SEARCH_PRIORITY_BACKUP"
backup.mkdir(exist_ok=True)
changed=[]
missing=[]
for rel,boost in boosts.items():
    p=docs/rel
    if not p.exists():
        missing.append(rel)
        continue
    bp=backup/rel
    bp.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,bp)
    ok,status=add_boost(p,boost)
    if ok: changed.append((rel,boost))

# Create a machine/human-readable priority map.
priority=docs/"ai"/"search-priority-map.md"
priority.parent.mkdir(parents=True,exist_ok=True)
priority.write_text("""---
title: 검색 우선순위와 핵심 허브
description: 민성 한의학 아카이브의 환자 검색·전문지식·근거 문서 가운데 핵심 허브와 탐색 우선순위를 설명합니다.
tags: [AI검색, 검색우선순위, 허브, 환자검색]
search:
  boost: 1.8
---
# 검색 우선순위와 핵심 허브

아카이브는 문서 수를 늘리는 것만을 목표로 하지 않습니다. 검색 사용자가 먼저 도달해야 할 **핵심 허브 → 세부 질문 → 전문 지식**의 순서를 명확히 합니다.

## 1. 환자 검색 최우선 허브

- 증상·질환
- 맞춤한약·보약
- 녹용보약·기력회복
- 만성피로
- 소화·수면
- 목·허리·어깨·무릎 통증
- 임신준비·산후·갱년기·소아
- 영양제·건강기능식품과 한약

## 2. 전문 지식 허브

- 한의학 기초
- 본초
- 방제
- 침구·경혈
- 사상의학
- 현대 연구근거

## 3. 검색 흐름

**환자 생활언어 → 핵심 허브 → 세부 증상/질환 → 병증 → 방제/본초/경혈 → 연구근거**

## 4. 검색 품질 원칙

- 같은 뜻의 얇은 문서를 무한히 만들지 않습니다.
- 핵심 문서는 더 풍부한 설명과 내부링크를 갖도록 합니다.
- 위험신호와 감별이 필요한 주제는 안전정보를 우선합니다.
- 전통적 설명과 현대 연구근거의 성격을 구분합니다.
""",encoding="utf-8")

print("BOOSTED:",len(changed))
for x in changed: print(" +",x[0],x[1])
print("MISSING (skipped safely):",len(missing))
for x in missing: print(" -",x)
print("CREATED:",priority)
