# Observability and Tracing Plan

## Section purpose

Teach how to reconstruct and measure agent behavior across components and services.

## Learning outcomes

Design structured events, logs, metrics, traces, spans, correlation, lineage, sampling, redaction, replay, dashboards, and debugging workflows.

## Prerequisites

[Human-in-the-loop systems](../10-human-in-the-loop/chapter-plan.md) and complete run lifecycle.

## Planned child chapters

Main path:

1. `01-events-traces-metrics-and-correlation.md`

Deep dive:

2. `02-lineage-replay-redaction-retention-and-integrations.md`

## Required concepts

Telemetry, event, log, metric, trace, span, attribute, correlation identifier, lineage, sampling, redaction, and replay.

## Concepts explicitly out of scope

Detection rules, security operations, and exhaustive vendor product surveys.

## Recommended teaching order

Define questions, emit structured events, compose traces, derive metrics, then manage sensitive content and replay.

## Required diagrams or visuals

Trace tree across model, retrieval, tool, and handoff spans; telemetry data-flow diagram.

## Recommended examples

Instrument a mocked run with OpenTelemetry-shaped spans; compare with OpenAI Agents SDK tracing.

## Sources

Authoritative source categories: Official telemetry specifications and framework tracing docs.

Candidate primary sources:

- [OpenTelemetry agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/)
- [Langfuse documentation](https://langfuse.com/docs)
- [LangSmith observability documentation](https://docs.langchain.com/langsmith/observability)
- [Arize Phoenix documentation](https://arize.com/docs/phoenix/)

## Connections to later security chapters

[Human interfaces and observability security](../../07-security-by-component-and-workflow-stage/05-human-interfaces-and-observability/chapter-plan.md).

## Open questions

OpenTelemetry agent conventions are in development. Which stable project schema should wrap changing fields?

## Completion criteria

A complete run can be reconstructed without assuming that sensitive raw prompts are always recorded.
