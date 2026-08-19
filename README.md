# 민성 한의학 아카이브 V2

공개 주소: https://wiki.minseong.co.kr/

## 이번 버전의 핵심
- 10개 대분류 체계 고정
- 문서별 front matter(태그·상태·검토일)
- Material for MkDocs 검색 + tags + meta
- 문서 편집/출처/상태 정책
- 본초·방제·질환·고전·연구 템플릿
- robots.txt + llms.txt + MkDocs 자동 sitemap
- GitHub Actions 자동 빌드/배포

## 적용 방법
현재 저장소에 이 패키지의 **내용물**을 덮어씁니다. `.github`, `docs`, `mkdocs.yml`, `requirements.txt`, `README.md`가 저장소 루트에 위치해야 합니다.

GitHub Desktop에서 변경 사항을 확인한 뒤:
1. Summary: `Upgrade archive structure to V2`
2. Commit to main
3. Push origin
4. Actions에서 `Deploy MkDocs to GitHub Pages` 성공 확인

## 권장 운영 흐름
1. 새 문서는 `docs/templates/`의 표준 양식으로 시작
2. 초안 → 보강중 → 검토완료 상태 관리
3. 출처를 먼저 확보한 뒤 현대 연구 문단 작성
4. 관련 본초·방제·변증·질환을 내부링크로 연결
5. 공개 URL(slug)은 가급적 변경하지 않음

## 1차 콘텐츠 목표
- 본초 100
- 방제 100
- 변증 50
- 질환·증상 100
- 고전 20
- 현대 연구 리뷰 100
