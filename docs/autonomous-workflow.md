# Autonomous Workflow

A continuation prompt advances one controlled unit.

## Resolve

1. Preserve unrelated worktree changes.
2. Run `python3 scripts/main.py state resolve`. Trust its selected unit and mode. Do not load full `PROJECT_STATUS.md` or `ROADMAP.md`.
3. Read returned local instructions, plan, and only required policies.

## Author run

Use when mode is `author`.

1. If state is `idle`, run `python3 scripts/main.py state start`.
2. Turn scope into research questions. Check official material. Use `python3 scripts/main.py fetch <url> -o /tmp/<id>.md` for clean Markdown. Register claims with `python3 scripts/main.py source` under mirrored `sources/<chapter-path>/`. Load only active sources.
3. Advance to `drafting`; personalize structure to the plan. Keep core sections, omit empty placeholders. Use simple English; define technical terms. Do not create ASCII schemas. End with a next-unit navigation button.
4. Advance to `building-assets`; add visuals. Mirror paths under `assets/images/`. Proactively design multiple canonical cartoon illustrations per chapter (2 to 4 diagrams) using the image generation skill. Save prompts in `source/<image-name>-prompt.txt` before generating. Never use scripted drawing schemes. If endpoint quota is exhausted, save prompts in `source/` and record a temporary pending visual task in `AGENTS.md` to be generated when quotas reset.
5. Advance to `validating`; unwrap Markdown prose paragraphs to one line. Run examples, `python3 scripts/main.py validate`, and verify site generation with `npm --prefix site run build && npm --prefix site run check`.
6. Run `python3 scripts/main.py state review` and stop.

Resume recorded state; do not repeat finished work.

## Review run

Use when mode is `review`.

1. Review against plan, evidence, artifacts, template, and prerequisites. Reject jargon, compressed background, or unexplained diagrams. Verify that multiple visual opportunities were evaluated and illustrated.
2. Reopen sources. Rerun examples, tests, repository validation, and site build check.
3. Fix findings, unwrap Markdown prose paragraphs, and revalidate with `python3 scripts/main.py validate` and `npm --prefix site run check`.
4. Run `python3 scripts/main.py state complete`. Stop without starting the next unit.

Update `README.md` only for public changes.

## Blocked run

Use when mode is `blocked`. Confirm whether the blocker is resolved. If yes, run `python3 scripts/main.py state resume`. Otherwise report the blocker and stop.

## Acquisition rules

- Reopen plan candidates; search results and memory are not evidence.
- Do not hotlink images or create SVGs. Prefer generated cartoon illustrations.
- Save prompts in `source/` before generation. Save outputs in chapter folders.
- Do not embed downloaded SVG or HTML.

## Selection rules

- If in `review`, run only the review loop.
- Stay within the unit. Deep dives return to the main path.
- Stop at review, completion, or when evidence is missing.

## State transitions

```text
idle -> researching -> drafting -> building-assets -> validating -> review -> idle
```

Move to `blocked` with `python3 scripts/main.py state block "reason"`. Run `python3 scripts/main.py state resume` after resolution. Only `complete` advances `completed_through`.

## Git checkpoint

Content completion and Git publication are separate. When authorized, validate, stage unit files, commit, and push directly.
