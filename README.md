![From LLMs to Secure Agents: a three-stage path from a basic language model to an agentic system and then a secured agentic system](assets/images/repo-images/banner.png)

<div align="center">

<h1>From LLMs to Secure Agents</h1>

<p><strong>A deep, visual, source-grounded guide to understanding complete agentic AI systems and learning how to secure them.</strong></p>

<p><a href="ROADMAP.md"><img alt="Guide organized in two passes" src="https://img.shields.io/badge/guide-2_passes-2f80ed?style=flat-square"></a> <a href="ROADMAP.md"><img alt="180 ordered guide units" src="https://img.shields.io/badge/guide_units-180-14a38b?style=flat-square"></a> <a href="docs/evidence-policy.md"><img alt="Source-grounded content" src="https://img.shields.io/badge/evidence-source_grounded-6c63b5?style=flat-square"></a> <a href="docs/visuals-policy.md"><img alt="Local and attributed visuals" src="https://img.shields.io/badge/visuals-local_%26_attributed-e5a93d?style=flat-square"></a></p>

<p>Architecture first · Security second · Sources and visuals traced</p>

</div>

## The idea

Agent security is difficult to learn from isolated vulnerability lists. This project first builds a **complete mental model of an agentic system**, including architecture, context, memory, retrieval, tools, identity, execution, human control, observability, protocols, and end-to-end workflows. It then revisits the same system through a **threat model, controls, tests, and secure reference architectures**.

The guide assumes **working familiarity with large language models and prompts**. It gives only short refreshers when an agentic concept needs them. API and Python experience helps, but is not required. The focus is the agentic system, not model internals or prompt engineering.

The presentation combines **precise technical writing** with clear diagrams, reproducible plots, and approachable illustrations. It also maps current engineering vocabulary to stable system concepts, so terms such as context engineering, harness engineering, and loop engineering remain useful instead of becoming detached trend labels. Illustrations support technical detail and evidence.

## Two learning passes

| Pass | Goal | Main sections |
| --- | --- | --- |
| **1. Understand** | Explain how the complete system works | foundations, architectures, building blocks, frameworks, protocols, end-to-end workflows |
| **2. Secure** | Revisit that system through concrete threats and controls | threat model, component risks, attack paths, secure architectures, testing and assurance |

**Detailed security starts only after Pass 1 is complete.** Architecture chapters contain a short security preview that links forward.

## Guide structure

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

Every guide directory has a local `AGENTS.md` and `chapter-plan.md`. Together they define scope, prerequisites, teaching order, sources, visuals, examples, and the boundary between the two passes.

## Reproducible autonomous workflow

A future agent can resume from machine-readable project state, resolve the next unit, research and write **only that unit**, fetch or create its visuals, validate it, and stop at review. A separate continuation reviews and completes that unit before the guide advances.

```text
Read AGENTS.md and continue the guide from the last checkpoint.
```

Each completed unit includes:

- checked source records with exact claims and canonical links;
- local, attributed visuals, with reproducible diagrams and plots where possible;
- small runnable examples when the plan requires them;
- deterministic repository validation;
- updated project state and a concise changelog entry.

Run the validator with:

```bash
python3 scripts/validate_repo.py
```

## Authoring and publishing

**Markdown is the canonical knowledge format.** It stays readable in GitHub, keeps reviews and citations clear, and costs less context than repeated page markup. The future static site will generate semantic HTML and add CSS, JavaScript, navigation, search, themes, and interactive features from that source. See the [site policy](docs/site-policy.md).

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Compact entry point for every agent run |
| `PROJECT_STATUS.md` | Operational progress and resume state |
| `ROADMAP.md` | Stable dependency-ordered guide |
| `docs/` | Focused project policies |
| `knowledge/` | Canonical chapters and local plans |
| `sources/` | Verified source records |
| `assets/images/` | One local image folder per chapter, plus repository images |
| `assets/attribution.yml` | Index of chapter-local visual manifests |
| `scripts/` | State automation, validation, generation, and regression tests |
| `examples/` | Runnable examples and security labs |
| `site/` | Future static site implementation |
