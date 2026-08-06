#!/usr/bin/env python3
"""Create or update a checked source record from command arguments."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def main() -> int:
    parser = argparse.ArgumentParser()
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
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.id):
        parser.error("--id must use lowercase kebab-case")
    path = ROOT / "sources" / f"{args.id}.yml"
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
