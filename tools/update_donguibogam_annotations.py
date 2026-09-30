"""Rebuild search annotations without changing imported text or public record IDs."""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/assets/donguibogam"


def main():
    annotations = json.loads((ROOT / "data/donguibogam/search-annotations.json").read_text())
    manifest = json.loads((BASE / "manifest.json").read_text())
    # Match explicit Korean titles in existing herb documents; never guess a slug.
    herb_links = {}
    for path in sorted((ROOT / "docs/herbs").glob("*.md")):
        raw = path.read_text(encoding="utf-8-sig")
        if not raw.startswith("---"):
            continue
        title = str((yaml.safe_load(raw.split("---", 2)[1]) or {}).get("title", ""))
        for name in re.findall(r"[가-힣]{2,8}", title.split("(", 1)[0]):
            herb_links.setdefault(name, "/herbs/" + path.stem + "/")
    changed = linked = 0
    for group in manifest["groups"].values():
        path = BASE / group["file"]
        rows = json.loads(path.read_text())
        parent = None
        for row in rows:
            title = unicodedata.normalize("NFKC", row["title"])
            names = annotations["names"].get(title, "").split()
            old = list(row["aliases"])
            row["aliases"] = list(dict.fromkeys(old + names))
            for name in names:
                url = herb_links.get(name)
                if url and not any(link["url"] == url for link in row["links"]):
                    row["links"].append({"title": name, "url": url})
                    linked += 1
            if title in annotations["part_names"] and parent and parent["source"] == row["source"]:
                row["context_title"] = parent["title"]
                part = annotations["part_names"][title]
                labels = [name + " " + part for name in parent["aliases"]]
                row["aliases"] = list(dict.fromkeys(row["aliases"] + labels))
            elif title not in annotations["part_names"]:
                parent = row if row["aliases"] else None
            changed += old != row["aliases"]
        path.write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + "\n")
        group["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest["annotations"] = annotations["note"]
    guide = json.loads((ROOT / "data/donguibogam/volume-guide.json").read_text())
    by_number = {v["number"]: v for v in guide["volumes"]}
    for scan in manifest["scans"]:
        scan.update(by_number[scan["number"]])
        scan["title"] = f"{scan['division']} 권{scan['volume']}"
        scan["evidence_image"] = scan["thumbnail"].replace("/page1-", f"/page{scan['evidence_page']}-")
    manifest["volume_guide_source"] = guide["source"]
    (BASE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n")
    (ROOT / "data/donguibogam/source-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated Korean aliases for {changed} rows; added {linked} herb context links.")


if __name__ == "__main__":
    main()
