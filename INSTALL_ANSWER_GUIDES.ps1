$ErrorActionPreference="Stop"
try{
 $Root=Split-Path -Parent $MyInvocation.MyCommand.Path
 Set-Location $Root
 if(-not(Test-Path "docs")){throw "docs folder not found"}
 $src=Join-Path $Root "_answer_guides_payload"
 if(-not(Test-Path $src)){throw "payload folder not found"}
 $dest=Join-Path $Root "docs\answer-guides"
 New-Item -ItemType Directory -Force -Path $dest|Out-Null
 Copy-Item (Join-Path $src "*.md") $dest -Force
 Write-Host "ANSWER GUIDES INSTALLED: 5" -ForegroundColor Green
 Write-Host "Files copied to docs\answer-guides" -ForegroundColor Cyan
}
catch{Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red}
Read-Host "Press Enter to close"
