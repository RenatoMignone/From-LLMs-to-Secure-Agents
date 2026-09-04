# Agent Architectures Plan

## Section purpose

Teach stable orchestration patterns before component and framework detail.

## Learning outcomes

The reader can choose and diagram single-agent loops, routers, pipelines, parallel workers, evaluator-optimizer loops, plan-execute systems, supervisors, handoffs, and event-driven graphs.

## Prerequisites

[Agent foundations](../01-agent-foundations/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-architecture-selection-criteria.md`
2. `02-single-agent-and-reactive-loops.md`
3. `03-sequential-routing-and-parallel-workflows.md`

Deep dives:

4. `04-plan-and-execute.md`
5. `05-evaluator-optimizer-and-reflection.md`
6. `06-state-machines-and-event-driven-graphs.md`
7. `07-supervisors-handoffs-and-agent-as-tool.md`

Main path resumes:

8. `08-architecture-trade-offs.md`

## Required concepts

Begin with the least dynamic design that solves the task. Add routing, parallelism, loops, planning, evaluation, durable graphs, and multi-agent control. Distinguish architecture patterns from the runtime harness that realizes them. Compare determinism, latency, cost, debuggability, failure propagation, and termination.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Component internals, framework APIs, and detailed security analysis.

## Required diagrams or visuals

- Visual: pattern catalog using one consistent notation.
- Example: the same small task expressed as pipeline, router, and agent loop.
- Framework examples: LangGraph, Google Agent Development Kit, Semantic Kernel, and AutoGen only after patterns are understood.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: official framework pattern guides and primary planning or reflection research.

Candidate primary sources:

- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [Google Agent Development Kit agents](https://adk.dev/agents/)
- [Semantic Kernel orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/)
- [AutoGen teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
- [Self-Refine](https://papers.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)

## Connections to later security chapters

Each pattern links forward to compound-risk analysis in [end-to-end attack paths](../07-security-by-component-and-workflow-stage/07-end-to-end-attack-paths/chapter-plan.md).

## Open questions

Clarify where manager-worker patterns end and true peer coordination begins.

## Completion criteria

Every later component and workflow can be placed into one or more named architecture patterns without framework-specific language.
