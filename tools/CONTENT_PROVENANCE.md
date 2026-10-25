# 출처·내용 지문과 외부 유사 문서 점검

`content_provenance.py`는 `page_discovery.py` 다음에 실행하는 MkDocs hook이다.
방문자 추적·복제자 신원 확인·접근 차단·숨겨진 문구 삽입을 하지 않는다.

## 배포 결과

- 본문 하단: 문서명·고정 원문 URL, 문서 ID, 본문 SHA-256, 복사 출처 안내.
- 본문 80자 이상 일반 복사: 원문 URL·문서 ID·지문 앞 12자리 추가. 입력란·짧은 선택·코드 복사는 유지.
- `assets/provenance/manifest.json`: 전체 문서의 ID·원문 URL·소스와 본문 지문·빌드 기준 Git 커밋 및 공개 검색용 문장 일부.
- `assets/provenance/search-index.json`과 `search-batches/NNN.json`: 예약 검색용 핵심 문서와 24개 단위의 작은 표본 묶음. ISO 주 번호를 묶음 수로 나눈 나머지로 조사 묶음을 고르고 그 안의 문서·문구를 교대로 확인한다.
- `assets/ai/pages/**/index.json`: 원래 공개 본문에 출처 정보를 함께 내보낸다. 해시는 머리말·탐색·출처 UI를 제외한 기존 Article.body_text를 NFC 정규화하고 공백을 합쳐 UTF-8 SHA-256으로 계산한다.
- 8개 명시적 자체 제작 SVG 폴더: 배포본에 도메인 워터마크와 출처 메타데이터를 삽입한다. 원본 파일·기존 저작자 표시·경혈 ID·viewBox를 유지한다. 외부 이미지와 3D 모형은 대상이 아니다. 새 폴더는 제작·출처를 확인한 후 allowlist에 추가한다.

문서 ID는 원문 URL에서 결정되며 방문자마다 바뀌지 않는다. 본문 변경은 내용 지문을 바꾼다.
지문만으로 저작권 귀속이나 독립적으로 인증된 최초 작성 시각을 입증하지 못한다.
Git 커밋 이력과 공개 버전은 원문 변경 순서와 대조를 위한 참고자료다. GitHub Pages의 이전 빌드에서 생성한 manifest도 해당 gh-pages Git 커밋에서 확인할 수 있다.

## 점검

빌드 후 `python tools/audit_content_provenance.py`로 전 문서·도표를 확인한다.
`tools/check_content_provenance.cjs`는 실제 복사와 모바일·데스크톱 표시를 검증한다.
두 파일의 문장 겹침은 `python tools/compare_content_reuse.py original.json candidate.txt`로 로컬 비교할 수 있다.
첫 입력은 공개 본문 JSON 또는 UTF-8 텍스트, 둘째 입력은 직접 확인·저장한 후보 본문이다.
이 도구는 외부 전송을 하지 않는다. 문장 변형은 놓칠 수 있으며 수치는 침해 판정이 아니다.

## 외부 검색 운영

ChatGPT의 예약 점검은 공개 검색을 이용한 주간 표본 조사다. GitHub Actions가 유료 검색 API나 비밀키 없이 인터넷 전체를 상시 검사하는 구조가 아니다.
manifest의 `search_samples`에서 최근 수정·핵심 페이지와 이전 조사에서 다루지 않은 문서를 교대로 고른다.
일반 의학 사실·고전 원문보다 자체 설명·비교표의 독특한 문구를 우선 검색한다.
검색 결과는 원문을 열어 확인하고 원문 URL·Git 이력·후보 URL·실제 일치 구절과 구조·출처 표시를 대조한다.
명시적 인용·공통 원자료·본인 사이트·공식 미러를 제외하고, 의심 사례만 보고한다.
접근 실패·검색 결과 없음은 무단 전재가 없다는 증명이 아니다. 경고 전송·신고·삭제 요청은 자동으로 하지 않는다.
