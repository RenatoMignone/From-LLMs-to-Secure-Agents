# Tools, Identity, and Credential Security Plan

## Section purpose

Analyze the boundary where model-selected requests acquire real authority.

## Learning outcomes

Model excessive agency, unsafe tool selection, parameter manipulation, authorization bypass, confused deputy, over-broad delegation, impersonation, token theft, secret leakage, replay, stale authorization, and revocation gaps.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 tools and identity.

## Planned child chapters

1. `01-tool-identity-and-credential-attacks.md`
2. `02-authorization-controls-tests-and-recovery.md`

## Required concepts

Excessive agency, least privilege, policy enforcement point, confused deputy, delegation, impersonation, token audience, scope, replay, rotation, revocation, and break-glass recovery.

## Concepts explicitly out of scope

Sandbox escape detail and protocol-only threats.

## Recommended teaching order

Start at tool request, verify actor and subject, authorize exact effects, issue bounded credentials, execute, audit, revoke, and recover.

## Required diagrams or visuals

Tool authorization sequence, delegation chain, and credential exposure map.

## Recommended examples

Deny-by-default policy tests, scope and audience checks, short-lived token fixture, revocation test, and secret-redaction test.

## Sources

Authoritative source categories: IETF standards, SPIFFE, MCP authorization, OWASP, and official framework security docs.

Candidate primary sources:

- [OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693.html)
- [OAuth 2.0 Security Best Current Practice](https://www.ietf.org/rfc/rfc9700.pdf)
- [SPIFFE standard](https://spiffe.io/docs/latest/spiffe-specs/)
- [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)

## Connections to later security chapters

Feeds authority controls in [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

How can user intent be bound to a delegated credential across multi-step and multi-agent workflows?

## Completion criteria

Every side effect has authenticated actor and subject, explicit authorization, bounded credential, audit evidence, revocation, and recovery behavior.
