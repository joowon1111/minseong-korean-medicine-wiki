$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Docs = Join-Path $Root "docs"
if (-not (Test-Path $Docs)) {
    Write-Host "ERROR: docs 폴더를 찾을 수 없습니다." -ForegroundColor Red
    Read-Host "Enter를 누르면 종료합니다"
    exit 1
}

$Report = Join-Path $Root "CONTENT_QUALITY_AUDIT_REPORT.md"
$JsonOut = Join-Path $Root "CONTENT_QUALITY_AUDIT.json"

function Get-FrontMatter([string]$Text) {
    if ($Text.StartsWith("---")) {
        $m=[regex]::Match($Text,'(?s)^---\s*\r?\n(.*?)\r?\n---')
        if ($m.Success) { return $m.Groups[1].Value }
    }
    return ""
}
function Get-Body([string]$Text) {
    return [regex]::Replace($Text,'(?s)^---\s*\r?\n.*?\r?\n---\s*','',1)
}
function Get-Title([string]$Text,[string]$Fallback) {
    $fm=Get-FrontMatter $Text
    $m=[regex]::Match($fm,'(?m)^title:\s*(.+?)\s*$')
    if ($m.Success) { return $m.Groups[1].Value.Trim().Trim('"').Trim("'") }
    $body=Get-Body $Text
    $m=[regex]::Match($body,'(?m)^#\s+(.+?)\s*$')
    if ($m.Success) { return $m.Groups[1].Value.Trim() }
    return $Fallback
}
function Get-Description([string]$Text) {
    $fm=Get-FrontMatter $Text
    $m=[regex]::Match($fm,'(?m)^description:\s*(.+?)\s*$')
    if ($m.Success) { return $m.Groups[1].Value.Trim().Trim('"').Trim("'") }
    return ""
}
function Normalize-Title([string]$s) {
    $x=$s.ToLower()
    $x=[regex]::Replace($x,'[^가-힣a-z0-9]+',' ')
    $stop=@('한약','보약','한의원','환자검색','찾기','증상','치료','관련','가이드','무엇인가요','어떻게')
    $t=@()
    foreach($v in $x.Split(' ',[System.StringSplitOptions]::RemoveEmptyEntries)) {
        if ($stop -notcontains $v) { $t += $v }
    }
    return ($t -join ' ')
}

$rows=@()
$files=Get-ChildItem $Docs -Recurse -File -Filter *.md
foreach($f in $files) {
    $text=Get-Content $f.FullName -Raw -Encoding UTF8
    $body=Get-Body $text
    $clean=[regex]::Replace($body,'(?s)```.*?```',' ')
    $clean=[regex]::Replace($clean,'<[^>]+>',' ')
    $words=[regex]::Matches($clean,'[가-힣A-Za-z0-9]+').Count
    $links=[regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')
    $internal=0
    foreach($l in $links) {
        $target=$l.Groups[1].Value
        if ($target -notmatch '^(https?:|mailto:|#)') { $internal++ }
    }
    $rel=$f.FullName.Substring($Docs.FullName.Length).TrimStart('\').Replace('\','/')
    $rows += [pscustomobject]@{
        file=$rel
        title=(Get-Title $text $f.BaseName)
        description=(Get-Description $text)
        words=$words
        internal_links=$internal
    }
}

$thin=@($rows | Where-Object {$_.words -lt 180} | Sort-Object words)
$veryThin=@($rows | Where-Object {$_.words -lt 100} | Sort-Object words)
$noDesc=@($rows | Where-Object {[string]::IsNullOrWhiteSpace($_.description)})
$lowLinks=@($rows | Where-Object {$_.internal_links -lt 3} | Sort-Object internal_links,words)

$groups=@{}
foreach($r in $rows) {
    $n=Normalize-Title $r.title
    if ($n) {
        if (-not $groups.ContainsKey($n)) { $groups[$n]=@() }
        $groups[$n] += $r.file
    }
}
$dupes=@()
foreach($k in $groups.Keys) {
    if ($groups[$k].Count -gt 1) {
        $dupes += [pscustomobject]@{ key=$k; files=$groups[$k] }
    }
}

$summary=[ordered]@{
    files=$rows.Count
    thin_under_180=$thin.Count
    very_thin_under_100=$veryThin.Count
    missing_description=$noDesc.Count
    low_internal_links_under_3=$lowLinks.Count
    duplicate_normalized_title_groups=$dupes.Count
}

$data=[ordered]@{
    summary=$summary
    very_thin=$veryThin
    thin=$thin
    missing_description=$noDesc
    low_links=$lowLinks
    duplicate_groups=$dupes
}
$data | ConvertTo-Json -Depth 8 | Set-Content $JsonOut -Encoding UTF8

$sb=New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# 민성 한의학 아카이브 콘텐츠 품질 감사 보고서")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("이 보고서는 문서를 자동 삭제하거나 병합하지 않습니다. 검토 후보만 찾습니다.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## 요약")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- 전체 Markdown 문서: **$($rows.Count)**")
[void]$sb.AppendLine("- 180단어 미만 얇은 문서 후보: **$($thin.Count)**")
[void]$sb.AppendLine("- 100단어 미만 매우 얇은 문서 후보: **$($veryThin.Count)**")
[void]$sb.AppendLine("- description 없는 문서: **$($noDesc.Count)**")
[void]$sb.AppendLine("- 내부링크 3개 미만 문서: **$($lowLinks.Count)**")
[void]$sb.AppendLine("- 정규화 제목 중복 그룹: **$($dupes.Count)**")
[void]$sb.AppendLine("")

function Add-Table($builder,[string]$heading,$items,[int]$limit=120) {
    [void]$builder.AppendLine("## $heading")
    [void]$builder.AppendLine("")
    if (@($items).Count -eq 0) {
        [void]$builder.AppendLine("_없음_")
        [void]$builder.AppendLine("")
        return
    }
    [void]$builder.AppendLine("| 파일 | 제목 | 단어수 | 내부링크 |")
    [void]$builder.AppendLine("| --- | --- | ---: | ---: |")
    foreach($r in @($items | Select-Object -First $limit)) {
        $title=($r.title -replace '\|','\|')
        [void]$builder.AppendLine("| ``$($r.file)`` | $title | $($r.words) | $($r.internal_links) |")
    }
    [void]$builder.AppendLine("")
}
Add-Table $sb "1. 매우 얇은 문서 우선 검토" $veryThin 100
Add-Table $sb "2. 얇은 문서 후보" $thin 150
Add-Table $sb "3. description 없는 문서" $noDesc 150
Add-Table $sb "4. 내부링크 부족 후보" $lowLinks 150

[void]$sb.AppendLine("## 5. 제목 중복 그룹")
[void]$sb.AppendLine("")
if ($dupes.Count -eq 0) {
    [void]$sb.AppendLine("_없음_")
} else {
    foreach($d in $dupes) {
        [void]$sb.AppendLine("### $($d.key)")
        foreach($x in $d.files) { [void]$sb.AppendLine("- ``$x``") }
        [void]$sb.AppendLine("")
    }
}

[void]$sb.AppendLine("")
[void]$sb.AppendLine("## 권장 정리 원칙")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("1. 짧다는 이유만으로 문서를 삭제하지 않습니다.")
[void]$sb.AppendLine("2. 검색 의도가 다른 문서는 유지합니다.")
[void]$sb.AppendLine("3. 같은 검색 의도와 내용이 반복되면 핵심 허브 통합 후보로 검토합니다.")
[void]$sb.AppendLine("4. 핵심 허브는 세부문서보다 더 풍부한 설명과 내부링크를 갖도록 보강합니다.")
[void]$sb.AppendLine("5. 녹용보약·맞춤한약·기력회복·통증·자율신경·여성·소아 등 주요 진료 연관 문서는 병합 전에 우선 보강 여부를 검토합니다.")

$sb.ToString() | Set-Content $Report -Encoding UTF8

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host "감사 완료" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host "전체 문서: $($rows.Count)"
Write-Host "180단어 미만: $($thin.Count)"
Write-Host "100단어 미만: $($veryThin.Count)"
Write-Host "description 누락: $($noDesc.Count)"
Write-Host "내부링크 3개 미만: $($lowLinks.Count)"
Write-Host ""
Write-Host "CREATED: CONTENT_QUALITY_AUDIT_REPORT.md" -ForegroundColor Cyan
Write-Host "CREATED: CONTENT_QUALITY_AUDIT.json" -ForegroundColor Cyan
Write-Host ""
Read-Host "Enter를 누르면 종료합니다"
