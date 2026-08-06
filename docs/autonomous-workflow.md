# Autonomous Workflow

The prompt "Read `AGENTS.md` and continue from the last checkpoint" advances one unit through one controlled run.

## Resolve

1. Inspect the worktree and preserve unrelated changes.
2. Run `python3 scripts/project_state.py resolve`. Trust its selected unit and mode. Do not load full `PROJECT_STATUS.md` or `ROADMAP.md`.
3. Read returned local instructions, plan, and only required policies.

## Author run

Use when mode is `author`.

1. If state is `idle`, run `python3 scripts/project_state.py start`.
2. Turn unit scope into research questions. Research only that unit. Check current official material and practitioner discussion for useful field terms. Open every cited source and register exact claims with `scripts/register_source.py`.
3. Advance to `drafting`; write only the selected chapter using its template.
4. Advance to `building-assets`; add only plan-required visuals and examples. Register visuals with `scripts/register_visual.py`.
5. Advance to `validating`; run relevant examples, generators, tests, and `python3 scripts/validate_repo.py`.
6. Run `python3 scripts/project_state.py review` and stop. Do not start review in this run.

Resume an interrupted author run from its recorded state. Inspect existing artifacts first and do not repeat finished work.

## Review run

Use when mode is `review`.

1. Review only the current unit against its plan, sources, artifacts, template, terminology status, and pass boundary.
2. Reopen important sources. Rerun examples, generators, tests, and repository validation.
3. Fix findings within this unit and revalidate.
4. Run `python3 scripts/project_state.py complete`. It advances state and writes one changelog entry. Stop without starting the next unit.

Update `README.md` only when public structure, navigation, or project facts changed.

## Blocked run

Use when mode is `blocked`. Confirm whether the recorded blocker is resolved. If yes, run `python3 scripts/project_state.py resume` and continue only the restored state. Otherwise report the blocker and stop without changing state.

## Acquisition rules

- Candidate sources in a plan are leads, not evidence. Reopen and verify them for the current unit.
- Search results, snippets, and model memory are not citable sources.
- Treat social posts as terminology provenance, attributed experience, or research leads. Verify technical claims elsewhere.
- Do not hotlink images. Download an allowed copy or create a project-owned visual.
- If reuse rights are unclear, do not download the visual. Prefer an original diagram or generated illustration.
- Generated images follow the installed `imagegen` skill. Save project outputs in `assets/images/<chapter-id>/` and record them.
- Technical diagrams and plots must be code-native and reproducible. Do not use image generation for precise topology, labels, or quantitative claims.
- Download into a temporary directory. Check final URL, media type, size, license, dimensions, and visible content before moving files into `assets/`.
- Do not embed downloaded SVG or HTML. Recreate the diagram or safely rasterize a permitted source.

## Selection rules

- If the current unit is in `review`, run only the review loop.
- Do not cross unit boundaries. Record external gaps as blockers or unresolved questions.
- Stop at review, completion, or when evidence, authority, or a prerequisite is missing.

## State transitions

Allowed forward path:

```text
idle -> researching -> drafting -> building-assets -> validating -> review -> idle
```

Any active state may move to `blocked` with `python3 scripts/project_state.py block "reason"`. After resolution, run `python3 scripts/project_state.py resume`. Only `complete` advances `completed_through`.

## Git checkpoint

Content completion and Git publication are separate. Never assume authorization to stage, commit, or push. When explicitly authorized, validate first, stage only unit-related files, create one focused commit, and push directly to the requested branch. Do not open a pull request unless explicitly requested.
