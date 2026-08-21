$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "QUALITY_BACKUP_STEP5"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_QUALITY_LINKS_STEP5 -->"

$SkipPatterns=@(
"templates/","/references.md","guide/status-policy.md","guide/citation-policy.md"
)

function Rel($p){ return $p.FullName.Substring($Docs.Length).TrimStart('\').Replace('\','/') }
function Is-Skip([string]$rel){
    foreach($x in $SkipPatterns){ if($rel.Contains($x)){ return $true } }
    return $false
}
function Get-Title([string]$text,[string]$fallback){
    if($text -match '(?m)^title:\s*(.+?)\s*$'){ return $Matches[1].Trim().Trim('"').Trim("'") }
    if($text -match '(?m)^#\s+(.+?)\s*$'){ return $Matches[1].Trim() }
    return $fallback
}
function Has-Description([string]$text){ return $text -match '(?m)^description:\s*\S+' }
function Add-Description([string]$text,[string]$desc){
    if(Has-Description $text){ return $text }
    if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
        $fm=$Matches[1].TrimEnd()+"`r`ndescription: $desc"
        return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$fm`r`n---",1)
    }
    return "---`r`ndescription: $desc`r`n---`r`n"+$text
}
function Backup($p,$rel){
    $b=Join-Path $Backup $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent) | Out-Null
    Copy-Item $p $b -Force
}
function Count-InternalLinks([string]$text){
    $n=0
    foreach($m in [regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')){
        $x=$m.Groups[1].Value
        if($x -notmatch '^(https?:|mailto:|#)'){ $n++ }
    }
    return $n
}
function RelativeTarget($from,$targetRel){
    $target=Join-Path $Docs $targetRel
    if(-not (Test-Path $target)){ return $null }
    return [System.IO.Path]::GetRelativePath((Split-Path $from -Parent),$target).Replace('\','/')
}

# Priority areas only; avoids indiscriminate editing of all 1265 docs.
$Areas=@(
    @{Prefix="acupuncture-clinical/"; Desc="침구치료의 임상 감별·치료전략·안전·경과평가를 구조화한 심화 문서입니다.";
      Hubs=@(@("침구·치료 한눈에 보기","acupuncture-integrated/index.md"),@("통증·증상으로 침구치료 찾기","acupuncture-integrated/by-symptom.md"),@("침구치료 안전·위험신호","acupuncture-integrated/safety.md"))},
    @{Prefix="evidence-clinical/"; Desc="한의학 연구근거의 설계·근거수준·임상 적용을 이해하기 위한 연구 해석 심화 문서입니다.";
      Hubs=@(@("연구·근거 임상 해석","evidence-integrated/index.md"),@("논문·PMID·DOI 찾기","evidence-integrated/find-research.md"),@("근거와 출처를 따라가는 방법","ai/evidence-map.md"))},
    @{Prefix="foundations-clinical/"; Desc="한의학 기초이론을 변증·치법·임상추론으로 연결하는 임상 심화 문서입니다.";
      Hubs=@(@("한의학 기초 한눈에 보기","foundations-integrated/index.md"),@("증상·질환 한눈에 보기","conditions/index.md"),@("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md"))},
    @{Prefix="herbal-formula-clinical/"; Desc="본초와 방제를 병증·치법·처방구조·안전·경과평가로 연결하는 임상 심화 문서입니다.";
      Hubs=@(@("본초·방제 한눈에 보기","herbal-integrated/index.md"),@("방제 찾기","herbal-integrated/formulas.md"),@("본초 찾기","herbal-integrated/herbs.md"))},
    @{Prefix="herbal-integrated/"; Desc="환자 증상과 한의학적 병증을 본초·방제·안전·근거 자료로 연결하는 통합 한약 지식 문서입니다.";
      Hubs=@(@("본초·방제 한눈에 보기","herbal-integrated/index.md"),@("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md"),@("맞춤한약","conditions/custom-herbal-medicine.md"))},
    @{Prefix="acupuncture-integrated/"; Desc="증상·경혈·근골격 기능·침·전침·약침·안전을 연결하는 통합 침구 지식 문서입니다.";
      Hubs=@(@("침구·치료 한눈에 보기","acupuncture-integrated/index.md"),@("통증·증상으로 침구치료 찾기","acupuncture-integrated/by-symptom.md"),@("경혈·경락 찾기","acupuncture-integrated/points-meridians.md"))}
)

$changed=0; $descAdded=0; $linksAdded=0
$files=Get-ChildItem $Docs -Recurse -File -Filter *.md
foreach($p in $files){
    $rel=Rel $p
    if(Is-Skip $rel){ continue }
    $area=$null
    foreach($a in $Areas){ if($rel.StartsWith($a.Prefix)){ $area=$a; break } }
    if($null -eq $area){ continue }

    $text=Get-Content $p.FullName -Raw -Encoding UTF8
    $orig=$text
    $title=Get-Title $text $p.BaseName

    if(-not (Has-Description $text)){
        $desc="$title — $($area.Desc)"
        $text=Add-Description $text $desc
        $descAdded++
    }

    $internal=Count-InternalLinks $text
    if($internal -lt 3 -and -not $text.Contains($Marker)){
        $valid=@()
        foreach($h in $area.Hubs){
            $target=RelativeTarget $p.FullName $h[1]
            if($target -and $p.FullName -ne (Join-Path $Docs $h[1])){ $valid += ,@($h[0],$target) }
        }
        if($valid.Count -gt 0){
            $block="`r`n`r`n$Marker`r`n## 관련 핵심 허브`r`n`r`n"
            foreach($v in $valid){ $block+="- [$($v[0])]($($v[1]))`r`n" }
            $text=$text.TrimEnd()+$block
            $linksAdded++
        }
    }

    if($text -ne $orig){
        Backup $p $rel
        Set-Content $p.FullName $text -Encoding UTF8
        Write-Host "QUALITY: $rel" -ForegroundColor Green
        $changed++
    }
}

Write-Host ""
Write-Host "STEP 5 완료" -ForegroundColor Cyan
Write-Host "수정 문서: $changed"
Write-Host "description 추가: $descAdded"
Write-Host "내부링크 허브 블록 추가: $linksAdded"
Write-Host "템플릿·references·정책문서는 예외 처리했습니다."
Write-Host "원본 백업: QUALITY_BACKUP_STEP5"
Read-Host "Enter를 누르면 종료합니다"
