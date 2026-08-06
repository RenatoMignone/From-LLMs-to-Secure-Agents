#!/usr/bin/env python3
"""Advance the single-unit guide workflow without hand-editing project state."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "PROJECT_STATUS.md"
STATE_ORDER = ["researching", "drafting", "building-assets", "validating", "review"]


def parse_status() -> tuple[dict[str, Any], str]:
    content = STATUS_PATH.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        raise SystemExit("PROJECT_STATUS.md has no YAML front matter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise SystemExit("PROJECT_STATUS.md front matter is not a mapping")
    return data, match.group(2).lstrip("\n")


def write_status(data: dict[str, Any], body: str) -> None:
    payload = "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n\n" + body.rstrip() + "\n"
    descriptor, temp_name = tempfile.mkstemp(prefix="project-status-", suffix=".md", dir=ROOT)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
        os.replace(temp_name, STATUS_PATH)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def numbered_directory(parent: Path, number: int) -> Path:
    matches = sorted(path for path in parent.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}-"))
    if len(matches) != 1:
        raise SystemExit(f"Cannot resolve {number:02d}-* under {parent.relative_to(ROOT)}")
    return matches[0]


def roadmap_units() -> list[dict[str, str]]:
    content = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    units: list[dict[str, str]] = []
    for unit_id, number_text, title in re.findall(r"^\d+\. `(P[12]-([0-9-]+))` (.+)$", content, re.MULTILINE):
        numbers = [int(part) for part in number_text.split("-")]
        top = numbered_directory(ROOT / "knowledge", numbers[0])
        if len(numbers) == 2:
            directory, child = top, numbers[1]
        else:
            directory, child = numbered_directory(top, numbers[1]), numbers[2]
        plan = directory / "chapter-plan.md"
        match = re.search(rf"^\s*{child}\. `([^`]+)`$", plan.read_text(encoding="utf-8"), re.MULTILINE)
        if not match:
            raise SystemExit(f"Cannot resolve {unit_id} in {plan.relative_to(ROOT)}")
        units.append({
            "id": unit_id,
            "title": title,
            "path": (directory / match.group(1)).relative_to(ROOT).as_posix(),
            "plan": plan.relative_to(ROOT).as_posix(),
            "pass": "architecture" if unit_id.startswith("P1-") else "security",
        })
    return units


def expected_next(data: dict[str, Any], units: list[dict[str, str]]) -> dict[str, str] | None:
    completed = data.get("completed_through")
    if completed is None:
        return units[0]
    for index, unit in enumerate(units):
        if unit["id"] == completed:
            return units[index + 1] if index + 1 < len(units) else None
    raise SystemExit(f"Unknown completed_through value: {completed}")


def chapter_template(unit: dict[str, str]) -> str:
    common = {
        "title": unit["title"],
        "unit_id": unit["id"],
        "summary": "",
        "prerequisites": [],
        "learning_objectives": [],
        "source_records": [],
        "visual_assets": [],
        "example_paths": [],
        "pass": unit["pass"],
        "status": "outline",
        "last_reviewed": None,
    }
    architecture = [
        "Why this matters", "Simple mental model", "Position in the agent workflow", "How it works",
        "Main variants", "Minimal implementation", "Framework implementations", "Data flow and state changes",
        "Trust boundaries", "Reliability failures", "Executable example", "Limitations and trade-offs",
        "Security preview", "Open research questions", "Key takeaways", "References",
    ]
    security = [
        "Architecture and workflow scope", "Threat model assumptions", "Assets and trust boundaries",
        "Failures and attacks", "Preventive controls", "Detective controls", "Recovery controls",
        "Security tests", "Secure design pattern", "Limitations and residual risk", "Open research questions",
        "Key takeaways", "References",
    ]
    headings = architecture if unit["pass"] == "architecture" else security
    front = yaml.safe_dump(common, sort_keys=False, allow_unicode=True).rstrip()
    return f"---\n{front}\n---\n\n# {unit['title']}\n\n" + "\n\n".join(f"## {heading}" for heading in headings) + "\n"


def update_chapter_status(path: Path, status: str, reviewed: bool = False) -> None:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        raise SystemExit(f"Missing chapter front matter: {path.relative_to(ROOT)}")
    data = yaml.safe_load(match.group(1))
    data["status"] = status
    if reviewed:
        data["last_reviewed"] = dt.date.today().isoformat()
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n\n" + match.group(2).lstrip("\n"), encoding="utf-8")


def run_validator() -> None:
    result = subprocess.run([sys.executable, "scripts/validate_repo.py"], cwd=ROOT, check=False)
    if result.returncode:
        raise SystemExit("Validation failed. State was not advanced.")


def append_changelog(unit: dict[str, str]) -> None:
    path = ROOT / "CHANGELOG.md"
    date = dt.date.today().isoformat()
    content = path.read_text(encoding="utf-8").rstrip()
    date_heading = "" if f"## {date}" in content else f"\n\n## {date}"
    entry = (
        f"{date_heading}\n\n### {unit['id']} complete\n\n"
        f"- Files or sections: `{unit['path']}` and its evidence, visuals, or examples\n"
        f"- Summary: Completed and reviewed {unit['title']}.\n"
        "- Validation: Passed repository validation and the unit review checklist.\n"
    )
    path.write_text(content + entry, encoding="utf-8")


def command_start(data: dict[str, Any], body: str, units: list[dict[str, str]]) -> None:
    if data.get("current_unit") is not None or data.get("current_unit_state") != "idle":
        raise SystemExit("A unit is already active. Resume it instead of starting another.")
    unit = expected_next(data, units)
    if unit is None:
        raise SystemExit("All roadmap units are complete.")
    if data.get("blockers"):
        raise SystemExit("Clear recorded blockers before starting a unit.")
    chapter = ROOT / unit["path"]
    if not chapter.exists():
        chapter.write_text(chapter_template(unit), encoding="utf-8")
    data.update({
        "current_phase": "pass-1-architecture" if unit["pass"] == "architecture" else "pass-2-security",
        "current_unit": unit["id"],
        "current_unit_path": unit["path"],
        "current_unit_state": "researching",
        "blocked_from": None,
        "units_in_review": [],
    })
    write_status(data, body)
    print(f"Started {unit['id']}: {unit['path']}")


def command_set(data: dict[str, Any], body: str, requested: str) -> None:
    current = data.get("current_unit_state")
    if current not in STATE_ORDER[:-1] or requested not in STATE_ORDER:
        raise SystemExit(f"Cannot transition from {current} to {requested}")
    if STATE_ORDER.index(requested) != STATE_ORDER.index(current) + 1:
        raise SystemExit(f"Expected next state after {current}: {STATE_ORDER[STATE_ORDER.index(current) + 1]}")
    data["current_unit_state"] = requested
    write_status(data, body)
    print(f"State: {requested}")


def command_review(data: dict[str, Any], body: str) -> None:
    if data.get("current_unit_state") != "validating":
        raise SystemExit("Review may start only after validating.")
    run_validator()
    unit_id = data["current_unit"]
    update_chapter_status(ROOT / data["current_unit_path"], "review")
    data["current_unit_state"] = "review"
    data["units_in_review"] = [unit_id]
    data["last_validation_date"] = dt.date.today().isoformat()
    write_status(data, body)
    print(f"Ready for separate review: {unit_id}")


def command_block(data: dict[str, Any], body: str, reason: str) -> None:
    current = data.get("current_unit_state")
    if data.get("current_unit") is None or current not in STATE_ORDER:
        raise SystemExit("Only an active unit may be blocked.")
    data["blocked_from"] = current
    data["current_unit_state"] = "blocked"
    data["blockers"] = list(dict.fromkeys([*data.get("blockers", []), reason]))
    write_status(data, body)
    print(f"Blocked {data['current_unit']}: {reason}")


def command_resume(data: dict[str, Any], body: str) -> None:
    if data.get("current_unit_state") != "blocked" or data.get("blocked_from") not in STATE_ORDER:
        raise SystemExit("No resumable blocked unit is recorded.")
    restored = data["blocked_from"]
    data["current_unit_state"] = restored
    data["blocked_from"] = None
    data["blockers"] = []
    write_status(data, body)
    print(f"Resumed {data['current_unit']} at {restored}")


def command_complete(data: dict[str, Any], body: str, units: list[dict[str, str]]) -> None:
    if data.get("current_unit_state") != "review":
        raise SystemExit("A unit may complete only from review state.")
    run_validator()
    unit = next(item for item in units if item["id"] == data["current_unit"])
    update_chapter_status(ROOT / unit["path"], "complete", reviewed=True)
    data["completed_through"] = unit["id"]
    data["current_unit"] = None
    data["current_unit_path"] = None
    data["current_unit_state"] = "idle"
    data["blocked_from"] = None
    data["units_in_review"] = []
    following = expected_next(data, units)
    data["next_recommended_unit"] = following["id"] if following else None
    data["last_validation_date"] = dt.date.today().isoformat()
    append_changelog(unit)
    write_status(data, body)
    print(f"Completed {unit['id']}. Next: {data['next_recommended_unit']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show")
    subparsers.add_parser("resolve")
    subparsers.add_parser("start")
    state_parser = subparsers.add_parser("set")
    state_parser.add_argument("state", choices=STATE_ORDER[1:-1])
    subparsers.add_parser("review")
    block_parser = subparsers.add_parser("block")
    block_parser.add_argument("reason")
    subparsers.add_parser("resume")
    subparsers.add_parser("complete")
    args = parser.parse_args()
    data, body = parse_status()
    units = roadmap_units()
    if args.command == "show":
        print(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), end="")
    elif args.command == "resolve":
        selected = next((unit for unit in units if unit["id"] == data.get("current_unit")), None) or expected_next(data, units)
        state = data.get("current_unit_state")
        mode = "blocked" if state == "blocked" else "review" if state == "review" else "author"
        local_instructions = (Path(selected["path"]).parent / "AGENTS.md").as_posix() if selected else None
        result = {
            "unit_id": selected["id"] if selected else None,
            "title": selected["title"] if selected else None,
            "chapter_path": selected["path"] if selected else None,
            "local_instructions_path": local_instructions,
            "plan_path": selected["plan"] if selected else None,
            "pass": selected["pass"] if selected else None,
            "mode": mode,
            "state": state,
            "blockers": data.get("blockers", []),
        }
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True), end="")
    elif args.command == "start":
        command_start(data, body, units)
    elif args.command == "set":
        command_set(data, body, args.state)
    elif args.command == "review":
        command_review(data, body)
    elif args.command == "block":
        command_block(data, body, args.reason)
    elif args.command == "resume":
        command_resume(data, body)
    elif args.command == "complete":
        command_complete(data, body, units)
    return 0


if __name__ == "__main__":
    sys.exit(main())
