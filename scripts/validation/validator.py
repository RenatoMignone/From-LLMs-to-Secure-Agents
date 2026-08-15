"""Validate guide structure, state, chapters, evidence, and visual assets."""

from __future__ import annotations

import hashlib
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path.cwd() if (Path.cwd() / "PROJECT_STATUS.md").is_file() else Path(__file__).resolve().parents[2]
ERRORS: list[str] = []
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
        fail(f"cannot read yaml {relative(path)}: {error}")
        return None


def front_matter(path: Path) -> dict[str, Any] | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        fail(f"cannot read {relative(path)}: {error}")
        return None
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        fail(f"missing yaml front matter: {relative(path)}")
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        fail(f"cannot parse front matter in {relative(path)}: {error}")
        return None
    if not isinstance(data, dict):
        fail(f"front matter must be a mapping: {relative(path)}")
        return None
    return data


def numbered_directory(parent: Path, number: int) -> Path | None:
    matches = sorted(path for path in parent.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}-"))
    if len(matches) != 1:
        return None
    return matches[0]


def child_learning_paths(plan_path: Path) -> dict[int, str]:
    if not plan_path.is_file():
        return {}
    content = plan_path.read_text(encoding="utf-8")
    paths: dict[int, str] = {}
    learning_path = "main"
    for line in content.splitlines():
        clean = line.strip().lower()
        if "deep dive" in clean or "deep-dive" in clean:
            learning_path = "deep-dive"
            continue
        elif "main path" in clean:
            learning_path = "main"
            continue
        item = re.match(r"^\s*(\d+)\.\s+`[^`]+`", line)
        if item:
            paths[int(item.group(1))] = learning_path
    return paths


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_roadmap_entry(unit_id: str, title: str, pass_name: str) -> Unit:
    parts = unit_id.split("-")
    if len(parts) < 3 or not parts[0].startswith("P"):
        fail(f"invalid unit id: {unit_id}")
        return Unit(unit_id, title, "", "", pass_name, "main")
    numbers = [int(p) if p.isdigit() else None for p in parts[1:]]
    if any(n is None for n in numbers):
        fail(f"invalid unit id numbers: {unit_id}")
        return Unit(unit_id, title, "", "", pass_name, "main")
    top = numbered_directory(ROOT / "knowledge", numbers[0])
    if top is None:
        fail(f"cannot resolve top-level section for {unit_id}")
        return Unit(unit_id, title, "", "", pass_name, "main")
    if len(numbers) == 2:
        directory = top
        child = numbers[1]
    else:
        directory = numbered_directory(top, numbers[1])
        child = numbers[2]
    if directory is None:
        fail(f"cannot resolve section directory for {unit_id}")
        return Unit(unit_id, title, "", "", pass_name, "main")
    plan = directory / "chapter-plan.md"
    learning_paths = child_learning_paths(plan)
    learning_path = learning_paths.get(child, "main")
    if not plan.is_file():
        fail(f"missing chapter-plan.md: {relative(plan)}")
        chapter_path = ""
    else:
        plan_text = plan.read_text(encoding="utf-8")
        plan_match = re.search(rf"^\s*{child}\. `([^`]+)`$", plan_text, re.MULTILINE)
        if not plan_match:
            fail(f"unit not found in plan {relative(plan)}: {unit_id}")
            chapter_path = ""
        else:
            chapter_file = directory / plan_match.group(1)
            chapter_path = relative(chapter_file)
            slug = slugify(title)
            expected_name = f"{child:02d}-{slug}.md"
            if chapter_file.name != expected_name:
                fail(f"roadmap and plan filename drift for {unit_id}: {chapter_file.name} != {expected_name}")
    return Unit(unit_id, title, chapter_path, relative(plan) if plan.is_file() else "", pass_name, learning_path)


def resolve_units() -> list[Unit]:
    roadmap_path = ROOT / "ROADMAP.md"
    if not roadmap_path.is_file():
        fail("missing ROADMAP.md")
        return []
    content = roadmap_path.read_text(encoding="utf-8")
    current_pass = "architecture"
    units: list[Unit] = []
    for line in content.splitlines():
        if line.startswith("## Pass 1"):
            current_pass = "architecture"
        elif line.startswith("## Pass 2"):
            current_pass = "security"
        match = re.match(r"^\d+\.\s+`([^`]+)`\s+(.+)$", line)
        if match:
            unit_id, title = match.group(1), match.group(2).strip()
            units.append(parse_roadmap_entry(unit_id, title, current_pass))
    return units


def chapter_image_folder(unit: Unit) -> Path:
    chapter = Path(unit.chapter_path)
    relative_chapter = chapter.relative_to(Path("knowledge"))
    return ROOT / "assets" / "images" / relative_chapter.with_suffix("")


def chapter_source_folder(unit: Unit) -> Path:
    chapter = Path(unit.chapter_path)
    relative_chapter = chapter.relative_to(Path("knowledge"))
    return ROOT / "sources" / relative_chapter.with_suffix("")


def chapter_example_folder(unit: Unit) -> Path:
    chapter = Path(unit.chapter_path)
    relative_chapter = chapter.relative_to(Path("knowledge"))
    return ROOT / "examples" / relative_chapter.with_suffix("")


def check_text_and_links() -> None:
    markdown_link = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    markdown_image = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    html_link = re.compile(r'<a\s+[^>]*href=["\']([^"\']+)["\']', re.IGNORECASE)
    ignored = {".git", ".github", "tmp", "__pycache__", "site"}
    extensions = {".md", ".yml", ".yaml", ".json", ".py", ".txt"}
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
        targets = [target for _, target in markdown_link.findall(content)] + [target for _, target in markdown_image.findall(content)] + list(html_link.findall(content))
        for raw in targets:
            target = raw.strip().removeprefix("<").removesuffix(">").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                fail(f"broken internal link: {relative(path)} -> {target}")
        for _, raw in markdown_image.findall(content):
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
    }
    for plan in (ROOT / "knowledge").rglob("chapter-plan.md"):
        relative_plan = relative(plan)
        if relative_plan == "knowledge/chapter-plan.md":
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
    required_fields = ["current_phase", "completed_through", "current_unit", "current_unit_path", "current_unit_state", "blocked_from", "blockers", "units_in_review", "next_recommended_unit", "last_validation_date"]
    for field in required_fields:
        if field not in status:
            fail(f"PROJECT_STATUS.md front matter missing required field: {field}")
    by_id = {unit.unit_id: unit for unit in units}
    completed_through = status.get("completed_through")
    if completed_through and completed_through not in by_id:
        fail(f"completed_through not in roadmap: {completed_through}")
    current_unit = status.get("current_unit")
    if current_unit and current_unit not in by_id:
        fail(f"current_unit not in roadmap: {current_unit}")
    current_state = status.get("current_unit_state")
    if current_state not in STATE_NAMES | {"idle", "blocked"}:
        fail(f"unknown current_unit_state: {current_state}")
    active_path = status.get("current_unit_path")
    if current_unit and active_path != by_id[current_unit].chapter_path:
        fail(f"current_unit_path mismatch: {active_path} != {by_id[current_unit].chapter_path}")
    expected = None
    if completed_through is None:
        expected = units[0].unit_id if units else None
    else:
        index = next((idx for idx, unit in enumerate(units) if unit.unit_id == completed_through), None)
        if index is not None and index + 1 < len(units):
            expected = units[index + 1].unit_id
    if status.get("next_recommended_unit") != expected:
        fail(f"next_recommended_unit must be {expected}, got {status.get('next_recommended_unit')}")
    completed_set = set()
    for unit in units:
        completed_set.add(unit.unit_id)
        if unit.unit_id == completed_through:
            break
    if completed_through is None:
        completed_set.clear()
    for unit in units:
        chapter_file = ROOT / unit.chapter_path
        if chapter_file.is_file():
            if unit.unit_id not in completed_set and unit.unit_id != current_unit:
                fail(f"chapter exists ahead of the operational frontier: {unit.unit_id} -> {unit.chapter_path}")


def check_sources(units: list[Unit]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for unit in units:
        source_folder = chapter_source_folder(unit)
        if not source_folder.is_dir():
            fail(f"missing chapter source folder: {relative(source_folder)}")
    required_source_fields = ["id", "title", "authors_or_organization", "source_type", "canonical_url", "claims_supported", "limitations", "used_in"]
    for source_file in (ROOT / "sources").rglob("*.yml"):
        if source_file.name in {".gitkeep", "source-template.yml"}:
            continue
        data = load_yaml(source_file)
        if data is None or not isinstance(data, dict):
            continue
        for field in required_source_fields:
            if field not in data or data[field] is None:
                fail(f"source record missing field '{field}': {relative(source_file)}")
        source_id = data.get("id")
        if not source_id:
            continue
        if source_file.stem != source_id:
            fail(f"source id does not match filename: {relative(source_file)}")
        if source_id in records:
            fail(f"duplicate source record id: {source_id}")
        records[source_id] = data
        parent = source_file.parent
        is_project_source = parent == (ROOT / "sources" / "project")
        matching_unit = next((unit for unit in units if chapter_source_folder(unit) == parent), None)
        if not is_project_source and matching_unit is None:
            fail(f"source record folder does not match any known chapter path: {relative(source_file)}")
        unit_ids = data.get("unit_ids", [])
        if len(unit_ids) > 1:
            fail(f"source record belongs to more than one unit: {relative(source_file)}")
        if matching_unit is not None:
            if unit_ids and unit_ids != [matching_unit.unit_id]:
                fail(f"source unit_ids mismatch for {relative(source_file)}: expected {[matching_unit.unit_id]}, got {unit_ids}")
        elif is_project_source and unit_ids:
            fail(f"project-level source cannot define unit_ids: {relative(source_file)}")
        local_copy = data.get("local_copy")
        if local_copy:
            target = ROOT / local_copy
            if not target.is_file():
                fail(f"missing local copy: {relative(source_file)} -> {local_copy}")
            elif data.get("sha256") != hashlib.sha256(target.read_bytes()).hexdigest():
                fail(f"local copy checksum mismatch: {relative(source_file)}")
    return records


def check_examples(units: list[Unit]) -> None:
    for unit in units:
        example_folder = chapter_example_folder(unit)
        if not example_folder.is_dir():
            fail(f"missing chapter example folder: {relative(example_folder)}")


def check_visuals(units: list[Unit]) -> set[str]:
    visual_files: set[str] = set()
    for unit in units:
        image_folder = chapter_image_folder(unit)
        if not image_folder.is_dir():
            fail(f"missing chapter image folder: {relative(image_folder)}")
    for image_path in (ROOT / "assets" / "images").rglob("*"):
        if not image_path.is_file() or image_path.name == ".gitkeep":
            continue
        if image_path.suffix.lower() == ".svg":
            fail(f"SVG is not allowed for visual assets: {relative(image_path)}")
        if image_path.suffix.lower() in {".png", ".webp", ".jpg", ".jpeg"}:
            visual_files.add(relative(image_path))
    return visual_files


def check_chapters(units: list[Unit], sources: dict[str, dict[str, Any]], visual_files: set[str]) -> None:
    by_path = {unit.chapter_path: unit for unit in units}
    seen_units: set[str] = set()
    required_front_matter = {"title", "unit_id", "summary", "prerequisites", "learning_objectives", "source_records", "visual_assets", "example_paths", "pass", "learning_path", "status", "last_reviewed"}
    core_architecture_headings = {
        "Why this matters", "How it works", "Security preview", "Key takeaways", "References",
    }
    allowed_architecture_headings = {
        "Why this matters", "Simple mental model", "Position in the agent workflow", "How it works",
        "Main variants", "Minimal implementation", "Framework implementations", "Data flow and state changes",
        "Trust boundaries", "Reliability failures", "Worked example", "Limitations and trade-offs",
        "Security preview", "Open research questions", "Key takeaways", "References",
    }
    core_security_headings = {
        "Architecture and workflow scope", "Threat model assumptions", "Failures and attacks",
        "Preventive controls", "Key takeaways", "References",
    }
    allowed_security_headings = {
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
        core = core_architecture_headings if unit.pass_name == "architecture" else core_security_headings
        allowed = allowed_architecture_headings if unit.pass_name == "architecture" else allowed_security_headings
        for heading in sorted(core - headings):
            fail(f"chapter missing core heading '{heading}': {chapter_path}")
        for heading in sorted(headings - allowed):
            fail(f"chapter contains unknown heading '{heading}': {chapter_path}")
        for heading in sorted(allowed.intersection(headings)):
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
            normalized = visual_path if visual_path.startswith("assets/") else f"assets/{visual_path}"
            if normalized not in visual_files and not (ROOT / normalized).is_file():
                fail(f"chapter references missing visual: {chapter_path} -> {visual_path}")
        for example_path in metadata.get("example_paths", []):
            target = ROOT / example_path
            if not target.exists():
                fail(f"chapter example path missing: {chapter_path} -> {example_path}")


def main() -> int:
    global ERRORS
    ERRORS = []
    required = [
        "AGENTS.md", "README.md", "PROJECT_STATUS.md", "ROADMAP.md", "CHANGELOG.md",
        "docs/autonomous-workflow.md", "requirements-dev.txt", "scripts/main.py", "scripts/README.md",
        ".github/workflows/validate.yml",
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
    check_examples(units)
    visuals = check_visuals(units)
    check_chapters(units, sources, visuals)
    if ERRORS:
        print("Validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    chapters = len([path for path in (ROOT / "knowledge").rglob("*.md") if path.name not in {"AGENTS.md", "chapter-plan.md"}])
    print(f"Validation passed: {len(units)} roadmap units, {chapters} chapters, {len(visuals)} visual assets, {len(sources)} source records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
