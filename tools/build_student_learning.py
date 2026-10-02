"""Build traceable study decks from the archive, without clinical-dose questions.

The generated datasets are committed so the learning room also works on ordinary
MkDocs builds. IDs depend on source paths/codes, not the order of cards.
"""
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote, unquote
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from atomic_output import write_bytes

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = DOCS / 'assets/learning'
SUBJECTS = {'acupoints': '경혈학', 'acupuncture': '침구학', 'herbs': '본초학', 'formulas': '방제학'}


def clean(value):
    value = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', value)
    value = re.sub(r'<[^>]*>|\{#[^}]+\}', '', value)
    return re.sub(r'\s+', ' ', value.replace('*', '').replace('`', '')).strip()


def normalized(value):
    return re.sub(r'\([^)]*\)|[^a-zA-Z0-9가-힣]', '', clean(value)).lower()


def url(path):
    path = Path(path).as_posix()
    return '/' + quote(path[:-8] if path.endswith('index.md') else path[:-3] + '/', safe='/')


def sections(text):
    return re.findall(r'^## (.*?)\n(.*?)(?=^## |\Z)', text, re.M | re.S)


def table_rows(text):
    return [[clean(c.strip()) for c in line.strip().strip('|').split('|')]
            for line in text.splitlines() if line.startswith('|') and not re.match(r'^\|[ :|-]+\|$', line)]


def first_table(text):
    match = re.search(r'^\|[^\n]+\n(?:\|[^\n]+\n?)+', text, re.M)
    return table_rows(match[0]) if match else []


def card(identifier, title, category, facts, path, prompt=None):
    return {'id': identifier, 'title': title, 'category': category,
            'prompt': prompt or f'{title}의 핵심을 떠올려 보세요.',
            'facts': [{'label': k, 'value': clean(v)} for k, v in facts if clean(v)],
            'source': url(path), 'sourceTitle': title + ' 원문'}


def acupoints():
    catalog = json.loads((ROOT / 'data/acupoint_catalog.json').read_text())['points']
    atlas = json.loads((ROOT / 'data/acupoint_diagrams.json').read_text())['regions']
    region_by_code = {p['code']: r['id'] for r in atlas for p in r['points']}
    result = []
    for code, p in catalog.items():
        facts = [('혈명·경맥', f"{p['name_ko']}({p['name_zh']}) · {p['meridian']}"),
                 ('표준 위치', p['location_ko'])]
        attr = p.get('specific_attributes', {}).get('existing_summary')
        if attr and attr not in ('없음', '—', '-'):
            facts.append(('특정혈 요약', attr))
        c = card('point-' + code, f"{p['name_ko']} {code}", p['meridian'], facts, p['path'],
                 f"{code}의 혈명·경맥·위치를 떠올려 보세요.")
        c.update(code=code, name=p['name_ko'], diagram=f"/assets/acupoint-atlas/{region_by_code[code]}.svg#{code}",
                 quizDiagram=f"/assets/learning/diagrams/{region_by_code[code]}.svg#{code}")
        result.append(c)
    return result


def herb_cards():
    excluded = {'index', 'sasang-formula-reverse-index', 'astragalus-tonic-guide',
                'alisma-extra', 'musk', 'fresh-rehmannia', 'rehmannia-preparata'}
    result = []
    for p in sorted((DOCS / 'herbs').glob('*.md')):
        if p.stem in excluded:
            continue
        text = p.read_text(encoding='utf-8-sig')
        title = clean(re.search(r'^# (.*)', text, re.M)[1])
        facts = {}
        aliases = {'생약명': '생약명', '대표 생약명': '생약명', '국제 생약명': '생약명',
                   '생약명 계열': '생약명', '약용 부위': '약용 부위', '약용부위': '약용 부위',
                   '기원·약용부위': '기원·약용 부위', '기원·약용 부위': '기원·약용 부위',
                   '대표 기원·약용 부위': '기원·약용 부위', '성미': '성미', '귀경': '귀경',
                   '성미·귀경': '성미·귀경', '전통적 성미·귀경': '성미·귀경', '성미(性味)': '성미',
                   '귀경(歸經)': '귀경', '핵심 효능': '전통 효능', '전통 효능': '전통 효능',
                   '전통 효능축': '전통 효능', '전통적 효능': '전통 효능'}
        # Only key/value tables; comparison tables are never read as the herb's identity.
        for cells in table_rows(text):
            if len(cells) == 2 and cells[0] in aliases and not any(w in cells[1] for w in ['함께 보는', '처방에서 확인']):
                facts.setdefault(aliases[cells[0]], cells[1])
        for label, value in re.findall(r'^-?\s*\*\*([^:*]+):\*\*\s*(.+)', text, re.M):
            if label in aliases:
                facts.setdefault(aliases[label], clean(value))
        for label, value in re.findall(r'^- ([^:]+):\s*(.+)', text, re.M):
            if label in aliases:
                facts.setdefault(aliases[label], clean(value))
        for heading, body in sections(text):
            if '효능' not in heading:
                continue
            rows = table_rows(body)
            if rows and rows[0][0] in ('효능', '전통 효능'):
                facts.setdefault('전통 효능', ' · '.join(r[0] for r in rows[1:]))
                break
            if heading.startswith(('전통적 효능', '전통적 핵심 효능')):
                bold = re.findall(r'\*\*([^*]+)\*\*', body.split('\n\n')[0])
                if not bold:
                    bold = re.findall(r'^- \*\*([^*]+)\*\*', body, re.M)
                if bold:
                    facts.setdefault('전통 효능', ' · '.join(bold))
                    break
        # A few prose-led documents intentionally have no identity table.
        prose = {
            'atractylodes': ('건비익기(健脾益氣)·조습이수(燥濕利水)·지한(止汗)', 'intro'),
            'honey': ('보중·윤조·완급·조화', 'intro'),
            'elm-root-bark': ('이수통림·소종산결', 'intro'),
            'cervi-parvum-cornu': ('보신양·익정혈·강근골·조충임·탁창독', 'table'),
            'fritillaria': ('청열윤폐(淸熱潤肺)·화담지해(化痰止咳)·산결(散結)', 'intro'),
        }
        if p.stem in prose:
            value, _ = prose[p.stem]
            assert all(token in text for token in re.findall(r'[가-힣]{2,}', value)), p
            facts.setdefault('전통 효능', value)
        if p.stem == 'mihudeung':
            facts['문헌 이름 구분'] = '미후등식장탕의 처방명과 후대 구성의 미후도 표기를 구분하며, 식물 기원·약용 부위를 임의로 확정하지 않습니다.'
        for heading, part in sections(text):
            if any(w in heading for w in ['효능', '전통 본초학']) and '전통 효능' not in facts:
                definitions = re.findall(r'^- \*\*([^:*]+):\*\*', part, re.M)
                if definitions:
                    facts['전통 효능'] = ' · '.join(definitions)
                    break
        if '기원·약용 부위' in facts and any(w in facts.get('약용 부위', '') for w in ['인지', '시험물']):
            del facts['약용 부위']
        # Application rows give context beyond a memorized name list.
        for heading, body in sections(text):
            if any(w in heading for w in ['대표 처방', '처방에서', '주요 처방']):
                rows = table_rows(body)
                if rows and len(rows[0]) >= 2:
                    examples = [' — '.join(r) for r in rows[1:3]]
                    if examples:
                        facts['배합 예'] = ' / '.join(examples)
                break
        tags = re.search(r'^tags:\s*\[(.*)\]', text, re.M)
        candidates = [x.strip() for x in tags[1].split(',')] if tags else []
        categories = {'보익약': '보익·수삽', '수삽약': '보익·수삽', '해표약': '산한해표·소산풍열',
                      '청열사화약': '청열', '청열조습약': '청열', '청열해독약': '청열', '청열량혈약': '청열',
                      '이수삼습약': '이수·거습', '온리약': '온리', '이기약': '화담·이기·소식'}
        category = next((categories[x] for x in candidates if x in categories), '핵심 본초')
        if category == '핵심 본초':
            efficacy = facts.get('전통 효능', '')
            groups = [('산한해표·소산풍열', ['해표', '발한', '소산풍열', '발표산풍', '해기발표']),
                      ('보익·수삽', ['보기', '보혈', '보비', '보신', '보간신', '자보간신', '양혈', '양음', '대보원기', '온신', '수렴', '렴폐']),
                      ('청열', ['청열', '사화', '량혈', '사폐', '청허열']),
                      ('활혈·거풍습', ['활혈', '파혈', '거풍습', '거풍제습', '속상']),
                      ('화담·이기·소식', ['화담', '거담', '이기', '행기', '소간', '파기', '消痞', '소식', '강기', '하기']),
                      ('이수·거습', ['이수', '삼습', '화습', '조습']),
                      ('온리', ['온중', '회양', '산한지통', '보화']),
                      ('안신·개규·식풍', ['안신', '식풍', '개규']),
                      ('사하·윤장', ['사하', '윤장'])]
            category = next((group for group, tokens in groups if any(t in efficacy for t in tokens)), '기원·문헌 본초')
        if not facts:
            raise ValueError(f'No substantive facts: {p}')
        result.append(card('herb-' + p.stem, title, category, list(facts.items()), p.relative_to(DOCS),
                           f'{title}의 효능·약용 부위·배합을 설명해 보세요.'))
    return result


def formula_cards():
    text = (DOCS / 'herbal-integrated/general-formulary.md').read_text()
    core = re.search(r'^## 임상 핵심 처방 100선.*?\n(.*?)(?=^## )', text, re.M | re.S)[1]
    result = []
    category = ''
    for line in core.splitlines():
        if line.startswith('### '):
            category = re.sub(r' \d+선$', '', line[4:])
        m = re.search(r'\[([^]]+)\]\(([^)]+\.md)\)', line)
        if not m or not line.startswith('|'):
            continue
        path = (DOCS / 'herbal-integrated' / unquote(m[2])).resolve()
        cols = table_rows(line)[0]
        facts = [('구조 읽기', cols[1]), ('수치·법제 확인', cols[2])]
        body = path.read_text(encoding='utf-8-sig')
        # Preserve the source's preparation/version labels instead of guessing a universal composition.
        for heading, part in sections(body):
            if any(w in heading for w in ['처방 구조', '방제 구조', '삼보삼사', '네 가지 구성축', '네 약미의 역할', '여덟 약미', '수록 구성', '수록본의 구성', '배합과 복법']) or heading == '구성':
                rows = first_table(part)
                if rows:
                    facts.append(('원문 배합축', ' / '.join(' — '.join(row) for row in rows[1:5])))
                    break
        c = card('formula-' + path.stem.replace(' ', '-'), m[1], category, facts, path.relative_to(DOCS),
                 f'{m[1]}의 기본 구조와 가공·제형 확인점을 떠올려 보세요.')
        c['overviewSource'] = '/herbal-integrated/general-formulary/#core-formulas-100'
        result.append(c)
    assert len(result) == 100, len(result)
    comparison = 'herbal-integrated/formula-structure.md'
    text = (DOCS / comparison).read_text(encoding='utf-8-sig')
    body = next(b for h, b in sections(text) if h == '계열별 빠른 비교')
    for row in first_table(body)[1:]:
        result.append(card('formula-family-' + row[0], row[0] + ' 처방 계열 비교', '처방 계열 비교',
                           [('대표 처방', row[1]), ('분기 기준', row[2]), ('감별 질문', row[3])], comparison,
                           f'{row[0]} 계열의 대표 처방과 갈림점을 설명해 보세요.'))
    return result


def acupuncture_cards():
    result = []
    five_path = 'acupuncture-specific/five-shu.md'
    text = (DOCS / five_path).read_text()
    table = re.search(r'^\| 경맥 \| 정.*?(?=\n\n)', text, re.M | re.S)[0]
    for row in table_rows(table)[1:]:
        result.append(card('shu-' + re.search(r'[A-Z]{2}', row[0])[0], row[0] + ' 오수혈', '오수혈',
                           list(zip(['정(井)', '형(滎)', '수(兪)', '경(經)', '합(合)'], row[1:])), five_path))
        for classification, point in zip(['정(井)', '형(滎)', '수(兪)', '경(經)', '합(合)'], row[1:]):
            result.append(card('shu-point-' + point.split()[0], point + ' 오수혈 분류', '오수혈 개별 60혈',
                               [('소속 경맥', row[0]), ('오수혈 분류', classification)], five_path,
                               f'{point}의 소속 경맥과 정·형·수·경·합 분류는?'))
    special_path = 'acupuncture-specific/special-points-atlas.md'
    for heading, body in sections((DOCS / special_path).read_text()):
        rows = table_rows(body)
        if heading.startswith('12경맥'):
            for row in rows[1:]:
                result.append(card('yuan-' + re.search(r'[A-Z]{2}', row[0])[0], row[0] + ' 원·낙·극', '원혈·낙혈·극혈',
                                   list(zip(['원혈', '낙혈', '극혈'], row[1:])), special_path))
        elif heading == '배수혈·모혈':
            for row in rows[1:]:
                result.append(card('back-front-' + row[0], row[0] + ' 수모혈', heading,
                                   list(zip(['배수혈', '모혈'], row[1:])), special_path))
        elif heading == '팔맥교회혈':
            for row in rows[1:]:
                result.append(card('extra-' + row[0].split()[0], row[0], heading,
                                   [('연결 기경', row[1]), ('배합 짝', row[2])], special_path))
        elif heading in ('팔회혈', '육부 하합혈'):
            for i, item in enumerate(body.strip().split(' · ')):
                m = re.match(r'(\S+) ([A-Z]{2}\d+ .+)', clean(item))
                if m:
                    result.append(card(('meeting-' if heading == '팔회혈' else 'lower-') + m[1], m[1], heading,
                                       [('대표 혈', m[2])], special_path, f'{m[1]}에 연결되는 경혈은?'))
    pairing = 'acupuncture-specific/pairing-principles.md'
    text = (DOCS / pairing).read_text()
    for row in table_rows(text.split('## 대표 배혈법')[0])[1:]:
        result.append(card('class-' + row[0], row[0], '특정혈 개념', [('전통적 정의', row[1]), ('연결', row[2])], pairing))
    section = next(b for h, b in sections(text) if h == '대표 배혈법')
    for title, definition in re.findall(r'- \*\*([^*]+)\*\*[:：]\s*(.+)', section):
        result.append(card('pair-' + title, title, '배혈 원리', [('구성 원리', definition)], pairing))
    pairs = next(b for h, b in sections(text) if h == '팔맥교회혈 대표 짝')
    for row in first_table(pairs)[1:]:
        result.append(card('extra-pair-' + row[0].split()[0], row[0], '팔맥교회혈 짝 복습',
                           [('연결 기경', row[1])], pairing, f'{row[0]} 조합에 연결된 두 기경은?'))
    for code, name, area in re.findall(r'^- ([A-Z]{2}\d+) (\S+) — (.+)', text, re.M):
        result.append(card('four-' + code, f'{code} {name} 사총혈', '사총혈', [('대표 부위', area)], pairing))
    modalities = 'acupuncture-integrated/modalities.md'
    text = (DOCS / modalities).read_text()
    rows = table_rows(next(b for h, b in sections(text) if h == '치료수단 비교'))
    for row in rows[1:]:
        result.append(card('method-' + row[0], row[0], '치료수단', [('자극 방식', row[1]), ('확인할 점', row[3])], modalities))
    rows = table_rows(next(b for h, b in sections(text) if h == '전침을 선택할 때'))
    for row in rows[1:]:
        result.append(card('electro-' + row[0], '전침 ' + row[0], '전침 설계', [('확인 항목', row[1])], modalities))
    evidence = 'acupuncture-integrated/evidence.md'
    text = (DOCS / evidence).read_text()
    for heading, category, key in [('비교군에 따라 달라지는 질문', '비교군 읽기', '답하는 질문'),
                                   ('치료 프로토콜에서 추출할 항목', '연구 기록', '기록 항목')]:
        rows = first_table(next(b for h, b in sections(text) if h == heading))
        for row in rows[1:]:
            result.append(card('research-' + row[0], row[0], category, [(key, row[1])], evidence))
    section = next(b for h, b in sections(text) if h == '연구설계별 해석')
    for title, definition in re.findall(r'- \*\*([^:*]+):\*\*\s*(.+)', section):
        result.append(card('design-' + title, title, '연구설계', [('해석 범위', definition)], evidence))
    return result


def herb_comparison_cards():
    """Read each comparison's first table only; don't mix secondary examples."""
    path = 'herbal-integrated/herb-comparisons.md'
    text = (DOCS / path).read_text(encoding='utf-8-sig')
    result = []
    for heading, body in sections(text):
        rows = first_table(body)
        if not rows:
            continue
        title = re.sub(r'\s*\{#[^}]+\}', '', heading)
        if rows[0][0] == '구분':
            # Transposed 시호/향부자 table: preserve the two named columns.
            for column in (1, 2):
                name = rows[0][column]
                facts = [('비교 묶음', title)] + [(r[0], r[column]) for r in rows[1:]]
                result.append(card('herb-compare-' + name, name + ' 비교·감별', '본초 비교·감별', facts, path))
        else:
            name_column = 1 if rows[0][0] == '병증 방향' else 0
            for row in rows[1:]:
                name = row[name_column]
                facts = [('비교 묶음', title)] + [(rows[0][i], v) for i, v in enumerate(row) if i != name_column]
                result.append(card('herb-compare-' + title + '-' + name, name + ' 비교·감별', '본초 비교·감별',
                                   facts, path, f'{title} 중 {name}의 상대적 차이는?'))
    return result


def shuffled(items, seed):
    return sorted(items, key=lambda x: hashlib.sha256((seed + str(x)).encode()).hexdigest())


def make_question(c, label, pool, kind='fact', prompt=None):
    fact = next(f for f in c['facts'] if f['label'] == label)
    value = fact['value']
    # Deduplicate Hanja/typography variants; don't offer the same answer twice.
    seen = {normalized(value)}
    candidates = []
    for other in shuffled(pool, c['id'] + label):
        f = next((f for f in other['facts'] if f['label'] == label), None)
        if other['id'] == c['id'] or not f or normalized(f['value']) in seen:
            continue
        seen.add(normalized(f['value']))
        candidates.append({'text': f['value'], 'owner': other['title'], 'ownerId': other['id'], 'source': other['source']})
        if len(candidates) == 3:
            break
    if len(candidates) < 3:
        return None
    answer = {'text': value, 'owner': c['title'], 'ownerId': c['id'], 'source': c['source'], 'correct': True}
    options = shuffled([answer] + candidates, c['id'] + label + 'options')
    comparison = next((f['value'] for f in c['facts'] if f['label'] == '비교 묶음'), '')
    scope = f'「{comparison}」에서 ' if comparison else ''
    q = {'id': c['id'] + '-' + kind + '-' + label, 'cardId': c['id'], 'category': c['category'],
         'kind': kind, 'prompt': prompt or f"{scope}{c['title']}의 {label}으로 정리된 것은?",
         'options': options, 'answer': next(i for i, o in enumerate(options) if o.get('correct')),
         'explanation': f"{c['title']} — {label}: {value}", 'source': c['source']}
    for option in options:
        option.pop('correct', None)
    return q


def quizzes(subject, cards):
    questions = []
    for c in cards:
        if subject == 'acupoints':
            q = make_question(c, '혈명·경맥', cards, 'name', f"{c['code']}의 혈명과 소속 경맥은?")
            questions.append(q)
            others = [p for p in cards if p['category'] == c['category'] and p['id'] != c['id']]
            if len(others) < 3:
                others = [p for p in cards if p['id'] != c['id']]
            choices = shuffled([c] + shuffled(others, c['id'])[:3], c['id'] + 'point-options')
            options = [{'text': p['title'], 'owner': p['title'], 'ownerId': p['id'], 'source': p['source'],
                        'detail': next(f['value'] for f in p['facts'] if f['label'] == '표준 위치')} for p in choices]
            base = {'cardId': c['id'], 'category': c['category'], 'options': options,
                    'answer': choices.index(c), 'source': c['source'],
                    'explanation': c['title'] + '의 표준 위치: ' + c['facts'][1]['value']}
            location = c['facts'][1]['value']
            if not re.search(r'(?<![A-Z0-9])' + c['code'] + r'(?![0-9])', location) and c['name'] not in location:
                questions.append(dict(base, id=c['id'] + '-location', kind='location', prompt='다음 표준 위치에 해당하는 경혈은?', context=location))
            questions.append(dict(base, id=c['id'] + '-diagram', kind='diagram', prompt='도해의 붉은 점에 해당하는 경혈은?', diagram=c['quizDiagram']))
        else:
            labels = {'herbs': ['생약명', '전통 효능', '약용 부위', '기원·약용 부위', '성미', '귀경', '성미·귀경'],
                      'formulas': ['구조 읽기', '수치·법제 확인', '원문 배합축', '대표 처방', '분기 기준', '감별 질문']}.get(subject)
            if subject == 'herbs' and c['category'] == '본초 비교·감별':
                labels = [f['label'] for f in c['facts'] if f['label'] not in ('비교 묶음', '처방에서 보기', '배합에서 보기', '상세 문서')]
            if labels is None:
                labels = [f['label'] for f in c['facts'] if f['label'] != '연결']
            pool = [p for p in cards if p['category'] == c['category']] if subject == 'acupuncture' else cards
            for label in labels:
                if any(f['label'] == label for f in c['facts']):
                    q = make_question(c, label, pool)
                    if q:
                        questions.append(q)
                    # Reverse recall only when this complete source description is unique.
                    fact = next(f for f in c['facts'] if f['label'] == label)
                    same = [p for p in cards if any(f['label'] == label and normalized(f['value']) == normalized(fact['value']) for f in p['facts'])]
                    short_title = re.sub(r' 비교·감별| 오수혈 분류| 처방 계열 비교', '', c['title'])
                    if len(same) == 1 and len(cards) >= 4 and normalized(short_title) not in normalized(fact['value']) and label not in ('수치·법제 확인', '약용 부위', '성미', '귀경', '성미·귀경', '오수혈 분류', '소속 경맥'):
                        candidates = [p for p in cards if p['category'] == c['category']]
                        selected, seen = [c], {normalized(c['title'])}
                        for p in shuffled(candidates, c['id'] + label):
                            if normalized(p['title']) not in seen:
                                selected.append(p)
                                seen.add(normalized(p['title']))
                            if len(selected) == 4:
                                break
                        if len(selected) != 4:
                            continue
                        choices = shuffled(selected, c['id'] + label + 'recall')
                        questions.append({'id': c['id'] + '-recall-' + label, 'cardId': c['id'], 'category': c['category'],
                                          'kind': 'recall', 'prompt': '원문의 다음 설명과 연결된 학습 항목은?',
                                          'context': label + ': ' + fact['value'],
                                          'options': [{'text': p['title'], 'owner': p['title'], 'ownerId': p['id'], 'source': p['source']} for p in choices],
                                          'answer': choices.index(c), 'explanation': c['title'] + ' — ' + label + ': ' + fact['value'], 'source': c['source']})
    return questions


def blank_diagrams():
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ns = '{http://www.w3.org/2000/svg}'
    for source in sorted((DOCS / 'assets/acupoint-atlas').glob('*.svg')):
        tree = ET.fromstring(source.read_text())
        points = list(tree.iter(ns + 'a'))
        if not points:
            continue
        # Region headings and descriptions sometimes contain the answer too.
        for child in tree:
            if child.tag in (ns + 'title', ns + 'desc'):
                child.text = '경혈 위치 연습 — 붉은 점의 위치를 확인하세요.'
            elif child.tag == ns + 'text' and child.attrib.get('y') == '38':
                child.text = '경혈 위치 연습'
        for point in points:
            point.tag = ns + 'g'
            point.attrib.pop('href', None)
            point.attrib.pop('target', None)
            point.attrib.pop('aria-label', None)
            for child in list(point):
                if child.tag != ns + 'circle':
                    point.remove(child)
        write_bytes(OUT / 'diagrams' / source.name, ET.tostring(tree, encoding='utf-8', xml_declaration=True))


def validate(decks):
    all_ids = set()
    for subject, deck in decks.items():
        cards = {c['id']: c for c in deck['cards']}
        if len(cards) != len(deck['cards']):
            raise ValueError('Duplicate card IDs')
        for record in deck['cards'] + deck['questions']:
            if record['id'] in all_ids:
                raise ValueError('Duplicate ID ' + record['id'])
            all_ids.add(record['id'])
            if not record['source'].startswith('/'):
                raise ValueError('Non-local source')
        for q in deck['questions']:
            assert q['cardId'] in cards and 0 <= q['answer'] < 4 and len(q['options']) == 4
            assert len({normalized(o['text']) for o in q['options']}) == 4, q['id']
            for option in q['options']:
                owner = cards[option['ownerId']]
                assert option['source'] == owner['source'], q['id']
                assert option['text'] == owner['title'] or option['text'] in [f['value'] for f in owner['facts']], q['id']
        for c in deck['cards']:
            assert c['facts'] and all(f['value'] for f in c['facts']), c['id']


def build():
    builders = {'acupoints': acupoints, 'acupuncture': acupuncture_cards, 'herbs': herb_cards, 'formulas': formula_cards}
    decks = {}
    for subject, builder in builders.items():
        cards = builder()
        if subject == 'herbs':
            cards.extend(herb_comparison_cards())
        decks[subject] = {'schema': 1, 'subject': subject, 'title': SUBJECTS[subject], 'cards': cards, 'questions': quizzes(subject, cards)}
    validate(decks)
    return decks


def main():
    decks = build()
    for subject, deck in decks.items():
        write_bytes(OUT / (subject + '.json'), (json.dumps(deck, ensure_ascii=False, indent=2) + '\n').encode())
    manifest = {'schema': 1, 'version': '20261002-3', 'subjects': [
        {'id': s, 'title': SUBJECTS[s], 'cards': len(d['cards']), 'questions': len(d['questions']), 'file': s + '.json'}
        for s, d in decks.items()]}
    write_bytes(OUT / 'manifest.json', (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
    blank_diagrams()
    for subject, deck in decks.items():
        path = DOCS / 'learning' / (subject + '.md')
        if not path.exists():
            continue
        # Only the directory block is generated. The study plan stays editorial.
        text = path.read_text().split('<!-- STUDY_DIRECTORY_START -->')[0].rstrip()
        lines = ['\n\n<!-- STUDY_DIRECTORY_START -->', '## 전체 학습 요약과 원문 {#study-directory}',
                 f"{len(deck['cards'])}개 카드의 핵심 내용을 단원별로 확인하세요. 아래 요약은 JavaScript 없이도 읽을 수 있습니다.", '']
        groups = defaultdict(list)
        for c in deck['cards']:
            groups[c['category']].append(c)
        for category, cards in groups.items():
            lines.extend(['<details markdown="1">', f'<summary>{category} · {len(cards)}개 카드</summary>', ''])
            for c in cards:
                lines.extend([f"**{c['title']}**", ''])
                for fact in c['facts']:
                    lines.append(f"- **{fact['label']}:** {fact['value']}")
                lines.extend(['', f"[원문에서 확인]({c['source']})", ''])
            lines.extend(['</details>', ''])
        lines.append('<!-- STUDY_DIRECTORY_END -->\n')
        write_bytes(path, (text + '\n'.join(lines)).encode())
    # Public counts are generated from the same decks as the interactive tool.
    for subject, deck in decks.items():
        path = DOCS / 'learning' / (subject + '.md')
        if path.exists():
            text = path.read_text()
            text = re.sub(r'\*\*\d+개 카드 · [\d,]+문제\.', f"**{len(deck['cards'])}개 카드 · {len(deck['questions']):,}문제.", text)
            write_bytes(path, text.encode())
    hub = DOCS / 'learning/index.md'
    if hub.exists():
        text = hub.read_text()
        text = re.sub(r'학습카드 [\d,]+개 · 해설형 문제 [\d,]+개',
                      f"학습카드 {sum(len(d['cards']) for d in decks.values()):,}개 · 해설형 문제 {sum(len(d['questions']) for d in decks.values()):,}개", text)
        for subject, deck in decks.items():
            text = re.sub(r'(\| \[' + SUBJECTS[subject] + r'\]\(' + subject + r'\.md\) \| )\d+( \| )[\d,]+',
                          lambda m: m[1] + str(len(deck['cards'])) + m[2] + f"{len(deck['questions']):,}", text)
            text = re.sub(r'(href="/learning/' + subject + r'/".*?<small>)\d+개 카드',
                          lambda m: m[1] + str(len(deck['cards'])) + '개 카드', text)
        write_bytes(hub, text.encode())
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == '__main__':
    main()
