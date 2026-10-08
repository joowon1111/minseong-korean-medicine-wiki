#!/usr/bin/env python3
"""Build comparison cards and cited passage search from the archive itself."""
import json
import re
from pathlib import Path
import yaml
from atomic_output import write_bytes

DOCS = Path('docs')
OUT = DOCS / 'assets' / 'archive-tools'

def plain(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'!?\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'\s+', ' ', re.sub(r'[*`#]', '', text)).strip()

def parse(text):
    text = text.lstrip('\ufeff')
    if text.startswith('---\n'):
        parts = text.split('---', 2)
        return yaml.safe_load(parts[1]) or {}, parts[2]
    return {}, text

def url_for(path):
    p = path.relative_to(DOCS).as_posix()[:-3]
    return '/' if p == 'index' else '/' + (p[:-5] if p.endswith('/index') else p + '/')

def sections(body):
    chunks = re.split(r'(?m)^(#{1,6}\s+.+)$', body)
    title, anchor = '', ''
    for i in range(0, len(chunks), 2):
        content = chunks[i]
        if content.strip():
            yield title, anchor, content
        if i + 1 < len(chunks):
            heading = chunks[i + 1]
            match = re.search(r'\{#([^}]+)\}', heading)
            anchor = match.group(1) if match else ''
            title = plain(re.sub(r'\{#[^}]+\}', '', heading))

def build():
    passages = []
    by_url = {}
    for path in sorted(DOCS.rglob('*.md')):
        if 'templates' in path.parts:
            continue
        meta, body = parse(path.read_text(encoding='utf-8-sig'))
        url = url_for(path)
        h1 = re.search(r'^#\s+(.+)$', body, re.M)
        title = str(meta.get('title') or (plain(h1.group(1)) if h1 else path.stem))
        parts = list(sections(body))
        by_url[url] = (body, parts)
        kind = ('formula' if '/formulas/' in url or url.startswith('/sasang-formula') else
                'herb' if url.startswith('/herbs/') else
                'classic' if url.startswith(('/classics/', '/donguibogam-', '/shanghan-', '/jingui-', '/donguisusebowon-')) else
                'evidence' if url.startswith(('/research/', '/authority/', '/evidence-')) else 'clinical')
        for heading, anchor, content in parts:
            text = plain(content)
            if len(text) < 30:
                continue
            # Keep excerpts bounded; overlapping windows preserve phrases at boundaries.
            for offset in range(0, len(text), 750):
                excerpt = text[offset:offset + 900]
                if len(excerpt) < 30:
                    continue
                tags = meta.get('tags', [])
                passages.append({'title': title, 'heading': heading, 'url': url + ('#' + anchor if anchor else ''),
                                 'kind': kind, 'text': excerpt, 'tags': tags if isinstance(tags, list) else [str(tags)]})
    cards = []
    for subject in ('formulas', 'herbs'):
        deck = json.loads((DOCS / 'assets' / 'learning' / (subject + '.json')).read_text())
        for card in deck['cards']:
            row = {k: card[k] for k in ('id', 'title', 'category', 'facts', 'source')}
            row['kind'] = 'formula' if subject == 'formulas' else 'herb'
            row['aliases'] = card.get('aliases', [])
            row['peers'] = card.get('preferredPeers', [])
            source_url = card['source'].split('#')[0]
            body, parts = by_url.get(source_url, ('', []))
            row['sections'] = [{'title': h, 'text': plain(c)[:1800], 'url': source_url + ('#' + a if a else '')}
                               for h, a, c in parts if re.search(r'出典|출전|구성|약량|용량|주치|효능|병기|안전|금기|성미|귀경|기원|부위', h)][:8]
            row['links'] = sorted(set('/herbs/' + m + '/' for m in re.findall(r'\]\((?:\.\./)?herbs/([a-z0-9-]+)\.md(?:#[^)]*)?\)', body)))
            row['links'] += sorted(set('/formulas/' + m + '/' for m in re.findall(r'\]\((?:\.\./)?formulas/([a-z0-9-]+)\.md(?:#[^)]*)?\)', body)))
            cards.append(row)
    return {'schema': 1, 'cards': cards}, {'schema': 1, 'passages': passages}

def main():
    comparison, search = build()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in [('comparison.json', comparison), ('passages.json', search)]:
        write_bytes(OUT / name, (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    print(f"Archive tools: {len(comparison['cards'])} comparison cards, {len(search['passages'])} cited passages")

if __name__ == '__main__':
    main()
