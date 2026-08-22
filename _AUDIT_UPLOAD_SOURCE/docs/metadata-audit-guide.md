---
title: 문서 메타데이터 점검표
description: 새 문서를 추가할 때 title·description·tags·status·last_reviewed를 빠짐없이 확인하는 점검표입니다.
tags: [운영, 메타데이터, 품질관리]
status: 검토완료
last_reviewed: 2026-08-19
---

# 문서 메타데이터 점검표

새 문서를 추가하거나 기존 문서를 크게 수정할 때 다음 항목을 확인한다.

- [ ] `title`이 문서 주제와 정확히 일치하는가?
- [ ] `description`이 한 문장으로 문서 내용을 설명하는가?
- [ ] `tags`가 2~5개 정도의 핵심 분류를 담는가?
- [ ] `status`가 기록되어 있는가?
- [ ] `last_reviewed` 날짜가 있는가?
- [ ] H1 제목이 front matter의 title과 의미상 일치하는가?
- [ ] 첫 문단에서 주제를 직접 정의하는가?
- [ ] 관련 본초·방제·질환·고전·연구 문서로 내부링크가 있는가?
- [ ] 현대 연구를 언급했다면 PMID/DOI를 가능한 범위에서 기록했는가?
- [ ] 같은 주제를 설명하는 중복 canonical 페이지가 생기지 않았는가?

## 권장 front matter

```yaml
---
title: 문서 제목
description: 문서가 무엇을 설명하는지 한 문장으로 정리합니다.
tags: [핵심태그1, 핵심태그2]
status: 검토완료
last_reviewed: 2026-08-19
---
```

이 표준은 콘텐츠 양이 커져도 검색·AI·사람 모두가 일관되게 문서를 이해하도록 하기 위한 운영 기준이다.

<!-- MINSEONG_ONE_SHOT_FIX_V2 -->
## 관련 핵심 문서

- [아카이브 안내](guide/index.md)
- [증상·질환](conditions/index.md)
- [AI 검색 구조](ai-index.md)

