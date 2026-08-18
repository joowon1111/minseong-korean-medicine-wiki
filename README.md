# 민성 한의학 아카이브

## 로컬 실행
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```
브라우저에서 http://127.0.0.1:8000 확인.

## GitHub Pages 배포
1. 새 GitHub 저장소를 만들고 이 폴더 전체를 업로드합니다.
2. 기본 브랜치를 `main`으로 둡니다.
3. Actions가 실행되면 `gh-pages` 브랜치가 생성됩니다.
4. Repository Settings → Pages → Deploy from a branch → `gh-pages` / root 선택.
5. Custom domain에 `wiki.minseong.co.kr` 입력 후 HTTPS를 활성화합니다.
6. 도메인 DNS에서 `wiki` CNAME을 GitHub Pages 주소(`사용자명.github.io`)로 연결합니다.

## 문서 추가
`docs/` 아래에 Markdown 파일을 만들고 `mkdocs.yml`의 `nav:`에 추가합니다.

## 권장 문서 원칙
전통 문헌, 현대 연구, 임상적 해설을 명확히 구분하고 DOI/PMID 및 원전 출전을 가능한 범위에서 기록합니다.
