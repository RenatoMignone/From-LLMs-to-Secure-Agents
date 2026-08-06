# Prerequisites Plan

## Section purpose

Give the reader the minimum software-system vocabulary needed to trace an agent. Do not reteach large language models.

## Learning outcomes

The reader can read a component diagram, distinguish data from instructions, follow an HTTP and JSON exchange, identify a process and trust boundary, and interpret identity, permission, event, state, and side effect.

## Prerequisites

Working familiarity with large language models and prompts. No programming or API experience is required.

## Planned child chapters

1. `01-reader-contract-and-system-map.md`
2. `02-data-control-and-trust-boundaries.md`
3. `03-requests-events-state-and-side-effects.md`
4. `04-identity-authority-and-least-privilege-primer.md`

## Required concepts

Start with the project system map. Then teach data flow versus control flow, processes and network calls, structured messages, state transitions, identities, permissions, and trust boundaries. End with the notation reused in later diagrams.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Large language model internals, model training, prompt engineering, agent patterns, framework APIs, detailed threats, controls, and security testing.

## Required diagrams or visuals

- Visual: one labeled system-context diagram and one state-transition legend.
- Example: a mocked request that changes state and emits an event.
- Framework examples: none.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: Internet Engineering Task Force standards and National Institute of Standards and Technology terminology.

Candidate primary sources:

- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- [OAuth 2.0 Token Exchange, RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)

## Connections to later security chapters

Provide vocabulary used by the [threat model](../06-threat-model/chapter-plan.md), especially assets, actors, authority, boundaries, and side effects.

## Open questions

Decide whether basic distributed-systems retry semantics need a short appendix or can wait for reliability and operations.

## Completion criteria

All later plans can reference one consistent system diagram and glossary without redefining these terms.
