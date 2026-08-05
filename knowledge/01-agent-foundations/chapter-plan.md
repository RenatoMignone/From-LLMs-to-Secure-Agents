# Agent Foundations Plan

## Section purpose

Define agentic systems by observable behavior and system structure, not by product labels.

## Learning outcomes

The reader can define an agent, trace a perception-decision-action loop, distinguish deterministic workflows from model-directed agents, identify autonomy levels, and state termination conditions.

## Prerequisites

[Prerequisites](../00-prerequisites/chapter-plan.md).

## Planned child chapters

1. `01-what-is-an-agent.md`
2. `02-the-agent-loop.md`
3. `03-workflows-versus-agents.md`
4. `04-goals-policies-environments-and-autonomy.md`
5. `05-run-lifecycle-and-termination.md`

## Required concepts

Define model, agent, environment, observation, action, goal, and policy. Build a manual loop. Compare fixed code paths with model-selected paths. Add autonomy levels, feedback, errors, budgets, and explicit stop conditions.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Framework tutorials, deep component internals, multi-agent coordination, and detailed security.

## Required diagrams or visuals

- Visual: model call, deterministic workflow, and agent loop side by side.
- Example: a framework-free typed tool loop with a hard turn limit.
- Framework examples: brief terminology cross-check only.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: official agent framework documentation and primary agent-pattern papers.

Candidate primary sources:

- [OpenAI Agents SDK overview](https://openai.github.io/openai-agents-python/)
- [Google Agent Development Kit agents](https://adk.dev/agents/)
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [ReAct](https://arxiv.org/abs/2210.03629)

## Connections to later security chapters

Link the security preview to [threat modeling](../06-threat-model/chapter-plan.md) and end-to-end goal, action, and termination risks.

## Open questions

Agent definitions vary across standards and frameworks. The chapter must present a project definition and label competing definitions.

## Completion criteria

A reader can classify an unfamiliar system as a model call, workflow, agent, or hybrid and justify the classification.
