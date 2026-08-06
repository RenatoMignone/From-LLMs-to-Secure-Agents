#!/usr/bin/env python3
"""Register a local visual and generate its mechanical provenance fields."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--kind", choices=["diagram", "plot", "downloaded", "generated"], required=True)
    parser.add_argument("--file", required=True, help="Path relative to assets/")
    parser.add_argument("--creator", required=True)
    parser.add_argument("--license", required=True)
    parser.add_argument("--alt", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--used-in", action="append", required=True)
    parser.add_argument("--source-record", action="append", default=[])
    parser.add_argument("--editable-source")
    parser.add_argument("--source-url")
    parser.add_argument("--direct-asset-url")
    parser.add_argument("--license-url")
    parser.add_argument("--generated-with")
    parser.add_argument("--prompt-file")
    parser.add_argument("--modified", action="store_true")
    args = parser.parse_args()
    asset = ASSETS / args.file
    if not asset.is_file():
        parser.error(f"visual does not exist: assets/{args.file}")
    expected_folder = "repo-images" if args.unit_id == "project" else args.unit_id.lower()
    if asset.parent.name != expected_folder:
        parser.error(f"visual must be directly under assets/images/{expected_folder}/")
    manifest_path = asset.parent / "manifest.yml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {
        "schema_version": 1,
        "unit_id": args.unit_id,
        "visuals": [],
    }
    entry = {
        "id": args.id,
        "title": args.title,
        "kind": args.kind,
        "file": args.file,
        "editable_source": args.editable_source,
        "creator": args.creator,
        "source_url": args.source_url,
        "direct_asset_url": args.direct_asset_url,
        "license": args.license,
        "license_url": args.license_url,
        "accessed": dt.date.today().isoformat(),
        "generated_with": args.generated_with,
        "prompt_file": args.prompt_file,
        "modified": args.modified,
        "sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "alt": args.alt,
        "caption": args.caption,
        "source_records": list(dict.fromkeys(args.source_record)),
        "used_in": list(dict.fromkeys(args.used_in)),
    }
    manifest["visuals"] = [item for item in manifest.get("visuals", []) if item.get("id") != args.id]
    manifest["visuals"].append(entry)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    index_path = ASSETS / "attribution.yml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    manifest_relative = manifest_path.relative_to(ASSETS).as_posix()
    index["manifests"] = sorted(set([*index.get("manifests", []), manifest_relative]))
    index_path.write_text(yaml.safe_dump(index, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(manifest_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
