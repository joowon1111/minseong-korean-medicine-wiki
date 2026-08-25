$ErrorActionPreference = "Stop"
$target = Join-Path $PSScriptRoot "docs\evidence-radar"

Write-Host "Minseong Evidence Radar public cleanup" -ForegroundColor Cyan

if (Test-Path $target) {
    Remove-Item $target -Recurse -Force
    Write-Host "Removed public docs/evidence-radar folder." -ForegroundColor Green
} else {
    Write-Host "docs/evidence-radar already absent." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Internal tools/evidence-radar is NOT touched." -ForegroundColor Green
Write-Host "Reviewed evidence already merged into condition pages is NOT touched." -ForegroundColor Green
