"""Compare saved texts/AI page JSON locally; similarity is a clue, not a verdict.

Usage: python tools/compare_content_reuse.py original.json candidate.txt
No network requests, external uploads, automatic accusations or takedowns.
"""
import argparse
import json
from pathlib import Path
import re

from content_provenance import normalize_text


def read_text(path):
    text = Path(path).read_text(encoding='utf-8-sig')
    if Path(path).suffix == '.json':
        text = json.loads(text)['text']
    return text


def comparison(original, candidate, width=12):
    a, b = [re.sub(r'\W+', '', normalize_text(s)).lower() for s in (original, candidate)]
    def shingles(s):
        return set(s[i:i+width] for i in range(max(0, len(s)-width+1)))
    left, right = shingles(a), shingles(b)
    shared = left & right
    return {'method': f'{width}-character shingles after NFC, punctuation/whitespace removal and lowercase',
            'original_coverage': round(len(shared)/len(left), 4) if left else 0,
            'candidate_coverage': round(len(shared)/len(right), 4) if right else 0,
            'shared_shingles': len(shared),
            'interpretation': 'Textual overlap only. Shared facts, quotations and third-party source material require manual review. Paraphrases may be missed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original')
    parser.add_argument('candidate')
    args = parser.parse_args()
    print(json.dumps(comparison(read_text(args.original), read_text(args.candidate)), ensure_ascii=False, indent=2))
