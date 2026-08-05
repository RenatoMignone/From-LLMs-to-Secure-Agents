# Model Context Protocol Plan

## Section purpose

Teach the protocol that connects artificial intelligence applications to external tools, resources, and prompts.

## Learning outcomes

Explain host, client, and server roles; JSON-RPC lifecycle; capability negotiation; tools, resources, prompts, sampling, elicitation, transports, sessions, and authorization.

## Prerequisites

[Framework translations](../01-frameworks/chapter-plan.md), tools, context, and identity.

## Planned child chapters

1. `01-purpose-architecture-and-lifecycle.md`
2. `02-capabilities-tools-resources-and-prompts.md`
3. `03-transports-sessions-and-versioning.md`
4. `04-sampling-elicitation-and-roots.md`
5. `05-authorization-and-deployment-models.md`
6. `06-framework-integration.md`

## Required concepts

Model Context Protocol, host, client, server, capability, primitive, JSON-RPC, standard input/output transport, Streamable HTTP, session, and authorization server.

## Concepts explicitly out of scope

Attack catalogs, secure deployment recipes, and third-party server recommendations.

## Recommended teaching order

Start with roles and lifecycle, teach primitives, add transports and optional capabilities, then authorization and framework translation.

## Required diagrams or visuals

Host-client-server diagram, initialization sequence, and primitive/data-direction matrix.

## Recommended examples and framework use

Mock protocol messages and one minimal tool contract. Do not implement a server yet.

## Sources

Authoritative source categories: Versioned official specification, official SDK documentation, and IETF authorization standards.

Candidate primary sources:

- [MCP architecture](https://modelcontextprotocol.io/specification/2025-11-25/architecture)
- [MCP authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [MCP security policy and trust model](https://github.com/modelcontextprotocol/modelcontextprotocol/security)
- [OAuth 2.0 Security Best Current Practice](https://www.ietf.org/rfc/rfc9700.pdf)

## Connections to later security chapters

[Multi-agent and protocol security](../../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md) and [tools and credentials](../../07-security-by-component-and-workflow-stage/03-tools-identity-and-credentials/chapter-plan.md).

## Open questions

The protocol evolves quickly. Confirm the latest stable specification and feature status before writing.

## Completion criteria

The reader can trace lifecycle, capabilities, data direction, transport, session, and authorization without relying on one SDK.
