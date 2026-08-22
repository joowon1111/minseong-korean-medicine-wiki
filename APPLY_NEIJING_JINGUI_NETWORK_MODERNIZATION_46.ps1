$ErrorActionPreference="Stop"
try{
$R=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $R
if(!(Test-Path "docs")){throw "docs not found"}

$bk="_backup_neijing_jingui46_"+(Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force $bk|Out-Null
$count=0

foreach($s in Get-ChildItem "_payload\docs" -Recurse -File){
    $rel=$s.FullName.Substring((Resolve-Path "_payload\docs").Path.Length+1)
    $dest=Join-Path "docs" $rel
    $dir=Split-Path $dest -Parent

    if(!(Test-Path $dir)){New-Item -ItemType Directory -Force $dir|Out-Null}
    if(Test-Path $dest){Copy-Item $dest (Join-Path $bk ($rel.Replace("\","_"))) -Force}
    Copy-Item $s.FullName $dest -Force
    $count++
}

Write-Host "NEIJING JINGUI NETWORK MODERNIZATION 46 COMPLETE" -ForegroundColor Green
Write-Host ("Updated pages: "+$count) -ForegroundColor Cyan
Write-Host "Neijing and Jingui clinical networks rebuilt in place without duplicate append layers." -ForegroundColor Cyan
Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{
Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
