$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not(Test-Path $Docs)){Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1}

$Backup=Join-Path $Root "FORMULA_NETWORK_BACKUP_STEP9"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_FORMULA_NETWORK_STEP9 -->"

$Targets=@(
@("formulas/banxia-xiexin-tang.md","소화·위장","한열착잡·비위불화","소화불량 한약 처방 찾기","herbal-integrated/formula-for-digestion.md"),
@("formulas/pingwei-san.md","소화·위장","습체·비위불화","소화불량 한약 처방 찾기","herbal-integrated/formula-for-digestion.md"),
@("formulas/xiangsha-liujunzi-tang.md","소화·허약","비기허·기체","소화불량 한약 처방 찾기","herbal-integrated/formula-for-digestion.md"),
@("formulas/erchen-tang.md","담·소화","담습","소화불량 한약 처방 찾기","herbal-integrated/formula-for-digestion.md"),
@("formulas/baohe-wan.md","식적·소화","식적","소화불량 한약 처방 찾기","herbal-integrated/formula-for-digestion.md"),
@("formulas/wujisan.md","통증·냉증·소화","한습·기혈울체","근골격 통증 한약 처방 찾기","herbal-integrated/formula-for-pain.md"),
@("formulas/huishou-san.md","목·어깨·통증","기혈울체·담","근골격 통증 한약 처방 찾기","herbal-integrated/formula-for-pain.md"),
@("formulas/qingshang-juantong-tang.md","두통","풍·담·화 등 두통 병증","두통·어지럼 한약 처방 찾기","herbal-integrated/formula-for-headache.md"),
@("formulas/tianwang-buxin-dan.md","불면·심계","음혈부족·심신불안","불면 한약 처방 찾기","herbal-integrated/formula-for-insomnia.md"),
@("formulas/suanzaoren-tang.md","불면·수면","심혈부족·허번","불면 한약 처방 찾기","herbal-integrated/formula-for-insomnia.md"),
@("formulas/jiawei-wendan-tang.md","불면·담","담열·심신불안","불면 한약 처방 찾기","herbal-integrated/formula-for-insomnia.md"),
@("formulas/wenjing-tang.md","여성·월경","충임허한·어혈","여성·월경·산후 한약 처방 찾기","herbal-integrated/formula-for-women.md"),
@("formulas/tiaojing-zhongyu-tang.md","여성·임신준비","월경·생식 관련 병증","여성·월경·산후 한약 처방 찾기","herbal-integrated/formula-for-women.md"),
@("formulas/jiawei-xiaoyao-san.md","여성·갱년기·스트레스","간울·화열","갱년기·상열감 한약 처방 찾기","herbal-integrated/formula-for-menopause.md"),
@("formulas/ziyin-jianghuo-tang.md","갱년기·허열","음허화왕","갱년기·상열감 한약 처방 찾기","herbal-integrated/formula-for-menopause.md"),
@("formulas/shengmai-san.md","피로·기력","기음양허","피로·기력저하 한약 처방 찾기","herbal-integrated/formula-for-fatigue.md"),
@("formulas/ssanghwa-tang.md","피로·회복","기혈허·피로","피로·기력저하 한약 처방 찾기","herbal-integrated/formula-for-fatigue.md"),
@("formulas/danggui-buxue-tang.md","피로·보혈","기혈허","피로·기력저하 한약 처방 찾기","herbal-integrated/formula-for-fatigue.md"),
@("formulas/xiaoqinglong-tang.md","비염·기침","풍한·수음","비염·코막힘 한약 처방 찾기","herbal-integrated/formula-for-rhinitis.md"),
@("formulas/jingjie-lianqiao-tang.md","비염·인후·염증성 증상","풍열·울체","비염·코막힘 한약 처방 찾기","herbal-integrated/formula-for-rhinitis.md"),
@("formulas/renshen-suyin.md","감기·기침·허약","기허·외감·담","감기·기침 한약 처방 찾기","herbal-integrated/formula-for-cold-cough.md"),
@("formulas/galgeun-tang.md","감기·경항부","태양표증·항배강","감기·기침 한약 처방 찾기","herbal-integrated/formula-for-cold-cough.md"),
@("formulas/wuling-san.md","부종·수습","수습정체","부종·수습과 본초 찾기","herbal-integrated/herbs-for-edema.md"),
@("formulas/zhuling-tang.md","수습·배뇨","수열호결·음상","부종·수습과 본초 찾기","herbal-integrated/herbs-for-edema.md")
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
 $rel=$x[0]; $area=$x[1]; $pattern=$x[2]; $bridgeLabel=$x[3]; $bridgeRel=$x[4]
 $p=Join-Path $Docs $rel
 if(-not(Test-Path $p)){Write-Host "SKIP missing: $rel" -ForegroundColor Yellow; continue}
 $text=Get-Content $p -Raw -Encoding UTF8
 if($text.Contains($Marker)){continue}

 $b=Join-Path $Backup $rel
 New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent)|Out-Null
 Copy-Item $p $b -Force

 $title=GetTitle $text ([IO.Path]::GetFileNameWithoutExtension($p))
 $text=AddDesc $text "$title — $area 영역에서 $pattern 병증과 연결해 구성·치법·본초·임상 활용을 탐색하는 방제 문서입니다."

 $block="`r`n`r`n$Marker`r`n## 이 처방을 지식망에서 찾는 방법`r`n`r`n"
 $block+="**$area → $pattern → $title → 구성 본초 → 환자 증상과 경과평가** 순으로 연결해 볼 수 있습니다.`r`n`r`n"
 $links=@(
  @($bridgeLabel,$bridgeRel),
  @("방제 찾기","herbal-integrated/formulas.md"),
  @("본초 찾기","herbal-integrated/herbs.md"),
  @("같은 증상인데 처방이 다른 이유","herbal-integrated/formula-selection-guide.md"),
  @("본초·방제 안전·복용 주의","herbal-integrated/safety.md")
 )
 $block+="## 관련 핵심 문서`r`n`r`n"
 foreach($l in $links){$r=RLink $p $l[1]; if($r){$block+="- [$($l[0])]($r)`r`n"}}
 Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
 Write-Host "FORMULA NETWORK: $rel" -ForegroundColor Green
 $changed++
}
Write-Host ""
Write-Host "STEP 9 완료: $changed 개 주요 방제 문서 보강" -ForegroundColor Cyan
Write-Host "원본 백업: FORMULA_NETWORK_BACKUP_STEP9"
Read-Host "Enter를 누르면 종료합니다"
