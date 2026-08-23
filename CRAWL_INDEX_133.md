# 133 크롤링·AI 색인 구조 최종 점검

## 점검 결과

### robots.txt
현재 설정이 적절하여 **수정하지 않았습니다**.

- `User-agent: *`
- `Allow: /`
- `Sitemap: https://wiki.minseong.co.kr/sitemap.xml`

### llms.txt
기존 내용은 오래된 핵심 주제 위주여서 최근 작업을 반영해 업데이트했습니다.

추가·강화:
- 아카이브 안내
- 증상 기반 한약 탐색
- 질환별 현대 근거 카드
- 대표 본초 근거
- 최근 한약 처방 임상근거
- WHO 표준 361경혈 아틀라스
- 요통·불면·기능성소화불량 임상 지식망
- 근거 가이드·참고문헌 DB
- AI 해석 가이드

llms.txt에 수록한 내부 URL: 47개
업로드된 docs 기준 존재하지 않는 URL: **0개 — PASS**

### AI·검색엔진용 사이트 구조
`docs/ai/site-structure.md`를 최근 구조에 맞게 전면 최신화했습니다.

핵심 관계:
`자연어 질문 → 증상 → R-code → 질환 → 감별 → 변증 → 본초·방제 → 경혈·침구 → 현대근거 → PMID·DOI`

## 교체 파일
- `docs/llms.txt`
- `docs/ai/site-structure.md`

mkdocs.yml 수정 없음.

Summary:
Refresh crawl and AI index structure
