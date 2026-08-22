$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function Log($msg) {
    Write-Host $msg
    Add-Content -Path "_quality_audit\AUDIT_PROGRESS.txt" -Value ("[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $msg) -Encoding UTF8
}

try {
    $Root = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $Root

    New-Item -ItemType Directory -Force "_quality_audit" | Out-Null
    "민성 한의학 아카이브 구조 감사 - 실행 시작" | Set-Content "_quality_audit\AUDIT_PROGRESS.txt" -Encoding UTF8
    "# 민성 한의학 아카이브 전체 품질감사 — 구조 1차" | Set-Content "_quality_audit\AUDIT_REPORT.md" -Encoding UTF8
    Add-Content "_quality_audit\AUDIT_REPORT.md" "`r`n> 이 보고서는 사이트 파일을 수정하지 않는 진단 전용입니다.`r`n" -Encoding UTF8

    if (-not (Test-Path "docs")) { throw "docs 폴더가 없습니다. ZIP을 저장소 최상위에 풀어주세요." }

    Log "1/6 Markdown 파일 목록 수집 중..."
    $docsRoot = (Resolve-Path "docs").Path
    $files = @(Get-ChildItem "docs" -Recurse -File -Filter "*.md")
    Log ("Markdown {0}개 확인" -f $files.Count)

    $existing = @{}
    foreach($f in $files) {
        $r = $f.FullName.Substring($docsRoot.Length).TrimStart('\').Replace('\','/')
        $existing[$r] = $true
    }

    Log "2/6 front matter / H1 / 핵심답변 검사 중..."
    $noFront = @()
    $noH1 = @()
    $noCore = @()
    $answerCount = 0
    $thin = @()
    $i = 0

    foreach($f in $files) {
        $i++
        if(($i % 100) -eq 0) { Log ("  문서 {0}/{1}" -f $i,$files.Count) }

        $r = $f.FullName.Substring($docsRoot.Length).TrimStart('\').Replace('\','/')
        $text = [System.IO.File]::ReadAllText($f.FullName)

        if(-not $text.StartsWith("---")) { $noFront += $r }
        if($text -notmatch '(?m)^#\s+\S') { $noH1 += $r }
        if(($text -replace '\s+',' ').Length -lt 650) { $thin += $r }

        if($r.StartsWith("answer-guides/")) {
            $answerCount++
            if($text -notmatch '(?m)^##\s+핵심 답변\s*$') { $noCore += $r }
        }
    }

    Log "3/6 mkdocs nav 등록 여부 검사 중..."
    $navText = ""
    if(Test-Path "mkdocs.yml") { $navText = [System.IO.File]::ReadAllText((Resolve-Path "mkdocs.yml").Path) }
    $notInNav = @()
    foreach($r in $existing.Keys) {
        if($navText -notmatch [regex]::Escape($r)) { $notInNav += $r }
    }

    Log "4/6 내부 Markdown 링크 검사 중..."
    $broken = @()
    $incoming = @{}
    $i = 0
    foreach($f in $files) {
        $i++
        if(($i % 100) -eq 0) { Log ("  링크 검사 {0}/{1}" -f $i,$files.Count) }

        $src = $f.FullName.Substring($docsRoot.Length).TrimStart('\').Replace('\','/')
        $text = [System.IO.File]::ReadAllText($f.FullName)

        foreach($m in [regex]::Matches($text, '\[[^\]]+\]\(([^)]+)\)')) {
            $target = $m.Groups[1].Value.Trim()
            if([string]::IsNullOrWhiteSpace($target)) { continue }
            if($target.StartsWith("http://") -or $target.StartsWith("https://") -or $target.StartsWith("mailto:") -or $target.StartsWith("#")) { continue }

            $target = ($target -split '#')[0]
            $target = ($target -split '\?')[0]
            if([string]::IsNullOrWhiteSpace($target)) { continue }

            try {
                $base = Split-Path $f.FullName -Parent
                $candidate = [System.IO.Path]::GetFullPath((Join-Path $base $target))
                if(-not $candidate.StartsWith($docsRoot)) { continue }

                $tr = $candidate.Substring($docsRoot.Length).TrimStart('\').Replace('\','/')
                if($tr.EndsWith("/")) { $tr += "index.md" }
                if(-not $tr.EndsWith(".md")) { $tr += ".md" }

                if($existing.ContainsKey($tr)) {
                    if(-not $incoming.ContainsKey($tr)) { $incoming[$tr] = 0 }
                    $incoming[$tr] = [int]$incoming[$tr] + 1
                } else {
                    $broken += ("{0} -> {1} [resolved: {2}]" -f $src,$target,$tr)
                }
            } catch {
                $broken += ("{0} -> {1} [path parse error]" -f $src,$target)
            }
        }
    }

    Log "5/6 고아 페이지 후보 계산 중..."
    $orphans = @()
    foreach($r in $existing.Keys) {
        $inc = 0
        if($incoming.ContainsKey($r)) { $inc = [int]$incoming[$r] }
        if($inc -eq 0 -and ($navText -notmatch [regex]::Escape($r)) -and -not $r.EndsWith("index.md")) {
            $orphans += $r
        }
    }

    Log "6/6 보고서 작성 중..."
    $report = "_quality_audit\AUDIT_REPORT.md"

    Add-Content $report ("## 요약`r`n`r`n- 전체 Markdown: **{0}**`r`n- answer-guides: **{1}**`r`n- 깨진 내부링크: **{2}**`r`n- nav 미등록: **{3}**`r`n- 고아 페이지 후보: **{4}**`r`n- front matter 없음: **{5}**`r`n- H1 없음: **{6}**`r`n- 얇은 페이지 후보: **{7}**`r`n- 핵심답변 없는 answer-guide: **{8}**`r`n" -f $files.Count,$answerCount,$broken.Count,$notInNav.Count,$orphans.Count,$noFront.Count,$noH1.Count,$thin.Count,$noCore.Count) -Encoding UTF8

    function WriteSection($title,$items) {
        Add-Content $report ("`r`n## {0}`r`n" -f $title) -Encoding UTF8
        if(@($items).Count -eq 0) {
            Add-Content $report "- 없음" -Encoding UTF8
        } else {
            $count = 0
            foreach($x in @($items | Sort-Object)) {
                if($count -ge 400) { Add-Content $report "- ... 나머지 생략" -Encoding UTF8; break }
                Add-Content $report ("- " + $x) -Encoding UTF8
                $count++
            }
        }
    }

    WriteSection "깨진 내부링크" $broken
    WriteSection "고아 페이지 후보" $orphans
    WriteSection "nav 미등록 문서" $notInNav
    WriteSection "front matter 없음" $noFront
    WriteSection "H1 없음" $noH1
    WriteSection "핵심답변 없는 answer-guide" $noCore
    WriteSection "얇은 페이지 후보" $thin

    $broken | Set-Content "_quality_audit\broken_links.txt" -Encoding UTF8
    $orphans | Set-Content "_quality_audit\orphans.txt" -Encoding UTF8
    $notInNav | Set-Content "_quality_audit\not_in_nav.txt" -Encoding UTF8

    Log "감사 완료!"
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host " QUALITY AUDIT SUCCESS" -ForegroundColor Green
    Write-Host " _quality_audit\AUDIT_REPORT.md 생성 완료" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Green
}
catch {
    New-Item -ItemType Directory -Force "_quality_audit" | Out-Null
    $err = $_ | Out-String
    $err | Set-Content "_quality_audit\AUDIT_ERROR_FULL.txt" -Encoding UTF8
    Write-Host ""
    Write-Host "AUDIT ERROR" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "상세 오류: _quality_audit\AUDIT_ERROR_FULL.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"
