#!/usr/bin/env python3
"""Build a local discovery index from the archive's existing reviewed records.

No uploaded application code, meshes, 3D coordinates or AI annotations are used.
Location attribution and clinical provenance stay attached to their own records.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/assets/acupoint-atlas/discovery.json'


def load(name):
    return json.loads((ROOT / 'data' / (name + '.json')).read_text(encoding='utf-8'))


def url(path):
    base, _, anchor = path.partition('#')
    base = base.removesuffix('.md')
    if base.endswith('/index'):
        base = base[:-6]
    return '/' + base + '/' + ('#' + anchor if anchor else '')


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    return re.sub(r'\s+', ' ', text.replace('**', '').replace('`', '')).strip()


def anatomy(path):
    text = (ROOT / 'docs' / path).read_text(encoding='utf-8')
    match = re.search(r'^## (?:해부학과 안전|해부학·안전|자침법·안전)\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not match:
        return ''
    paragraphs = re.split(r'\n\s*\n', match[1].strip())
    # Summarize only the first existing paragraph, with the full source linked.
    return plain(paragraphs[0])


def clinical_rows(point, references):
    rows = []
    for layer, label in [('traditional', '전통 주치·활용'), ('clinical', '진료지침·배혈'), ('research', '현대 연구')]:
        entries = point[layer]
        if not entries:
            continue
        # The index is a preview; the original document retains all locators.
        for entry in entries[:3]:
            description = entry.get('text') or ' · '.join(entry.get('items', []))
            if not description:
                description = entry.get('explanation', '')
            reference = references.get(entry.get('source_id'), {})
            rows.append({'layer': label, 'label': entry.get('label', label),
                         'text': plain(description),
                         'source': reference.get('url', entry.get('source_url', '')),
                         'locator': entry.get('locator', '')})
    return rows


def build():
    catalog = load('acupoint_catalog')
    clinical = load('acupoint_clinical')['points']
    diagrams = load('acupoint_diagrams')['regions']
    routes = {r['code']: r for r in load('meridian_routes')['routes']}
    point_diagrams = {p['code']: r for r in diagrams for p in r['points']}
    entries = []
    for code, point in catalog['points'].items():
        region = point_diagrams[code]
        notes = clinical[code]
        rows = clinical_rows(point, catalog['references'])
        anatomical = anatomy(point['path'])
        entry = {'id': code, 'kind': 'standard', 'name': point['name_ko'],
                 'han': point['name_zh'], 'code': code,
                 'meridian': point['meridian_code'], 'meridian_name': point['meridian'],
                 'region': region['group'], 'href': url(point['path']),
                 'location': point['location_ko'], 'anatomy': anatomical,
                 'rows': rows, 'assessment': point['assessment']['text'],
                 'diagrams': [{'src': '/assets/acupoint-atlas/' + region['id'] + '.svg#' + code,
                               'title': region['title']}],
                 'route': url(routes[point['meridian_code']]['path']),
                 'route_diagram': '/assets/meridian-routes/' + point['meridian_code'].lower() + '.svg',
                 'standard_reference': point['standard_reference'],
                 'roles': [{'label': r[0], 'meridian': r[1]} for r in point.get('saam_roles', [])],
                 'attributes': point['specific_attributes']['existing_summary']}
        entry['search'] = plain(' '.join([entry['name'], entry['han'], code, entry['meridian_name'],
            entry['region'], entry['location'], anatomical, entry['attributes'],
            ' '.join(notes['indications']), ' '.join(notes['actions']),
            ' '.join(r['label'] + ' ' + r['text'] for r in rows)]))
        entries.append(entry)
    lookup = {e['code']: e for e in entries}
    for formula in load('saam_formulas')['formulas']:
        for mode, bo, sa, meaning in [('정격', 'tonify', 'sedate', '허증의 기본 조합'),
                                      ('승격', 'excess_tonify', 'excess_sedate', '실증의 기본 조합')]:
            points = [{'role': role, 'code': code, 'name': lookup[code]['name'], 'href': lookup[code]['href']}
                      for field, role in [(bo, '보'), (sa, '사')] for code in formula[field]]
            entry = {'id': 'saam-' + formula['meridian'].lower() + '-' + bo,
                     'kind': 'saam', 'name': formula['name'] + mode, 'code': '', 'han': '',
                     'meridian': formula['meridian'], 'meridian_name': formula['name'] + '경',
                     'region': '손·발의 오수혈',
                     'href': '/acupuncture-specific/saam-12-meridians/#' + formula['meridian'].lower(),
                     'location': meaning, 'anatomy': '', 'assessment': formula['clinical'],
                     'rows': [{'layer': '전통 조합', 'label': '함께 살필 양상', 'text': formula['assessment'],
                               'source': load('saam_formulas')['source'], 'locator': '표 1 · 현대 코드 대조는 상세 문서 참조'}],
                     'points': points,
                     'diagrams': [dict(lookup[code]['diagrams'][0], code=code, name=lookup[code]['name'], role=role)
                                  for field, role in [(bo, '보'), (sa, '사')] for code in formula[field]]}
            entry['search'] = ' '.join([entry['name'], formula['name'] + '경 ' + mode, formula['meridian'],
                                       formula['assessment'], ' '.join(p['name'] + ' ' + p['code'] for p in points)])
            entries.append(entry)
    for region in load('tung_acupuncture')['regions']:
        for point in region['points']:
            profile = point['clinical_profile']
            entry = {'id': 'tung-' + region['id'] + '-' + point['id'], 'kind': 'tung',
                     'name': point['name'], 'han': point['han'], 'code': '', 'meridian': '',
                     'meridian_name': '동씨기혈', 'region': region['title'].split(' · ')[0],
                     'href': '/tung-acupuncture/' + region['id'] + '/#' + point['id'],
                     'location': point['location'], 'anatomy': '', 'assessment': profile['clinical'],
                     'rows': [{'layer': '전승 자료', 'label': '대표 주치', 'text': ' · '.join(profile['indications']),
                               'source': profile['source'], 'locator': ''},
                              {'layer': '전승 자료', 'label': '활용 방향', 'text': profile['actions'],
                               'source': profile['source'], 'locator': ''}],
                     'diagrams': [{'src': '/assets/tung-atlas/' + region['id'] + '.svg#' + point['id'],
                                   'title': region['title']}], 'note': region['note']}
            entry['search'] = ' '.join([entry['name'], entry['han'], entry['region'], entry['location'],
                                       ' '.join(profile['indications']), profile['actions'], point.get('reading', '')])
            entries.append(entry)
    # Searchable concepts, not an invented 12-meridian cold/heat prescription table.
    for name, words in [('한격', '한증 냉증 화혈 수혈 한열'), ('열격', '열증 열감 화혈 수혈 한열')]:
        entries.append({'id': 'saam-' + ('cold' if name == '한격' else 'heat'), 'kind': 'saam',
                        'name': name + ' · 출처별 구성 읽기', 'han': '', 'code': '', 'meridian': '',
                        'meridian_name': '사암침법', 'region': '한열 조합의 원리',
                        'href': '/acupuncture-specific/saam-12-meridians/#saam-cold-heat',
                        'location': '한열 조합의 명칭과 보사 구성은 함께 확인합니다.',
                        'anatomy': '', 'assessment': '개별 경맥의 한격·열격 전수 처방표는 이 탐색기의 수록 범위에 포함하지 않습니다.',
                        'rows': [], 'diagrams': [], 'search': name + ' ' + words})
    return {'schema_version': 1,
            'scope': '361 표준경혈 · 사암침 정격·승격 24조합과 한열 개념 2항목 · 동씨기혈 50 위치점',
            'location_attribution': 'KM-Agent, Won-Yung Lee 외 5인, 2026, CC BY 4.0; 기존 아카이브 위치 자료를 탐색용으로 재구성',
            'location_source': 'https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv',
            'location_license': 'https://github.com/wonyung-lee/km-agent/blob/main/LICENSE',
            'entries': entries}


def main():
    OUTPUT.write_text(json.dumps(build(), ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print('Built local acupoint discovery index')


if __name__ == '__main__':
    main()
