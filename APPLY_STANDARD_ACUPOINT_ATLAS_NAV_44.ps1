$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Status = Join-Path $Root "APPLY_44_STATUS.txt"

try {
    if (!(Test-Path "mkdocs.yml")) {
        throw "mkdocs.yml not found"
    }

    $Backup = "mkdocs_44_backup_" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".yml"
    Copy-Item "mkdocs.yml" $Backup -Force

    $Lines = Get-Content "mkdocs.yml" -Encoding UTF8
    $AtlasPath = "acupoint-network/standard-atlas.md"
    $AtlasLabel = "WHO 표준 361경혈 아틀라스"

    $Clean = New-Object System.Collections.Generic.List[string]
    foreach ($Line in $Lines) {
        if ($Line -match [regex]::Escape($AtlasPath)) {
            continue
        }
        $Clean.Add($Line)
    }
    $Lines = @($Clean)

    $SectionIndex = -1
    $SectionIndent = -1

    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match '^\s*-\s*침구·치료\s*:\s*$') {
            $SectionIndex = $i
            $SectionIndent = ([regex]::Match($Lines[$i], '^\s*').Value.Length)
            break
        }
    }

    $NewLines = New-Object System.Collections.Generic.List[string]

    if ($SectionIndex -ge 0) {
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            $NewLines.Add($Lines[$i])
            if ($i -eq $SectionIndex) {
                $ChildIndent = " " * ($SectionIndent + 4)
                $NewLines.Add($ChildIndent + "- " + $AtlasLabel + ": " + $AtlasPath)
            }
        }
    }
    else {
        $Inserted = $false
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            $Line = $Lines[$i]
            if (!$Inserted -and $Line -match 'acupoint-network/index\.md') {
                $Indent = [regex]::Match($Line, '^\s*').Value
                $NewLines.Add($Indent + "- " + $AtlasLabel + ": " + $AtlasPath)
                $Inserted = $true
            }
            $NewLines.Add($Line)
        }

        if (!$Inserted) {
            throw "Could not find acupuncture nav section or acupoint-network/index.md"
        }
    }

    $NewLines | Set-Content "mkdocs.yml" -Encoding UTF8

    $Result = Get-Content "mkdocs.yml" -Raw -Encoding UTF8
    $Count = ([regex]::Matches($Result, [regex]::Escape($AtlasPath))).Count

    if ($Count -ne 1) {
        throw ("Atlas nav entry count is " + $Count + ", expected 1")
    }

    @(
        "COMPLETE",
        "Added nav entry: " + $AtlasLabel,
        "Path: " + $AtlasPath,
        "Entry count: " + $Count,
        "Backup: " + $Backup
    ) | Set-Content $Status -Encoding UTF8

    Write-Host ""
    Write-Host "STANDARD ACUPOINT ATLAS NAV 44 COMPLETE" -ForegroundColor Green
    Write-Host "Added as a high-visibility left navigation item." -ForegroundColor Cyan
    Write-Host ("Backup: " + $Backup) -ForegroundColor Yellow
}
catch {
    @(
        "FAILED",
        $_.Exception.Message,
        ($_ | Out-String)
    ) | Set-Content $Status -Encoding UTF8

    Write-Host ""
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host "See APPLY_44_STATUS.txt" -ForegroundColor Yellow
}

Read-Host "Press Enter to close"
