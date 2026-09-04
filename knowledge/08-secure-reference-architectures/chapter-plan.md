# Secure Reference Architectures Plan

## Section purpose

Compose previously taught controls into reusable designs for different authority and exposure levels.

## Learning outcomes

The reader can choose trust zones, enforcement points, credential paths, isolation boundaries, approval gates, telemetry, recovery mechanisms, and residual-risk statements for a complete system.

## Prerequisites

All [component and workflow security](../07-security-by-component-and-workflow-stage/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-method-and-read-only-knowledge-agent.md`
2. `02-human-approved-action-and-sandboxed-execution.md`

Deep dive:

3. `03-multi-agent-high-assurance-and-recovery.md`

## Required concepts

Define security objectives and trust assumptions. Start with read-only access. Add side effects, isolated execution, multi-agent delegation, central policy enforcement, credential brokering, tamper-aware telemetry, kill switches, rollback, and recovery.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Universal blueprints, product procurement advice, and assurance without evidence.

## Required diagrams or visuals

- Visual: deployment, trust-zone, credential-flow, control-plane, and recovery diagrams.
- Example: declarative policy and architecture manifests as pseudocode.
- Framework examples: provider-neutral first, then selected framework hooks.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: NIST risk management, IETF authorization standards, workload identity standards, isolation documentation, and OWASP implementation guidance.

Candidate primary sources:

- [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- [OWASP securing agentic applications](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/)
- [OAuth 2.0 Security Best Current Practice, RFC 9700](https://www.ietf.org/rfc/rfc9700.pdf)
- [OAuth 2.0 Token Exchange, RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)
- [SPIFFE standard](https://spiffe.io/docs/latest/spiffe-specs/)
- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/)
- [Firecracker design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md)

## Connections to later security chapters

Each architecture must declare the tests and evidence required by [security assurance](../09-security-testing-evaluation-and-assurance/chapter-plan.md).

## Open questions

Define assurance tiers without implying that a specific technology guarantees a tier.

## Completion criteria

Every reference design maps components, threats, controls, telemetry, recovery, and residual risk end to end.
