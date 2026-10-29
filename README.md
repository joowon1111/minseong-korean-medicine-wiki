# 민성 한의학 아카이브

공개 주소: https://wiki.minseong.co.kr/

## 현재 원본과 실행 경로

| 경로 | 역할 |
|---|---|
| `docs/` | 현재 공개 문서·정적 자산·기존 URL의 원본 |
| `mkdocs.yml` | 메뉴·플러그인·빌드 훅·리다이렉트 설정 |
| `data/` | 학술·경혈·학습 기능의 원본 데이터 |
| `tools/` | 생성기·검증기·MkDocs 훅·테스트 |
| `overrides/` | 사이트 템플릿 |
| `services/archive-ai/` | AI 서버 소스와 배포 설정 |
| `.github/workflows/` | 실제 검증·배포·Evidence Radar 실행 경로 |

문서를 찾거나 수정할 때는 `docs/`에서 시작합니다. 저장소 전체에서 같은 파일명을 찾아 첫 결과를 수정하지 않습니다. `_backup*`, `*_BACKUP*`, `_AUDIT_UPLOAD_SOURCE`의 남은 파일은 내용 차이가 있어 보존한 과거 자료이며 현재 페이지가 아닙니다. `_payload`와 다른 payload 폴더는 설치 스크립트의 입력일 수 있습니다. 특히 `_payload/extra_pages`는 현재 경혈 검증기에서도 검사합니다.

## 로컬 검증

먼저 `AGENTS.md`를 읽고 `python -m pip install -r requirements.txt`로 의존성을 설치합니다. 배포 순서에 맞춘 검증은 다음과 같습니다.

```sh
python tools/build_acupoint_supplements.py --check
python tools/build_korean_search_index.py
python tools/check_secrets.py
python tools/build_ai_knowledge_layer.py
python tools/audit_internal_links.py
python -m unittest discover -s tools -p 'test_*.py'
node --test tools/test_*.cjs
python tools/build_archive_tools.py
python tools/build_archive_ai_config.py
python -m mkdocs build
python tools/audit_internal_links.py --site
python tools/audit_page_discovery.py
python tools/audit_content_provenance.py
python tools/audit_seo.py
```

Node.js 22와 Python 3.12를 기준으로 GitHub Actions가 검증합니다. 브라우저 반응형·검색·출처 표시 검사와 AI 서버 번들 검증은 `.github/workflows/validate.yml`을 따릅니다. `main` 병합 후 `.github/workflows/deploy.yml`이 GitHub Pages를 배포합니다.

## 변경과 복구

현재 문서에 내용을 통합하고 기존 URL·앵커·내부 링크·학술 출처를 유지합니다. 원문·처방 이본·원본 데이터는 이름이 같다는 이유로 병합하지 않습니다. 과거 APPLY/INSTALL 스크립트를 실행하면 오래된 내용으로 덮어쓸 수 있으므로 현재 편집·배포 절차를 우선합니다.

새 백업 복제본을 커밋하는 대신 Git 브랜치·커밋·PR을 사용합니다. 정리 전 파일은 [2026-10-29 정리 기록](reports/repository-cleanup-2026-10-29/README.md)의 기준 커밋과 파일별 blob SHA로 추적할 수 있습니다. 보안 검사는 스테이징 후 커밋·푸시 전에 반드시 다시 실행합니다.
