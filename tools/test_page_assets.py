"""Widget loading must preserve dependencies and never leak between pages."""
from types import SimpleNamespace
import unittest
import page_assets


class PageAssets(unittest.TestCase):
    def render(self, html, config=None):
        config = config or {"theme": {"features": []}, "extra_css": [], "extra_javascript": [
            "assets/reading-layout.js", "assets/archive-tools/search-core.js?v=1",
            "assets/archive-tools/ai-client.js", "assets/archive-tools/tools.js",
            "assets/learning/learning.js", "assets/korean-search-185.js",
        ]}
        original = list(config["extra_javascript"])
        page = SimpleNamespace(content=html, file=SimpleNamespace(src_uri="conditions/test.md"))
        context = page_assets.on_page_context({"config": config}, page=page, config=config, nav=None)
        self.assertEqual(config["extra_javascript"], original)
        return context["config"]["extra_javascript"]

    def test_article_keeps_search_and_reading_aids_without_widget_bundles(self):
        self.assertEqual(self.render("<h1>Article</h1>"), ["assets/reading-layout.js", "assets/korean-search-185.js"])

    def test_comparison_keeps_core_before_ui_without_ai(self):
        scripts = self.render("<div data-archive-compare='formula'></div>")
        self.assertIn("assets/archive-tools/search-core.js?v=1", scripts)
        self.assertIn("assets/archive-tools/tools.js", scripts)
        self.assertNotIn("assets/archive-tools/ai-client.js", scripts)
        self.assertLess(scripts.index("assets/archive-tools/search-core.js?v=1"), scripts.index("assets/archive-tools/tools.js"))

    def test_finder_keeps_ai_and_learning_does_not_leak_to_next_article(self):
        self.assertIn("assets/archive-tools/ai-client.js", self.render("<div data-archive-finder></div>"))
        self.assertIn("assets/learning/learning.js", self.render("<div data-learning-room></div>"))
        self.assertNotIn("assets/learning/learning.js", self.render("<p>ordinary article</p>"))

    def test_daily_and_reader_markers_handle_quotes_and_attributes(self):
        needed = page_assets.needed_assets("<section data-daily-km-topics></section><div id='dsb-reader'></div>", "index.md")
        self.assertTrue(needed["assets/daily-korean-medicine/reader-core.js"])
        self.assertTrue(needed["assets/daily-korean-medicine/special.js"])
        self.assertFalse(needed["assets/daily-korean-medicine.js"])
        self.assertTrue(needed["assets/donguisusebowon/reader.js"])
        self.assertFalse(page_assets.needed_assets("<!-- <div data-learning-room> -->", "index.md")["assets/learning/learning.js"])

    def test_point_detail_keeps_diagram_styles_without_explorer_scripts(self):
        needed = page_assets.needed_assets(
            '<div class="acupoint-location"><nav class="acupoint-sequence"></nav></div>',
            'acupuncture/points/lu2.md')
        self.assertTrue(needed["assets/acupoint-atlas/explorer.css"])
        self.assertFalse(needed["assets/acupoint-atlas/explorer.js"])
        self.assertFalse(needed["assets/acupoint-atlas/discovery.js"])

    def test_instant_navigation_keeps_shared_subscribers(self):
        config = {"theme": {"features": ["navigation.instant"]}, "extra_css": [], "extra_javascript": ["assets/learning/learning.js"]}
        self.assertEqual(self.render("", config), ["assets/learning/learning.js"])
