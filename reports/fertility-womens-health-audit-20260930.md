# 여성의학·난임 전수 점검 및 편집 결정 (2026-09-30)

기준: 최신 기본 브랜치 main `ca8fc234d5dc763e987f9d6d7bf87c4e40a83b06`. 먼저 2,114개 Markdown 전체를 요청 키워드로 검색해 659개 관련 후보의 전문 텍스트·제목·목차·링크와 중복 여부를 조사했다. ‘생리’에는 일반 생리학, ‘임신’에는 본초 안전성의 간접 언급도 포함된다. **659개 모두가 난임 전문 문서인 것은 아니며, 모두를 임상적으로 재검토했다는 의미도 아니다.** 직접 관련 핵심 문서는 전문을 읽고 보강·통합 대상을 선정했다.

분류 1은 현재 보존할 좋은 전문 자료 또는 범위 밖 간접 참조, 2는 내용·근거·연결 보강, 3은 통합, 4는 기존 자료를 상위 지도에 편입, 5는 기존 대응 문서가 없어 독립 설명이 필요한 핵심 신규 문서다. 각 문서의 상세 결정과 키워드는 동명 JSON에 기록했다.

## 통합과 주소 유지

- `conditions/pcos.md` → `conditions/polycystic-ovary-syndrome.md`
- `conditions/preconception-herbal.md` → `conditions/infertility-preconception.md`#preconception-herbal
- `conditions/fertility-fatigue.md` → `conditions/infertility-preconception.md`#whole-health
- `conditions/amenorrhea.md` → `conditions/irregular-menstruation.md`#amenorrhea
- `conditions/scanty-menstruation.md` → `conditions/irregular-menstruation.md`#scanty-menstruation
- `conditions/ovulation-pain.md` → `womens-health/reproductive-physiology.md`#ovulation-pain

## 신규 문서의 이유

정상 생식생리·충임 이론, DOR/AMH·고령, 남성 난임, 내막증·선근증, 난관/내막, 원인불명, RIF·RPL, 변증, 초진 문진, 질염, 창부도담탕·오자연종환은 각각 별도의 독해·검사·감별·안전 또는 출전 질문이 있다. 배란장애·생활관리·FAQ·고령·정액검사·처방 단계별 관리에는 별도의 얇은 페이지를 만들지 않고 핵심 본문에 포함했다. 새로운 세부 문서를 좌측 메뉴에 각각 추가하지 않았다.

## 근거와 편집 원칙

WHO 난임 2025, WHO 정액검사 6판 2021, NICE NG257 2026, ASRM RIF/RPL 2026, AUA/ASRM 남성 지침 2024, PCOS 국제지침 2023, ESHRE 원인불명 2023·내막증 2022·POI 2024·난소자극 2025를 확인했다. 임상임신과 생아출산·배란/호르몬·통증을 구분하고 RCT와 긍정적 고찰의 비교군·비뚤림·한계를 병기했다. 고전 이론을 현대 호르몬·질환과 등치하지 않았다.

《임신 동의보감》은 임신 준비·부부·전신 건강을 연결하는 구성 아이디어만 참고했다. 비공개 본문을 추정하거나 문장·독창적 표현을 옮기지 않았다. 실제 문서는 독립적으로 검토한 고전·지침·논문과 기존 아카이브 자료로 구성했다.

## 최종 검증

- 원본 2,122개 Markdown: 깨진 내부 링크·URL 충돌·중복 제목·정확히 같은 내용·raw HTML .md 링크 0건.
- 생성 사이트: 깨진 링크·앵커 0건. Page discovery 2,117개 대상·17,556개 제목 앵커 검증 통과. 검색은 탐색 대상 제외 정책 때문에 원본 개수와 다르다.
- Python 116개 및 JavaScript 2개 테스트 통과.
- 모든 Markdown front matter YAML 검사 오류 0건. 신규 14개 문서 1,781–6,909자, 각각 본문에서 들어오는 링크 1개 이상.
- 전체 고아 후보도 조사했다. 탐색 메뉴와 자동 추천을 제외한 Markdown 본문 링크만 계산하면 기존 142개가 남으며, 신규 문서의 고아는 0개다. 기존 전문 아틀라스 등을 무관한 난임 페이지에 강제로 연결하지 않았다.
- 새로 인용한 지침·논문을 원문/공식 페이지로 대조하고 잘못된 PMID·ASRM/ESHRE 주소를 수정했다. 일부 외부 사이트의 봇 차단·결제/접근 제한은 링크 오류와 구분했다.
- 저장소 전체 Git index의 비밀정보 검사 통과. 공개 검토 날짜를 일괄 변경하지 않았고 세부 문서의 독립 메뉴를 추가하지 않았다.

## 분류별 전체 목록

| 기존 경로 | 분류 | 결정 |
|---|---|---|
| `docs/acupoint-network/by-condition.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupoint-network/standard-atlas.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/extra-points/ex-ca1.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl10-tianzhu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl13-feishu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl17-geshu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl18-ganshu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl20-pishu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl24.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/bl25-dachangshu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl28-pangguangshu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl31.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/bl32.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/bl57-chengshan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl60-kunlun.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl62-shenmai.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/bl67.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/cv17-danzhong.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/cv19.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/cv2.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/cv3.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/cv4-guanyuan.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/acupuncture/points/cv5.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/cv6-qihai.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/cv7.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ex-hn3-yintang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gb21-jianjing.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gb26.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/gb28.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/gb30-huantiao.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gb39-xuanzhong.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gb40-qiuxu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gb41.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/gv14-dazhui.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gv2.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/gv26-shuigou.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/gv4-mingmen.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ht3-shaohai.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/ht5-tongli.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/ki1-yongquan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/ki12.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ki13.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ki14.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ki2.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ki5.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/ki6-zhaohai.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/ki7-fuliu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/ki8.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/li10-shousanli.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/li11-quchi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/li15-jianyu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/li20-yingxiang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/li4-hegu.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr1.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr11.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr13-zhangmen.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/lr14-qimen.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/lr2.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr3-taichong.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr5.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr8-ququan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lr9.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/lu1-zhongfu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/lu5-chize.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/lu9-taiyuan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/pc4-ximen.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/pc7-daling.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/si11-tianzong.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/si3-houxi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/si6-yanglao.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/sp1.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/sp10-xuehai.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/sp4-gongsun.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/sp6-sanyinjiao.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/sp8.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/sp9-yinlingquan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st25-tianshu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st26.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/st27.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/st29.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/st30.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture/points/st35-dubi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st37-shangjuxu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st40-fenglong.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st42-chongyang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/st44-neiting.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/te17-yifeng.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture/points/te5-waiguan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/acupoints-meridians.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/evidence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/methods.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/musculoskeletal.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture-integrated/pharmacopuncture.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-integrated/points-for-womens-health.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/acupuncture-integrated/points-meridians.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture-integrated/safety.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-science/autonomic.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-science/brain-central.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-science/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-science/pain-modulation.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-science/peripheral-afferent.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-specific/saam-12-meridians.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/acupuncture-specific/saam-acupuncture.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/acupuncture-specific/saam-evidence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/ai/clinic-knowledge-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/ai/patient-search-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/ai-index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/adult-acne-recurrent-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/cold-hands-feet-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/fatigue-after-diet-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/answer-guides/lighter-period-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/menopause-heat-sleep-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/period-pain-worsening-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/pms-headache-swelling-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/post-period-fatigue-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/postmeal-sleepiness-guide.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/answer-guides/postpartum-recovery-slow-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/standing-dizziness-guide.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/answer-guides/women-lifecycle-guide.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/authority/conditions/acupuncture-positive-evidence-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/carpal-tunnel.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/conditions/chronic-pelvic-inflammatory-disease.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/cinv-acupoint-patterns.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/conditions/endometriosis-related-pain.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/authority/conditions/female-infertility-art.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/authority/conditions/gynecologic-pelvic-pain-evidence-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/nausea-vomiting-acupoint-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/conditions/nausea-vomiting-pregnancy.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/obese-pcos.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/pcos-ovulation-dose-response.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/authority/conditions/peripheral-facial-palsy.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/conditions/polycystic-ovary-syndrome.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/authority/conditions/postoperative-urinary-retention-cervical-cancer.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/postoperative-urinary-retention.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/conditions/postpartum-breastfeeding-insufficiency.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/postpartum-depression.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/postpartum-lactation.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/pregnancy-symptoms-acupuncture-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/primary-dysmenorrhea.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/conditions/women-endocrine-reproductive-evidence-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/danggui-shaoyao-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/herbal-formula-evidence-hub.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/menopause-herbal-formula-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/migraine-herbal-evidence.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/shakuyaku-kanzo-tang-update.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/formulas/wenjing-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/formulas/wuzi-yanzong-wan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/herbs/angelica.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/herbs/chuanxiong.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/herbs/cornus-fructus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/herbs/dioscorea.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/herbs/ginseng.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/herbs/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/authority/herbs/velvet-antler.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/herbs/white-peony.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/authority/herbs/ziziphus-seed.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/autonomic/acupoint-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/autonomic/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/beiji-qianjin-yaofang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/cheonggang-uigam.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/donguibogam-acupuncture.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/donguibogam-tangaek.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/donguisusebowon.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/huangdi-neijing.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/classics/jingyue-quanshu.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue/chapters/abdominal-cold-food.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/jinkui-yaolue/chapters/bleeding-stasis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/jinkui-yaolue/chapters/blood-bi-deficiency.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue/chapters/gynecology.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue/chapters/limbs-hernia-worms.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/jinkui-yaolue/chapters/organs-accumulations.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/jinkui-yaolue/chapters/postpartum.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue/chapters/preface.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/jinkui-yaolue/chapters/pregnancy.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue/chapters/water-qi.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/jinkui-yaolue.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/nanjing.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/piwei-lun.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/shanghanlun/clauses/prefaces-pulse.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/shanghanlun/clauses/taiyang-lower.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/classics/uihak-ipmun.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/zhenjiu-dacheng.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics/zhenjiu-jiayi-jing.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/classics-network/comparison.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/clinical-reasoning/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/clinical-safety/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/clinical-safety/treatment-checklist.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/compare/gongjin-vs-gyeongok.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/concepts/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/concepts/pathological-products.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/abdominal-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/acne.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/acupuncture-frequency.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/acupuncture-herbal-combination.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/acupuncture-pain-question.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/amenorrhea.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/anemia-fatigue.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/anemia-lab.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/ankle-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/anxiety.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/assisted-reproduction-support.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/bloating.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/carpal-tunnel.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/child-rhinitis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/chronic-fatigue.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/chronic-kidney-disease.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/cluster-headache.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/cold-hands-feet.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/cold-sensitivity.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/common-cold.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/constipation.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/cough.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/cupping-question.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/custom-herbal-medicine.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/cystitis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/deer-antler-tonic-guide.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/dequervain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/diabetic-kidney-disease.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/diarrhea.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/dizziness.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/dysmenorrhea.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/dyspepsia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/early-awakening.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/edema-swelling.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/edema-weight.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/electroacupuncture-question.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/energy-recovery.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/facial-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/facial-palsy.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/fatty-liver.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/fertility-fatigue.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/flank-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/foot-numbness.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/gastritis-symptoms.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/hair-loss.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/headache.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/healthy-weight-management.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/heavy-menstruation.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/herbal-consultation-prep.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/herbal-extract-products.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/herbal-medicine-after-checkup.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/hip-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/hwabyeong.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/hyperthyroidism.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/hypothyroidism.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/ibs.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/index.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/infertility-preconception.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/inflammation-markers.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/insomnia.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/irregular-menstruation.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/knee-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/limb-numbness.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/liver-supplements-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/low-back-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/lumbar-disc-herniation.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/lumbar-spinal-stenosis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/male-menopause.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/menieres-disease.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/menopause-herbal.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/menopause-joint-pain.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/menopause.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/migraine.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/miscarriage-recovery.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/multi-supplement-review.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/muscle-cramps.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/natural-products-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/nausea.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/neck-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/normal-checkup-fatigue.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/obesity.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/omega3-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/overactive-bladder.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/ovulation-pain.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/palpitation.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/panic-disorder.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/pcos.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/pelvic-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/perimenopause.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/pharmacopuncture-frequency.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/pharmacopuncture-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/pharmacopuncture-what-is.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/pms.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/polycystic-ovary-syndrome.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/postoperative-recovery.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/postpartum-herbal.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/postpartum-recovery.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/postpartum-sweating.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/postpartum-wrist-pain.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/preconception-herbal.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/prediabetes.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/pregnancy-herbal-care.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/probiotics-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/pruritus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/psoriasis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/red-ginseng-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/restless-legs-syndrome.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/rheumatoid-arthritis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/rhinitis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/scanty-menstruation.md` | 3 통합 | 중복 또는 얇은 독립 안내를 핵심 문서에 흡수; 기존 URL 리디렉션 |
| `docs/conditions/seborrheic-dermatitis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/shingles.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/sinusitis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/supplements-herbal-medicine.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/temporomandibular-disorder.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/tension-headache.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/thoracic-back-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/thyroid-lab.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/tonic-supplement-choice.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/treatment-response-evaluation.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/type-2-diabetes.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/urticaria.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/uterine-fibroids.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/conditions/vitamins-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/weight-management-herbal.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/weight-plateau.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/conditions/womens-herbal.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/conditions/wrist-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/diagnostics/blood-deficiency.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/blood-stasis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/differentials/blood-stasis-vs-cold-damp-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/differentials/qi-vs-blood-vs-qi-blood.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/four-examinations.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/diagnostics/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/patterns/blood-deficiency.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/diagnostics/patterns/blood-stasis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/patterns/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/patterns/liver-qi-stagnation.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/patterns/qi-blood-deficiency.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/diagnostics/qi-blood-fluid-patterns.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/diagnostics/zangfu-patterns.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/donguibogam-network/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/donguisusebowon-network/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/evidence-clinical/guidelines.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/evidence-clinical/km-specific.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/evidence-guide/preclinical.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/evidence-integrated/clinical-application.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/evidence-integrated/sasang-evidence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/faq/conditions-faq.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formula-architecture/siwu-qi-blood-family.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/banxia-houpo-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/baohe-wan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/bawei-dihuang-wan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/bazhen-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/bazheng-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/bufei-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/buhuanjin-zhengqi-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/bulsu-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/cangerzi-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/chaihu-guizhi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/chaihu-jia-longgu-muli-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/chaihu-shugan-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/chuanxiong-chatiao-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/dabo-wonjeon.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/dachaihu-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/dachengqi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/dajianzhong-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/dalsaeng-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/dan-nokyong-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/danggui-buxue-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/danggui-shaoyao-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/danggui-susan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/fangfeng-tongsheng-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/fangji-huangqi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/fenxin-qiyin.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/gojin-eumja.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/gongjin-dan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/guibi-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/guizhi-fuling-wan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/guizhi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/gungha-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/gyeongok-go.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/huanglian-jiedu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/huangqi-guizhi-wuwu-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/huishou-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/huoxiang-zhengqi-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/ikgi-bohyeol-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/jiaoai-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/jiawei-wendan-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/jiawei-xiaoyao-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/jichuan-jian.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/jinlida.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/jiuwei-qianghuo-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/kaiyu-zhongyu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/lianqiao-baidu-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/longdan-xiegan-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/mahuang-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/maidong-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/mazi-ren-wan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/qingjing-siwu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/qingshang-juantong-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/qingxin-lianzi-yin.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/renshen-yangrong-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/renshen-yangwei-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/saenghwa-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/shaofu-zhuyu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/shengmai-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/shoutai-wan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/shujing-huoxue-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/siwu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/ssanghwa-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/suanzaoren-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/taishan-panshi-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/taohe-chengqi-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/tianwang-buxin-dan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/tiaojing-zhongyu-tang.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/formulas/wandai-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/weiling-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/wenjing-tang.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/formulas/xiangsha-liujunzi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/xiangsha-yangwei-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/xiaochaihu-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/xiaofeng-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/xiaoyao-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/xingsu-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/xuefu-zhuyu-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/yigan-san.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/yougui-wan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/yueju-wan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/yukwul-tang.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/yulin-zhu.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/formulas/yupingfeng-san.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/zhigancao-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/zhuling-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/ziyin-jianghuo-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/formulas/zuogui-wan.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations/liver.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/foundations/pathogenesis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations/qi-blood-fluid.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations/zangfu-overview.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations-clinical/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/foundations-integrated/classics-modern.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations-integrated/clinical-reasoning.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/foundations-integrated/diagnosis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/foundations-integrated/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/foundations-integrated/pattern-treatment.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/foundations-integrated/zangfu-qi-blood-fluids.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/glossary/blood-stasis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/blood.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/body-fluids.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/essence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/heart-spleen-deficiency.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/kidney-yang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/phlegm-fluid.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/qi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/glossary/sinking-middle-qi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/guide/editorial-policy.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbal-formula-clinical/safety.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbal-integrated/efficacy-indication-standard.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/evidence.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/formula-for-fatigue.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/formula-for-insomnia.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/formula-for-menopause.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/formula-for-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/formula-for-women.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/herbal-integrated/formulas.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/general-formulary.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/heat-clearing-herbs.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/herb-comparisons.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/herbs-for-stress.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/herbs-for-women.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/herbal-integrated/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbal-integrated/safety.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/herbal-integrated/tonic-recovery.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/acanthopanax-bark.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/achyranthes.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/aconite.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/akebia-stem.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/amomum.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/anemarrhena.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/angelica-pubescens.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/angelica.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/herbs/arctium.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/areca-pericarp.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/astragalus-tonic-guide.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/astragalus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/atractylodes-lancea.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/bamboo-shavings.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/barley-malt.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/bombyx-batryticatus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/bupleurum.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/categories/blood.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/categories/harmonize.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/categories/nourish-yin.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/categories/tonics.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/cervi-parvum-cornu.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/chrysanthemum.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/chuanxiong.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/cinnamon-bark.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/cinnamon-twig.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/citrus-immature.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/citrus-peel.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/coix.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/coptis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/cornus-fructus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/corydalis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/cuscuta-seed.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/cynanchum-wilfordii.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/cyperus.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/dandelion.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/dioscorea.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/dipsacus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/dried-chestnut.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/elm-root-bark.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/ephedra.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/eucommia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/evodia-fruit.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/forsythia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/fritillaria.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/gastrodia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/ginseng.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/green-citrus-peel.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/hawthorn.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/honeysuckle.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/jujube-fruit.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/leonurus.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/magnolia-bark.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/mihudeung.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/mint.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/moutan.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/musk.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/notopterygium.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/ophiopogon-extra.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/peach-kernel.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/phellodendron.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/pinellia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/polyporus.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/prepared-rehmannia.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/qinghao.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/raphanus-seed.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/red-peony.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/rhubarb.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/safflower.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/salvia.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/saposhnikovia.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/sasang-formula-reverse-index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/schisandra.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/schizonepeta.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/scutellaria.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/tsaoko-fruit.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/uncaria.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/herbs/vitex-fruit.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/white-peony.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/zedoary-rhizome.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/herbs/ziziphus-seed.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/history/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/immune-allergy/inflammation-pain.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/jingui-network/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/meridian-network/chong-vessel.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/meridian-network/conception-vessel.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/meridian-network/liver-meridian.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/meridian-network/spleen-meridian.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/musculoskeletal-ultrasound/safety.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/neijing-network/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/nerve-entrapment/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/acupoint-combinations.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/acupuncture-clinical-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/classic-to-evidence-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/condition-expansion-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/condition-to-treatment-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/formula-to-condition-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/network/herb-to-formula-map.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/pattern-treatment/blood-deficiency.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pattern-treatment/blood-stasis.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pattern-treatment/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pattern-treatment/phlegm-fluid.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/physicians/lee-je-ma.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/physicians/li-shizhen.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/physicians/zhu-danxi.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/pillar/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pillar/metabolic-checkup.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pillar/pediatrics.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pillar/skin-hair.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pillar/tonic-recovery.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/pillar/urology-mens-health.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/pillar/womens-health.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/portal/acupuncture.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/portal/herbs-formulas.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/portal/maps.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/questions/choice/qi-vs-qi-blood-deficiency.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/research/evidence-levels.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/research/formulas/gyeongok-go.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/research/references/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/sasang/diagnosis-research.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang/donguisusebowon.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang/sasang-intro-patient.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang/sasang-vs-constitution.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-clinical-detail/treatment-modalities.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-food/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-cards/cheongpyesagan-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-cards/gwangye-buja-ijung-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-cards/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-cards/jowiseungcheong-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-cards/selection-principles.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-combination-network/taeeumin-network.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-library/galgeunhaegi-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-library/haenginseungcheong-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-library/osuyubujairijung-tang.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-library/soeumin-extended-formulas.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-formula-library/taeeumin-extended-formulas.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-guideline/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-history/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-integrated/evidence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-integrated/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-integrated/soyangin.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-integrated/taeeumin.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/sasang-original-symptoms/emotion.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-original-symptoms/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-pattern-differential/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-progression/healthy-signs.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-progression/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-progression/recovery-signs.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-questions/what-is-donguisusebowon.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-severity/taeyangin.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/sasang-treatment/emotion.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-clinical/headache.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-clinical/rhinitis.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-herbal-guide/digestive/r10-abdominal-pelvic-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/digestive/r14-bloating.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/digestive/r63-appetite-intake.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-herbal-guide/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/neuro-mental/r42-dizziness.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/neuro-mental/r45-emotional.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/neuro-mental/r46-sleep.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/neuro-mental/r51-headache.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/respiratory-ent/r05-cough.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-herbal-guide/respiratory-ent/r53-fatigue.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-herbal-guide/systemic-skin/r21-rash-itch.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/symptom-herbal-guide/systemic-skin/r52-generalized-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/urogenital/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-herbal-guide/urogenital/r11-pelvic-perineal.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/symptom-herbal-guide/urogenital/r30-urinary.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-integrated/cold-hands-hot-flush.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-integrated/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-integrated/postpartum-fatigue-pain.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/symptom-integrated/treatment-evidence.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/taegeuk-acupuncture/constitutions.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/taegeuk-acupuncture/evidence.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/taegeuk-acupuncture/index.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/taegeuk-acupuncture/points.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/treatments/electroacupuncture.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/tung-acupuncture/foot.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/tung-acupuncture/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/tung-acupuncture/lower-leg.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/womens-health/fertility-pregnancy-postpartum.md` | 2 보강 | 핵심 본문·연결 또는 근거·안전성 보강 |
| `docs/zangfu-pattern-network/index.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/zangfu-pattern-network/interrelationships.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/zangfu-pattern-network/kidney-bladder.md` | 1 보존 | 관련 언급·전통 주치·임신 주의 자료 유지; 난임 독립 문서 증설 대상 아님 |
| `docs/zangfu-pattern-network/liver-gallbladder.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/zangfu-pattern-network/spleen-stomach.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |
| `docs/zangfu-pattern-network/treatment-map.md` | 4 허브 편입 | 기존 전문 자료 재사용; 난임/여성 허브·방제·본초·침구 지도에서 접근 |

## 분류 5: 신규 핵심 문서

- `docs/conditions/adenomyosis.md`
- `docs/conditions/diminished-ovarian-reserve.md`
- `docs/conditions/endometriosis.md`
- `docs/conditions/male-infertility.md`
- `docs/conditions/recurrent-implantation-failure.md`
- `docs/conditions/recurrent-pregnancy-loss.md`
- `docs/conditions/tubal-endometrial-infertility.md`
- `docs/conditions/unexplained-infertility.md`
- `docs/conditions/vaginitis.md`
- `docs/formulas/cangfu-daotan-tang.md`
- `docs/formulas/wuzi-yanzong-wan.md`
- `docs/womens-health/fertility-intake.md`
- `docs/womens-health/fertility-patterns.md`
- `docs/womens-health/reproductive-physiology.md`
