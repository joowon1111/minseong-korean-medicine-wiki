$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R

$Out=Join-Path $R "_quality_audit_43"
New-Item -ItemType Directory -Force $Out | Out-Null
$Report=Join-Path $Out "43_VALIDATION_REPORT.md"
$Progress=Join-Path $Out "43_VALIDATION_PROGRESS.txt"
$ErrorFile=Join-Path $Out "43_VALIDATION_ERROR.txt"

"STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Set-Content $Progress -Encoding UTF8
"" | Set-Content $ErrorFile -Encoding UTF8

try {
    if(!(Test-Path "docs\acupuncture\points")){
        throw "docs\acupuncture\points not found"
    }

    $expected=@{
      LU=11; LI=20; ST=45; SP=21; HT=9; SI=19; BL=67;
      KI=27; PC=9; TE=23; GB=44; LR=14; GV=28; CV=24
    }
    $order=@("LU","LI","ST","SP","HT","SI","BL","KI","PC","TE","GB","LR","GV","CV")

    $codes=New-Object System.Collections.Generic.List[string]
    $duplicateMap=@{}
    $files=@(Get-ChildItem "docs\acupuncture\points" -Filter *.md -File)

    Write-Host ("Scanning point pages: "+$files.Count) -ForegroundColor Cyan

    foreach($f in $files){
        $txt=Get-Content $f.FullName -Raw -Encoding UTF8
        $matches=[regex]::Matches($txt,'(?im)^\|\s*WHO 코드\s*\|\s*\*\*([A-Z]{1,2}\d{1,2})\*\*\s*\|')
        foreach($m in $matches){
            $code=$m.Groups[1].Value.ToUpper()
            $codes.Add($code)
            if(!$duplicateMap.ContainsKey($code)){ $duplicateMap[$code]=@() }
            $duplicateMap[$code]+=$f.FullName
        }
    }

    $unique=@($codes | Sort-Object -Unique)
    $standardPattern='^(LU(?:[1-9]|1[01])|LI(?:[1-9]|1\d|20)|ST(?:[1-9]|[1-3]\d|4[0-5])|SP(?:[1-9]|1\d|2[01])|HT[1-9]|SI(?:[1-9]|1\d)|BL(?:[1-9]|[1-5]\d|6[0-7])|KI(?:[1-9]|1\d|2[0-7])|PC[1-9]|TE(?:[1-9]|1\d|2[0-3])|GB(?:[1-9]|[1-3]\d|4[0-4])|LR(?:[1-9]|1[0-4])|GV(?:[1-9]|1\d|2[0-8])|CV(?:[1-9]|1\d|2[0-4]))$'
    $stdCodes=@($unique | Where-Object { $_ -match $standardPattern })

    $expectedCodes=New-Object System.Collections.Generic.List[string]
    foreach($mer in $order){
        for($i=1;$i -le $expected[$mer];$i++){
            $expectedCodes.Add("$mer$i")
        }
    }

    $missing=@($expectedCodes | Where-Object { $_ -notin $stdCodes })
    $unexpected=@($stdCodes | Where-Object { $_ -notin $expectedCodes })
    $duplicates=@()
    foreach($k in $duplicateMap.Keys){
        $arr=@($duplicateMap[$k] | Sort-Object -Unique)
        if($arr.Count -gt 1){
            $duplicates += [PSCustomObject]@{Code=$k;Files=($arr -join "; ")}
        }
    }

    $lines=New-Object System.Collections.Generic.List[string]
    $lines.Add("# 43 표준경혈 통합 검증 보고서")
    $lines.Add("")
    $lines.Add("- 검사한 `docs/acupuncture/points` 문서: **$($files.Count)개**")
    $lines.Add("- 발견한 WHO 표준 코드: **$($stdCodes.Count) / 361**")
    $lines.Add("- 누락 코드: **$($missing.Count)개**")
    $lines.Add("- 예상 밖 표준코드: **$($unexpected.Count)개**")
    $lines.Add("- 중복 코드가 여러 파일에 존재하는 경우: **$($duplicates.Count)개**")
    $lines.Add("")
    $lines.Add("## 경맥별 혈수")
    $lines.Add("")
    $allCountsOK=$true
    foreach($mer in $order){
        $n=@($stdCodes | Where-Object { $_ -match "^$mer\d+$" }).Count
        $exp=$expected[$mer]
        if($n -ne $exp){$allCountsOK=$false}
        $mark=if($n -eq $exp){"PASS"}else{"CHECK"}
        $lines.Add("- **$mer**: $n / $exp — $mark")
    }

    $lines.Add("")
    $lines.Add("## 누락 코드")
    if($missing.Count -eq 0){$lines.Add("- 없음")}
    else{$lines.Add("- "+($missing -join ", "))}

    $lines.Add("")
    $lines.Add("## 예상 밖 코드")
    if($unexpected.Count -eq 0){$lines.Add("- 없음")}
    else{$lines.Add("- "+($unexpected -join ", "))}

    $lines.Add("")
    $lines.Add("## 중복 코드")
    if($duplicates.Count -eq 0){$lines.Add("- 없음")}
    else{
        foreach($d in $duplicates){
            $lines.Add("- **$($d.Code)** — $($d.Files)")
        }
    }

    $lines.Add("")
    $lines.Add("## 최종 판정")
    if($stdCodes.Count -eq 361 -and $missing.Count -eq 0 -and $unexpected.Count -eq 0 -and $allCountsOK){
        $lines.Add("")
        $lines.Add("**PASS — WHO 표준 361혈 코드·경맥별 혈수 검증 완료**")
    } else {
        $lines.Add("")
        $lines.Add("**CHECK REQUIRED — 일부 누락·중복 또는 경맥별 혈수 불일치 확인 필요**")
    }

    $lines | Set-Content $Report -Encoding UTF8
    @(
      "COMPLETE"
      "Standard codes: $($stdCodes.Count) / 361"
      "Missing: $($missing.Count)"
      "Unexpected: $($unexpected.Count)"
      "Duplicate codes: $($duplicates.Count)"
      "Report: _quality_audit_43/43_VALIDATION_REPORT.md"
    ) | Set-Content $Progress -Encoding UTF8

    Write-Host ""
    Write-Host "ACUPOINT ATLAS 43 VALIDATION COMPLETE" -ForegroundColor Green
    Write-Host ("Standard codes: "+$stdCodes.Count+" / 361") -ForegroundColor Cyan
    Write-Host ("Missing: "+$missing.Count) -ForegroundColor Cyan
    Write-Host ("Duplicates: "+$duplicates.Count) -ForegroundColor Cyan
    Write-Host "Created: _quality_audit_43\43_VALIDATION_REPORT.md" -ForegroundColor Yellow
}
catch {
    ($_ | Out-String) | Set-Content $ErrorFile -Encoding UTF8
    "FAILED" | Set-Content $Progress -Encoding UTF8
    Write-Host ("VALIDATION ERROR: "+$_.Exception.Message) -ForegroundColor Red
    Write-Host "See _quality_audit_43\43_VALIDATION_ERROR.txt" -ForegroundColor Yellow
}

Read-Host "Press Enter to close"
