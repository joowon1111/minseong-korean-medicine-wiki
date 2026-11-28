"""Core-list progress cannot be inflated by variants, aliases or navigation."""
from copy import deepcopy
from html import unescape
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from ontology import build_ontology, RESOURCE
from formula_coverage import core_entries, formula_coverage, coverage_markdown, FORMULARY, MARKER
import ontology_views as views

class FormulaCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=Path('docs')
        cls.payload,_=build_ontology(cls.docs,Path('data/ontology.json'))

    def test_real_core_list_is_distinct_from_all_registered_documents(self):
        report=formula_coverage(self.payload,self.docs)
        self.assertEqual(report['summary'],dict(core_total=100,core_registered=51,core_pending=49,
            all_registered_documents=56,other_registered_documents=5,registered_variants=64))
        outside={v['label'] for e in report['other_registered'] for v in e['variants']}
        self.assertIn('인삼양위탕 — 국방 수록형',outside)
        self.assertIn('향사평위산 — 동의보감 회춘 인용 수록형',outside)
        self.assertEqual(len(report['core']),100)
        for e in report['core']:
            self.assertEqual(e['has_composition_records'],bool(e['variants']))
        self.assertEqual(report,formula_coverage(self.payload,self.docs))

    def test_an_extra_variant_does_not_inflate_document_progress(self):
        p=deepcopy(self.payload)
        node=deepcopy(next(n for n in p['@graph'] if n['@id']==RESOURCE+'#siwu-guofang'))
        node['@id']+='-test-variant';node['skos:prefLabel']['@value']+=' 검증 이본'
        statement=deepcopy(next(n for n in p['@graph'] if n.get('rdf:subject',{}).get('@id')==RESOURCE+'#siwu-guofang' and n.get('rdf:predicate',{}).get('@id')=='km:containsHerb'))
        statement['@id']+='-test-variant';statement['rdf:subject']['@id']=node['@id']
        p['@graph'] += [node,statement]
        result=formula_coverage(p,self.docs)
        self.assertEqual(result['summary']['core_registered'],51)
        self.assertEqual(result['summary']['all_registered_documents'],56)
        self.assertEqual(result['summary']['registered_variants'],65)
        entry=next(e for e in result['core'] if e['label']=='사물탕')
        self.assertTrue(any(v['id']==node['@id'] for v in entry['variants']))

    def test_navigation_and_matching_alias_cannot_turn_a_pending_formula_into_registered(self):
        p=deepcopy(self.payload)
        node=deepcopy(next(n for n in p['@graph'] if n['@id']==RESOURCE+'#siwu-guofang'))
        node['@id']+='-alias-only';node['skos:altLabel']=['향사양위탕']
        node['foaf:page']['@id']='https://wiki.minseong.co.kr/formulas/xiangsha-yangwei-tang/#source-dose-original'
        statement=deepcopy(next(n for n in p['@graph'] if n.get('rdf:predicate',{}).get('@id')=='km:containsHerb'))
        statement['@id']+='-navigation';statement['rdf:subject']['@id']=node['@id'];statement['rdf:predicate']['@id']='km:links_to_herb'
        p['@graph'] += [node,statement]
        result=formula_coverage(p,self.docs)
        self.assertEqual(result['summary']['core_registered'],51)
        self.assertFalse(next(e for e in result['core'] if e['label']=='향사양위탕')['has_composition_records'])

    def test_missing_memberships_update_pending_list_and_preserve_variant_sources(self):
        p=deepcopy(self.payload)
        p['@graph']=[n for n in p['@graph'] if not(n.get('rdf:subject',{}).get('@id')==RESOURCE+'#siwu-guofang' and n.get('rdf:predicate',{}).get('@id')=='km:containsHerb')]
        result=formula_coverage(p,self.docs)
        self.assertEqual(result['summary']['core_registered'],50)
        self.assertEqual(result['summary']['core_pending'],50)
        self.assertFalse(next(e for e in result['core'] if e['label']=='사물탕')['has_composition_records'])
        current=formula_coverage(self.payload,self.docs)
        for e in current['core']:
            for v in e['variants']:
                self.assertGreater(v['herb_count'],0)
                self.assertTrue(all('#' in s for s in v['sources']))

    def test_duplicate_core_rows_fail_instead_of_silently_changing_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs=Path(tmp);(docs/'herbal-integrated').mkdir();(docs/'formulas').mkdir()
            (docs/'formulas/a.md').write_text('# 처방')
            (docs/FORMULARY).write_text('## 핵심 {#core-formulas-100}\n### 처방군\n'+('| [처방](../formulas/a.md) |\n'*100))
            with self.assertRaisesRegex(ValueError,'100 distinct'):core_entries(docs)

    def test_visible_formulary_shows_each_status_and_source_variant(self):
        report=formula_coverage(self.payload,self.docs)
        rendered=unescape(coverage_markdown(report))
        self.assertIn('51/100개',rendered.replace('**',''))
        self.assertIn('대기 처방 보기',rendered)
        self.assertIn('https://wiki.minseong.co.kr/formulas/xiangsha-yangwei-tang/',rendered)
        for e in report['core']:
            for v in e['variants']:self.assertIn(v['url'],rendered)
        markdown=(self.docs/FORMULARY).read_text()
        page=SimpleNamespace(file=SimpleNamespace(src_uri=FORMULARY))
        built=views.on_page_markdown(markdown,page=page,config={'docs_dir':str(self.docs)},files=[])
        self.assertNotIn(MARKER,built)
        self.assertIn(coverage_markdown(report),built)
        with self.assertRaises(ValueError):views.on_page_markdown(markdown+MARKER,page=page,config={'docs_dir':str(self.docs)},files=[])

if __name__=='__main__':unittest.main()
