# Security by Component and Workflow Stage Plan

## Section purpose

Apply the shared threat model to every Pass 1 component and workflow step.

## Learning outcomes

The reader can locate each risk, explain its preconditions and impact, and select preventive, detective, and recovery controls with stated limitations.

## Prerequisites

[Threat model](../06-threat-model/chapter-plan.md).

## Planned child sections

1. [Instructions, context, and models](01-instructions-context-and-models/chapter-plan.md)
2. [Retrieval, memory, and data](02-retrieval-memory-and-data/chapter-plan.md)
3. [Tools, identity, and credentials](03-tools-identity-and-credentials/chapter-plan.md)
4. [Execution and supply chain](04-execution-and-supply-chain/chapter-plan.md)
5. [Human interfaces and observability](05-human-interfaces-and-observability/chapter-plan.md)
6. [Multi-agent systems and protocols](06-multi-agent-and-protocols/chapter-plan.md)
7. [End-to-end attack paths](07-end-to-end-attack-paths/chapter-plan.md)
8. [Governance and secure lifecycle](08-governance-and-secure-lifecycle/chapter-plan.md)

## Required concepts

Follow runtime data flow. For each boundary: normal function, failure, attack preconditions, impact, prevention, detection, recovery, residual risk, and test hook. Finish with compound attack paths and lifecycle governance.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Taxonomy-only lists, controls detached from architecture, and finalized reference architectures.

## Required diagrams or visuals

- Visual: component-risk-control matrix and layered attack-path diagrams.
- Example: safe, non-destructive test cases and policy pseudocode.
- Framework examples: use official guardrail and authorization hooks only as translations.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: OWASP, NIST, MITRE ATLAS, official protocol security guidance, official advisories, and peer-reviewed attack and defense papers. Candidate sources appear in child plans.

Candidate primary sources:

- [OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [NIST Adversarial Machine Learning taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [MITRE ATLAS](https://atlas.mitre.org/)

## Connections to later security chapters

Control sets feed [secure reference architectures](../08-secure-reference-architectures/chapter-plan.md) and their test hooks feed [security assurance](../09-security-testing-evaluation-and-assurance/chapter-plan.md).

## Open questions

Maintain a crosswalk so overlapping taxonomies do not create duplicate chapters.

## Completion criteria

Every Pass 1 component and workflow stage has at least one explicit risk review, and every control maps to a stated threat and test.
