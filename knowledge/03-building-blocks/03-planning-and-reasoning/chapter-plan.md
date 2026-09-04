# Planning and Reasoning Plan

## Section purpose

Teach explicit task decomposition and model-directed decision patterns without relying on hidden reasoning traces.

## Learning outcomes

Compare reactive, plan-first, interleaved reason-act, planner-executor, reflection, evaluator-optimizer, and search patterns; choose stop and replan rules.

## Prerequisites

[Context construction](../02-context-construction/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-reactive-and-reason-act-patterns.md`
2. `02-decomposition-and-plan-execute.md`

Deep dives:

3. `03-reflection-evaluation-and-replanning.md`
4. `04-search-budgets-and-termination.md`

## Required concepts

Task decomposition, plan, subtask, action selection, observation, evaluator, feedback, replan trigger, search frontier, and budget.

## Concepts explicitly out of scope

Claims about private chain of thought, model training, and security attacks.

## Recommended teaching order

Start reactive, externalize plans, separate planner from executor, add feedback and search, then bound every loop.

## Required diagrams or visuals

Pattern comparison and plan-state transition diagram.

## Recommended examples

A visible structured plan executed against mocked tools; framework translations to LangGraph and Semantic Kernel.

## Sources

Authoritative source categories: Primary agent and reasoning papers plus official pattern docs.

Candidate primary sources:

- [ReAct](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve](https://aclanthology.org/2023.acl-long.147/)
- [Self-Refine](https://papers.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- [LangGraph workflows](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

## Connections to later security chapters

[Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open questions

When does explicit planning improve measured outcomes enough to justify its cost and failure surface?

## Completion criteria

Every pattern has inputs, outputs, state, replan conditions, termination, and evaluation criteria.
