$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "HIGH_VALUE_BACKUP_STEP8"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_HIGH_VALUE_REPAIR_STEP8 -->"

$Groups=@(
@{Files=@("tonic-masterpieces/deer-antler/index.md","tonic-masterpieces/deer-antler/clinical-map.md","tonic-masterpieces/deer-antler/quality-parts.md","tonic-masterpieces/deer-antler/research.md");
Desc="녹용의 본초학·품질·임상 활용·현대 연구를 기력저하·허약·회복기와 맞춤한약 지식으로 연결하는 심화 문서입니다.";
Links=@(@("녹용보약 환자 안내","conditions/deer-antler-tonic-guide.md"),@("맞춤한약","conditions/custom-herbal-medicine.md"),@("기력회복·허약","conditions/energy-recovery.md"),@("피로·기력회복 본초 찾기","herbal-integrated/herbs-for-fatigue.md"))},
@{Files=@("tonic-masterpieces/gongjindan/index.md","tonic-masterpieces/gongjindan/clinical-map.md","tonic-masterpieces/gongjindan/composition.md");
Desc="공진단의 구성·방의·기력·회복 관련 임상 활용을 맞춤 한약과 본초·방제 지식으로 연결하는 심화 문서입니다.";
Links=@(@("공진단 환자 안내","conditions/gongjin-dan-guide.md"),@("맞춤한약","conditions/custom-herbal-medicine.md"),@("기력회복·허약","conditions/energy-recovery.md"),@("본초·방제 한눈에 보기","herbal-integrated/index.md"))},
@{Files=@("tonic-masterpieces/gyeongokgo/index.md","tonic-masterpieces/gyeongokgo/clinical-map.md","tonic-masterpieces/gyeongokgo/composition.md","tonic-masterpieces/gyeongokgo/fatigue-recovery.md");
Desc="경옥고의 구성·방의·피로·허약·회복 관련 활용과 현대 연구를 연결하는 심화 문서입니다.";
Links=@(@("경옥고 환자 안내","conditions/gyeongokgo-guide.md"),@("맞춤한약","conditions/custom-herbal-medicine.md"),@("기력회복·허약","conditions/energy-recovery.md"),@("보익·회복 핵심","herbal-integrated/tonic-recovery.md"))},
@{Files=@("tonic-masterpieces/comparison.md","tonic-masterpieces/selection-followup.md");
Desc="녹용·공진단·경옥고를 단순 우열이 아니라 환자 상태·처방구조·치료목표·경과평가 관점에서 비교하는 문서입니다.";
Links=@(@("맞춤한약","conditions/custom-herbal-medicine.md"),@("녹용보약","conditions/deer-antler-tonic-guide.md"),@("기력회복·허약","conditions/energy-recovery.md"),@("영양제·건기식과 한약","conditions/supplements-herbal-medicine.md"))},
@{Files=@("symptom-integrated/red-flags.md","symptom-clinical/red-flags.md","symptom-clinical/followup.md");
Desc="증상·질환에서 위험신호·감별·치료반응·경과 재평가를 구조적으로 연결하는 임상 안전 문서입니다.";
Links=@(@("증상·질환 한눈에 보기","conditions/index.md"),@("침구치료 안전·위험신호","acupuncture-integrated/safety.md"),@("환자 질문 검색 지도","ai/patient-search-map.md"))},
@{Files=@("diagnostics/index.md","eight-principles-network/integrated-map.md","zangfu-pattern-network/integrated-map.md");
Desc="한의학의 팔강·장부·기혈진액·병인병기와 임상 변증을 증상과 치료방향으로 연결하는 진단·변증 핵심 지도입니다.";
Links=@(@("한의학 기초 한눈에 보기","foundations-integrated/index.md"),@("증상·질환 한눈에 보기","conditions/index.md"),@("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md"))}
)

function Get-Title($text,$fallback){
 if($text -match '(?m)^title:\s*(.+?)\s*$'){return $Matches[1].Trim().Trim('"').Trim("'")}
 if($text -match '(?m)^#\s+(.+?)\s*$'){return $Matches[1].Trim()}
 return $fallback
}
function Add-Description($text,$desc){
 if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
  $fm=$Matches[1]
  if($fm -match '(?m)^description:\s*.*$'){$fm=[regex]::Replace($fm,'(?m)^description:\s*.*$',"description: $desc",1)}
  else{$fm=$fm.TrimEnd()+"`r`ndescription: $desc"}
  return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
 }
 return "---`r`ndescription: $desc`r`n---`r`n"+$text
}
function RelLink($from,$targetRel){
 $target=Join-Path $Docs $targetRel
 if(-not(Test-Path $target)){return $null}
 return [System.IO.Path]::GetRelativePath((Split-Path $from -Parent),$target).Replace('\','/')
}
$changed=0
foreach($g in $Groups){
 foreach($rel in $g.Files){
  $p=Join-Path $Docs $rel
  if(-not(Test-Path $p)){Write-Host "SKIP missing: $rel" -ForegroundColor Yellow; continue}
  $text=Get-Content $p -Raw -Encoding UTF8
  if($text.Contains($Marker)){continue}
  $b=Join-Path $Backup $rel
  New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
  Copy-Item $p $b -Force
  $title=Get-Title $text ([IO.Path]::GetFileNameWithoutExtension($p))
  $text=Add-Description $text "$title — $($g.Desc)"
  $block="`r`n`r`n$Marker`r`n## 지식망에서의 위치`r`n`r`n이 문서는 단독 정보로 끝나지 않고 **환자 질문 → 증상·병증 → 치료 선택 → 전문 한의학 지식 → 경과평가**의 흐름 안에서 읽습니다.`r`n`r`n## 함께 보면 좋은 핵심 문서`r`n`r`n"
  foreach($x in $g.Links){
   $link=RelLink $p $x[1]
   if($link){$block+="- [$($x[0])]($link)`r`n"}
  }
  Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
  Write-Host "REPAIRED: $rel" -ForegroundColor Green
  $changed++
 }
}
Write-Host ""
Write-Host "STEP 8 완료: $changed 개 고가치 문서 보강" -ForegroundColor Cyan
Write-Host "원본 백업: HIGH_VALUE_BACKUP_STEP8"
Read-Host "Enter를 누르면 종료합니다"
