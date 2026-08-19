# Agent Instructions

Build a sequential, source-grounded, visual guide to agentic AI and its security.

## Run contract

1. Run `python3 scripts/main.py state resolve`. Do not read full `PROJECT_STATUS.md` or `ROADMAP.md` during normal runs.
2. Read returned local `AGENTS.md`, `chapter-plan.md`, and only selected policies.
3. Follow the matching author, review, or blocked path in `docs/autonomous-workflow.md`.
4. Work on one unit. Stop after review, completion, or a recorded blocker.

## Policy map

- Scope and structure: `docs/project-charter.md`, `docs/information-architecture.md`
- Prose and chapters: `docs/style-guide.md`, `docs/chapter-template.md`
- Sources, visuals, and code: `docs/evidence-policy.md`, `docs/visuals-policy.md`, `docs/examples-policy.md`
- Site and upkeep: `docs/site-policy.md`, `docs/maintenance.md`, `docs/roadmap.md`

## Invariants

- Use simple, accessible English; define technical terms on first use. Omit empty placeholders.
- Never create ASCII/text-based .md schemas. Generate PNG/WebP cartoon illustrations matching `assets/images/repo-images/source/prompt.txt`.
- Include multiple cartoon visuals per chapter (2 to 4 where possible, covering architecture, control flow, boundaries, and threat paths) whenever visual illustration improves reader comprehension.
- Include a next-unit navigation button/link at the end of each chapter.
- Teach in dependency order: functional architecture before detailed security.
- Preserve a short main path; label deep-dive branches clearly.
- Map risks to components; ground claims in official sources (`sources/<chapter-path>/<source-id>.yml`).
- Keep visuals local and traceable; save visual prompts in `source/` before generating. No SVGs.
- Mirror chapters under `assets/images/`, `sources/`, and `examples/`.
- Keep Markdown canonical; generate and validate the site (`npm --prefix site run build && npm --prefix site run check`).
- Store small runnable examples under `examples/<chapter-path>/`.
- Let scripts update operational metadata. Update `README.md` only when public facts change.
- Treat `PROJECT_STATUS.md` front matter as operational truth.
- Make minimal implementation code blocks expandable by default using `<details><summary>Expand minimal Python implementation</summary>...</details>` so that code is expandable on demand by the reader.
- Do not use em dashes.

