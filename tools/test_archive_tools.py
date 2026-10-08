import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_archive_tools as builder

class ArchiveToolsTests(unittest.TestCase):
    def test_extracts_real_passage_and_explicit_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp)
            (docs / 'formulas').mkdir()
            (docs / 'herbs').mkdir()
            (docs / 'assets/learning').mkdir(parents=True)
            (docs / 'formulas/test.md').write_text('---\ntitle: 시험탕\n---\n# 시험탕\n\n## 구성·용량 {#dose}\n\n[인삼](../herbs/ginseng.md)과 백출을 구성으로 명시한 원문 발췌가 들어갑니다.\n', encoding='utf-8')
            (docs / 'herbs/ginseng.md').write_text('# 인삼\n\n## 효능\n\n기원과 부위를 구분하는 본초의 전통 효능 설명입니다. 본문을 직접 확인합니다.', encoding='utf-8')
            for name in ['formulas', 'herbs']:
                card = {'id': name + '-test', 'title': '시험', 'category': '시험', 'facts': [], 'source': '/formulas/test/' if name == 'formulas' else '/herbs/ginseng/'}
                (docs / f'assets/learning/{name}.json').write_text(json.dumps({'cards': [card]}))
            with patch.object(builder, 'DOCS', docs):
                compare, search = builder.build()
                self.assertEqual(builder.url_for(docs / 'formulas/test.md'), '/formulas/test/')
                self.assertEqual(builder.url_for(docs / 'nested/index.md'), '/nested/')
            self.assertEqual(compare['cards'][0]['links'], ['/herbs/ginseng/'])
            self.assertEqual(compare['cards'][0]['sections'][0]['url'], '/formulas/test/#dose')
            passage = next(p for p in search['passages'] if p['heading'] == '구성·용량')
            self.assertIn('인삼과 백출', passage['text'])
            self.assertEqual(passage['kind'], 'formula')
            self.assertNotIn('추정', passage['text'])

    def test_plain_removes_markup_not_passage_text(self):
        self.assertEqual(builder.plain('**인삼** · [백출](a.md) <span>복령</span>'), '인삼 · 백출 복령')
        self.assertEqual(builder.parse('\ufeff---\ntitle: 제목\n---\n# 본문')[0]['title'], '제목')

if __name__ == '__main__':
    unittest.main()
