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
        views.on_pre_build({})

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

    def test_herb_document_keeps_exact_ingredient_part_names(self):
        poria = views.herb_formula_table(self.payload, 'herbs/poria.md')
        rows = [line for line in poria.splitlines() if line.startswith('| <a')]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum('>복령</a> |' in line for line in rows), 3)
        self.assertEqual(sum('>적복령</a> |' in line for line in rows), 1)
        red = next(line for line in rows if '>적복령</a> |' in line)
        self.assertIn('동의보감 몽문 수록형', red)
        self.assertIn('#donguibogam-version', red)
        bark = views.herb_formula_table(self.payload, 'herbs/cinnamon-bark.md')
        self.assertIn('>계심</a>', bark)
        self.assertNotIn('>육계</a>', bark)

    def test_herb_lookups_preserve_formulation_context_and_exact_page(self):
        text = views.herb_formula_table(self.payload, 'herbs/ginseng.md')
        self.assertIn('사군자탕 — 국방 수록형', text)
        self.assertIn('육군자탕 — 의학심오 수록형', text)
        self.assertIn('산조인탕 — 동의보감 몽문 수록형', text)
        self.assertNotIn('산조인탕 — 금궤요략 수록형', text)
        with self.assertRaises(ValueError):
            views.herb_formula_table(self.payload, 'herbs/ginseng-extract.md')
        seed = views.herb_formula_table(self.payload, 'herbs/ziziphus-seed.md')
        self.assertIn('산조인탕 — 금궤요략 수록형', seed)
        self.assertIn('산조인탕 — 동의보감 몽문 수록형', seed)

    def test_herb_markers_are_explicit_and_fail_on_invalid_placement(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='herbs/poria.md'))
        config = {'docs_dir': 'docs'}
        with patch.object(views, 'herb_payload', return_value=self.payload):
            text = views.on_page_markdown(views.HERB_MARKER, page=page, config=config, files=[])
            self.assertIn('>복령</a>', text)
            self.assertIn('>적복령</a>', text)
            self.assertNotIn(views.HERB_MARKER, text)
            self.assertEqual(views.on_page_markdown('Normal article', page=page, config=config, files=[]), 'Normal article')
            with self.assertRaises(ValueError):
                views.on_page_markdown(views.HERB_MARKER*2, page=page, config=config, files=[])
            page.file.src_uri = 'conditions/insomnia.md'
            with self.assertRaises(ValueError):
                views.on_page_markdown(views.HERB_MARKER, page=page, config=config, files=[])

    def test_next_build_refreshes_herb_payloads(self):
        with patch.object(views, 'build_ontology', return_value=(self.payload, {})) as builder:
            first = views.herb_payload('docs')
            self.assertEqual(first, views.herb_payload('docs'))
            self.assertEqual(builder.call_count, 1)
            updated = deepcopy(self.payload)
            builder.return_value = (updated, {'changed': True})
            views.on_pre_build({})
            self.assertIs(views.herb_payload('docs'), updated)
            self.assertEqual(builder.call_count, 2)

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
