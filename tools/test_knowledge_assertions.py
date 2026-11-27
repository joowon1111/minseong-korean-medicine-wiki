"""Source attribution, domain and reproducibility checks for curated relations."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_ai_knowledge_layer as ai


class KnowledgeAssertions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.docs = Path(self.tmp.name) / 'docs'
        (self.docs / 'formulas').mkdir(parents=True)
        self.page = self.docs / 'formulas/a.md'
        self.page.write_text('# Formula\n## Composition {#composition}\nIncludes ginseng.\n')
        self.source = Path(self.tmp.name) / 'assertions.json'
        self.entities = [
            {'id': 'km:formulas/a', 'type': 'formula', 'source_path': 'formulas/a.md',
             'url': ai.BASE_URL + '/formulas/a/'},
            {'id': 'km:herbs/ginseng', 'type': 'herb', 'source_path': 'herbs/ginseng.md',
             'url': ai.BASE_URL + '/herbs/ginseng/'},
        ]
        self.row = {'source': 'km:formulas/a', 'relation': 'has_ingredient',
                    'target': 'km:herbs/ginseng', 'context': 'Specified edition',
                    'evidence': {'source_path': 'formulas/a.md', 'anchor': 'composition',
                                 'quote': 'Includes ginseng.'}}

    def build(self, rows):
        self.source.write_text(json.dumps({'schema_version': '1.0', 'assertions': rows}))
        with patch.object(ai, 'DOCS', self.docs):
            return ai.build_assertions(self.entities, self.source)

    def test_evidence_url_context_and_determinism(self):
        payload = self.build([self.row])
        self.assertEqual(payload, self.build([self.row]))
        row = payload['assertions'][0]
        self.assertEqual(row['context'], 'Specified edition')
        self.assertEqual(row['evidence']['url'], ai.BASE_URL + '/formulas/a/#composition')
        self.assertEqual(row['evidence']['quote'], 'Includes ginseng.')
        self.assertIn('has_ingredient', payload['relation_types'])

    def test_missing_or_incompatible_entities_and_unknown_relations(self):
        for field, value in [('target', 'km:missing'), ('source', 'km:herbs/ginseng'),
                             ('relation', 'treats_condition')]:
            row = copy.deepcopy(self.row)
            row[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.build([row])

    def test_missing_source_excerpt_and_anchor_block_export(self):
        for field, value in [('source_path', '../outside.md'), ('quote', 'Changed text'),
                             ('quote', ''), ('anchor', 'removed')]:
            row = copy.deepcopy(self.row)
            row['evidence'][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.build([row])

    def test_quote_must_belong_to_the_cited_heading_section(self):
        self.page.write_text('## Composition {#composition}\nEmpty.\n'
                             '## Other section {#other}\nIncludes ginseng.\n')
        with self.assertRaises(ValueError):
            self.build([self.row])
        self.page.write_text('## Composition {#composition}\n'
                             '### Subsection\nIncludes ginseng.\n')
        self.assertEqual(len(self.build([self.row])['assertions']), 1)

    def test_hidden_text_cannot_support_an_assertion(self):
        for hidden in ['<!-- Includes ginseng. -->', '<script>Includes ginseng.</script>',
                       '<template>Includes ginseng.</template>']:
            self.page.write_text('## Composition {#composition}\n' + hidden)
            with self.subTest(hidden=hidden), self.assertRaises(ValueError):
                self.build([self.row])

    def test_duplicate_context_rejected_but_distinct_editions_preserved(self):
        with self.assertRaises(ValueError):
            self.build([self.row, self.row])
        other = copy.deepcopy(self.row)
        other['context'] = 'Different edition'
        self.assertEqual(len(self.build([self.row, other])['assertions']), 2)

    def test_invalid_rows_and_evidence_fields(self):
        for bad in [None, {}, {**self.row, 'context': []},
                    {**self.row, 'evidence': {'source_path': 'formulas/a.md'}},
                    {**self.row, 'unexpected': True}]:
            with self.subTest(row=bad), self.assertRaises(ValueError):
                self.build([bad])

    def test_base_formula_cannot_reference_itself(self):
        row = copy.deepcopy(self.row)
        row['relation'] = 'has_base_formula'
        row['target'] = row['source']
        with self.assertRaises(ValueError):
            self.build([row])

    def test_missing_source_is_not_silently_ignored(self):
        with self.assertRaises(FileNotFoundError):
            ai.build_assertions([], Path(self.tmp.name) / 'missing.json')

    def test_meridians_and_collections_have_distinct_types(self):
        self.assertEqual(ai.entity_type(ai.DOCS / 'meridian-network/stomach-meridian.md'), 'meridian')
        self.assertEqual(ai.entity_type(ai.DOCS / 'meridian-network/heart-meridian.md'), 'meridian')
        for path in ['meridian-network/index.md', 'meridian-network/extraordinary-vessels.md',
                     'meridian-network/special-points/index.md']:
            self.assertNotEqual(ai.entity_type(ai.DOCS / path), 'meridian')
