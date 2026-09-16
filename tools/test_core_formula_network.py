#!/usr/bin/env python3
"""Regression checks for the core formula and processing knowledge network."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FORMULARY = DOCS / "herbal-integrated/general-formulary.md"


class CoreFormulaNetworkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.formulary = FORMULARY.read_text(encoding="utf-8")
        self.core_section = self.formulary.split(
            "## 임상 핵심 처방 50선", 1
        )[1].split("\n## 비위·소화", 1)[0]

    def test_core_list_has_exactly_fifty_unique_formula_links(self) -> None:
        links = re.findall(r"^\| \[([^]]+)]\(([^)]+)\)", self.core_section, re.MULTILINE)
        self.assertEqual(len(links), 50)
        self.assertEqual(len({name for name, _ in links}), 50)

    def test_all_core_formula_targets_exist(self) -> None:
        links = re.findall(r"^\| \[([^]]+)]\(([^)]+)\)", self.core_section, re.MULTILINE)
        base = FORMULARY.parent
        for name, target in links:
            path = (base / target.split("#", 1)[0]).resolve()
            with self.subTest(formula=name, target=target):
                self.assertTrue(path.is_file())
                self.assertTrue(path.is_relative_to(DOCS.resolve()))

    def test_processing_standard_covers_required_fields(self) -> None:
        evidence = (DOCS / "herbal-integrated/evidence.md").read_text(encoding="utf-8")
        for term in (
            "기준 원료", "포제명", "포제 목적", "원방 단위", "현대 사용량",
            "제형·제법", "전탕 순서", "선전", "후하", "용화",
        ):
            with self.subTest(term=term):
                self.assertIn(term, evidence)

    def test_foundational_formula_pages_document_processing(self) -> None:
        slugs = (
            "sijunzi-tang", "siwu-tang", "liujunzi-tang", "bazhen-tang",
            "shi-quan-da-bu-tang",
        )
        for slug in slugs:
            text = (DOCS / f"formulas/{slug}.md").read_text(encoding="utf-8-sig")
            with self.subTest(slug=slug):
                self.assertIn("법제", text)
                self.assertTrue("출전" in text or "원방" in text)
                self.assertIn("제형", text)

    def test_eight_foundational_herbs_include_processing_guidance(self) -> None:
        slugs = (
            "ginseng", "atractylodes", "poria", "licorice",
            "prepared-rehmannia", "angelica", "white-peony", "chuanxiong",
        )
        for slug in slugs:
            text = (DOCS / f"herbs/{slug}.md").read_text(encoding="utf-8-sig")
            with self.subTest(slug=slug):
                self.assertTrue(any(term in text for term in ("수치", "법제", "포제", "가공")))


if __name__ == "__main__":
    unittest.main()
