$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "SASANG_CORE_BACKUP_STEP11"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_SASANG_CORE_STEP11 -->"

$Targets=@(
@("sasang/four-constitutions.md","사상체질의 기본 구조","네 체질의 생리·병리와 소증·병증을 비교하는 기본 허브"),
@("sasang/soeumin.md","소음인","소화·냉열·땀·대변·수면과 표리병·순역증을 함께 보는 체질 문서"),
@("sasang/soyangin.md","소양인","열감·갈증·수면·대변·소증과 병증의 경중을 함께 보는 체질 문서"),
@("sasang/taeeumin.md","태음인","땀·호흡·소화·체력·한열과 표리병의 흐름을 함께 보는 체질 문서"),
@("sasang/taeyangin.md","태양인","소증과 해역·열격 등 병증의 흐름을 함께 보는 체질 문서"),
@("sasang/integrated-map.md","사상의학 통합 지식 지도","체질 → 소증 → 병증 → 중증도 → 처방 → 회복신호를 연결하는 통합지도"),
@("sasang/pattern-formula-map.md","사상체질 → 병증·처방 지도","체질명만이 아니라 현재 병증을 통해 처방으로 연결하는 지도"),
@("sasang-symptoms/integrated-map.md","증상 → 사상체질병증 탐색 지도","환자 생활언어를 체질별 소증·현재 병증과 연결하는 지도"),
@("sasang-original-symptoms/fatigue-recovery.md","피로·회복","체질별 평소 기력과 병후 회복 양상을 소증으로 추적하는 문서"),
@("sasang-original-symptoms/digestion-appetite.md","소화·식욕","체질별 소화·식욕의 평소 상태와 병증 변화를 구분하는 소증 문서"),
@("sasang-original-symptoms/sweating.md","땀","발한의 양뿐 아니라 땀 후 편안함·피로·냉열을 함께 보는 소증 문서"),
@("sasang-original-symptoms/sleep.md","수면","입면·각성·꿈·회복감과 현재 병증을 함께 보는 소증 문서"),
@("sasang-original-symptoms/stool.md","대변","빈도·형태·배변 후 느낌과 체질 병증의 변화를 함께 보는 소증 문서"),
@("sasang-original-symptoms/urination.md","소변","빈도·야간뇨·양상과 체질 병증의 변화를 함께 보는 소증 문서"),
@("sasang-original-symptoms/cold-heat.md","한열","추위·더위·상열·냉감의 시간패턴과 다른 소증을 함께 보는 문서"),
@("sasang-progression/worsening-signs.md","사상체질 악화 신호 체크포인트","소증의 붕괴와 병증 진행을 시간순으로 추적하는 악화 지도"),
@("sasang-progression/recovery-signs.md","사상체질 회복 신호 체크포인트","소화·수면·대소변·땀·기력의 회복 순서를 추적하는 지도"),
@("sasang-severity/recovery-prognosis.md","회복·예후 추적","병증의 경중과 소증 회복을 함께 보며 예후를 재평가하는 문서"),
@("sasang-formulas/hyeongbangdojeok-san.md","형방도적산","소양인 병증과 처방 선택의 맥락을 연결하는 대표 사상처방"),
@("sasang-formulas/hyeongbangsabaek-san.md","형방사백산","소양인 병증과 한열·표리의 맥락을 연결하는 대표 사상처방"),
@("sasang-formulas/yanggyeoksanhwa-tang.md","양격산화탕","소양인 리열 병증과 증상 경중을 연결하는 대표 사상처방")
)

function GetTitle($text,$fallback){
 if($text -match '(?m)^title:\s*(.+?)\s*$'){return $Matches[1].Trim().Trim('"').Trim("'")}
 if($text -match '(?m)^#\s+(.+?)\s*$'){return $Matches[1].Trim()}
 return $fallback
}
function AddDesc($text,$desc){
 if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
  $fm=$Matches[1]
  if($fm -match '(?m)^description:\s*.*$'){$fm=[regex]::Replace($fm,'(?m)^description:\s*.*$',"description: $desc",1)}
  else{$fm=$fm.TrimEnd()+"`r`ndescription: $desc"}
  return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
 }
 return "---`r`ndescription: $desc`r`n---`r`n"+$text
}
function RLink($from,$rel){
 $target=Join-Path $Docs $rel
 if(-not(Test-Path $target)){return $null}
 return [IO.Path]::GetRelativePath((Split-Path $from -Parent),$target).Replace('\','/')
}

$changed=0
foreach($x in $Targets){
 $rel=$x[0]; $label=$x[1]; $role=$x[2]
 $p=Join-Path $Docs $rel
 if(-not(Test-Path $p)){Write-Host "SKIP missing: $rel" -ForegroundColor Yellow; continue}
 $text=Get-Content $p -Raw -Encoding UTF8
 if($text.Contains($Marker)){continue}

 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force
 $title=GetTitle $text $label
 $text=AddDesc $text "$title — $role."

 $block="`r`n`r`n$Marker`r`n## 사상의학 지식망에서의 위치`r`n`r`n"
 $block+="사상의학에서는 체질명 하나로 상태를 단정하지 않고 **평소의 소증 → 현재 증상의 변화 → 표리·순역과 병증의 경중 → 처방 선택 → 치료 후 소증 회복**의 흐름을 함께 봅니다.`r`n`r`n"
 $block+="특히 같은 증상이라도 **언제 심해지는지, 식사·수면·대변·소변·땀·냉열·기력 중 무엇이 먼저 무너지고 무엇이 먼저 회복되는지**가 병증의 경중과 경과를 판단하는 중요한 단서가 될 수 있습니다.`r`n`r`n"
 $block+="## 관련 핵심 문서`r`n`r`n"
 $links=@(
  @("사상의학 개요","sasang/index.md"),
  @("사상체질 기본 구조","sasang/four-constitutions.md"),
  @("사상체질 병증·처방 지도","sasang/pattern-formula-map.md"),
  @("증상에서 사상체질병증 찾기","sasang-symptoms/integrated-map.md"),
  @("사상체질 회복 신호","sasang-progression/recovery-signs.md"),
  @("사상체질 악화 신호","sasang-progression/worsening-signs.md"),
  @("환자용 사상체질 안내","sasang/sasang-intro-patient.md")
 )
 foreach($l in $links){$r=RLink $p $l[1]; if($r -and $r -ne [IO.Path]::GetFileName($p)){$block+="- [$($l[0])]($r)`r`n"}}
 Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
 Write-Host "SASANG CORE: $rel" -ForegroundColor Green
 $changed++
}
Write-Host ""
Write-Host "STEP 11 완료: $changed 개 사상의학 핵심 문서 보강" -ForegroundColor Cyan
Write-Host "원본 백업: SASANG_CORE_BACKUP_STEP11"
Read-Host "Enter를 누르면 종료합니다"
