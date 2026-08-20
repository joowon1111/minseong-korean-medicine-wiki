$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Minseong Sasang Formula NAV Repair ===" -ForegroundColor Cyan
Write-Host ""

# Find repository root from current folder or common GitHub folder.
$repo = Get-Location
if (-not (Test-Path (Join-Path $repo "mkdocs.yml"))) {
    $candidates = @(
        "$HOME\Documents\GitHub\minseong-korean-medicine-wiki",
        "$HOME\GitHub\minseong-korean-medicine-wiki",
        "C:\GitHub\minseong-korean-medicine-wiki"
    )
    foreach ($c in $candidates) {
        if (Test-Path (Join-Path $c "mkdocs.yml")) { $repo = Get-Item $c; break }
    }
}

$mkdocs = Join-Path $repo "mkdocs.yml"
$docs = Join-Path $repo "docs"
$lib = Join-Path $docs "sasang-formula-library"

if (-not (Test-Path $mkdocs)) {
    throw "mkdocs.yml을 찾지 못했습니다. 이 파일을 저장소 최상위에서 실행하세요."
}
if (-not (Test-Path $lib)) {
    throw "docs\sasang-formula-library 폴더를 찾지 못했습니다."
}

# Backup
$backup = "$mkdocs.before-sasang-nav-repair"
Copy-Item $mkdocs $backup -Force

# Read current file without changing unrelated content.
$text = Get-Content $mkdocs -Raw -Encoding UTF8

# Remove an earlier auto-generated block if script is run again.
$start = "# BEGIN AUTO SASANG FORMULA LIBRARY NAV"
$end = "# END AUTO SASANG FORMULA LIBRARY NAV"
$pattern = "(?ms)^\s*" + [regex]::Escape($start) + ".*?^\s*" + [regex]::Escape($end) + "\s*\r?\n?"
$text = [regex]::Replace($text, $pattern, "")

# Build nav items from every markdown file currently in the folder.
$files = Get-ChildItem $lib -Filter "*.md" -File | Sort-Object Name
$items = New-Object System.Collections.Generic.List[string]

foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $title = $null

    if ($content -match '(?m)^title:\s*(.+?)\s*$') {
        $title = $matches[1].Trim().Trim('"').Trim("'")
    }
    if (-not $title -and $content -match '(?m)^#\s+(.+?)\s*$') {
        $title = $matches[1].Trim()
    }
    if (-not $title) {
        $title = [IO.Path]::GetFileNameWithoutExtension($f.Name)
    }

    $path = "sasang-formula-library/" + $f.Name
    $items.Add("        - `"$title`": `"$path`"")
}

if ($items.Count -eq 0) { throw "sasang-formula-library 안에 md 파일이 없습니다." }

$block = @()
$block += "      - `"사상처방 전체 색인·처방집`":"
$block += "        $start"
$block += $items
$block += "        $end"
$blockText = ($block -join "`r`n")

# Insert into existing 사상의학 nav section, immediately before the next top-level nav item.
$lines = $text -split "`r?`n"
$sasangIndex = -1
for ($i=0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s{2}-\s+["'']?사상의학["'']?\s*:') {
        $sasangIndex = $i
        break
    }
}
if ($sasangIndex -lt 0) {
    Copy-Item $backup $mkdocs -Force
    throw "mkdocs.yml nav에서 '사상의학' 항목을 찾지 못했습니다. 원본은 복구했습니다."
}

$insertAt = $lines.Count
for ($i=$sasangIndex+1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s{2}-\s+') {
        $insertAt = $i
        break
    }
}

$newLines = New-Object System.Collections.Generic.List[string]
for ($i=0; $i -lt $insertAt; $i++) { $newLines.Add($lines[$i]) }
$newLines.Add($blockText)
for ($i=$insertAt; $i -lt $lines.Count; $i++) { $newLines.Add($lines[$i]) }

$newText = ($newLines -join "`r`n")
Set-Content -Path $mkdocs -Value $newText -Encoding UTF8

Write-Host "완료: 현재 sasang-formula-library의 모든 .md 파일을 nav에 등록했습니다." -ForegroundColor Green
Write-Host "백업: $backup" -ForegroundColor DarkGray
Write-Host ""
Write-Host "이제 GitHub Desktop에서 변경사항을 확인한 뒤 Commit -> Push origin 하세요." -ForegroundColor Yellow
Write-Host "Commit: Register complete Sasang formula library in navigation"
Write-Host ""
Read-Host "Enter를 누르면 닫힙니다"
