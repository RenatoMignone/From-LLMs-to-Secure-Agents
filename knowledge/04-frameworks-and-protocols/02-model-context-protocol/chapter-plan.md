# Model Context Protocol Plan

## Section purpose

Teach the protocol that connects artificial intelligence applications to external tools, resources, and prompts.

## Learning outcomes

Explain host, client, and server roles; JSON-RPC requests; per-request capabilities and optional discovery; tools, resources, prompts, sampling, elicitation, transports, subscriptions, application state, compatibility, and authorization.

## Prerequisites

[Framework translations](../01-frameworks/chapter-plan.md), tools, context, and identity.

## Planned child chapters

Deep dives:

1. `01-architecture-capabilities-transports-and-lifecycle.md`
2. `02-authorization-deployment-and-extension-features.md`

## Required concepts

Model Context Protocol, host, client, server, capability, primitive, JSON-RPC, standard input/output transport, Streamable HTTP, session, and authorization server.

## Concepts explicitly out of scope

Attack catalogs, secure deployment recipes, and third-party server recommendations.

## Recommended teaching order

Start with roles and lifecycle, teach primitives, add transports and optional capabilities, then authorization and framework translation.

## Required diagrams or visuals

Host-client-server diagram, request and discovery sequence, and primitive/data-direction matrix.

## Recommended examples and framework use

Mock protocol messages and one minimal tool contract. Do not implement a server yet.

## Version baseline and compatibility

Use the 2026-07-28 specification as the review baseline. Teach self-contained requests carrying protocol version and capabilities, optional `server/discover`, and server requests for client input through `InputRequiredResult`. Separate stateless protocol requests from application state and notification subscriptions. Earlier initialization and session-wide capability negotiation belong in an explicitly versioned compatibility comparison, not the current core model.

Distinguish tools, resources and prompts from optional extension features. Verify Tasks, Skills over MCP and MCP Apps status and opt-in requirements before writing. Replace an initialization sequence with a request/discovery/input-return sequence for this baseline. Sources: [MCP architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture) and [versioned specification](https://modelcontextprotocol.io/specification/2026-07-28).

## Sources

Authoritative source categories: Versioned official specification, official SDK documentation, and IETF authorization standards.

Candidate primary sources:

- [MCP architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)
- [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [MCP security policy and trust model](https://github.com/modelcontextprotocol/modelcontextprotocol/security)
- [OAuth 2.0 Security Best Current Practice](https://www.ietf.org/rfc/rfc9700.pdf)

## Connections to later security chapters

[Multi-agent and protocol security](../../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md) and [tools and credentials](../../07-security-by-component-and-workflow-stage/03-tools-identity-and-credentials/chapter-plan.md).

## Open questions

The protocol evolves quickly. Confirm the latest stable specification and feature status before writing.

## Completion criteria

The reader can trace lifecycle, capabilities, data direction, transport, application state, and authorization without relying on one SDK.
