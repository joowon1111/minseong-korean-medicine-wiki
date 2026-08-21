$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "ROLE_SEPARATION_BACKUP_STEP3"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$PatientMarker="<!-- MINSEONG_PATIENT_ROLE_V1 -->"
$ClinicalMarker="<!-- MINSEONG_CLINICAL_ROLE_V1 -->"

$Pairs=@(
@{Patient="conditions/low-back-pain.md"; Clinical="symptom-clinical/low-back-pain.md"; Name="요통";
PatientText="이 문서는 **환자가 느끼는 허리통증을 생활언어에서 이해하기 위한 입구**입니다. 언제 아픈지, 다리저림이 있는지, 오래 앉기·운전·걷기와 어떤 관계가 있는지부터 살펴보고 필요한 감별과 치료 정보를 찾아갑니다.";
ClinicalText="이 문서는 요통을 **임상적으로 감별하고 치료전략을 정리하는 심화 문서**입니다. 통증 분포, 신경학적 증상, 기능저하, 위험신호와 치료반응을 구조적으로 평가합니다."},
@{Patient="conditions/shoulder-pain.md"; Clinical="symptom-clinical/shoulder-pain.md"; Name="어깨통증";
PatientText="이 문서는 **팔을 들 때 아픔, 옷 입기 불편, 야간통 등 환자가 실제로 표현하는 어깨 증상**에서 시작합니다. 일상동작과 통증 위치를 바탕으로 관련 질환·침·약침·재활 지식으로 연결합니다.";
ClinicalText="이 문서는 어깨통증의 **임상 감별과 기능평가 심화**를 담당합니다. 능동·수동 ROM, 근력, 회전근개·오십견·경추성 통증 등 주요 감별축과 치료경과를 봅니다."},
@{Patient="conditions/dyspepsia.md"; Clinical="symptom-clinical/dyspepsia.md"; Name="소화불량";
PatientText="이 문서는 **더부룩함, 체기, 조기포만, 트림, 식후불편처럼 환자가 실제로 느끼는 소화 증상**에서 시작합니다. 식사와의 관계와 동반증상을 살펴 한약·방제·경혈 지식으로 연결합니다.";
ClinicalText="이 문서는 소화불량의 **임상적 증상군 분류와 감별 심화**를 담당합니다. 증상 지속기간, 경고증상, 식사·배변 패턴과 비허·담습·식적 등 한의학적 병증을 구조적으로 연결합니다."},
@{Patient="conditions/rhinitis.md"; Clinical="symptom-clinical/rhinitis.md"; Name="비염";
PatientText="이 문서는 **콧물, 재채기, 코막힘, 후비루처럼 환자가 검색하는 비염 증상**에서 시작합니다. 계절성·유발요인·감기와의 차이를 살펴 관련 한약·침구 자료로 연결합니다.";
ClinicalText="이 문서는 비염의 **임상 감별과 치료전략 심화**를 담당합니다. 증상 양상, 지속성, 동반 호흡기 증상과 풍한·풍열·담습·폐비기허 등의 병증을 함께 봅니다."},
@{Patient="conditions/headache.md"; Clinical="symptom-clinical/headache.md"; Name="두통";
PatientText="이 문서는 **머리가 지끈거려요, 뒷머리가 당겨요, 한쪽 머리가 아파요 같은 환자 표현**에서 시작합니다. 시간패턴·유발요인·목 긴장·오심 등을 살펴 관련 두통 유형과 치료정보로 연결합니다.";
ClinicalText="이 문서는 두통의 **임상 감별과 위험신호·치료전략 심화**를 담당합니다. 편두통·긴장형·경추성 양상과 신경학적 위험신호, 치료반응을 구조적으로 평가합니다."},
@{Patient="conditions/insomnia.md"; Clinical="symptom-clinical/insomnia.md"; Name="불면";
PatientText="이 문서는 **잠들기 어렵다, 자주 깬다, 새벽에 깬다, 자도 개운하지 않다**처럼 환자가 느끼는 수면 문제에서 시작합니다. 수면패턴과 피로·심계·갱년기·스트레스를 연결해 탐색합니다.";
ClinicalText="이 문서는 불면의 **임상적 패턴 분류와 치료경과 심화**를 담당합니다. 입면·수면유지·조기각성, 낮 기능, 동반 증상과 한의학적 병증을 구조적으로 평가합니다."},
@{Patient="conditions/fatigue.md"; Clinical="symptom-clinical/fatigue.md"; Name="피로";
PatientText="이 문서는 **계속 피곤해요, 자도 피곤해요, 오후만 되면 지쳐요 같은 환자 생활언어**에서 시작합니다. 수면·식욕·소화·활동 후 회복·검사결과와의 관계를 살펴봅니다.";
ClinicalText="이 문서는 피로의 **임상적 원인 감별과 경과평가 심화**를 담당합니다. 지속기간, 기능저하, 수면·영양·내과적 원인과 기허·혈허·기혈양허 등 병증을 구조화합니다."}
)

function Backup-File($p,$rel){
    $b=Join-Path $Backup $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $b -Parent) | Out-Null
    Copy-Item $p $b -Force
}
function Ensure-Description([string]$text,[string]$desc){
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
foreach($pair in $Pairs){
    $pp=Join-Path $Docs $pair.Patient
    $cp=Join-Path $Docs $pair.Clinical

    if(Test-Path $pp){
        $txt=Get-Content $pp -Raw -Encoding UTF8
        if(-not $txt.Contains($PatientMarker)){
            Backup-File $pp $pair.Patient
            $desc="$($pair.Name)을 환자 생활언어와 실제 불편에서 이해하고 위험신호·감별·한의치료·임상 심화 자료로 연결하는 환자용 안내입니다."
            $txt=Ensure-Description $txt $desc
            $rel=[System.IO.Path]::GetRelativePath((Split-Path $pp -Parent),$cp).Replace('\','/')
            $block="`r`n`r`n$PatientMarker`r`n## 이 문서의 역할`r`n`r`n$($pair.PatientText)`r`n`r`n더 전문적인 감별·치료전략은 [$($pair.Name) 임상 심화]($rel)에서 이어서 볼 수 있습니다.`r`n"
            Set-Content $pp ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "PATIENT ROLE: $($pair.Patient)" -ForegroundColor Green
            $changed++
        }
    } else { Write-Host "SKIP patient missing: $($pair.Patient)" -ForegroundColor Yellow }

    if(Test-Path $cp){
        $txt=Get-Content $cp -Raw -Encoding UTF8
        if(-not $txt.Contains($ClinicalMarker)){
            Backup-File $cp $pair.Clinical
            $desc="$($pair.Name)의 임상 감별·위험신호·병증·치료전략·경과평가를 구조화한 한의학 임상 심화 문서입니다."
            $txt=Ensure-Description $txt $desc
            $rel=[System.IO.Path]::GetRelativePath((Split-Path $cp -Parent),$pp).Replace('\','/')
            $block="`r`n`r`n$ClinicalMarker`r`n## 이 문서의 역할`r`n`r`n$($pair.ClinicalText)`r`n`r`n일반적인 증상 설명과 생활언어 검색은 [$($pair.Name) 환자 안내]($rel)에서 먼저 볼 수 있습니다.`r`n"
            Set-Content $cp ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "CLINICAL ROLE: $($pair.Clinical)" -ForegroundColor Cyan
            $changed++
        }
    } else { Write-Host "SKIP clinical missing: $($pair.Clinical)" -ForegroundColor Yellow }
}

Write-Host ""
Write-Host "STEP 3 완료: $changed 개 문서 역할·상호링크 보강" -ForegroundColor Cyan
Write-Host "삭제/병합된 문서는 없습니다."
Write-Host "원본 백업: ROLE_SEPARATION_BACKUP_STEP3"
Read-Host "Enter를 누르면 종료합니다"
