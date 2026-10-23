"""Protect canonical identity and prevent accidental de-indexing."""
import unittest
from audit_seo import validate


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
