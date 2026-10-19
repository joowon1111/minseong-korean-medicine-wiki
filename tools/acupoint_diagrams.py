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
    meridian_index.cache_clear()
    for path, (region, point) in diagram_index().items():
        prefix = re.fullmatch(r'([A-Z]+)(\d+)', point['code'])[1]
        route = meridian_index()[prefix]
        if not (ROOT / 'docs' / route['path']).is_file():
            raise ValueError('Missing meridian document: ' + route['path'])
        asset = ROOT / 'docs/assets/acupoint-atlas' / (region['id'] + '.svg')
        if not asset.is_file() or not (ROOT / 'docs' / path).is_file():
            raise ValueError('Missing acupoint diagram or document: ' + path)
        if not LOCATION.search((ROOT / 'docs' / path).read_text(encoding='utf-8')):
            raise ValueError('Missing location section: ' + path)


def sequence_navigation(point):
    """Follow numeric order within one meridian, never across its endpoints."""
    meridian, number = re.fullmatch(r'([A-Z]+)(\d+)', point['code']).groups()
    points = {p['code']: p for _, p in diagram_index().values()}
    links = []
    for offset, label, rel in [(-1, '← 이전 경혈', 'prev'), (1, '다음 경혈 →', 'next')]:
        neighbor = points.get(meridian + str(int(number) + offset))
        if neighbor:
            url = '/' + neighbor['path'].removesuffix('.md') + '/'
            title = neighbor['name'] + ' ' + neighbor['code']
            links.append(f'<a rel="{rel}" href="{escape(url)}"><span class="acupoint-sequence-label">{label}</span><strong>{escape(title)}</strong></a>')
    return '<nav class="acupoint-sequence" aria-label="같은 경맥의 이전·다음 경혈">' + '\n'.join(links) + '</nav>'


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
<p><a class="md-button" href="/acupoint-network/3d-map/?point={code}">3D 지도에서 {title} 보기 →</a></p>
{sequence_navigation(point)}
<object data="{asset}" type="image/svg+xml" aria-label="{title} 위치 도해"><img src="{asset}" alt="{title}이 강조된 {escape(region['title'])} 도해" width="640" height="660" loading="lazy"></object>
<p><strong>{title}</strong> · 붉은 표시가 이 문서의 경혈입니다. <a href="{asset}">그림 확대</a> · <a href="/acupoint-network/standard-atlas/#five-shu-diagrams">다른 부위·경혈 찾기</a></p>
<p>{note}</p>
<p class="acupoint-note">해부학적 위치 관계를 단순화한 교육용 도해입니다. 정확한 위치는 아래 설명과 함께 확인합니다.</p>
</div>
'''
    return markdown[:match.end()] + block + markdown[match.end():]


@lru_cache(maxsize=1)
def meridian_index():
    """Use the same canonical names and destinations as the meridian diagrams."""
    routes = json.loads((ROOT / 'data/meridian_routes.json').read_text(encoding='utf-8'))['routes']
    return {route['code']: route for route in routes}


def on_page_content(html, page, config, files):
    """Keep heading text/anchors intact while placing its parent beside it."""
    entry = diagram_index().get(page.file.src_uri)
    if entry is None or 'class="acupoint-title-row"' in html:
        return html
    point = entry[1]
    prefix = re.fullmatch(r'([A-Z]+)(\d+)', point['code'])[1]
    route = meridian_index()[prefix]
    url = '/' + route['path'].removesuffix('.md') + '/'
    overview = '_5' if prefix in {'CV', 'GV'} else '_2'
    heading = re.search(r'<h1\b[^>]*>.*?</h1>', html, re.S)
    if heading is None:
        raise ValueError('Missing acupoint heading: ' + page.file.src_uri)
    block = (
        '<div class="acupoint-title-row">' + heading[0]
        + '<nav class="acupoint-meridian" aria-label="소속 경맥과 전체 경맥 탐색">'
        + f'<a class="acupoint-meridian-parent" href="{escape(url)}"><span>소속 경맥</span>'
        + f'<strong>{escape(route["title"])} {escape(prefix)} →</strong></a>'
        + '</nav></div>'
        + '<nav class="acupoint-meridian-overview" aria-label="경락·경맥 한눈에 보기">'
        + f'<a href="/meridian-network/#{overview}">경락·경맥 한눈에 보기 →</a></nav>'
    )
    return html[:heading.start()] + block + html[heading.end():]
