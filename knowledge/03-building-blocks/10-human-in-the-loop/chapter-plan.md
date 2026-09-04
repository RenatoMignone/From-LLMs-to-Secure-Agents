# Human-in-the-Loop Systems Plan

## Section purpose

Teach explicit human control points within asynchronous and stateful agent workflows.

## Learning outcomes

Design clarification, review, approval, intervention, escalation, takeover, timeout, rejection, resumption, and audit behavior.

## Prerequisites

[Execution environments](../09-execution-environments/chapter-plan.md), state, and identity.

## Planned child chapters

1. `01-human-control-approval-and-escalation.md`
2. `02-interrupts-steering-feedback-and-operator-experience.md`

## Required concepts

Human-in-the-loop, human-on-the-loop, approval, confirmation, review, escalation, interruption, takeover, rejection, and service-level objective.

## Concepts explicitly out of scope

Detailed social engineering, interface deception attacks, and claims that humans guarantee safety.

## Recommended teaching order

Classify human roles, place control points by consequence, define lifecycle behavior, then evaluate workload and effectiveness.

## Required diagrams or visuals

Approval sequence with pause and resume, and consequence-versus-autonomy matrix.

## Recommended examples

A mocked approval queue with expiration and revalidation; translate to AutoGen and OpenAI Agents SDK.

## Sources

Authoritative source categories: Official framework lifecycle and human-input documentation plus human-computer interaction research when drafting.

Candidate primary sources:

- [AutoGen human-in-the-loop](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)
- [OpenAI Agents SDK running agents](https://openai.github.io/openai-agents-python/running_agents/)
- [Google Agent Development Kit agents](https://adk.dev/agents/)

## Connections to later security chapters

[Human interfaces and observability security](../../07-security-by-component-and-workflow-stage/05-human-interfaces-and-observability/chapter-plan.md).

## Open questions

What measurable conditions make an approval meaningful rather than ceremonial?

## Completion criteria

Every human control point has trigger, context, authority, timeout, rejection, resume, and audit semantics.
