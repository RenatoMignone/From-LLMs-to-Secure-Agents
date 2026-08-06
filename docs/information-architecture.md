# Information Architecture

## Top-level path

```text
knowledge/
  00-prerequisites/
  # Pass 1: Understand the complete agentic system
  01-agent-foundations/
  02-agent-architectures/
  03-building-blocks/
  04-frameworks-and-protocols/
  05-end-to-end-workflows/
  # Pass 2: Secure the system
  06-threat-model/
  07-security-by-component-and-workflow-stage/
  08-secure-reference-architectures/
  09-security-testing-evaluation-and-assurance/
  10-open-research-questions/
```

## Substantial branches

```text
03-building-blocks/
  01-models-and-routing/
  02-context-construction/
  03-planning-and-reasoning/
  04-state-and-lifecycle/
  05-memory/
  06-retrieval-and-rag/
  07-tools-and-function-calling/
  08-identity-authorization-and-secrets/
  09-execution-environments/
  10-human-in-the-loop/
  11-observability-and-tracing/
  12-evaluation-and-benchmarks/
  13-multi-agent-systems/
  14-learning-and-self-improvement/
  15-reliability-and-operations/
  16-artifacts-and-multimodal-io/
```

```text
04-frameworks-and-protocols/
  01-frameworks/
  02-model-context-protocol/
  03-agent-to-agent-protocols/
```

```text
07-security-by-component-and-workflow-stage/
  01-instructions-context-and-models/
  02-retrieval-memory-and-data/
  03-tools-identity-and-credentials/
  04-execution-and-supply-chain/
  05-human-interfaces-and-observability/
  06-multi-agent-and-protocols/
  07-end-to-end-attack-paths/
```

## Planning files

Every directory shown above contains `AGENTS.md` and `chapter-plan.md`. Create chapter files only when their roadmap unit is selected.

## Unit artifacts

```text
sources/<source-id>.yml
assets/attribution.yml
assets/images/
  repo-images/<repository-image>
  <chapter-id>/
    <final-visual>
    manifest.yml
    source/<editable-input>
examples/<unit-id-lowercase>/
```

Use the chapter's lowercase `unit_id` as `chapter-id`. Give each chapter one image folder, and do not create it until the selected chapter requires a visual.

Each image folder owns its visual metadata. `assets/attribution.yml` indexes those local manifests.

## File rules

- Use numbered prefixes for reading order.
- Use lowercase kebab-case names.
- Keep one main concept per file.
- Split files that mix separate learning goals.
- Use nested directories only when the topic needs them.
- Do not create decorative empty directories.
- Keep detailed risks, controls, recovery, and security tests in Pass 2.
- Link architecture security previews forward and security chapters back.
