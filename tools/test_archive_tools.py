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

    def test_extended_formulas_keep_subsections_separate_and_link_to_their_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            docs=Path(temp)
            (docs/'sasang-formula-library').mkdir()
            (docs/'sasang-formula-cards').mkdir()
            body='# 소음인 처방\n\n## 첫탕(一湯) {#first}\n\n### 깊이 읽기\n\n| 항목 | 값 |\n|---|---|\n| 핵심 증후 | 첫 처방의 냉감 |\n| 구성·법제 | 계지 7.5 g |\n| 감별 처방 | [둘탕](#second) |\n| 근거와 한계 | 출전 첫 기록 |\n\n## 둘탕(二湯) {#second}\n\n**병증 위치:** 둘 처방의 병증\n\n**구성·출전:** 생지황 15 g\n\n출전: 둘 기록\n'
            path=docs/'sasang-formula-library/soeumin-extended-formulas.md';path.write_text(body)
            with patch.object(builder,'DOCS',docs):
                source=builder.url_for(path)
                by_url={source:(body,list(builder.sections(body)))}
                cards=[]
                builder.expand_catalog(cards,by_url)
            self.assertEqual(len(cards),2)
            first,second=cards
            self.assertEqual(first['source'],source+'#first')
            self.assertEqual(second['system'],'소음인')
            self.assertIn(source+'#second',first['links'])
            first_text=' '.join(f['value'] for f in first['facts'])
            second_text=' '.join(f['value'] for f in second['facts'])
            self.assertIn('계지 7.5 g',first_text)
            self.assertNotIn('생지황 15 g',first_text)
            self.assertIn('생지황 15 g',second_text)
            self.assertNotIn('계지 7.5 g',second_text)
            self.assertTrue(all(section['url'].startswith(source+'#') for section in first['sections']))

    def test_complete_catalog_resolves_every_group_and_all_formula_sections(self):
        compare,_=builder.build()
        cards=[c for c in compare['cards'] if c['kind']=='formula']
        sources={c['source'] for c in cards}
        ids={c['id'] for c in cards}
        self.assertEqual(len(ids),len(cards))
        for g in compare['groups']:
            self.assertTrue(2 <= len(g['ids']) <= 4)
            self.assertTrue(set(g['ids']) <= ids)
        for path in (builder.DOCS/'sasang-formula-library').glob('*-extended-formulas.md'):
            import re
            text=path.read_text()
            for name,anchor in re.findall(r'^## (.+?) \{#([^}]+)\}',text,re.M):
                if re.match(r'[^\s(]+(?:탕|산|환|음|단)\(',name):
                    self.assertIn(builder.url_for(path)+'#'+anchor,sources)
        self.assertIn('/sasang-formula-cards/dokhwaljihwang-tang/',sources)
        self.assertIn('/classics/shanghanlun/clauses/jueyin/#clause-338',sources)
        self.assertIn('/formula-architecture/shanghan-family/#waidai-fuling-yin',sources)
        self.assertIn('/formulas/liu%20wei%20dihuang%20wan/',sources)
        self.assertIn(compare['idAliases']['document-formulas-liu wei dihuang wan'],ids)
        self.assertFalse(any(c['category']=='처방 계열 비교' for c in cards))

    def test_annotated_primary_recipe_does_not_take_an_appended_formulas_dose(self):
        with tempfile.TemporaryDirectory() as temp:
            docs=Path(temp);folder=docs/'classics/jinkui-yaolue/chapters';folder.mkdir(parents=True)
            (folder/'test.md').write_text('# 금궤요략\n\n## 계지가용골모려탕 {#one}\n\n> 桂枝加龍骨牡蠣湯主之。\n\n    桂枝加龍骨牡蠣湯方：（판본의 부기）\n\n    桂枝（三兩） 龍骨（三兩） 牡蠣（三兩）\n\n    右三味，煎服。\n\n    天雄散方：\n\n    天雄（三兩） 白朮（八兩）\n',encoding='utf-8')
            cards=[]
            with patch.object(builder,'DOCS',docs):builder.add_classical_recipes(cards)
            self.assertEqual(len(cards),1)
            self.assertIn('桂枝加龍骨牡蠣湯',cards[0]['title'])
            dose=next(f['value'] for f in cards[0]['facts'] if f['label']=='구성·약량')
            self.assertIn('龍骨（三兩）',dose)
            self.assertNotIn('天雄',dose)

    def test_plain_removes_markup_not_passage_text(self):
        self.assertEqual(builder.plain('**인삼** · [백출](a.md) <span>복령</span>'), '인삼 · 백출 복령')
        self.assertEqual(builder.parse('\ufeff---\ntitle: 제목\n---\n# 본문')[0]['title'], '제목')

if __name__ == '__main__':
    unittest.main()
