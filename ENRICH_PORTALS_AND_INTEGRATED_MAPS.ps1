$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "PORTAL_MAP_BACKUP_STEP6"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$Marker="<!-- MINSEONG_PORTAL_MAP_ENRICH_V1 -->"

$Targets=@(
@{File="diagnostics/index.md"; Desc="한의학의 진단·변증 체계를 팔강·장부·기혈진액·병인병기와 임상 의사결정으로 연결하는 진단 허브입니다."; Body=@"
## 진단·변증을 어떻게 탐색하나요?

한의학의 진단은 하나의 증상만 보는 것이 아니라 **한열·허실·표리·음양, 장부, 기혈진액, 병인·병기와 증상의 시간적 변화**를 함께 해석합니다.

### 핵심 흐름

- 증상과 생활패턴 파악
- 위험신호와 서양의학적 감별
- 팔강변증으로 큰 방향 설정
- 장부·기혈진액·병인병기로 세분화
- 치법과 방제·본초·침구로 연결
- 치료 후 반응을 재평가

이 허브는 환자 증상에서 전문적인 변증 체계로 넘어가는 관문 역할을 합니다.
"@},
@{File="research/index.md"; Desc="한의학 관련 현대 연구를 임상시험·체계적 문헌고찰·메타분석·관찰연구·기전연구의 층위로 탐색하는 연구 허브입니다."; Body=@"
## 현대 연구를 어떻게 읽나요?

한의학 연구는 연구 설계에 따라 의미가 다릅니다. **무작위대조시험, 체계적 문헌고찰·메타분석, 관찰연구, 증례, 전임상·기전연구**를 구분해서 읽는 것이 중요합니다.

### 연구를 따라가는 순서

1. 어떤 질문을 다루는 연구인지 확인
2. 연구설계와 대상자·중재·비교군 확인
3. 효과크기와 불확실성 확인
4. 안전성·이상반응 확인
5. 실제 임상에 얼마나 적용 가능한지 판단
6. 전통적 사용과 현대 연구결과를 구분

가능한 경우 PMID·DOI 등 식별자를 통해 원문으로 추적합니다.
"@},
@{File="foundations-clinical/integrated-map.md"; Desc="음양오행·장부·기혈진액·병인병기·변증·치법을 실제 임상 흐름으로 연결하는 한의학 기초 통합 지도입니다."; Body=@"
## 한의학 기초에서 임상으로

**음양·오행 → 장부 → 기혈진액 → 병인·병기 → 변증 → 치법 → 본초·방제·침구**의 흐름으로 연결합니다.

이 지도는 개념을 따로 암기하는 용도가 아니라, 환자의 실제 증상을 어떤 틀로 해석하고 치료 방향으로 연결하는지 보여주는 임상형 지식지도입니다.
"@},
@{File="symptom-clinical/integrated-map.md"; Desc="환자 증상에서 감별·위험신호·기능평가·한의학적 병증·치료전략으로 이어지는 증상 임상 통합 지도입니다."; Body=@"
## 증상에서 임상 판단으로

환자의 표현을 그대로 출발점으로 삼되, 다음 단계로 깊어집니다.

**생활언어 → 증상 패턴 → 위험신호 → 주요 감별 → 기능평가 → 한의학적 병증 → 한약·침구·약침 → 경과평가**

피로·소화·수면·통증·비염·어지럼·두근거림 등 여러 증상이 동시에 나타날 때도 이 흐름을 사용합니다.
"@},
@{File="herbal-formula-clinical/integrated-map.md"; Desc="환자 증상과 병증에서 치법·본초·방제·처방구조·경과조정까지 연결하는 본초·방제 임상 통합 지도입니다."; Body=@"
## 본초·방제를 임상에서 연결하는 순서

**증상 → 병증 → 치법 → 핵심 본초 → 방제 → 가감 → 경과 재평가**

같은 증상이라도 한열·허실·기혈진액·소화·수면·연령에 따라 다른 처방이 선택될 수 있습니다. 이 지도는 한약을 '제품명'이 아니라 **병증과 배합구조**로 이해하도록 연결합니다.
"@},
@{File="acupuncture-clinical/integrated-map.md"; Desc="통증·저림·기능저하에서 해부학·MPS·경혈·침·전침·약침·안전·재평가로 연결하는 침구 임상 통합 지도입니다."; Body=@"
## 침구치료 임상 지도

침구치료는 단순히 '어디가 아픈가'만 보지 않습니다.

**통증 위치 → 유발동작 → ROM·근력·신경증상 → MPS·해부학적 구조 → 경혈·치료점 → 침·전침·약침 → 안전성 → 경과평가**

근골격 통증과 자율신경·소화·수면 등 전신 증상은 서로 다른 치료축으로 연결할 수 있습니다.
"@},
@{File="evidence-clinical/integrated-map.md"; Desc="고전·현대 연구·근거수준·임상 적용을 구분해 한의학 근거를 해석하는 통합 지도입니다."; Body=@"
## 근거를 임상으로 연결하기

근거를 한 줄의 '효과 있음/없음'으로 단순화하지 않습니다.

- 고전·원전의 전통적 근거
- 임상시험과 체계적 문헌고찰
- 관찰연구와 증례
- 기전·전임상 연구
- 진료지침과 실제 적용 가능성

각 근거의 성격과 한계를 구분하고, 환자의 상태와 치료목표에 맞춰 해석합니다.
"@},
@{File="zangfu-pattern-network/integrated-map.md"; Desc="장부변증을 비위·간담·심소장·폐대장·신방광의 증상군과 치법·방제로 연결하는 통합 지도입니다."; Body=@"
## 장부변증 통합 지도

장부변증은 장기의 해부학적 질환명과 동일한 개념이 아니라, **증상·기능·기혈진액·한열허실을 장부 기능체계로 해석하는 한의학적 틀**입니다.

비·위, 간·담, 심·소장, 폐·대장, 신·방광의 주요 병증을 서로 비교하고 치법·본초·방제로 연결합니다.
"@},
@{File="eight-principles-network/integrated-map.md"; Desc="팔강변증의 표리·한열·허실·음양을 증상 패턴과 치료 방향으로 연결하는 통합 지도입니다."; Body=@"
## 팔강변증 통합 지도

팔강은 복잡한 증상을 **표리·한열·허실·음양**의 큰 축으로 정리하는 기본 틀입니다.

팔강만으로 처방을 결정하지 않고, 장부·기혈진액·병인병기와 결합해 실제 치료방향으로 세분화합니다.
"@},
@{File="portal/conditions.md"; Desc="환자 생활언어에서 증상·질환·위험신호·한의학적 병증·치료지식으로 들어가는 증상 포털입니다."; Body=@"
## 증상·질환 포털

질환명을 몰라도 **피곤해요, 잠이 안 와요, 소화가 안 돼요, 허리가 아파요**처럼 실제 표현에서 시작할 수 있습니다.

환자용 설명 → 임상 심화 → 한약·침구·연구근거까지 단계적으로 연결합니다.
"@},
@{File="portal/herbs-formulas.md"; Desc="본초와 방제를 증상·병증·치법·배합구조·임상 활용으로 탐색하는 한약 포털입니다."; Body=@"
## 본초·방제 포털

약재명이나 처방명뿐 아니라 **피로, 소화, 수면, 통증, 비염, 여성건강** 같은 증상에서 본초와 방제로 들어갈 수 있습니다.

본초 → 방제 → 병증 → 환자 증상 → 현대 연구근거가 서로 연결됩니다.
"@},
@{File="portal/acupuncture.md"; Desc="침·전침·약침·경혈·MPS를 증상과 해부학적 기능평가에서 탐색하는 침구 포털입니다."; Body=@"
## 침구·치료 포털

통증 부위나 생활동작에서 시작해 **MPS·경혈·침·전침·약침·안전·치료반응**으로 이어지는 구조입니다.

환자가 검색하는 표현과 임상가가 사용하는 해부학·기능평가 용어를 서로 연결합니다.
"@},
@{File="portal/evidence.md"; Desc="한의학의 고전적 근거와 현대 임상연구를 구분해 탐색하는 연구·근거 포털입니다."; Body=@"
## 연구·근거 포털

전통적 사용과 현대 연구를 같은 수준으로 섞지 않고 **고전·임상시험·체계적 문헌고찰·관찰연구·기전연구**를 구분해 탐색합니다.

가능한 문서는 PMID·DOI를 통해 원문 근거로 이어집니다.
"@},
@{File="portal/basics.md"; Desc="음양오행·장부·기혈진액·병인병기·변증치법을 한의학 전체 구조 안에서 이해하는 기초 포털입니다."; Body=@"
## 한의학 기초 포털

한의학의 기초개념을 개별 용어로 끝내지 않고 **증상 해석과 치료 방향**으로 연결합니다.

음양·오행 → 장부 → 기혈진액 → 병인병기 → 변증 → 치법의 흐름으로 탐색합니다.
"@},
@{File="portal/maps.md"; Desc="민성 한의학 아카이브의 주요 통합지도와 검색경로를 한곳에서 연결하는 지식지도 포털입니다."; Body=@"
## 지식지도·안내

아카이브의 핵심은 문서 개수가 아니라 **문서 사이의 연결관계**입니다.

환자 생활언어, 증상·질환, 병증, 방제, 본초, 경혈·침구, 고전, 현대 연구를 여러 통합지도를 통해 오갈 수 있습니다.
"@}
)

function Add-Description([string]$text,[string]$desc){
    if($text -match '(?s)^---\s*\r?\n(.*?)\r?\n---'){
        $fm=$Matches[1]
        if($fm -match '(?m)^description:\s*.*$'){
            $newfm=[regex]::Replace($fm,'(?m)^description:\s*.*$',"description: $desc",1)
        } else { $newfm=$fm.TrimEnd()+"`r`ndescription: $desc" }
        return [regex]::Replace($text,'(?s)^---\s*\r?\n.*?\r?\n---',"---`r`n$newfm`r`n---",1)
    }
    return "---`r`ndescription: $desc`r`n---`r`n"+$text
}

$changed=0
foreach($item in $Targets){
    $p=Join-Path $Docs $item.File
    if(-not (Test-Path $p)){ Write-Host "SKIP missing: $($item.File)" -ForegroundColor Yellow; continue }
    $text=Get-Content $p -Raw -Encoding UTF8
    if($text.Contains($Marker)){ Write-Host "SKIP already enriched: $($item.File)"; continue }

    $b=Join-Path $Backup $item.File
    New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent) | Out-Null
    Copy-Item $p $b -Force

    $text=Add-Description $text $item.Desc
    $block="`r`n`r`n$Marker`r`n"+$item.Body.Trim()+"`r`n"
    Set-Content $p ($text.TrimEnd()+$block) -Encoding UTF8
    Write-Host "ENRICHED MAP/PORTAL: $($item.File)" -ForegroundColor Green
    $changed++
}

Write-Host ""
Write-Host "STEP 6 완료: $changed 개 포털·통합지도 보강" -ForegroundColor Cyan
Write-Host "원본 백업: PORTAL_MAP_BACKUP_STEP6"
Read-Host "Enter를 누르면 종료합니다"
