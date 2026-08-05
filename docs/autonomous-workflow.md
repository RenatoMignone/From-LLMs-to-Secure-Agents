# Autonomous Workflow

This workflow makes the prompt "Read `AGENTS.md` and continue from the last checkpoint" sufficient to complete one unit.

## Resume contract

- If `Current unit` is set, resume it from `Current unit state`.
- Otherwise use `Next recommended unit` and verify its title and planned filename in the nearest `chapter-plan.md`.
- Inspect the worktree before editing. Preserve unrelated work.
- Set `Current unit`, `Current unit path`, and `Current unit state: researching` before collecting artifacts.
- A unit is complete only after its chapter, sources, visuals, examples, validation, and state updates are complete.

## Unit loop

1. Read root `AGENTS.md`, `PROJECT_STATUS.md`, and `ROADMAP.md`.
2. Use the user-selected unit, or select the first unblocked incomplete roadmap unit.
3. Read the nearest local `AGENTS.md`, its `chapter-plan.md`, and only the global policies they require.
4. Research only that unit. Turn its required concepts into research questions, search current authoritative sources, open every cited source, and create or update source records.
5. Write or revise only that unit using `docs/chapter-template.md`.
6. Add only the visuals and examples required by its plan. Choose an original diagram, reproducible plot, licensed download, or generated image by following `docs/visuals-policy.md`. Store every chapter visual under `assets/images/<chapter-id>/` and update `assets/attribution.yml`.
7. Validate content, links, source records, citations, local visual files, visual metadata, accessibility text, examples, terminology, pass boundaries, and em dashes. Run `python3 scripts/validate_repo.py`.
8. Update `README.md`, mark the unit complete in `PROJECT_STATUS.md`, set the next unblocked unit, and append one concise `CHANGELOG.md` entry.
9. Stop. Do not begin another unit unless the user explicitly requests it.

## Acquisition rules

- Candidate sources in a plan are leads, not evidence. Reopen and verify them for the current unit.
- Search results, snippets, and model memory are not citable sources.
- Do not hotlink images. Download an allowed copy or create a project-owned visual.
- If reuse rights are unclear, do not download the visual. Prefer an original diagram or generated illustration.
- Generated images follow the installed `imagegen` skill. Project-bound outputs must be copied into `assets/images/<chapter-id>/` and recorded.
- Technical diagrams and plots must be code-native and reproducible. Do not use image generation for precise topology, labels, or quantitative claims.

## Interrupted work

- Keep the current unit and state in `PROJECT_STATUS.md`.
- Keep verified source records and finished visual metadata even if prose is incomplete.
- On resume, inspect existing artifacts and continue from the recorded state. Do not repeat completed acquisition without a reason.

## Selection rules

- A unit is unblocked when all roadmap dependencies are complete and no blocker is recorded.
- If the current unit is in review, address only that review unless directed otherwise.
- Do not work across sections to fill incidental gaps. Record them as blockers or unresolved questions.
- Stop when the unit meets its plan, when review is required, or when evidence, authority, or a prerequisite is missing.
