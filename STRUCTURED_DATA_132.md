# 132 구조화 데이터·AI 검색 신호 강화

## 적용
핵심 질환 9개에 Schema.org JSON-LD `MedicalWebPage` + `MedicalCondition` 구조를 추가했습니다.

적용 페이지:
- `conditions/functional-dyspepsia.md`
- `conditions/insomnia.md`
- `conditions/low-back-pain.md`
- `conditions/knee-pain.md`
- `conditions/allergic-rhinitis.md`
- `conditions/migraine.md`
- `conditions/pcos.md`
- `conditions/chronic-prostatitis.md`
- `conditions/fatigue.md`

운영 가이드:
- `docs/guide/structured-data.md`

## 포함 정보
- 페이지 name / description
- 실제 공개 URL
- ko-KR
- 상위 WebSite
- MedicalCondition 주제
- 환자 검색어 + 전문용어 keywords
- dateModified

## 검증
- 모든 JSON-LD 파싱 PASS
- 각 JSON-LD URL과 실제 문서 경로 일치 PASS
- 본문 치료효과를 새로 추가하지 않음

mkdocs.yml 수정 없음.

Summary:
Add clinical structured data
