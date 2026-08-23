# 134 전체 품질점검·중복·메타데이터 감사

## 검사 범위
사용자가 업로드한 `docs.zip` 전체 Markdown 문서를 검사했습니다.

- Markdown 문서: **2087개**
- 우선순위 핵심 문서의 안전한 메타데이터 보완: **8개**
- `.md.md` 형태 중복 파일: **0개**
- 제목 중복 그룹: **42개**
- 전체 내부링크 중 현재 업로드본 기준 미해결 후보: **76개**

## 이번에 자동 수정한 것
핵심 영역(`conditions`, `authority/conditions`, `authority/formulas`, `authority/herbs`) 중
이미 YAML title이 존재하지만 description 또는 last_reviewed가 빠진 문서만 안전하게 보완했습니다.

본문, 임상근거, 링크 목적지는 자동으로 추측해 수정하지 않았습니다.

## 중요
이번 감사는 사용자가 업로드한 `docs.zip` 시점의 스냅샷을 기준으로 합니다.
130~133 단계에서 이후 수정된 파일은 이 ZIP에 아직 포함되지 않을 수 있으므로,
여기서 검출된 링크 후보를 다시 일괄 수정하면 이미 고친 내용을 되돌릴 위험이 있습니다.

따라서 134에서는 **확실한 메타데이터 누락만 패치**하고,
불확실한 링크·중복은 보고서에 남겨 다음 최신 docs.zip 재수집 시 재검사하도록 했습니다.

## 미해결 링크 상위 패턴
- `../../acupoint-network/extra-points.md` — 55건
- `../clinical-core/pathways/dyspepsia.md` — 3건
- `../clinical-core/pathways/knee-leg-pain.md` — 2건
- `../../clinical-core/pathways/fatigue-recovery.md` — 2건
- `../clinical-core/pathways/rhinitis-cough.md` — 1건
- `../clinical-core/pathways/fatigue-recovery.md` — 1건
- `../about/` — 1건
- `jingui-yaolue.md` — 1건
- `../clinical-core/pathways/insomnia.md` — 1건
- `../clinical-core/pathways/low-back-pain.md` — 1건
- `../formulas/shaoyao-gancao-tang.md` — 1건
- `/portal/` — 1건
- `../../clinical-core/pathways/low-back-pain.md` — 1건
- `../../clinical-core/pathways/dyspepsia.md` — 1건
- `../research/references.md` — 1건
- `../../herbs/ligusticum.md` — 1건
- `../../clinical-core/pathways/insomnia.md` — 1건
- `../../clinical-core/pathways/women-cold-blood.md` — 1건

## 중복 제목
중복 제목은 반드시 오류를 의미하지 않습니다. 질환 본문·authority 근거카드·질문형 문서가
같은 제목을 사용할 수 있으므로 자동 삭제하지 않았습니다.

## 권장 결론
현재는 대규모 자동수정보다 **안정화 단계**가 적절합니다.
130~133 반영 후 새 `docs.zip`을 다시 만들었을 때 링크 감사를 한 번 더 수행하면
실제 남은 오류만 정확하게 분리할 수 있습니다.

Summary:
Audit metadata and content quality
