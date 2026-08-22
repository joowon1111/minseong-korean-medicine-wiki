$ErrorActionPreference="Stop"
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
$Status="APPLY_43_URL_FIX_STATUS.txt"

try{
 "STARTED $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"|Set-Content $Status -Encoding UTF8
 if(!(Test-Path "docs")){throw "docs not found. ZIP을 docs와 mkdocs.yml이 있는 저장소 최상위에 풀어주세요."}

 $bk="_backup_acupoint43_urlfix_"+(Get-Date -Format "yyyyMMdd-HHmmss")
 New-Item -ItemType Directory -Force $bk|Out-Null
 New-Item -ItemType Directory -Force "docs\acupoint-network"|Out-Null

 # 1. standard-atlas.md: if missing, reconstruct from the 361 integrated point pages.
 $atlas="docs\acupoint-network\standard-atlas.md"
 if(Test-Path $atlas){Copy-Item $atlas (Join-Path $bk "standard-atlas.md") -Force}

 $expected=@{LU=11;LI=20;ST=45;SP=21;HT=9;SI=19;BL=67;KI=27;PC=9;TE=23;GB=44;LR=14;GV=28;CV=24}
 $order=@("LU","LI","ST","SP","HT","SI","BL","KI","PC","TE","GB","LR","GV","CV")
 $pointRows=@()

 foreach($f in Get-ChildItem "docs\acupuncture\points" -Filter *.md -File){
   $txt=Get-Content $f.FullName -Raw -Encoding UTF8
   $m=[regex]::Match($txt,'(?im)^\|\s*WHO 코드\s*\|\s*\*\*([A-Z]{1,2}\d{1,2})\*\*\s*\|')
   if(!$m.Success){continue}
   $code=$m.Groups[1].Value.ToUpper()
   $nm=[regex]::Match($txt,'(?m)^#\s+(.+)$')
   $title=if($nm.Success){$nm.Groups[1].Value}else{$code}
   $mer=[regex]::Match($code,'^[A-Z]+').Value
   if($order -contains $mer){
     $pointRows += [PSCustomObject]@{Code=$code;Meridian=$mer;Title=$title;Path=$f.FullName}
   }
 }
 $unique=@($pointRows|Sort-Object Code -Unique)
 if($unique.Count -ne 361){throw "Expected 361 standard point pages, found $($unique.Count). Run 43 validation first."}

 function Num([string]$c){return [int]([regex]::Match($c,'\d+').Value)}
 function Relative([string]$from,[string]$to){
   $fromFull=[IO.Path]::GetFullPath((Join-Path $R $from))
   $toFull=[IO.Path]::GetFullPath($to)
   $fromDir=[IO.Path]::GetDirectoryName($fromFull)
   $u1=[Uri]($fromDir.TrimEnd("\")+"\")
   $u2=[Uri]$toFull
   return [Uri]::UnescapeDataString($u1.MakeRelativeUri($u2).ToString())
 }

 $lines=@(
"---",
"title: WHO 표준 361경혈 임상 아틀라스",
"description: 12경맥·임맥·독맥 361혈의 표준 위치·취혈·특정혈·임상 지식망을 기존 경혈 체계 안에서 탐색합니다.",
"status: 검토완료",
"last_reviewed: 2026-08-22",
"---",
"# WHO 표준 361경혈 임상 아틀라스",
"",
"이 페이지는 새로운 별도 경혈 체계를 만드는 것이 아니라, 기존 개별 경혈·경맥·특정혈·배혈 문서를 **WHO 표준 361경혈 기준으로 한곳에서 탐색하는 기준 허브**입니다.",
"",
"## 경맥별 전체 경혈"
 )
 foreach($mer in $order){
   $rows=@($unique|Where-Object {$_.Meridian -eq $mer}|Sort-Object @{Expression={Num $_.Code}})
   $lines+=""
   $lines+="### $mer — $($rows.Count)혈"
   $parts=@()
   foreach($x in $rows){
     $rel=Relative "docs\acupoint-network\standard-atlas.md" $x.Path
     $parts+=("["+$x.Title+"]("+$rel+")")
   }
   $lines+=($parts -join " · ")
 }
 $lines+=@(
"",
"## 관련 지식망",
"",
"- [경혈 임상 지식망](index.md)",
"- [경맥→증상 임상 지도](by-condition.md)",
"- [경락·경맥 임상 지식망](../meridian-network/index.md)",
"- [특정혈 임상 지식망](../meridian-network/special-points/index.md)",
"- [임상 핵심 배혈](../network/acupoint-combinations.md)"
 )
 $lines|Set-Content $atlas -Encoding UTF8

 # 2. Integrate atlas into acupoint-network index without appending duplicate blocks.
 $hub="docs\acupoint-network\index.md"
 if(Test-Path $hub){
   Copy-Item $hub (Join-Path $bk "acupoint-network-index.md") -Force
   $txt=Get-Content $hub -Raw -Encoding UTF8
   $block=@"
<!-- MS_43_URL_FIX_START -->
## WHO 표준경혈 전체 탐색

- [WHO 표준 361경혈 임상 아틀라스](standard-atlas.md)
- [경맥→증상 임상 지도](by-condition.md)
- [특정혈 임상 지식망](../meridian-network/special-points/index.md)

개별 경혈의 기존 임상 내용에 표준 위치·취혈·자침 안전 정보를 통합해 두었으며, 이 허브에서 361혈 전체를 경맥별로 탐색할 수 있습니다.
<!-- MS_43_URL_FIX_END -->
"@
   if($txt -match '(?s)<!-- MS_43_URL_FIX_START -->.*?<!-- MS_43_URL_FIX_END -->'){
      $txt=[regex]::Replace($txt,'(?s)<!-- MS_43_URL_FIX_START -->.*?<!-- MS_43_URL_FIX_END -->',$block)
   } else {
      $m=[regex]::Match($txt,'(?m)^#\s+.*$')
      if($m.Success){$txt=$txt.Insert($m.Index+$m.Length,"`r`n`r`n"+$block+"`r`n")}
      else{$txt=$block+"`r`n`r`n"+$txt}
   }
   Set-Content $hub $txt -Encoding UTF8
 }

 # 3. Fix accidental links containing acupuncture/acupoint-network or .md public-style paths.
 $changed=0
 foreach($f in Get-ChildItem "docs" -Recurse -Filter *.md -File){
   $txt=Get-Content $f.FullName -Raw -Encoding UTF8
   $old=$txt
   $txt=$txt.Replace("/acupuncture/acupoint-network/standard-atlas.md","/acupoint-network/standard-atlas/")
   $txt=$txt.Replace("/acupuncture/acupoint-network/standard-atlas/","/acupoint-network/standard-atlas/")
   if($txt -ne $old){
      Copy-Item $f.FullName (Join-Path $bk ("link_"+($f.FullName.Substring((Resolve-Path "docs").Path.Length+1).Replace("\","_")))) -Force
      Set-Content $f.FullName $txt -Encoding UTF8
      $changed++
   }
 }

 # 4. Local existence + 361 link validation.
 $atlasTxt=Get-Content $atlas -Raw -Encoding UTF8
 $atlasLinks=[regex]::Matches($atlasTxt,'\[[^\]]+\]\(([^)]+)\)')
 $broken=@()
 foreach($m in $atlasLinks){
   $href=$m.Groups[1].Value
   if($href -match '^(https?://|#)'){continue}
   $target=($href -split '#')[0]
   $dest=Join-Path (Split-Path $atlas -Parent) $target
   if(!(Test-Path $dest)){$broken+=$href}
 }
 $report=@(
"# 43 URL·허브 검증 보고서",
"",
"- `docs/acupoint-network/standard-atlas.md` 존재: **$(Test-Path $atlas)**",
"- 아틀라스 내 링크 수: **$($atlasLinks.Count)**",
"- 깨진 상대링크: **$($broken.Count)**",
"- 잘못된 `/acupuncture/acupoint-network/...` 링크 수정 문서: **$changed개**",
"",
"## 예상 공개 URL",
"",
"`https://wiki.minseong.co.kr/acupoint-network/standard-atlas/`",
"",
"`.md`를 공개 URL 끝에 붙이지 않습니다.",
"",
"## 판정",
$(if((Test-Path $atlas) -and $broken.Count -eq 0){"**PASS — standard-atlas 허브 파일 및 내부링크 검증 완료**"}else{"**CHECK REQUIRED**"})
 )
 New-Item -ItemType Directory -Force "_quality_audit_43"|Out-Null
 $report|Set-Content "_quality_audit_43\43_URL_FIX_REPORT.md" -Encoding UTF8

 @(
 "COMPLETE",
 "Atlas: docs/acupoint-network/standard-atlas.md",
 "Expected public URL: https://wiki.minseong.co.kr/acupoint-network/standard-atlas/",
 "Broken atlas links: $($broken.Count)",
 "Report: _quality_audit_43/43_URL_FIX_REPORT.md",
 "Backup: $bk"
 )|Set-Content $Status -Encoding UTF8

 Write-Host "ACUPOINT ATLAS 43 URL FIX COMPLETE" -ForegroundColor Green
 Write-Host "Canonical public path: /acupoint-network/standard-atlas/" -ForegroundColor Cyan
 Write-Host ("Broken atlas links: "+$broken.Count) -ForegroundColor Cyan
 Write-Host "Report: _quality_audit_43\43_URL_FIX_REPORT.md" -ForegroundColor Yellow
}catch{
 ("FAILED`r`n"+($_|Out-String))|Set-Content $Status -Encoding UTF8
 Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
 Write-Host "See APPLY_43_URL_FIX_STATUS.txt" -ForegroundColor Yellow
}
Read-Host "Press Enter to close"
