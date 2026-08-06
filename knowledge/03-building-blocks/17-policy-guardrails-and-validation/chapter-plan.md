# Policy, Guardrails, and Validation Plan

## Section purpose

Make constraints and validation explicit functional components rather than scattered framework features.

## Learning outcomes

The reader can place policy decisions, enforcement points, validators, guardrails, and configuration ownership around model and tool activity.

## Prerequisites

[Tools and function calling](../07-tools-and-function-calling/chapter-plan.md), [identity](../08-identity-authorization-and-secrets/chapter-plan.md), and [human control](../10-human-in-the-loop/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-policy-constraints-and-the-control-plane.md`
2. `02-input-and-context-validation.md`
3. `03-intent-action-and-tool-call-validation.md`
4. `04-output-schemas-validation-and-safe-rendering.md`
5. `05-guardrails-moderation-and-failure-behavior.md`

Deep dive:

6. `06-agent-registry-configuration-and-versioning.md`

## Required concepts

Constraint, invariant, policy decision point, policy enforcement point, input validator, intent gate, action validator, output schema, safe renderer, guardrail, fail closed, fail open, registry, configuration, and version.

## Recommended teaching order

Teach deterministic policy and validation before probabilistic guardrails. End with operational ownership and versioning.

## Concepts explicitly out of scope

Detailed prompt-injection defenses, content-policy debates, and claims that a guardrail guarantees safety.

## Required diagrams or visuals

- Visual: control-plane and data-plane map with labeled enforcement points.
- Example: a deterministic action policy surrounding an untrusted model proposal.
- Framework examples: provider-neutral first, then concise hook translations.

## Recommended code and framework examples

Use a small policy object, typed schemas, explicit denial outcomes, and testable validators.

## Sources

Categories: authorization standards, official framework guardrail documentation, secure-design guidance, and primary validation research.

Candidate primary sources:

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST agent identity and authorization concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)
- [OpenAI practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

## Connections to later security chapters

Security chapters test bypass, ambiguity, policy drift, unsafe rendering, and failure behavior at every enforcement point.

## Open questions

Which semantic intent checks can be made reliable enough to enforce independently of the model that proposed an action?

## Completion criteria

The reference system has explicit, independently testable constraint, validation, and enforcement components.
