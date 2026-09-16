#!/usr/bin/env python3
"""Regression checks for the core formula and processing knowledge network."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FORMULARY = DOCS / "herbal-integrated/general-formulary.md"


class CoreFormulaNetworkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.formulary = FORMULARY.read_text(encoding="utf-8")
        self.core_section = self.formulary.split(
            "## 임상 핵심 처방 100선", 1
        )[1].split("\n## 비위·소화", 1)[0]

    def test_core_list_has_exactly_one_hundred_unique_formula_links(self) -> None:
        links = re.findall(r"^\| \[([^]]+)]\(([^)]+)\)", self.core_section, re.MULTILINE)
        self.assertEqual(len(links), 100)
        self.assertEqual(len({name for name, _ in links}), 100)
        self.assertEqual(len({target for _, target in links}), 100)

    def test_core_list_is_integrated_by_clinical_axis(self) -> None:
        expected = (
            "보기·기혈·회복 16선", "보음·보양·신허 6선",
            "비위·소화·온중·변비 14선", "담음·기체·안신 12선",
            "외감·호흡·이비인후 13선", "청열·습열·온병·피부 10선",
            "수습·부종·배뇨 6선", "여성·임신·산후 11선",
            "통증·풍습·활혈 9선", "화해·공하 3선",
        )
        positions = [self.core_section.index(heading) for heading in expected]
        self.assertEqual(positions, sorted(positions))

    def test_legacy_fifty_anchor_is_preserved(self) -> None:
        self.assertIn('id="core-formulas-50"', self.formulary)
        self.assertIn('{#core-formulas-100}', self.formulary)

    def test_all_core_formula_targets_exist(self) -> None:
        links = re.findall(r"^\| \[([^]]+)]\(([^)]+)\)", self.core_section, re.MULTILINE)
        base = FORMULARY.parent
        for name, target in links:
            path = (base / unquote(target.split("#", 1)[0])).resolve()
            with self.subTest(formula=name, target=target):
                self.assertTrue(path.is_file())
                self.assertTrue(path.is_relative_to(DOCS.resolve()))

    def test_original_core_fifty_are_preserved_inside_the_hundred(self) -> None:
        names = {name for name, _ in re.findall(
            r"^\| \[([^]]+)]\(([^)]+)\)", self.core_section, re.MULTILINE
        )}
        original = {
            "사군자탕", "육군자탕", "사물탕", "팔물탕", "십전대보탕",
            "보중익기탕", "귀비탕", "생맥산", "당귀보혈탕", "육미지황환",
            "공진단", "경옥고", "평위산", "향사육군자탕", "삼령백출산",
            "이진탕", "온담탕", "반하사심탕", "보화환", "반하후박탕",
            "제천전", "계지탕", "마황탕", "갈근탕", "소청룡탕",
            "소시호탕", "대시호탕", "마행감석탕", "맥문동탕", "오령산",
            "진무탕", "영계출감탕", "황련해독탕", "용담사간탕", "백호탕",
            "방풍통성산", "팔정산", "당귀작약산", "계지복령환", "온경탕",
            "생화탕", "가미소요산", "혈부축어탕", "보양환오탕", "소복축어탕",
            "독활기생탕", "오적산", "작약감초탕", "산조인탕", "천왕보심단",
        }
        self.assertEqual(len(original), 50)
        self.assertTrue(original.issubset(names))

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

    def test_expansion_formula_pages_include_processing_guidance(self) -> None:
        slugs = (
            "yupingfeng-san", "zhigancao-tang", "huangqi-guizhi-wuwu-tang",
            "lizhong-tang", "xiaojianzhong-tang", "huangqi-jianzhong-tang",
            "xiaoyao-san", "mazi-ren-wan", "dachengqi-tang", "bulsu-san",
            "qingying-tang", "sanren-tang", "zhuling-tang", "jiaoai-tang",
            "shoutai-wan",
        )
        for slug in slugs:
            text = (DOCS / f"formulas/{slug}.md").read_text(encoding="utf-8-sig")
            with self.subTest(slug=slug):
                self.assertTrue(any(term in text for term in ("수치", "법제", "포제", "가공")))
                self.assertTrue(any(term in text for term in ("제형", "탕제", "산제", "환제")))

    def test_expansion_herbs_include_processing_guidance(self) -> None:
        slugs = (
            "astragalus", "cinnamon-twig", "ephedra",
            "coptis", "scutellaria", "cinnamon-bark",
        )
        for slug in slugs:
            text = (DOCS / f"herbs/{slug}.md").read_text(encoding="utf-8-sig")
            with self.subTest(slug=slug):
                self.assertTrue(any(term in text for term in ("수치", "법제", "포제", "가공")))


if __name__ == "__main__":
    unittest.main()
