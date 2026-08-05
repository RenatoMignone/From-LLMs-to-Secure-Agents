# Memory Plan

## Section purpose

Explain reusable information storage across turns and runs.

## Learning outcomes

Distinguish working, episodic, semantic, procedural, and profile memory; design write, consolidate, retrieve, update, forget, expire, and evaluate operations.

## Prerequisites

[State and lifecycle](../04-state-and-lifecycle/chapter-plan.md).

## Planned child chapters

1. `01-memory-versus-context-and-state.md`
2. `02-short-term-and-working-memory.md`
3. `03-persistent-memory-types-and-lifecycle.md`
4. `04-consolidation-forgetting-and-evaluation.md`

## Required concepts

Memory record, scope, salience, recency, relevance, consolidation, reflection, conflict, expiration, deletion, and provenance.

## Concepts explicitly out of scope

General RAG variants, model-weight training, and detailed poisoning controls.

## Recommended teaching order

Separate memory from context and state, teach run-scoped memory, add persistence and retrieval, then lifecycle and evaluation.

## Required diagrams or visuals

Memory-tier diagram and write-consolidate-retrieve lifecycle.

## Recommended examples

An in-memory store with explicit write and delete policies; compare AutoGen and LangGraph memory abstractions.

## Sources

Authoritative source categories: Primary memory-agent research and official framework documentation.

Candidate primary sources:

- [MemGPT](https://arxiv.org/abs/2310.08560)
- [Generative Agents](https://doi.org/10.1145/3586183.3606763)
- [AutoGen AgentChat introduction](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html)
- [LangGraph Agent Server persistence](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)

## Connections to later security chapters

[Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md).

## Open questions

How should conflicting and time-dependent memories be represented and evaluated?

## Completion criteria

Memory types, ownership, lifecycle, provenance, and deletion behavior are testable.
