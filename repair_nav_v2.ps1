$ErrorActionPreference = "Stop"
Write-Host "=== Minseong NAV restore + safe repair V2 ===" -ForegroundColor Cyan

$repo = Get-Location
$mkdocs = Join-Path $repo "mkdocs.yml"
$backup = Join-Path $repo "mkdocs.yml.before-sasang-nav-repair"

if (-not (Test-Path $mkdocs)) { throw "mkdocs.yml이 있는 저장소 최상위에서 실행하세요." }
if (-not (Test-Path $backup)) { throw "mkdocs.yml.before-sasang-nav-repair 백업을 찾지 못했습니다." }

# 1) Restore known-good YAML first.
Copy-Item $backup $mkdocs -Force
Write-Host "1/3 정상 백업 복구 완료" -ForegroundColor Green

# 2) Use Python + PyYAML to parse and modify YAML structurally.
$py = @'
from pathlib import Path
import yaml, sys

p=Path("mkdocs.yml")
cfg=yaml.safe_load(p.read_text(encoding="utf-8-sig"))
if not isinstance(cfg, dict) or not isinstance(cfg.get("nav"), list):
    raise SystemExit("nav 구조를 읽을 수 없습니다.")

library = Path("docs/sasang-formula-library")
if not library.exists():
    raise SystemExit("docs/sasang-formula-library 폴더가 없습니다.")

items=[]
for f in sorted(library.glob("*.md")):
    text=f.read_text(encoding="utf-8-sig")
    title=None
    try:
        if text.startswith("---"):
            parts=text.split("---",2)
            if len(parts)>=3:
                fm=yaml.safe_load(parts[1]) or {}
                title=fm.get("title")
    except Exception:
        pass
    if not title:
        for line in text.splitlines():
            if line.startswith("# "):
                title=line[2:].strip()
                break
    if not title:
        title=f.stem
    items.append({str(title): f"sasang-formula-library/{f.name}"})

sasang=None
for node in cfg["nav"]:
    if isinstance(node,dict) and "사상의학" in node:
        sasang=node["사상의학"]
        break
if not isinstance(sasang,list):
    raise SystemExit("'사상의학' nav 목록을 찾지 못했습니다.")

# idempotent: remove old generated section then append valid mapping.
sasang[:] = [x for x in sasang if not (isinstance(x,dict) and "사상처방 전체 색인·처방집" in x)]
sasang.append({"사상처방 전체 색인·처방집": items})

# Validate in memory, then write.
rendered=yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False, width=1000)
yaml.safe_load(rendered)
p.write_text(rendered, encoding="utf-8")
print(f"등록 문서: {len(items)}개")
'@

$tmp = Join-Path $repo "_repair_sasang_nav_v2.py"
Set-Content -Path $tmp -Value $py -Encoding UTF8

python $tmp
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $mkdocs -Force
    Remove-Item $tmp -ErrorAction SilentlyContinue
    throw "YAML 구조 수정 실패. 정상 백업으로 자동 복구했습니다."
}
Remove-Item $tmp -ErrorAction SilentlyContinue
Write-Host "2/3 구조 기반 NAV 등록 완료" -ForegroundColor Green

# 3) Validate with the exact build command used by Actions, if mkdocs is installed locally.
python -c "import yaml; yaml.safe_load(open('mkdocs.yml',encoding='utf-8')); print('YAML parse: OK')"
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $mkdocs -Force
    throw "YAML 검증 실패. 정상 백업으로 자동 복구했습니다."
}

$mkdocsCmd = Get-Command mkdocs -ErrorAction SilentlyContinue
if ($mkdocsCmd) {
    mkdocs build --strict
    if ($LASTEXITCODE -ne 0) {
        Copy-Item $backup $mkdocs -Force
        throw "mkdocs build --strict 실패. 정상 백업으로 자동 복구했습니다. 화면의 오류를 보내주세요."
    }
    Write-Host "3/3 mkdocs build --strict: OK" -ForegroundColor Green
} else {
    Write-Host "3/3 YAML parse OK. 로컬에 mkdocs가 없어 strict build는 GitHub Actions에서 확인합니다." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "완료. GitHub Desktop에서 mkdocs.yml만 변경되었는지 확인하세요." -ForegroundColor Cyan
Write-Host "Commit: Safely register Sasang formula library navigation"
Read-Host "Enter를 누르면 닫힙니다"
