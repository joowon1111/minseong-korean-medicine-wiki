$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(-not(Test-Path "docs")){throw "docs folder not found"}
$stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_clinical11_"+$stamp;New-Item -ItemType Directory -Force $bk|Out-Null
foreach($p in @("docs\\herbs\\index.md","docs\\formulas\\index.md","docs\\acupuncture\\index.md","docs\\pillar\\acupuncture-treatment.md","docs\\ai-index.md")){if(Test-Path $p){Copy-Item $p (Join-Path $bk ($p.Replace("\\","_"))) -Force}}
foreach($x in Get-ChildItem "_payload\\herbs" -File){$d=Join-Path "docs\\herbs" $x.Name;if(-not(Test-Path $d)){Copy-Item $x.FullName $d}}
foreach($x in Get-ChildItem "_payload\\formulas" -File){$d=Join-Path "docs\\formulas" $x.Name;if(-not(Test-Path $d)){Copy-Item $x.FullName $d}}
foreach($x in Get-ChildItem "_payload\\points" -File){$d=Join-Path "docs\\acupuncture\\points" $x.Name;if(-not(Test-Path $d)){Copy-Item $x.FullName $d}}
New-Item -ItemType Directory -Force "docs\\clinical-core"|Out-Null;Copy-Item "_payload\\clinical-core-index.md" "docs\\clinical-core\\index.md" -Force
$line="`r`n`r`n## 임상 핵심 확장`r`n→ [임상 핵심 본초·방제·경혈](../clinical-core/index.md)`r`n"
foreach($p in @("docs\\herbs\\index.md","docs\\formulas\\index.md","docs\\acupuncture\\index.md","docs\\pillar\\acupuncture-treatment.md")){if(Test-Path $p){$t=Get-Content $p -Raw -Encoding UTF8;if($t -notmatch "clinical-core/index.md"){Add-Content $p $line -Encoding UTF8}}}
if(Test-Path "docs\\ai-index.md"){$t=Get-Content "docs\\ai-index.md" -Raw -Encoding UTF8;if($t -notmatch "clinical-core/index.md"){Add-Content "docs\\ai-index.md" "`r`n## 임상 핵심 본초·방제·경혈`r`n- [임상 핵심 통합 허브](clinical-core/index.md)`r`n" -Encoding UTF8}}
Write-Host "CLINICAL CORE EXPANSION 11 COMPLETE" -ForegroundColor Green;Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
