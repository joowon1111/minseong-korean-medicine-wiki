"""Composition browsing preserves qualified identities and current source data."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ontology import build_ontology
import ontology_views as views


class OntologyViews(unittest.TestCase):
    def test_treatment_routes_keep_exact_ids_and_both_qualified_sources(self):
        rendered = views.pattern_treatment_routes(self.payload)
        rows = [line for line in rendered.splitlines() if line.startswith('| <a')]
        self.assertEqual(len(rows), 19)
        blood = next(row for row in rows if '사물탕 — 국방 수록형' in row)
        self.assertIn('>혈허</a>', blood)
        self.assertIn('>보혈</a>', blood)
        self.assertNotIn('>기혈쌍보</a>', blood)
        for name in ('팔진탕 — 만병회춘 수록형', '십전대보탕 — 국방 수록형'):
            row = next(row for row in rows if name in row)
            self.assertIn('>기혈양허</a>', row)
            self.assertIn('>기혈쌍보</a>', row)
        self.assertEqual(rendered.count('class="ontology-treatment-route"'), 19)
        self.assertIn('외과이례', rendered)
        self.assertIn('五分', rendered)
        self.assertIn('냉감', rendered)
        for node in self.payload['@graph']:
            if node.get('rdf:predicate', {}).get('@id') in (
                    'km:hasTraditionalTreatmentPrinciple', 'km:hasTraditionalPatternContext'):
                self.assertIn(node['dcterms:source']['@id'], rendered)
        self.assertIn('반하후박탕 — 금궤요략 수록형', rendered)
        self.assertEqual(rendered, views.pattern_treatment_routes(self.payload))

    def test_route_join_does_not_infer_from_aliases_or_navigation(self):
        payload = deepcopy(self.payload)
        for record in payload['@graph']:
            if (record.get('rdf:predicate', {}).get('@id') == 'km:hasTraditionalTreatmentPrinciple'
                    and record['rdf:subject']['@id'].endswith('#blood-deficiency')):
                record['rdf:predicate']['@id'] = 'km:links_to_treatment_principle'
        text = views.pattern_treatment_routes(payload)
        self.assertNotIn('사물탕 — 국방 수록형', text)
        self.assertIn('팔진탕 — 만병회춘 수록형', text)
        alternate = deepcopy(next(n for n in payload['@graph']
                                  if n['@id'].endswith('#blood-deficiency')))
        alternate['@id'] += '-different-concept'
        payload['@graph'].append(alternate)
        record = deepcopy(next(n for n in self.payload['@graph']
                               if n.get('rdf:predicate', {}).get('@id') == 'km:hasTraditionalTreatmentPrinciple'
                               and n['rdf:subject']['@id'].endswith('#blood-deficiency')))
        record['@id'] += '-other-pattern'
        record['rdf:subject']['@id'] = alternate['@id']
        payload['@graph'].append(record)
        self.assertEqual(text, views.pattern_treatment_routes(payload))

    def test_route_view_preserves_alternate_evidence_and_escapes_all_text(self):
        payload = deepcopy(self.payload)
        record = deepcopy(next(n for n in payload['@graph']
                               if n.get('rdf:predicate', {}).get('@id') == 'km:hasTraditionalPatternContext'
                               and n['rdf:subject']['@id'].endswith('#siwu-guofang')))
        record['@id'] += '-alternate-evidence'
        record['dcterms:source']['@id'] += '-alternate'
        record['skos:scopeNote']['@value'] = 'left | right\n<script>bad()</script>'
        record['dcterms:description']['@value'] = '<img src=x onerror=bad()> | [click](javascript:bad) **excerpt**'
        payload['@graph'].append(record)
        rendered = views.pattern_treatment_routes(payload)
        self.assertEqual(rendered.count('class="ontology-treatment-route"'), 20)
        self.assertIn(record['dcterms:source']['@id'], rendered)
        self.assertIn('left &#124; right<br>&lt;script&gt;', rendered)
        self.assertIn('&lt;img', rendered)
        self.assertIn('&#91;click&#93;', rendered)
        self.assertNotIn('[click]', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertNotIn('<img', rendered)
        for row in rendered.splitlines():
            if row.startswith('| <a'):
                self.assertEqual(row.count('|'), 5)
        record['rdf:object']['@id'] = next(n['@id'] for n in payload['@graph']
                                          if n['@id'].endswith('#ginseng'))
        with self.assertRaises(ValueError):
            views.pattern_treatment_routes(payload)

    def test_treatment_marker_expands_once_from_the_shared_payload(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='network/index.md'))
        rendered = views.on_page_markdown(views.MARKER + views.TREATMENT_MARKER,
                                         page=page, config={'docs_dir': 'docs'}, files=[])
        self.assertNotIn(views.TREATMENT_MARKER, rendered)
        self.assertIn('class="ontology-treatment-route"', rendered)
        with self.assertRaises(ValueError):
            views.on_page_markdown(views.MARKER + views.TREATMENT_MARKER * 2,
                                   page=page, config={'docs_dir': 'docs'}, files=[])

    def test_explicit_variants_compare_shared_and_distinct_ingredient_ids(self):
        text = views.variant_comparisons(self.payload)
        panels = text.split('<details class="ontology-variant-comparison">')[1:]
        self.assertEqual(len(panels), 7)
        suanzaoren = next(p for p in panels if '산조인탕' in p.split('</summary>')[0])
        common = suanzaoren.split('</p>', 1)[0]
        self.assertIn('공통으로 등록된 본초 (3)', common)
        self.assertNotIn('복령</a>', common)
        self.assertIn('>복령</a>', suanzaoren)
        self.assertIn('>적복령</a>', suanzaoren)
        guibi = next(p for p in panels if '귀비탕' in p.split('</summary>')[0])
        self.assertIn('공통으로 등록된 본초 (8)', guibi)
        self.assertIn('>당귀</a>', guibi)
        self.assertIn('>원지</a>', guibi)
        self.assertIn('#donguibogam-version', guibi)

    def test_same_herbs_keep_different_doses_and_all_source_conditions(self):
        text = views.variant_comparisons(self.payload)
        self.assertIn('15립', text)
        self.assertIn('감초 2량·대조 20매', text)
        self.assertIn('감초 3량·대조 12매', text)
        self.assertIn('백복령 48량', text)
        self.assertIn('백복령 24량', text)
        self.assertEqual(text.count('class="ontology-variant-records"'), 7)
        for record in self.payload['@graph']:
            if record['@type'] == 'rdf:Statement' and record['rdf:predicate']['@id'] == 'km:sharesNameWith':
                self.assertIn(record['dcterms:source']['@id'], text)

    def test_links_aliases_and_duplicate_records_do_not_create_variant_pairs(self):
        payload = deepcopy(self.payload)
        text = views.variant_comparisons(payload)
        record = deepcopy(next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                               and n['rdf:predicate']['@id'] == 'km:sharesNameWith'))
        record['@id'] += '-reverse'
        record['rdf:subject'], record['rdf:object'] = record['rdf:object'], record['rdf:subject']
        payload['@graph'].append(record)
        self.assertEqual(text, views.variant_comparisons(payload))
        record['rdf:predicate']['@id'] = 'km:links_to_formula'
        self.assertEqual(text, views.variant_comparisons(payload))
        payload['@graph'] = [n for n in payload['@graph'] if n.get('rdf:predicate', {}).get('@id') != 'km:sharesNameWith']
        self.assertEqual(views.variant_comparisons(payload), '')

    def test_variant_view_escapes_labels_definitions_and_conditions(self):
        payload = deepcopy(self.payload)
        for node in payload['@graph']:
            if node['@id'].endswith('#guibi-jisheng'):
                node['skos:prefLabel']['@value'] = '<img src=x onerror=bad()>'
                node['skos:definition']['@value'] = '<script>bad()</script>'
            if (node['@type'] == 'rdf:Statement'
                    and node.get('rdf:subject', {}).get('@id', '').endswith('#guibi-jisheng')):
                node['skos:scopeNote']['@value'] = '<img src=x onerror=bad()>'
        text = views.variant_comparisons(payload)
        self.assertNotIn('<img', text)
        self.assertNotIn('<script>', text)
        self.assertIn('&lt;img', text)
        self.assertIn('&lt;script&gt;', text)

    def test_classical_context_controls_preserve_conditions_without_table_injection(self):
        payload = deepcopy(self.payload)
        record = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                      and n['rdf:predicate']['@id'] == 'km:recordsFormula')
        record['skos:scopeNote']['@value'] = 'left | right\nnew <tag>'
        text = views.classical_formula_table(payload)
        self.assertEqual(text.count('class="ontology-clause-context"'), 16)
        self.assertIn('left &#124; right<br>new &lt;tag&gt;', text)
        self.assertIn('先與小建中湯', text)
        self.assertIn('不差者，與小柴胡湯', text)
        for row in text.splitlines():
            if row.startswith('| <a'):
                self.assertEqual(row.count('|'), 5)

    def test_variant_marker_expands_once_in_the_existing_network_hook(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='network/index.md'))
        text = views.on_page_markdown(views.MARKER + '\n' + views.VARIANT_MARKER,
                                      page=page, config={'docs_dir': 'docs'}, files=[])
        self.assertNotIn(views.VARIANT_MARKER, text)
        self.assertIn('class="ontology-variant-comparison"', text)
        with self.assertRaises(ValueError):
            views.on_page_markdown(views.MARKER + views.VARIANT_MARKER * 2,
                                    page=page, config={'docs_dir': 'docs'}, files=[])

    def test_meridian_members_are_complete_numerically_ordered_and_source_qualified(self):
        text = views.meridian_members(self.payload)
        rows = [line for line in text.splitlines() if line.startswith('| <a')]
        self.assertEqual(len(rows), 14)
        self.assertEqual(sum(int(line.split(' | ')[1]) for line in rows), 361)
        pc = next(line for line in rows if '>수궐음심포경</a>' in line)
        self.assertIn(' | 9 | ', pc)
        self.assertIn('/pericardium-meridian/#_3', pc)
        self.assertIn('>내관 PC6</a>', pc)
        sp = next(line for line in rows if '>족태음비경</a>' in line)
        self.assertLess(sp.index('SP2</a>'), sp.index('SP10</a>'))
        payload = deepcopy(self.payload)
        record = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                      and n['rdf:predicate']['@id'] == 'km:belongsToMeridian')
        duplicate = deepcopy(record)
        duplicate['@id'] += '-another-source'
        payload['@graph'].append(duplicate)
        self.assertEqual(text, views.meridian_members(payload))
        duplicate['rdf:predicate']['@id'] = 'km:links_to_meridian'
        self.assertEqual(text, views.meridian_members(payload))

    def test_network_marker_uses_the_existing_payload(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='network/index.md'))
        text = views.on_page_markdown(views.MARKER + '\n' + views.MERIDIAN_MARKER,
                                      page=page, config={'docs_dir': 'docs'}, files=[])
        self.assertNotIn(views.MERIDIAN_MARKER, text)
        self.assertIn('>회음 CV1</a>', text)
        self.assertIn('>은교 GV28</a>', text)
        with self.assertRaises(ValueError):
            views.on_page_markdown(views.MARKER + views.MERIDIAN_MARKER * 2,
                                    page=page, config={'docs_dir': 'docs'}, files=[])

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
        inverse = rendered.split('### 본초에서 처방 찾아가기', 1)[1]
        self.assertIn('인삼</a>', inverse)
        red = next(line for line in inverse.splitlines() if '>적복령</a> |' in line)
        self.assertIn('산조인탕 — 동의보감 몽문 수록형', red)
        self.assertNotIn('산조인탕 — 금궤요략 수록형', red)

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
        self.assertGreaterEqual(len(rows), 5)
        self.assertGreaterEqual(sum('>복령</a> |' in line for line in rows), 4)
        self.assertEqual(sum('>적복령</a> |' in line for line in rows), 1)
        red = next(line for line in rows if '>적복령</a> |' in line)
        self.assertIn('동의보감 몽문 수록형', red)
        self.assertIn('#donguibogam-version', red)
        bark = views.herb_formula_table(self.payload, 'herbs/cinnamon-bark.md')
        self.assertIn('>계심</a>', bark)
        self.assertIn('>육계</a>', bark)
        heart = next(line for line in bark.splitlines() if '>계심</a>' in line and '산조인탕' in line)
        self.assertIn('동의보감 몽문 수록형', heart)

    def test_banxia_houpo_links_use_dried_leaf_and_formula_source(self):
        for slug, name in [('perilla-leaf', '자소엽'), ('magnolia-bark', '후박')]:
            rendered = views.herb_formula_table(self.payload, 'herbs/' + slug + '.md')
            rows = [line for line in rendered.splitlines() if line.startswith('| <a')]
            banxia = [line for line in rows if '반하후박탕 — 금궤요략 수록형' in line]
            self.assertEqual(len(banxia), 1)
            self.assertIn('>' + name + '</a>', banxia[0])
            self.assertIn('/formulas/banxia-houpo-tang/#source-dose-original', banxia[0])

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

    def test_priority_herb_pages_expose_every_registered_membership(self):
        expected = {'fresh-ginger': 17, 'jujube-fruit': 16, 'cinnamon-twig': 10,
                    'pinellia': 13, 'moschus': 1, 'cervi-parvum-cornu': 1,
                    'cornus-fructus': 5, 'dried-ginger': 4}
        for slug, count in expected.items():
            with self.subTest(herb=slug):
                source = 'herbs/' + slug + '.md'
                markdown = (Path('docs') / source).read_text()
                self.assertEqual(markdown.count(views.HERB_MARKER), 1)
                page = SimpleNamespace(file=SimpleNamespace(src_uri=source))
                text = views.on_page_markdown(markdown, page=page,
                                              config={'docs_dir': 'docs'}, files=[])
                self.assertNotIn(views.HERB_MARKER, text)
                table = views.herb_formula_table(self.payload, source)
                self.assertEqual(sum(line.startswith('| <a') for line in table.splitlines()), count)
                self.assertEqual(table.count('class="ontology-herb-context"'), count)

    def test_herb_conditions_retain_adjuncts_doses_and_preparation_identities(self):
        fresh = views.herb_formula_table(self.payload, 'herbs/fresh-ginger.md')
        dried = views.herb_formula_table(self.payload, 'herbs/dried-ginger.md')
        self.assertIn('기본 4미의 제조 배합과 매회 전탕 재료를 구분', fresh)
        self.assertIn('생강 三片·대추 二枚', fresh)
        self.assertNotIn('반하사심탕 — 상한론 송본 수록형', fresh)
        self.assertIn('반하사심탕 — 상한론 송본 수록형', dried)
        dates = views.herb_formula_table(self.payload, 'herbs/jujube-fruit.md')
        shanghan = next(line for line in dates.splitlines() if '소건중탕 — 상한론 송본 수록형</a>' in line)
        jinkui = next(line for line in dates.splitlines() if '소건중탕 — 금궤요략 수록형</a>' in line)
        self.assertIn('大棗 20매', shanghan)
        self.assertIn('大棗 12매', jinkui)
        banxia = views.herb_formula_table(self.payload, 'herbs/pinellia.md')
        self.assertIn('>반하곡</a>', banxia)
        self.assertIn('반하곡: 발효 가공', banxia)
        antler = views.herb_formula_table(self.payload, 'herbs/cervi-parvum-cornu.md')
        self.assertIn('제조 배합', antler)
        self.assertNotIn('보중익기탕', antler)

    def test_herb_conditions_escape_html_pipes_and_line_breaks(self):
        payload = deepcopy(self.payload)
        statement = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                         and n['rdf:predicate']['@id'] == 'km:containsHerb'
                         and n['rdf:object']['@id'].endswith('#fresh-ginger'))
        statement['skos:scopeNote']['@value'] = 'left | right\nnew <script>bad()</script>'
        text = views.herb_formula_table(payload, 'herbs/fresh-ginger.md')
        self.assertNotIn('<script>', text)
        self.assertIn('left &#124; right<br>new &lt;script&gt;bad()&lt;/script&gt;', text)
        for line in text.splitlines():
            if line.startswith('| <a'):
                self.assertEqual(line.count('|'), 4)

    def test_herb_view_keeps_multiple_qualifications_without_duplicate_rows(self):
        payload = deepcopy(self.payload)
        statement = next(n for n in payload['@graph'] if n['@type'] == 'rdf:Statement'
                         and n['rdf:predicate']['@id'] == 'km:containsHerb'
                         and n['rdf:object']['@id'].endswith('#fresh-ginger'))
        original = views.herb_formula_table(payload, 'herbs/fresh-ginger.md')
        extra = deepcopy(statement)
        extra['@id'] += '-additional-qualification'
        payload['@graph'].append(extra)
        self.assertEqual(views.herb_formula_table(payload, 'herbs/fresh-ginger.md'), original)
        extra['skos:scopeNote']['@value'] = '추가 조건 기록'
        text = views.herb_formula_table(payload, 'herbs/fresh-ginger.md')
        self.assertIn(statement['skos:scopeNote']['@value'], text)
        self.assertIn('추가 조건 기록', text)
        self.assertEqual(sum(line.startswith('| <a') for line in text.splitlines()), 17)
        extra['rdf:predicate']['@id'] = 'km:links_to_herb'
        self.assertEqual(views.herb_formula_table(payload, 'herbs/fresh-ginger.md'), original)

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
