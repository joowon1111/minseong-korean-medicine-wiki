#!/usr/bin/env python3
"""Regression checks for the herb efficacy-to-indication knowledge network."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class HerbEfficacyNetworkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.standard = (DOCS / "herbal-integrated/efficacy-indication-standard.md").read_text(
            encoding="utf-8"
        )
        self.heat = (DOCS / "herbal-integrated/heat-clearing-herbs.md").read_text(
            encoding="utf-8"
        )

    def test_major_efficacy_groups_are_defined(self) -> None:
        terms = (
            "해표", "청열", "사하", "방향화습", "이수삼습", "거풍습", "온리",
            "이기", "소식", "화담", "지해평천", "활혈거어", "지혈", "안신",
            "평간식풍", "개규", "보기", "보혈", "보음", "보양", "수삽", "구충",
        )
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, self.standard)

    def test_five_heat_clearing_groups_and_core_herbs_are_present(self) -> None:
        terms = (
            "청열사화", "청열조습", "청열해독", "청열량혈", "청허열",
            "석고", "지모", "황련", "황금", "황백", "금은화", "연교",
            "생지황", "목단피", "적작약", "청호", "지골피",
        )
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, self.heat)

    def test_detailed_guides_are_integrated_through_herb_finder(self) -> None:
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        herb_finder = (DOCS / "herbal-integrated/herbs.md").read_text(encoding="utf-8")

        self.assertIn("  - 본초 찾기: herbal-integrated/herbs.md", nav)
        self.assertNotIn("본초 효능·주치 표준: herbal-integrated/efficacy-indication-standard.md", nav)
        self.assertNotIn("청열약 5분류 비교: herbal-integrated/heat-clearing-herbs.md", nav)
        self.assertIn("efficacy-indication-standard.md", herb_finder)
        self.assertIn("heat-clearing-herbs.md", herb_finder)

    def test_core_heat_herbs_link_back_to_comparison(self) -> None:
        slugs = (
            "gypsum", "anemarrhena", "coptis", "scutellaria", "phellodendron",
            "honeysuckle", "forsythia", "rehmannia-root-fresh", "moutan",
            "red-peony", "qinghao", "digupi",
        )
        for slug in slugs:
            text = (DOCS / f"herbs/{slug}.md").read_text(encoding="utf-8-sig")
            with self.subTest(slug=slug):
                self.assertIn("heat-clearing-herbs.md", text)

    def test_oversimplified_equations_are_explicitly_rejected(self) -> None:
        for phrase in (
            "청열=항염", "활혈거어=혈액순환 개선", "보익=면역증강",
            "안신=진정", "화담=거담",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.standard)


if __name__ == "__main__":
    unittest.main()
