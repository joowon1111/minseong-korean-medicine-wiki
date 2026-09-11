#!/usr/bin/env python3
"""Integrate reviewed clinical data into existing point sections, preserving URLs."""
import argparse
import json
import posixpath
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- ACUPOINT_CLINICAL_START -->'
END = '<!-- ACUPOINT_CLINICAL_END -->'


def saam_roles(formulas):
    roles = defaultdict(list)
    for formula in formulas:
        for field, label in [('tonify', '정격 보혈'), ('sedate', '정격 사혈'),
                             ('excess_tonify', '승격 보혈'), ('excess_sedate', '승격 사혈')]:
            for code in formula[field]:
                roles[code].append((formula['name'] + label, formula['meridian'].lower()))
    return roles


def point_block(code, point, roles):
    target = posixpath.relpath(point['clinical_path'], posixpath.dirname(point['path']))
    actions = '; '.join(point['actions']).removeprefix('치료 목표 — ')
    label = '활용 방향' if point['actions'][0].startswith('치료 목표') else '효능의 전통적 설명'
    if code == 'ST17':
        label = '용도'
    lines = [START, '| 항목 | 내용 |', '|---|---|',
             '| 대표 주치·용도 | ' + ' · '.join(point['indications']) + ' |',
             f'| {label} | {actions} |',
             f'| 임상 평가·활용 | {point["clinical"]} [평가 자료]({target}) |',
             f'| 주치 출처 | [{point["name"]} 전통 주치·교육자료]({point["source"]}) |']
    if roles.get(code):
        links = [f'[{label}](../../acupuncture-specific/saam-12-meridians.md#{anchor})'
                 for label, anchor in roles[code]]
        lines.append('| 사암침법에서의 역할 | ' + ' · '.join(links) + ' |')
    lines.extend(['', '주치와 효능은 전통적 활용을 요약한 것입니다. 실제 치료에서는 증상·기능과 배혈 전체를 평가합니다.', END])
    return '\n'.join(lines)


def integrate_point(text, block):
    if START in text:
        assert text.count(START) == text.count(END) == 1
        return re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, text, flags=re.S)
    generic = r'이 혈의 전통적 효능·주치는[^\n]+통합해 읽습니다\.'
    traditional = re.search(r'(?m)^## (전통적 임상 연결|전통적 의미와 주치)\n', text)
    if traditional:
        end = re.search(r'(?m)^## ', text[traditional.end():])
        stop = traditional.end() + end.start() if end else len(text)
        text = text[:traditional.end()] + '\n' + block + '\n\n' + text[stop:]
        return re.sub(generic + r'\n\n', '', text)
    if re.search(generic, text):
        return re.sub(generic, lambda _: block, text, count=1)
    raise ValueError('No existing clinical section found')


def tung_block(point):
    c = point['clinical_profile']
    return '\n'.join([START,
        '**대표 주치(전승):** ' + ' · '.join(c['indications']) + '.', '',
        '**효능·활용 방향(전승):** ' + c['actions'], '',
        '**임상 활용:** ' + c['clinical'], '',
        '[주치 출처](' + c['source'] + ')', END])


def integrate_tung(text, points):
    for point in points:
        match = re.search(r'(?m)^### [^\n]+\{#' + re.escape(point['id']) + r'\}\n', text)
        if not match:
            raise ValueError('Missing Tung anchor: ' + point['id'])
        following = re.search(r'(?m)^#{2,3} ', text[match.end():])
        stop = match.end() + following.start() if following else len(text)
        section = text[match.end():stop]
        block = tung_block(point)
        if START in section:
            section = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, section, flags=re.S)
        else:
            source = re.search(r'(?m)^\[위치 출처', section)
            if not source:
                raise ValueError('Missing source position: ' + point['id'])
            section = section[:source.start()] + block + '\n\n' + section[source.start():]
        text = text[:match.end()] + section + text[stop:]
    return text


def outputs():
    points = json.loads((ROOT / 'data/acupoint_clinical.json').read_text())['points']
    formulas = json.loads((ROOT / 'data/saam_formulas.json').read_text())['formulas']
    regions = json.loads((ROOT / 'data/tung_acupuncture.json').read_text())['regions']
    roles = saam_roles(formulas)
    # Read whole documents before editing; collect all outputs before writing any.
    result = {}
    for code, point in points.items():
        path = ROOT / 'docs' / point['path']
        result[path] = integrate_point(path.read_text(), point_block(code, point, roles))
    for region in regions:
        path = ROOT / 'docs/tung-acupuncture' / (region['id'] + '.md')
        result[path] = integrate_tung(path.read_text(), region['points'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = outputs()
    stale = [path for path, content in result.items() if path.read_text() != content]
    if args.check:
        if stale:
            raise SystemExit('Clinical sections need regeneration: ' + ', '.join(str(p.relative_to(ROOT)) for p in stale))
        print(f'Clinical sections current: {len(result)} documents')
    else:
        for path in stale:
            path.write_text(result[path])
        print(f'Clinical sections integrated: {len(stale)} documents')


if __name__ == '__main__':
    main()
