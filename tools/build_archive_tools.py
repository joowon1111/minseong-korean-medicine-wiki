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
    text = re.sub(r'(?m)^\|[ :|\-]+\|[ \t]*$', '', text)
    text = re.sub(r'(?m)^\|(.+?)\|[ \t]*$', lambda m: ' · '.join(c.strip() for c in m[1].split('|')), text)
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
    from urllib.parse import quote
    return '/' if p == 'index' else '/' + quote(p[:-5] if p.endswith('/index') else p + '/', safe='/')

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


def linked_documents(body, source):
    """Resolve actual markdown links, including section-local Sasang references."""
    from urllib.parse import urlsplit
    import posixpath
    links = set()
    for raw in re.findall(r'\]\(([^)\s]+)', body):
        split = urlsplit(raw)
        if split.scheme or split.netloc:
            continue
        if not split.path:
            target = source.split('#')[0]
        else:
            target = posixpath.normpath(posixpath.join(source.split('#')[0].rstrip('/').rsplit('/', 1)[0], split.path)) if not split.path.startswith('/') else split.path
            if target.endswith('.md'):
                target = target[:-3].removesuffix('/index') + '/'
        if target.startswith(('/herbs/', '/formulas/', '/sasang-formula-')):
            links.add(target + ('#' + split.fragment if split.fragment else ''))
    return sorted(links)


def table_values(body):
    rows = []
    for line in body.splitlines():
        if not line.startswith('|') or re.match(r'^\|[ :|\-]+\|$', line):
            continue
        cols = [plain(c) for c in line.strip().strip('|').split('|')]
        if len(cols) >= 2:
            rows.append(cols)
    return rows


def formula_facts(body, parts, legacy):
    """Summaries quote existing rows/sections; never invent missing composition or doses."""
    rows = table_values(body)
    facts = []
    def field(label, keys, headings, limit=900):
        value = next((r[1] for r in rows if re.fullmatch(keys, r[0])), '')
        if not value:
            match = re.search(r'(?m)^\*\*(?:'+keys+r')[:：]\*\*\s*([^\n]+)', body)
            value = plain(match[1]) if match else ''
        if not value:
            value = next((plain(c) for h, a, c in parts if re.search(headings, h) and not h.startswith(('관련 증상','관련 변증','증상별 감별'))), '')
        if not value and label == '배합·치법':
            value = ' · '.join(f['value'] for f in legacy if re.search(r'구조|배합|치법', f['label']))
        if value:
            facts.append({'label': label, 'value': value[:limit]})
    # A source/edition is read from its own recorded line, not a mixed dose table.
    value = next((r[1] for r in rows if r[0] in ('출전', '대조 출전', '근거와 한계')), '')
    if not value:
        match = re.search(r'(?m)^(?:\*\*(?:대조 수록본|출전)[^\n]*|출전[:：][^\n]+)', body)
        value = plain(match[0]) if match else next((plain(c).split('원문 발췌')[0] for h,a,c in parts if re.search('출전|원전|근거',h)), '')
    if value:
        facts.append({'label':'출전·판본','value':value[:600]})
    field('병증·주치', r'중심 병증|중심 증후|병증 위치|적용 소증·병증 단계|주치|전통적 주치|핵심 증후|핵심 병기|대표 단서|대표 증상축', r'전통적 주치|전통적 활용|임상.*단서|임상.*선택|병증 위치|효능|주치|깊이 읽기')
    composition = next((r[1] for r in rows if re.fullmatch(r'기본 구성|원방 약미|구성·법제|핵심 구성|구성', r[0])), '')
    if not composition:
        match=re.search(r'(?m)^\*\*구성[^\n]*?[:：]\*\*\s*([^\n]+)', body)
        composition=plain(match[1]) if match else ''
    if not composition:
        for h,a,c in parts:
            if re.search(r'구성|약량|용량', h):
                table = table_values(c)
                if len(table) > 1 and re.search(r'본초|약재|약명|구성|약미', table[0][0]):
                    composition = ' · '.join(' '.join(r[:2]) for r in table[1:])
                    break
    if not composition:
        composition = next((plain(c) for h,a,c in parts if re.search('구성',h)), '')
    if composition:
        facts.append({'label':'구성·약량','value':composition[:1400]})
    field('배합·치법', r'핵심 치법|치법|처방 구조|구조|병리 축|중심 치법', r'처방 구조|구성축|배합|방제 구조')
    field('유사 처방·감별', r'감별 처방|가까운 비교|가까운 처방과 감별', r'유사 처방|가까운 처방|비슷한 처방|비교.*처방|감별|계열의 연결|처방의 확장|이공산.*육군자탕')
    field('법제·제형', r'제형|제법|현대 조제의 핵심', r'수치.*법제|법제.*전탕|제형|제법')
    field('안전·관찰', r'주의사항|복용·관찰|경과·안전', r'안전|금기|주의|경과 관찰|경과관찰|복용과 경과|오해 바로잡기')
    return facts or [{'label':'본문 개요','value':plain(body)[:600]}]



def add_classical_recipes(cards):
    """Index missing named recipes only where a clause records its own ingredients."""
    known = {re.split(r'[（( ·—]', c['title'])[0] for c in cards if c['kind']=='formula' and c['source'].startswith('/formulas/')}
    seen = set(known)
    appendix=DOCS/'formula-architecture/shanghan-family.md'
    if appendix.exists():
        _,body=parse(appendix.read_text(encoding='utf-8-sig'))
        match=re.search(r'(?ms)^### 외대복령음[^\n]*\{#waidai-fuling-yin\}\n(.*?)(?=^## |\Z)',body)
        if match:
            chunk=match[1];source=url_for(appendix)+'#waidai-fuling-yin'
            rows=table_values(chunk)
            cards.append({'id':'classical-waidai-fuling-yin','title':'외대복령음(茯苓飲) · 금궤요략 부방','category':'금궤요략 부방','kind':'formula','system':'일반 방제','source':source,'aliases':['복령음','외대복령음','茯苓飲'],'peers':[],
                'facts':[{'label':'출전·판본','value':'《금궤요략》 담음해수병맥증병치 부방 · 《외대비요》 인용'},
                         {'label':'병증·주치','value':plain(chunk.strip().split('\n\n')[0])[:1000]},
                         {'label':'구성·약량','value':' · '.join(r[0] for r in rows[1:])},
                         {'label':'배합·치법','value':' · '.join(r[1] for r in rows[1:])},
                         {'label':'안전·관찰','value':'금궤요략 부방 수록량과 외대비요 계통의 용량 차이를 구분하며 현대 복용량으로 일괄 환산하지 않습니다.'}],
                'sections':[{'title':'부방의 출전·구성·해설','text':plain(chunk)[:3000],'url':source}], 'links':linked_documents(chunk,source)})

    for folder,work in [('shanghanlun/clauses','상한론'),('jinkui-yaolue/chapters','금궤요략')]:
        for path in sorted((DOCS/'classics'/folder).glob('*.md')):
            meta,body=parse(path.read_text(encoding='utf-8-sig'))
            headings=list(re.finditer(r'^## (.+?) \{#([^}]+)\}\s*$',body,re.M))
            for i,h in enumerate(headings):
                chunk=body[h.end():headings[i+1].start() if i+1<len(headings) else len(body)]
                recipes=list(re.finditer(r'(?m)^[ \t]*([\u3400-\u9fff]+(?:湯|丸|散|飲|丹))方(?:[：:][^\n]*|[ \t]*)$',chunk))
                names=re.findall(r'[가-힣]+(?:탕|환|산|음|단)',h[1])
                if not recipes or len(names)!=1 or names[0] in seen or names[0] in ('수음','승기탕','청룡탕','음호산'):
                    continue
                recipe=recipes[0]
                recipe_text=chunk[recipe.end():recipes[1].start() if len(recipes)>1 else len(chunk)]
                lines=[line.strip() for line in recipe_text.splitlines() if line.strip()]
                if not lines or not re.search(r'[（(].*?[兩枚升斤錢分合]',lines[0]):
                    continue
                name=names[0];seen.add(name)
                source=url_for(path)+'#'+h[2]
                context=re.sub(r'\?\?\?.*','',chunk[:recipe.start()])
                directions=next((line for line in lines[1:] if line.startswith(('右','上'))),'')
                cards.append({'id':'classical-'+path.stem+'--'+h[2], 'title':name+'('+recipe[1]+') · '+work+' 원방','category':work+' 원방','kind':'formula','system':'일반 방제','source':source,'aliases':[name,recipe[1]],'peers':[],
                              'facts':[{'label':'출전·판본','value':str(meta.get('title',work))+' · '+h[1]},
                                       {'label':'병증·주치','value':plain(context)[:1100]},
                                       {'label':'구성·약량','value':lines[0]},
                                       {'label':'법제·제형','value':directions[:1400]},
                                       {'label':'안전·관찰','value':'원전에 기록된 역사적 약량·제법입니다. 현대 복용량이나 자가 조제 지침으로 사용하지 않고 원전·현재 제제·금기와 법제를 구분해 확인합니다.'}],
                              'sections':[{'title':'조문·처방 구성·제법 원문','text':plain(chunk)[:3000],'url':source}], 'links':linked_documents(chunk,source)})


def expand_catalog(cards, by_url):
    """Include actual Sasang cards and every anchored formula in the extended libraries."""
    paths = list((DOCS/'sasang-formula-cards').glob('*.md'))
    known = {c['source'] for c in cards}
    for path in sorted(paths):
        meta, body = parse(path.read_text(encoding='utf-8-sig'))
        h1 = re.search(r'^# (.+)', body, re.M)
        if not h1 or not re.match(r'[^\s(]+(?:탕|산|환|음|단)\(', h1[1]):
            continue
        source = url_for(path)
        if source not in known:
            cards.append({'id':'document-sasang-formula-cards-'+path.stem,'title':plain(h1[1]).replace(' 임상 카드',''),'category':'사상처방','kind':'formula','facts':[],'source':source,'aliases':[],'peers':[]})
    for path in sorted((DOCS/'sasang-formula-library').glob('*-extended-formulas.md')):
        meta, body = parse(path.read_text(encoding='utf-8-sig'))
        # Keep every h3 paragraph inside its h2 formula, rather than truncating at the first subsection.
        matches = list(re.finditer(r'^## (.+?) \{#([^}]+)\}\s*$', body, re.M))
        for i,m in enumerate(matches):
            if not re.match(r'[^\s(]+(?:탕|산|환|음|단)\(', m[1]):
                continue
            chunk = body[m.end():matches[i+1].start() if i+1<len(matches) else len(body)]
            source = url_for(path)+'#'+m[2]
            by_url[source] = ('# '+m[1]+'\n'+chunk, list(sections(chunk)))
            cards.append({'id':'document-sasang-formula-library-'+path.stem+'--'+m[2],'title':m[1],'category':'사상처방','kind':'formula','facts':[],'source':source,'aliases':[],'peers':[]})
    groups_path = DOCS/'assets/archive-tools/formula-groups.json'
    groups = json.loads(groups_path.read_text())['groups'] if groups_path.exists() else []
    source_categories = {url:g['category'] for g in reversed(groups) for url in g['sources']}
    for row in cards:
        if row['kind'] != 'formula':
            continue
        source = row['source']
        # Existing family/overview IDs remain available for saved URLs but are not counted as individual prescriptions.
        if not source.startswith(('/formulas/','/sasang-formula-')) or ('extended-formulas/' in source and '#' not in source) or '상세 문서 안내' in row['title']:
            row['kind']='guide'
            continue
        body, parts = by_url.get(source, by_url.get(source.split('#')[0], ('',[])))
        row['facts'] = formula_facts(body,parts,row['facts'])
        if len(row['facts']) < 3 and body:
            existing={f['label'] for f in row['facts']}
            for label,pattern in [('원문·해석',r'원문|풀이|해석'),('본문 설명',r'어떤 처방|제제|대상|한눈에 보기|구성과 배합')]:
                value=next((plain(c) for h,a,c in parts if re.search(pattern,h)),'')
                if value and label not in existing: row['facts'].append({'label':label,'value':value[:1000]})
        row['links'] = linked_documents(body, source)
        row['sections'] = [{'title':h,'text':plain(c)[:2400],'url':source.split('#')[0]+('#'+(a or source.split('#',1)[1]) if a or '#' in source else '')}
                           for h,a,c in parts if re.search(r'出典|출전|원문|원전|구성|약량|용량|주치|효능|병기|안전|금기|법제|제형|근거|감별',h)][:12]
        if '#' in source and not row['sections']:
            row['sections']=[{'title':'개별 처방 본문·출전','text':plain(body)[:2400],'url':source}]
        if source.startswith('/sasang-formula-'):
            if 'soyangin-' in source: type_='소양인'
            elif 'soeumin-' in source: type_='소음인'
            elif 'taeeumin-' in source: type_='태음인'
            else: type_=next((t for t in ('소양인','소음인','태음인','태양인') if t in body[:1200]), '사상체질')
            row['system']=type_
            row['category']='사상처방 · '+type_
            if type_ not in row['title']:
                row['title']=row['title'].replace(' 임상 카드','')+' · '+type_
        else:
            row['system']='일반 방제'
            if source in source_categories: row['category']=source_categories[source]
            elif row['category']=='그 밖의 본문 자료': row['category']='그 밖의 일반 방제'
        row['aliases'] = list(dict.fromkeys(row.get('aliases',[])+[plain(re.sub(r'\([^)]*\)| · .*| — .*','',row['title']))]))
    add_classical_recipes(cards)
    by_source = {c['source']:c for c in cards if c['kind']=='formula'}
    resolved=[]
    for group in groups:
        missing=[u for u in group['sources'] if u not in by_source]
        if missing:
            raise ValueError(f"Comparison group {group['id']} has missing formulas: {missing}")
        ids=[by_source[u]['id'] for u in group['sources']]
        resolved.append({k:v for k,v in group.items() if k!='sources'} | {'ids':ids})
        for u in group['sources']:
            row=by_source[u]
            row['peers']=list(dict.fromkeys(row.get('peers',[])+[i for i in ids if i!=row['id']]))
    return resolved


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
                'classic' if url.startswith(('/classics/', '/classics-network/', '/donguibogam-', '/shanghan-', '/jingui-', '/neijing-', '/wenbing-', '/bangyakhappyeon-', '/donguisusebowon-')) else
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
    known_sources = {row['source'].split('#')[0] for row in cards}
    candidates = list((DOCS / 'formulas').glob('*.md')) + list((DOCS / 'herbs').glob('*.md')) + list((DOCS / 'sasang-formula-library').glob('*.md'))
    for path in sorted(candidates):
        source = url_for(path)
        if path.stem == 'index' or source in known_sources:
            continue
        meta, body = parse(path.read_text(encoding='utf-8-sig'))
        h1 = re.search(r'^#\s+(.+)$', body, re.M)
        title = plain(re.sub(r'\{#[^}]+\}', '', h1.group(1))) if h1 else str(meta.get('title', path.stem))
        parts = list(sections(body))
        kind = 'herb' if path.parent.name == 'herbs' else 'formula'
        facts = []
        for label, pattern in [('출전·기원', r'출전|기원'), ('구성·약용 부위', r'구성|약용 부위|용량|약량'), ('효능·주치', r'효능|주치'), ('성미·귀경', r'성미|귀경')]:
            text = next((plain(c) for h, a, c in parts if re.search(pattern, h)), '')
            if text:
                facts.append({'label': label, 'value': text[:1200]})
        if not facts:
            facts = [{'label': '문서 개요', 'value': plain(body)[:600]}]
        cards.append({'id': 'document-' + path.parent.name + '-' + path.stem, 'title': title,
                      'category': '사상의학 처방' if path.parent.name == 'sasang-formula-library' else '그 밖의 본문 자료',
                      'kind': kind, 'aliases': [], 'peers': [], 'source': source, 'facts': facts,
                      'sections': [{'title': h, 'text': plain(c)[:1800], 'url': source + ('#' + a if a else '')}
                                   for h, a, c in parts if re.search(r'출전|구성|약량|용량|주치|효능|병기|안전|금기|성미|귀경|기원|부위', h)][:8],
                      'links': []})
    groups = expand_catalog(cards, by_url)
    return {'schema': 1, 'cards': cards, 'groups': groups}, {'schema': 1, 'passages': passages}

def main():
    comparison, search = build()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in [('comparison.json', comparison), ('passages.json', search)]:
        write_bytes(OUT / name, (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    print(f"Archive tools: {len(comparison['cards'])} comparison cards, {len(search['passages'])} cited passages")

if __name__ == '__main__':
    main()
