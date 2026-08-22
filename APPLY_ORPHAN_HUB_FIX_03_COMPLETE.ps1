$ErrorActionPreference="Stop"
function Upsert($target,$start,$end,$payload,$heading){
  if(-not(Test-Path $target)){throw "$target not found"}
  $body=Get-Content $payload -Raw -Encoding UTF8
  $block=$start+"`r`n`r`n## "+$heading+"`r`n`r`n"+$body+"`r`n"+$end
  $t=Get-Content $target -Raw -Encoding UTF8
  if($t.Contains($start)){
    $pat=[regex]::Escape($start)+".*?"+[regex]::Escape($end)
    $t=[regex]::Replace($t,$pat,$block,[Text.RegularExpressions.RegexOptions]::Singleline)
  }else{$t=$t.TrimEnd()+"`r`n`r`n"+$block+"`r`n"}
  Set-Content $target $t -Encoding UTF8
}
try{
  $R=Split-Path -Parent $MyInvocation.MyCommand.Path;Set-Location $R
  if(-not(Test-Path "docs")){throw "docs folder not found"}
  $stamp=Get-Date -Format "yyyyMMdd-HHmmss";$bk="_backup_orphan_hubs_"+$stamp
  New-Item -ItemType Directory -Force $bk|Out-Null
  foreach($p in @("docs\conditions\index.md","docs\answer-guides\index.md","docs\ai-index.md")){
    if(Test-Path $p){$dest=Join-Path $bk ($p.Replace("\","_"));Copy-Item $p $dest -Force}
  }
  if(-not(Test-Path "docs\answer-guides")){New-Item -ItemType Directory -Force "docs\answer-guides"|Out-Null}
  if(-not(Test-Path "docs\answer-guides\index.md")){
@'
---
title: AI 질문형 답변 가이드
description: 환자가 실제로 검색하는 자연어 질문을 증상과 주제별로 찾아보는 민성 한의학 아카이브 답변 가이드입니다.
---
# AI 질문형 답변 가이드

실제 환자가 묻는 자연어 질문을 분야별로 탐색할 수 있습니다.
'@ | Set-Content "docs\answer-guides\index.md" -Encoding UTF8
  }
  Upsert "docs\conditions\index.md" "<!-- ORPHAN_CONDITIONS_HUB_START -->" "<!-- ORPHAN_CONDITIONS_HUB_END -->" "_hub_payload\conditions_orphans.md" "증상·질환 상세 문서 더 찾아보기"
  Upsert "docs\answer-guides\index.md" "<!-- ORPHAN_ANSWERS_HUB_START -->" "<!-- ORPHAN_ANSWERS_HUB_END -->" "_hub_payload\answer_orphans.md" "자연어 질문 전체 탐색"
  if(Test-Path "docs\ai-index.md"){
    $s="<!-- ORPHAN_HUB_LINKS_START -->";$e="<!-- ORPHAN_HUB_LINKS_END -->"
    $b=@'
<!-- ORPHAN_HUB_LINKS_START -->

## 전체 증상·질문 더 찾아보기

- [증상·질환 전체 상세 색인](conditions/index.md)
- [AI 자연어 질문 전체 가이드](answer-guides/index.md)

세부 문서를 상단 메뉴에 모두 나열하지 않고 **핵심 색인 → 분야별 허브 → 세부 문서**로 연결합니다.

<!-- ORPHAN_HUB_LINKS_END -->
'@
    $t=Get-Content "docs\ai-index.md" -Raw -Encoding UTF8
    if($t.Contains($s)){
      $pat=[regex]::Escape($s)+".*?"+[regex]::Escape($e)
      $t=[regex]::Replace($t,$pat,$b,[Text.RegularExpressions.RegexOptions]::Singleline)
    }else{$t=$t.TrimEnd()+"`r`n`r`n"+$b}
    Set-Content "docs\ai-index.md" $t -Encoding UTF8
  }
  Write-Host "ORPHAN HUB FIX 03 COMPLETE" -ForegroundColor Green
  Write-Host "Exact audited orphan pages are now linked through hubs." -ForegroundColor Green
  Write-Host ("Backup: "+$bk) -ForegroundColor Yellow
}catch{Write-Host ("ERROR: "+$_.Exception.Message) -ForegroundColor Red}
Read-Host "Press Enter to close"
