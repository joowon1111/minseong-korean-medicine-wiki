# 한의학 지식망 정리·심화 — 2026-10-24

기준 커밋: `f425d17f952a92abf30fd7498355386ded8f1d98`

범위는 `docs/network/*.md` 44개 전체와 메뉴에 함께 있는 예방·기능회복 연구 지도, 질환 확장 지도의 직접 연결 질환 10개다. 전체 사이트 2천여 문서의 전수 보강으로 표현하지 않는다.

판단: 18개 통합, 12개 본문 심화, 14개 유지. 짧다는 이유만으로 통합하지 않고 검색 의도·고유 설명·중복을 확인했다. 처방의 동명 이본은 병합하지 않는다.

## 우선순위

| 순위 | 현재 경로 | 확인한 결손 | 유지·심화·통합 선택 | 구체 작업 | 영향도 | 작업량 | 완료 기준 |
|---|---|---|---|---|---|---|---|
| 1 | `network/*-formulas.md` 7개 | 역탐색 표와 반복, 링크목록 위주 | 통합 | 고유 구성 연결을 본초→방제 표에 흡수 | 높음 | 중간 | 7개 주소·절 이동, 내부 유입 갱신 |
| 2 | 처방 소개·구성 8개 | 대표 처방·비교·구성 허브와 중복 | 통합 | 원료·가공·이본 설명을 대표 경로로 연결 | 높음 | 큼 | 원문·품질·본초 링크 보존 |
| 3 | 피로·임상·분류 지도 3개 | 회복·통합치료·분류 기준과 중복 | 통합 | 대표 지도와 분류 안내로 연결 | 높음 | 중간 | 과거 URL·앵커 의미 유지 |
| 4 | 남길 핵심 지도 12개 | 배합 이유·감별·경과 설명 부족 | 심화 | 분야별 질문·치료 이유·연구·기능 회복 연결 | 높음 | 큼 | 기존 제목 앵커와 메뉴 탐색 검증 |
| 5 | 나머지 14개 | 독립 목적·충분한 비교·근거가 이미 있음 | 유지 | 필요한 유입 링크만 갱신 | 중간 | 작음 | 내용 중복·빈 절·깨진 링크 없음 |

## 44개 처리 상태

| 기존 경로 | 처리 | 대표 경로·판단 |
|---|---|---|
| `network/acupoint-combinations.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/acupuncture-clinical-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/angelica-formulas.md` | 통합 | `network/herb-to-formula-map.md#_4` |
| `network/astragalus-formulas.md` | 통합 | `network/herb-to-formula-map.md#_3` |
| `network/atractylodes-formulas.md` | 통합 | `network/herb-to-formula-map.md#atractylodes-poria` |
| `network/classic-to-evidence-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/clinical-map.md` | 통합 | `network/condition-to-treatment-map.md#_1` |
| `network/condition-expansion-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/condition-to-treatment-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/dyspepsia-acupoints.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/dyspepsia-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/fatigue-acupoints.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/fatigue-map.md` | 통합 | `network/recovery-map.md#_1` |
| `network/formula-acupoint-combinations.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/formula-composition-hub.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/formula-family-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/formula-to-condition-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/ginseng-formulas.md` | 통합 | `network/herb-to-formula-map.md#_2` |
| `network/gongjin-composition.md` | 통합 | `network/formula-composition-hub.md#gongjin` |
| `network/gongjin-dan-map.md` | 통합 | `formulas/gongjin-dan.md#source-dose-original` |
| `network/gongjin-vs-gyeongok.md` | 통합 | `compare/gongjin-vs-gyeongok.md#composition` |
| `network/gyeongok-composition.md` | 통합 | `network/formula-composition-hub.md#gyeongok` |
| `network/gyeongok-go-map.md` | 통합 | `formulas/gyeongok-go.md#source-dose-original` |
| `network/herb-pair-combinations.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/herb-to-formula-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/index.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/insomnia-acupoints.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/insomnia-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/integrated-knowledge-graph.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/licorice-formulas.md` | 통합 | `network/herb-to-formula-map.md#licorice` |
| `network/low-back-pain-acupoints.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/low-back-pain-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/navigation-guide.md` | 통합 | `guide/taxonomy.md#herb-formula-navigation` |
| `network/physician-classic-formula-lineage.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/pinellia-formulas.md` | 통합 | `network/herb-to-formula-map.md#_6` |
| `network/poria-formulas.md` | 통합 | `network/herb-to-formula-map.md#atractylodes-poria` |
| `network/recovery-map.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/shanghan-taiyang-map.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/shengmai-composition.md` | 통합 | `network/formula-composition-hub.md#shengmai` |
| `network/shipjeondaebo-composition.md` | 통합 | `network/formula-composition-hub.md#shipjeondaebo` |
| `network/tonic-formula-compare.md` | 유지 | 독립 목적과 기존 상세 설명·근거를 유지; 필요한 링크만 갱신 |
| `network/tonic-formula-lineage.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/tonic-wellness-hub.md` | 심화 | 감별·배합 이유·원문·제형 또는 기능 재평가를 본문에 통합 |
| `network/wuling-composition.md` | 통합 | `network/formula-composition-hub.md#wuling` |

## 질환 직접 연결 10개와 추가 메뉴

| 경로 | 판단 |
|---|---|
| `conditions/neck-pain.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/shoulder-pain.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/knee-pain.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/low-back-pain.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/headache.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/dizziness.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/rhinitis.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/cough.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/menopause.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `conditions/postpartum-recovery.md` | 기존 감별·변증·치료·생활·근거 설명 유지. 확장 지도에서 목적별 직접 연결 |
| `research/prevention-function.md` | 연구 질문·대상·결과 비교가 충실하여 유지 |

## 검증

- 전체 내부 유입 링크 39개를 28개 문서에서 대표 경로로 갱신했다.
- 과거 18개 URL은 기본 목적지와 기존 제목 앵커별 이동을 제공한다. 고정 목적지에 과거 해시를 중복 부착하는 기본 리다이렉트 동작을 해당 18개에 한해 교정한다.
- Python 184개·Node 109개 테스트 통과. 기존 주소의 실제 JavaScript 실행·알려진/알 수 없는/깨진 해시와 중복 해시, 공개 본문 제외 동작을 검증했다.
- 최종 MkDocs 빌드 통과. 전체 소스·생성 사이트 누락 링크·앵커, URL 충돌·중복 제목·본문 0.
- 2,239개 공개 문서·20,680개 제목 앵커의 discovery 및 SEO 검사 통과. 설명 누락·중복 0.
- 유지한 26개 문서의 기존 제목 ID 240개와 18개 리다이렉트·모든 과거 절 목적지를 생성 HTML에서 대조했다. 통합 전 URL이 검색 색인에 남지 않음을 확인했다.
- PR CI에서 18개 옛 주소의 기본 이동·기존 절 이동 36건과 320/1440px 메뉴·가로 넘침을 브라우저로 확인하도록 추가했다.
