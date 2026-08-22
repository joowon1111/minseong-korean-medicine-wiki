# 민성 한의학 아카이브 전체 품질감사 — 실제 저장소 분석

## 핵심 수치
- Markdown 문서: **1392**
- answer-guides: **111**
- 깨진 내부 Markdown 링크: **70**
- mkdocs nav 미등록 문서: **444**
- 고아 페이지 후보: **325**
- front matter 없는 문서: **629**
- H1 없는 문서: **8**
- 얇은 문서 후보: **429**
- `## 핵심 답변`이 없는 answer-guide: **3**
- 중복 title 그룹: **2**

## 가장 먼저 고칠 문제
깨진 링크 70건 중 **66건이 answer-guides**에서 발생합니다. 대부분 최근 질문형 가이드가 과거에 존재한다고 가정한 conditions 경로를 가리킨 문제입니다.

주요 잘못된 대상:
- conditions/autonomic-dysfunction.md: 24건
- conditions/leg-numbness.md: 9건
- conditions/pediatric-tonic.md: 6건
- conditions/womens-lifecycle.md: 6건
- conditions/anorexia.md: 6건
- conditions/globus-sensation.md: 5건
- conditions/hand-numbness.md: 4건
- conditions/prostate-urinary.md: 3건

## nav / 고아 페이지 해석
nav 미등록 444건을 전부 nav에 넣는 것은 권장하지 않습니다. 특히 conditions 255건, answer-guides 111건이어서 상단 메뉴가 과도하게 커집니다.
대신 **index/허브/ai-index에서 내부링크를 받게 하는 방식**이 적절합니다.

고아 후보 325건 중:
- conditions: 204
- answer-guides: 76
- herbal-integrated: 11
- sasang: 10
- symptom-integrated: 10

따라서 2차 작업은 nav 대량등록이 아니라 **conditions/index + answer-guides/index + 주요 pillar 허브에서 문서군을 묶어 링크**하는 방식이 좋습니다.

## front matter 629건
초기 문서가 대량으로 front matter 없이 만들어진 흔적입니다. 이것을 한 번에 자동 생성하면 title/description 품질이 낮아질 수 있으므로 이번 안전패치에서는 건드리지 않습니다.
다음 단계에서 **환자 검색 가치가 높은 conditions / formulas / herbs부터 우선순위로 보강**하는 것이 좋습니다.

## answer-guide 핵심답변 누락 3건
- regional-dialect-query-variants.md
- colloquial-symptom-synonyms.md
- dialect-content-policy.md

이 세 문서는 일반 환자 질문 페이지가 아니라 사투리/생활구어 보조 문서이므로 구조상 오류라기보다 예외 문서입니다. 사용자가 사투리 영역을 핵심색인에서 제외하기로 했으므로 당장 수정할 필요는 없습니다.

## 중복 title
`근거·참고문헌`이라는 제목이 여러 사상/보익 reference 문서에서 반복됩니다. 문서 성격상 허용 가능하지만 SEO title 차별화를 위해 나중에 '공진단 근거·참고문헌' 식으로 구체화하는 것이 좋습니다.

`동의보감 탕액편`은 network와 classics 쪽에 중복 title이 있어 역할 차별화가 필요합니다.

## 이번 안전 수정 패치
이번 ZIP은 **확실하게 존재하지 않는 경로만 실제 존재하는 관련 문서로 교체**합니다.
대규모 nav 변경, front matter 자동생성, 문서 삭제/병합은 하지 않습니다.

다음 단계 권장:
1. 깨진 링크 안전수정
2. answer-guides 76개 고아 후보를 answer-guides/index와 핵심 허브에 연결
3. conditions 204개 고아 후보를 증상별 허브로 연결
4. 중요 문서부터 front matter 보강
5. 마지막으로 질문 유사도/카니벌라이제이션 정밀감사
