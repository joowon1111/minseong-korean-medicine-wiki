"""Authored case/comparison questions, distinct from generated fact recall."""
import json
from collections import Counter
from copy import deepcopy
from urllib.parse import urlsplit

# Legacy storage keys and question IDs preserve existing browser progress.
LEVELS = {'high': '중', 'expert': '상'}
START = '<!-- ADVANCED_QUESTIONS_START -->'
END = '<!-- ADVANCED_QUESTIONS_END -->'


def advanced_questions(root, decks, named_points=lambda text: text):
    payload = json.loads((root / 'data/advanced_learning.json').read_text())
    assert payload['schema'] == 1
    rows = payload['questions']
    per_level = payload['questionsPerLevel']
    assert isinstance(per_level, int) and per_level >= 10
    assert Counter((r['subject'], r['difficulty']) for r in rows) == Counter(
        {(s, level): per_level for s in decks for level in LEVELS})
    assert len({r['id'] for r in rows}) == len(rows)
    result = {s: [] for s in decks}
    for row in rows:
        row = deepcopy(row)
        if row['subject'] in ('acupoints', 'acupuncture'):
            for key in ('prompt', 'context', 'explanation', 'discriminator'):
                row[key] = named_points(row[key])
            for option in row['options']:
                for key in ('text', 'detail'):
                    option[key] = named_points(option[key])
        subject = row['subject']
        card = next(c for c in decks[subject]['cards'] if c['id'] == row['cardId'])
        assert row['id'].startswith('advanced-' + subject + '-' + row['difficulty'] + '-')
        assert row['context'] and row['prompt'] and card['title'] in row['explanation']
        assert len(row['options']) == 4 and isinstance(row['answer'], int) and 0 <= row['answer'] < 4
        assert len({o['text'] for o in row['options']}) == 4
        assert len({o['detail'] for o in row['options']}) == 4
        assert all(o['text'].strip() and o['detail'].strip() for o in row['options'])
        assert row['discriminator'].strip()
        assert isinstance(row['nearestWrong'], int) and 0 <= row['nearestWrong'] < 4
        assert row['nearestWrong'] != row['answer']
        q = deepcopy(row)
        q.pop('subject')
        q.update(kind='advanced', category=card['category'], source=f'/learning/{subject}/#{q["id"]}',
                 relatedSource=card['source'])
        for i, option in enumerate(q['options']):
            option.update(owner='정답 근거' if i == q['answer'] else '오답 감별', ownerId=card['id'], source=q['source'])
        result[subject].append(q)
    return result


def static_questions(questions):
    counts = Counter(q['difficulty'] for q in questions)
    lines = [START, '## 중·상 문제와 보기별 해설 {#advanced-questions}', '',
             f'각 난이도 {counts["high"]}문제씩입니다. **중**은 여러 단서와 가까운 개념을 함께 구별하고, **상**은 '
             '예외·조건 변화·복수 분류 또는 출전의 차이를 판단합니다. 난이도는 출제 의도에 따른 구분이며 '
             '실제 정답률로 보정한 등급은 아닙니다. 퀴즈의 **문제 난이도**에서 선택하거나 아래 문항을 읽어 보세요. '
             '증례·수치는 교육용 가정이고, 제시된 체질·병론 안에서 문헌을 읽는 문제는 체질 판정 검사가 아닙니다.', '']
    for level, label in LEVELS.items():
        lines += [f'### {label} · 통합·감별 {counts[level]}문제', '']
        for number, q in enumerate((q for q in questions if q['difficulty'] == level), 1):
            lines += [f'<span id="{q["id"]}"></span>', '', f'**{label} {number}. {q["prompt"]}**', '', q['context'], '']
            lines += [f'{i + 1}. {o["text"]}' for i, o in enumerate(q['options'])]
            lines += ['', '<details markdown="1">', '<summary>정답·보기별 해설 펼치기</summary>', '',
                      f'**정답: {q["answer"] + 1}번** — {q["explanation"]}', '']
            lines += [f'**결정적 감별 단서:** {q["discriminator"]}', '',
                      f'**가장 가까운 오답:** {q["nearestWrong"] + 1}번 — {q["options"][q["nearestWrong"]]["detail"]}', '']
            lines += [f'- **{i + 1}번 ({"정답" if i == q["answer"] else "오답"}):** {o["detail"]}' for i, o in enumerate(q['options'])]
            lines += ['', f'[연결 학습 원문]({q["relatedSource"]})', '', '</details>', '']
    lines += [END, '']
    return '\n'.join(lines)


def validate_advanced(q):
    assert q['difficulty'] in LEVELS
    assert q['context'] and q['relatedSource'].startswith('/')
    assert urlsplit(q['source']).fragment == q['id']
    assert q['source'].startswith('/learning/')
    assert q['discriminator'].strip() and q['nearestWrong'] in range(4) and q['nearestWrong'] != q['answer']
    assert all(o['ownerId'] == q['cardId'] and o['source'] == q['source'] and o['detail'].strip() for o in q['options'])
