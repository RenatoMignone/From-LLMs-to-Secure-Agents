# Human Interfaces and Observability Security Plan

## Section purpose

Analyze how people authorize or misunderstand agent actions and how telemetry supports detection without creating new exposure.

## Learning outcomes

Model approval fatigue, deceptive or incomplete summaries, spoofed confirmations, unsafe rendering, social engineering, missing audit data, telemetry leakage, log injection, trace tampering, alert gaps, and privacy conflicts.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 human oversight, observability, and artifacts.

## Planned child chapters

1. `01-human-trust-approval-and-interface-failures.md`
2. `02-notifications-escalation-and-takeover.md`
3. `03-telemetry-leakage-integrity-and-retention.md`
4. `04-detection-alerting-investigation-and-replay.md`
5. `05-controls-tests-and-recovery.md`

## Required concepts

Approval fatigue, informed consent, action preview, trusted path, unsafe rendering, audit log, sensitive telemetry, log injection, trace integrity, alert, investigation, and replay.

## Concepts explicitly out of scope

General usability design and component attacks that do not affect human or telemetry boundaries.

## Recommended teaching order

Analyze decision interfaces, escalation and takeover, telemetry collection and protection, then detection, investigation, and recovery.

## Required diagrams or visuals

Approval information flow, trusted-interface boundary, and detect-investigate-recover timeline.

## Recommended examples

Approval-context completeness test, inert active-content fixture, trace-redaction test, tamper-detection fixture, and alert-to-disable exercise.

## Sources

Authoritative source categories: OWASP agentic guidance, NIST risk guidance, OpenTelemetry specifications, and official tracing docs.

Candidate primary sources:

- [OWASP securing agentic applications](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/)
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [OpenTelemetry agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/)

## Connections to later security chapters

Feeds monitoring and incident-ready designs in [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

How can approval quality and operator workload be measured without treating clicks as effective control?

## Completion criteria

Human decisions and telemetry have integrity, privacy, completeness, detection, escalation, and recovery requirements with tests.
