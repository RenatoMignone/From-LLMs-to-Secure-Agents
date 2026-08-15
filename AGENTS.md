# Agent Instructions

Build a sequential, source-grounded, visual guide to agentic AI and its security.

## Run contract

1. Run `python3 scripts/main.py state resolve`. Do not read full `PROJECT_STATUS.md` or `ROADMAP.md` during a normal unit run.
2. Read returned local `AGENTS.md`, `chapter-plan.md`, and only policies selected there.
3. Follow the matching author, review, or blocked path in `docs/autonomous-workflow.md`.
4. Work on one unit. Stop after review, completion, or a recorded blocker.

## Policy map

- Scope and structure: `docs/project-charter.md`, `docs/information-architecture.md`
- Prose and chapters: `docs/style-guide.md`, `docs/chapter-template.md`
- Sources, visuals, and code: `docs/evidence-policy.md`, `docs/visuals-policy.md`, `docs/examples-policy.md`
- Site and upkeep: `docs/site-policy.md`, `docs/maintenance.md`, `docs/roadmap.md`

Normal chapter runs load style and evidence. Load other policies only when required.

## Invariants

- Assume LLM and prompt familiarity, not software vocabulary. Teach needed terms with familiar examples; use plain English before technical terms. Do not compress essential background.
- Use a scenario, labeled visual, or table whenever helpful.
- Teach in dependency order. Finish functional architecture and workflows before detailed security.
- Preserve a short main learning path. Put specialized expansions in labeled deep-dive branches that readers may skip without losing later prerequisites.
- Map risks to known components or workflow steps. State uncertainty and limitations.
- Ground important claims in official sources or primary research.
- Keep final visuals local and traceable. Do not create SVGs. Prefer verified raster downloads or generated PNG/WebP.
- Mirror chapters under `assets/images/`, `sources/`, and `examples/`, without `knowledge/` or `.md`. Save visual prompts in local `source/` before generation.
- Store chapter sources at `sources/<chapter-path>/<source-id>.yml` and repository records at `sources/project/<source-id>.yml`. Load only unit-scoped sources into context.
- Keep Markdown canonical. Generate the site from it.
- Store runnable examples under `examples/<chapter-path>/`. Keep examples small, safe, and linked to their chapters.
- Prefer prose, tables, visuals, pseudocode, or inline code. Create runnable code only when execution clarifies behavior.
- Let scripts update operational metadata. Update `README.md` only when public facts change.
- Treat `PROJECT_STATUS.md` front matter as operational truth. Never infer completion from files alone.
- Do not use em dashes.
