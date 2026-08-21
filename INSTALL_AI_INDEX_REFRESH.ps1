$ErrorActionPreference = "Stop"

try {
    $Root = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $Root

    if (-not (Test-Path "docs")) {
        throw "docs folder not found. Extract this ZIP into the repository root."
    }

    $src = Join-Path $Root "_ai_index_payload\ai-index.md"
    $dest = Join-Path $Root "docs\ai-index.md"

    if (-not (Test-Path $src)) {
        throw "payload ai-index.md not found."
    }

    if (Test-Path $dest) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backup = Join-Path $Root ("docs\ai-index.backup-" + $stamp + ".md")
        Copy-Item $dest $backup -Force
        Write-Host "Backup created: $backup" -ForegroundColor Yellow
    }

    Copy-Item $src $dest -Force

    $text = Get-Content $dest -Raw -Encoding UTF8
    if ($text -notmatch "AI 질문형 답변 가이드") {
        throw "Validation failed: new ai-index content was not written."
    }

    Write-Host ""
    Write-Host "AI INDEX REFRESH COMPLETE" -ForegroundColor Green
    Write-Host "Updated: docs\ai-index.md" -ForegroundColor Green
    Write-Host "Dialect/lifestyle-language section: NOT included" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next: review git diff -> Commit -> Push -> check GitHub Actions." -ForegroundColor Cyan
}
catch {
    Write-Host ""
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
