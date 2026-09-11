"""Keep the cited Taegeuk formula table and existing atlas summaries consistent."""
import argparse
import json
import posixpath
import re
from pathlib import Path

from build_acupoint_clinical import taegeuk_roles, domestic_rows

ROOT = Path(__file__).resolve().parents[1]


def replace_section(text, name, block):
    start, end = f'<!-- {name}_START -->', f'<!-- {name}_END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Missing or duplicate section: {name}')
    return re.sub(re.escape(start) + r'.*?' + re.escape(end),
                  lambda _: start + '\n' + block + '\n' + end, text, flags=re.S)


def outputs():
    data = json.loads((ROOT / 'data/taegeuk_formulas.json').read_text())
    clinical_data = json.loads((ROOT / 'data/acupoint_clinical.json').read_text())
    atlas = clinical_data['points']

    def link(code):
        point = atlas[code]
        return f'[{point["name"]} {code}](../{point["path"]})'

    table = ['| 체질 | 심경혈 補 | 원혈 補 | 원혈 瀉 |', '|---|---|---|---|']
    for f in data['formulas']:
        table.append(f'| [{f["name"]}](#{f["id"]}) | {link(f["heart"])} | '
                     f'{link(f["tonify"][1])} | {link(f["sedate"][0])} |')

    profiles = []
    roles = taegeuk_roles(data['formulas'])
    for code, attrs in data['points'].items():
        point = atlas[code]
        role_links = ' · '.join(f'[{label}](constitutions.md#{anchor})' for label, anchor in roles[code])
        # Existing clinical summaries contain no Markdown paths; link their source and evaluation explicitly.
        assessment = posixpath.relpath(point['clinical_path'], 'taegeuk-acupuncture')
        summary = domestic_rows(point, clinical_data.get('references', {}))
        if summary is None:
            summary = ['| 대표 주치(전통) | ' + ' · '.join(point['indications']) + ' |',
                       '| 효능·활용 방향(전통) | ' + '; '.join(point['actions']) + ' |',
                       f'| 주치 출처 | [기존 경혈 문서의 교육자료]({point["source"]}) |']
        profiles += [f'### {point["name"]} {code} {{#{code.lower()}}}', '',
                     f'**[위치·취혈 도해와 상세 주치](../{point["path"]})**', '',
                     '| 항목 | 내용 |', '|---|---|',
                     f'| 소속 경맥 | [{attrs["meridian"]} 전체 주행](../{attrs["meridian_path"]}) |',
                     f'| 특정혈 | {attrs["specific"]} |',
                     f'| 태극침법 역할 | {role_links} |'] + summary + [
                     f'| 임상 평가 | {point["clinical"]} [평가 자료]({assessment}) |', '']
    result = {}
    for filename, marker, content in [('constitutions.md', 'TAEGEUK_FORMULAS', table),
                                       ('points.md', 'TAEGEUK_POINTS', profiles)]:
        path = ROOT / 'docs/taegeuk-acupuncture' / filename
        result[path] = replace_section(path.read_text(), marker, '\n'.join(content).strip())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = outputs()
    stale = [p for p, content in result.items() if p.read_text() != content]
    if args.check and stale:
        raise SystemExit('Taegeuk tables need regeneration: ' + ', '.join(map(str, stale)))
    if not args.check:
        for path in stale:
            path.write_text(result[path])
    print(f'Taegeuk: 4 formulas, 9 points; {len(stale)} documents ' + ('stale' if args.check else 'updated'))


if __name__ == '__main__':
    main()
