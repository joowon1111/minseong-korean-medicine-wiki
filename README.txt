37단계 — 중복 레이어 통합 + 감사 정확도 개선

Audit 30 상위권에 다시 나타난 acupoint-network/gv20.md 등은
33에서 만든 acupuncture/points 상세 문서와 같은 주제의 초창기 중복 URL입니다.
기경팔맥도 acupuncture/extraordinary/*와 meridian-network/*가 중복되어 있습니다.

이번 단계:
- 핵심 경혈 중복 URL 8개를 canonical 상세문서 연결페이지로 정리
- 기경팔맥 중복 URL 8개를 32단계 상세문서 연결페이지로 정리
- URL은 삭제하지 않아 기존 링크/색인을 보존
- templates/references/bridge를 일반 임상문서와 동일하게 점수매기지 않는 감사 기준 추가
- guide/status-policy.md 현대화

실행:
1. APPLY_DUPLICATE_LAYER_CONSOLIDATION_37.bat
2. Commit / Push
선택:
3. RUN_DUPLICATE_AWARE_AUDIT_37.bat

Summary:
Consolidate duplicate legacy knowledge layers into canonical clinical pages
