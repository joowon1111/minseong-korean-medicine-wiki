$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
if(!(Test-Path "docs")){throw "docs not found"}
$bk="_backup_sasang_classics34_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
foreach($src in Get-ChildItem "_payload\docs" -Recurse -File){
 $rel=$src.FullName.Substring((Resolve-Path "_payload\docs").Path.Length+1)
 $dest=Join-Path "docs" $rel
 $dir=Split-Path $dest -Parent
 if(!(Test-Path $dir)){New-Item -ItemType Directory -Force $dir|Out-Null}
 if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ($rel.Replace("\","_"))) -Force}
 Copy-Item $src.FullName $dest -Force
}
Write-Host "SASANG CLASSICS DETAIL MODERNIZATION 34 COMPLETE" -ForegroundColor Green
Write-Host "7 legacy/detail pages integrated or rebuilt in place, not appended." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
