$ErrorActionPreference = "Stop"

try {
    $Root = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $Root
    $Docs = Join-Path $Root "docs"

    if (-not (Test-Path $Docs)) {
        throw "docs 폴더를 찾을 수 없습니다. 이 파일을 저장소 최상위에 두고 실행하세요."
    }

    $Backup = Join-Path $Root "ONE_SHOT_BACKUP_V2"
    New-Item -ItemType Directory -Force -Path $Backup | Out-Null
    $Report = Join-Path $Root "ONE_SHOT_FIX_REPORT_V2.md"
    $Marker = "<!-- MINSEONG_ONE_SHOT_FIX_V2 -->"

    # Windows PowerShell 5.1 호환 상대경로 함수
    function Get-RelativePathCompat([string]$FromFile, [string]$ToFile) {
        $fromDir = Split-Path -Parent $FromFile
        $fromUri = New-Object System.Uri(($fromDir.TrimEnd('\') + '\'))
        $toUri = New-Object System.Uri($ToFile)
        $rel = $fromUri.MakeRelativeUri($toUri).ToString()
        return [System.Uri]::UnescapeDataString($rel).Replace('\','/')
    }

    function Get-DocRel([string]$FullPath) {
        $docsUri = New-Object System.Uri(($Docs.TrimEnd('\') + '\'))
        $fileUri = New-Object System.Uri($FullPath)
        return [System.Uri]::UnescapeDataString($docsUri.MakeRelativeUri($fileUri).ToString())
    }

    function Get-Title([string]$text,[string]$fallback){
        if($text -match '(?m)^title:\s*(.+?)\s*$'){
            return $Matches[1].Trim().Trim('"').Trim("'")
        }
        if($text -match '(?m)^#\s+(.+?)\s*$'){
            return $Matches[1].Trim()
        }
        return $fallback
    }

    function Has-Description([string]$text){
        return $text -match '(?m)^description:\s*\S+'
    }

    function Add-Description([string]$text,[string]$desc){
        if(Has-Description $text){ return $text }

        if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
            $fm = $Matches[1].TrimEnd() + "`r`ndescription: $desc"
            return [regex]::Replace(
                $text,
                '(?s)^---\s*\r?\n.*?\r?\n---',
                "---`r`n$fm`r`n---",
                1
            )
        }

        return "---`r`ndescription: $desc`r`n---`r`n" + $text
    }

    function Count-InternalLinks([string]$text){
        $n=0
        foreach($m in [regex]::Matches($text,'\[[^\]]+\]\(([^)]+)\)')){
            $target=$m.Groups[1].Value
            if($target -notmatch '^(https?:|mailto:|#)'){
                $n++
            }
        }
        return $n
    }

    function Backup-File([string]$p,[string]$rel){
        $b = Join-Path $Backup $rel.Replace('/','\')
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $b) | Out-Null
        Copy-Item $p $b -Force
    }

    function Get-Category([string]$rel){
        if($rel -match '^conditions/'){
            return @{
                Desc="환자 증상·질환을 위험신호·감별·한의학적 병증과 치료 지식으로 연결하는 문서입니다."
                Hubs=@(
                    @("증상·질환 한눈에 보기","conditions/index.md"),
                    @("환자 질문 검색 지도","ai/patient-search-map.md"),
                    @("맞춤한약","conditions/custom-herbal-medicine.md")
                )
            }
        }
        elseif($rel -match '^formulas/'){
            return @{
                Desc="한약 처방의 구성·치법·병증·본초와 임상 활용을 연결하는 방제 문서입니다."
                Hubs=@(
                    @("방제 찾기","herbal-integrated/formulas.md"),
                    @("본초 찾기","herbal-integrated/herbs.md"),
                    @("처방 선택 원리","herbal-integrated/formula-selection-guide.md")
                )
            }
        }
        elseif($rel -match '^herbs/'){
            return @{
                Desc="본초의 성미·귀경·효능·병증·배합과 실제 방제 속 역할을 연결하는 본초 문서입니다."
                Hubs=@(
                    @("본초 찾기","herbal-integrated/herbs.md"),
                    @("본초 비교·감별","herbal-integrated/herb-comparisons.md"),
                    @("방제 찾기","herbal-integrated/formulas.md")
                )
            }
        }
        elseif($rel -match '^(acupuncture|acupoint-network|meridian-network|acupuncture-clinical|acupuncture-integrated)/'){
            return @{
                Desc="경혈·경락·해부학·침·전침·약침과 임상 안전을 연결하는 침구 문서입니다."
                Hubs=@(
                    @("침구·치료 한눈에 보기","acupuncture-integrated/index.md"),
                    @("증상으로 침구치료 찾기","acupuncture-integrated/by-symptom.md"),
                    @("침구 안전·위험신호","acupuncture-integrated/safety.md")
                )
            }
        }
        elseif($rel -match '^(sasang|sasang-|donguisusebowon-network)/'){
            return @{
                Desc="사상체질의 소증·병증·표리·순역·처방·경과평가를 연결하는 사상의학 문서입니다."
                Hubs=@(
                    @("사상의학 개요","sasang/index.md"),
                    @("사상체질 기본 구조","sasang/four-constitutions.md"),
                    @("사상 병증·처방 지도","sasang/pattern-formula-map.md")
                )
            }
        }
        elseif($rel -match '^(foundations|diagnostics|eight-principles-network|zangfu-pattern-network|pattern-treatment|concepts)/'){
            return @{
                Desc="한의학 기초개념을 변증·병증·치법과 임상 의사결정으로 연결하는 문서입니다."
                Hubs=@(
                    @("한의학 기초 한눈에 보기","foundations-integrated/index.md"),
                    @("진단·변증","diagnostics/index.md"),
                    @("증상·치법으로 본초·방제 찾기","herbal-integrated/by-symptom-treatment.md")
                )
            }
        }
        elseif($rel -match '^(classics|classics-network|neijing-network|shanghan-network|jingui-network|donguibogam-network|bangyakhappyeon-network|wenbing-network)/'){
            return @{
                Desc="한의학 고전의 문헌적 맥락을 현대 증상·병증·본초·방제 지식과 구분해 연결하는 문서입니다."
                Hubs=@(
                    @("한의학 고전 읽기","classics-network/reading-path.md"),
                    @("주요 고전 비교","classics-network/comparison.md"),
                    @("근거와 출처","ai/evidence-map.md")
                )
            }
        }
        elseif($rel -match '^(evidence|research)/'){
            return @{
                Desc="한의학 연구의 설계·근거수준·임상 적용과 한계를 구분해 읽기 위한 연구 문서입니다."
                Hubs=@(
                    @("연구·근거 임상 해석","evidence-integrated/index.md"),
                    @("논문·PMID·DOI 찾기","evidence-integrated/find-research.md"),
                    @("근거와 출처","ai/evidence-map.md")
                )
            }
        }
        else {
            return @{
                Desc="민성 한의학 아카이브의 관련 전문 지식과 연결되는 문서입니다."
                Hubs=@(
                    @("아카이브 안내","guide/index.md"),
                    @("증상·질환","conditions/index.md"),
                    @("AI 검색 구조","ai-index.md")
                )
            }
        }
    }

    $Exclude = '(^|/)(templates?|guide)(/|$)|(^|/)(references|citation-policy|status-policy|clinical-template)\.md$'

    $beforeFiles = Get-ChildItem $Docs -Recurse -File -Filter *.md
    $beforeDesc = 0
    $beforeLow = 0

    foreach($p in $beforeFiles){
        $t=Get-Content $p.FullName -Raw -Encoding UTF8
        if(-not(Has-Description $t)){ $beforeDesc++ }
        if((Count-InternalLinks $t)-lt 3){ $beforeLow++ }
    }

    $changed=0
    $descAdded=0
    $linksAdded=0

    foreach($p in $beforeFiles){
        $rel = Get-DocRel $p.FullName
        if($rel -match $Exclude){ continue }

        $text = Get-Content $p.FullName -Raw -Encoding UTF8
        $orig = $text
        $title = Get-Title $text $p.BaseName
        $cat = Get-Category $rel

        if(-not(Has-Description $text)){
            $text = Add-Description $text "$title — $($cat.Desc)"
            $descAdded++
        }

        if((Count-InternalLinks $text)-lt 3 -and -not $text.Contains($Marker)){
            $valid=@()

            foreach($h in $cat.Hubs){
                $targetPath = Join-Path $Docs $h[1].Replace('/','\')
                if(Test-Path $targetPath){
                    if((Resolve-Path $targetPath).Path -ne (Resolve-Path $p.FullName).Path){
                        $r = Get-RelativePathCompat $p.FullName (Resolve-Path $targetPath).Path
                        $valid += ,@($h[0],$r)
                    }
                }
            }

            if($valid.Count -gt 0){
                $block="`r`n`r`n$Marker`r`n## 관련 핵심 문서`r`n`r`n"
                foreach($v in $valid){
                    $block += "- [$($v[0])]($($v[1]))`r`n"
                }
                $text = $text.TrimEnd() + $block
                $linksAdded++
            }
        }

        if($text -ne $orig){
            Backup-File $p.FullName $rel
            Set-Content $p.FullName $text -Encoding UTF8
            $changed++
        }
    }

    $afterFiles = Get-ChildItem $Docs -Recurse -File -Filter *.md
    $afterDesc=0
    $afterLow=0

    foreach($p in $afterFiles){
        $t=Get-Content $p.FullName -Raw -Encoding UTF8
        if(-not(Has-Description $t)){ $afterDesc++ }
        if((Count-InternalLinks $t)-lt 3){ $afterLow++ }
    }

    $rep=@"
# ONE SHOT FIX REPORT V2

## 실제 적용 결과
- 전체 Markdown: $($afterFiles.Count)
- 수정 문서: $changed
- description 실제 추가: $descAdded
- 내부링크 블록 실제 추가: $linksAdded

## 전후 비교
- description 누락: **$beforeDesc → $afterDesc**
- 내부링크 3개 미만: **$beforeLow → $afterLow**

## 제외
templates / guide / references / policy / clinical-template 등은 의도적으로 제외했습니다.

## 안전
모든 수정 전 원본은 ONE_SHOT_BACKUP_V2 폴더에 백업했습니다.
"@

    Set-Content $Report $rep -Encoding UTF8

    Write-Host ""
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host "ONE-SHOT V2 실제 수정 + 자체 검증 완료" -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host "수정 문서: $changed"
    Write-Host "description 누락: $beforeDesc -> $afterDesc" -ForegroundColor Cyan
    Write-Host "내부링크 3개 미만: $beforeLow -> $afterLow" -ForegroundColor Cyan
    Write-Host "보고서: ONE_SHOT_FIX_REPORT_V2.md"
    Write-Host ""

    if($changed -eq 0){
        Write-Host "WARNING: 수정된 문서가 0개입니다. Commit하지 마세요." -ForegroundColor Red
    }
}
catch {
    Write-Host ""
    Write-Host "==============================================" -ForegroundColor Red
    Write-Host "실행 오류" -ForegroundColor Red
    Write-Host "==============================================" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "오류 상세는 ONE_SHOT_ERROR_LOG.txt 에도 저장됩니다." -ForegroundColor Yellow
    ($_ | Out-String) | Set-Content (Join-Path $Root "ONE_SHOT_ERROR_LOG.txt") -Encoding UTF8
}

Write-Host ""
Read-Host "Enter를 누르면 창이 닫힙니다"
