# Source Instructions

Read `docs/evidence-policy.md`.

Rules:

- One focused record per source.
- Mirror every chapter path under `sources/`, omitting `knowledge/` and `.md`.
- Use `sources/<chapter-path>/<source-id>.yml` for a chapter record. Use `sources/project/<source-id>.yml` only for repository-wide material.
- Load only the source folder needed for the current chapter and topic into context.
- Record exact supported claims.
- Record canonical URL or DOI, access and verification dates, version, and limitations.
- Prefer official and primary sources.
- Do not cite unread sources.
- Do not treat search snippets or plan candidates as checked evidence.
- Add a checksum when a licensed local copy is required.
- Mark conflicting evidence.
- Review time-sensitive sources before reuse.
- Use `scripts/main.py source` instead of formatting records by hand.
