#!/usr/bin/env python3
"""Register a local visual and generate its mechanical provenance fields."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import struct
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def chapter_image_folder(unit_id: str, used_in: list[str]) -> Path:
    """Return the image folder that mirrors the owning chapter's Markdown path."""
    if unit_id == "project":
        return ASSETS / "images" / "repo-images"
    for relative_path in used_in:
        chapter = ROOT / relative_path
        if not chapter.is_file() or chapter.suffix != ".md":
            continue
        try:
            chapter_relative = chapter.relative_to(ROOT / "knowledge")
        except ValueError:
            continue
        match = re.match(r"^---\n(.*?)\n---(?:\n|$)", chapter.read_text(encoding="utf-8"), re.DOTALL)
        if match and re.search(rf"^unit_id:\s*{re.escape(unit_id)}\s*$", match.group(1), re.MULTILINE):
            return ASSETS / "images" / chapter_relative.with_suffix("")
    raise ValueError(f"--used-in must include the knowledge chapter owned by {unit_id}")


def existing_manifest(unit_id: str) -> Path:
    matches = []
    for path in (ASSETS / "images").rglob("manifest.yml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("unit_id") == unit_id:
            matches.append(path)
    if len(matches) != 1:
        raise ValueError(f"expected one visual manifest for {unit_id}, found {len(matches)}")
    return matches[0]


def image_metadata(path: Path) -> tuple[str, int, int]:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return "image/png", width, height
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return "image/webp", width, height
        if chunk == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
            width = int.from_bytes(data[26:28], "little") & 0x3FFF
            height = int.from_bytes(data[28:30], "little") & 0x3FFF
            return "image/webp", width, height
        if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            return "image/webp", width, height
    raise ValueError("final visual must be a valid PNG or WebP image")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--title")
    parser.add_argument("--kind", choices=["diagram", "plot", "downloaded", "generated"])
    parser.add_argument("--file", help="Path relative to assets/")
    parser.add_argument("--creator")
    parser.add_argument("--license")
    parser.add_argument("--alt")
    parser.add_argument("--caption")
    parser.add_argument("--used-in", action="append", default=[])
    parser.add_argument("--source-record", action="append", default=[])
    parser.add_argument("--editable-source")
    parser.add_argument("--source-url")
    parser.add_argument("--direct-asset-url")
    parser.add_argument("--license-url")
    parser.add_argument("--generated-with")
    parser.add_argument("--prompt-file")
    parser.add_argument("--modified", action="store_true")
    parser.add_argument("--remove", action="store_true", help="Remove this visual record before deleting its asset.")
    args = parser.parse_args()
    if args.remove:
        try:
            manifest_path = existing_manifest(args.unit_id)
        except ValueError as error:
            parser.error(str(error))
        if not manifest_path.is_file():
            parser.error(f"visual manifest does not exist: {manifest_path.relative_to(ROOT)}")
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        before = manifest.get("visuals", [])
        manifest["visuals"] = [item for item in before if item.get("id") != args.id]
        if len(before) == len(manifest["visuals"]):
            parser.error(f"visual id is not registered: {args.id}")
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(manifest_path.relative_to(ROOT))
        return 0
    required = {"--title": args.title, "--kind": args.kind, "--file": args.file, "--creator": args.creator,
                "--license": args.license, "--alt": args.alt, "--caption": args.caption}
    missing = [name for name, value in required.items() if not value]
    if missing or not args.used_in:
        parser.error(f"missing required registration fields: {', '.join([*missing, *( [ '--used-in' ] if not args.used_in else [])])}")
    try:
        expected_folder = chapter_image_folder(args.unit_id, args.used_in)
    except ValueError as error:
        parser.error(str(error))
    if args.kind == "generated" and not args.prompt_file:
        parser.error("--prompt-file is required for a generated visual and must exist before registration")
    asset = ASSETS / args.file
    if not asset.is_file():
        parser.error(f"visual does not exist: assets/{args.file}")
    if asset.suffix.lower() not in {".png", ".webp"}:
        parser.error("final visual must use a .png or .webp extension; SVG is not allowed")
    try:
        media_type, width, height = image_metadata(asset)
    except ValueError as error:
        parser.error(str(error))
    if args.prompt_file and not (ASSETS / args.prompt_file).is_file():
        parser.error(f"prompt file does not exist: assets/{args.prompt_file}")
    if args.prompt_file and (ASSETS / args.prompt_file).parent != asset.parent / "source":
        parser.error("prompt file must be in the visual's chapter-local source/ directory")
    if args.kind == "downloaded":
        download_fields = {
            "--source-url": args.source_url,
            "--direct-asset-url": args.direct_asset_url,
            "--license-url": args.license_url,
        }
        missing_download = [name for name, value in download_fields.items() if not value]
        if missing_download:
            parser.error(f"downloaded visual requires provenance fields: {', '.join(missing_download)}")
        invalid_urls = [name for name, value in download_fields.items() if not value.startswith("https://")]
        if invalid_urls:
            parser.error(f"downloaded visual provenance URLs must use HTTPS: {', '.join(invalid_urls)}")
    if asset.parent != expected_folder:
        parser.error(f"visual must be directly under {expected_folder.relative_to(ROOT)}/")
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
        "media_type": media_type,
        "width": width,
        "height": height,
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
