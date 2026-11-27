"""Check generated page JSON, structured data, and heading anchors against HTML."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from ontology import page_projections


class PageHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.alternates = []
        self.schemas = []
        self.ontologies = []
        self._script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'link' and attrs.get('rel') == 'alternate' and attrs.get('type') == 'application/json':
            self.alternates.append(attrs.get('href'))
        if tag == 'link' and attrs.get('rel') == 'describedby' and attrs.get('type') == 'application/ld+json':
            self.ontologies.append(attrs.get('href'))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self._script = []

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self._script is not None:
            self.schemas.append(json.loads(''.join(self._script)))
            self._script = None


def site_path(site, url, base):
    parsed, root = urlsplit(url), urlsplit(base)
    prefix = root.path.rstrip('/') + '/'
    if (parsed.scheme, parsed.netloc) != (root.scheme, root.netloc) or not parsed.path.startswith(prefix):
        raise ValueError(f'URL outside this site: {url}')
    target = (site / unquote(parsed.path[len(prefix):])).resolve()
    if not target.is_relative_to(site.resolve()):
        raise ValueError(f'Path outside site_dir: {url}')
    return target / 'index.html' if parsed.path.endswith('/') else target


def audit(site):
    index = json.loads((site / 'assets/ai/page-index.json').read_text(encoding='utf-8'))
    pages, base = index['pages'], index['base_url']
    expected = {element.text for element in ET.parse(site / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    urls = [row['url'] for row in pages]
    documents = [row['document'] for row in pages]
    if not pages or set(urls) != expected or len(set(urls)) != len(urls) or len(set(documents)) != len(documents):
        raise ValueError('Page index must cover each sitemap URL exactly once, with unique documents')
    global_ontology = site / 'assets/ai/ontology.jsonld'
    projections = page_projections(json.loads(global_ontology.read_text(encoding='utf-8'))) if global_ontology.exists() else {}
    if set(projections) - set(urls):
        raise ValueError('Ontology source pages must be public sitemap pages')
    heading_count = 0
    for row in pages:
        parser = PageHTML()
        parser.feed(site_path(site, row['url'], base).read_text(encoding='utf-8'))
        if parser.alternates != [row['document']] or not parser.schemas:
            raise ValueError(f'Missing or duplicate discovery metadata: {row["url"]}')
        payload = json.loads(site_path(site, row['document'], base).read_text(encoding='utf-8'))
        if payload['url'] != row['url'] or payload['title'] != row['title']:
            raise ValueError(f'Document identity mismatch: {row["url"]}')
        projection = projections.get(row['url'])
        if projection:
            ontology = payload.get('ontology', {})
            document = ontology.get('document')
            if (not document or row.get('ontology_document') != document
                    or parser.ontologies.count(document) != 1
                    or ontology.get('concept_ids') != projection['concept_ids']
                    or ontology.get('statement_ids') != projection['statement_ids']):
                raise ValueError(f'Ontology discovery metadata mismatch: {row["url"]}')
            projected = json.loads(site_path(site, document, base).read_text(encoding='utf-8'))
            if projected != projection['payload']:
                raise ValueError(f'Ontology projection mismatch: {row["url"]}')
        elif 'ontology' in payload or 'ontology_document' in row:
            raise ValueError(f'Unexpected ontology metadata: {row["url"]}')
        for heading in payload['headings']:
            if heading['url'].split('#', 1)[0] != row['url'] or unquote(urlsplit(heading['url']).fragment) not in parser.ids:
                raise ValueError(f'Missing heading anchor: {heading["url"]}')
            heading_count += 1
        for item in payload['related_reading']:
            if not site_path(site, item['url'], base).is_file():
                raise ValueError(f'Missing related document: {item["url"]}')
    return len(pages), heading_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', type=Path, default=Path('site'))
    args = parser.parse_args()
    try:
        pages, headings = audit(args.site_dir)
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print(f'Page discovery audit failed: {error}')
        return 1
    print(f'Page discovery: {pages} documents, {headings} heading anchors; no errors')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
