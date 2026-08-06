# Agent Instructions

Build a sequential, source-grounded, visual guide to agentic AI and its security.

## Run contract

1. Run `python3 scripts/project_state.py resolve`. Do not read full `PROJECT_STATUS.md` or `ROADMAP.md` during a normal unit run.
2. Read returned local `AGENTS.md`, `chapter-plan.md`, and only policies selected there.
3. Follow the matching author, review, or blocked path in `docs/autonomous-workflow.md`.
4. Work on one unit. Stop after review, completion, or a recorded blocker.

## Policy map

- Scope and structure: `docs/project-charter.md`, `docs/information-architecture.md`
- Prose and chapters: `docs/style-guide.md`, `docs/chapter-template.md`
- Sources, visuals, and code: `docs/evidence-policy.md`, `docs/visuals-policy.md`, `docs/examples-policy.md`
- Site and upkeep: `docs/site-policy.md`, `docs/maintenance.md`, `docs/roadmap.md`

Normal chapter runs load style and evidence policies. The generated scaffold and validator enforce the chapter template; open that policy only for structural repair. Load visuals or examples policy only when the plan requires that artifact. Load other policies only for structural, site, or maintenance work.

## Invariants

- Assume the reader has working familiarity with large language models and prompts. Give only brief, just-in-time refreshers needed for agentic topics. Do not teach model internals in depth.
- Teach in dependency order. Finish functional architecture and workflows before detailed security.
- Map risks to known components or workflow steps. State uncertainty and limitations.
- Ground important claims in official sources or primary research.
- Keep final visuals local and traceable. Prefer original visuals and attribute reuse.
- Keep Markdown canonical. Generate the site from it.
- Keep examples small, safe, runnable, and linked to their chapters.
- Let scripts update operational metadata. Update `README.md` only when public facts change.
- Treat `PROJECT_STATUS.md` front matter as the operational source of truth. Never infer completion from files alone.
- Do not use em dashes.
