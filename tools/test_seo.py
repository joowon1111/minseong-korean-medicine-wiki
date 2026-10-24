"""Protect canonical identity and prevent accidental de-indexing."""
import unittest
from pathlib import Path
import tempfile
from audit_seo import description_inventory, validate


class SEOTests(unittest.TestCase):
    url = 'https://example.org/article/'
    html = '''<head><title>문서</title><link rel="canonical" href="https://example.org/article/">
    <meta property="og:url" content="https://example.org/article/">
    <meta property="og:title" content="문서"><meta property="og:site_name" content="아카이브">
    <meta property="og:locale" content="ko_KR"><meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="문서"></head>'''

    def test_valid_identity(self):
        self.assertEqual(validate(self.html, self.url).titles, ['문서'])

    def test_conflicting_canonical_and_duplicate_titles_fail(self):
        for html in (self.html.replace('rel="canonical"', 'rel="alternate"'),
                     self.html.replace('</head>', '<title>다른 제목</title></head>'),
                     self.html.replace('property="og:url"', 'property="other"')):
            with self.assertRaises(ValueError):
                validate(html, self.url)

    def test_robots_directives(self):
        for key in ('robots', 'googlebot'):
            for directive in ('noindex,follow', 'NONE', 'noindex'):
                with self.assertRaisesRegex(ValueError, 'Non-indexable'):
                    validate(self.html + f'<meta name="{key}" content="{directive}">', self.url)
        validate(self.html + '<meta name="robots" content="index,follow">', self.url)

    def test_inventory_distinguishes_empty_fallback_and_shared_descriptions(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            urls = []
            for slug, description in (('home', '공통 설명'), ('fallback', ' 공통  설명 '),
                                      ('empty', '  \n '), ('unique', '무릎 침 연구의 통증과 기능 평가')):
                url = f'https://example.org/{slug}/'
                urls.append(url)
                target = site / slug / 'index.html'
                target.parent.mkdir()
                target.write_text(self.html.replace(self.url, url).replace(
                    '</head>', f'<meta name="description" content="{description}"></head>'), encoding='utf-8')
            (site / 'sitemap.xml').write_text(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
                ''.join(f'<url><loc>{url}</loc></url>' for url in urls) + '</urlset>', encoding='utf-8')
            result = description_inventory(site, '공통 설명')
            self.assertEqual(result['empty_urls'], [urls[2]])
            self.assertEqual(result['site_description_urls'], urls[:2])
            self.assertEqual(result['duplicate_groups'], [{'description': '공통 설명', 'urls': urls[:2]}])
            self.assertEqual(result['page_count'], 4)
