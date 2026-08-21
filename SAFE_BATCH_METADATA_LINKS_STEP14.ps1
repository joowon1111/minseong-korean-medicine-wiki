$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "SAFE_BATCH_BACKUP_STEP14"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_SAFE_BATCH_STEP14 -->"

$Batches=@(
@{
 Name="침구 임상"
 Prefix="acupuncture-clinical/"
 Desc="침구치료의 임상 감별·치료강도·안전·치료반응을 구조화한 심화 문서입니다."
 Hubs=@(
  @("침구·치료 임상 심화","acupuncture-clinical/index.md"),
  @("통증·증상으로 침구치료 찾기","acupuncture-integrated/by-symptom.md"),
  @("침구치료 안전·위험신호","acupuncture-integrated/safety.md"),
  @("근골격 통증 핵심","acupuncture-integrated/musculoskeletal.md")
 )
},
@{
 Name="연구근거 임상"
 Prefix="evidence-clinical/"
 Desc="연구설계·근거수준·임상 적용과 한계를 이해하기 위한 한의학 근거 해석 심화 문서입니다."
 Hubs=@(
  @("연구·근거 임상 해석","evidence-integrated/index.md"),
  @("논문·PMID·DOI 찾기","evidence-integrated/find-research.md"),
  @("근거와 출처를 따라가는 방법","ai/evidence-map.md")
 )
},
@{
 Name="한의학 기초 임상"
 Prefix="foundations-clinical/"
 Desc="한의학 기초이론을 실제 변증·치법·임상추론으로 연결하는 심화 문서입니다."
 Hubs=@(
  @("한의학 기초 한눈에 보기","foundations-integrated/index.md"),
  @("진단·변증","diagnostics/index.md"),
  @("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md")
 )
},
@{
 Name="본초·방제 임상"
 Prefix="herbal-formula-clinical/"
 Desc="본초와 방제를 병증·치법·처방구조·안전·경과평가로 연결하는 임상 심화 문서입니다."
 Hubs=@(
  @("본초·방제 한눈에 보기","herbal-integrated/index.md"),
  @("방제 찾기","herbal-integrated/formulas.md"),
  @("본초 찾기","herbal-integrated/herbs.md"),
  @("본초·방제 안전","herbal-integrated/safety.md")
 )
},
@{
 Name="증상 임상"
 Prefix="symptom-clinical/"
 Desc="증상에서 위험신호·감별·기능평가·치료전략·경과재평가로 이어지는 임상 심화 문서입니다."
 Hubs=@(
  @("증상·질환 한눈에 보기","conditions/index.md"),
  @("환자 질문 검색 지도","ai/patient-search-map.md"),
  @("치료효과 평가","conditions/treatment-response-evaluation.md")
 )
}
)

$SkipRegex='(^|/)(index|references|template|clinical-template)\.md$'
function GetTitle($text,$fallback){
 if($text -match '(?m)^title:\s*(.+?)\s*$'){return $Matches[1].Trim().Trim('"').Trim("'")}
 if($text -match '(?m)^#\s+(.+?)\s*$'){return $Matches[1].Trim()}
 return $fallback
}
function HasDesc($text){return $text -match '(?m)^description:\s*\S+'}
function AddDesc($text,$desc){
 if(HasDesc $text){return $text}
 if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
  $fm=$Matches[1].TrimEnd()+"`r`ndescription: $desc"
  return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
 }
 return "---`r`ndescription: $desc`r`n---`r`n"+$text
}
function CountLinks($text){
 $n=0
 foreach($m in [regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')){
  if($m.Groups[1].Value -notmatch '^(https?:|mailto:|#)'){$n++}
 }
 return $n
}
function RLink($from,$rel){
 $target=Join-Path $Docs $rel
 if(-not(Test-Path $target)){return $null}
 return [IO.Path]::GetRelativePath((Split-Path $from -Parent),$target).Replace('\','/')
}
function Backup($p,$rel){
 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force
}

$changed=0;$descCount=0;$linkCount=0
foreach($batch in $Batches){
 $folder=Join-Path $Docs $batch.Prefix
 if(-not(Test-Path $folder)){continue}
 foreach($p in Get-ChildItem $folder -File -Filter *.md){
  $rel=[IO.Path]::GetRelativePath($Docs,$p.FullName).Replace('\','/')
  if($rel -match $SkipRegex){continue}
  $text=Get-Content $p.FullName -Raw -Encoding UTF8
  $orig=$text
  $title=GetTitle $text $p.BaseName
  if(-not(HasDesc $text)){
   $text=AddDesc $text "$title — $($batch.Desc)"
   $descCount++
  }
  if((CountLinks $text) -lt 3 -and -not $text.Contains($Marker)){
   $block="`r`n`r`n$Marker`r`n## 관련 핵심 허브`r`n`r`n"
   $added=0
   foreach($h in $batch.Hubs){
    $r=RLink $p.FullName $h[1]
    if($r){$block+="- [$($h[0])]($r)`r`n";$added++}
   }
   if($added -gt 0){$text=$text.TrimEnd()+$block;$linkCount++}
  }
  if($text -ne $orig){
   Backup $p.FullName $rel
   Set-Content $p.FullName $text -Encoding UTF8
   Write-Host "SAFE BATCH: $rel" -ForegroundColor Green
   $changed++
  }
 }
}

Write-Host ""
Write-Host "STEP 14 완료" -ForegroundColor Cyan
Write-Host "수정 문서: $changed"
Write-Host "description 추가: $descCount"
Write-Host "내부링크 보강: $linkCount"
Write-Host "원본 백업: SAFE_BATCH_BACKUP_STEP14"
Read-Host "Enter를 누르면 종료합니다"
