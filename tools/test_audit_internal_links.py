"""Regression checks for generated HTML links and anchors (no network required)."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import audit_internal_links as audit

class GeneratedLinks(unittest.TestCase):
    def check_html(self, files):
        with tempfile.TemporaryDirectory() as directory:
            site=Path(directory)
            for name, text in files.items():
                p=site/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
            output=io.StringIO()
            with patch.object(audit,'SITE',site),contextlib.redirect_stdout(output):
                result=audit.audit_site()
            return result,output.getvalue()

    def test_encoded_korean_and_same_page_anchors(self):
        errors,_=self.check_html({'index.html':'<h2 id="한글 제목"></h2><a href="#%ED%95%9C%EA%B8%80%20%EC%A0%9C%EB%AA%A9">x</a>'})
        self.assertEqual(errors,0)

    def test_missing_anchor_fails(self):
        errors,output=self.check_html({'index.html':'<a href="target/#missing">x</a>','target/index.html':'<h2 id="existing">x</h2>'})
        self.assertEqual(errors,1);self.assertIn('ERROR generated anchor',output)

    def test_absolute_same_origin_is_checked(self):
        errors,_=self.check_html({'index.html':'<a href="https://wiki.minseong.co.kr/target/#missing">x</a>','target/index.html':'x'})
        self.assertEqual(errors,1)

    def test_query_entities_and_encoded_path(self):
        errors,_=self.check_html({'index.html':'<a href="a%23b/?x=1&amp;y=2#ok">x</a>','a#b/index.html':'<h2 id="ok">x</h2>'})
        self.assertEqual(errors,0)

    def test_external_and_text_fragments_are_not_missing_ids(self):
        errors,_=self.check_html({'index.html':'<a href="https://example.com/no/#no">x</a><a href="#:~:text=hello">x</a><a href="mailto:a@example.com">x</a>'})
        self.assertEqual(errors,0)

    def test_directory_without_index_is_missing(self):
        errors,output=self.check_html({'index.html':'<a href="empty/">x</a>','empty/file.txt':'x'})
        self.assertEqual(errors,1);self.assertIn('ERROR generated link',output)

if __name__=='__main__':unittest.main()
