![From LLMs to Secure Agents: a three-stage path from a basic language model to an agentic system and then a secured agentic system](assets/images/repo-images/banner.png)

<div align="center">

<h1>From LLMs to Secure Agents</h1>

<p><strong>A growing visual and source-grounded guide to understanding agentic AI systems and learning how to secure them.</strong></p>

<p><a href="https://renatomignone.github.io/From-LLMs-to-Secure-Agents/"><img alt="Documentation website" src="https://img.shields.io/badge/docs-live_site-14a38b?style=flat-square"></a> <a href="ROADMAP.md"><img alt="Guide organized in two passes" src="https://img.shields.io/badge/guide-2_passes-2f80ed?style=flat-square"></a> <a href="docs/evidence-policy.md"><img alt="Source-grounded content" src="https://img.shields.io/badge/evidence-source_grounded-6c63b5?style=flat-square"></a> <a href="docs/visuals-policy.md"><img alt="Local and attributed visuals" src="https://img.shields.io/badge/visuals-local_%26_attributed-e5a93d?style=flat-square"></a></p>

<p>Architecture first · Security second · Sources and visuals traced</p>

</div>

## The idea

Agent security is difficult to learn from isolated vulnerability lists. This project first builds a **complete mental model of an agentic system**, including architecture, context, memory, retrieval, tools, identity, execution, human control, observability, protocols, and end-to-end workflows. It then revisits the same system through a **threat model, controls, tests, and secure reference architectures**.

![From LLMs to Secure Agents: Core Purpose and Mental Model](assets/images/repo-images/project-purpose.png)

The guide assumes **working familiarity with large language models and prompts**. It gives only short refreshers when an agentic concept needs them. API and Python experience helps, but is not required. The focus is the agentic system, not model internals or prompt engineering.

The reader follows a focused **main path** through the complete system. Specialized mechanisms and implementation detail live in clearly labeled **deep-dive branches** that can remain collapsed until needed. Additional vendor, protocol, regulatory, sector, and research topics are deferred unless they materially improve the stable system model.

The presentation combines **precise technical writing** with clear diagrams, reproducible plots, and approachable illustrations. It also maps current engineering vocabulary to stable system concepts, so terms such as context engineering, harness engineering, and loop engineering remain useful instead of becoming detached trend labels.

## Current status

The project is in **early alpha**. The first, architecture-focused learning pass is in progress. The detailed threat modeling and security chapters are planned but are not yet presented as complete production guidance.

Published chapters, examples, and the website are usable now, but their depth and editorial maturity vary. Check [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for the machine-maintained checkpoint and [`ROADMAP.md`](ROADMAP.md) for planned scope. See [`docs/ai-assistance.md`](docs/ai-assistance.md) for how AI-assisted work is reviewed and where its limits remain.

## Two learning passes

| Pass | Goal | Main sections |
| --- | --- | --- |
| **1. Understand** | Explain how the complete system works | foundations, architectures, building blocks, policy, lifecycle, interfaces, protocols, workflows |
| **2. Secure** | Revisit that system through concrete threats and controls | threat model, component risks, governance, secure lifecycle, reference architectures, assurance |

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

## Maintaining the guide

Repository work is scoped to one guide unit at a time. Machine-readable state identifies the current unit, while local plans define its sources, visuals, examples, and review criteria. See [`AGENTS.md`](AGENTS.md) for the workflow and [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup and review requirements.

```bash
# Resolve the current unit
python3 scripts/main.py state resolve

# Check repository consistency
python3 scripts/main.py validate
```

## Publishing and static website

**Markdown under `knowledge/` is the canonical knowledge format.** The static website is a deterministic projection of this knowledge base built with Astro and Starlight, deployed to GitHub Pages at:

🔗 **[renatomignone.github.io/From-LLMs-to-Secure-Agents](https://renatomignone.github.io/From-LLMs-to-Secure-Agents/)**

The reader-facing site uses chapter titles and section-based identifiers rather than internal workflow IDs. It also provides responsive WebP illustrations, a published-learning-path overview, and local Continue Reading progress without an account or tracking service.

To develop or build the site locally:

```bash
cd site
npm ci
npm run dev    # Start local development server with auto-rebuilding pipeline
npm run build  # Build production static site to site/dist/
npm run check  # Verify site integrity, links, images, and endpoints
```

See [`docs/site-policy.md`](docs/site-policy.md) and [`site/AGENTS.md`](site/AGENTS.md) for publishing invariants.

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Compact entry point for every agent run |
| `PROJECT_STATUS.md` | Operational progress and resume state |
| `ROADMAP.md` | Stable dependency-ordered guide |
| `docs/` | Focused project policies |
| `knowledge/` | Canonical chapters and local plans |
| `sources/` | Verified source records mirroring the chapter hierarchy |
| `assets/images/` | Image folders mirroring the chapter hierarchy, plus repository images |
| `scripts/` | Modular CLI toolkit, validation suite, and regression tests |
| `examples/` | Runnable examples and security labs mirroring the chapter hierarchy |
| `site/` | Static documentation website (Astro & Starlight) |

## Project stewardship

- [`CONTRIBUTING.md`](CONTRIBUTING.md) explains setup, quality gates, sources, and contribution expectations.
- [`GOVERNANCE.md`](GOVERNANCE.md) explains how decisions and reviews work.
- [`SUPPORT.md`](SUPPORT.md) routes questions, defects, and sensitive reports.
- [`CITATION.cff`](CITATION.cff) provides citation metadata for the repository.
- [`docs/editorial-review.md`](docs/editorial-review.md) separates human editorial judgment from automated checks.
- [`docs/release-process.md`](docs/release-process.md) defines when a citable alpha release is ready.

## Author & Maintainer

**Renato Mignone** ([GitHub](https://github.com/RenatoMignone))
AI Systems & Security Researcher.

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), and [`docs/ai-assistance.md`](docs/ai-assistance.md) before submitting issues or pull requests.

## Security

Please report vulnerabilities confidentially according to [`SECURITY.md`](SECURITY.md).

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
