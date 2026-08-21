$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}
$Backup=Join-Path $Root "FOUNDATIONS_BACKUP_STEP13"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_FOUNDATIONS_3LAYER_STEP13 -->"

$Groups=@(
@("음양·오행",
 "foundations/yinyang-five-phases.md",
 "foundations-clinical/yinyang-fivephases.md",
 "foundations-integrated/yinyang-fivephases.md",
 "한의학의 음양·오행 개념 자체를 설명하는 기초 문서",
 "음양·오행을 실제 증상과 임상추론으로 연결하는 임상 브리지",
 "음양·오행을 장부·기혈진액·병인병기·변증치법과 연결하는 통합 허브"),
@("병인·병기",
 "foundations/pathogenesis.md",
 "foundations-clinical/etiology-pathogenesis.md",
 "foundations-integrated/etiology-pathogenesis.md",
 "병인과 병기의 기본 개념을 설명하는 기초 문서",
 "환자의 원인·유발요인·증상 진행을 병기로 해석하는 임상 브리지",
 "병인병기를 장부·기혈진액·변증·치법·방제로 연결하는 통합 허브"),
@("변증·치법",
 "foundations/pattern-treatment.md",
 "foundations-clinical/pattern-to-treatment.md",
 "foundations-integrated/pattern-treatment.md",
 "변증과 치법의 기본 의미를 설명하는 기초 문서",
 "증상정보에서 변증을 세우고 치료방향으로 넘어가는 임상 브리지",
 "팔강·장부·기혈진액 병증과 치법·본초·방제·침구를 연결하는 통합 허브"),
@("장부·기혈진액",
 "foundations/zangfu.md",
 "foundations-clinical/zangfu-to-pattern.md",
 "foundations-integrated/zangfu-qi-blood-fluids.md",
 "장부와 기혈진액의 기본 기능체계를 설명하는 기초 문서",
 "장부 기능과 기혈진액 변화를 실제 병증으로 연결하는 임상 브리지",
 "장부·기혈진액을 병인병기·변증·치법과 연결하는 통합 허브")
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
function Backup($p,$rel){
 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force
}
function R($from,$rel){
 $t=Join-Path $Docs $rel
 if(-not(Test-Path $t)){return $null}
 return [IO.Path]::GetRelativePath((Split-Path $from -Parent),$t).Replace('\','/')
}
$changed=0
foreach($g in $Groups){
 $name=$g[0]
 $rels=@($g[1],$g[2],$g[3])
 $roles=@($g[4],$g[5],$g[6])
 for($i=0;$i -lt 3;$i++){
  $rel=$rels[$i]; $p=Join-Path $Docs $rel
  if(-not(Test-Path $p)){Write-Host "SKIP missing: $rel" -ForegroundColor Yellow; continue}
  $text=Get-Content $p -Raw -Encoding UTF8
  if($text.Contains($Marker)){continue}
  Backup $p $rel
  $text=AddDesc $text "$name — $($roles[$i])."
  $layer=@("기초 개념","임상 브리지","통합 허브")[$i]
  $block="`r`n`r`n$Marker`r`n## 이 문서의 지식 계층`r`n`r`n**$layer** — $($roles[$i]).`r`n`r`n"
  $block+="한의학 개념을 서로 중복해서 반복하기보다 **기초 개념 → 임상 해석 → 통합적 치료 연결**의 단계로 읽도록 구성합니다.`r`n`r`n## 같은 주제의 다른 계층`r`n`r`n"
  for($j=0;$j -lt 3;$j++){
   if($j -eq $i){continue}
   $link=R $p $rels[$j]
   if($link){$block+="- [$(@('기초 개념','임상 브리지','통합 허브')[$j])]($link)`r`n"}
  }
  $extra=@(
   @("진단·변증 허브","diagnostics/index.md"),
   @("증상·질환 한눈에 보기","conditions/index.md"),
   @("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md")
  )
  $block+="`r`n## 임상 지식망 연결`r`n`r`n"
  foreach($x in $extra){$link=R $p $x[1]; if($link){$block+="- [$($x[0])]($link)`r`n"}}
  Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
  Write-Host "$layer : $rel" -ForegroundColor Green
  $changed++
 }
}

# Eight principles network: strengthen core nodes and link to foundation layers.
$Eight=@(
@("eight-principles-network/exterior-interior.md","표리(表裏)"),
@("eight-principles-network/cold-heat.md","한열(寒熱)"),
@("eight-principles-network/deficiency-excess.md","허실(虛實)"),
@("eight-principles-network/yin-yang.md","음양(陰陽)"),
@("eight-principles-network/combined-patterns.md","팔강의 조합"),
@("eight-principles-network/clinical-reasoning.md","팔강변증 임상 추론"),
@("eight-principles-network/treatment-map.md","팔강에서 치법으로")
)
foreach($x in $Eight){
 $rel=$x[0]; $p=Join-Path $Docs $rel
 if(-not(Test-Path $p)){continue}
 $text=Get-Content $p -Raw -Encoding UTF8
 if($text.Contains($Marker)){continue}
 Backup $p $rel
 $text=AddDesc $text "$($x[1]) — 팔강변증을 증상 패턴·병증의 경중·치법으로 연결하는 진단 지식망 문서입니다."
 $block="`r`n`r`n$Marker`r`n## 팔강변증에서의 위치`r`n`r`n팔강은 하나의 증상을 단독으로 분류하는 표가 아니라 **표리·한열·허실·음양의 조합과 시간에 따른 변화**를 통해 병증의 큰 방향을 잡는 틀입니다. 이후 장부·기혈진액·병인병기와 결합해 치료 방향을 구체화합니다.`r`n`r`n"
 $links=@(@("팔강변증 통합 지도","eight-principles-network/integrated-map.md"),@("진단·변증","diagnostics/index.md"),@("변증·치법 통합","foundations-integrated/pattern-treatment.md"))
 foreach($l in $links){$z=R $p $l[1];if($z){$block+="- [$($l[0])]($z)`r`n"}}
 Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
 Write-Host "EIGHT PRINCIPLES: $rel" -ForegroundColor Cyan
 $changed++
}
Write-Host ""
Write-Host "STEP 13 완료: $changed 개 기초이론·팔강 문서 역할 보강" -ForegroundColor Cyan
Write-Host "원본 백업: FOUNDATIONS_BACKUP_STEP13"
Read-Host "Enter를 누르면 종료합니다"
