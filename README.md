# From LLMs to Secure Agents

A sequential, visual, source-grounded knowledge base about how agentic AI systems work, how they are built, how they fail, and how to secure them.

## Reader assumptions

The reader already understands:

- large language models;
- prompts and context windows;
- basic API use;
- basic Python.

## Learning path

### Pass 1: Understand the complete agentic system

1. From LLM calls to agents
2. Agent architectures
3. Core building blocks
4. Frameworks and protocols
5. One complete end-to-end workflow

### Pass 2: Secure the system

6. Threat model
7. Security by component and workflow stage
8. Preventive, detective, and recovery controls
9. Security tests and secure reference architectures
10. Evaluation, assurance, and open research questions

Detailed security begins only after the complete architecture and end-to-end workflows are understood.

## Curriculum structure

```text
knowledge/
  00-prerequisites/
  01-agent-foundations/
  02-agent-architectures/
  03-building-blocks/
  04-frameworks-and-protocols/
  05-end-to-end-workflows/
  06-threat-model/
  07-security-by-component-and-workflow-stage/
  08-secure-reference-architectures/
  09-security-testing-evaluation-and-assurance/
  10-open-research-questions/
```

Every curriculum directory contains a local `AGENTS.md` and `chapter-plan.md`. These define scope, prerequisites, sources, visuals, examples, security boundaries, and completion criteria without containing final chapter prose.

## Autonomous workflow

Future agents read `PROJECT_STATUS.md`, resume the current unit or select the next unblocked unit in `ROADMAP.md`, complete only that unit, update project state, and stop. Each run fetches and verifies the unit's sources, creates its source records, adds its required local visuals and examples, validates the repository, and records the next checkpoint. See `docs/autonomous-workflow.md`.

Use this resume prompt:

```text
Read AGENTS.md and continue the work from the last checkpoint.
```

Run the deterministic repository checks with:

```bash
python3 scripts/validate_repo.py
```

Visuals are stored by unit under `assets/<unit-id-lowercase>/`. The project prefers code-native diagrams and plots, permits license-checked downloads, and uses the installed image generation skill for suitable illustrations. Every final visual is local and registered in `assets/attribution.yml`.

## Repository

```text
AGENTS.md
README.md
PROJECT_STATUS.md  Current operational state
ROADMAP.md         Stable ordered unit queue
CHANGELOG.md       Concise completed-change history
docs/       Project rules
knowledge/  Canonical chapters
examples/   Runnable examples and labs
sources/    Source records
assets/     Visuals and attribution
scripts/    Repository validation
site/       Static site files
```

## Status

- Project rules and autonomous source and visual workflow: ready
- Curriculum plans: ready
- Knowledge chapters: not started
- Examples: not started
- Website: not started
