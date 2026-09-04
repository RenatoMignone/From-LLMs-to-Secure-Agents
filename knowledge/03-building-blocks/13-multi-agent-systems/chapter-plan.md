# Multi-Agent Systems Plan

## Section purpose

Explain architectures in which multiple agent instances coordinate or delegate work.

## Learning outcomes

Compare agent-as-tool, handoff, supervisor-worker, router-specialist, blackboard, group chat, debate, peer-to-peer, and event-driven teams; manage messages, shared state, authority, and termination.

## Prerequisites

Single-agent building blocks and [evaluation](../12-evaluation-and-benchmarks/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-multi-agent-roles-delegation-and-coordination.md`

Deep dive:

2. `02-shared-state-failures-termination-and-evaluation.md`

## Required concepts

Role, specialist, manager, supervisor, worker, peer, delegation, handoff, agent-as-tool, shared context, shared state, consensus, and termination.

## Concepts explicitly out of scope

Wire protocols and detailed cross-agent security.

## Recommended teaching order

Justify multiple agents, add controlled delegation, compare coordination patterns, define shared information, then failures and evaluation.

## Required diagrams or visuals

Pattern comparison, delegation chain, and multi-agent state machine.

## Recommended examples

Mocked manager-specialist and peer-task workflows; translate to OpenAI Agents SDK, AutoGen, and Semantic Kernel.

## Sources

Authoritative source categories: Primary multi-agent papers and official framework documentation.

Candidate primary sources:

- [AutoGen paper](https://arxiv.org/abs/2308.08155)
- [CAMEL](https://proceedings.neurips.cc/paper/2023/hash/a3621ee907def47c1b952ade25c67698-Abstract-Conference.html)
- [OpenAI Agents SDK orchestration](https://openai.github.io/openai-agents-python/multi_agent/)
- [AutoGen teams](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)
- [Semantic Kernel orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/)

## Connections to later security chapters

[Multi-agent and protocol security](../../07-security-by-component-and-workflow-stage/06-multi-agent-and-protocols/chapter-plan.md).

## Open questions

Which coordination benefits persist after controlling for extra model calls and context?

## Completion criteria

Every pattern states control ownership, message flow, authority, shared state, failure handling, termination, and evaluation.
