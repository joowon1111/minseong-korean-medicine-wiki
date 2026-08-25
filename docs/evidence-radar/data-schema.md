# 민성 Evidence Record 데이터 스키마

```yaml
evidence_id:
title:
published_date:
journal:
pmid:
doi:
source:
  provider:
  source_type:
classification:
  korean_medicine:
  human_study:
  study_type:
  systematic_review:
  kcd_candidates: []
  condition_tags: []
  treatment_tags: []
pico:
  population:
  intervention:
  comparator:
  outcomes: []
clinical:
  sample_size:
  treatment_duration:
  followup:
  main_result:
  clinical_meaning:
  safety:
archive_links:
  conditions: []
  formulas: []
  herbs: []
  acupoints: []
  acupuncture: []
  sasang: []
  ultrasound: []
review:
  auto_generated: true
  human_reviewed: false
  reviewed_date:
```

`kcd_candidates`는 자동분류 단계에서는 후보값입니다.

`clinical_meaning`은 논문의 결론을 반복하는 칸이 아니라 **민성 아카이브의 어느 임상 질문에 답하는 연구인지**를 기록합니다.

`archive_links`를 통해 논문을 단순 저장하지 않고 기존 지식망에 연결합니다.
