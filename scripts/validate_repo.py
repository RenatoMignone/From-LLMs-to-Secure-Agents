#!/usr/bin/env python3
"""Validate curriculum structure, links, source records, and visual ownership."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def text_files() -> list[Path]:
    extensions = {".md", ".yml", ".yaml", ".py"}
    ignored = {".git", "tmp"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in extensions
        and not ignored.intersection(path.relative_to(ROOT).parts)
    ]


required_root = [
    "AGENTS.md",
    "README.md",
    "PROJECT_STATUS.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "docs/autonomous-workflow.md",
    "assets/attribution.yml",
]
for relative in required_root:
    if not (ROOT / relative).is_file():
        fail(f"missing required file: {relative}")

for directory in [ROOT / "knowledge", *[p for p in (ROOT / "knowledge").rglob("*") if p.is_dir()]]:
    for name in ("AGENTS.md", "chapter-plan.md"):
        if not (directory / name).is_file():
            fail(f"missing {name}: {directory.relative_to(ROOT)}")

roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
unit_ids = re.findall(r"^\d+\. `(P[12]-[^`]+)`", roadmap, re.MULTILINE)
if len(unit_ids) != len(set(unit_ids)):
    fail("ROADMAP.md contains duplicate unit identifiers")
pass_two = next((index for index, unit in enumerate(unit_ids) if unit.startswith("P2-")), None)
if pass_two is None or any(unit.startswith("P1-") for unit in unit_ids[pass_two:]):
    fail("ROADMAP.md does not keep all Pass 1 units before Pass 2")

status = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
next_match = re.search(r"Next recommended unit: `([^`]+)`", status)
if not next_match or next_match.group(1) not in unit_ids:
    fail("PROJECT_STATUS.md next unit is missing from ROADMAP.md")

markdown_link = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
markdown_image = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
attribution = (ROOT / "assets/attribution.yml").read_text(encoding="utf-8")

for path in text_files():
    content = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)
    if "\u2014" in content:
        fail(f"em dash: {relative}")
    for number, line in enumerate(content.splitlines(), 1):
        if line.endswith((" ", "\t")):
            fail(f"trailing whitespace: {relative}:{number}")

    if path.suffix != ".md":
        continue
    for raw in markdown_link.findall(content):
        target = raw.strip().removeprefix("<").removesuffix(">").split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            fail(f"broken internal link: {relative} -> {target}")
    for raw in markdown_image.findall(content):
        target = raw.strip().removeprefix("<").removesuffix(">").split("#", 1)[0]
        if target.startswith(("http://", "https://")):
            fail(f"hotlinked image: {relative} -> {target}")
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            fail(f"missing image: {relative} -> {target}")
            continue
        try:
            asset_relative = resolved.relative_to(ROOT / "assets")
        except ValueError:
            fail(f"chapter image is outside assets/: {relative} -> {target}")
            continue
        if asset_relative.as_posix() not in attribution:
            fail(f"image missing from assets/attribution.yml: {asset_relative}")

source_keys = {
    "id",
    "title",
    "authors_or_organization",
    "source_type",
    "canonical_url",
    "accessed",
    "last_verified",
    "status",
    "claims_supported",
    "limitations",
    "unit_ids",
    "used_in",
}
source_ids: set[str] = set()


def yaml_list(content: str, key: str) -> list[str]:
    match = re.search(rf"^{re.escape(key)}:\s*\n((?:  - .*\n?)*)", content, re.MULTILINE)
    if not match:
        return []
    return [line.removeprefix("  - ").strip() for line in match.group(1).splitlines()]


for record in (ROOT / "sources").glob("*.yml"):
    if record.name == "source-template.yml":
        continue
    content = record.read_text(encoding="utf-8")
    keys = {
        match.group(1)
        for match in re.finditer(r"^([a-z][a-z0-9_]*):", content, re.MULTILINE)
    }
    for missing in sorted(source_keys - keys):
        fail(f"source record missing {missing}: {record.relative_to(ROOT)}")
    source_id_match = re.search(r"^id:\s*(\S+)", content, re.MULTILINE)
    if not source_id_match:
        continue
    source_id = source_id_match.group(1)
    if source_id in source_ids:
        fail(f"duplicate source id: {source_id}")
    source_ids.add(source_id)
    if record.stem != source_id:
        fail(f"source id does not match filename: {record.relative_to(ROOT)}")
    for used_in in yaml_list(content, "used_in"):
        if not (ROOT / used_in).exists():
            fail(f"source record has missing used_in path: {record.name} -> {used_in}")
    for unit_id in yaml_list(content, "unit_ids"):
        if unit_id not in unit_ids:
            fail(f"source record has unknown unit id: {record.name} -> {unit_id}")

asset_files = [
    path
    for path in (ROOT / "assets").rglob("*")
    if path.is_file()
    and path.name not in {"AGENTS.md", "attribution.yml"}
    and "source" not in path.relative_to(ROOT / "assets").parts
]
for asset in asset_files:
    relative = asset.relative_to(ROOT / "assets").as_posix()
    if relative not in attribution:
        fail(f"unregistered final asset: assets/{relative}")

chapter_files = [
    path
    for path in (ROOT / "knowledge").rglob("*.md")
    if path.name not in {"AGENTS.md", "chapter-plan.md"}
]
for chapter in chapter_files:
    content = chapter.read_text(encoding="utf-8")
    for key in ("unit_id:", "source_records:", "visual_assets:", "example_paths:", "pass:"):
        if key not in content:
            fail(f"chapter front matter missing {key} {chapter.relative_to(ROOT)}")

if ERRORS:
    print("Validation failed:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(
    f"Validation passed: {len(unit_ids)} roadmap units, "
    f"{len(chapter_files)} chapters, {len(asset_files)} final visuals, "
    f"{len(list((ROOT / 'sources').glob('*.yml'))) - 1} source records."
)
