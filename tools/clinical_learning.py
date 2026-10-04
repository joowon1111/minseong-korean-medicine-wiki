"""Independent five-option reasoning items with optional structured observations."""
from collections import Counter
from copy import deepcopy
import json

START = '<!-- CLINICAL_QUESTIONS_START -->'
END = '<!-- CLINICAL_QUESTIONS_END -->'
LEVELS = {'high': '중', 'expert': '상'}


def clinical_questions(root, decks):
    payload = json.loads((root / 'data/clinical_learning.json').read_text())
    assert payload['schema'] == 1
    rows = payload['questions']
    assert Counter((r['subject'], r['difficulty']) for r in rows) == Counter(
        {(s, level): 4 for s in decks for level in LEVELS})
    assert len({r['id'] for r in rows}) == len(rows)
    result = {s: [] for s in decks}
    for row in rows:
        q = deepcopy(row)
        subject = q.pop('subject')
        c = next(c for c in decks[subject]['cards'] if c['id'] == q['cardId'])
        q.update(kind='clinical', category=c['category'],
                 source=f'/learning/{subject}/#{q["id"]}', relatedSource=c['source'])
        for i, option in enumerate(q['options']):
            option.update(owner='정답 근거' if i == q['answer'] else '오답 감별',
                          ownerId=c['id'], source=q['source'])
        validate_clinical(q)
        result[subject].append(q)
    return result


def validate_clinical(q):
    assert q['difficulty'] in LEVELS and q['context'] and q['prompt']
    assert len(q['options']) == 5 and type(q['answer']) is int and q['answer'] in range(5)
    assert len({o['text'] for o in q['options']}) == 5
    assert all(o['text'].strip() and o['detail'].strip() for o in q['options'])
    assert q['discriminator'] and q['nearestWrong'] in range(5) and q['nearestWrong'] != q['answer']
    assert q['source'].endswith('#' + q['id']) and q['relatedSource'].startswith('/')
    if 'table' in q:
        t = q['table']
        assert t['caption'] and len(t['headers']) >= 2 and t['rows']
        assert all(len(row) == len(t['headers']) for row in t['rows'])


def static_questions(questions):
    lines = [START, '## 증례·배혈·본초 추론 5지선다 {#clinical-questions}', '',
             '증례의 경과·보존된 기능·설맥·배합 목적을 종합해 **가장 적절한 답 하나**를 고릅니다. '
             '수치와 증례는 자체 작성한 교육용 가정이며, 전통 변증과 현대 검사 해석은 각각의 근거로 구분합니다. '
             '실제 환자의 확정 진단이나 개인별 처방을 대신하지 않습니다. 퀴즈의 **문제 유형 → 증례·배혈·본초 추론 (5지선다)**에서 같은 문항을 풀 수 있습니다.', '']
    for n, q in enumerate(questions, 1):
        lines += [f'<span id="{q["id"]}"></span>', '',
                  f'### {n}. {LEVELS[q["difficulty"]]} · {q["prompt"]}', '', q['context'], '']
        if 'table' in q:
            t = q['table']
            lines += [t['caption'], '', '| ' + ' | '.join(t['headers']) + ' |',
                      '| ' + ' | '.join('---' for _ in t['headers']) + ' |']
            lines += ['| ' + ' | '.join(row) + ' |' for row in t['rows']]
            lines += ['']
        lines += [f'{i + 1}. {o["text"]}' for i, o in enumerate(q['options'])]
        lines += ['', '<details markdown="1">', '<summary>정답·감별 해설 펼치기</summary>', '',
                  f'**정답: {q["answer"] + 1}번** — {q["explanation"]}', '',
                  f'**결정적 감별 단서:** {q["discriminator"]}', '',
                  f'**가장 가까운 오답:** {q["nearestWrong"] + 1}번 — {q["options"][q["nearestWrong"]]["detail"]}', '']
        lines += [f'- **{i + 1}번:** {o["detail"]}' for i, o in enumerate(q['options'])]
        lines += ['', f'[연결 학습 원문]({q["relatedSource"]})']
        lines += [f' · [{r["title"]}]({r["url"]})' for r in q.get('references', [])]
        lines += ['', '</details>', '']
    return '\n'.join(lines + [END, ''])
