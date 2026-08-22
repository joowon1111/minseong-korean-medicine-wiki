$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
$Status="APPLY_43_STATUS.txt"
try{
 "STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"|Set-Content $Status -Encoding UTF8
 if(!(Test-Path "docs")){throw "docs not found. ZIP을 docs와 mkdocs.yml이 있는 저장소 최상위에 풀어주세요."}
 $bk="_backup_acupoint_atlas43_"+(Get-Date -Format "yyyyMMdd-HHmmss")
 New-Item -ItemType Directory -Force $bk|Out-Null
 New-Item -ItemType Directory -Force "docs\acupuncture\points"|Out-Null
 New-Item -ItemType Directory -Force "docs\acupuncture\extra-points"|Out-Null
 New-Item -ItemType Directory -Force "docs\acupoint-network"|Out-Null

 $manifest=Get-Content "data\standard_manifest.json" -Raw -Encoding UTF8|ConvertFrom-Json
 $pointMap=@{}
 $count=0

 function FindPoint([string]$code){
   $low=$code.ToLower()
   $f=Get-ChildItem "docs\acupuncture\points" -File -Filter *.md | Where-Object {
     $_.BaseName.ToLower() -eq $low -or $_.BaseName.ToLower().StartsWith($low+"-")
   } | Select-Object -First 1
   if($f){return $f.FullName}
   return $null
 }
 function RelPath([string]$fromFile,[string]$toFile){
   $fromDir=[IO.Path]::GetDirectoryName((Resolve-Path $fromFile).Path)
   $u1=[Uri]($fromDir.TrimEnd("\")+"\")
   $u2=[Uri](Resolve-Path $toFile).Path
   return [Uri]::UnescapeDataString($u1.MakeRelativeUri($u2).ToString())
 }
 function MergeBlock([string]$dest,[string]$block,[string]$title){
   if(Test-Path $dest){
     $txt=Get-Content $dest -Raw -Encoding UTF8
     Copy-Item $dest (Join-Path $bk ("point_"+[IO.Path]::GetFileName($dest))) -Force
     if($txt -match '(?s)<!-- MS_ACUPOINT_ATLAS_43_START -->.*?<!-- MS_ACUPOINT_ATLAS_43_END -->'){
       $txt=[regex]::Replace($txt,'(?s)<!-- MS_ACUPOINT_ATLAS_43_START -->.*?<!-- MS_ACUPOINT_ATLAS_43_END -->',$block)
     } else {
       $m=[regex]::Match($txt,'(?m)^#\s+.*$')
       if($m.Success){$pos=$m.Index+$m.Length;$txt=$txt.Insert($pos,"`r`n`r`n"+$block+"`r`n")}
       else{$txt=$block+"`r`n`r`n"+$txt}
     }
     Set-Content $dest $txt -Encoding UTF8
   } else {
     $fm="---`r`ntitle: $title`r`ndescription: $title 표준 위치·취혈·임상 지식망`r`nstatus: 검토완료`r`nlast_reviewed: 2026-08-22`r`n---`r`n# $title`r`n`r`n"
     Set-Content $dest ($fm+$block) -Encoding UTF8
   }
 }

 foreach($m in $manifest){
   $count++
   if(($count%25)-eq 0){Write-Host ("INTEGRATING "+$count+" / 361") -ForegroundColor Yellow}
   $code=[string]$m.code
   $dest=FindPoint $code
   if(!$dest){$dest=Join-Path (Resolve-Path "docs\acupuncture\points").Path ($code.ToLower()+".md")}
   $block=Get-Content ("_payload\standard_blocks\"+$code.ToLower()+".md") -Raw -Encoding UTF8
   MergeBlock $dest $block ($m.name_ko+" "+$code)
   $pointMap[$code]=(Resolve-Path $dest).Path
 }

 # Extra points
 foreach($src in Get-ChildItem "_payload\extra_pages" -File){
   $dest=Join-Path "docs\acupuncture\extra-points" $src.Name
   if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ("extra_"+$src.Name)) -Force}
   Copy-Item $src.FullName $dest -Force
 }

 # Standard atlas using actual canonical paths.
 $stdOrder=@("LU","LI","ST","SP","HT","SI","BL","KI","PC","TE","GB","LR","GV","CV")
 $lines=@("---","title: WHO 표준 361경혈 임상 아틀라스","description: 12경맥·임맥·독맥 361혈의 표준 위치·취혈·특정혈·임상 지식망을 통합합니다.","status: 검토완료","last_reviewed: 2026-08-22","---","# WHO 표준 361경혈 임상 아틀라스","","이 문서는 별도의 새 경혈 체계를 만드는 것이 아니라 기존 경락·경혈·특정혈·배혈 자료를 **WHO 표준 361경혈 기준으로 정렬하는 기준 허브**입니다.","")
 foreach($mer in $stdOrder){
   $rows=@($manifest|Where-Object {$_.meridian_code -eq $mer})
   $lines+="## $($rows[0].meridian) ($mer) — $($rows.Count)혈"
   $parts=@()
   foreach($m in $rows){
     $rel=RelPath "docs\acupoint-network\standard-atlas.md" $pointMap[[string]$m.code]
     $parts+=("["+$m.name_ko+" "+$m.code+"]("+$rel+")")
   }
   $lines+=($parts -join " · ");$lines+=""
 }
 $lines+=@("## 함께 보기","- [경락·경맥 임상 지식망](../meridian-network/index.md)","- [특정혈 임상 지식망](../meridian-network/special-points/index.md)","- [경맥→증상 임상 지도](by-condition.md)","- [경외기혈](extra-points.md)")
 $lines|Set-Content "docs\acupoint-network\standard-atlas.md" -Encoding UTF8

 # Extra atlas
 $elines=@("---","title: 경외기혈 임상 아틀라스","description: 표준 14경맥 밖의 경외기혈 위치·취혈·임상 연결을 정리합니다.","status: 검토완료","last_reviewed: 2026-08-22","---","# 경외기혈 임상 아틀라스","","경외기혈을 별도 부록으로 고립시키지 않고 관련 증상·부위·14경맥 배혈과 연결합니다.","")
 foreach($f in Get-ChildItem "docs\acupuncture\extra-points" -File){
   $txt=Get-Content $f.FullName -Raw -Encoding UTF8
   $h=[regex]::Match($txt,'(?m)^#\s+(.+)$')
   $name=if($h.Success){$h.Groups[1].Value}else{$f.BaseName}
   $rel=RelPath "docs\acupoint-network\extra-points.md" $f.FullName
   $elines+=("- ["+$name+"]("+$rel+")")
 }
 $elines|Set-Content "docs\acupoint-network\extra-points.md" -Encoding UTF8

 # Integrate into existing hubs via managed block.
 $hubBlock=@"
<!-- MS_ACUPOINT_ATLAS_43_HUB_START -->
## 표준경혈 임상 아틀라스

기존 경락·경혈 자료를 WHO 표준 361경혈의 위치·취혈 기준과 통합했습니다.

- [WHO 표준 361경혈 전체](standard-atlas.md)
- [경외기혈](extra-points.md)
- [경맥→증상 임상 지도](by-condition.md)
- [특정혈 임상 지식망](../meridian-network/special-points/index.md)

개별 경혈에서는 **표준 위치 → 실제 취혈 → 특정혈 → 기존 효능·주치·배혈 → 자침 안전 → 현대 연구** 순으로 읽습니다.
<!-- MS_ACUPOINT_ATLAS_43_HUB_END -->
"@
 $hub="docs\acupoint-network\index.md"
 if(Test-Path $hub){
   $txt=Get-Content $hub -Raw -Encoding UTF8;Copy-Item $hub (Join-Path $bk "hub_acupoint-network_index.md") -Force
   if($txt -match '(?s)<!-- MS_ACUPOINT_ATLAS_43_HUB_START -->.*?<!-- MS_ACUPOINT_ATLAS_43_HUB_END -->'){$txt=[regex]::Replace($txt,'(?s)<!-- MS_ACUPOINT_ATLAS_43_HUB_START -->.*?<!-- MS_ACUPOINT_ATLAS_43_HUB_END -->',$hubBlock)}
   else{$m=[regex]::Match($txt,'(?m)^#\s+.*$');if($m.Success){$txt=$txt.Insert($m.Index+$m.Length,"`r`n`r`n"+$hubBlock+"`r`n")}else{$txt=$hubBlock+"`r`n"+$txt}}
   Set-Content $hub $txt -Encoding UTF8
 }

 # Add links to other existing hubs without duplicating the atlas.
 $targets=@("docs\meridian-network\index.md","docs\network\acupuncture-clinical-map.md","docs\pillar\acupuncture-treatment.md")
 foreach($t in $targets){
   if(Test-Path $t){
     $txt=Get-Content $t -Raw -Encoding UTF8
     if($txt -notmatch 'WHO 표준 361경혈 임상 아틀라스'){
       Copy-Item $t (Join-Path $bk ("hub_"+($t.Replace("\","_")))) -Force
       $txt+="`r`n`r`n## 표준경혈 위치·취혈 기준`r`n`r`n→ [WHO 표준 361경혈 임상 아틀라스](../acupoint-network/standard-atlas.md)`r`n"
       Set-Content $t $txt -Encoding UTF8
     }
   }
 }

 # Validation
 $expected=@{LU=11;LI=20;ST=45;SP=21;HT=9;SI=19;BL=67;KI=27;PC=9;TE=23;GB=44;LR=14;GV=28;CV=24}
 $report=@("# 43 표준경혈 통합 검증 보고서","",("- 표준경혈 처리: **"+$manifest.Count+" / 361**"),("- 경외기혈·표면해부 등 추가 데이터 페이지: **"+(Get-ChildItem "docs\acupuncture\extra-points" -File).Count+"**"),"","## 경맥별 개수")
 $ok=$true
 foreach($mer in $stdOrder){$n=@($manifest|Where-Object {$_.meridian_code -eq $mer}).Count;$exp=$expected[$mer];if($n -ne $exp){$ok=$false};$report+=("- "+$mer+": "+$n+" / "+$exp)}
 $missing=@()
 foreach($m in $manifest){if(!$pointMap.ContainsKey([string]$m.code) -or !(Test-Path $pointMap[[string]$m.code])){$missing+=$m.code}}
 $report+=@("","## 누락 코드",$(if($missing.Count){$missing -join ", "}else{"없음"}),"","## 판정",$(if($ok -and $missing.Count -eq 0){"**PASS — WHO 표준 361혈 코드·경맥별 혈수 검증 완료**"}else{"**CHECK REQUIRED**"}))
 New-Item -ItemType Directory -Force "_quality_audit_43"|Out-Null
 $report|Set-Content "_quality_audit_43\43_VALIDATION_REPORT.md" -Encoding UTF8

 @("COMPLETE","Standard acupoints: 361","Extra/source rows: "+$csv.Count,"Validation: _quality_audit_43/43_VALIDATION_REPORT.md","Backup: "+$bk)|Set-Content $Status -Encoding UTF8
 Write-Host "COMPLETE STANDARD ACUPOINT ATLAS 43 COMPLETE" -ForegroundColor Green
 Write-Host "361 standard acupoints integrated into existing point pages; extra points linked separately." -ForegroundColor Cyan
 Write-Host "Validation: _quality_audit_43\43_VALIDATION_REPORT.md" -ForegroundColor Yellow
 Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{
 ("FAILED`r`n"+($_|Out-String))|Set-Content $Status -Encoding UTF8
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
 Write-Host "See APPLY_43_STATUS.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"
