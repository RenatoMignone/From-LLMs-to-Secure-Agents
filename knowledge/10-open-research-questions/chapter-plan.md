# Open Research Questions Plan

## Section purpose

Identify unresolved problems that materially affect architecture or security decisions.

## Learning outcomes

The reader can distinguish established guidance from hypotheses, prioritize evidence gaps, and design research that tests system-level claims.

## Prerequisites

The complete [security assurance](../09-security-testing-evaluation-and-assurance/chapter-plan.md) section.

## Planned child chapters

1. `01-definitions-autonomy-and-measurement.md`
2. `02-robust-planning-memory-and-continual-learning.md`
3. `03-composable-security-and-protocol-trust.md`
4. `04-evaluation-validity-and-assurance-limits.md`
5. `05-human-agent-and-societal-boundaries.md`

## Required concepts

For each question, state why it matters, current evidence, conflicting findings, missing experiments, measurable hypotheses, and what result would change engineering guidance.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Predictions presented as facts, broad artificial general intelligence debates detached from system design, and duplicate summaries of earlier chapters.

## Required diagrams or visuals

- Visual: evidence-gap map and research dependency graph.
- Example: experiment-design templates, not implementations.
- Framework examples: only when a framework behavior is itself the research object.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: recent peer-reviewed work, official evolving specifications, benchmark papers, replication studies, and documented negative results.

Candidate primary sources:

- [AgentCL](https://arxiv.org/abs/2606.02461)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Tau-bench](https://arxiv.org/abs/2406.12045)
- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)
- [OpenTelemetry agent conventions, development status](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)

## Connections to later security chapters

This section closes the guide and points maintainers back to the [project plan](../chapter-plan.md) when evidence changes require structural revisions.

## Open questions

All child chapters are question-driven and must be reviewed for currency before writing.

## Completion criteria

Each research question is falsifiable or operationally investigable, cites checked evidence, and states why resolving it would change practice.
