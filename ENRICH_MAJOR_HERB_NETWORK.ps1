$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "HERB_NETWORK_BACKUP_STEP10"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_HERB_NETWORK_STEP10 -->"

$Targets=@(
@("herbs/ginseng.md","인삼","피로·기력회복","보기","herbal-integrated/herbs-for-fatigue.md"),
@("herbs/astragalus.md","황기","피로·허약·회복","보기·고표","herbal-integrated/herbs-for-fatigue.md"),
@("herbs/atractylodes.md","백출","소화·비위·허약","건비·조습","herbal-integrated/herbs-for-digestion.md"),
@("herbs/poria.md","복령","소화·수습·심신","건비·이수·안신","herbal-integrated/herbs-for-digestion.md"),
@("herbs/citrus-peel.md","진피","소화·기체·담","이기·조습화담","herbal-integrated/herbs-for-digestion.md"),
@("herbs/pinellia.md","반하","담·오심·소화","조습화담·강역","herbal-integrated/herbs-for-digestion.md"),
@("herbs/amomum.md","사인","소화·비위","화습·행기","herbal-integrated/herbs-for-digestion.md"),
@("herbs/angelica.md","당귀","보혈·여성·회복","보혈·활혈","herbal-integrated/herbs-for-women.md"),
@("herbs/rehmannia-prepared.md","숙지황","보혈·보익·갱년기","보혈·자음","herbal-integrated/herbs-for-menopause.md"),
@("herbs/peony-white.md","백작약","혈허·근육·여성","양혈·유간","herbal-integrated/herbs-for-women.md"),
@("herbs/jujube-seed.md","산조인","불면·수면","양심안신","herbal-integrated/herbs-for-sleep.md"),
@("herbs/polygala.md","원지","불면·심신·건망","안신·화담","herbal-integrated/herbs-for-sleep.md"),
@("herbs/achyranthes.md","우슬","허리·무릎·근골격","보간신·강근골·활혈","herbal-integrated/herbs-for-pain.md"),
@("herbs/eucommia.md","두충","허리·무릎·근골격","보간신·강근골","herbal-integrated/herbs-for-pain.md"),
@("herbs/dipsacus.md","속단","근골격·회복","보간신·속근골","herbal-integrated/herbs-for-pain.md"),
@("herbs/angelica-pubescens.md","독활","통증·풍습","거풍습·지통","herbal-integrated/herbs-for-pain.md"),
@("herbs/cyperus.md","향부자","스트레스·여성·기체","소간이기","herbal-integrated/herbs-for-stress.md"),
@("herbs/bupleurum.md","시호","스트레스·소양·간울","소간·해울","herbal-integrated/herbs-for-stress.md"),
@("herbs/alismatis.md","택사","부종·수습","이수삼습","herbal-integrated/herbs-for-edema.md"),
@("herbs/aconite.md","부자","냉증·양허","회양·온양","herbal-integrated/herbs.md"),
@("herbs/acorus.md","석창포","담·신지·개규","화담·개규","herbal-integrated/herbs.md"),
@("herbs/anemarrhena.md","지모","열·음허","청열·자음","herbal-integrated/herbs.md")
)

function FindFile($preferred,$name){
 $p=Join-Path $Docs $preferred
 if(Test-Path $p){return $p}
 # Safe fallback: exact title match in herbs only.
 foreach($f in Get-ChildItem (Join-Path $Docs "herbs") -File -Filter *.md){
  $t=Get-Content $f.FullName -Raw -Encoding UTF8
  if($t -match "(?m)^#\s+$([regex]::Escape($name))(?:\(|（|\s|$)" -or $t -match "(?m)^title:\s*$([regex]::Escape($name))(?:\(|（|\s|$)"){return $f.FullName}
 }
 return $null
}
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
 $preferred=$x[0]; $name=$x[1]; $area=$x[2]; $role=$x[3]; $bridge=$x[4]
 $p=FindFile $preferred $name
 if(-not $p){Write-Host "SKIP missing herb: $name" -ForegroundColor Yellow; continue}
 $text=Get-Content $p -Raw -Encoding UTF8
 if($text.Contains($Marker)){continue}
 $rel=[IO.Path]::GetRelativePath($Docs,$p).Replace('\','/')
 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force

 $title=GetTitle $text $name
 $text=AddDesc $text "$title — $area 영역에서 $role 역할과 관련 방제·병증·환자 증상을 연결해 탐색하는 본초 문서입니다."
 $block="`r`n`r`n$Marker`r`n## 이 본초를 지식망에서 찾는 방법`r`n`r`n"
 $block+="**$area → 관련 병증 → $title → $role → 관련 방제 → 환자 증상과 경과평가** 순으로 연결해 볼 수 있습니다.`r`n`r`n"
 $block+="한 약재의 효능만으로 처방 전체를 설명하지 않고 **성미·귀경·병증·배합관계와 실제 방제 속 역할**을 함께 봅니다.`r`n`r`n## 관련 핵심 문서`r`n`r`n"
 $links=@(
  @("관련 증상에서 본초 찾기",$bridge),
  @("본초 찾기","herbal-integrated/herbs.md"),
  @("주요 본초 비교·감별","herbal-integrated/herb-comparisons.md"),
  @("방제 찾기","herbal-integrated/formulas.md"),
  @("본초·방제 안전·복용 주의","herbal-integrated/safety.md")
 )
 foreach($l in $links){$r=RLink $p $l[1]; if($r){$block+="- [$($l[0])]($r)`r`n"}}
 Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
 Write-Host "HERB NETWORK: $rel" -ForegroundColor Green
 $changed++
}
Write-Host ""
Write-Host "STEP 10 완료: $changed 개 주요 본초 문서 보강" -ForegroundColor Cyan
Write-Host "원본 백업: HERB_NETWORK_BACKUP_STEP10"
Read-Host "Enter를 누르면 종료합니다"
