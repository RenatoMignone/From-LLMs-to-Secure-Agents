# Contributing to From LLMs to Secure Agents

Thank you for helping improve the guide. Useful contributions include corrections, clearer explanations, source updates, accessibility fixes, site improvements, and small runnable examples.

For a substantial change, open an issue or start a discussion before investing significant time. Small corrections can go directly to a pull request. Please also read the [Code of Conduct](CODE_OF_CONDUCT.md), [governance model](GOVERNANCE.md), [editorial review guide](docs/editorial-review.md), and [AI assistance policy](docs/ai-assistance.md).

## Project invariants

1. Markdown under `knowledge/` is the canonical chapter source. Do not edit generated site content.
2. Important technical and security claims must resolve to records under `sources/`. Follow `docs/evidence-policy.md`.
3. Do not use em dash characters. Prefer shorter sentences, commas, colons, or parentheses.
4. Visuals must follow `docs/visuals-policy.md`. Store their prompts under the matching `assets/images/<chapter-path>/source/` directory. Do not add text-based diagrams to chapters.
5. Runnable examples belong under the matching `examples/<chapter-path>/` directory. Each implemented example needs a short README and automated tests.
6. Preserve the dependency order defined by the roadmap. Architecture is taught before detailed security.

## Development setup

### Prerequisites

- Python 3.11 or later
- Node.js 22.12 or later, with npm
- Git

The repository includes `.nvmrc` for Node version managers.

```bash
git clone https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents.git
cd From-LLMs-to-Secure-Agents

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements-dev.txt

npm --prefix site ci
```

Run the same quality gates used in continuous integration:

```bash
python scripts/main.py validate
python -m pytest -q
npm --prefix site run quality
```

## Propose a change

- Use a bug report for broken behavior, links, layout, or tooling.
- Use content feedback for a factual issue, unclear explanation, or accessibility concern.
- Use a source proposal for authoritative material that supports or challenges a claim.
- Use a discussion for questions, broad ideas, or changes to the information architecture.
- Report sensitive defects privately according to `SECURITY.md`.

Issues should describe the reader or maintainer problem, the relevant path or URL, and the expected result. A proposed solution is welcome but not required.

## Add or update a source

Do not write source YAML by hand. Open the canonical material, identify the exact claim it supports and its limitations, then use the source command:

```bash
python scripts/main.py source --help
```

The command records fields such as `canonical_url`, `authors_or_organization`, `source_type`, `date`, `accessed`, `claims_supported`, and `limitations` in the current schema. Add the resulting source identifier to the chapter front matter and cite it near the supported claim.

## Add or update an example

An implemented example should include:

- a focused module or harness that runs without external credentials;
- a `README.md` with purpose, requirements, and execution instructions;
- tests under `tests/test_*.py` that are discovered by the repository-wide pytest run;
- safe defaults and explicit boundaries for side effects.

Directories containing only `.gitkeep` are roadmap mirrors, not incomplete implementations.

## Use AI assistance responsibly

AI-assisted contributions are welcome, but the contributor remains responsible for every submitted change. Review generated prose and code, open cited sources, run the quality gates, and disclose material AI assistance in the pull request. See `docs/ai-assistance.md` for the complete policy.

## Submit a pull request

1. Branch from current `main`.
2. Keep the change focused and use clear conventional commits, such as `docs: clarify tool execution boundaries`.
3. Add or update tests when behavior changes.
4. Run all quality gates.
5. Complete the pull request template and call out limitations or follow-up work.

Maintainers may ask for revisions when a change is out of sequence, weakly sourced, inaccessible, too broad, or difficult to maintain. A closed proposal can be reconsidered when its prerequisites or evidence change.
