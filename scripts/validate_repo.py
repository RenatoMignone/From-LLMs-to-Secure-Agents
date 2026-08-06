#!/usr/bin/env python3
"""Validate guide structure, state, chapters, evidence, and visual provenance."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as error:
    print(f"Missing validation dependency: {error.name}. Run: pip install -r requirements-dev.txt")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
FORMAT_CHECKER = FormatChecker()
STATE_NAMES = {"researching", "drafting", "building-assets", "validating", "review"}


@dataclass(frozen=True)
class Unit:
    unit_id: str
    title: str
    chapter_path: str
    plan_path: str
    pass_name: str
    learning_path: str


def fail(message: str) -> None:
    ERRORS.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        fail(f"invalid YAML: {relative(path)}: {error}")
        return None


def load_schema(name: str) -> dict[str, Any]:
    path = ROOT / "schemas" / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"invalid schema: {relative(path)}: {error}")
        return {}


def validate_schema(data: Any, schema_name: str, label: str) -> None:
    schema = load_schema(schema_name)
    if not schema:
        return
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "root"
        fail(f"schema error: {label}:{location}: {error.message}")


def front_matter(path: Path) -> dict[str, Any] | None:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        fail(f"missing YAML front matter: {relative(path)}")
        return None
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        fail(f"invalid front matter: {relative(path)}: {error}")
        return None
    if not isinstance(value, dict):
        fail(f"front matter is not a mapping: {relative(path)}")
        return None
    return value


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def image_metadata(path: Path) -> tuple[str, int, int]:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return "image/png", width, height
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            return "image/webp", 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if chunk == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
            return "image/webp", int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
        if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return "image/webp", (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    raise ValueError("not a valid PNG or WebP image")


def numbered_directory(parent: Path, number: int) -> Path | None:
    matches = sorted(path for path in parent.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}-"))
    if len(matches) != 1:
        fail(f"expected one {number:02d}-* directory under {relative(parent)}")
        return None
    return matches[0]


def child_learning_paths(plan_text: str) -> dict[int, str]:
    paths: dict[int, str] = {}
    learning_path = "main"
    for line in plan_text.splitlines():
        marker = line.strip().lower()
        if marker in {"deep dive:", "deep dives:"} or "optional deep-dive branch" in marker:
            learning_path = "deep-dive"
        elif marker in {"main path:", "main path resumes:"}:
            learning_path = "main"
        match = re.match(r"^\s*(\d+)\. `[^`]+`$", line)
        if match:
            paths[int(match.group(1))] = learning_path
    return paths


def resolve_units() -> list[Unit]:
    roadmap_path = ROOT / "ROADMAP.md"
    roadmap = roadmap_path.read_text(encoding="utf-8")
    entries = re.findall(r"^\d+\. `(P[12]-([0-9-]+))` (.+)$", roadmap, re.MULTILINE)
    units: list[Unit] = []
    seen: set[str] = set()
    for unit_id, number_text, title in entries:
        if unit_id in seen:
            fail(f"duplicate roadmap unit: {unit_id}")
            continue
        seen.add(unit_id)
        numbers = [int(part) for part in number_text.split("-")]
        top = numbered_directory(ROOT / "knowledge", numbers[0])
        if top is None:
            continue
        if len(numbers) == 2:
            directory, child_number = top, numbers[1]
        elif len(numbers) == 3:
            directory = numbered_directory(top, numbers[1])
            child_number = numbers[2]
            if directory is None:
                continue
        else:
            fail(f"unsupported unit identifier shape: {unit_id}")
            continue
        plan = directory / "chapter-plan.md"
        plan_text = plan.read_text(encoding="utf-8")
        match = re.search(rf"^\s*{child_number}\. `([^`]+)`$", plan_text, re.MULTILINE)
        if not match:
            fail(f"missing plan entry for {unit_id}: {relative(plan)}")
            continue
        filename = match.group(1)
        expected_filename = f"{child_number:02d}-{slugify(title)}.md"
        if filename != expected_filename:
            fail(f"roadmap and plan filename drift: {unit_id}: {filename} != {expected_filename}")
        units.append(Unit(
            unit_id,
            title,
            relative(directory / filename),
            relative(plan),
            "architecture" if unit_id.startswith("P1-") else "security",
            child_learning_paths(plan_text).get(child_number, "main"),
        ))
    planned = []
    for plan in (ROOT / "knowledge").rglob("chapter-plan.md"):
        planned.extend(re.findall(r"^\s*\d+\. `([0-9]{2}-[^`]+\.md)`$", plan.read_text(encoding="utf-8"), re.MULTILINE))
    if len(entries) != len(planned):
        fail(f"roadmap and plan counts differ: {len(entries)} != {len(planned)}")
    first_pass_two = next((index for index, unit in enumerate(units) if unit.pass_name == "security"), None)
    if first_pass_two is None or any(unit.pass_name == "architecture" for unit in units[first_pass_two:]):
        fail("Pass 1 units must all precede Pass 2 units")
    return units


def check_text_and_links() -> None:
    extensions = {".md", ".yml", ".yaml", ".py", ".json"}
    ignored = {".git", "tmp", "__pycache__"}
    markdown_link = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    markdown_image = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    html_link = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in extensions or ignored.intersection(path.relative_to(ROOT).parts):
            continue
        content = path.read_text(encoding="utf-8")
        if "\u2014" in content:
            fail(f"em dash: {relative(path)}")
        for number, line in enumerate(content.splitlines(), 1):
            if line.endswith((" ", "\t")):
                fail(f"trailing whitespace: {relative(path)}:{number}")
        if path.suffix != ".md":
            continue
        targets = list(markdown_link.findall(content)) + list(markdown_image.findall(content)) + list(html_link.findall(content))
        for raw in targets:
            target = raw.strip().removeprefix("<").removesuffix(">").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                fail(f"broken internal link: {relative(path)} -> {target}")
        for raw in markdown_image.findall(content):
            target = raw.strip().removeprefix("<").removesuffix(">").split("#", 1)[0]
            if target.startswith(("http://", "https://")) and path != ROOT / "README.md":
                fail(f"hotlinked content image: {relative(path)} -> {target}")


def check_planning_files() -> None:
    required_headings = {
        "Section purpose",
        "Learning outcomes",
        "Prerequisites",
        "Required concepts",
        "Concepts explicitly out of scope",
        "Recommended teaching order",
        "Required diagrams or visuals",
        "Sources",
        "Connections to later security chapters",
        "Open questions",
        "Completion criteria",
    }
    directories = [ROOT / "knowledge", *(path for path in (ROOT / "knowledge").rglob("*") if path.is_dir())]
    for directory in directories:
        for name in ("AGENTS.md", "chapter-plan.md"):
            if not (directory / name).is_file():
                fail(f"missing {name}: {relative(directory)}")
        plan = directory / "chapter-plan.md"
        if not plan.exists():
            continue
        headings = set(re.findall(r"^## (.+)$", plan.read_text(encoding="utf-8"), re.MULTILINE))
        for heading in sorted(required_headings - headings):
            fail(f"missing plan heading '{heading}': {relative(plan)}")


def check_instruction_budgets() -> None:
    limits = {
        "AGENTS.md": 350,
        "docs/autonomous-workflow.md": 650,
        "docs/style-guide.md": 300,
        "docs/chapter-template.md": 400,
        "docs/evidence-policy.md": 300,
        "docs/visuals-policy.md": 650,
        "docs/examples-policy.md": 180,
        "knowledge/AGENTS.md": 260,
    }
    for name, limit in limits.items():
        count = len((ROOT / name).read_text(encoding="utf-8").split())
        if count > limit:
            fail(f"instruction word budget exceeded: {name}: {count} > {limit}")
    for path in (ROOT / "knowledge").rglob("AGENTS.md"):
        if path == ROOT / "knowledge" / "AGENTS.md":
            continue
        count = len(path.read_text(encoding="utf-8").split())
        if count > 180:
            fail(f"local instruction word budget exceeded: {relative(path)}: {count} > 180")


def check_status(units: list[Unit]) -> None:
    path = ROOT / "PROJECT_STATUS.md"
    status = front_matter(path)
    if status is None:
        return
    validate_schema(status, "project-status.schema.json", relative(path))
    by_id = {unit.unit_id: unit for unit in units}
    completed = status.get("completed_through")
    current = status.get("current_unit")
    expected_index = 0 if completed is None else next((index + 1 for index, unit in enumerate(units) if unit.unit_id == completed), -1)
    if completed is not None and completed not in by_id:
        fail(f"unknown completed_through unit: {completed}")
    expected_next = units[expected_index].unit_id if 0 <= expected_index < len(units) else None
    if status.get("next_recommended_unit") != expected_next:
        fail(f"next_recommended_unit must be {expected_next}")
    if current is None:
        if status.get("current_unit_path") is not None:
            fail("current_unit_path must be null while current_unit is null")
        if status.get("current_unit_state") != "idle":
            fail("current_unit_state must be idle while current_unit is null")
        if status.get("units_in_review"):
            fail("units_in_review must be empty while current_unit is null")
        if status.get("blocked_from") is not None:
            fail("blocked_from must be null while current_unit is null")
    else:
        if current != expected_next or current not in by_id:
            fail(f"current_unit must be the next dependency unit: {expected_next}")
        else:
            unit = by_id[current]
            if status.get("current_unit_path") != unit.chapter_path:
                fail(f"current_unit_path must be {unit.chapter_path}")
        if status.get("current_unit_state") == "idle":
            fail("an active unit cannot have idle state")
        reviews = status.get("units_in_review", [])
        if status.get("current_unit_state") == "review" and reviews != [current]:
            fail("review state requires the current unit as the only review unit")
        if status.get("current_unit_state") != "review" and current in reviews:
            fail("unit may enter units_in_review only in review state")
        if status.get("current_unit_state") == "blocked":
            if status.get("blocked_from") not in STATE_NAMES or not status.get("blockers"):
                fail("blocked state requires blocked_from and at least one blocker")
        elif status.get("blocked_from") is not None:
            fail("blocked_from is allowed only in blocked state")
    for index, unit in enumerate(units):
        chapter = ROOT / unit.chapter_path
        should_be_complete = index < expected_index
        is_current = unit.unit_id == current
        if should_be_complete:
            if not chapter.is_file():
                fail(f"completed unit chapter is missing: {unit.unit_id} -> {unit.chapter_path}")
            else:
                metadata = front_matter(chapter)
                if metadata is not None and metadata.get("status") != "complete":
                    fail(f"completed unit chapter is not complete: {unit.unit_id}")
        elif is_current:
            if not chapter.is_file():
                fail(f"current unit chapter is missing: {unit.unit_id} -> {unit.chapter_path}")
            elif status.get("current_unit_state") == "review":
                metadata = front_matter(chapter)
                if metadata is not None and metadata.get("status") != "review":
                    fail(f"review unit chapter is not in review: {unit.unit_id}")
        elif chapter.exists():
            fail(f"chapter exists ahead of the operational frontier: {unit.unit_id} -> {unit.chapter_path}")


def check_sources(units: list[Unit]) -> dict[str, dict[str, Any]]:
    unit_ids = {unit.unit_id for unit in units}
    records: dict[str, dict[str, Any]] = {}
    for path in (ROOT / "sources").rglob("*.yml"):
        if path.name == "source-template.yml":
            continue
        data = load_yaml(path)
        validate_schema(data, "source-record.schema.json", relative(path))
        if not isinstance(data, dict) or not isinstance(data.get("id"), str):
            continue
        source_id = data["id"]
        if source_id in records:
            fail(f"duplicate source id: {source_id}")
        records[source_id] = data
        if path.stem != source_id:
            fail(f"source id does not match filename: {relative(path)}")
        expected_owner = data.get("unit_ids", [])[0].lower() if len(data.get("unit_ids", [])) == 1 else "project"
        if len(data.get("unit_ids", [])) > 1:
            fail(f"source record belongs to more than one unit: {source_id}")
        if path.parent.name != expected_owner:
            fail(f"source record folder must match owner: {relative(path)}")
        for unit_id in data.get("unit_ids", []):
            if unit_id not in unit_ids:
                fail(f"source record has unknown unit id: {source_id} -> {unit_id}")
        for used_in in data.get("used_in", []):
            if not (ROOT / used_in).is_file():
                fail(f"source record has missing used_in path: {source_id} -> {used_in}")
        local_copy = data.get("local_copy")
        if local_copy:
            copy_path = ROOT / local_copy
            if not copy_path.is_file():
                fail(f"source local_copy missing: {source_id} -> {local_copy}")
            elif hashlib.sha256(copy_path.read_bytes()).hexdigest() != data.get("sha256"):
                fail(f"source checksum mismatch: {source_id}")
        elif data.get("sha256"):
            fail(f"source checksum requires local_copy: {source_id}")
    return records


def check_visuals(source_ids: set[str], unit_ids: set[str]) -> dict[str, dict[str, Any]]:
    index_path = ROOT / "assets" / "attribution.yml"
    index = load_yaml(index_path)
    validate_schema(index, "attribution-index.schema.json", relative(index_path))
    indexed = set(index.get("manifests", [])) if isinstance(index, dict) else set()
    actual = {path.relative_to(ROOT / "assets").as_posix() for path in (ROOT / "assets" / "images").rglob("manifest.yml")}
    if indexed != actual:
        fail(f"visual manifest index differs: missing={sorted(actual - indexed)}, stale={sorted(indexed - actual)}")
    visual_files: dict[str, dict[str, Any]] = {}
    for manifest_relative in sorted(indexed):
        manifest_path = ROOT / "assets" / manifest_relative
        if not manifest_path.is_file():
            fail(f"indexed visual manifest missing: {manifest_relative}")
            continue
        data = load_yaml(manifest_path)
        validate_schema(data, "visual-manifest.schema.json", f"assets/{manifest_relative}")
        if not isinstance(data, dict):
            continue
        manifest_unit = data.get("unit_id")
        if manifest_unit != "project" and manifest_unit not in unit_ids:
            fail(f"visual manifest has unknown unit: assets/{manifest_relative} -> {manifest_unit}")
        if manifest_unit != "project" and manifest_path.parent.name != str(manifest_unit).lower():
            fail(f"visual manifest folder must match unit id: assets/{manifest_relative}")
        for visual in data.get("visuals", []):
            if not isinstance(visual, dict) or not isinstance(visual.get("file"), str):
                continue
            file_name = visual["file"]
            if file_name in visual_files:
                fail(f"duplicate visual record: {file_name}")
            visual_files[file_name] = visual | {"unit_id": data.get("unit_id")}
            asset = ROOT / "assets" / file_name
            if asset.suffix.lower() not in {".png", ".webp"}:
                fail(f"final visual must be PNG or WebP: assets/{file_name}")
            if not asset.is_file():
                fail(f"visual file missing: assets/{file_name}")
                continue
            if asset.parent != manifest_path.parent:
                fail(f"visual is not owned by its manifest folder: assets/{file_name}")
            if hashlib.sha256(asset.read_bytes()).hexdigest() != visual.get("sha256"):
                fail(f"visual checksum mismatch: assets/{file_name}")
            try:
                actual_metadata = image_metadata(asset)
                recorded_metadata = (visual.get("media_type"), visual.get("width"), visual.get("height"))
                if recorded_metadata != actual_metadata:
                    fail(f"visual media metadata mismatch: assets/{file_name}")
            except ValueError:
                fail(f"visual is not a valid PNG or WebP: assets/{file_name}")
            for optional_path in ("editable_source", "prompt_file"):
                value = visual.get(optional_path)
                if value and not (ROOT / "assets" / value).is_file():
                    fail(f"visual {optional_path} missing: assets/{value}")
            prompt_file = visual.get("prompt_file")
            if prompt_file and (ROOT / "assets" / prompt_file).parent != asset.parent / "source":
                fail(f"visual prompt_file must be chapter-local: assets/{file_name}")
            if visual.get("kind") == "generated" and not visual.get("prompt_file"):
                fail(f"generated visual requires prompt_file: assets/{file_name}")
            if visual.get("kind") == "downloaded":
                for field in ("source_url", "direct_asset_url", "license_url"):
                    if not visual.get(field):
                        fail(f"downloaded visual requires {field}: assets/{file_name}")
            for used_in in visual.get("used_in", []):
                if not (ROOT / used_in).is_file():
                    fail(f"visual used_in missing: {file_name} -> {used_in}")
            for source_id in visual.get("source_records", []):
                if source_id not in source_ids:
                    fail(f"visual references unknown source: {file_name} -> {source_id}")
    final_assets = {
        path.relative_to(ROOT / "assets").as_posix()
        for path in (ROOT / "assets" / "images").rglob("*")
        if path.is_file() and path.name != "manifest.yml" and "source" not in path.relative_to(ROOT / "assets").parts
    }
    if set(visual_files) != final_assets:
        fail(f"visual records differ from files: unregistered={sorted(final_assets - set(visual_files))}, missing={sorted(set(visual_files) - final_assets)}")
    return visual_files


def check_chapters(units: list[Unit], sources: dict[str, dict[str, Any]], visuals: dict[str, dict[str, Any]]) -> None:
    by_path = {unit.chapter_path: unit for unit in units}
    seen_units: set[str] = set()
    required_front_matter = {"title", "unit_id", "summary", "prerequisites", "learning_objectives", "source_records", "visual_assets", "example_paths", "pass", "learning_path", "status", "last_reviewed"}
    architecture_headings = {
        "Why this matters", "Simple mental model", "Position in the agent workflow", "How it works",
        "Main variants", "Minimal implementation", "Framework implementations", "Data flow and state changes",
        "Trust boundaries", "Reliability failures", "Worked example", "Limitations and trade-offs",
        "Security preview", "Open research questions", "Key takeaways", "References",
    }
    security_headings = {
        "Architecture and workflow scope", "Threat model assumptions", "Assets and trust boundaries",
        "Failures and attacks", "Preventive controls", "Detective controls", "Recovery controls",
        "Security tests", "Secure design pattern", "Limitations and residual risk", "Open research questions",
        "Key takeaways", "References",
    }
    forbidden_architecture = {"Failures and attacks", "Preventive controls", "Detective controls", "Recovery controls", "Security tests"}
    for path in (ROOT / "knowledge").rglob("*.md"):
        if path.name in {"AGENTS.md", "chapter-plan.md"}:
            continue
        chapter_path = relative(path)
        unit = by_path.get(chapter_path)
        if unit is None:
            fail(f"chapter is not a roadmap unit: {chapter_path}")
            continue
        metadata = front_matter(path)
        if metadata is None:
            continue
        missing = required_front_matter - set(metadata)
        for key in sorted(missing):
            fail(f"chapter front matter missing {key}: {chapter_path}")
        unit_id = metadata.get("unit_id")
        if unit_id != unit.unit_id:
            fail(f"chapter unit_id mismatch: {chapter_path}")
        if unit_id in seen_units:
            fail(f"duplicate chapter unit_id: {unit_id}")
        seen_units.add(unit_id)
        if metadata.get("title") != unit.title:
            fail(f"chapter title mismatch: {chapter_path}")
        if metadata.get("pass") != unit.pass_name:
            fail(f"chapter pass mismatch: {chapter_path}")
        if metadata.get("learning_path") != unit.learning_path:
            fail(f"chapter learning_path mismatch: {chapter_path}")
        if not isinstance(metadata.get("summary"), str) or not metadata["summary"].strip():
            fail(f"chapter summary is empty: {chapter_path}")
        if not isinstance(metadata.get("learning_objectives"), list) or not metadata["learning_objectives"]:
            fail(f"chapter learning_objectives are empty: {chapter_path}")
        if not isinstance(metadata.get("source_records"), list) or not metadata["source_records"]:
            fail(f"chapter source_records are empty: {chapter_path}")
        if metadata.get("status") not in {"outline", "draft", "review", "complete", "deprecated"}:
            fail(f"chapter has invalid status: {chapter_path}")
        content = path.read_text(encoding="utf-8")
        headings = set(re.findall(r"^## (.+)$", content, re.MULTILINE))
        required = architecture_headings if unit.pass_name == "architecture" else security_headings
        for heading in sorted(required - headings):
            fail(f"chapter missing heading '{heading}': {chapter_path}")
        for heading in sorted(required.intersection(headings)):
            section = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
            if section is None or not section.group(1).strip():
                fail(f"chapter section is empty '{heading}': {chapter_path}")
        if unit.pass_name == "architecture" and headings.intersection(forbidden_architecture):
            fail(f"architecture chapter contains detailed security headings: {chapter_path}")
        for source_id in metadata.get("source_records", []):
            record = sources.get(source_id)
            if record is None:
                fail(f"chapter references unknown source: {chapter_path} -> {source_id}")
            elif unit.unit_id not in record.get("unit_ids", []) or chapter_path not in record.get("used_in", []):
                fail(f"source backlink missing: {source_id} -> {unit.unit_id}, {chapter_path}")
        for visual_path in metadata.get("visual_assets", []):
            normalized = visual_path.removeprefix("assets/")
            visual = visuals.get(normalized)
            if visual is None:
                fail(f"chapter references unknown visual: {chapter_path} -> {visual_path}")
            elif visual.get("unit_id") != unit.unit_id or chapter_path not in visual.get("used_in", []):
                fail(f"visual ownership or backlink mismatch: {chapter_path} -> {visual_path}")
        for example_path in metadata.get("example_paths", []):
            target = ROOT / example_path
            if not target.exists():
                fail(f"chapter example path missing: {chapter_path} -> {example_path}")


def main() -> int:
    required = [
        "AGENTS.md", "README.md", "PROJECT_STATUS.md", "ROADMAP.md", "CHANGELOG.md",
        "docs/autonomous-workflow.md", "assets/attribution.yml",
        "requirements-dev.txt", "scripts/project_state.py", "scripts/register_source.py",
        "scripts/register_visual.py", ".github/workflows/validate.yml",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            fail(f"missing required file: {name}")
    check_text_and_links()
    check_planning_files()
    check_instruction_budgets()
    units = resolve_units()
    check_status(units)
    sources = check_sources(units)
    visuals = check_visuals(set(sources), {unit.unit_id for unit in units})
    check_chapters(units, sources, visuals)
    if ERRORS:
        print("Validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    chapters = len([path for path in (ROOT / "knowledge").rglob("*.md") if path.name not in {"AGENTS.md", "chapter-plan.md"}])
    print(f"Validation passed: {len(units)} roadmap units, {chapters} chapters, {len(visuals)} final visuals, {len(sources)} source records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
