$ErrorActionPreference="Stop"
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

try {
  if (!(Test-Path "docs")) { throw "docs folder not found" }

  $Names=@(
    "irritable-bowel-syndrome",
    "functional-constipation",
    "anxiety",
    "menopause",
    "chronic-prostatitis-cpps",
    "overactive-bladder",
    "asthma",
    "copd",
    "diabetic-peripheral-neuropathy",
    "parkinson-disease",
    "chemotherapy-nausea-vomiting",
    "chemotherapy-induced-peripheral-neuropathy",
    "radiation-xerostomia",
    "insomnia",
    "fatigue",
    "depression",
    "dyspnea",
    "postpartum-lactation",
    "sciatica",
    "frozen-shoulder",
    "hip-osteoarthritis",
    "musculoskeletal-evidence-overview",
    "female-infertility-art",
    "postoperative-nausea-vomiting",
    "cancer-related-fatigue",
    "acupuncture-positive-evidence-map"
  )

  $changed=0
  foreach($File in Get-ChildItem "docs" -Recurse -File -Filter "*.md") {
    $Text=Get-Content $File.FullName -Raw -Encoding UTF8
    $New=$Text
    foreach($Name in $Names) {
      # Absolute/source-style references
      $New=$New.Replace("/authority/conditions/"+$Name+".md", "/authority/conditions/"+$Name+"/")
      $New=$New.Replace("authority/conditions/"+$Name+".md", "/authority/conditions/"+$Name+"/")
      # Same-directory Markdown links such as (name.md)
      $New=$New.Replace("(" + $Name + ".md)", "(/authority/conditions/" + $Name + "/)")
    }
    if($New -ne $Text) {
      Set-Content $File.FullName $New -Encoding UTF8
      $changed++
    }
  }

  Write-Host "CONDITION PUBLIC URL FIX 72 COMPLETE" -ForegroundColor Green
  Write-Host ("Changed markdown files: "+$changed) -ForegroundColor Cyan
  Write-Host "mkdocs.yml was NOT modified." -ForegroundColor Yellow
}
catch {
  Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red
}
Read-Host "Press Enter to close"
