$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Status = Join-Path $Root "APPLY_43_URL_FIX_V2_STATUS.txt"

try {
    "STARTED" | Set-Content $Status -Encoding UTF8

    if (!(Test-Path "docs")) {
        throw "docs folder not found"
    }
    if (!(Test-Path "docs\acupuncture\points")) {
        throw "docs\acupuncture\points folder not found"
    }

    $Backup = "_backup_acupoint43_urlfix_v2_" + (Get-Date -Format "yyyyMMdd-HHmmss")
    New-Item -ItemType Directory -Force $Backup | Out-Null
    New-Item -ItemType Directory -Force "docs\acupoint-network" | Out-Null
    New-Item -ItemType Directory -Force "_quality_audit_43" | Out-Null

    $Expected = @{
        LU=11; LI=20; ST=45; SP=21; HT=9; SI=19; BL=67
        KI=27; PC=9; TE=23; GB=44; LR=14; GV=28; CV=24
    }
    $Order = @("LU","LI","ST","SP","HT","SI","BL","KI","PC","TE","GB","LR","GV","CV")

    $Rows = @()
    foreach ($File in Get-ChildItem "docs\acupuncture\points" -File -Filter *.md) {
        $Text = Get-Content $File.FullName -Raw -Encoding UTF8
        $Match = [regex]::Match($Text, '(?im)^\|\s*WHO\s+.*?\|\s*\*\*([A-Z]{1,2}\d{1,2})\*\*\s*\|')
        if (!$Match.Success) {
            $Match = [regex]::Match($Text, '(?im)\*\*((?:LU|LI|ST|SP|HT|SI|BL|KI|PC|TE|GB|LR|GV|CV)\d{1,2})\*\*')
        }
        if (!$Match.Success) { continue }

        $Code = $Match.Groups[1].Value.ToUpper()
        $Meridian = [regex]::Match($Code, '^[A-Z]+').Value
        if (!($Order -contains $Meridian)) { continue }

        $Heading = [regex]::Match($Text, '(?m)^#\s+(.+)$')
        if ($Heading.Success) { $Title = $Heading.Groups[1].Value.Trim() }
        else { $Title = $Code }

        $Rows += [PSCustomObject]@{
            Code=$Code
            Meridian=$Meridian
            Title=$Title
            Path=$File.FullName
        }
    }

    $Rows = @($Rows | Sort-Object Code -Unique)
    if ($Rows.Count -ne 361) {
        throw ("Expected 361 standard acupoints but found " + $Rows.Count)
    }

    function PointNumber([string]$Code) {
        return [int]([regex]::Match($Code, '\d+').Value)
    }

    function RelativePath([string]$FromFile, [string]$ToFile) {
        $FromFull = [IO.Path]::GetFullPath((Join-Path $Root $FromFile))
        $ToFull = [IO.Path]::GetFullPath($ToFile)
        $FromDir = [IO.Path]::GetDirectoryName($FromFull)
        $BaseUri = New-Object System.Uri(($FromDir.TrimEnd('\') + '\'))
        $TargetUri = New-Object System.Uri($ToFull)
        return [Uri]::UnescapeDataString($BaseUri.MakeRelativeUri($TargetUri).ToString())
    }

    $Atlas = "docs\acupoint-network\standard-atlas.md"
    if (Test-Path $Atlas) {
        Copy-Item $Atlas (Join-Path $Backup "standard-atlas.md") -Force
    }

    $Lines = New-Object System.Collections.Generic.List[string]
    $Lines.Add("---")
    $Lines.Add("title: WHO Standard 361 Acupoint Clinical Atlas")
    $Lines.Add("description: Standard 361 acupoints integrated with the existing Minseong meridian and clinical acupoint network.")
    $Lines.Add("status: reviewed")
    $Lines.Add("last_reviewed: 2026-08-22")
    $Lines.Add("---")
    $Lines.Add("# WHO Standard 361 Acupoint Clinical Atlas")
    $Lines.Add("")
    $Lines.Add("This hub indexes the existing canonical acupoint pages by the WHO standard 361-point system.")
    $Lines.Add("")

    foreach ($Meridian in $Order) {
        $MeridianRows = @($Rows | Where-Object { $_.Meridian -eq $Meridian } | Sort-Object @{Expression={PointNumber $_.Code}})
        $Lines.Add("## " + $Meridian + " - " + $MeridianRows.Count + " points")
        $Parts = @()
        foreach ($Row in $MeridianRows) {
            $Rel = RelativePath "docs\acupoint-network\standard-atlas.md" $Row.Path
            $Parts += ("[" + $Row.Title + "](" + $Rel + ")")
        }
        $Lines.Add(($Parts -join " | "))
        $Lines.Add("")
    }

    $Lines.Add("## Related knowledge networks")
    $Lines.Add("")
    $Lines.Add("- [Clinical acupoint network](index.md)")
    $Lines.Add("- [Meridian-to-symptom map](by-condition.md)")
    $Lines.Add("- [Meridian network](../meridian-network/index.md)")
    $Lines.Add("- [Special-point network](../meridian-network/special-points/index.md)")
    $Lines.Add("- [Clinical point combinations](../network/acupoint-combinations.md)")
    $Lines | Set-Content $Atlas -Encoding UTF8

    # Integrate link into existing hub using an ASCII-only managed block.
    $Hub = "docs\acupoint-network\index.md"
    if (Test-Path $Hub) {
        Copy-Item $Hub (Join-Path $Backup "acupoint-network-index.md") -Force
        $HubText = Get-Content $Hub -Raw -Encoding UTF8
        $Block = @'
<!-- MS_43_URL_FIX_V2_START -->
## WHO standard 361-acupoint atlas

- [WHO standard 361-acupoint clinical atlas](standard-atlas.md)
- [Meridian-to-symptom clinical map](by-condition.md)
- [Special-point clinical network](../meridian-network/special-points/index.md)

The atlas is an index into the existing canonical point pages. It does not create a competing duplicate acupoint system.
<!-- MS_43_URL_FIX_V2_END -->
'@
        if ($HubText -match '(?s)<!-- MS_43_URL_FIX_V2_START -->.*?<!-- MS_43_URL_FIX_V2_END -->') {
            $HubText = [regex]::Replace($HubText, '(?s)<!-- MS_43_URL_FIX_V2_START -->.*?<!-- MS_43_URL_FIX_V2_END -->', $Block)
        } else {
            $H = [regex]::Match($HubText, '(?m)^#\s+.*$')
            if ($H.Success) {
                $HubText = $HubText.Insert($H.Index + $H.Length, "`r`n`r`n" + $Block + "`r`n")
            } else {
                $HubText = $Block + "`r`n`r`n" + $HubText
            }
        }
        Set-Content $Hub $HubText -Encoding UTF8
    }

    # Validate all atlas relative links.
    $AtlasText = Get-Content $Atlas -Raw -Encoding UTF8
    $LinkMatches = [regex]::Matches($AtlasText, '\[[^\]]+\]\(([^)]+)\)')
    $Broken = @()
    foreach ($M in $LinkMatches) {
        $Href = $M.Groups[1].Value
        if ($Href -match '^(https?://|#)') { continue }
        $Target = ($Href -split '#')[0]
        $Destination = Join-Path (Split-Path $Atlas -Parent) $Target
        if (!(Test-Path $Destination)) {
            $Broken += $Href
        }
    }

    $Report = New-Object System.Collections.Generic.List[string]
    $Report.Add("# 43 URL Fix V2 Validation")
    $Report.Add("")
    $Report.Add("- Atlas file exists: **" + (Test-Path $Atlas) + "**")
    $Report.Add("- Standard acupoints indexed: **" + $Rows.Count + " / 361**")
    $Report.Add("- Atlas links checked: **" + $LinkMatches.Count + "**")
    $Report.Add("- Broken relative links: **" + $Broken.Count + "**")
    $Report.Add("")
    $Report.Add("## Expected public path")
    $Report.Add("")
    $Report.Add("`/acupoint-network/standard-atlas/`")
    $Report.Add("")
    $Report.Add("Do not add `.md` to the public URL.")
    $Report.Add("")
    $Report.Add("## Result")
    if ((Test-Path $Atlas) -and $Rows.Count -eq 361 -and $Broken.Count -eq 0) {
        $Report.Add("**PASS**")
    } else {
        $Report.Add("**CHECK REQUIRED**")
    }
    $Report | Set-Content "_quality_audit_43\43_URL_FIX_V2_REPORT.md" -Encoding UTF8

    @(
        "COMPLETE",
        "Atlas: docs/acupoint-network/standard-atlas.md",
        "Standard acupoints: 361",
        "Broken links: " + $Broken.Count,
        "Expected public path: /acupoint-network/standard-atlas/",
        "Report: _quality_audit_43/43_URL_FIX_V2_REPORT.md"
    ) | Set-Content $Status -Encoding UTF8

    Write-Host ""
    Write-Host "ACUPOINT ATLAS 43 URL FIX V2 COMPLETE" -ForegroundColor Green
    Write-Host "Atlas: docs\acupoint-network\standard-atlas.md" -ForegroundColor Cyan
    Write-Host "Public path: /acupoint-network/standard-atlas/" -ForegroundColor Cyan
    Write-Host ("Broken links: " + $Broken.Count) -ForegroundColor Cyan
}
catch {
    ("FAILED`r`n" + ($_ | Out-String)) | Set-Content $Status -Encoding UTF8
    Write-Host ""
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host "See APPLY_43_URL_FIX_V2_STATUS.txt" -ForegroundColor Yellow
}

Read-Host "Press Enter to close"
