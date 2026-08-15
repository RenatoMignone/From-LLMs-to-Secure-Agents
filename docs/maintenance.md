# Maintenance

## Before editing

1. Read root `AGENTS.md`.
2. Run `python3 scripts/main.py state resolve`.
3. Read returned local instructions, plan, and selected policies.
4. Follow returned run mode in `docs/autonomous-workflow.md`.

## After editing

1. Run `python3 scripts/main.py validate`.
2. Run unit examples, generators, and tests.
3. Check citations, terminology, limitations, and required artifact metadata. Recheck the status and provenance of emerging terms.
4. Confirm pass boundary and required cross-links.
5. Let state scripts update `PROJECT_STATUS.md` and `CHANGELOG.md`.
6. Update navigation or `README.md` only when public facts changed.

## Status values

- planned
- outline
- draft
- review
- complete
- deprecated

The operational states and allowed transitions are defined in `docs/autonomous-workflow.md`.
