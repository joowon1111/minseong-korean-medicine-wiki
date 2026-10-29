#!/usr/bin/env python3
"""Regenerate seven supplemental records without manufacturing missing point names.

Run --check in CI. Never overwrite other point pages. The legacy Windows
installer calls this after copying its historic point payload.
"""
import argparse
import csv
import json
from pathlib import Path
import re

from acupoint_record_types import supplementary_type

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/wonyung-lee/km-agent/blob/main/data/acupoints.csv'
LABELS = {
    'surface_anatomy': '표면해부학적 위치 확인 자료',
    'auricular_anatomy': '귀 해부학 자료',
    'auricular_point_combination': '이침 배혈 예시',
}


def load_records():
    config = json.loads((ROOT / 'data/acupoint_supplements.json').read_text())
    with (ROOT / 'data/acupoints_416_ccby4.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    records = {r['entity_id']: r for r in rows}
    expected = {f'SA{i}' for i in range(1, 5)} | {f'AA{i}' for i in range(1, 4)}
    if set(config['records']) != expected:
        raise ValueError('Supplemental record coverage changed; review taxonomy first')
    for code in expected:
        row, info = records[code], config['records'][code]
        if row['category'] != supplementary_type(code):
            raise ValueError(f'{code}: incorrect CSV category')
        if row['name_ko'] != info['source_name_ko']:
            raise ValueError(f'{code}: upstream name changed; review descriptive title')
        if row['method'].strip() or row['needling'].strip():
            raise ValueError(f'{code}: new procedure data requires editorial review')
        if not row['location_ko'].strip() or re.search(r'\bnan\b', info['title'], re.I):
            raise ValueError(f'{code}: missing content/title')
    return records, config


def render(code, row, info):
    kind = supplementary_type(code)
    label = LABELS[kind]
    title = f"{info['title']} ({code})"
    section = '이침 배혈 구성' if kind == 'auricular_point_combination' else '원본의 위치·구조 설명'
    text = f'''---
title: {title}
description: {info['description']}
status: 초안
record_type: {kind}
source_record_id: {code}
tags: [{label}]
source_standard: KM-Agent acupoints.csv / CC BY 4.0
---
# {title}

## 분류
**{label}** · 원본 자료 식별자 **{code}**

{info['intro']}

## 위치

### {section}

{row['location_ko'].strip()}

## 자료의 범위

<span id="_4"></span>
<span id="_5"></span>

{info['scope']}

사람의 내용 감수가 필요한 초안입니다. 분류·명칭·원본 대조와 자동 검증의 범위는 구별해 읽어 주세요.

## 출처와 연결 {{#sources}}

[KM-Agent acupoints.csv]({SOURCE})의 {code}행. Won-Yung Lee·Ji-Hwan Kim·Jungtae Leem·Byung-Wook Lee·Seungho Lee·Young Woo Kim, 2026, CC BY 4.0. 원본 설명을 보존하고 제목·분류·자료 범위 해설을 편집했습니다. SA·AA의 명칭과 자료 식별자는 이 데이터셋의 표기이며, WHO 표준 361경혈과 구분합니다.

→ [경외기혈 통합 목록 — 해부학·이침 참고자료](../../acupoint-network/extra-points.md#supplementary-materials)
→ [WHO 표준 361경혈 임상 아틀라스](../../acupoint-network/standard-atlas.md)
'''
    return text


def outputs():
    records, config = load_records()
    result = {}
    for code, info in config['records'].items():
        content = render(code, records[code], info)
        for directory in ('docs/acupuncture/extra-points', '_payload/extra_pages'):
            result[ROOT / directory / f'{code.lower()}.md'] = content
    result[ROOT / 'docs/acupoint-network/extra-points.md'] = render_index(records, config)
    return result


def render_index(records, config):
    text = '''---
title: 경외기혈 통합 목록
description: 경외기혈 48개 문서와 표면해부학·귀 해부학·이침 배혈 참고자료를 구분해 탐색합니다.
---

# 경외기혈 통합 목록

경외기혈 상세 문서를 부위별로 탐색합니다. 같은 원본 데이터에 들어 있던 표면해부학·이침 자료는 아래의 **해부학·이침 참고자료**에서 자료 성격에 따라 구분합니다.

| 자료 | 의미 | 탐색 범위 |
|---|---|---|
| 표준경혈 | 14경맥에 속한 361경혈 | [WHO 표준 아틀라스](standard-atlas.md) |
| 경외기혈 | 아래 EX 코드로 연결하는 개별 혈위 | 부위별 경외기혈 48개 문서 |
| 표면해부학 | 신체 구조·거리·촉지 기준 | SA1~SA4, 위치 확인 자료 4건 |
| 귀 해부학 | 이침 학습의 해부학적 기준 구조 | AA1, 구조 설명 1건 |
| 이침 배혈 예시 | 여러 이침점을 묶은 조합 | AA2·AA3, 조합 2건 |

SA·AA는 원본 데이터의 자료 식별자입니다. 개별 경혈, 해부학적 기준점, 이침점 조합은 서로 다른 단위로 읽습니다. 기존 문서 주소는 유지합니다.

'''
    for heading, prefix in [('두경부', 'EX-HN'), ('상지', 'EX-UE'), ('하지', 'EX-LE'), ('배부·기타', 'EX-B')]:
        text += f'## {heading}\n\n'
        codes = sorted((code for code in records if code.startswith(prefix)), key=lambda c: int(c[len(prefix):]))
        text += ' · '.join(f'[{code}](../acupuncture/extra-points/{code.lower()}.md)' for code in codes) + '\n\n'
    text += '[EX-CA1](../acupuncture/extra-points/ex-ca1.md)\n\n'
    text += '''## 해부학·이침 참고자료 {#supplementary-materials}

이 자료들은 경외기혈의 혈수에 포함하지 않습니다. 취혈·자침 정보가 없는 행에는 일반 경외기혈의 시술 안내를 적용하지 않고 원본에 수록된 범위를 표시합니다.

'''
    for kind, heading in [('surface_anatomy', '표면해부학적 위치 확인'), ('auricular_anatomy', '귀 해부학'), ('auricular_point_combination', '이침 배혈 예시')]:
        text += f'### {heading}\n\n'
        for code, info in config['records'].items():
            if supplementary_type(code) == kind:
                text += f"- [{info['title']} ({code})](../acupuncture/extra-points/{code.lower()}.md)\n"
        text += '\n'
    text += '→ [WHO 표준 361경혈 임상 아틀라스](standard-atlas.md)\n'
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for path, content in outputs().items():
        if not path.exists() or path.read_text(encoding='utf-8-sig') != content:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(content, encoding='utf-8')
    if args.check and changed:
        raise SystemExit('Supplemental pages out of sync: ' + ', '.join(changed))
    print(f'Supplemental record taxonomy: PASS (7 records; {len(changed)} updates)')


if __name__ == '__main__':
    main()
