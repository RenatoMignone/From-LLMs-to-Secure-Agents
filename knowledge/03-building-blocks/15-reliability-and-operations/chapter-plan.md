# Reliability and Operations Plan

## Section purpose

Teach the runtime mechanisms that keep agent services bounded, available, repeatable, and maintainable.

## Learning outcomes

Design queues, workers, leases, retries, backoff, rate limits, timeouts, budgets, circuit breakers, fallbacks, concurrency limits, caching, deployment versions, rollback, and service objectives.

## Prerequisites

[Learning and self-improvement](../14-learning-and-self-improvement/chapter-plan.md), state, observability, and evaluation.

## Planned child chapters

1. `01-service-boundaries-queues-and-workers.md`
2. `02-timeouts-retries-backoff-and-idempotency.md`
3. `03-budgets-rate-limits-and-circuit-breakers.md`
4. `04-caching-versioning-deployment-and-rollback.md`
5. `05-service-level-objectives-and-capacity.md`

## Required concepts

Queue, worker, lease, backoff, timeout, budget, quota, circuit breaker, cache, deployment, rollback, service-level indicator, and service-level objective.

## Concepts explicitly out of scope

Detailed denial-of-service attacks and incident-response playbooks.

## Recommended teaching order

Define service topology, handle transient failure, bound resource use, manage versions and rollback, then measure objectives.

## Required diagrams or visuals

Queue-worker lifecycle and layered budget diagram.

## Recommended examples

A mocked scheduler configuration with retry and budget policies; compare durable framework runtime behavior.

## Sources

Authoritative source categories: Official runtime, framework, and distributed-systems documentation.

Candidate primary sources:

- [LangGraph Agent Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)
- [OpenAI Agents SDK running agents](https://openai.github.io/openai-agents-python/running_agents/)
- [AutoGen termination](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html)

## Connections to later security chapters

[Execution and supply-chain security](../../07-security-by-component-and-workflow-stage/04-execution-and-supply-chain/chapter-plan.md) and [end-to-end attack paths](../../07-security-by-component-and-workflow-stage/07-end-to-end-attack-paths/chapter-plan.md).

## Open questions

What default resource budgets make examples realistic without tying them to one provider?

## Completion criteria

Failure, overload, retry, version change, and rollback behavior are explicit and measurable.
