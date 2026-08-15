# Knowledge Instructions

- Purpose: hold the canonical two-pass guide and, later, its chapters.
- Reader prerequisite: working familiarity with large language models and prompts. API and Python experience is helpful, not required.
- May assume: only concepts completed earlier in `ROADMAP.md`.
- Do not cover yet: detailed security before Pass 1 is complete, or any unit not selected for the current run.
- Terminology: use the canonical terms defined by earlier sections; define new terms once.
- Required links: every unit links to prerequisites, its section plan, and the next relevant section.
- Security scope: Pass 1 permits only short forward-linked previews; detailed security belongs in Pass 2.

Rules:

- Use `scripts/main.py state resolve`; do not load the full roadmap.
- Work only on the resolved unit and run mode.
- Read the nearest local `AGENTS.md` and `chapter-plan.md`.
- Create `index.md` only when its roadmap unit is selected.
- Always read style and evidence policies. Personalize chapter structure to the topic, keeping core sections and omitting empty placeholders.
- Read visuals or examples policy only when the plan requires that artifact.
- Link prerequisites and next steps; avoid duplicate explanations.
- Pass 1 explains function before its brief security preview. Pass 2 maps threats and controls to taught components.
