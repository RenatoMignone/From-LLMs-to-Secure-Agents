# Framework Translations Plan

## Section purpose

Compare current agent frameworks by mapping them to the stable architecture already taught.

## Learning outcomes

Identify runtime ownership, graph and loop abstractions, tools, state, memory, human input, multi-agent patterns, tracing, evaluation, deployment, and protocol support in each framework.

## Prerequisites

[Frameworks and protocols](../chapter-plan.md) and all building blocks.

## Planned child chapters

Main path:

1. `01-comparison-method-and-versioning.md`

Deep dives:

2. `02-openai-agents-sdk.md`
3. `03-langchain-and-langgraph.md`
4. `04-autogen.md`
5. `05-semantic-kernel.md`
6. `06-google-agent-development-kit.md`
7. `07-crewai-and-llamaindex.md`

Main path resumes:

8. `08-cross-framework-translation.md`

## Required concepts

Framework, runtime, orchestration graph, session, thread, checkpoint, tool adapter, handoff, hook, plugin, and version.

## Concepts explicitly out of scope

Exhaustive API reference, framework rankings, and detailed security reviews.

## Recommended teaching order

Define a comparison matrix, examine each framework with the same canonical workflow, then translate one design across frameworks.

## Required diagrams or visuals

Framework abstraction matrix and equivalent workflow diagrams.

## Recommended examples and framework use

Small pseudocode translations only. Full runnable implementations wait for later example tasks.

## Sources

Authoritative source categories: Official versioned framework documentation.

Candidate primary sources:

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [LangGraph reference](https://langchain-ai.github.io/langgraph/reference/)
- [LangChain reference](https://reference.langchain.com/)
- [AutoGen](https://microsoft.github.io/autogen/)
- [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/)
- [Google Agent Development Kit](https://adk.dev/agents/)
- [CrewAI agents](https://docs.crewai.com/en/concepts/agents)
- [LlamaIndex agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/)

## Connections to later security chapters

[Multi-agent and protocol security](../../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md) and relevant component-security sections.

## Open questions

Framework convergence, renaming, and experimental features require version checks at writing time.

## Completion criteria

Each framework is described through the same stable concepts, versions are recorded, and no framework becomes the canonical explanation.
