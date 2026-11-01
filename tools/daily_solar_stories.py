"""Reuse the canonical 24 solar-term stories in the daily reader, at build time."""
import html
import re
from pathlib import Path
from urllib.parse import urljoin

import markdown


def story_templates(docs_dir):
    source = (Path(docs_dir) / "daily-korean-medicine/solar-terms.md").read_text(encoding="utf-8")
    sections = re.findall(r"(?ms)^### ([^\n]+ — [^\n]+?) \{#([a-z-]+)\}\n(.*?)(?=^#{1,3} |\Z)", source)
    if len(sections) != 24:
        raise ValueError("The daily reader requires all 24 canonical solar-term stories")
    templates = []
    for title, anchor, body in sections:
        rendered = markdown.markdown(body, extensions=["extra"])
        # Resolve links relative to the canonical Markdown source.
        def resolve(match):
            url = html.unescape(match[1])
            if not re.match(r"^[a-z]+:|^//", url, re.I):
                url = urljoin("/daily-korean-medicine/solar-terms.md", url)
                url = re.sub(r"/index\.md(?=[?#]|$)", "/", url)
                url = re.sub(r"\.md(?=[?#]|$)", "/", url)
            return 'href="' + html.escape(url, quote=True) + '"'
        rendered = re.sub(r'href="([^"]*)"', resolve, rendered)
        templates.append('<template id="daily-term-story-' + anchor + '"><h3>' +
                         html.escape(title) + '</h3>' + rendered + '</template>')
    return "\n".join(templates)


def on_page_content(html, *, page, config, files):
    if page.file.src_uri != "daily-korean-medicine/index.md":
        return html
    return html + "\n" + story_templates(config["docs_dir"])
