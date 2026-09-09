"""Insert the shared, selected-point diagram into existing location sections."""
from functools import lru_cache
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LOCATION = re.compile(r'^(?:## 위치와 취혈|### WHO 표준 기반 위치)\s*$', re.M)
MARKER = '<!-- acupoint-location-diagram -->'


@lru_cache(maxsize=1)
def diagram_index():
    data = json.loads((ROOT / 'data/acupoint_diagrams.json').read_text(encoding='utf-8'))
    result = {}
    for region in data['regions']:
        for point in region['points']:
            if point['path'] in result:
                raise ValueError('Duplicate acupoint diagram destination: ' + point['path'])
            result[point['path']] = (region, point)
    return result


def on_pre_build(config):
    diagram_index.cache_clear()
    for path, (region, point) in diagram_index().items():
        asset = ROOT / 'docs/assets/acupoint-atlas' / (region['id'] + '.svg')
        if not asset.is_file() or not (ROOT / 'docs' / path).is_file():
            raise ValueError('Missing acupoint diagram or document: ' + path)
        if not LOCATION.search((ROOT / 'docs' / path).read_text(encoding='utf-8')):
            raise ValueError('Missing location section: ' + path)


def on_page_markdown(markdown, page, config, files):
    entry = diagram_index().get(page.file.src_uri)
    if entry is None or MARKER in markdown:
        return markdown
    region, point = entry
    match = LOCATION.search(markdown)
    if match is None:
        raise ValueError('Missing location section: ' + page.file.src_uri)
    code = escape(point['code'])
    title = escape(point['name'] + ' ' + point['code'])
    asset = '/assets/acupoint-atlas/' + region['id'] + '.svg#' + code
    note = escape(region['notes'])
    block = f'''\n\n{MARKER}
<div class="acupoint-location">
<object data="{asset}" type="image/svg+xml" aria-label="{title} 위치 도해"><img src="{asset}" alt="{title}이 강조된 {escape(region['title'])} 도해" width="640" height="660" loading="lazy"></object>
<p><strong>{title}</strong> · 붉은 표시가 이 문서의 경혈입니다. <a href="{asset}">그림 확대</a> · <a href="/acupoint-network/standard-atlas/#five-shu-diagrams">다른 부위·경혈 찾기</a></p>
<p>{note}</p>
<p class="acupoint-note">해부학적 위치 관계를 단순화한 교육용 도해입니다. 정확한 위치는 아래 설명과 함께 확인합니다.</p>
</div>
'''
    return markdown[:match.end()] + block + markdown[match.end():]
