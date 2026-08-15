#!/usr/bin/env python3
"""Unified modular CLI entry point for project workflow, state, sources, visuals, and validation."""

import argparse
import sys
from pathlib import Path
from typing import Sequence

# Add scripts directory to sys.path to allow module imports
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from fetch import fetcher as fetch_module
from sources import registrar as source_module
from state import manager as state_module
from validation import validator as validate_module


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 scripts/main.py",
        description="Unified modular CLI toolkit for 'From LLMs to Secure Agents'.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True, help="Available submodules")

    # state
    subparsers.add_parser(
        "state",
        help="Manage workflow state transitions (resolve, start, set, review, block, resume, complete)",
        add_help=False,
    )

    # source
    subparsers.add_parser(
        "source",
        help="Register a verified source record under sources/<chapter-path>/",
        add_help=False,
    )

    # validate
    subparsers.add_parser(
        "validate",
        help="Run comprehensive repository validation suite",
    )

    # fetch
    subparsers.add_parser(
        "fetch",
        help="Fetch and convert web URLs / documents to clean token-efficient Markdown",
        add_help=False,
    )

    if argv is None:
        raw_args = sys.argv[1:]
    else:
        raw_args = list(argv)

    if not raw_args:
        parser.print_help()
        return 0

    first = raw_args[0]
    rest = raw_args[1:]

    if first in ("-h", "--help"):
        parser.print_help()
        return 0

    if first == "state":
        return state_module.main(rest)
    elif first == "source":
        return source_module.main(rest)
    elif first == "validate":
        return validate_module.main()
    elif first == "fetch":
        return fetch_module.main(rest)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
