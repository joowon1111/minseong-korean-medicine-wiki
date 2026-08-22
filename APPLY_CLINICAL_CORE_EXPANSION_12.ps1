$ErrorActionPreference="Stop"
function CopyMissing($src,$dst){foreach($x in Get-ChildItem $src -File){$d=Join-Path $dst $x.Name;if(-not(Test-Path $d)){Copy-Item $x.FullName $d}}}
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R;if(-not(Test-Path "docs\clinical-core\index.md")){throw "11단계 임상 핵심 허브가 없습니다."}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_clinical12_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\clinical-core\index.md","docs\herbs\index.md","docs\formulas\index.md","docs\acupuncture\index.md","docs\pillar\acupuncture-treatment.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\","_"))) -Force}}
CopyMissing "_payload\herbs" "docs\herbs";CopyMissing "_payload\formulas" "docs\formulas";CopyMissing "_payload\points" "docs\acupuncture\points"
$t=Get-Content "docs\clinical-core\index.md" -Raw -Encoding UTF8;$b=Get-Content "_payload\hub_block.md" -Raw -Encoding UTF8;$s="<!-- CLINICAL_CORE_PHASE2_START -->";$e="<!-- CLINICAL_CORE_PHASE2_END -->"
if($t.Contains($s)){$pat=[regex]::Escape($s)+".*?"+[regex]::Escape($e);$t=[regex]::Replace($t,$pat,$b,[Text.RegularExpressions.RegexOptions]::Singleline)}else{$t=$t.TrimEnd()+"`r`n`r`n"+$b};Set-Content "docs\clinical-core\index.md" $t -Encoding UTF8
Write-Host "CLINICAL CORE EXPANSION 12 COMPLETE" -ForegroundColor Green;Write-Host "Existing pages were not overwritten." -ForegroundColor Cyan;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red};Read-Host "Press Enter to close"
