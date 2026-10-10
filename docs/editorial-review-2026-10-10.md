# Editorial review: October 10, 2026

## Scope and review type

This author review follows the reader's request to improve readability and update the architecture coverage. It revises the 51 published chapters, with concrete openings where earlier introductions assumed too much systems vocabulary and one comprehension question with an expandable answer in every chapter. It does not represent independent technical or audience review. The 99-unit curriculum and completion checkpoint remain unchanged: 51 complete, 48 remaining.

## Corrections made

- Rewrote persistent memory, run/thread/event models, and grounding/retrieval evaluation around a concrete task and explicit implementation limits.
- Distinguished namespaces from authorization, in-memory dictionaries from durable stores, and record deletion from removal of every derived copy.
- Separated execution completion from task correctness, SDK state from managed services, and checkpoint replay from repeating external actions. Explained that a resumed LangGraph interrupt restarts its node.
- Removed universal correctness, latency and cost claims from architecture, routing, context and RAG comparisons. Research observations and illustrative configurations retain their scope.
- Corrected faithfulness scoring and single-query reciprocal rank. Added examples of missing evidence, lexical overlap that contradicts a claim, namespace-prefix collisions, expiry boundaries, reducer replay and missing tool handlers.
- Corrected context-engineering citation titles and publication dates, marked GenAI telemetry conventions as development, and identified the expired Idempotency-Key Internet-Draft as a draft rather than an RFC.
- Replaced misleading memory and architecture-selection illustrations using the built-in image generation tool; stored prompts beside the local WebP assets.

## Architecture coverage

| Topic | Published material or planned treatment |
| --- | --- |
| Managed harness, environment and application ownership | Run/thread chapter and execution boundaries; framework and reliability plans |
| Direct and programmatic tool calling | Tools chapter and offline comparison using the same dispatcher |
| Steering while a response runs | Human-control chapter, with provider and transport scope |
| Long-running work across sessions | Reliability and end-to-end plans: progress artifacts, recovery and checkable outcomes |
| Authored skill packages | Learning plan: progressive disclosure, versioning and distinction from learned skills or weight updates |
| MCP 2026-07-28 | Protocol plan: stateless requests, per-request capabilities, optional discovery and versioned legacy compatibility |
| Computer use and voice | Multimodal plan: observation, action, partial output, interruption and verification |
| Harness evaluation | Evaluation plan: fixed tasks, repeated trials and complete configuration reporting |

Future plans define required coverage; they are not published chapters or completed units. Official documentation was checked for the claims added in this review. Source records describe support and limitations; historical record identifiers do not determine publication dates.

## Validation

Repository structure, source records, links, runnable examples, regression tests and the generated site are checked before publication. Automated checks establish implementation and publishing consistency; they do not replace independent review or prove general task reliability.

Verified artifacts: 38 published Python examples, 21 repository regression tests, two publishing tests, 99-unit repository validation, and the site build and integrity check.

Replacement images: [memory namespaces](../assets/images/03-building-blocks/05-memory/03-persistent-memory-types-and-lifecycle/01-persistent-memory-taxonomy-and-namespaces.webp) and [architecture comparison](../assets/images/02-agent-architectures/08-architecture-trade-offs/03-measured-architecture-selection.webp). Their saved generation prompts are [memory prompt](../assets/images/03-building-blocks/05-memory/03-persistent-memory-types-and-lifecycle/source/01-persistent-memory-taxonomy-and-namespaces-v2-prompt.txt) and [architecture prompt](../assets/images/02-agent-architectures/08-architecture-trade-offs/source/03-measured-architecture-selection-prompt.txt). Both used the built-in image generation tool through the imagegen skill.
