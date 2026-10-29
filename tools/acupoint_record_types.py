"""Record semantics shared by supplemental-page generation and AI export.

SA/AA are source record identifiers, not WHO point codes. Keep their old URLs.
"""
import re


def supplementary_type(code):
    code = code.upper()
    if re.fullmatch(r'SA[1-4]', code):
        return 'surface_anatomy'
    if code == 'AA1':
        return 'auricular_anatomy'
    if code in {'AA2', 'AA3'}:
        return 'auricular_point_combination'
    return None
