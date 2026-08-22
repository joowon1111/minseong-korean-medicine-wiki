37 FIXED

오류 원인:
기존 APPLY PowerShell에 RUN_DUPLICATE_AWARE_AUDIT_37.py를 자기 자신에게 Copy-Item 하는 잘못된 한 줄이 있었습니다.

이번 수정:
- 자기 자신 복사 명령 완전 제거
- APPLY 성공/실패를 APPLY_37_STATUS.txt에 기록
- 적용과 감사를 완전히 분리
- 감사도 Python 없이 PowerShell-only FIXED BAT 제공
- 기존 bridge/canonical 구조는 그대로 유지

실행 순서:
1) ZIP을 저장소 최상위에 덮어쓰기
2) APPLY_DUPLICATE_LAYER_CONSOLIDATION_37_FIXED.bat 실행
3) "DUPLICATE LAYER CONSOLIDATION 37 FIXED COMPLETE" 확인
4) Commit / Push → GitHub Actions 초록불
5) 그 후 선택적으로 RUN_DUPLICATE_AWARE_AUDIT_37_FIXED.bat 실행

감사 성공 시:
_quality_audit_37/AUDIT_REPORT_37.md
_quality_audit_37/AUDIT_RANKING_37.tsv
_quality_audit_37/AUDIT_PROGRESS.txt
_quality_audit_37/AUDIT_ERROR_FULL.txt
