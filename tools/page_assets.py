"""Render widget assets only where their HTML is present; never mutate build config."""
from html.parser import HTMLParser
from urllib.parse import urlsplit


class WidgetMarkers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = set()
        self.ids = set()
        self.classes = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.attributes.update(values)
        self.ids.add(values.get("id"))
        self.classes.update((values.get("class") or "").split())

    handle_startendtag = handle_starttag


def needed_assets(html, source):
    markers = WidgetMarkers()
    markers.feed(html)
    attributes, ids, classes = markers.attributes, markers.ids, markers.classes
    tools = bool(attributes & {"data-archive-compare", "data-archive-finder"})
    atlas = bool(ids & {"acupoint-controls", "acupoint-discovery"}) or "acupoint-region" in classes
    daily = bool(attributes & {"data-daily-km", "data-daily-km-topics"})
    return {
        "assets/acupoint-3d/launch.js": "data-acupoint-3d" in attributes,
        "assets/acupoint-3d/map.css": "data-acupoint-3d" in attributes,
        "assets/archive-tools/search-core.js": tools,
        "assets/archive-tools/ai-client.js": "data-archive-finder" in attributes,
        "assets/archive-tools/tools.js": tools,
        "assets/archive-tools/tools.css": tools,
        "assets/donguisusebowon/reader.js": "dsb-reader" in ids,
        "assets/donguisusebowon/reader.css": "dsb-reader" in ids,
        "assets/donguibogam/bootstrap.js": "dgb-reader" in ids,
        "assets/donguibogam/reader.css": "dgb-reader" in ids,
        "assets/acupoint-atlas/explorer.js": atlas,
        "assets/acupoint-atlas/discovery.js": "acupoint-discovery" in ids,
        "assets/acupoint-atlas/explorer.css": atlas,
        "assets/learning/learning.js": "data-learning-room" in attributes,
        "assets/learning/learning.css": "data-learning-room" in attributes,
        "assets/daily-korean-medicine/reader-core.js": daily,
        "assets/daily-korean-medicine.js": "data-daily-km" in attributes,
        "assets/daily-korean-medicine/special.js": "data-daily-km-topics" in attributes,
        "stylesheets/korean-medicine-guide.css": source == "korean-medicine-guide/index.md",
    }


def on_page_context(context, *, page, config, nav):
    # Instant navigation keeps a shared document. Retain all assets if enabled,
    # so a later widget page still has its subscribers and styles available.
    if "navigation.instant" in config["theme"].get("features", []):
        return context
    needed = needed_assets(page.content, page.file.src_uri)
    rendered_config = dict(config)
    for key in ("extra_javascript", "extra_css"):
        rendered_config[key] = [
            asset for asset in config[key]
            if needed.get(urlsplit(asset if isinstance(asset, str) else asset.path).path, True)
        ]
    context["config"] = rendered_config
    return context
