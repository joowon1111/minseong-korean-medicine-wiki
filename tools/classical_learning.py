"""Editorial classical banks: sourced readings, close peers and authored cases."""
import json

LABELS = [('original', '우리말 풀이'), ('interpretation', '판독 핵심'), ('treatment', '치법·처방')]


def classical_deck(root, subject, shuffled):
    filename = 'shanghan_learning.json' if subject == 'shanghanlun' else 'sasang_learning.json'
    rows = json.loads((root / 'data' / filename).read_text())['items']
    cards = []
    for row in rows:
        source = f'/learning/{subject}/#{row["id"]}'
        facts = [('원문 구분', row['originalLabel']),
                 ('분류 표지어' if row.get('sourceKind') == 'cpg' else '원문', row['original']),
                 ('판본·범위', row['edition']), ('우리말 풀이', row['translation']),
                 ('판독 핵심', row['pattern']), ('치법·처방', row['treatment']), ('감별·해석', row['note'])]
        if row.get('quizCase'):
            facts.append(('증례 독해', row['quizCase']))
        cards.append({'id': row['id'], 'title': row['title'], 'category': row['category'],
                      'prompt': row['original'] + '\n우리말 뜻과 병증·치법의 연결을 설명해 보세요.',
                      'facts': [{'label': k, 'value': v} for k, v in facts], 'source': source,
                      'sourceTitle': row['title'] + ' 원문·학습 해설',
                      'relatedSource': row['relatedSource'], 'reference': row['reference'],
                      'referenceLabel': row.get('referenceLabel', '원전 판본')})
    by_id = {c['id']: c for c in cards}
    questions = []
    for row in rows:
        c = by_id[row['id']]
        # Editorial close comparisons outrank category and data order.
        peers = row.get('compareWith', [])
        assert len(peers) == len(set(peers)) and c['id'] not in peers, c['id']
        assert all(identifier in by_id for identifier in peers), c['id']
        pool = [p for p in cards if p['id'] != c['id']]
        pool.sort(key=lambda p: (peers.index(p['id']) if p['id'] in peers else len(peers),
                                 p['category'] != c['category'], cards.index(p)))
        labels = LABELS + ([('case', None)] if row.get('quizCase') else [])
        def answer_value(card, label):
            return card['title'] if label is None else next(f['value'] for f in card['facts'] if f['label'] == label)
        for kind, label in labels:
            value = answer_value(c, label)
            selected, seen = [c], {value}
            for p in pool:
                # A second clause for the same formula is useful in reading/case
                # comparisons but can also be true as a method-only answer.
                if kind == 'treatment' and p['id'] in row.get('treatmentAvoid', []):
                    continue
                v = answer_value(p, label)
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
                options.append({'text': answer_value(p, label), 'owner': p['title'], 'ownerId': p['id'],
                                'source': p['source'], 'detail': detail})
            prompts = {'original': '다음 원문·분류 표지어의 우리말 풀이로 맞는 것은?',
                       'interpretation': '다음 독해 사례의 판독 핵심으로 맞는 것은?',
                       'treatment': '다음 제시문과 병증 문맥에 연결되는 치법·처방 설명은?',
                       'case': '다음 병증·배합 독해 사례에 가장 직접 대응하는 학습 항목은?'}
            actual_kind = 'formula' if kind == 'treatment' and row['id'].startswith('sasang-formula-') else kind
            context = row['case'] if kind == 'interpretation' else row['original']
            if kind == 'treatment':
                context += '\n' + row['case']
            if kind == 'case':
                context = row['quizCase']
            questions.append({'id': c['id'] + '-' + kind, 'cardId': c['id'], 'category': c['category'],
                              'kind': actual_kind, 'prompt': prompts[kind], 'context': context,
                              'options': options, 'answer': choices.index(c),
                              'explanation': c['title'] + ' — ' + row['translation'] + ' ' + row['pattern'] + ' ' + row['treatment'] + ' ' + row['note'],
                              'source': c['source']})
    return {'schema': 1, 'subject': subject, 'title': '상한론' if subject == 'shanghanlun' else '사상의학',
            'cards': cards, 'questions': questions}
