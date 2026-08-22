$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Status = Join-Path $Root "APPLY_44_YAML_FIX_V4_STATUS.txt"

function Write-Status {
    param([string[]]$Lines)
    $Lines | Set-Content $Status -Encoding UTF8
}

try {
    Write-Status @("STARTED")

    if (!(Test-Path "mkdocs.yml")) {
        throw "mkdocs.yml not found"
    }

    $Backup = "mkdocs_44_yaml_fix_v4_backup_" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".yml"
    Copy-Item "mkdocs.yml" $Backup -Force

    $Lines = @(Get-Content "mkdocs.yml" -Encoding UTF8)

    $AtlasPath = "acupoint-network/standard-atlas.md"
    $IndexPath = "acupoint-network/index.md"
    $AtlasLabel = "WHO 표준 361경혈 아틀라스"

    # Remove every existing atlas nav line first.
    $Clean = New-Object System.Collections.Generic.List[string]
    foreach ($Line in $Lines) {
        if ($Line -notmatch [regex]::Escape($AtlasPath)) {
            $Clean.Add($Line)
        }
    }
    $Lines = @($Clean)

    # Find the canonical acupoint-network index nav line.
    $TargetIndex = -1
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match [regex]::Escape($IndexPath)) {
            $TargetIndex = $i
            break
        }
    }

    if ($TargetIndex -lt 0) {
        throw "Could not find acupoint-network/index.md in mkdocs.yml"
    }

    $TargetLine = $Lines[$TargetIndex]
    $Indent = [regex]::Match($TargetLine, '^\s*').Value

    # Insert atlas at EXACTLY the same indentation as the known-good sibling.
    $AtlasLine = $Indent + "- " + $AtlasLabel + ": " + $AtlasPath

    $New = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($i -eq $TargetIndex) {
            $New.Add($AtlasLine)
        }
        $New.Add($Lines[$i])
    }

    $New | Set-Content "mkdocs.yml" -Encoding UTF8

    # Structural checks.
    $Result = Get-Content "mkdocs.yml" -Raw -Encoding UTF8
    $AtlasCount = ([regex]::Matches($Result, [regex]::Escape($AtlasPath))).Count
    $IndexCount = ([regex]::Matches($Result, [regex]::Escape($IndexPath))).Count

    if ($AtlasCount -ne 1) {
        throw ("Atlas path count is " + $AtlasCount + ", expected 1")
    }
    if ($IndexCount -lt 1) {
        throw "acupoint-network/index.md disappeared unexpectedly"
    }

    # Verify exact sibling indentation after save.
    $SavedLines = @(Get-Content "mkdocs.yml" -Encoding UTF8)
    $SavedAtlas = $SavedLines | Where-Object { $_ -match [regex]::Escape($AtlasPath) } | Select-Object -First 1
    $SavedIndex = $SavedLines | Where-Object { $_ -match [regex]::Escape($IndexPath) } | Select-Object -First 1

    $AtlasIndent = [regex]::Match($SavedAtlas, '^\s*').Value.Length
    $IndexIndent = [regex]::Match($SavedIndex, '^\s*').Value.Length

    if ($AtlasIndent -ne $IndexIndent) {
        throw ("Indent mismatch. Atlas=" + $AtlasIndent + ", Index=" + $IndexIndent)
    }

    # Save a nearby snippet for easy inspection.
    $AtlasLineNo = 0
    for ($i = 0; $i -lt $SavedLines.Count; $i++) {
        if ($SavedLines[$i] -match [regex]::Escape($AtlasPath)) {
            $AtlasLineNo = $i
            break
        }
    }

    $Start = [Math]::Max(0, $AtlasLineNo - 4)
    $End = [Math]::Min($SavedLines.Count - 1, $AtlasLineNo + 6)
    $Snippet = @()
    for ($i = $Start; $i -le $End; $i++) {
        $Snippet += (("{0,4}: " -f ($i + 1)) + $SavedLines[$i])
    }
    $Snippet | Set-Content "MKDOCS_44_FIXED_SNIPPET.txt" -Encoding UTF8

    Write-Status @(
        "COMPLETE",
        ("Atlas path count: " + $AtlasCount),
        ("Atlas indentation: " + $AtlasIndent),
        ("Index indentation: " + $IndexIndent),
        ("Backup: " + $Backup),
        "Snippet: MKDOCS_44_FIXED_SNIPPET.txt"
    )

    Write-Host ""
    Write-Host "STANDARD ACUPOINT ATLAS NAV 44 YAML FIX V4 COMPLETE" -ForegroundColor Green
    Write-Host ("Atlas indentation: " + $AtlasIndent + " spaces") -ForegroundColor Cyan
    Write-Host ("Index indentation: " + $IndexIndent + " spaces") -ForegroundColor Cyan
    Write-Host "Created MKDOCS_44_FIXED_SNIPPET.txt" -ForegroundColor Yellow
}
catch {
    Write-Status @(
        "FAILED",
        $_.Exception.Message,
        ($_ | Out-String)
    )

    Write-Host ""
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host "See APPLY_44_YAML_FIX_V4_STATUS.txt" -ForegroundColor Yellow
}

Read-Host "Press Enter to close"
