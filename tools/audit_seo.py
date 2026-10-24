"""Validate indexable HTML identity; inventory missing and generic descriptions."""
import argparse
from collections import Counter
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

import yaml

from audit_page_discovery import site_path


class Signals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.titles, self.meta = [], [], {}
        self._title = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self._title = []
        if tag == 'link' and 'canonical' in attrs.get('rel', '').split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property', '')).lower()
            self.meta.setdefault(key, []).append(attrs.get('content', ''))

    def handle_data(self, data):
        if self._title is not None:
            self._title.append(data)

    def handle_endtag(self, tag):
        if tag == 'title' and self._title is not None:
            self.titles.append(''.join(self._title).strip())
            self._title = None


def validate(html, url):
    signals = Signals()
    signals.feed(html)
    if len(signals.titles) != 1 or not signals.titles[0]:
        raise ValueError(f'Missing or duplicate title: {url}')
    if signals.canonicals != [url]:
        raise ValueError(f'Canonical must match sitemap URL exactly: {url}')
    if signals.meta.get('og:url') != [url]:
        raise ValueError(f'Open Graph URL must match canonical: {url}')
    for key in ('og:title', 'og:site_name', 'og:locale', 'twitter:card', 'twitter:title'):
        values = signals.meta.get(key, [])
        if len(values) != 1 or not values[0].strip():
            raise ValueError(f'Missing or duplicate {key}: {url}')
    for value in signals.meta.get('robots', []) + signals.meta.get('googlebot', []):
        if {'noindex', 'none'} & set(value.lower().replace(',', ' ').split()):
            raise ValueError(f'Non-indexable URL included in sitemap: {url}')
    descriptions = signals.meta.get('description', [])
    if len(descriptions) > 1:
        raise ValueError(f'Duplicate description tags: {url}')
    return signals


def normalize_description(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()


def description_inventory(site, site_description=''):
    urls = [node.text for node in ET.parse(site / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if not urls or len(urls) != len(set(urls)):
        raise ValueError('Sitemap must contain unique URLs')
    from urllib.parse import urlsplit
    parts = urlsplit(urls[0])
    base = f'{parts.scheme}://{parts.netloc}/'
    pages = []
    for url in urls:
        signals = validate(site_path(site, url, base).read_text(encoding='utf-8'), url)
        text = normalize_description(signals.meta.get('description', [''])[0])
        pages.append({'url': url, 'description': text})
    descriptions = Counter(page['description'] for page in pages)
    generic = normalize_description(site_description)
    return {
        'page_count': len(pages),
        'empty_urls': [page['url'] for page in pages if not page['description']],
        'site_description_urls': [page['url'] for page in pages if generic and page['description'] == generic],
        'duplicate_groups': [
            {'description': text, 'urls': [page['url'] for page in pages if page['description'] == text]}
            for text, count in descriptions.items() if text and count > 1
        ],
        'pages': pages,
    }


def audit(site):
    inventory = description_inventory(site)
    return inventory['page_count'], Counter(page['description'] for page in inventory['pages'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', type=Path, default=Path('site'))
    parser.add_argument('--config-file', type=Path, default=Path('mkdocs.yml'))
    parser.add_argument('--report', type=Path, help='Write the description inventory and affected URLs as JSON')
    args = parser.parse_args()
    try:
        config = yaml.safe_load(args.config_file.read_text(encoding='utf-8'))
        inventory = description_inventory(args.site_dir, config.get('site_description', ''))
        count = inventory['page_count']
    except (ValueError, OSError, ET.ParseError) as error:
        print(f'SEO audit failed: {error}')
        return 1
    print(f'SEO: {count} sitemap URLs; titles, canonicals, social identity and indexability valid')
    shared = sum(len(group['urls']) for group in inventory['duplicate_groups'])
    print(f'Description inventory: {len(inventory["empty_urls"])} empty; {shared} pages share a description')
    print(f'Site-wide description: {len(inventory["site_description_urls"])} pages (the homepage may intentionally use it)')
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
