$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Status = Join-Path $Root 'APPLY_43_URL_FIX_V3_STATUS.txt'

try {
    'STARTED' | Set-Content $Status -Encoding UTF8

    if (!(Test-Path 'docs')) {
        throw 'docs folder not found'
    }

    if (!(Test-Path 'docs\acupuncture\points')) {
        throw 'docs\acupuncture\points folder not found'
    }

    New-Item -ItemType Directory -Force 'docs\acupoint-network' | Out-Null
    New-Item -ItemType Directory -Force '_quality_audit_43' | Out-Null

    $Backup = '_backup_acupoint43_urlfix_v3_' + (Get-Date -Format 'yyyyMMdd-HHmmss')
    New-Item -ItemType Directory -Force $Backup | Out-Null

    $Order = @('LU','LI','ST','SP','HT','SI','BL','KI','PC','TE','GB','LR','GV','CV')
    $Expected = @{
        LU=11
        LI=20
        ST=45
        SP=21
        HT=9
        SI=19
        BL=67
        KI=27
        PC=9
        TE=23
        GB=44
        LR=14
        GV=28
        CV=24
    }

    $Rows = @()

    foreach ($File in Get-ChildItem 'docs\acupuncture\points' -File -Filter '*.md') {
        $Text = Get-Content $File.FullName -Raw -Encoding UTF8

        $Match = [regex]::Match(
            $Text,
            '(?im)^\|\s*WHO\s+.*?\|\s*\*\*((?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR|GV|CV)\d{1,2})\*\*\s*\|'
        )

        if (!$Match.Success) {
            $Match = [regex]::Match(
                $Text,
                '(?im)\*\*((?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR|GV|CV)\d{1,2})\*\*'
            )
        }

        if (!$Match.Success) {
            continue
        }

        $Code = $Match.Groups[1].Value.ToUpper()
        $Meridian = [regex]::Match($Code, '^[A-Z]+').Value

        if (!($Order -contains $Meridian)) {
            continue
        }

        $Heading = [regex]::Match($Text, '(?m)^#\s+(.+)$')
        if ($Heading.Success) {
            $Title = $Heading.Groups[1].Value.Trim()
        }
        else {
            $Title = $Code
        }

        $Rows += [PSCustomObject]@{
            Code = $Code
            Meridian = $Meridian
            Title = $Title
            FileName = $File.Name
        }
    }

    $Rows = @($Rows | Sort-Object Code -Unique)

    if ($Rows.Count -ne 361) {
        throw ('Expected 361 standard acupoints but found ' + $Rows.Count)
    }

    function Get-PointNumber {
        param([string]$Code)
        return [int]([regex]::Match($Code, '\d+').Value)
    }

    $Atlas = 'docs\acupoint-network\standard-atlas.md'

    if (Test-Path $Atlas) {
        Copy-Item $Atlas (Join-Path $Backup 'standard-atlas.md') -Force
    }

    $Lines = @()
    $Lines += '---'
    $Lines += 'title: WHO Standard 361 Acupoint Clinical Atlas'
    $Lines += 'description: Standard 361 acupoints integrated with the existing Minseong meridian and clinical acupoint network.'
    $Lines += 'status: reviewed'
    $Lines += 'last_reviewed: 2026-08-22'
    $Lines += '---'
    $Lines += '# WHO Standard 361 Acupoint Clinical Atlas'
    $Lines += ''
    $Lines += 'This page indexes the existing canonical point pages by the WHO standard 361-point system.'
    $Lines += ''

    foreach ($Meridian in $Order) {
        $MeridianRows = @(
            $Rows |
            Where-Object { $_.Meridian -eq $Meridian } |
            Sort-Object @{ Expression = { Get-PointNumber $_.Code } }
        )

        $Lines += ('## ' + $Meridian + ' - ' + $MeridianRows.Count + ' points')

        $Parts = @()
        foreach ($Row in $MeridianRows) {
            $Link = '../acupuncture/points/' + $Row.FileName
            $Parts += ('[' + $Row.Title + '](' + $Link + ')')
        }

        $Lines += ($Parts -join ' | ')
        $Lines += ''
    }

    $Lines += '## Related knowledge networks'
    $Lines += ''
    $Lines += '- [Clinical acupoint network](index.md)'
    $Lines += '- [Meridian-to-symptom map](by-condition.md)'
    $Lines += '- [Meridian network](../meridian-network/index.md)'
    $Lines += '- [Special-point network](../meridian-network/special-points/index.md)'
    $Lines += '- [Clinical point combinations](../network/acupoint-combinations.md)'

    $Lines | Set-Content $Atlas -Encoding UTF8

    $Hub = 'docs\acupoint-network\index.md'
    if (Test-Path $Hub) {
        Copy-Item $Hub (Join-Path $Backup 'acupoint-network-index.md') -Force

        $HubText = Get-Content $Hub -Raw -Encoding UTF8
        $StartMarker = '<!-- MS_43_URL_FIX_V3_START -->'
        $EndMarker = '<!-- MS_43_URL_FIX_V3_END -->'

        $BlockLines = @()
        $BlockLines += $StartMarker
        $BlockLines += '## WHO standard 361-acupoint atlas'
        $BlockLines += ''
        $BlockLines += '- [WHO standard 361-acupoint clinical atlas](standard-atlas.md)'
        $BlockLines += '- [Meridian-to-symptom clinical map](by-condition.md)'
        $BlockLines += '- [Special-point clinical network](../meridian-network/special-points/index.md)'
        $BlockLines += ''
        $BlockLines += 'This atlas indexes the existing canonical point pages and does not create a duplicate point system.'
        $BlockLines += $EndMarker

        $Block = $BlockLines -join [Environment]::NewLine

        if ($HubText.Contains($StartMarker) -and $HubText.Contains($EndMarker)) {
            $Pattern = '(?s)' + [regex]::Escape($StartMarker) + '.*?' + [regex]::Escape($EndMarker)
            $HubText = [regex]::Replace($HubText, $Pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $Block })
        }
        else {
            $Heading = [regex]::Match($HubText, '(?m)^#\s+.*$')
            if ($Heading.Success) {
                $InsertAt = $Heading.Index + $Heading.Length
                $HubText = $HubText.Insert(
                    $InsertAt,
                    [Environment]::NewLine + [Environment]::NewLine + $Block + [Environment]::NewLine
                )
            }
            else {
                $HubText = $Block + [Environment]::NewLine + [Environment]::NewLine + $HubText
            }
        }

        Set-Content $Hub $HubText -Encoding UTF8
    }

    $Broken = @()

    foreach ($Row in $Rows) {
        $Target = Join-Path 'docs\acupuncture\points' $Row.FileName
        if (!(Test-Path $Target)) {
            $Broken += $Row.Code
        }
    }

    $CountProblems = @()

    foreach ($Meridian in $Order) {
        $Count = @($Rows | Where-Object { $_.Meridian -eq $Meridian }).Count
        if ($Count -ne $Expected[$Meridian]) {
            $CountProblems += ($Meridian + ':' + $Count)
        }
    }

    $Report = @()
    $Report += '# 43 URL Fix V3 Validation'
    $Report += ''
    $Report += ('- Atlas file exists: ' + (Test-Path $Atlas))
    $Report += ('- Standard acupoints indexed: ' + $Rows.Count + ' / 361')
    $Report += ('- Missing point files: ' + $Broken.Count)
    $Report += ('- Meridian count problems: ' + $CountProblems.Count)
    $Report += ''
    $Report += '## Expected public path'
    $Report += ''
    $Report += '/acupoint-network/standard-atlas/'
    $Report += ''
    $Report += 'The public URL should not end with .md.'
    $Report += ''
    $Report += '## Result'

    if (
        (Test-Path $Atlas) -and
        $Rows.Count -eq 361 -and
        $Broken.Count -eq 0 -and
        $CountProblems.Count -eq 0
    ) {
        $Report += 'PASS'
    }
    else {
        $Report += 'CHECK REQUIRED'
    }

    $Report | Set-Content '_quality_audit_43\43_URL_FIX_V3_REPORT.md' -Encoding UTF8

    $StatusLines = @()
    $StatusLines += 'COMPLETE'
    $StatusLines += 'Atlas: docs/acupoint-network/standard-atlas.md'
    $StatusLines += 'Standard acupoints: 361'
    $StatusLines += ('Missing point files: ' + $Broken.Count)
    $StatusLines += ('Meridian count problems: ' + $CountProblems.Count)
    $StatusLines += 'Expected public path: /acupoint-network/standard-atlas/'
    $StatusLines += 'Report: _quality_audit_43/43_URL_FIX_V3_REPORT.md'
    $StatusLines | Set-Content $Status -Encoding UTF8

    Write-Host ''
    Write-Host 'ACUPOINT ATLAS 43 URL FIX V3 COMPLETE' -ForegroundColor Green
    Write-Host 'Atlas created: docs\acupoint-network\standard-atlas.md' -ForegroundColor Cyan
    Write-Host 'Public path: /acupoint-network/standard-atlas/' -ForegroundColor Cyan
    Write-Host ('Missing point files: ' + $Broken.Count) -ForegroundColor Cyan
    Write-Host ('Meridian count problems: ' + $CountProblems.Count) -ForegroundColor Cyan
}
catch {
    $Failure = @()
    $Failure += 'FAILED'
    $Failure += $_.Exception.Message
    $Failure += ($_ | Out-String)
    $Failure | Set-Content $Status -Encoding UTF8

    Write-Host ''
    Write-Host ('ERROR: ' + $_.Exception.Message) -ForegroundColor Red
    Write-Host 'See APPLY_43_URL_FIX_V3_STATUS.txt' -ForegroundColor Yellow
}

Read-Host 'Press Enter to close'
