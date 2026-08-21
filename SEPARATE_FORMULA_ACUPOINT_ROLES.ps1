$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$Docs=Join-Path $Root "docs"
if(-not (Test-Path $Docs)){ Write-Host "ERROR: docs 폴더 없음" -ForegroundColor Red; Read-Host; exit 1 }

$Backup=Join-Path $Root "FORMULA_POINT_BACKUP_STEP4"
New-Item -ItemType Directory -Force -Path $Backup | Out-Null
$FormulaMarker="<!-- MINSEONG_FORMULA_ROLE_V1 -->"
$PointMarker="<!-- MINSEONG_POINT_ROLE_V1 -->"

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
function Relative-Link($fromFile,$toFile){
    return [System.IO.Path]::GetRelativePath((Split-Path $fromFile -Parent),$toFile).Replace('\','/')
}

# 대표 방제 문서 vs 고전/심화 문서
$FormulaPairs=@(
@{Primary="formulas/buzhong-yiqi-tang.md"; Deep="formulas/buzhong-yiqi-classic.md"; Name="보중익기탕";
PrimaryText="이 문서는 보중익기탕을 **대표 방제 문서**로 정리합니다. 구성·치법·주요 병증·현대적 검색어를 한눈에 보고, 고전적 의미와 원방 맥락은 심화 문서로 연결합니다.";
DeepText="이 문서는 보중익기탕의 **고전·원방·전통적 병기 해석을 더 깊게 보는 심화 문서**입니다. 대표 문서와 겹치는 기본 설명보다 출전·방의·병증 해석을 중심으로 봅니다."},
@{Primary="formulas/shi-quan-da-bu-tang.md"; Deep="formulas/shiquan-dabu-classic.md"; Name="십전대보탕";
PrimaryText="이 문서는 십전대보탕의 **대표 방제 문서**입니다. 기혈양허·허약·회복기 등 환자 검색과 처방 구조를 연결합니다.";
DeepText="이 문서는 십전대보탕의 **고전적 방의와 원방 맥락을 다루는 심화 문서**입니다. 구성 본초의 역할과 전통적 적응 개념을 대표 문서보다 깊게 봅니다."},
@{Primary="formulas/guibi-tang.md"; Deep="formulas/guipi-classic.md"; Name="귀비탕";
PrimaryText="이 문서는 귀비탕의 **대표 방제 문서**로, 피로·불면·심계·건망·식욕저하 같은 환자 검색어와 심비양허 병증을 연결합니다.";
DeepText="이 문서는 귀비탕의 **고전적 병기·방의 심화**를 담당합니다. 심비양허와 기혈허의 전통적 해석, 구성 본초의 역할을 더 깊게 정리합니다."},
@{Primary="formulas/duhuo-jisheng-tang.md"; Deep="formulas/duhuo-jisheng-classic.md"; Name="독활기생탕";
PrimaryText="이 문서는 독활기생탕의 **대표 방제 문서**로, 만성 요통·관절통·허약·한습 등 환자 검색과 처방 구조를 연결합니다.";
DeepText="이 문서는 독활기생탕의 **고전적 방의와 병증 심화**를 담당합니다. 풍한습비·간신부족·기혈허 등 전통적 조합을 더 깊게 봅니다."}
)

$changed=0
foreach($pair in $FormulaPairs){
    $pp=Join-Path $Docs $pair.Primary
    $dp=Join-Path $Docs $pair.Deep

    if(Test-Path $pp){
        $txt=Get-Content $pp -Raw -Encoding UTF8
        if(-not $txt.Contains($FormulaMarker)){
            Backup-File $pp $pair.Primary
            $txt=Ensure-Description $txt "$($pair.Name)의 구성·치법·주요 병증·환자 검색어를 연결하는 대표 방제 문서입니다."
            $link=if(Test-Path $dp){ Relative-Link $pp $dp } else { $null }
            $block="`r`n`r`n$FormulaMarker`r`n## 이 문서의 역할`r`n`r`n$($pair.PrimaryText)`r`n"
            if($link){ $block+="`r`n고전적 방의와 원방 맥락은 [$($pair.Name) 고전·심화 문서]($link)에서 이어서 볼 수 있습니다.`r`n" }
            Set-Content $pp ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "FORMULA PRIMARY: $($pair.Primary)" -ForegroundColor Green
            $changed++
        }
    } else { Write-Host "SKIP missing primary: $($pair.Primary)" -ForegroundColor Yellow }

    if(Test-Path $dp){
        $txt=Get-Content $dp -Raw -Encoding UTF8
        if(-not $txt.Contains($FormulaMarker)){
            Backup-File $dp $pair.Deep
            $txt=Ensure-Description $txt "$($pair.Name)의 고전 출전·방의·전통적 병증 해석을 다루는 심화 방제 문서입니다."
            $link=if(Test-Path $pp){ Relative-Link $dp $pp } else { $null }
            $block="`r`n`r`n$FormulaMarker`r`n## 이 문서의 역할`r`n`r`n$($pair.DeepText)`r`n"
            if($link){ $block+="`r`n기본 구성과 환자 검색 중심 설명은 [$($pair.Name) 대표 문서]($link)에서 먼저 볼 수 있습니다.`r`n" }
            Set-Content $dp ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "FORMULA DEEP: $($pair.Deep)" -ForegroundColor Cyan
            $changed++
        }
    }
}

# 경혈 네트워크 문서 vs 경혈 상세 문서
$PointPairs=@(
@{Network="acupoint-network/li4.md"; Detail="acupuncture/points/li4-hegu.md"; Name="합곡 LI4"},
@{Network="acupoint-network/sp6.md"; Detail="acupuncture/points/sp6-sanyinjiao.md"; Name="삼음교 SP6"},
@{Network="acupoint-network/pc6.md"; Detail="acupuncture/points/pc6-neiguan.md"; Name="내관 PC6"},
@{Network="acupoint-network/gv20.md"; Detail="acupuncture/points/gv20-baihui.md"; Name="백회 GV20"},
@{Network="acupoint-network/bl23.md"; Detail="acupuncture/points/bl23-shenshu.md"; Name="신수 BL23"},
@{Network="acupoint-network/bl40.md"; Detail="acupuncture/points/bl40-weizhong.md"; Name="위중 BL40"},
@{Network="acupoint-network/ht7.md"; Detail="acupuncture/points/ht7-shenmen.md"; Name="신문 HT7"},
@{Network="acupoint-network/st36.md"; Detail="acupuncture/points/st36-zusanli.md"; Name="족삼리 ST36"}
)

foreach($pair in $PointPairs){
    $np=Join-Path $Docs $pair.Network
    $dp=Join-Path $Docs $pair.Detail

    if(Test-Path $np){
        $txt=Get-Content $np -Raw -Encoding UTF8
        if(-not $txt.Contains($PointMarker)){
            Backup-File $np $pair.Network
            $txt=Ensure-Description $txt "$($pair.Name)을 증상·경락·관련 경혈과 연결하는 경혈 네트워크 문서입니다."
            $link=if(Test-Path $dp){ Relative-Link $np $dp } else { $null }
            $block="`r`n`r`n$PointMarker`r`n## 이 문서의 역할`r`n`r`n이 문서는 **경혈 네트워크 관점**에서 $($pair.Name)을 봅니다. 어떤 증상군·경락·다른 경혈과 연결되는지 탐색하는 지식지도 역할을 합니다.`r`n"
            if($link){ $block+="`r`n정확한 위치·취혈·해부학·자침 관련 상세 설명은 [$($pair.Name) 상세 문서]($link)에서 이어서 볼 수 있습니다.`r`n" }
            Set-Content $np ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "POINT NETWORK: $($pair.Network)" -ForegroundColor Green
            $changed++
        }
    }

    if(Test-Path $dp){
        $txt=Get-Content $dp -Raw -Encoding UTF8
        if(-not $txt.Contains($PointMarker)){
            Backup-File $dp $pair.Detail
            $txt=Ensure-Description $txt "$($pair.Name)의 위치·취혈·해부학적 구조·자침 안전을 중심으로 정리한 경혈 상세 문서입니다."
            $link=if(Test-Path $np){ Relative-Link $dp $np } else { $null }
            $block="`r`n`r`n$PointMarker`r`n## 이 문서의 역할`r`n`r`n이 문서는 **경혈 상세 문서**로 $($pair.Name)의 위치·취혈·해부학적 구조와 안전한 자침을 중심으로 봅니다.`r`n"
            if($link){ $block+="`r`n증상·경락·다른 경혈과의 연결은 [$($pair.Name) 네트워크 문서]($link)에서 볼 수 있습니다.`r`n" }
            Set-Content $dp ($txt.TrimEnd()+$block) -Encoding UTF8
            Write-Host "POINT DETAIL: $($pair.Detail)" -ForegroundColor Cyan
            $changed++
        }
    }
}

Write-Host ""
Write-Host "STEP 4 완료: $changed 개 방제·경혈 문서 역할·상호링크 보강" -ForegroundColor Cyan
Write-Host "삭제/병합된 문서는 없습니다."
Write-Host "원본 백업: FORMULA_POINT_BACKUP_STEP4"
Read-Host "Enter를 누르면 종료합니다"
