"""Index/knowledge graph contracts, malformed metadata and interrupted writes."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import atomic_output
import build_korean_search_index as search
import build_ai_knowledge_layer as ai

class BuildOutputs(unittest.TestCase):
    def test_metadata_invalid_yaml_and_non_mapping(self):
        for parser in (search.strip_frontmatter, ai.parse_frontmatter):
            for value in ('[broken', '[1, 2]', 'word', '42'):
                fm, body = parser('---\n' + value + '\n---\n# Title')
                self.assertEqual(fm, {})
                self.assertIn('# Title', body)
            self.assertEqual(parser('plain'), ({}, 'plain'))

    def test_title_keywords_urls_and_aliases(self):
        self.assertEqual(search.title_from({}, '# Heading', Path('fallback.md')), 'Heading')
        self.assertEqual(search.title_from({}, '', Path('fallback.md')), 'fallback')
        self.assertEqual(search.url_from(Path('docs/index.md')), '/')
        self.assertEqual(search.url_from(Path('docs/topic/index.md')), '/topic/')
        self.assertIn('잠이 안 와요', search.keyword_set('불면', '', {}))
        self.assertNotIn('<', search.clean_markdown('<b>Title</b> [link](url)'))

    def test_graph_deterministic_edges_and_explicit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs/'conditions').mkdir()
            (docs/'index.md').write_text('# Home\n[one](conditions/a.md) [two](conditions/a.md)')
            (docs/'conditions/a.md').write_text('---\nkcd: G47\n---\n# 불면\nG99 in body\nPMID: 12345678')
            with patch.object(ai, 'DOCS', docs):
                entities, relations = ai.build()
                ai.validate(entities, relations)
                self.assertEqual((entities, relations), ai.build())
                self.assertEqual(len(relations), 1)
                entity = next(e for e in entities if e['name'] == '불면')
                self.assertEqual(entity['codes'], {'kcd': ['G47']})
                self.assertEqual(entity['evidence_ids']['pmid'], ['12345678'])
                for url in ('https://evil.test/a', 'http://[broken', '../outside.md', 'javascript:alert(1)'):
                    self.assertIsNone(ai.resolve_target(docs/'index.md', url, {}))

    def test_graph_rejects_duplicates_and_dangling_edges(self):
        entity = {'id':'a', 'url':'/a', 'source_path':'a.md'}
        with self.assertRaises(ValueError): ai.validate([entity, entity], [])
        with self.assertRaises(ValueError): ai.validate([entity], [{'source':'a','relation':'links_to','target':'missing'}])
        ai.validate([], [])

    def test_failed_replace_preserves_previous_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'index.json'; path.write_bytes(b'old')
            with patch.object(Path, 'replace', side_effect=PermissionError()):
                with self.assertRaises(PermissionError): atomic_output.write_bytes(path, b'new')
            self.assertEqual(path.read_bytes(), b'old')
            self.assertEqual(list(Path(tmp).iterdir()), [path])
            atomic_output.write_bytes(path, b'new')
            self.assertEqual(path.read_bytes(), b'new')

    def test_unchanged_output_does_not_write_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'index.json'; path.write_bytes(b'old')
            with patch.object(ai, 'write_bytes') as writer:
                ai.write_if_changed(path, b'old')
                writer.assert_not_called()
