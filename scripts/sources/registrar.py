"""Create or update a checked source record under sources/<chapter-path>/."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Sequence

import yaml

ROOT = Path.cwd() if (Path.cwd() / "PROJECT_STATUS.md").is_file() else Path(__file__).resolve().parents[2]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def numbered_directory(parent: Path, number: int) -> Path | None:
    matches = sorted(path for path in parent.iterdir() if path.is_dir() and path.name.startswith(f"{number:02d}-"))
    if len(matches) != 1:
        return None
    return matches[0]


def resolve_chapter_rel(unit_id: str, used_in: list[str]) -> Path:
    if unit_id == "project":
        return Path("project")
    for doc in used_in:
        path = Path(doc)
        if path.suffix == ".md" and "knowledge/" in path.as_posix():
            return path.relative_to(ROOT / "knowledge").with_suffix("")
    roadmap_path = ROOT / "ROADMAP.md"
    if roadmap_path.is_file():
        content = roadmap_path.read_text(encoding="utf-8")
        match = re.search(rf"^\s*-\s*`({re.escape(unit_id)})`\s*-\s*([^:]+):\s*`([^`]+)`", content, re.MULTILINE)
        if match:
            chapter_file = Path(match.group(3))
            return chapter_file.relative_to(ROOT / "knowledge").with_suffix("")
        parts = unit_id.split("-")
        if len(parts) >= 3 and parts[0].startswith("P"):
            numbers = [int(p) if p.isdigit() else None for p in parts[1:]]
            if all(n is not None for n in numbers):
                top = numbered_directory(ROOT / "knowledge", numbers[0])
                if len(numbers) == 2:
                    directory, child = top, numbers[1]
                else:
                    directory, child = numbered_directory(top, numbers[1]), numbers[2]
                if directory is not None:
                    plan = directory / "chapter-plan.md"
                    if plan.is_file():
                        plan_match = re.search(rf"^\s*{child}\. `([^`]+)`$", plan.read_text(encoding="utf-8"), re.MULTILINE)
                        if plan_match:
                            chapter_file = directory / plan_match.group(1)
                            return chapter_file.relative_to(ROOT / "knowledge").with_suffix("")
    raise ValueError(f"cannot resolve chapter folder for unit {unit_id}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 scripts/main.py source",
        description="Register a verified source record with supported claims and canonical citations.",
    )
    parser.add_argument("--id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--organization", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--claim", action="append", required=True)
    parser.add_argument("--limitation", action="append", required=True)
    parser.add_argument("--topic", action="append", default=[])
    parser.add_argument("--unit", action="append", default=[])
    parser.add_argument("--used-in", action="append", required=True)
    parser.add_argument("--date")
    parser.add_argument("--doi")
    parser.add_argument("--version")
    parser.add_argument("--local-copy")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.id):
        parser.error("--id must use lowercase kebab-case")
    if len(args.unit) > 1:
        parser.error("a source record belongs to one unit; register separate records when needed")
    unit_name = args.unit[0] if args.unit else "project"
    try:
        owner_rel = resolve_chapter_rel(unit_name, args.used_in)
    except ValueError as error:
        parser.error(str(error))
    folder = ROOT / "sources" / owner_rel
    folder.mkdir(parents=True, exist_ok=True)
    gitkeep = folder / ".gitkeep"
    if gitkeep.exists():
        gitkeep.unlink()
    path = folder / f"{args.id}.yml"
    previous = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    today = dt.date.today().isoformat()
    record = {
        "id": args.id,
        "title": args.title,
        "authors_or_organization": args.organization,
        "date": args.date,
        "source_type": args.source_type,
        "canonical_url": args.url,
        "doi": args.doi,
        "version": args.version,
        "accessed": previous.get("accessed", today),
        "last_verified": today,
        "status": "checked",
        "claims_supported": unique([*previous.get("claims_supported", []), *args.claim]),
        "limitations": unique([*previous.get("limitations", []), *args.limitation]),
        "related_topics": unique([*previous.get("related_topics", []), *args.topic]),
        "unit_ids": unique([*previous.get("unit_ids", []), *args.unit]),
        "used_in": unique([*previous.get("used_in", []), *args.used_in]),
        "local_copy": args.local_copy,
        "sha256": None,
    }
    if args.local_copy:
        import hashlib

        local = ROOT / args.local_copy
        if not local.is_file():
            parser.error(f"local copy does not exist: {args.local_copy}")
        record["sha256"] = hashlib.sha256(local.read_bytes()).hexdigest()
    path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
