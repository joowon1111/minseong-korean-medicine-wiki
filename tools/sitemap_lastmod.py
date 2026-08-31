"""Replace MkDocs' build-date sitemap values with per-document Git dates."""

from __future__ import annotations

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse


SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def _repository_root(config: object) -> Path:
    config_file = getattr(config, "config_file_path", None)
    if config_file:
        return Path(config_file).resolve().parent
    return Path.cwd().resolve()


def _git_document_dates(repository_root: Path, docs_dir: Path) -> dict[str, str]:
    """Return the latest commit date for each document, newest commit first."""

    docs_relative = docs_dir.relative_to(repository_root).as_posix()
    command = [
        "git",
        "log",
        "--format=%x1e%cI",
        "--name-only",
        "--no-renames",
        "--",
        docs_relative,
    ]
    completed = subprocess.run(
        command,
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    dates: dict[str, str] = {}
    for block in completed.stdout.split("\x1e"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        commit_date, *paths = lines
        for path in paths:
            if path.endswith(".md"):
                dates.setdefault(Path(path).as_posix(), commit_date)

    return dates


def _source_document(
    location: str,
    *,
    site_url: str,
    docs_dir: Path,
) -> Path | None:
    parsed_location = urlparse(location)
    parsed_site = urlparse(site_url)

    if parsed_location.netloc != parsed_site.netloc:
        return None

    site_path = parsed_site.path.rstrip("/")
    page_path = unquote(parsed_location.path)
    if site_path and page_path.startswith(site_path + "/"):
        page_path = page_path[len(site_path) :]

    relative = page_path.strip("/")
    if not relative:
        candidates = [docs_dir / "index.md"]
    else:
        candidates = [docs_dir / relative / "index.md", docs_dir / f"{relative}.md"]

    return next((candidate for candidate in candidates if candidate.is_file()), None)


def update_sitemap(config: object) -> tuple[int, int]:
    """Update sitemap lastmod values and return (updated, total) counts."""

    repository_root = _repository_root(config)
    site_dir = Path(config["site_dir"]).resolve()
    docs_dir = Path(config["docs_dir"]).resolve()
    site_url = str(config["site_url"])
    sitemap_path = site_dir / "sitemap.xml"

    if not sitemap_path.is_file():
        raise RuntimeError(f"Sitemap was not generated: {sitemap_path}")

    git_dates = _git_document_dates(repository_root, docs_dir)
    if not git_dates:
        raise RuntimeError(
            "No Git document history was found. In CI, checkout with fetch-depth: 0."
        )

    ET.register_namespace("", SITEMAP_NAMESPACE)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespace = {"sitemap": SITEMAP_NAMESPACE}

    updated = 0
    entries = root.findall("sitemap:url", namespace)
    for entry in entries:
        location_element = entry.find("sitemap:loc", namespace)
        if location_element is None or not location_element.text:
            continue

        source = _source_document(
            location_element.text,
            site_url=site_url,
            docs_dir=docs_dir,
        )
        if source is None:
            continue

        git_path = source.relative_to(repository_root).as_posix()
        commit_date = git_dates.get(git_path)
        if not commit_date:
            continue

        lastmod = entry.find("sitemap:lastmod", namespace)
        if lastmod is None:
            lastmod = ET.SubElement(entry, f"{{{SITEMAP_NAMESPACE}}}lastmod")
        lastmod.text = commit_date
        updated += 1

    if updated != len(entries):
        raise RuntimeError(
            f"Only {updated} of {len(entries)} sitemap URLs mapped to Git-tracked documents."
        )

    ET.indent(tree, space="  ")
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    return updated, len(entries)


def on_post_build(config: object, **_: object) -> None:
    """MkDocs hook: correct sitemap dates after every build, including gh-deploy."""

    updated, total = update_sitemap(config)
    print(f"Sitemap lastmod: updated {updated}/{total} URLs from Git history")
