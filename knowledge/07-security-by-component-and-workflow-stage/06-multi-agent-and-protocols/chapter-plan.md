# Multi-Agent and Protocol Security Plan

## Section purpose

Analyze risks introduced by delegation, peer interaction, protocol discovery, remote tasks, and transitive trust.

## Learning outcomes

Model malicious or compromised agents, agent impersonation, capability-card poisoning, message and artifact injection, delegation drift, privilege amplification, shared-memory poisoning, protocol downgrade, session hijacking, token passthrough, and cascading failures.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 multi-agent systems, MCP, and A2A.

## Planned child chapters

1. `01-agent-identity-trust-and-impersonation.md`
2. `02-delegation-messages-shared-state-and-cascades.md`
3. `03-mcp-trust-authorization-and-server-risk.md`
4. `04-a2a-discovery-tasks-artifacts-and-bindings.md`
5. `05-controls-tests-recovery-and-residual-risk.md`

## Required concepts

Agent identity, transitive trust, delegation drift, capability advertisement, message provenance, protocol downgrade, token passthrough, session hijacking, and trust domain.

## Concepts explicitly out of scope

Repeating single-agent prompt injection without showing the cross-agent propagation path.

## Recommended teaching order

Establish peer identities and trust, trace delegation and shared state, analyze MCP and A2A boundaries, then apply controls and compound tests.

## Required diagrams or visuals

Cross-agent trust graph, delegation and credential sequence, and protocol attack-path diagram.

## Recommended examples

Signed-card verification fixture, message provenance checks, delegation depth limit, token-audience test, compromised-peer isolation, and cancellation recovery.

## Sources

Authoritative source categories: Official MCP and A2A specifications and trust models, OWASP multi-agent guidance, IETF standards, and primary multi-agent threat research.

Candidate primary sources:

- [MCP architecture](https://modelcontextprotocol.io/specification/2025-11-25/architecture)
- [MCP authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [MCP trust model](https://github.com/modelcontextprotocol/modelcontextprotocol/security)
- [A2A specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- [OWASP multi-agent threat modeling guide](https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/)
- [OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693.html)

## Connections to later security chapters

Feeds cross-domain [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

How should trust and authorization compose across opaque agents operated by different organizations?

## Completion criteria

Every agent and protocol hop has identity, provenance, authorization, trust assumptions, failure containment, cancellation, and recovery tests.
