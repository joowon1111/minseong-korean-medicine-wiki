$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "CLASSICS_BACKUP_STEP12"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_CLASSICS_ROLE_STEP12 -->"

$Pairs=@(
@("classics/huangdi-neijing.md","classics-network/huangdi-neijing.md","황제내경",
"원전의 성격·구성·핵심 개념을 소개하는 기본 문서",
"음양·장부·기혈진액·경락·병인병기·진단 등 현대 한의학 지식망으로 연결하는 문서"),
@("classics/shanghanlun.md","classics-network/shanghan-lun.md","상한론",
"원전의 육경변증·방증·처방 체계를 소개하는 기본 문서",
"육경병의 진행·증상·방제·현대 임상 탐색경로를 연결하는 지식망 문서"),
@("classics/jinkui-yaolue.md","classics-network/jingui-yaolue.md","금궤요략",
"잡병·내상·부인과 등 원전의 구성과 주요 병증을 소개하는 기본 문서",
"허로·담음·흉비·복만·부인병 등을 현대 증상·병증·방제로 연결하는 지식망 문서"),
@("classics/donguibogam.md","classics-network/donguibogam.md","동의보감",
"내경·외형·잡병·탕액·침구 등 동의보감의 구성과 원전적 성격을 소개하는 기본 문서",
"동의보감의 편제와 내용을 현대 한의학의 증상·본초·방제·침구 탐색으로 연결하는 문서"),
@("classics/donguisusebowon.md","classics-network/donguisusebowon.md","동의수세보원",
"사상의학 원전의 구성·체질·병증·처방 체계를 소개하는 기본 문서",
"사상체질·소증·표리·순역·중증도·처방·현대 연구를 연결하는 지식망 문서")
)

function AddDesc($text,$desc){
 if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
  $fm=$Matches[1]
  if($fm -match '(?m)^description:\s*.*$'){$fm=[regex]::Replace($fm,'(?m)^description:\s*.*$',"description: $desc",1)}
  else{$fm=$fm.TrimEnd()+"`r`ndescription: $desc"}
  return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
 }
 return "---`r`ndescription: $desc`r`n---`r`n"+$text
}
function RelLink($from,$to){
 return [IO.Path]::GetRelativePath((Split-Path $from -Parent),$to).Replace('\','/')
}
function Backup($p,$rel){
 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force
}

$changed=0
foreach($x in $Pairs){
 $basicRel=$x[0]; $netRel=$x[1]; $name=$x[2]; $basicRole=$x[3]; $netRole=$x[4]
 $basic=Join-Path $Docs $basicRel
 $net=Join-Path $Docs $netRel

 if(Test-Path $basic){
  $text=Get-Content $basic -Raw -Encoding UTF8
  if(-not $text.Contains($Marker)){
   Backup $basic $basicRel
   $text=AddDesc $text "$name — $basicRole."
   $block="`r`n`r`n$Marker`r`n## 이 문서의 역할`r`n`r`n이 문서는 **$basicRole**입니다. 원전의 내용을 현대 임상 개념과 동일시하지 않고, 먼저 문헌의 구성과 전통적 맥락을 이해하는 출발점으로 사용합니다.`r`n"
   if(Test-Path $net){$block+="`r`n현대 한의학 지식과의 연결은 [$name 현대 지식망]($(RelLink $basic $net))에서 이어서 볼 수 있습니다.`r`n"}
   Set-Content $basic ($text.TrimEnd()+$block) -Encoding UTF8
   Write-Host "CLASSIC BASIC: $basicRel" -ForegroundColor Green
   $changed++
  }
 }
 if(Test-Path $net){
  $text=Get-Content $net -Raw -Encoding UTF8
  if(-not $text.Contains($Marker)){
   Backup $net $netRel
   $text=AddDesc $text "$name — $netRole."
   $block="`r`n`r`n$Marker`r`n## 이 문서의 역할`r`n`r`n이 문서는 **$netRole**입니다. 원전의 전통적 설명과 현대 연구·임상 해석을 구분하면서 관련 증상·병증·방제·본초·침구 문서로 확장합니다.`r`n"
   if(Test-Path $basic){$block+="`r`n원전의 기본 구성과 문헌적 맥락은 [$name 원전·기본 문서]($(RelLink $net $basic))에서 먼저 볼 수 있습니다.`r`n"}
   Set-Content $net ($text.TrimEnd()+$block) -Encoding UTF8
   Write-Host "CLASSIC NETWORK: $netRel" -ForegroundColor Cyan
   $changed++
  }
 }
}

# Bangyakhappyeon has no exact duplicate pair in audit, so strengthen its own network role.
$Bang=@(
@("bangyakhappyeon-network/integrated-map.md","방약합편 → 현대 한의학 통합 지도"),
@("bangyakhappyeon-network/clinical-navigation.md","방약합편 처방 탐색법"),
@("bangyakhappyeon-network/what-is-bangyakhappyeon.md","방약합편이란?"),
@("bangyakhappyeon-network/boncho-yakseongga.md","손익본초와 약성가"),
@("bangyakhappyeon-network/seven-formulas-ten-agents.md","칠방·십제"),
@("bangyakhappyeon-network/sang-jung-ha.md","상통·중통·하통")
)
foreach($x in $Bang){
 $rel=$x[0]; $p=Join-Path $Docs $rel
 if(-not(Test-Path $p)){continue}
 $text=Get-Content $p -Raw -Encoding UTF8
 if($text.Contains($Marker)){continue}
 Backup $p $rel
 $text=AddDesc $text "$($x[1]) — 방약합편의 처방 분류·본초·임상 탐색 구조를 현대 한의학 지식망과 연결하는 문서입니다."
 $block="`r`n`r`n$Marker`r`n## 방약합편 지식망에서의 위치`r`n`r`n방약합편의 처방·본초 정보를 단순 목록으로 보지 않고 **증상 → 병증·치법 → 처방 → 구성 본초 → 현대 임상 자료**로 연결해 탐색합니다.`r`n`r`n"
 $targets=@(
  @("방제 찾기","herbal-integrated/formulas.md"),
  @("본초 찾기","herbal-integrated/herbs.md"),
  @("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md"),
  @("한의학 고전 비교","classics-network/comparison.md")
 )
 $block+="## 관련 핵심 문서`r`n`r`n"
 foreach($t in $targets){
  $dest=Join-Path $Docs $t[1]
  if(Test-Path $dest){$block+="- [$($t[0])]($(RelLink $p $dest))`r`n"}
 }
 Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
 Write-Host "BANGYAKHAPPYEON: $rel" -ForegroundColor Green
 $changed++
}

Write-Host ""
Write-Host "STEP 12 완료: $changed 개 고전·지식망 문서 역할 보강" -ForegroundColor Cyan
Write-Host "원본 백업: CLASSICS_BACKUP_STEP12"
Read-Host "Enter를 누르면 종료합니다"
