# Frameworks and Protocols Plan

## Section purpose

Show how stable architecture concepts map to current implementation ecosystems and interoperability contracts.

## Learning outcomes

The reader can compare orchestration frameworks without confusing their names with canonical concepts, explain Model Context Protocol roles, and distinguish agent-to-tool from agent-to-agent protocols.

## Prerequisites

[Building blocks](../03-building-blocks/chapter-plan.md).

## Planned child sections

1. [Framework translations](01-frameworks/chapter-plan.md)
2. [Model Context Protocol](02-model-context-protocol/chapter-plan.md)
3. [Agent-to-agent protocols](03-agent-to-agent-protocols/chapter-plan.md)

## Required concepts

Compare abstraction levels and runtime ownership first. Then teach Model Context Protocol host-client-server architecture. Finish with peer-agent discovery, tasks, messages, artifacts, streaming, and long-running work.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Replacing stable concepts with vendor terms, exhaustive API reference, and detailed protocol security.

## Required diagrams or visuals

- Visual: framework abstraction comparison and protocol-boundary map.
- Example: one tool exposed directly and through Model Context Protocol, plus one mocked peer-agent task.
- Framework examples: OpenAI Agents SDK, LangGraph, AutoGen, Semantic Kernel, Google Agent Development Kit, CrewAI, and LlamaIndex.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: official, versioned documentation and specifications.

Candidate primary sources:

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [LangGraph reference](https://langchain-ai.github.io/langgraph/reference/)
- [AutoGen](https://microsoft.github.io/autogen/)
- [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/)
- [Google Agent Development Kit](https://adk.dev/agents/)
- [CrewAI agents](https://docs.crewai.com/en/concepts/agents)
- [LlamaIndex agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/)

## Connections to later security chapters

Protocols and framework trust assumptions are revisited in [multi-agent and protocol security](../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md).

## Open questions

Track protocol and framework version churn without presenting preview features as stable.

## Completion criteria

The reader can translate the canonical workflow into at least three frameworks and explain where protocol boundaries replace in-process calls.
