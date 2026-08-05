# Evaluation and Benchmarks Plan

## Section purpose

Teach functional evaluation at component, trajectory, task, and system levels.

## Learning outcomes

Define tasks, datasets, simulators, oracles, metrics, repeated trials, pass rates, pass^k, trajectory grading, latency and cost measures, regression sets, and benchmark limitations.

## Prerequisites

[Observability and tracing](../11-observability-and-tracing/chapter-plan.md).

## Planned child chapters

1. `01-evaluation-levels-and-test-design.md`
2. `02-component-and-trajectory-metrics.md`
3. `03-end-to-end-task-and-reliability-evaluation.md`
4. `04-agent-benchmarks-and-limitations.md`
5. `05-regression-and-release-evaluation.md`

## Required concepts

Evaluation, benchmark, task, environment, simulator, oracle, metric, trajectory, task success, pass@k, pass^k, variance, contamination, and judge model.

## Concepts explicitly out of scope

Security red teaming and current leaderboard comparisons.

## Recommended teaching order

Start with intended behavior, define oracles and levels, add repeated end-to-end trials, study benchmarks, then operationalize regression.

## Required diagrams or visuals

Evaluation stack and metric-to-component map.

## Recommended examples

A deterministic mocked environment and trajectory grader; no live benchmark run.

## Sources

Authoritative source categories: Peer-reviewed benchmarks and official framework evaluation docs.

Candidate primary sources:

- [AgentBench](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html)
- [GAIA](https://openreview.net/pdf?id=fibxvahvs3)
- [Tau-bench](https://arxiv.org/abs/2406.12045)
- [SWE-bench](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html)
- [Google Agent Development Kit evaluation](https://adk.dev/agents/)

## Connections to later security chapters

[Security testing and assurance](../../09-security-testing-evaluation-and-assurance/chapter-plan.md).

## Open questions

How should non-deterministic reliability and simulator validity be communicated to practitioners?

## Completion criteria

Metrics align with system levels, repeated trials, costs, and known benchmark limitations.
