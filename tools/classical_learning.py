"""Editorial classical banks: three reading directions, stable IDs and sources."""
import json

LABELS = [('original', '우리말 풀이'), ('interpretation', '판독 핵심'), ('treatment', '치법·처방')]


def classical_deck(root, subject, shuffled):
    filename = 'shanghan_learning.json' if subject == 'shanghanlun' else 'sasang_learning.json'
    rows = json.loads((root / 'data' / filename).read_text())['items']
    cards = []
    for row in rows:
        source = f'/learning/{subject}/#{row["id"]}'
        facts = [('원문 구분', row['originalLabel']), ('원문', row['original']),
                 ('판본·범위', row['edition']), ('우리말 풀이', row['translation']),
                 ('판독 핵심', row['pattern']), ('치법·처방', row['treatment']), ('감별·해석', row['note'])]
        cards.append({'id': row['id'], 'title': row['title'], 'category': row['category'],
                      'prompt': row['original'] + '\n우리말 뜻과 병증·치법의 연결을 설명해 보세요.',
                      'facts': [{'label': k, 'value': v} for k, v in facts], 'source': source,
                      'sourceTitle': row['title'] + ' 원문·학습 해설',
                      'relatedSource': row['relatedSource'], 'reference': row['reference']})
    by_id = {c['id']: c for c in cards}
    questions = []
    for row in rows:
        c = by_id[row['id']]
        # Prefer the same family; widen only for small chapter groups.
        pool = [p for p in cards if p['id'] != c['id']]
        pool.sort(key=lambda p: (p['category'] != c['category'], cards.index(p)))
        for kind, label in LABELS:
            value = next(f['value'] for f in c['facts'] if f['label'] == label)
            selected, seen = [c], {value}
            for p in pool:
                v = next(f['value'] for f in p['facts'] if f['label'] == label)
                if v not in seen:
                    selected.append(p)
                    seen.add(v)
                if len(selected) == 4:
                    break
            assert len(selected) == 4, c['id']
            choices = shuffled(selected, c['id'] + kind)
            options = []
            for p in choices:
                def fact(key):
                    return next(f['value'] for f in p['facts'] if f['label'] == key)
                detail = fact('판독 핵심') + ' ' + fact('치법·처방') + ' ' + fact('감별·해석')
                options.append({'text': fact(label), 'owner': p['title'], 'ownerId': p['id'],
                                'source': p['source'], 'detail': detail})
            prompts = {'original': '다음 원문 구절·표지어의 우리말 풀이로 맞는 것은?',
                       'interpretation': '다음 독해 사례의 판독 핵심으로 맞는 것은?',
                       'treatment': '다음 원문과 병증 문맥에 연결되는 치법·처방 설명은?'}
            actual_kind = 'formula' if kind == 'treatment' and row['id'].startswith('sasang-formula-') else kind
            context = row['case'] if kind == 'interpretation' else row['original']
            if kind == 'treatment':
                context += '\n' + row['case']
            questions.append({'id': c['id'] + '-' + kind, 'cardId': c['id'], 'category': c['category'],
                              'kind': actual_kind, 'prompt': prompts[kind], 'context': context,
                              'options': options, 'answer': choices.index(c),
                              'explanation': c['title'] + ' — ' + row['translation'] + ' ' + row['pattern'] + ' ' + row['treatment'] + ' ' + row['note'],
                              'source': c['source']})
    return {'schema': 1, 'subject': subject, 'title': '상한론' if subject == 'shanghanlun' else '사상의학',
            'cards': cards, 'questions': questions}
