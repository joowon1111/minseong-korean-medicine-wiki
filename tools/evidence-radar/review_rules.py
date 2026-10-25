"""Conservative review gates; design labels are not certainty-of-effect grades."""
import re

EFFECT_DESIGNS = {
    'rct', 'clinical trial', 'systematic review',
    'systematic review & meta-analysis', 'meta-analysis',
}

def valid_title(value):
    title = str(value or '').strip()
    return bool(title) and title.lower().strip(' [].') not in {
        'not available', 'no title', 'untitled', 'n/a',
    }

def is_protocol(title, abstract='', publication_types=(), study_type=''):
    # A completed paper may mention its registered protocol or treatment protocol.
    label = ' '.join([str(title), str(study_type), *map(str, publication_types or [])]).lower()
    return bool(re.search(r'\bprotocol\b', label) or re.search(
        r'\bwill be (?:randomi[sz]ed|recruited|conducted|published)\b|'
        r'\bstudy protocol\b|\bprotocol for (?:a |the )?(?:systematic|randomi[sz]ed)',
        str(abstract).lower()))

def review_reasons(row):
    """Recheck content, even when upstream type/level claims A/B or RCT."""
    title = str(row.get('title') or '')
    abstract = str(row.get('abstract') or '')
    types = row.get('publication_types') or []
    if not isinstance(types, list):
        types = [types]
    text = ' '.join([title, abstract, str(row.get('study_type') or ''),
                     *map(str, types)]).lower()
    reasons = []
    pico = row.get('pico') if isinstance(row.get('pico'), dict) else {}
    if not abstract.strip() and not all(pico.get(key) for key in ('population', 'intervention', 'comparator', 'outcomes')):
        reasons.append('clinical-details-missing')
    if not valid_title(title):
        reasons.append('title-missing')
    if is_protocol(title, abstract, types, row.get('study_type')):
        reasons.append('protocol')
    if str(row.get('study_type') or '').lower() not in EFFECT_DESIGNS:
        reasons.append('not-completed-effect-study')
    if re.search(r'scoping review|theoretical|bibliometric|network pharmacology|molecular docking', text):
        reasons.append('not-completed-effect-study')
    if re.search(r'combined with|combining |adjunctive|adjuvant|add-on|\bplus\b|'
                 r'integrated.{0,60}(?:medicine|pharmacotherapy)|'
                 r'acupuncture.pharmacotherapy|multi(?:disciplinary|modal)|'
                 r'pharmacological and non.pharmacological|'
                 r'farmacol[oó]gicos y no farmacol[oó]gicos', text):
        reasons.append('indirect-or-combination')
    if re.search(r'warm[- ]needle|warm acupuncture|moxibustion|auricular|ear acupuncture', text):
        reasons.append('modality-components-review')
    if re.search(r'pilot|feasibility|retrospective registration|late.registration', text):
        reasons.append('pilot-or-registration-review')
    if re.search(r'retract|withdrawn|erratum|corrigendum|expression of concern', text):
        reasons.append('unsafe-publication-type')
    if not row.get('doi') and not row.get('pmid'):
        reasons.append('identifier-missing')
    if row.get('evidence_level') == 'P':
        reasons.append('protocol')
    return list(dict.fromkeys(reasons))
