from pathlib import Path
import shutil, sys, datetime

root = Path(__file__).resolve().parent
repo = root
cfg = repo / "mkdocs.yml"
status = repo / "APPLY_44_YAML_FIX_STATUS.txt"

try:
    if not cfg.exists():
        raise RuntimeError("mkdocs.yml not found")

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = repo / f"mkdocs_44_yaml_fix_backup_{ts}.yml"
    shutil.copy2(cfg, backup)

    text = cfg.read_text(encoding="utf-8-sig")
    lines = text.splitlines()

    atlas_path = "acupoint-network/standard-atlas.md"
    index_path = "acupoint-network/index.md"

    # Remove the malformed/current atlas nav entry only.
    lines = [line for line in lines if atlas_path not in line]

    # Find the existing acupoint-network/index.md nav item.
    target_i = None
    for i, line in enumerate(lines):
        if index_path in line:
            target_i = i
            break
    if target_i is None:
        raise RuntimeError("Could not find acupoint-network/index.md in mkdocs.yml nav")

    target_line = lines[target_i]
    indent = target_line[:len(target_line)-len(target_line.lstrip())]

    # Insert immediately before the existing acupoint-network item, as a true sibling.
    atlas_line = f"{indent}- WHO 표준 361경혈 아틀라스: {atlas_path}"
    lines.insert(target_i, atlas_line)

    new_text = "\n".join(lines) + "\n"

    # Parse before saving final file.
    try:
        import yaml
    except Exception as e:
        raise RuntimeError("PyYAML is not installed. requirements.txt build normally includes it.") from e

    parsed = yaml.safe_load(new_text)
    if not isinstance(parsed, dict):
        raise RuntimeError("YAML parsed but root is not a mapping")

    # Basic uniqueness checks.
    if new_text.count(atlas_path) != 1:
        raise RuntimeError(f"Atlas path appears {new_text.count(atlas_path)} times; expected 1")

    cfg.write_text(new_text, encoding="utf-8")

    status.write_text(
        "COMPLETE\n"
        f"Backup: {backup.name}\n"
        f"Inserted atlas before: {index_path}\n"
        f"Indent spaces: {len(indent)}\n"
        "YAML parse: PASS\n",
        encoding="utf-8"
    )

    print("STANDARD ACUPOINT ATLAS NAV 44 YAML FIX COMPLETE")
    print("YAML parse: PASS")
    print(f"Atlas sibling indentation: {len(indent)} spaces")
    print(f"Backup: {backup.name}")

except Exception as e:
    status.write_text("FAILED\n" + repr(e) + "\n", encoding="utf-8")
    print("ERROR:", e)
    sys.exit(1)
