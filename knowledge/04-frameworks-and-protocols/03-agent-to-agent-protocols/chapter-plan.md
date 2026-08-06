# Agent-to-Agent Protocols Plan

## Section purpose

Teach interoperability among independent, potentially opaque agent systems.

## Learning outcomes

Explain discovery, capability cards, tasks, messages, parts, artifacts, streaming, asynchronous updates, cancellation, authentication, authorization, tracing, and protocol bindings.

## Prerequisites

[Model Context Protocol](../02-model-context-protocol/chapter-plan.md) and multi-agent systems.

## Planned child chapters

Main path:

1. `01-agent-to-tool-versus-agent-to-agent.md`
2. `02-a2a-data-model-and-discovery.md`
3. `03-task-lifecycle-messages-and-artifacts.md`

Deep dive:

4. `04-streaming-push-and-long-running-work.md`

Main path resumes:

5. `05-bindings-identity-and-interoperability.md`
6. `06-protocol-landscape-and-selection.md`

## Required concepts

Agent2Agent, agent card, skill, task, message, part, artifact, extension, binding, streaming, push notification, and opaque execution.

## Concepts explicitly out of scope

Protocol hype, unversioned comparisons, and detailed attacks or mitigations.

## Recommended teaching order

Differentiate MCP and peer protocols, then teach discovery, task lifecycle, asynchronous interaction, identity, and selection criteria.

## Required diagrams or visuals

MCP versus A2A boundary diagram and A2A task-state sequence.

## Recommended examples and framework use

Mock agent card and task exchange using no network service.

## Sources

Authoritative source categories: Official protocol specifications and project governance material.

Candidate primary sources:

- [A2A specification](https://a2a-protocol.org/latest/specification)
- [Linux Foundation A2A announcement](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [IBM ACP project and A2A merger notice](https://research.ibm.com/projects/agent-communication-protocol)
- [Google Agent Development Kit A2A integration](https://adk.dev/agents/)

## Connections to later security chapters

[Multi-agent and protocol security](../../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md).

## Open questions

Other agent interoperability protocols remain fluid. Add them only after an authoritative stable specification is checked.

## Completion criteria

The reader can choose an interaction boundary and trace discovery, task state, content, identity, and failure semantics.
