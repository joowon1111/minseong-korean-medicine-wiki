$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Out = Join-Path $Root "_quality_audit_30"
New-Item -ItemType Directory -Force $Out | Out-Null

$Progress = Join-Path $Out "AUDIT_PROGRESS.txt"
$ErrorFile = Join-Path $Out "AUDIT_ERROR_FULL.txt"
$Report = Join-Path $Out "AUDIT_REPORT_30.md"
$Ranking = Join-Path $Out "AUDIT_RANKING.tsv"

"STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Set-Content $Progress -Encoding UTF8
"" | Set-Content $ErrorFile -Encoding UTF8

try {
    Write-Host "SECOND QUALITY AUDIT 30 FIXED - START" -ForegroundColor Green
    Write-Host "Output folder: _quality_audit_30" -ForegroundColor Cyan

    $Docs = Join-Path $Root "docs"
    if (!(Test-Path $Docs)) {
        throw "docs folder not found. Put this BAT/PS1 in the repository root beside docs and mkdocs.yml."
    }

    $files = @(Get-ChildItem $Docs -Recurse -Filter *.md -File)
    "FOUND $($files.Count) MARKDOWN FILES" | Add-Content $Progress -Encoding UTF8
    Write-Host ("Markdown files found: " + $files.Count) -ForegroundColor Cyan

    $rows = New-Object System.Collections.Generic.List[object]
    $broken = New-Object System.Collections.Generic.List[string]
    $legacy = New-Object System.Collections.Generic.List[string]
    $append = New-Object System.Collections.Generic.List[string]

    $priorityPrefixes = @(
        "conditions/","herbs/","formulas/","pillar/","network/",
        "formula-architecture/","sasang/","classics/","meridian-network/",
        "acupoint-network/","clinical-core/","diagnostics/","research/",
        "evidence-integrated/"
    )
    $legacyWords = @("TODO","TBD","placeholder")
    $appendWords = @("EXPANSION_","_START -->","ACUPOINT_ATLAS_","MERIDIAN_EXPANSION_")

    $i = 0
    foreach ($f in $files) {
        $i++
        if (($i % 50) -eq 0 -or $i -eq 1 -or $i -eq $files.Count) {
            $msg = "SCANNING $i / $($files.Count) : $($f.Name)"
            Write-Host $msg -ForegroundColor Yellow
            $msg | Add-Content $Progress -Encoding UTF8
        }

        $txt = Get-Content $f.FullName -Raw -Encoding UTF8
        if ($null -eq $txt) { $txt = "" }

        $rel = $f.FullName.Substring($Docs.Length).TrimStart('\').Replace('\','/')
        $body = $txt -replace '(?s)^---\s*.*?\s*---\s*',''
        $bodyCompact = ($body -replace '\s+','')
        $chars = $bodyCompact.Length
        $headings = ([regex]::Matches($body, '(?m)^#{1,6}\s+')).Count
        $links = [regex]::Matches($body, '\[[^\]]+\]\(([^)]+)\)')
        $internal = 0

        foreach ($m in $links) {
            $href = $m.Groups[1].Value.Trim()
            if ($href -match '^(https?://|#|mailto:|tel:)') { continue }
            $internal++

            $target = ($href -split '#')[0]
            $target = ($target -split '\?')[0]
            if ([string]::IsNullOrWhiteSpace($target)) { continue }

            $dest = Join-Path $f.DirectoryName $target
            $ok = Test-Path $dest
            if (!$ok -and [IO.Path]::GetExtension($dest) -eq "") {
                $ok = (Test-Path ($dest + ".md")) -or (Test-Path (Join-Path $dest "index.md"))
            }
            if (!$ok) {
                $broken.Add("$rel`t$href")
            }
        }

        $hasTitle = $txt -match '(?m)^title\s*:'
        $hasDesc = $txt -match '(?m)^description\s*:'
        $priority = $false
        foreach ($pp in $priorityPrefixes) {
            if ($rel.StartsWith($pp)) { $priority = $true; break }
        }

        $score = 0
        $reasons = New-Object System.Collections.Generic.List[string]
        if ($chars -lt 500) { $score += 5; $reasons.Add("very short body") }
        elseif ($chars -lt 900) { $score += 3; $reasons.Add("short body") }
        elseif ($chars -lt 1400) { $score += 1; $reasons.Add("content depth candidate") }

        if ($headings -lt 3) { $score += 2; $reasons.Add("few sections") }
        if ($internal -lt 2) { $score += 2; $reasons.Add("few internal links") }
        if (!$hasDesc) { $score += 1; $reasons.Add("missing description") }
        if ($priority) { $score += 1 }

        foreach ($w in $legacyWords) {
            if ($txt.IndexOf($w, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $score += 3
                $reasons.Add("legacy/incomplete marker")
                $legacy.Add("$rel`t$w")
                break
            }
        }
        foreach ($w in $appendWords) {
            if ($txt.IndexOf($w, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $score += 2
                $reasons.Add("old append marker")
                $append.Add("$rel`t$w")
                break
            }
        }

        $rows.Add([PSCustomObject]@{
            Score=$score
            Path=$rel
            BodyChars=$chars
            Headings=$headings
            InternalLinks=$internal
            HasTitle=$hasTitle
            HasDescription=$hasDesc
            Reasons=($reasons -join "; ")
        })
    }

    $sorted = @($rows | Sort-Object @{Expression="Score";Descending=$true}, @{Expression="BodyChars";Ascending=$true}, Path)
    $priorityRows = @($sorted | Where-Object {$_.Score -ge 5})

    "score`tpath`tbody_chars`theadings`tinternal_links`thas_title`thas_description`treasons" | Set-Content $Ranking -Encoding UTF8
    foreach ($r in $sorted) {
        "$($r.Score)`t$($r.Path)`t$($r.BodyChars)`t$($r.Headings)`t$($r.InternalLinks)`t$($r.HasTitle)`t$($r.HasDescription)`t$($r.Reasons)" | Add-Content $Ranking -Encoding UTF8
    }

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# Second Quality Audit 30")
    $lines.Add("")
    $lines.Add("- Markdown files scanned: **$($sorted.Count)**")
    $lines.Add("- Priority modernization candidates (score >= 5): **$($priorityRows.Count)**")
    $lines.Add("- Broken relative-link candidates: **$(@($broken | Sort-Object -Unique).Count)**")
    $lines.Add("")
    $lines.Add("## Priority modernization candidates")
    $lines.Add("")
    $lines.Add("|Rank|Document|Score|Body chars|Sections|Internal links|Reasons|")
    $lines.Add("|---:|---|---:|---:|---:|---:|---|")
    $rank=0
    foreach ($r in ($priorityRows | Select-Object -First 100)) {
        $rank++
        $reason = $r.Reasons.Replace("|","\|")
        $path = $r.Path.Replace("|","\|")
        $lines.Add("|$rank|``$path``|$($r.Score)|$($r.BodyChars)|$($r.Headings)|$($r.InternalLinks)|$reason|")
    }

    $lines.Add("")
    $lines.Add("## Broken relative-link candidates")
    $lines.Add("")
    $uniqueBroken = @($broken | Sort-Object -Unique)
    if ($uniqueBroken.Count -eq 0) {
        $lines.Add("- None detected")
    } else {
        foreach ($b in ($uniqueBroken | Select-Object -First 250)) {
            $parts = $b -split "`t",2
            $lines.Add("- ``$($parts[0])`` -> ``$($parts[1])``")
        }
    }

    $lines.Add("")
    $lines.Add("## Old append markers")
    $lines.Add("")
    $uniqueAppend = @($append | Sort-Object -Unique)
    if ($uniqueAppend.Count -eq 0) { $lines.Add("- None detected") }
    else { foreach ($a in $uniqueAppend) { $lines.Add("- ``$a``") } }

    $lines.Add("")
    $lines.Add("## Next-step rule")
    $lines.Add("")
    $lines.Add("Do not automatically overwrite high-scoring files. Read the actual source first, preserve useful material, and rebuild each priority group in place rather than appending new sections.")

    $lines | Set-Content $Report -Encoding UTF8

    @(
        "COMPLETE"
        "Markdown files: $($sorted.Count)"
        "Priority candidates: $($priorityRows.Count)"
        "Broken links: $($uniqueBroken.Count)"
        "Report: _quality_audit_30/AUDIT_REPORT_30.md"
        "Ranking: _quality_audit_30/AUDIT_RANKING.tsv"
    ) | Set-Content $Progress -Encoding UTF8

    Write-Host ""
    Write-Host "SECOND QUALITY AUDIT 30 FIXED COMPLETE" -ForegroundColor Green
    Write-Host ("Priority candidates: " + $priorityRows.Count) -ForegroundColor Cyan
    Write-Host ("Broken links: " + $uniqueBroken.Count) -ForegroundColor Cyan
    Write-Host "Created:" -ForegroundColor Yellow
    Write-Host "  _quality_audit_30\AUDIT_REPORT_30.md"
    Write-Host "  _quality_audit_30\AUDIT_RANKING.tsv"
    Write-Host "  _quality_audit_30\AUDIT_PROGRESS.txt"
    Write-Host "  _quality_audit_30\AUDIT_ERROR_FULL.txt"
}
catch {
    $msg = $_ | Out-String
    $msg | Set-Content $ErrorFile -Encoding UTF8
    "FAILED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Set-Content $Progress -Encoding UTF8
    Write-Host ""
    Write-Host ("AUDIT FAILED: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host "See _quality_audit_30\AUDIT_ERROR_FULL.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"
