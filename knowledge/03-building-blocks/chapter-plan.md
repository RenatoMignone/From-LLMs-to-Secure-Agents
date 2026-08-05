# Building Blocks Plan

## Section purpose

Provide the complete functional anatomy of production agentic systems.

## Learning outcomes

The reader can locate every model call, context item, plan, state transition, memory operation, retrieval step, tool action, identity, execution boundary, human control, trace, evaluation, agent message, adaptation step, operational mechanism, and artifact.

## Prerequisites

[Agent architectures](../02-agent-architectures/chapter-plan.md).

## Planned child sections

1. [Models and routing](01-models-and-routing/chapter-plan.md)
2. [Context construction](02-context-construction/chapter-plan.md)
3. [Planning and reasoning](03-planning-and-reasoning/chapter-plan.md)
4. [State and lifecycle](04-state-and-lifecycle/chapter-plan.md)
5. [Memory](05-memory/chapter-plan.md)
6. [Retrieval and RAG](06-retrieval-and-rag/chapter-plan.md)
7. [Tools and function calling](07-tools-and-function-calling/chapter-plan.md)
8. [Identity, authorization, and secrets](08-identity-authorization-and-secrets/chapter-plan.md)
9. [Execution environments](09-execution-environments/chapter-plan.md)
10. [Human-in-the-loop](10-human-in-the-loop/chapter-plan.md)
11. [Observability and tracing](11-observability-and-tracing/chapter-plan.md)
12. [Evaluation and benchmarks](12-evaluation-and-benchmarks/chapter-plan.md)
13. [Multi-agent systems](13-multi-agent-systems/chapter-plan.md)
14. [Learning and self-improvement](14-learning-and-self-improvement/chapter-plan.md)
15. [Reliability and operations](15-reliability-and-operations/chapter-plan.md)
16. [Artifacts and multimodal input/output](16-artifacts-and-multimodal-io/chapter-plan.md)

## Required concepts

Follow the numbered child sections. Preserve distinctions among context, state, memory, and artifacts. Treat identity and execution as functional architecture before their security implications.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Detailed attacks, control selection, security reference architectures, and framework-first explanations.

## Required diagrams or visuals

- Visual: one complete component map refined by each child section.
- Example: one framework-neutral runtime skeleton extended conceptually across sections.
- Framework examples: deferred to the framework section except short translations.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: official framework docs, protocol specifications, software standards, and primary systems research. Candidate sources are listed in each child plan.

Candidate primary sources:

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [ReAct](https://arxiv.org/abs/2210.03629)
- [OpenTelemetry semantic conventions for generative AI agents](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)

## Connections to later security chapters

Every child section must link to its matching area under [component security](../07-security-by-component-and-workflow-stage/chapter-plan.md).

## Open questions

Whether policy engines deserve a separate building-block branch should be reassessed after the authorization and tool sections are drafted.

## Completion criteria

The component map is complete enough to trace the Pass 1 end-to-end workflow without introducing a new architectural component.
