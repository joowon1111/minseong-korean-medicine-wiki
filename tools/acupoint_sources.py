"""Source roles shared by the standard atlas and Taegeuk summaries.

Metadata, classical interpretation, guideline point selection and trial-use
analysis are deliberately separate. A link to a location DB never supplies an
indication. Missing evidence stays missing rather than inheriting another role.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYERS = {'traditional': '전통적 효능·주치', 'clinical': '현대 임상 활용',
          'research': '현대 연구에서 다루어진 분야'}


def load_sources():
    return json.loads((ROOT / 'data/acupoint_sources.json').read_text())


def profile(code, point, sources):
    layers = {name: [] for name in LAYERS}
    if point.get('profile_kind') in ('domestic_review', 'domestic_literature'):
        primary = point['references'][0]
        layer = 'research' if primary['id'] == 'hwang2020' else 'traditional'
        layers[layer].append({
            'label': point['indications_label'], 'items': point['indications'],
            'explanation_label': point['actions_label'], 'explanation': '; '.join(point['actions']),
            'source_id': primary['id'], 'locator': primary['locator'],
            'supports': primary['supports'], 'origin': 'preserved_domestic_profile'})
        for item in point.get('additional_evidence', []):
            ref = next(r for r in point['references'] if r['id'] == item['source_id'])
            layer = 'traditional' if item['source_id'] == 'jung2015' else 'research'
            layers[layer].append({
                'label': item['label'], 'text': item['text'], 'source_id': item['source_id'],
                'locator': ref['locator'], 'supports': ref['supports'],
                'origin': 'preserved_domestic_profile'})
    else:
        layers['traditional'].append({
            'label': '대표 주치·용도', 'items': point['indications'],
            'explanation_label': '용도' if code == 'ST17' else '효능·활용 방향',
            'explanation': '; '.join(point['actions']),
            'source_url': point['source'], 'source_label': point['basis'],
            'origin': 'legacy_education'})
    for item in sources['points'].get(code, []):
        layers[item['layer']].append({k: v for k, v in item.items() if k != 'layer'})
    for entries in layers.values():
        entries.sort(key=lambda entry: entry.get('priority', 100))
    return layers


def render_profile(code, point, references, sources=None):
    sources = sources or load_sources()
    refs = {**references, **sources['references']}
    layers = profile(code, point, sources)
    citations = []
    lines = []
    for layer, title in LAYERS.items():
        if not layers[layer]:
            continue
        lines += [f'**{title}**', '']
        for item in layers[layer]:
            if 'source_id' in item:
                citation = (item['source_id'], item['locator'])
                if citation not in citations:
                    citations.append(citation)
                number = citations.index(citation) + 1
                ref = refs[item['source_id']]
                source_link = f' [출처 {number}]({ref["url"]})'
            elif item.get("source_url"):
                source_link = f' [{item["source_label"]}]({item["source_url"]})'
            else:
                source_link = ""
            text = item.get('text', ' · '.join(item.get('items', [])))
            lines.append(f'- **{item["label"]}:** {text}{source_link}')
            if item.get('explanation'):
                lines.append(f'- **{item["explanation_label"]}:** {item["explanation"]}')
        if layer == 'clinical':
            lines += ['', '진료지침의 배혈에서 맡는 역할입니다. 단일혈의 독립적인 효과를 뜻하지 않습니다.']
        lines.append('')
    meridian = ''.join(c for c in code if c.isalpha())
    lines += ['<details markdown="1">', '<summary>출처·원문과 해석 범위</summary>', '']
    for number, (source_id, locator) in enumerate(citations, 1):
        ref = refs[source_id]
        lines += [f'{number}. **{ref["evidence_type"]}** — {ref["authors"]}. '
                  f'[{ref["title"]}]({ref["url"]}). {ref["publication"]}. '
                  f'{ref["institution"]}. **{locator}**.'
                  + (f' DOI: {ref["doi"]}.' if ref.get('doi') else '')]
        if ref.get('policy_url'):
            lines[-1] += f' [이용조건]({ref["policy_url"]}).'
        if ref.get('pdf_url'):
            lines[-1] += f' [해당 쪽 PDF]({ref["pdf_url"]}).'
    lines += ['', f'**표준 정보:** [KMCRIC {point["name"]} {code}]'
              f'(https://www.kmcric.com/database/acupoint/{meridian}/{code})'
              '에서 위치·취혈 정보를 확인할 수 있습니다. 혈명·코드·소속 경맥을 대조했으며, '
              '이 링크를 주치·효능의 근거로 사용하지 않습니다.', '',
              '**위치 데이터:** [KM-Agent 경혈 자료]'
              '(https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv), '
              'Won-Yung Lee 외 5인, 2026, [CC BY 4.0]'
              '(https://github.com/wonyung-lee/km-agent/blob/main/LICENSE). '
              '기존 위치 자료를 사용하며, 일부 누락된 혈명 한자를 KMCRIC 목록과 대조하여 수정했습니다.', '',
              '논문·지침의 필요한 사실 관계를 자체 문장으로 요약했습니다. '
              '[자료별 범위와 이용조건](../../portal/acupuncture.md#sources)을 함께 확인하세요.',
              '', '</details>']
    # The point pages and Taegeuk page live at different depths.
    return '\n'.join(lines)


def catalog(clinical, sources, saam, taegeuk):
    manifest = json.loads((ROOT / 'data/standard_manifest.json').read_text())
    with (ROOT / 'data/acupoints_416_ccby4.csv').open(encoding='utf-8-sig', newline='') as f:
        locations = {r['entity_id']: r for r in csv.DictReader(f)}
    points = {}
    for identity in manifest:
        code = identity['code']
        point = clinical['points'][code]
        layers = profile(code, point, sources)
        source_ids = sorted({r['source_id'] for entries in layers.values() for r in entries if 'source_id' in r})
        attrs = sources.get('specific_attributes', {}).get(code, [])
        document = (ROOT / 'docs' / point['path']).read_text()
        specific = re.search(r'\*\*특정혈 속성:\*\* ([^\n]+)', document)
        if not specific:
            specific = re.search(r'\| 특정혈 \| ([^\n|]+)', document)
        points[code] = {
            **identity, 'path': point['path'],
            'location_ko': locations[code]['location_ko'], 'location_source': 'km_agent',
            'standard_reference': f'https://www.kmcric.com/database/acupoint/{identity["meridian_code"]}/{code}',
            'specific_attributes': {
                'existing_summary': specific.group(1).replace('**', '').strip() if specific else '',
                'existing_source_path': point['path'], 'reviewed_groups': attrs},
            'traditional': layers['traditional'], 'clinical': layers['clinical'], 'research': layers['research'],
            'assessment': {'text': point['clinical'], 'path': point['clinical_path'], 'origin': 'archive_editorial'},
            'saam_roles': saam.get(code, []), 'taegeuk_roles': taegeuk.get(code, []),
            'domestic_source_ids': source_ids,
            'coverage': {'domestic_traditional': any('source_id' in e for e in layers['traditional']),
                         'guideline': bool(layers['clinical']), 'research': bool(layers['research']),
                         'legacy_education': any(e.get('origin') == 'legacy_education' for e in layers['traditional'])}}
    summary = {'standard_points': len(points), 'standard_reference': len(points),
               'preserved_domestic_profiles': sum(p.get('profile_kind') == 'domestic_review' for p in clinical['points'].values()),
               'any_domestic_content': sum(bool(p['domestic_source_ids']) for p in points.values()),
               'legacy_content_only': sum(not p['domestic_source_ids'] for p in points.values()),
               'by_role': {role: sum(p['coverage'][role] for p in points.values())
                           for role in ['domestic_traditional', 'guideline', 'research', 'legacy_education']},
               'by_source': {key: sum(key in p['domestic_source_ids'] for p in points.values())
                             for key in {**clinical['references'], **sources['references']}}}
    return {'schema_version': 1, 'summary': summary,
            'scope_note': '위치·혈명 검증은 주치 검증과 별개이다. 국내 문헌의 관련 부위·배혈 해석도 전통층에 포함하며, 완전한 기본 주치 목록의 국내 검증을 뜻하지 않는다. 층별 경혈 수는 중복된다.',
            'common_references': sources['common_references'],
            'references': {**clinical['references'], **sources['references']}, 'points': points}


def portal_sources(data, sources):
    """Render a reader guide; keep coverage and audit history in the catalog."""
    lines = [
        '<!-- ACUPOINT_SOURCES_START -->',
        '경혈 자료는 **위치·취혈, 전통적 주치, 진료지침의 배혈, 임상시험 결과**를 나누어 읽습니다. '
        '경혈 페이지의 출처 링크에서 원문을 열고, 접이식 참고문헌에서 저자·논문명·해당 쪽과 표를 확인할 수 있습니다.', '',
        '| 궁금한 내용 | 확인할 자료 | 읽을 때 살필 점 |', '|---|---|---|',
        '| 혈자리는 어디에 있나요? | WHO 표준 위치와 KMCRIC 위치·취혈 자료 | 뼈·힘줄·근육 등의 표지와 자세, 좌우·부위 확인 |',
        '| 전통적으로 어떤 증상에 썼나요? | 고전 원문과 경혈·경혈군의 문헌연구 | 주치가 기록된 시대·문맥과 함께 사용한 혈 구성 |',
        '| 특정 질환에서는 어떻게 배혈하나요? | 해당 질환의 한의표준임상진료지침 | 대상 환자, 일반침·전침 등 치료 방식, 기본혈·변증별 가감 |',
        '| 어떤 치료 결과가 보고됐나요? | 무작위시험 등 사람 대상 임상연구 | 비교군, 전체 배혈·자극량·횟수, 통증·기능·추적 결과 |', '',
        '전통적 주치는 혈자리의 활용을 이해하는 자료이고, 진료지침과 임상시험은 특정 환자군에서 치료를 선택하고 평가하는 자료입니다. '
        '위치 자료에서는 취혈을, 주치 문헌에서는 활용의 맥락을, 임상시험에서는 치료 결과를 확인하면 서로 다른 자료가 연결됩니다.', '',
        '### 경혈 하나에서 배혈과 평가까지 이어 읽기 {#source-reading-examples}', '',
        '| 경혈·혈군 | 문헌과 배혈에서 볼 내용 | 다음에 읽을 자료 |', '|---|---|---|',
        '| 족삼리 ST36 | 복부·소화 관련 전통 주치와 기능성소화불량 지침의 배혈을 함께 읽음 | [족삼리 위치·주치](../acupuncture/points/st36-zusanli.md) · [기능성소화불량 평가·치료](../conditions/functional-dyspepsia.md) |',
        '| 태백 SP3 | 사암침 처방에서 비경 원혈인 태백을 어떤 보사 구성으로 쓰는지 확인 | [태백 위치·문헌](../acupuncture/points/sp3.md) · [사암침 정격·승격](../acupuncture-specific/saam-12-meridians.md) |',
        '| 합곡 LI4·태충 LR3 | 각 혈의 주치와 두 혈을 묶은 사관혈의 문헌 맥락을 구분 | [합곡](../acupuncture/points/li4-hegu.md) · [태충](../acupuncture/points/lr3-taichong.md) |',
        '| 신문 HT7·내관 PC6 | 불면 관련 배혈에서 수면·심계·긴장을 함께 평가하는 방법을 살핌 | [신문](../acupuncture/points/ht7-shenmen.md) · [내관](../acupuncture/points/pc6-neiguan.md) · [불면증](../conditions/insomnia.md) |', '',
        '혈자리 이름을 확인한 뒤에는 **왜 이 혈들을 함께 골랐는지, 무엇을 변화시키려는지**를 읽습니다. '
        '복부 불편은 식후포만·조기포만·오심을, 불면은 입면·야간각성·낮 기능을 나누어 기록하면 '
        '전통 주치와 현재 환자의 치료 목표를 구체적으로 연결할 수 있습니다. '
        '[배혈 원리](../meridian-network/special-points/index.md) · [치료 반응과 재평가](../acupuncture-clinical/response-reassessment.md).', '',
        '### 사용 빈도와 치료 효과는 어떻게 읽나요? {#trial-interpretation}', '',
        '경혈 사용 빈도 분석은 어떤 질환 연구에 어떤 혈이 자주 포함됐는지를 보여 줍니다. '
        '효과의 크기는 실제 환자시험의 치료군·비교군과 결과에서 확인합니다. '
        '2020·2021년 경혈 사용 양상 논문은 **같은 421개 임상시험** 자료를 분석하므로 '
        '자료의 출발점이 같은 후속 분석으로 함께 읽습니다.', '',
        '예를 들어 2020년 식후불편증후군 무작위시험은 성인 278명을 침 또는 가짜침에 배정해 '
        '4주간 12회 치료했습니다. 4주 전체 치료 반응률은 83.0%와 51.6%, '
        '식후포만·상복부팽만·조기포만 세 증상의 소실률은 27.8%와 17.3%로 보고됐습니다. '
        '전반적 호전과 세 증상의 완전 소실은 서로 다른 결과입니다. '
        '이 시험은 전체 배혈과 치료 일정의 결과이며, 개별 혈 하나의 효과를 따로 측정한 것은 아닙니다. '
        '16주 평가 완료는 228명으로, 탈락과 시술자 눈가림의 한계도 함께 확인합니다. '
        '[원 논문·PMID 32422066](https://pubmed.ncbi.nlm.nih.gov/32422066/).', '',
        '<details markdown="1">', '<summary>경혈 문헌·진료지침·임상연구 참고문헌</summary>', '']
    for key, ref in data['references'].items():
        lines += [f'- **{ref["authors"]}**. [{ref["title"]}]({ref["url"]}). '
                  f'{ref["publication"]}. {ref["institution"]}. {ref["evidence_type"]}.'
                  + (f' DOI: {ref["doi"]}.' if ref.get('doi') else '')]
    lines += ['', '만성요통 배혈은 **2020년판 한의표준임상진료지침**을 기준으로 소개합니다. '
              '지침을 읽을 때에는 발행 연도·대상 질환·치료 조건을 함께 확인하세요. '
              '기관 소속 연구자의 논문은 연구 결과로, 학회·기관의 지침은 임상 권고로 구분해 읽습니다.', '',
              '</details>', '', '<details markdown="1">', '<summary>위치 자료·원문·이용 안내</summary>', '',
              '- **[KMCRIC 표준경혈 DB](https://www.kmcric.com/database/acupoint):** '
              '혈명·코드와 위치·취혈 자료. [이용약관](https://www.kmcric.com/etc/agreement).',
              '- **[KM-Agent 경혈 위치 자료](https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv):** '
              'Won-Yung Lee·Ji-Hwan Kim·Jungtae Leem·Byung-Wook Lee·Seungho Lee·Young Woo Kim, 2026. '
              '[CC BY 4.0](https://github.com/wonyung-lee/km-agent/blob/main/LICENSE). '
              '이 자료의 이용조건은 KMCRIC의 본문·영상·이미지 이용조건과 별개입니다.',
              '- **[국가한의임상정보포털](https://nikom.or.kr/nckm/):** '
              '질환별 한의표준임상진료지침과 [저작권 정책](https://nikom.or.kr/nckm/html.do?menu_idx=95).',
              '- **[한의학고전DB](https://mediclassics.kr/):** '
              '고전의 원문·번역과 [자료 이용 안내](https://info.mediclassics.kr/document/guide/license).', '',
              '논문·지침은 각 원문의 이용조건을 따릅니다. 아카이브의 한국어 해설과 평가·기록 안내는 '
              '출처의 원문 인용·연구 결과와 구분해 표시합니다.', '',
              '</details>', '<!-- ACUPOINT_SOURCES_END -->']
    return '\n'.join(lines)
