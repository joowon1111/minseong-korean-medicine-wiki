"""Sitemap mapping must preserve existing output when Git metadata is incomplete."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import sitemap_lastmod as sitemap

class SitemapTests(unittest.TestCase):
    def test_source_resolution_and_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); docs=root/'docs';docs.mkdir()
            (docs/'index.md').write_text('# Home');(root/'outside.md').write_text('private')
            resolve=lambda url:sitemap._source_document(url, site_url='https://wiki.minseong.co.kr/wiki/',docs_dir=docs)
            self.assertEqual(resolve('https://wiki.minseong.co.kr/wiki/'),docs/'index.md')
            for url in ('https://evil.test/wiki/', 'https://wiki.minseong.co.kr/other/',
                        'https://wiki.minseong.co.kr/wiki/%2e%2e/outside/'):
                self.assertIsNone(resolve(url))

    def test_dates_and_missing_history_do_not_corrupt_sitemap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);docs=root/'docs';docs.mkdir();site=root/'site';site.mkdir()
            (docs/'index.md').write_text('# Home')
            path=site/'sitemap.xml'
            original='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://wiki.minseong.co.kr/</loc><lastmod>old</lastmod></url></urlset>'
            path.write_text(original)
            config={'site_dir':str(site),'docs_dir':str(docs),'site_url':'https://wiki.minseong.co.kr/'}
            with patch.object(sitemap,'_repository_root',return_value=root),patch.object(sitemap,'_git_document_dates',return_value={}):
                with self.assertRaises(RuntimeError):sitemap.update_sitemap(config)
            self.assertEqual(path.read_text(),original)
            with patch.object(sitemap,'_repository_root',return_value=root),patch.object(sitemap,'_git_document_dates',return_value={'docs/index.md':'2026-09-07T12:00:00Z'}):
                self.assertEqual(sitemap.update_sitemap(config),(1,1))
            self.assertIn('2026-09-07T12:00:00Z',path.read_text())
