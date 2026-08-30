# Agent Instructions

Build a sequential, source-grounded, visual guide to agentic AI and its security.

## Run contract

1. Run `python3 scripts/main.py state resolve`. Do not read full `PROJECT_STATUS.md` or `ROADMAP.md` during normal runs.
2. Read returned local `AGENTS.md`, `chapter-plan.md`, and only selected policies.
3. Check for any pending tasks below before starting new units.
4. Follow the matching author, review, or blocked path in `docs/autonomous-workflow.md`.
5. Work on one unit. Stop after review, completion, or a recorded blocker.

## Policy map

- Scope and structure: `docs/project-charter.md`, `docs/information-architecture.md`
- Prose and chapters: `docs/style-guide.md`, `docs/chapter-template.md`
- Sources, visuals, and code: `docs/evidence-policy.md`, `docs/visuals-policy.md`, `docs/examples-policy.md`
- Site and upkeep: `docs/site-policy.md`, `docs/maintenance.md`, `docs/roadmap.md`

## Invariants

- Use simple English; define technical terms on first use. Omit empty placeholders.
- Never create ASCII/text-based schemas or scripted/programmatic drawing schemes. Use the image generation skill for PNG/WebP cartoon illustrations matching `assets/images/repo-images/source/prompt.txt`.
- Include 2 to 4 cartoon visuals per chapter whenever visual illustration improves comprehension.
- If image generation quota is temporarily exhausted, save prompts in `source/` and record a pending entry in `AGENTS.md` for the next session to generate.
- Include a next-unit navigation button at the end of each chapter.
- Teach in dependency order: functional architecture before detailed security.
- Map risks to components; ground claims in official sources (`sources/<chapter-path>/<source-id>.yml`).
- Keep visuals local and traceable; save visual prompts in `source/` before generating. No SVGs.
- Keep Markdown canonical; validate the site (`npm --prefix site run build && npm --prefix site run check`).
- Store small runnable examples under `examples/<chapter-path>/`.
- Make minimal implementation code blocks expandable by default using `<details><summary>Expand minimal Python implementation</summary>...</details>`.
- Do not use em dashes.

## Temporary Pending Tasks

- [ ] **Generate Visual Assets**: When image generation quota resets (next reset window around 17:25 CEST / 15:25 UTC), generate PNG illustrations from saved `source/` prompts for:
  - `P1-03-03-04`: `assets/images/03-building-blocks/03-planning-and-reasoning/04-search-budgets-and-termination/source/` (image 3 pending: `03-termination-state-machine`)
  - `P1-03-04-01`: `assets/images/03-building-blocks/04-state-and-lifecycle/01-run-thread-and-event-models/source/` (3 prompts)
  - `P1-03-04-02`: `assets/images/03-building-blocks/04-state-and-lifecycle/02-checkpoints-interrupts-and-resumption/source/` (3 prompts)
  - `P1-03-04-03`: `assets/images/03-building-blocks/04-state-and-lifecycle/03-retries-idempotency-and-concurrency/source/` (3 prompts)
  - `P1-03-04-04`: `assets/images/03-building-blocks/04-state-and-lifecycle/04-termination-cancellation-and-cleanup/source/` (3 prompts)
  Link the generated images into their chapters, validate the site, and remove this entry.
