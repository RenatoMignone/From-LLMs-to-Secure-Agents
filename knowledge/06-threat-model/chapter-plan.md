# Threat Model Plan

## Section purpose

Create the shared security model used by every later security chapter.

## Learning outcomes

The reader can define scope, assets, actors, trust boundaries, attacker goals, capabilities, access, lifecycle stages, abuse cases, security properties, and risk assumptions for the Pass 1 workflows.

## Prerequisites

The complete [end-to-end workflows](../05-end-to-end-workflows/chapter-plan.md).

## Planned child chapters

1. `01-system-scope-assets-and-security-properties.md`
2. `02-actors-identities-and-trust-boundaries.md`
3. `03-attacker-goals-capabilities-and-access.md`
4. `04-threat-modeling-method.md`
5. `05-agentic-threat-taxonomies-and-crosswalks.md`
6. `06-reference-workflow-threat-model.md`

## Required concepts

Freeze the system model first. Identify assets and desired properties. Map actors and authority. Define attacker knowledge, access, and capabilities. Apply data-flow and misuse-case analysis. Use OWASP, MITRE ATLAS, and NIST as cross-checks, not as the chapter structure.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Detailed component mitigations and secure reference designs.

## Required diagrams or visuals

- Visual: trust-boundary data-flow diagram, actor-authority matrix, attack tree, and taxonomy crosswalk.
- Example: a structured threat-model record for the Pass 1 reference workflow.
- Framework examples: none beyond boundary examples.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: security standards, official threat taxonomies, and agentic security guidance.

Candidate primary sources:

- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [OWASP multi-agent threat modeling guide](https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [MITRE ATLAS](https://atlas.mitre.org/)

## Connections to later security chapters

Every later security chapter must state which threat-model assumptions and workflow identifiers it uses.

## Open questions

OWASP agentic guidance is changing quickly. Record versions and reconcile taxonomy changes before drafting.

## Completion criteria

Every Pass 1 component and data flow is in scope or explicitly excluded, and later chapters can map risks without inventing new attacker assumptions.
