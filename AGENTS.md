# AGENTS file

Build a sequential, source-grounded, visual knowledge base about agentic AI and agentic AI security.

## Start every task

1. Read `PROJECT_STATUS.md` and `ROADMAP.md`.
2. If the user says to continue, resume the current unit or select `Next recommended unit`.
3. Follow `docs/autonomous-workflow.md` unless the user selects a different unit.
4. Work on one unit only. Never start the next unit in the same run unless explicitly requested.

## Read by task

- Scope: `docs/project-charter.md`
- Structure: `docs/information-architecture.md`
- Writing: `docs/style-guide.md`
- Sources: `docs/evidence-policy.md`
- Visuals: `docs/visuals-policy.md`
- Code: `docs/examples-policy.md`
- Chapters: `docs/chapter-template.md`
- Website: `docs/site-policy.md`
- Maintenance: `docs/maintenance.md`
- Autonomous work: `docs/autonomous-workflow.md`
- Roadmap rules: `docs/roadmap.md`

Also read the nearest local `AGENTS.md` in the directory you edit.

## Core rules

1. Assume the reader already knows what an LLM is.
2. Teach in dependency order, from agents to secure agentic systems.
3. Use simple English. Define technical terms and acronyms on first use.
4. Explain function before security.
5. Map every risk to a concrete component or workflow step.
6. Support important claims with official sources or primary research.
7. Prefer original visuals. Attribute every reused visual.
8. Keep Markdown canonical. Generate the website from Markdown.
9. Keep examples small, safe, runnable, and linked to chapters.
10. Do not use em dashes.
11. Update `README.md` after structural or progress changes.
12. State limitations and uncertainty clearly.
13. Update source records, visual metadata, `PROJECT_STATUS.md`, and `CHANGELOG.md` as required by the workflow.
14. Keep cited sources and visual assets local, traceable, and linked to the unit that uses them.
