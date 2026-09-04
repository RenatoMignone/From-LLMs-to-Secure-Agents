# Security Testing, Evaluation, and Assurance Plan

## Section purpose

Turn threat and control claims into repeatable evidence.

## Learning outcomes

The reader can design security unit, integration, adversarial, regression, and recovery tests; measure utility-security trade-offs; evaluate trajectories; and make bounded assurance claims.

## Prerequisites

[Secure reference architectures](../08-secure-reference-architectures/chapter-plan.md).

## Planned child chapters

1. `01-security-properties-oracles-and-component-tests.md`
2. `02-adversarial-benchmarks-and-control-effectiveness.md`
3. `03-recovery-continuous-assurance-and-reporting.md`

## Required concepts

Define testable properties and oracles. Add deterministic policy tests, adversarial inputs, multi-step attacks, benchmark harnesses, repeated trials, recovery exercises, production monitoring, and evidence-based release decisions.

## Recommended teaching order

Follow the concept order stated above and the numbered child chapters.

## Concepts explicitly out of scope

Dangerous payloads, live unauthorized testing, leaderboard snapshots as durable conclusions, and claims that passing a benchmark proves security.

## Required diagrams or visuals

- Visual: test pyramid, evaluation pipeline, and evidence-to-assurance map.
- Example: safe fixtures for prompt injection, authorization denial, budget exhaustion, and rollback.
- Framework examples: AgentDojo and Agent Security Bench harness concepts, plus framework-native eval hooks.

## Recommended code and framework examples

Use the examples and framework translations listed above. Keep them small and subordinate to the concepts.

## Sources

Categories: peer-reviewed security benchmarks, NIST test and risk guidance, OWASP testing resources, and official framework evaluation docs.

Candidate primary sources:

- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)
- [InjecAgent](https://aclanthology.org/2024.findings-acl.624/)
- [Agent Security Bench](https://openreview.net/pdf?id=V4y0CpX4hK)
- [Task Shield](https://aclanthology.org/2025.acl-long.1435/)
- [NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [Google Agent Development Kit evaluation](https://adk.dev/agents/)

## Connections to later security chapters

Feed limitations and evidence gaps into [open research questions](../10-open-research-questions/chapter-plan.md).

## Open questions

How to avoid benchmark contamination, judge-model bias, simulator artifacts, and defenses tuned to static attacks.

## Completion criteria

Every reference architecture has executable test requirements, repeated-trial metrics, recovery checks, and a bounded assurance statement.
