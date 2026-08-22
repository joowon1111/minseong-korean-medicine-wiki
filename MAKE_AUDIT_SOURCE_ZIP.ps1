$ErrorActionPreference="Stop"
try{
    $Root=Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $Root

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host " Minseong Wiki Audit Source Collector" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""

    if(-not(Test-Path "docs")){throw "docs folder not found. ZIP을 저장소 최상위에 풀어주세요."}
    if(-not(Test-Path "mkdocs.yml")){throw "mkdocs.yml not found."}

    $stage="_AUDIT_UPLOAD_SOURCE"
    $zip="MINSEONG_WIKI_AUDIT_SOURCE.zip"

    if(Test-Path $stage){Remove-Item $stage -Recurse -Force}
    if(Test-Path $zip){Remove-Item $zip -Force}

    Write-Host "1/3 docs 폴더 복사 중..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force $stage | Out-Null
    Copy-Item "docs" "$stage\docs" -Recurse -Force

    Write-Host "2/3 mkdocs.yml 복사 중..." -ForegroundColor Yellow
    Copy-Item "mkdocs.yml" "$stage\mkdocs.yml" -Force

    if(Test-Path ".github"){
        Write-Host "   .github workflow도 포함합니다..." -ForegroundColor DarkGray
        Copy-Item ".github" "$stage\.github" -Recurse -Force
    }

    Write-Host "3/3 업로드용 ZIP 생성 중..." -ForegroundColor Yellow
    Compress-Archive -Path "$stage\*" -DestinationPath $zip -CompressionLevel Fastest -Force

    $size=(Get-Item $zip).Length
    $mb=[math]::Round($size/1MB,2)

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host " COMPLETE" -ForegroundColor Green
    Write-Host " 생성 파일: MINSEONG_WIKI_AUDIT_SOURCE.zip" -ForegroundColor Cyan
    Write-Host (" 크기: {0} MB" -f $mb) -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "이 ZIP 파일을 ChatGPT 채팅에 올려주세요." -ForegroundColor Yellow
}
catch{
    Write-Host ""
    Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
