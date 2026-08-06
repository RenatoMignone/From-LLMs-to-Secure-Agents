# Identity, Authorization, and Secrets Plan

## Section purpose

Teach how humans, services, workloads, and agents obtain identity and bounded authority.

## Learning outcomes

Trace authentication, authorization, policy decisions, delegation, impersonation, token exchange, scopes, capabilities, credential brokering, rotation, revocation, and secret storage.

## Prerequisites

[Tools and function calling](../07-tools-and-function-calling/chapter-plan.md).

## Planned child chapters

1. `01-principals-identities-and-authentication.md`
2. `02-authorization-policies-and-capabilities.md`
3. `03-delegation-impersonation-and-token-exchange.md`
4. `04-workload-identity.md`
5. `05-credentials-secrets-rotation-and-revocation.md`

## Required concepts

Principal, subject, actor, workload, credential, secret, token, scope, audience, resource, delegation chain, capability, policy decision point, and policy enforcement point.

## Concepts explicitly out of scope

Attack procedures, vendor identity setup, and protocol-specific authorization detail.

## Recommended teaching order

Identify principals, authenticate them, authorize actions, preserve delegation chains, then manage credentials over their lifecycle.

## Required diagrams or visuals

Actor-subject delegation flow, policy decision flow, and credential lifecycle.

## Recommended examples

A mocked authorization service issuing short-lived scoped capabilities; map to OAuth token exchange and SPIFFE.

## Sources

Authoritative source categories: IETF standards, SPIFFE specifications, and official protocol authorization docs.

Candidate primary sources:

- [OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693.html)
- [OAuth 2.0 Security Best Current Practice](https://www.ietf.org/rfc/rfc9700.pdf)
- [SPIFFE concepts](https://spiffe.io/docs/latest/spiffe/concepts/)
- [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [NIST software and AI agent identity and authorization concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)

## Connections to later security chapters

[Tools, identity, and credential security](../../07-security-by-component-and-workflow-stage/03-tools-identity-and-credentials/chapter-plan.md).

## Open questions

How should an agent identity relate to the runtime workload and represented human?

## Completion criteria

Every action can be attributed to a subject, actor, workload, policy decision, and bounded credential.
