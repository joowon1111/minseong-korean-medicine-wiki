"""Every dated solar-term card must have its complete canonical story."""
import json
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

from daily_solar_stories import story_templates, on_page_content

DOCS = Path(__file__).resolve().parents[1] / "docs"


class DailySolarStories(unittest.TestCase):
    def test_all_dated_cards_have_complete_stories_and_resolved_links(self):
        templates = story_templates(DOCS)
        data = json.loads((DOCS / "assets/daily-korean-medicine/yangsheng.json").read_text())
        cards = [card for card in data["cards"] if card.get("solarTerm")]
        self.assertEqual(len(cards), 24)
        for card in cards:
            anchor = card["relatedHref"].split("#")[1]
            body = re.search('<template id="daily-term-story-' + anchor + '">(.*?)</template>', templates, re.S)
            self.assertIsNotNone(body, card["solarTerm"])
            self.assertGreater(len(body[1]), 2000, card["solarTerm"])
            self.assertGreaterEqual(body[1].count("<h4>"), 3, card["solarTerm"])
        for link in re.findall('href="([^"]+)"', templates):
            self.assertTrue(link.startswith(("/", "https://")), link)
            self.assertNotRegex(link, r"\.md(?:[?#]|$)")

    def test_templates_are_only_attached_to_daily_reader(self):
        for source in ["index.md", "daily-korean-medicine/solar-terms.md"]:
            page = SimpleNamespace(file=SimpleNamespace(src_uri=source))
            self.assertEqual(on_page_content("original", page=page, config={}, files=None), "original")
