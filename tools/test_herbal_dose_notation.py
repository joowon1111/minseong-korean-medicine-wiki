"""Keep Korean herbal weight units distinct from time and fractions."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HerbalDoseNotationTests(unittest.TestCase):
    def test_weight_unit_explanations_use_pun(self):
        for path in (ROOT / "docs").rglob("*.md"):
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"(?:량|냥)·전·분|전·분(?:은|을|과| 관계)")
                self.assertNotRegex(text, r"\d+\s*푼의\s*\d+", "Keep fractions such as 10분의 1 distinct from weight units")

    def test_formula_amount_cells_do_not_use_minute_spelling(self):
        # Check only columns explicitly labelled as herbal amounts. Time,
        # decoction volume in prose, and proportional acupoint length are separate.
        amount_headers = {"수록량", "수록 약량", "원문량", "원문 약량", "금궤 수록량"}
        for path in (ROOT / "docs" / "formulas").glob("*.md"):
            amount_columns = []
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.startswith("|"):
                    amount_columns = []
                    continue
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if any(cell in amount_headers for cell in cells):
                    amount_columns = [i for i, cell in enumerate(cells) if cell in amount_headers]
                    continue
                for column in amount_columns:
                    if column < len(cells):
                        with self.subTest(path=str(path.relative_to(ROOT)), line=number):
                            self.assertNotRegex(cells[column], r"\d\s*분")


if __name__ == "__main__":
    unittest.main()
