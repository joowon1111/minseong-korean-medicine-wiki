"""Build-time reader navigation and public, page-sized machine-readable documents.

Exports use rendered article content, never arbitrary front matter or source files.
No browser JavaScript, tracking, clinical inference, or external requests are needed.
"""

from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote, urljoin, urlsplit

from mkdocs.exceptions import PluginError


_page_index = {}
PAGE_TYPES = {"WebPage", "MedicalWebPage", "FAQPage", "CollectionPage", "AboutPage"}
BLOCKS = {"p", "div", "li", "tr", "blockquote", "pre", "h1", "h2", "h3", "h4", "h5", "h6"}


def plain(value):
    return re.sub(r"\s+", " ", value).strip()


def page_language(page):
    """Only the explicitly supported English override changes the Korean default."""
    return "en" if page.meta.get("lang") == "en" else "ko-KR"


def document_title(page):
    for field in ("search_title", "title"):
        title = page.meta.get(field)
        if isinstance(title, str) and title.strip():
            return plain(title)
    return page.title


def reader_tools(page, config):
    """Opt-in provenance and citation controls; never infer an author/reviewer."""
    if page.meta.get("reader_tools") is not True:
        return ""
    root = config["site_url"]
    url = escape(page.canonical_url, quote=True)
    title = escape(document_title(page), quote=True)
    guide = escape(urljoin(root, "guide/"), quote=True)
    return (
        f'<aside class="archive-citation" aria-label="문서 출처와 공유" '
        f'data-archive-citation data-citation-title="{title}" data-citation-url="{url}">'
        f'<p>운영: <a href="{guide}#publisher">민성한의원</a> · '
        f'<a href="{guide}citation-policy/">출처·인용 원칙</a> · '
        f'<a href="{guide}editorial-policy/">편집 원칙</a></p>'
        f'<div class="archive-citation-actions"><a href="{url}">문서 고정 주소</a>'
        '<button type="button" data-copy-citation="url" hidden>주소 복사</button>'
        '<button type="button" data-copy-citation="citation" hidden>제목·출처 복사</button></div>'
        '<p data-citation-status role="status" aria-live="polite" hidden></p>'
        '<textarea data-citation-fallback aria-label="복사할 제목·출처 또는 주소" readonly hidden></textarea>'
        '</aside>'
    )


def http_url(value, base):
    if not isinstance(value, str) or not value or re.search(r"[\x00-\x20\\]", value):
        return None
    try:
        target = urljoin(base, value)
        parts = urlsplit(target)
        if parts.scheme in {"http", "https"} and parts.hostname and not parts.username and not parts.password:
            return target
    except ValueError:
        pass
    return None


class Article(HTMLParser):
    """Extract text and real heading IDs while excluding scripts and hidden nodes."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.headings = []
        self.links = []
        self.types = set()
        self._stack = []
        self._heading = None
        self._script = None
        self.section_marks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        hidden = (any(self._stack) or tag in {"script", "style", "template"}
                  or "hidden" in attrs or attrs.get("aria-hidden") == "true"
                  or "headerlink" in attrs.get("class", "").split())
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._script = []
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self._stack.append(hidden)
        if hidden:
            return
        if tag in BLOCKS or tag in {"br", "td", "th"}:
            self.text.append("\n" if tag in BLOCKS or tag == "br" else "\t")
        if tag in {"h2", "h3"} and attrs.get("id"):
            self.section_marks.append({"start": len(self.text), "links": len(self.links)})
            self._heading = {"level": int(tag[1]), "id": attrs["id"], "text": []}
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in {"br", "hr", "img", "input", "link", "meta", "source", "wbr", "area", "base", "col", "embed", "param", "track"}:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)
        if any(self._stack):
            return
        self.text.append(data)
        if self._heading is not None:
            self._heading["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            try:
                self._collect_types(json.loads("".join(self._script)))
            except (ValueError, TypeError):
                pass  # Existing editorial markup is preserved, not rewritten.
            self._script = None
        if tag in {"h2", "h3"} and self._heading is not None:
            self._heading["text"] = plain("".join(self._heading["text"]))
            self.headings.append(self._heading)
            self.section_marks[-1]["heading"] = self._heading
            self.section_marks[-1]["body"] = len(self.text)
            self._heading = None
        if self._stack:
            self._stack.pop()
        if tag in BLOCKS:
            self.text.append("\n")

    def _collect_types(self, node):
        if isinstance(node, list):
            for item in node:
                self._collect_types(item)
        elif isinstance(node, dict):
            types = node.get("@type", [])
            self.types.update([types] if isinstance(types, str) else
                              [item for item in types if isinstance(item, str)] if isinstance(types, list) else [])
            self._collect_types(node.get("@graph", []))

    def body_text(self):
        return "\n".join(line for part in "".join(self.text).splitlines() if (line := plain(part)))

    def passages(self, url):
        """Export contiguous visible sections, without inferring citation support."""
        result = []
        for i, mark in enumerate(self.section_marks):
            heading = mark.get("heading")
            if not heading:
                continue
            following = self.section_marks[i + 1] if i + 1 < len(self.section_marks) else {}
            text = "".join(self.text[mark["body"]:following.get("start", len(self.text))])
            links = self.links[mark["links"]:following.get("links", len(self.links))]
            result.append({"title": heading["text"], "level": heading["level"],
                           "url": url + "#" + quote(heading["id"]),
                           "text": "\n".join(line for part in text.splitlines() if (line := plain(part))),
                           "links": sorted({target for link in links if (target := http_url(link, url))})})
        return result


def breadcrumb_items(page, files, config):
    root = config["site_url"]
    items = [{"name": "Home" if page_language(page) == "en" else "홈", "url": root}]
    for parent in reversed(PurePosixPath(page.file.src_uri).parents):
        if str(parent) == ".":
            continue
        source = (parent / "index.md").as_posix()
        file = files.get_file_from_path(source)
        if file and file.page and source != page.file.src_uri:
            items.append({"name": file.page.title, "url": urljoin(root, file.url)})
    if page.canonical_url != root:
        items.append({"name": page.title, "url": page.canonical_url})
    return items


def related_items(page, files, config):
    rows = page.meta.get("related_reading", [])
    if not isinstance(rows, list) or len(rows) > 4:
        raise PluginError(f"{page.file.src_uri}: related_reading must contain at most four documents")
    items, seen = [], set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("document"), str):
            raise PluginError(f"{page.file.src_uri}: invalid related_reading entry")
        source = row["document"]
        file = files.get_file_from_path(source)
        if (not file or not file.page or source == page.file.src_uri
                or source in seen or not isinstance(row.get("reason"), str) or not row["reason"].strip()):
            raise PluginError(f"{page.file.src_uri}: invalid or duplicate related document: {source}")
        seen.add(source)
        items.append({"title": file.page.title, "url": urljoin(config["site_url"], file.url), "reason": row["reason"]})
    return items


def on_pre_build(config):
    _page_index.clear()


def on_page_content(html, page, config, files):
    article = Article()
    article.feed(html)
    breadcrumbs = breadcrumb_items(page, files, config)
    related = related_items(page, files, config)
    english = page_language(page) == "en"
    prefix = ""
    if len(breadcrumbs) > 1:
        links = [f'<a href="{escape(item["url"], quote=True)}">{escape(item["name"])}</a>' for item in breadcrumbs[:-1]]
        links.append(f'<span aria-current="page">{escape(page.title)}</span>')
        prefix += '<nav class="archive-breadcrumbs" aria-label="' + ("Breadcrumb" if english else "현재 문서 위치") + '">' + ' <span aria-hidden="true">›</span> '.join(links) + '</nav>'
    quick = []
    labels = (("Safety", ("safety", "precautions")), ("Sources", ("sources", "references"))) if english else (
        ("주의사항 먼저 보기", ("위험신호", "안전", "주의", "먼저 확인", "금기")),
        ("근거·출처 확인", ("참고", "출처", "references", "reference")))
    for label, terms in labels:
        match = next((heading for heading in article.headings
                      if any(term in heading["text"].lower() for term in terms)), None)
        if match:
            quick.append(f'<a href="#{escape(quote(match["id"]), quote=True)}">{label}</a>')
    if quick:
        prefix += '<div class="archive-reading-tools">'
        prefix += '<nav aria-label="' + ("Article shortcuts" if english else "본문 빠른 이동") + '">' + '\n'.join(quick) + '</nav>'
        prefix += '</div>'
    suffix = ""
    if related:
        cards = ''.join(f'<a class="archive-related-card" href="{escape(item["url"], quote=True)}"><strong>{escape(item["title"])}</strong><span>{escape(item["reason"])}</span></a>' for item in related)
        suffix = '<aside class="archive-related" aria-label="이어서 읽기"><p><strong>이어서 읽기</strong></p><div class="archive-related-grid">' + cards + '</div></aside>'
    document_path = 'assets/ai/pages/' + PurePosixPath(page.file.dest_uri).with_suffix('.json').as_posix()
    page.archive_discovery = {
        "article": article, "breadcrumbs": breadcrumbs, "related": related,
        "document_path": document_path,
    }
    return prefix + html + suffix + reader_tools(page, config)


def json_text(value):
    # JSON-LD is embedded in HTML: literal closing script tags must never escape.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def write_document(site_dir, relative, value):
    target = (Path(site_dir) / relative).resolve()
    if not target.is_relative_to(Path(site_dir).resolve()):
        raise PluginError("Machine-readable output must stay within site_dir")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json_text(value) + "\n", encoding="utf-8")


def on_post_page(output, page, config):
    data = getattr(page, "archive_discovery", None)
    if not data:
        return output
    article = data["article"]
    url = page.canonical_url
    root = config["site_url"]
    document_url = urljoin(root, quote(data["document_path"]))
    title = document_title(page)
    language = page_language(page)
    description = page.meta.get("description")
    description = description.strip() if isinstance(description, str) else ""
    graph = []
    if not (article.types & PAGE_TYPES):
        node = {"@type": "MedicalWebPage" if page.file.src_uri.startswith(("conditions/", "symptoms/", "herbs/", "formulas/", "authority/")) else "WebPage",
                "@id": url + "#webpage", "url": url, "name": title,
                "inLanguage": language, "isPartOf": {"@id": root + "#website"}}
        if description:
            node["description"] = description
        if data["related"]:
            node["relatedLink"] = [item["url"] for item in data["related"]]
        if len(data["breadcrumbs"]) > 1:
            node["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(node)
    if "BreadcrumbList" not in article.types and len(data["breadcrumbs"]) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": item["name"], "item": item["url"]}
            for i, item in enumerate(data["breadcrumbs"], 1)]})
    if url == root and "WebSite" not in article.types:
        graph.append({"@type": "WebSite", "@id": root + "#website", "url": root,
                      "name": config["site_name"], "inLanguage": "ko-KR"})
    export_title = "Article text (JSON)" if language == "en" else "문서 읽기 자료 (JSON)"
    head = '<link rel="alternate" type="application/json" title="' + export_title + '" href="' + escape(document_url, quote=True) + '">\n'
    if graph:
        head += '<script type="application/ld+json">' + json_text({"@context": "https://schema.org", "@graph": graph}) + '</script>\n'
    for name, value in {"og:title": title, "og:url": url, "og:type": "website", "og:site_name": config["site_name"], "og:description": description}.items():
        if value and f'property="{name}"' not in output:
            head += f'<meta property="{name}" content="{escape(value, quote=True)}">\n'
    links = sorted({target for link in article.links if (target := http_url(link, url))})
    payload = {"schema_version": "1.0", "url": url, "title": title,
               "language": language, "description": description,
               "text": article.body_text(),
               "sections": article.passages(url),
               "headings": [{"level": h["level"], "title": h["text"], "url": url + "#" + quote(h["id"])} for h in article.headings],
               "links": links, "related_reading": data["related"],
               "interpretation": "Public article text and navigation only; links do not establish clinical equivalence or treatment recommendations."}
    write_document(config["site_dir"], data["document_path"], payload)
    _page_index[url] = {"url": url, "title": title, "document": document_url}
    del page.archive_discovery  # Do not retain every article's parsed text after rendering.
    if language == "en":
        # The article is English; the shared Korean menus remain Korean.
        output = re.sub(r'(<html\b[^>]*\blang=")[^"]*(")', r'\g<1>en\2', output, count=1)
        output = re.sub(r'<body\b', '<body lang="ko"', output, count=1)
        output = re.sub(r'<article\b', '<article lang="en"', output, count=1)
        output = output.replace('<nav class="md-nav md-nav--secondary"', '<nav lang="en" class="md-nav md-nav--secondary"', 1)
    return output.replace('</head>', head + '</head>', 1)


def on_post_build(config):
    write_document(config["site_dir"], "assets/ai/page-index.json", {
        "schema_version": "1.0", "base_url": config["site_url"],
        "pages": [_page_index[url] for url in sorted(_page_index)]})

