"""Preserve retired network URLs, including legacy heading destinations."""
from __future__ import annotations
import html
import json
from pathlib import Path
from urllib.parse import quote, urljoin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files

MANIFEST = Path(__file__).with_name('network_consolidations.json')


def load_routes():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


def public_url(document, site_url):
    path, _, fragment = document.partition('#')
    if not path.endswith('.md') or path.startswith('/') or '..' in Path(path).parts:
        raise ValueError('Expected a relative Markdown destination')
    path = path[:-8] if path.endswith('/index.md') else path[:-3] + '/'
    return urljoin(site_url, path) + ('#' + quote(fragment, safe='-_.~') if fragment else '')


def render_redirect(route, site_url):
    destinations = {'': public_url(route['target'], site_url)}
    destinations.update({key: public_url(value, site_url) for key, value in route['anchors'].items()})
    target = destinations['']
    payload = json.dumps(destinations, ensure_ascii=False).replace('<', '\\u003c')
    return '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<title>통합된 문서로 이동</title><meta name="robots" content="noindex,follow">
<link rel="canonical" href="%s">
<script>const destinations=%s;
let fragment=location.hash.slice(1);try{fragment=decodeURIComponent(fragment)}catch(e){}
location.replace(destinations[fragment]||destinations[""]);
</script><noscript><meta http-equiv="refresh" content="0;url=%s"></noscript>
</head><body><p>관련 설명을 통합했습니다. <a href="%s">대표 문서로 이동</a></p></body></html>
''' % (html.escape(target.split('#')[0], quote=True), payload, html.escape(target, quote=True), html.escape(target, quote=True))


@event_priority(100)
def on_files(files, config, **kwargs):
    retired = load_routes()
    return Files(file for file in files if file.src_uri not in retired)


@event_priority(-100)
def on_post_build(config, **kwargs):
    site = Path(config['site_dir'])
    for source, route in load_routes().items():
        path = site / source.removesuffix('.md') / 'index.html'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_redirect(route, config['site_url']), encoding='utf-8')
