"""Regression tests for public exports, navigation, and structured metadata."""

from datetime import date, timedelta
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from mkdocs.exceptions import PluginError
import page_discovery as discovery
from audit_page_discovery import audit, site_path


class Files:
    def __init__(self, pages):
        self.pages = pages

    def get_file_from_path(self, path):
        return self.pages.get(path)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = {"site_url": "https://example.org/wiki/", "site_name": "아카이브", "site_dir": self.temp.name}
        self.page = SimpleNamespace(
            title='시험 <문서>', canonical_url='https://example.org/wiki/conditions/test/',
            meta={"description": '설명 "테스트"', "last_reviewed": "2026-01-02", "private_note": "DO NOT EXPORT"},
            file=SimpleNamespace(src_uri='conditions/test.md', dest_uri='conditions/test/index.html'))
        self.files = Files({"conditions/index.md": SimpleNamespace(url='conditions/', page=SimpleNamespace(title='증상·질환')),
                            "conditions/next.md": SimpleNamespace(url='conditions/next/', page=SimpleNamespace(title='다음 문서'))})
        discovery.on_pre_build(self.config)

    def render(self, body):
        content = discovery.on_page_content(body, self.page, self.config, self.files)
        output = discovery.on_post_page('<html><head></head><body>' + content + '</body></html>', self.page, self.config)
        payload = json.loads((Path(self.temp.name) / 'assets/ai/pages/conditions/test/index.json').read_text())
        return content, output, payload

    def test_english_article_and_exports_keep_korean_chrome(self):
        self.page.meta["lang"] = "en"
        body = '<h2 id="references">Sources and Further Reading</h2><p>English text</p>'
        content = discovery.on_page_content(body, self.page, self.config, self.files)
        output = discovery.on_post_page('<html lang="ko"><head></head><body class="theme"><article class="md-content__inner">' + content + '</article></body></html>', self.page, self.config)
        payload = json.loads((Path(self.temp.name) / 'assets/ai/pages/conditions/test/index.json').read_text())
        self.assertIn('<html lang="en">', output)
        self.assertIn('<body lang="ko" class="theme">', output)
        self.assertIn('<article lang="en" class="md-content__inner">', output)
        self.assertIn('"inLanguage":"en"', output)
        self.assertEqual(payload['language'], 'en')
        self.assertIn('>Home</a>', content)
        self.assertIn('>Sources</a>', content)
        self.assertIn('aria-label="Article shortcuts"', content)
        self.assertIn('title="Article text (JSON)"', output)

    def test_default_and_unsupported_languages_keep_korean(self):
        for value in (None, 'ko', 'ko-KR', 'fr', '<script>', {}):
            self.page.meta['lang'] = value
            content, output, payload = self.render('<h2 id="sources">출처</h2>')
            self.assertEqual(payload['language'], 'ko-KR')
            self.assertIn('"inLanguage":"ko-KR"', output)
            self.assertIn('근거·출처 확인', content)
            self.assertNotIn('<body lang=', output)

    def test_public_text_and_real_anchors_only(self):
        content, output, payload = self.render('<h1>시험</h1><h2 id="safety">주의사항<a class="headerlink" href="#safety">¶</a></h2><p>공개 <strong>본문</strong></p><script>private()</script><div hidden><p>숨김</p></div><p aria-hidden="true">장식</p><h2 id="sources">근거와 참고자료</h2><a href="../next/">다음</a>')
        self.assertIn('주의사항 먼저 보기', content)
        self.assertIn('href="#sources"', content)
        self.assertIn('공개 본문', payload['text'])
        for hidden in ['private()', '숨김', '장식', 'DO NOT EXPORT', '¶']:
            self.assertNotIn(hidden, payload['text'])
        self.assertNotIn('private_note', payload)
        self.assertEqual(payload['headings'][0]['url'], self.page.canonical_url + '#safety')
        self.assertIn('https://example.org/wiki/conditions/next/', payload['links'])
        self.assertIn('rel="alternate" type="application/json"', output)
        self.assertNotIn('private_note', output)

    def test_breadcrumbs_share_visible_and_structured_paths(self):
        content, output, _ = self.render('<h1>시험</h1>')
        self.assertIn('aria-current="page"', content)
        self.assertIn('시험 &lt;문서&gt;', content)
        self.assertIn('https://example.org/wiki/conditions/', content)
        self.assertIn('"position":3', output)
        self.assertNotIn('lastReviewed', output)
        self.assertNotIn('dateModified', output)

    def test_existing_medical_schema_is_not_duplicated(self):
        markup = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"MedicalWebPage","name":"기존 문서"}</script>'
        _, output, payload = self.render(markup + '<p>본문</p>')
        self.assertEqual(output.count('"@type":"MedicalWebPage"'), 1)
        self.assertIn(markup, output)
        self.assertNotIn('기존 문서', payload['text'])

    def test_existing_graph_and_faq_types(self):
        parser = discovery.Article()
        parser.feed('<script type="application/ld+json">{"@graph":[{"@type":["FAQPage","WebPage"]}]}</script>')
        self.assertEqual(parser.types, {'FAQPage', 'WebPage'})

    def test_script_and_attribute_escaping(self):
        self.page.title = '</script><script>alert(1)</script>"'
        _, output, payload = self.render('<p>본문</p>')
        self.assertNotIn('<script>alert(1)</script>', output)
        self.assertIn('\\u003c/script\\u003e', output)
        self.assertEqual(payload['title'], self.page.title)

    def test_review_dates_stay_private_for_all_values(self):
        for value in ('2026-01-02', date(2026, 1, 2), None, '', {}, 'invalid', '2026-02-30', (date.today() + timedelta(days=1)).isoformat()):
            self.page.meta['last_reviewed'] = value
            content, output, payload = self.render('')
            self.assertNotIn('문서 검토일', content)
            self.assertNotIn('lastReviewed', output)
            self.assertNotIn('last_reviewed', payload)
            self.assertEqual(payload['text'], '')
            self.assertNotIn('archive-reading-tools', content)
            self.assertEqual(self.page.meta['last_reviewed'], value)

    def test_unsafe_urls_are_not_exported(self):
        for value in ('javascript:alert(1)', 'data:text/html,test', 'https://user:pass@example.org/', 'https://[', '/bad\\path', '/line\nbreak', None):
            self.assertIsNone(discovery.http_url(value, self.page.canonical_url))
        self.assertEqual(discovery.http_url('#참고', self.page.canonical_url), self.page.canonical_url + '#참고')

    def test_search_title_and_citation_preserve_editorial_title_and_privacy(self):
        self.page.meta['search_title'] = '검색 질문: "조건" <비교>'
        self.page.meta['reader_tools'] = True
        original_title = self.page.title
        content, output, payload = self.render('<p>본문</p>')
        self.assertEqual(payload['title'], self.page.meta['search_title'])
        self.assertEqual(self.page.title, original_title)
        self.assertIn('data-citation-title="검색 질문: &quot;조건&quot; &lt;비교&gt;"', content)
        self.assertIn('data-citation-url="' + self.page.canonical_url + '"', content)
        self.assertIn('https://example.org/wiki/guide/#publisher', content)
        self.assertIn('data-copy-citation="citation" hidden', content)
        self.assertIn('출처·인용 원칙', content)
        for field in ('lastReviewed', 'dateModified', 'reviewedBy', '"author"'):
            self.assertNotIn(field, output)
        self.assertEqual(payload['text'], '본문')

    def test_citation_is_opt_in_and_title_falls_back(self):
        for value in (None, False, 'true'):
            self.page.meta['reader_tools'] = value
            self.assertEqual(discovery.reader_tools(self.page, self.config), '')
        for value in ('', '  ', {}, None):
            self.page.meta['search_title'] = value
            self.assertEqual(discovery.document_title(self.page), self.page.title)

    def test_curated_related_documents(self):
        self.page.meta['related_reading'] = [{'document': 'conditions/next.md', 'reason': '다음 단계 <확인>'}]
        content, output, payload = self.render('<p>본문</p>')
        self.assertIn('다음 단계 &lt;확인&gt;', content)
        self.assertIn('"relatedLink"', output)
        self.assertEqual(len(payload['related_reading']), 1)
        self.assertNotIn('다음 단계', payload['text'])

    def test_invalid_related_documents_fail_the_build(self):
        for rows in ({}, ['bad'], [{'document': '../outside.md', 'reason': '이동'}],
                     [{'document': 'conditions/next.md', 'reason': ''}],
                     [{'document': 'conditions/next.md', 'reason': '이동'}] * 2):
            self.page.meta['related_reading'] = rows
            with self.assertRaises(PluginError):
                discovery.on_page_content('<p>본문</p>', self.page, self.config, self.files)

    def test_output_cannot_escape_site(self):
        with self.assertRaises(PluginError):
            discovery.write_document(self.temp.name, '../outside.json', {})

    def test_page_index_resets_between_builds(self):
        self.render('<p>본문</p>')
        discovery.on_post_build(self.config)
        index = Path(self.temp.name) / 'assets/ai/page-index.json'
        self.assertEqual(len(json.loads(index.read_text())['pages']), 1)
        discovery.on_pre_build(self.config)
        discovery.on_post_build(self.config)
        self.assertEqual(json.loads(index.read_text())['pages'], [])

    def test_home_has_website_and_no_single_item_breadcrumb(self):
        self.page.canonical_url = self.config['site_url']
        self.page.file.src_uri = 'index.md'
        content, output, _ = self.render('<h1>홈</h1>')
        self.assertNotIn('archive-breadcrumbs', content)
        self.assertNotIn('BreadcrumbList', output)
        self.assertIn('"@type":"WebSite"', output)

    def test_sections_preserve_context_and_exclude_hidden_content(self):
        _, _, payload = self.render(
            '<p>도입부</p><h2 id="한글">출전 <em>비교</em></h2>'
            '<p>구성 차이 <a href="https://example.net/source">원전</a></p>'
            '<div hidden><h3 id="hidden">숨긴 제목</h3><p>PRIVATE</p></div>'
            '<h3 id="trial">현대 연구</h3><p>대상과 기간 <a href="../next/">관련 문서</a></p>'
            '<script>SECRET</script><h2 id="empty">다음 절</h2>')
        sections = payload['sections']
        self.assertEqual([s['title'] for s in sections], ['출전 비교', '현대 연구', '다음 절'])
        self.assertEqual(sections[0]['text'], '구성 차이 원전')
        self.assertEqual(sections[0]['url'], self.page.canonical_url + '#%ED%95%9C%EA%B8%80')
        self.assertEqual(sections[0]['links'], ['https://example.net/source'])
        self.assertEqual(sections[1]['links'], ['https://example.org/wiki/conditions/next/'])
        self.assertEqual(sections[2]['text'], '')
        self.assertNotIn('도입부', str(sections))
        self.assertNotIn('PRIVATE', str(sections))
        self.assertNotIn('SECRET', str(sections))
        self.assertIn('도입부', payload['text'])

    def test_home_editor_identity_extends_existing_publisher_graph(self):
        source = (Path(__file__).resolve().parents[1] / 'docs/index.md').read_text()
        parser = discovery.Article()
        parser.feed(source)
        self.assertIn('WebSite', parser.types)
        start = source.index('<script type="application/ld+json">') + len('<script type="application/ld+json">')
        graph = json.loads(source[start:source.index('</script>', start)])['@graph']
        website, = [node for node in graph if node['@type'] == 'WebSite']
        editors = {node['@id']: node for node in graph if node['@type'] == 'Person'}
        self.assertEqual({editors[ref['@id']]['name'] for ref in website['editor']}, {'목정일', '김문정'})
        self.assertEqual(website['publisher']['@id'], 'https://wiki.minseong.co.kr/#publisher')
        for person in editors.values():
            self.assertEqual(person['worksFor']['@id'], 'https://www.minseong.co.kr/#organization')
            self.assertNotIn('reviewedBy', person)

    def test_unanchored_html_heading_ends_previous_passage_without_inventing_url(self):
        _, _, payload = self.render('<h2 id="source">출전</h2><p>원문 문맥</p>'
                                    '<h2>도구 화면</h2><p>별도 안내</p>'
                                    '<h3 id="result">결과</h3><p>연구 결과</p>')
        self.assertEqual([s['text'] for s in payload['sections']], ['원문 문맥', '연구 결과'])
        self.assertIn('별도 안내', payload['text'])

    def test_encoded_document_url_and_editorial_title(self):
        self.page.meta['title'] = '정확한 문서 제목'
        self.page.file.dest_uri = 'conditions/한글 이름/index.html'
        html = discovery.on_page_content('<p>본문</p>', self.page, self.config, self.files)
        output = discovery.on_post_page('<head></head>' + html, self.page, self.config)
        self.assertIn('conditions/%ED%95%9C%EA%B8%80%20%EC%9D%B4%EB%A6%84/index.json', output)
        payload = json.loads((Path(self.temp.name) / 'assets/ai/pages/conditions/한글 이름/index.json').read_text())
        self.assertEqual(payload['title'], '정확한 문서 제목')

    def test_generated_audit_detects_missing_anchors_and_incomplete_index(self):
        _, output, _ = self.render('<h2 id="section">본문</h2>')
        discovery.on_post_build(self.config)
        site = Path(self.temp.name)
        html = site / 'conditions/test/index.html'
        html.parent.mkdir(parents=True)
        html.write_text(output)
        (site / 'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + self.page.canonical_url + '</loc></url></urlset>')
        self.assertEqual(audit(site), (1, 1))
        html.write_text(output.replace('id="section"', 'id="other"'))
        with self.assertRaisesRegex(ValueError, 'Missing heading'):
            audit(site)
        discovery.on_pre_build(self.config)
        discovery.on_post_build(self.config)
        with self.assertRaisesRegex(ValueError, 'each sitemap URL'):
            audit(site)

    def test_auditor_rejects_external_paths_and_traversal(self):
        for url in ('https://other.org/wiki/a/', 'https://example.org/wiki2/a/',
                    'https://example.org/wiki/%2e%2e/outside.json'):
            with self.assertRaises(ValueError):
                site_path(Path(self.temp.name), url, self.config['site_url'])


if __name__ == '__main__':
    unittest.main()

