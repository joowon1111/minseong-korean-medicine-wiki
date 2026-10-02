"""Keep explicitly authored patient search terms in the generated index."""
from pathlib import Path
import unittest

from build_korean_search_index import clean_markdown, keyword_set, strip_frontmatter


class AuthoredKeywordsTests(unittest.TestCase):
    def test_search_text_strips_heading_and_link_attributes(self):
        self.assertEqual(clean_markdown('# 약재 {#1}\n[곡아](grain.md){#grain-enzymes .card}\n설명'),
                         '약재 곡아 설명')

    def test_search_text_preserves_ordinary_braced_content(self):
        self.assertEqual(clean_markdown('용량 {1, 2}와 원문 {참고}'), '용량 {1, 2}와 원문 {참고}')

    def test_keywords_only_facial_palsy_metadata_remains_searchable(self):
        path = Path(__file__).resolve().parents[1] / "docs/authority/conditions/peripheral-facial-palsy.md"
        fm, _ = strip_frontmatter(path.read_text(encoding="utf-8-sig"))
        # The term may exist only in metadata; neither tags nor body may supply it.
        keys = keyword_set("말초성 안면마비", "", {"keywords": fm["keywords"]})
        self.assertIn("구안와사", keys)

    def test_mixed_fields_trim_deduplicate_and_ignore_empty_values(self):
        keys = keyword_set("", "", {"tags": [" 안면마비 ", None, ""],
                                     "keywords": "구안와사, 안면마비, "})
        self.assertEqual(keys, ["구안와사", "안면마비"])

    def test_unrelated_document_does_not_inherit_other_page_keywords(self):
        self.assertNotIn("구안와사", keyword_set("요통", "허리가 아파요", {}))


if __name__ == "__main__":
    unittest.main()
