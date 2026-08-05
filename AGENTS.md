# Agent Instructions

Build a sequential, source-grounded, visual guide to agentic AI and its security.

## Run contract

1. Read `PROJECT_STATUS.md` and `ROADMAP.md`.
2. For a continuation request, resume `Current unit`; if none, select `Next recommended unit`.
3. Read the nearest local `AGENTS.md` and its `chapter-plan.md`.
4. Follow `docs/autonomous-workflow.md`. Complete one unit, update its checkpoint, then stop. Start another unit only when explicitly asked.

## Policy map

- Scope and structure: `docs/project-charter.md`, `docs/information-architecture.md`
- Prose and chapters: `docs/style-guide.md`, `docs/chapter-template.md`
- Sources, visuals, and code: `docs/evidence-policy.md`, `docs/visuals-policy.md`, `docs/examples-policy.md`
- Site and upkeep: `docs/site-policy.md`, `docs/maintenance.md`, `docs/roadmap.md`

Read only policies relevant to the selected unit.

## Invariants

- Assume the reader understands large language models. Define later terms and acronyms in simple English.
- Teach in dependency order. Finish functional architecture and workflows before detailed security.
- Map risks to known components or workflow steps. State uncertainty and limitations.
- Ground important claims in official sources or primary research.
- Keep final visuals local and traceable. Prefer original visuals and attribute reuse.
- Keep Markdown canonical. Generate the site from it.
- Keep examples small, safe, runnable, and linked to their chapters.
- Update source and visual records, `README.md`, `PROJECT_STATUS.md`, and `CHANGELOG.md` as the workflow requires.
- Do not use em dashes.
