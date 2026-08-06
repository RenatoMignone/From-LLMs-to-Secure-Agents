# End-to-End Workflows Plan

## Section purpose

Complete Pass 1 by assembling all architecture components into traceable workflows.

## Learning outcomes

The reader can trace input, context, planning, retrieval, state, authority, policy decisions, validation, tool calls, execution, user interaction, human approval, artifacts, telemetry, evaluation, retries, and termination through a full run and its deployment boundary.

## Prerequisites

[Frameworks and protocols](../04-frameworks-and-protocols/chapter-plan.md) and every Pass 1 building block.

## Planned child chapters

1. `01-workflow-requirements-and-system-boundary.md`
2. `02-single-agent-research-and-action-workflow.md`
3. `03-durable-human-approved-workflow.md`
4. `04-multi-agent-delegation-workflow.md`
5. `05-trace-replay-and-functional-evaluation.md`

## Required concepts

Define one bounded service task and its agent harness: instructions, context, tools, state, constraints, policies, validators, permissions, user interface, tracing, verification, and recovery. Draw system, authority, enforcement, deployment, and user-interaction maps. Walk success, failure, retry, approval, steering, resume, cancellation, and termination. Then distinguish a single harnessed run from an external reusable operating loop, often called loop engineering, and evaluate complete trajectories.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

New component theory, exploit walkthroughs, defensive control detail, and security test design.

## Required diagrams or visuals

- Visual: sequence diagram, data-flow diagram, state machine, authority and enforcement map, deployment map, user-event flow, and trace tree for the same workflow.
- Example: a small mocked reference workflow specification, not a full implementation.
- Framework examples: one framework-neutral design plus concise LangGraph and OpenAI Agents SDK translations.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: official runtime documentation and primary agent evaluation research.

Candidate primary sources:

- [OpenAI Agents SDK running agents](https://openai.github.io/openai-agents-python/running_agents/)
- [LangGraph Agent Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)
- [AutoGen termination](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html)
- [OpenTelemetry agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [Tau-bench](https://arxiv.org/abs/2406.12045)
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [Harness-Bench](https://arxiv.org/abs/2605.27922)
- [IBM: What is loop engineering?](https://www.ibm.com/think/topics/loop-engineering)
- [Stop Hand-Holding Your Coding Agent](https://arxiv.org/abs/2607.00038)

## Connections to later security chapters

The exact workflows become the assets and attack paths for the [threat model](../06-threat-model/chapter-plan.md). The security preview is a forward-link map only.

## Open questions

Select a domain that permits realistic authorization and side effects while remaining safe and easy to mock. Treat harness engineering and loop engineering as evolving labels, and state where definitions overlap or conflict.

## Completion criteria

No new functional component is needed when Pass 2 begins, and every workflow step has a stable identifier for later risk mapping.
