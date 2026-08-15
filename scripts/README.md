# Scripts and Tooling

This directory contains the modular command-line toolkit and deterministic validation suite for the guide.

## Modular Architecture

The `scripts/` directory follows a single-responsibility modular architecture. `scripts/main.py` is the **only Python file directly in the root** of `scripts/`. All functional implementations are organized into dedicated subpackages with clear, focused responsibilities:

```text
scripts/
  ├── main.py              # Single CLI dispatcher and entry point
  ├── README.md            # Architecture and tooling documentation
  ├── fetch/               # Deterministic URL and document fetcher / Markdown converter
  │   ├── __init__.py
  │   └── fetcher.py
  ├── state/               # Workflow state machine and unit resolution
  │   ├── __init__.py
  │   └── manager.py
  ├── sources/             # Source record registration and schema validation
  │   ├── __init__.py
  │   └── registrar.py
  ├── validation/          # Comprehensive repository and integrity validator
  │   ├── __init__.py
  │   └── validator.py
  └── tests/               # Regression test suite for tools and state machine
      ├── __init__.py
      └── test_validate_repo.py
```

### Guidance for Future Modules

When building new tooling:
1. **Single Responsibility**: Each subpackage must handle one specific domain (e.g. static site generation, benchmark harvesting, export formatting).
2. **Modular Placement**: Create a new subfolder under `scripts/<domain>/` with its own `__init__.py` and focused implementation files. Do not add loose Python scripts to `scripts/` root.
3. **Dispatcher Registration**: Expose the subcommand in `scripts/main.py` and register arguments with standard `argparse`.
4. **Regression Testing**: Add unit and integration tests under `scripts/tests/`.

## Unified CLI Commands

Run all project operations through `python3 scripts/main.py <subcommand>`:

```bash
# Display help and available submodules
python3 scripts/main.py --help

# Workflow state management
python3 scripts/main.py state resolve
python3 scripts/main.py state start
python3 scripts/main.py state set <state>
python3 scripts/main.py state review
python3 scripts/main.py state complete

# Fetch and convert remote URLs / documents to token-efficient Markdown
python3 scripts/main.py fetch "https://www.rfc-editor.org/rfc/rfc8693.html" -o /tmp/rfc8693.md
python3 scripts/main.py fetch "https://example.com" --grep "authentication"

# Register verified source records
python3 scripts/main.py source \
  --id saltzer-schroeder-1975 \
  --title "The Protection of Information in Computer Systems" \
  --organization "IEEE" \
  --source-type "peer-reviewed paper" \
  --url "https://doi.org/10.1109/PROC.1975.9939" \
  --claim "Introduces least privilege and economy of mechanism." \
  --limitation "Focuses on time-sharing operating systems." \
  --used-in "knowledge/00-prerequisites/04-identity-authority-and-least-privilege-primer.md"

# Run complete repository validation
python3 scripts/main.py validate

# Run automated regression tests
python3 -m unittest discover -s scripts/tests
```

## Subpackage Responsibilities

| Subpackage | Purpose |
| --- | --- |
| `scripts/main.py` | Unified CLI dispatcher and argument parsing gateway. |
| `scripts/fetch/` | Converts web URLs, HTML, and PDFs to clean Markdown using `markitdown`. Trims HTML boilerplate to optimize agent context tokens. |
| `scripts/state/` | Manages operational state, unit resolution, and atomic progression. |
| `scripts/sources/` | Enforces source schemas, resolves chapter mirroring paths, and records citations. |
| `scripts/validation/` | Deterministic validation test suite for front matter, links, visual assets, and instruction budgets. |
| `scripts/tests/` | Automated regression tests for repository tools and lifecycle transitions. |
