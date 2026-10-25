"""Check published provenance against article exports and original SVG sources."""
import json
from hashlib import sha256
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from content_provenance import ROOT, MANIFEST, digest, document_id


def audit(site):
    data = json.loads((site / MANIFEST).read_text())
    index = json.loads((site / 'assets/ai/page-index.json').read_text())['pages']
    records = {row['url']: row for row in data['documents']}
    search_index = json.loads((site/'assets/provenance/search-index.json').read_text())
    batched = [row for batch in search_index['batches'] for row in json.loads((site/batch['path']).read_text())['documents']]
    assert {row['url'] for row in batched} == {row['url'] for row in records.values() if row['search_samples']}, 'Search batches incomplete'
    assert len(batched) == len({row['url'] for row in batched}), 'Duplicate search batch documents'
    assert len(records) == len(data['documents']) == len(index), 'Missing/duplicate provenance document'
    assert len({r['document_id'] for r in records.values()}) == len(records), 'Document ID collision'
    for row in index:
        record = records[row['url']]
        path = unquote(urlsplit(row['document']).path).lstrip('/')
        payload = json.loads((site / path).read_text())
        assert record['document_id'] == document_id(row['url']), row['url']
        assert digest(payload['text']) == record['text_sha256'], row['url']
        assert payload['provenance']['text_sha256'] == record['text_sha256'], row['url']
        html_path = site / Path(path.removeprefix('assets/ai/pages/')).with_suffix('.html')
        html = html_path.read_text()
        assert html.count('data-archive-provenance ') == 1, row['url']
        assert f'content="{record["document_id"]}"' in html, row['url']
        assert f'content="{record["text_sha256"]}"' in html, row['url']
        assert 'content-provenance.js' in html, row['url']
        assert 'content-provenance.css' in html, row['url']
        assert re.fullmatch('[0-9a-f]{64}', record['source_sha256']), row['url']
        assert sha256((ROOT/'docs'/record['source_path']).read_bytes()).hexdigest() == record['source_sha256'], row['url']
    for asset in data['artwork']:
        published = site / asset['path']
        source = ROOT / 'docs' / asset['path']
        original, marked = source.read_text(), published.read_text()
        assert sha256(marked.encode()).hexdigest() == asset['published_sha256'], str(published)
        assert 'id="minseong-provenance-watermark"' not in original, str(source)
        assert marked.count('id="minseong-provenance-watermark"') == 1, str(published)
        before, after = ET.fromstring(original), ET.fromstring(marked)
        old_ids = {e.attrib['id'] for e in before.iter() if 'id' in e.attrib}
        new_ids = {e.attrib['id'] for e in after.iter() if 'id' in e.attrib}
        assert old_ids <= new_ids, str(published)
        assert before.attrib['viewBox'] == after.attrib['viewBox'], str(published)
    print(f'Content provenance verified: {len(records)} documents, {len(data["artwork"])} SVGs; no errors')


if __name__ == '__main__':
    audit(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'site')
