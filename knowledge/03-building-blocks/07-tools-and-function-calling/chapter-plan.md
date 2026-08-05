# Tools and Function Calling Plan

## Section purpose

Explain how model outputs become typed capability requests and environment actions.

## Learning outcomes

Design schemas, descriptions, selection, argument validation, dispatch, results, errors, parallel calls, side effects, idempotency, confirmation, and tool lifecycle.

## Prerequisites

[Retrieval and RAG](../06-retrieval-and-rag/chapter-plan.md) and planning.

## Planned child chapters

1. `01-tools-actions-and-capabilities.md`
2. `02-schemas-selection-and-dispatch.md`
3. `03-results-errors-parallelism-and-retries.md`
4. `04-side-effects-idempotency-and-confirmation.md`
5. `05-tool-discovery-and-large-toolsets.md`

## Required concepts

Tool, function, schema, argument, dispatcher, result, side effect, idempotency, timeout, confirmation, namespace, and capability discovery.

## Concepts explicitly out of scope

MCP wire behavior, authorization controls, and exploit payloads.

## Recommended teaching order

Define capability boundaries, add typed calls, execute safely in functional terms, handle errors and side effects, then scale tool discovery.

## Required diagrams or visuals

Tool-call sequence and side-effect classification matrix.

## Recommended examples

Two typed mocked functions with validation, error results, and idempotency keys; translate to OpenAI Agents SDK.

## Sources

Authoritative source categories: Official tool-calling documentation and primary tool-use research.

Candidate primary sources:

- [OpenAI Agents SDK tools](https://openai.github.io/openai-agents-python/tools/)
- [Google Agent Development Kit tools](https://adk.dev/agents/)
- [Toolformer](https://arxiv.org/abs/2302.04761)
- [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/)

## Connections to later security chapters

[Tools, identity, and credential security](../../07-security-by-component-and-workflow-stage/03-tools-identity-and-credentials/chapter-plan.md).

## Open questions

How should dynamic tool discovery be evaluated without coupling architecture to one provider?

## Completion criteria

Tool requests and effects are typed, observable, bounded, and distinguishable from model text.
