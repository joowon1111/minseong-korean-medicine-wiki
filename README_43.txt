43단계 — WHO 표준 361경혈 + 경외기혈 통합 대형 패치

핵심 원칙
- 별도의 새 아틀라스를 기존 자료 뒤에 단순 추가하지 않습니다.
- 기존 docs/acupuncture/points의 개별 경혈 문서를 WHO 표준 위치·취혈 블록으로 직접 보강합니다.
- 33단계 등에서 이미 작성한 효능·배혈·현대연구 내용은 삭제하지 않고 그대로 보존합니다.
- 동일 코드 기존 페이지가 있으면 그 페이지가 canonical이며, 없는 혈만 새 페이지를 생성합니다.
- acupoint-network / meridian-network / 침구 임상 허브에 표준 아틀라스 연결을 통합합니다.
- 특정혈(원혈·락혈·극혈·오수혈·하합혈·팔회혈·모혈·배수혈·팔맥교회혈)을 개별 경혈에 교차 연결합니다.
- 361혈 + 경외기혈 데이터의 위치·취혈·자침 정보를 한 번에 처리합니다.
- 마지막에 경맥별 혈수와 누락 코드를 자동 검증합니다.

데이터 기준
1) WHO Standard Acupuncture Point Locations in the Western Pacific Region (2008)
2) KMCRIC 표준경혈 DB — WHO 표준 기반 위치·취혈·자침·주의
3) KM-Agent acupoints.csv — WHO 표준 기반 구조화 데이터, CC BY 4.0
   https://github.com/wonyung-lee/km-agent

실행
APPLY_COMPLETE_STANDARD_ACUPOINT_ATLAS_43.bat

성공 문구
COMPLETE STANDARD ACUPOINT ATLAS 43 COMPLETE

검증 파일
_quality_audit_43/43_VALIDATION_REPORT.md
APPLY_43_STATUS.txt

GitHub Desktop Summary
Build complete WHO-standard clinical acupoint atlas

GitHub Desktop Description
Integrate all standard acupoints into the existing meridian, special-point, clinical, anatomy, safety, and evidence knowledge networks.
