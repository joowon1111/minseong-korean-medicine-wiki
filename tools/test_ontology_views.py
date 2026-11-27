"""Composition browsing preserves qualified identities and current source data."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ontology import build_ontology
import ontology_views as views


class OntologyViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload, _ = build_ontology(Path('docs'), Path('data/ontology.json'))

    def tearDown(self):
        views.render_for_docs.cache_clear()

    def test_formula_variants_and_parts_remain_distinct(self):
        rendered = views.composition_tables(self.payload)
        lines = rendered.splitlines()
        jinkui = next(line for line in lines if line.startswith('| <a')
                      and '산조인탕 — 금궤요략 수록형</a> |' in line)
        donguibogam = next(line for line in lines if line.startswith('| <a')
                          and '산조인탕 — 동의보감 몽문 수록형</a> |' in line)
        self.assertIn('천궁</a>', jinkui)
        self.assertNotIn('인삼</a>', jinkui)
        self.assertIn('인삼</a>', donguibogam)
        self.assertIn('적복령</a>', donguibogam)
        self.assertIn('계심</a>', donguibogam)
        self.assertIn('#donguibogam-version', donguibogam)
        self.assertIn('#source-dose-original', jinkui)
        inverse = rendered.split('### 공통 본초에서 처방 찾아가기', 1)[1]
        self.assertIn('인삼</a>', inverse)
        # A one-formula part must not be silently equated with generic poria.
        self.assertNotIn('적복령</a>', inverse)
        self.assertNotIn('계심</a>', inverse)

    def test_navigation_links_never_create_composition_membership(self):
        payload = deepcopy(self.payload)
        statement = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                         and n['rdf:predicate']['@id'] == 'km:containsHerb')
        navigation = deepcopy(statement)
        navigation['@id'] += '-navigation'
        navigation['rdf:predicate']['@id'] = 'km:links_to_herb'
        navigation['rdf:object']['@id'] = next(n['@id'] for n in payload['@graph']
                                              if n['@id'].endswith('#gypsum'))
        payload['@graph'].append(navigation)
        self.assertEqual(views.composition_tables(payload), views.composition_tables(self.payload))

    def test_repeated_qualified_records_do_not_repeat_membership(self):
        payload = deepcopy(self.payload)
        statement = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                         and n['rdf:predicate']['@id'] == 'km:containsHerb')
        duplicate = deepcopy(statement)
        duplicate['@id'] += '-additional-qualification'
        payload['@graph'].append(duplicate)
        self.assertEqual(views.composition_tables(payload), views.composition_tables(self.payload))

    def test_literal_labels_cannot_inject_html_or_table_columns(self):
        rendered = views.link('<img src=x onerror=alert(1)>|[name](javascript:bad)`x`*y*', 'https://wiki.minseong.co.kr/topic/#a"b')
        self.assertNotIn('<img', rendered)
        self.assertNotIn('|', rendered)
        self.assertNotIn('[', rendered)
        self.assertNotIn('`', rendered)
        self.assertNotIn('*', rendered)
        self.assertIn('&lt;img', rendered)
        self.assertIn('&#124;', rendered)
        self.assertIn('&quot;', rendered)

    def test_only_network_page_expands_one_marker(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='network/index.md'))
        config = {'docs_dir': 'docs'}
        with patch.object(views, 'render_for_docs', return_value='Generated table'):
            text = views.on_page_markdown('Before\n' + views.MARKER, page=page, config=config, files=[])
            self.assertIn('Before', text)
            self.assertIn('Generated table', text)
            self.assertNotIn(views.MARKER, text)
            for bad in ('No marker', views.MARKER * 2):
                with self.assertRaises(ValueError):
                    views.on_page_markdown(bad, page=page, config=config, files=[])
            page.file.src_uri = 'conditions/insomnia.md'
            self.assertEqual(views.on_page_markdown(views.MARKER, page=page, config=config, files=[]), views.MARKER)

    def test_next_build_refreshes_the_data_projection(self):
        with patch.object(views, 'build_ontology', return_value=(self.payload, {})) as builder:
            first = views.render_for_docs('docs')
            self.assertEqual(first, views.render_for_docs('docs'))
            self.assertEqual(builder.call_count, 1)
            updated = deepcopy(self.payload)
            formula = next(n for n in updated['@graph'] if 'km:Formula' in n.get('@type', []))
            formula['skos:prefLabel']['@value'] = '새 수록형 명칭'
            builder.return_value = (updated, {})
            views.on_pre_build({})
            self.assertIn('새 수록형 명칭', views.render_for_docs('docs'))
            self.assertEqual(builder.call_count, 2)
