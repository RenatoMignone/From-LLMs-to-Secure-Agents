# Retrieval, Memory, and Data Security Plan

## Section purpose

Analyze how untrusted, stale, unauthorized, or poisoned data enters and persists in agent decisions.

## Learning outcomes

Model ingestion and corpus poisoning, embedding and index manipulation, access-filter failures, retrieval injection, provenance loss, memory poisoning, privacy leakage, retention failure, and cross-tenant exposure.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 retrieval, memory, and artifact sections.

## Planned child chapters

1. `01-ingestion-corpus-and-index-attacks.md`
2. `02-retrieval-manipulation-and-access-control.md`
3. `03-memory-poisoning-persistence-and-forgetting.md`
4. `04-data-privacy-provenance-and-lifecycle.md`
5. `05-controls-tests-and-recovery.md`

## Required concepts

Corpus poisoning, index poisoning, retrieval manipulation, memory poisoning, access filter, provenance, tenant boundary, retention, deletion, and data lineage.

## Concepts explicitly out of scope

General prompt injection already covered earlier and tool-execution internals.

## Recommended teaching order

Follow data from ingestion to index, retrieval, context, memory write, later recall, and deletion; apply controls at each transition.

## Required diagrams or visuals

Data lineage with enforcement points and poisoning persistence timeline.

## Recommended examples

Safe poisoned-document fixture, tenant-filter tests, provenance checks, memory quarantine, and deletion verification.

## Sources

Authoritative source categories: OWASP guidance, NIST privacy and adversarial machine learning guidance, and primary injection research.

Candidate primary sources:

- [OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [Indirect prompt injection research](https://arxiv.org/abs/2302.12173)
- [Agent Security Bench](https://openreview.net/pdf?id=V4y0CpX4hK)

## Connections to later security chapters

Feeds [end-to-end attack paths](../07-end-to-end-attack-paths/chapter-plan.md) and data controls in [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

How can memory usefulness, provenance, privacy, and poisoning resistance be measured together?

## Completion criteria

Every persistent data path has source trust, authorization, validation, provenance, retention, detection, quarantine, deletion, and recovery tests.
