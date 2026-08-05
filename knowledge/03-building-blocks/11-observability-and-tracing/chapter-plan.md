# Observability and Tracing Plan

## Section purpose

Teach how to reconstruct and measure agent behavior across components and services.

## Learning outcomes

Design structured events, logs, metrics, traces, spans, correlation, lineage, sampling, redaction, replay, dashboards, and debugging workflows.

## Prerequisites

[Human-in-the-loop systems](../10-human-in-the-loop/chapter-plan.md) and complete run lifecycle.

## Planned child chapters

1. `01-observability-model-and-events.md`
2. `02-traces-spans-and-correlation.md`
3. `03-metrics-cost-quality-and-latency.md`
4. `04-lineage-replay-redaction-and-retention.md`

## Required concepts

Telemetry, event, log, metric, trace, span, attribute, correlation identifier, lineage, sampling, redaction, and replay.

## Concepts explicitly out of scope

Detection rules, security operations, and vendor product surveys.

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

## Connections to later security chapters

[Human interfaces and observability security](../../07-security-by-component-and-workflow-stage/05-human-interfaces-and-observability/chapter-plan.md).

## Open questions

OpenTelemetry agent conventions are in development. Which stable project schema should wrap changing fields?

## Completion criteria

A complete run can be reconstructed without assuming that sensitive raw prompts are always recorded.
