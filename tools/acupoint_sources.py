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
            else:
                source_link = f' [{item["source_label"]}]({item["source_url"]})'
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
    counts = data['summary']
    roles = counts['by_role']
    lines = [
        '<!-- ACUPOINT_SOURCES_START -->',
        '**위치·혈명, 전통적 주치, 진료지침의 배혈, 현대 연구를 구분해 표시합니다.** '
        '경혈 페이지의 짧은 출처 링크로 원문을 열고, 접이식 참고문헌에서 저자·기관·논문명·해당 쪽과 표를 확인할 수 있습니다.', '',
        '| 출처의 역할 | 반영 범위 | 읽는 방법 |', '|---|---|---|',
        '| 표준 정보 | **361경혈**의 혈명·코드·소속 경맥 대조 및 KMCRIC 개별 링크 | 위치·취혈 DB를 주치의 근거로 대신 인용하지 않습니다. |',
        f'| 국내 문헌의 전통적 활용 | **{roles["domestic_traditional"]}경혈** | 기본 주치 외에 관련 부위·경혈군·배혈의 문헌 해석도 포함합니다. |',
        f'| 임상진료지침의 배혈 | **{roles["guideline"]}경혈** | 질환·대상 환자·치료 방식·변증 조건을 함께 봅니다. |',
        f'| 현대 연구의 활용·결과 | **{roles["research"]}경혈** | 사용 빈도 분석과 치료 결과를 구분합니다. 배혈 비교시험도 단일혈의 효과를 확정하지 않습니다. |', '',
        f'기존 국내 자료 **27경혈은 보존**했습니다. 족삼리의 기본 주치를 국내 문헌으로 교체하고, '
        f'문헌·지침을 보완하여 현재 **{counts["any_domestic_content"]}경혈**에 국내 주치·활용 자료가 연결되어 있습니다. '
        f'**{counts["legacy_content_only"]}경혈**의 주치·효능은 기존 교육자료 출처를 유지합니다. '
        '층별 경혈 수는 서로 중복됩니다.', '',
        '**361경혈 전체의 기본 전통 주치·효능을 포괄하고 이용 범위까지 확인한 국내 공통 원문은 아직 확보하지 못했습니다.** '
        '국내 자료가 일부만 확인된 혈은 기존 교육자료와 함께 표시합니다. 표준 DB 링크가 있다는 이유로 주치까지 국내 자료로 검증했다고 표시하지 않습니다.', '',
        '<details markdown="1">', '<summary>국내 문헌·진료지침과 확인한 범위</summary>', '']
    for key, ref in data['references'].items():
        lines += [f'- **{ref["authors"]}**. [{ref["title"]}]({ref["url"]}). '
                  f'{ref["publication"]}. {ref["institution"]}. '
                  f'{ref["evidence_type"]}; {counts["by_source"][key]}경혈에 반영.'
                  + (f' DOI: {ref["doi"]}.' if ref.get('doi') else '')]
    lines += ['', '만성요통은 공개 원문을 확인한 **2020년판**의 배혈을 소개합니다. '
              '2025년판의 등록은 확인했지만 원문을 확보하지 못하여 최신판 권고로 표시하지 않았습니다.', '',
              '2020·2021년 경혈 사용 양상 논문은 **같은 421개 임상시험** 자료를 분석하므로 '
              '독립적인 효과 검증 두 건으로 합산하지 않습니다. 기관 소속 연구자의 논문과 기관·학회의 공식 진료 권고도 구분합니다.', '',
              '</details>', '', '<details markdown="1">', '<summary>표준 자료의 출처와 이용조건</summary>', '',
              '- **[KMCRIC 표준경혈 DB](https://www.kmcric.com/database/acupoint):** 14경맥 목록의 혈명·코드를 대조했습니다. '
              '확인한 족삼리 상세 항목은 부위·취혈·침구법으로, 주치·효능 항목은 확인되지 않았습니다. '
              '[이용약관](https://www.kmcric.com/etc/agreement)에 따라 DB 본문·영상·이미지를 옮기지 않고 개별 링크를 제공합니다.',
              '- **[KM-Agent 경혈 위치 자료](https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv):** '
              'Won-Yung Lee·Ji-Hwan Kim·Jungtae Leem·Byung-Wook Lee·Seungho Lee·Young Woo Kim, 2026. '
              '[CC BY 4.0](https://github.com/wonyung-lee/km-agent/blob/main/LICENSE)의 기존 위치 데이터를 사용합니다. '
              '14경혈에서 누락된 한자 이름을 KMCRIC 목록과 대조해 수정했습니다. 이 라이선스가 KMCRIC 콘텐츠 전체에 적용되는 것은 아닙니다.',
              '- **국내 논문:** CC BY 자료와 비영리 조건이 있는 CC BY-NC 자료를 구분했습니다. '
              '아카이브의 비영리 지위를 가정하거나 원문 표·그림·문장을 전재하지 않고, 필요한 사실 관계를 자체 문장으로 짧게 정리했습니다. '
              '1993·2024년 경혈 문헌은 일반 재사용 허락을 확인하지 못하여 필요한 주치·배혈 사실과 원문 링크만 사용합니다. '
              '2012년 턱관절 배혈 비교시험은 CC BY-NC-ND 조건을 확인했으며 원문·표·그림을 전재하지 않습니다.',
              '- **NCKM 지침:** [저작권 정책](https://nikom.or.kr/nckm/html.do?menu_idx=95)과 각 지침의 판권을 확인했습니다. '
              '배혈의 사실을 요약하며, 권고문·표를 복제하지 않습니다. 지침과 이용조건 링크를 함께 제공합니다.',
              '- **KIOM 한의학고전DB:** [이용 안내](https://info.mediclassics.kr/document/guide/license)의 '
              '데이터 수집·재이용 조건에 따라 고전 원문·번역문을 대량 가져오지 않았습니다.', '',
              '각 혈의 임상 평가는 민성 한의학 아카이브의 평가·기록 안내입니다. 원문 출처가 뒷받침하는 내용과 구별해 읽습니다.', '',
              '</details>', '<!-- ACUPOINT_SOURCES_END -->']
    return '\n'.join(lines)
