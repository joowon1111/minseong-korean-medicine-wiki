"""Publish only the public server URL. Credentials never enter the static site."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit


def public_endpoint(value):
    if not value:
        return None
    u = urlsplit(value)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.port not in (None, 443):
        raise ValueError('ARCHIVE_AI_URL must be an HTTPS server base URL without credentials, query or fragment')
    return value.rstrip('/')


def main():
    target = Path('docs/assets/archive-tools/ai-config.json')
    target.write_text(json.dumps({'schema': 1, 'endpoint': public_endpoint(os.getenv('ARCHIVE_AI_URL', '').strip())}, ensure_ascii=False) + '\n')
    print('Archive AI public configuration generated')


if __name__ == '__main__':
    main()
