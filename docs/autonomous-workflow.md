# Autonomous Workflow

A continuation prompt advances one controlled unit.

## Resolve

1. Preserve unrelated worktree changes.
2. Run `python3 scripts/project_state.py resolve`. Trust its selected unit and mode. Do not load full `PROJECT_STATUS.md` or `ROADMAP.md`.
3. Read returned local instructions, plan, and only required policies.

## Author run

Use when mode is `author`.

1. If state is `idle`, run `python3 scripts/project_state.py start`.
2. Turn unit scope into research questions. Check current official material and useful practitioner terminology. Open every cited source and register exact claims with `scripts/register_source.py` under `sources/<unit-id-lowercase>/`.
3. Advance to `drafting`; write only the selected chapter using its template. Start from a familiar scenario, introduce one term at a time, and explain each visual nearby. Do not assume untaught software vocabulary.
4. Advance to `building-assets`; add required visuals. Mirror the chapter's path under `assets/images/`, omitting `knowledge/` and `.md`, and put every visual in that owning folder. For generated visuals, first save a local `source/` prompt that follows the banner style and specifies labels, layout, and constraints. Generate only after the prompt exists, inspect correspondence and legibility, then register it with `scripts/register_visual.py`.
5. Advance to `validating`; unwrap changed Markdown prose paragraphs to one physical line. Preserve front matter, headings, lists, tables, blockquotes, and code. Run relevant examples, generators, tests, and `python3 scripts/validate_repo.py`.
6. Run `python3 scripts/project_state.py review` and stop. Do not review in this run.

Resume recorded state; do not repeat finished work.

## Review run

Use when mode is `review`.

1. Review against the plan, evidence, artifacts, template, pass boundary, and reader prerequisites. Reject jargon, compressed background, decorative visuals, or unexplained diagrams.
2. Reopen important sources. Rerun examples, generators, tests, and validation.
3. Fix findings, unwrap changed Markdown prose paragraphs, and revalidate.
4. Run `python3 scripts/project_state.py complete`. It advances state and writes one changelog entry. Stop without starting the next unit.

Update `README.md` only for public changes.

## Blocked run

Use when mode is `blocked`. Confirm whether the recorded blocker is resolved. If yes, run `python3 scripts/project_state.py resume` and continue only the restored state. Otherwise report the blocker and stop without changing state.

## Acquisition rules

- Reopen plan candidates; they are leads, not evidence.
- Search results, snippets, and model memory are not citable sources.
- Treat social posts as terminology provenance, attributed experience, or research leads. Verify technical claims elsewhere.
- Do not hotlink images or create SVG assets. Download an allowed raster copy or create a project-owned PNG/WebP visual.
- If reuse rights are unclear, do not download the visual. Prefer a generated illustration.
- Generated images follow the installed `imagegen` skill. Before generation, save the complete prompt in the mirrored chapter folder's `source/`; adapt the repository banner's approachable technical-cartoon style, specify exact labels, layout, and constraints. Save outputs in the owning chapter folder, inspect them, then record them.
- Download into a temporary directory. Check final URL, media type, size, license, dimensions, and visible content before moving files into `assets/`.
- Do not embed downloaded SVG or HTML. Recreate the diagram or safely rasterize a permitted source.

## Selection rules

- If the current unit is in `review`, run only the review loop.
- Stay within the unit. Deep dives link to their main-path entry and return without creating core prerequisites.
- Stop at review, completion, or when evidence, authority, or a prerequisite is missing.

## State transitions

Allowed forward path:

```text
idle -> researching -> drafting -> building-assets -> validating -> review -> idle
```

Any active state may move to `blocked` with `python3 scripts/project_state.py block "reason"`. After resolution, run `python3 scripts/project_state.py resume`. Only `complete` advances `completed_through`.

## Git checkpoint

Content completion and Git publication are separate. Never assume authorization to stage, commit, or push. When explicitly authorized, validate first, stage only unit-related files, create one focused commit, and push directly to the requested branch. Do not open a pull request unless explicitly requested.
