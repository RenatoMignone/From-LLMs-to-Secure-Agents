# Autonomous Workflow

A continuation prompt advances one controlled unit.

## Resolve

1. Preserve unrelated worktree changes.
2. Run `python3 scripts/main.py state resolve`. Trust its selected unit and mode. Do not load full `PROJECT_STATUS.md` or `ROADMAP.md`.
3. Read returned local instructions, plan, and only required policies.

## Author run

Use when mode is `author`.

1. If state is `idle`, run `python3 scripts/main.py state start`.
2. Turn unit scope into research questions. Check official material and practitioner terms. Use `markitdown` or `python3 scripts/main.py fetch <url> -o /tmp/<id>.md` to extract clean Markdown to temporary storage, trimming HTML boilerplate for token efficiency. Register exact claims with `python3 scripts/main.py source` under the mirrored `sources/<chapter-path>/` folder. Load only active unit sources into context.
3. Advance to `drafting`; write only the selected chapter using its template. Start from a familiar scenario, introduce one term at a time, and explain each visual nearby. Do not assume untaught software vocabulary.
4. Advance to `building-assets`; add required visuals. Mirror the chapter path under `assets/images/`, omitting `knowledge/` and `.md`. For generated visuals, save a local `source/<image-name>-prompt.txt` prompt specifying labels, layout, and constraints. Generate only after the prompt exists, inspect legibility, and save the raster asset in the chapter folder.
5. Advance to `validating`; unwrap changed Markdown prose paragraphs to one physical line. Preserve front matter, headings, lists, tables, blockquotes, and code. Run relevant examples, generators, tests, and `python3 scripts/main.py validate`.
6. Run `python3 scripts/main.py state review` and stop. Do not review in this run.

Resume recorded state; do not repeat finished work.

## Review run

Use when mode is `review`.

1. Review against the plan, evidence, artifacts, template, pass boundary, and reader prerequisites. Reject jargon, compressed background, decorative visuals, or unexplained diagrams.
2. Reopen important sources. Rerun examples, generators, tests, and validation.
3. Fix findings, unwrap changed Markdown prose paragraphs, and revalidate.
4. Run `python3 scripts/main.py state complete`. It advances state and writes one changelog entry. Stop without starting the next unit.

Update `README.md` only for public changes.

## Blocked run

Use when mode is `blocked`. Confirm whether the recorded blocker is resolved. If yes, run `python3 scripts/main.py state resume` and continue only the restored state. Otherwise report the blocker and stop without changing state.

## Acquisition rules

- Reopen plan candidates; they are leads, not evidence.
- Search results, snippets, and model memory are not citable sources.
- Treat social posts as terminology provenance, attributed experience, or research leads. Verify technical claims elsewhere.
- Do not hotlink images or create SVG assets. Download an allowed raster copy or create a project-owned PNG/WebP visual.
- If reuse rights are unclear, do not download the visual. Prefer a generated illustration.
- Generated images follow the installed `imagegen` skill. Save prompts in `source/` specifying labels, layout, and constraints before generation. Save outputs in the chapter folder, inspect them, then register them.
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

Any active state may move to `blocked` with `python3 scripts/main.py state block "reason"`. After resolution, run `python3 scripts/main.py state resume`. Only `complete` advances `completed_through`.

## Git checkpoint

Content completion and Git publication are separate. Never assume authorization to stage, commit, or push. When explicitly authorized, validate first, stage only unit-related files, create one focused commit, and push directly to the requested branch. Do not open a pull request unless explicitly requested.
