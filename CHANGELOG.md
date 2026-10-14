# Changelog

## 2026-10-10

### Dependency alerts and bot pull requests

- Files or sections: site package manifest and lockfile, custom mobile navigation, Python development requirements and pinned GitHub Actions.
- Summary: Applied the reviewed bot updates directly on main, refreshed additional vulnerable transitive dependencies, scoped a patched selector-parser override, and adapted the custom menu to Starlight's native popover. Details are recorded in `docs/dependency-review-2026-10-10.md`.
- Validation: Clean install and npm/pip audits report zero known vulnerabilities. Passed Python and site tests, repository validation, site build/integrity checks and Chrome navigation checks.

### Readability and architecture review

- Files or sections: 51 published chapters, eight section plans, source records, four example folders, two replacement illustrations, editorial policies and README.
- Summary: Added concrete introductions and comprehension checks, rewrote memory/state/RAG explanations, corrected unsupported guarantees and source attribution, and documented managed harnesses, programmatic tools and mid-turn steering. Updated planned coverage for current MCP, skills, multi-session continuity, interactive modalities and harness evaluation without changing the 99-unit curriculum.
- Validation: Passed 38 published Python examples, 21 repository regression tests and two site pipeline tests. Repository validation checked 51 chapters, 107 visuals and 177 source records; built and checked the site. Review scope and limitations are recorded in `docs/editorial-review-2026-10-10.md`.

## 2026-09-04

### Curriculum scope reduction

- Files or sections: roadmap, local chapter plans and instructions, visual and artifact policies, validator, tests, and README
- Summary: Reduced the committed guide from 209 to 99 units while preserving the 38 existing chapters, the two-pass architecture-to-security model, and complete component coverage. Consolidated future chapters, moved specialized material into 23 deep dives, deferred volatile surveys, and replaced the fixed visual quota with purpose-driven illustrations.
- Validation: Passed repository validation for 99 roadmap units and checked state resolution at the unchanged next unit. Removed obsolete planned-unit artifact placeholders and limited mirrored folders to started chapters.

### Pending chapter visuals completed

- Files or sections: memory consolidation chapter, RAG ingestion chapter, image prompts, and generated site content
- Summary: Added and reviewed three purpose-driven visuals to each of the two existing chapters that had pending image tasks, then removed the resolved quota note.
- Validation: Inspected all six illustrations for labels and technical meaning, replaced three flawed memory drafts, ran the chapter examples, passed repository validation, and rebuilt and checked the site.

## 2026-08-05

### Curriculum checkpoint

- Files or sections: instruction policies, knowledge curriculum plans, project state files, and README
- Summary: Added a researched two-pass curriculum and autonomous one-unit workflow.
- Validation: Checked required planning files, sequence boundary, internal links, source candidates, and em dashes.

### Autonomous production checkpoint

- Files or sections: source policy, visual policy, workflow, templates, metadata, validator, state, and README
- Summary: Added resumable per-unit source acquisition, visual download and generation, provenance, and deterministic validation.
- Validation: Ran repository, link, curriculum boundary, source-record, visual-ownership, style, and Git checks.

### Repository presentation checkpoint

- Files or sections: root instructions, site policy, README, project banner, visual attribution, and project status
- Summary: Kept Markdown canonical, compacted the recurring run contract, and added a generated project identity and clearer repository overview.
- Validation: Checked the banner, attribution, links, policy consistency, instruction size, repository validation, and GitHub metadata.

### Image layout checkpoint

- Files or sections: visual storage policies, workflow, attribution, status, and README
- Summary: Adopted one `assets/images/<chapter-id>/` folder per chapter and registered the new repository banner.
- Validation: Checked image paths, banner metadata and checksum, internal links, style, and repository validation.

### Visual identity checkpoint

- Files or sections: README, visual policy, asset rules, and site policy
- Summary: Defined the approachable technical illustration style and added focused repository badges to a restrained README header.
- Validation: Checked badge targets, README rendering structure, policy consistency, internal links, style, and repository validation.

### README presentation refinement

- Files or sections: README
- Summary: Positioned the project as a deep technical guide, added compact structural badges, and removed operational checkpoint details from the project overview.
- Validation: Checked badge targets, layout structure, internal links, style, and repository validation.

### Reader scope refinement

- Files or sections: charter, instructions, style, chapter planning, project status, and README
- Summary: Set working LLM familiarity as the baseline and limited LLM coverage to brief refreshers needed for agentic topics.
- Validation: Checked scope language, internal links, style, and repository validation.

## 2026-08-06

### Automated production controls

- Files or sections: workflow, machine-readable state, state and provenance helpers, schemas, validator, CI, visual manifests, guide plans, and README
- Summary: Added script-driven unit progression and provenance registration with separate review, strict validation, continuous integration, protected main history, and pinned Actions.
- Validation: Passed repository validation, eleven regression tests, syntax checks, link checks, checksum checks, and style checks.

### Instruction context compression

- Files or sections: root and local instructions, autonomous workflow, artifact policies, state resolver, tests, changelog, and README
- Summary: Reduced recurring context with exact unit routing, conditional artifact policies, script-owned metadata, and unambiguous author, review, and blocked runs.
- Validation: Passed repository validation, thirteen regression tests, syntax checks, link checks, style checks, and enforced instruction-size budgets.

### Current field vocabulary

- Files or sections: research and maintenance workflow, evidence and style policies, chapter guidance, relevant Pass 1 plans, roadmap, and README
- Summary: Added controlled discovery and teaching of emerging practitioner terms, including context, harness, and loop engineering, without treating social posts as technical proof.
- Validation: Checked source provenance rules, prerequisite placement, internal links, instruction budgets, style, and repository tests.

### P1-00-01 complete

- Files or sections: `knowledge/00-prerequisites/01-reader-contract-and-system-map.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Reader contract and system map.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-10

### P1-00-02 complete

- Files or sections: `knowledge/00-prerequisites/02-data-control-and-trust-boundaries.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Data, control, and trust boundaries.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-12

### Chapter-mirrored image hierarchy

- Files or sections: image assets, chapter references, visual registration and validation, workflow policies, regression tests, and README
- Summary: Replaced flat unit-ID image folders with an asset hierarchy that mirrors every planned chapter and subchapter path.
- Validation: Passed repository validation, 21 regression tests, Python syntax checks, stale-path checks, and Git diff checks.

### P1-00-03 complete

- Files or sections: `knowledge/00-prerequisites/03-requests-events-state-and-side-effects.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Requests, events, state, and side effects.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-15

### P1-00-04 complete

- Files or sections: `knowledge/00-prerequisites/04-identity-authority-and-least-privilege-primer.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Identity, authority, and least privilege primer.
- Validation: Passed repository validation and the unit review checklist.

### P1-01-01 complete

- Files or sections: `knowledge/01-agent-foundations/01-what-is-an-agent.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed What is an agent.
- Validation: Passed repository validation and the unit review checklist.

### P1-01-02 complete

- Files or sections: `knowledge/01-agent-foundations/02-the-agent-loop.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed The agent loop.
- Validation: Passed repository validation and the unit review checklist.

### P1-01-03 complete

- Files or sections: `knowledge/01-agent-foundations/03-workflows-versus-agents.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Workflows versus agents.
- Validation: Passed repository validation and the unit review checklist.

### P1-01-04 complete

- Files or sections: `knowledge/01-agent-foundations/04-goals-policies-environments-and-autonomy.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Goals, policies, environments, and autonomy.
- Validation: Passed repository validation and the unit review checklist.

### P1-01-05 complete

- Files or sections: `knowledge/01-agent-foundations/05-run-lifecycle-and-termination.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Run lifecycle and termination.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-17

### P1-02-01 complete

- Files or sections: `knowledge/02-agent-architectures/01-architecture-selection-criteria.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Architecture selection criteria.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-02 complete

- Files or sections: `knowledge/02-agent-architectures/02-single-agent-and-reactive-loops.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Single-agent and reactive loops.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-03 complete

- Files or sections: `knowledge/02-agent-architectures/03-sequential-routing-and-parallel-workflows.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Sequential, routing, and parallel workflows.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-04 complete

- Files or sections: `knowledge/02-agent-architectures/04-plan-and-execute.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Plan and execute.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-05 complete

- Files or sections: `knowledge/02-agent-architectures/05-evaluator-optimizer-and-reflection.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Evaluator-optimizer and reflection.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-06 complete

- Files or sections: `knowledge/02-agent-architectures/06-state-machines-and-event-driven-graphs.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed State machines and event-driven graphs.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-07 complete

- Files or sections: `knowledge/02-agent-architectures/07-supervisors-handoffs-and-agent-as-tool.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Supervisors, handoffs, and agent-as-tool.
- Validation: Passed repository validation and the unit review checklist.

### P1-02-08 complete

- Files or sections: `knowledge/02-agent-architectures/08-architecture-trade-offs.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Architecture trade-offs.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-01-01 complete

- Files or sections: `knowledge/03-building-blocks/01-models-and-routing/01-model-roles-and-selection.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Model roles and selection.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-01-02 complete

- Files or sections: `knowledge/03-building-blocks/01-models-and-routing/02-routing-cascades-and-fallbacks.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Routing, cascades, and fallbacks.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-18

### P1-03-01-03 complete

- Files or sections: `knowledge/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Capability, cost, latency, and reliability.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-01-04 complete

- Files or sections: `knowledge/03-building-blocks/01-models-and-routing/04-routing-evaluation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Routing evaluation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-02-01 complete

- Files or sections: `knowledge/03-building-blocks/02-context-construction/01-context-sources-and-precedence.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Context sources and precedence.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-02-02 complete

- Files or sections: `knowledge/03-building-blocks/02-context-construction/02-context-budgets-selection-and-ordering.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Context budgets, selection, and ordering.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-02-03 complete

- Files or sections: `knowledge/03-building-blocks/02-context-construction/03-history-summaries-and-compression.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed History, summaries, and compression.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-02-04 complete

- Files or sections: `knowledge/03-building-blocks/02-context-construction/04-provenance-and-context-debugging.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Provenance and context debugging.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-03-01 complete

- Files or sections: `knowledge/03-building-blocks/03-planning-and-reasoning/01-reactive-and-reason-act-patterns.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Reactive and reason-act patterns.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-21

### P1-03-03-02 complete

- Files or sections: `knowledge/03-building-blocks/03-planning-and-reasoning/02-decomposition-and-plan-execute.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Decomposition and plan-execute.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-24

### P1-03-03-03 complete

- Files or sections: `knowledge/03-building-blocks/03-planning-and-reasoning/03-reflection-evaluation-and-replanning.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Reflection, evaluation, and replanning.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-03-04 complete

- Files or sections: `knowledge/03-building-blocks/03-planning-and-reasoning/04-search-budgets-and-termination.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Search, budgets, and termination.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-04-01 complete

- Files or sections: `knowledge/03-building-blocks/04-state-and-lifecycle/01-run-thread-and-event-models.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Run, thread, and event models.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-04-02 complete

- Files or sections: `knowledge/03-building-blocks/04-state-and-lifecycle/02-checkpoints-interrupts-and-resumption.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Checkpoints, interrupts, and resumption.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-04-03 complete

- Files or sections: `knowledge/03-building-blocks/04-state-and-lifecycle/03-retries-idempotency-and-concurrency.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Retries, idempotency, and concurrency.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-04-04 complete

- Files or sections: `knowledge/03-building-blocks/04-state-and-lifecycle/04-termination-cancellation-and-cleanup.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Termination, cancellation, and cleanup.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-29

### P1-03-05-01 complete

- Files or sections: `knowledge/03-building-blocks/05-memory/01-memory-versus-context-and-state.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Memory versus context and state.
- Validation: Passed repository validation and the unit review checklist.

## 2026-08-31

### P1-03-05-02 complete

- Files or sections: `knowledge/03-building-blocks/05-memory/02-short-term-and-working-memory.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Short-term and working memory.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-05-03 complete

- Files or sections: `knowledge/03-building-blocks/05-memory/03-persistent-memory-types-and-lifecycle.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Persistent memory types and lifecycle.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-05-04 complete

- Files or sections: `knowledge/03-building-blocks/05-memory/04-consolidation-forgetting-and-evaluation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Consolidation, forgetting, and evaluation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-06-01 complete

- Files or sections: `knowledge/03-building-blocks/06-retrieval-and-rag/01-rag-system-and-ingestion.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed RAG system and ingestion.
- Validation: Passed repository validation and the unit review checklist.

## 2026-09-12

### P1-03-06-02 complete

- Files or sections: `knowledge/03-building-blocks/06-retrieval-and-rag/02-sparse-dense-and-hybrid-retrieval.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Sparse, dense, and hybrid retrieval.
- Validation: Passed repository validation and the unit review checklist.

## 2026-09-13

### P1-03-06-03 complete

- Files or sections: `knowledge/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Chunking, ranking, and advanced retrieval.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-06-04 complete

- Files or sections: `knowledge/03-building-blocks/06-retrieval-and-rag/04-grounding-long-context-and-retrieval-evaluation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Grounding, long context, and retrieval evaluation.
- Validation: Passed repository validation and the unit review checklist.

## 2026-10-10

### P1-03-07-01 complete

- Files or sections: `knowledge/03-building-blocks/07-tools-and-function-calling/01-tool-capabilities-schemas-selection-and-dispatch.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Tool capabilities, schemas, selection, and dispatch.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-07-02 complete

- Files or sections: `knowledge/03-building-blocks/07-tools-and-function-calling/02-results-failures-side-effects-and-confirmation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Results, failures, side effects, and confirmation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-08-01 complete

- Files or sections: `knowledge/03-building-blocks/08-identity-authorization-and-secrets/01-identity-authentication-authorization-and-delegation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Identity, authentication, authorization, and delegation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-08-02 complete

- Files or sections: `knowledge/03-building-blocks/08-identity-authorization-and-secrets/02-workload-identity-credentials-and-revocation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Workload identity, credentials, and revocation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-09-01 complete

- Files or sections: `knowledge/03-building-blocks/09-execution-environments/01-execution-boundaries-isolation-and-sandboxes.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Execution boundaries, isolation, and sandboxes.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-09-02 complete

- Files or sections: `knowledge/03-building-blocks/09-execution-environments/02-browsers-files-networks-resources-and-cleanup.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Browsers, files, networks, resources, and cleanup.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-10-01 complete

- Files or sections: `knowledge/03-building-blocks/10-human-in-the-loop/01-human-control-approval-and-escalation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Human control, approval, and escalation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-10-02 complete

- Files or sections: `knowledge/03-building-blocks/10-human-in-the-loop/02-interrupts-steering-feedback-and-operator-experience.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Interrupts, steering, feedback, and operator experience.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-11-01 complete

- Files or sections: `knowledge/03-building-blocks/11-observability-and-tracing/01-events-traces-metrics-and-correlation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Events, traces, metrics, and correlation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-11-02 complete

- Files or sections: `knowledge/03-building-blocks/11-observability-and-tracing/02-lineage-replay-redaction-retention-and-integrations.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Lineage, replay, redaction, retention, and integrations.
- Validation: Passed repository validation and the unit review checklist.

## 2026-10-14

### P1-03-12-01 complete

- Files or sections: `knowledge/03-building-blocks/12-evaluation-and-benchmarks/01-evaluation-levels-test-design-and-metrics.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Evaluation levels, test design, and metrics.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-12-02 complete

- Files or sections: `knowledge/03-building-blocks/12-evaluation-and-benchmarks/02-benchmarks-regression-and-release-evaluation.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Benchmarks, regression, and release evaluation.
- Validation: Passed repository validation and the unit review checklist.

### P1-03-13-01 complete

- Files or sections: `knowledge/03-building-blocks/13-multi-agent-systems/01-multi-agent-roles-delegation-and-coordination.md` and its evidence, visuals, or examples
- Summary: Completed and reviewed Multi-agent roles, delegation, and coordination.
- Validation: Passed repository validation and the unit review checklist.
