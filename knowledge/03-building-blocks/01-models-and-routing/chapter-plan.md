# Models and Routing Plan

## Section purpose

Explain how an agent selects, configures, routes among, and falls back across models.

## Learning outcomes

Choose models by capability, modality, latency, cost, context, tool support, privacy, and reliability; explain static selection, rules, cascades, learned routers, ensembles, retries, and fallback.

## Prerequisites

[Building blocks](../chapter-plan.md) and agent architectures.

## Planned child chapters

Main path:

1. `01-model-roles-and-selection.md`
2. `02-routing-cascades-and-fallbacks.md`

Deep dive:

3. `03-capability-cost-latency-and-reliability.md`

Main path resumes:

4. `04-routing-evaluation.md`

## Required concepts

Model role, provider adapter, capability profile, routing policy, cascade, fallback, ensemble, rate limit, and model-version pinning.

## Concepts explicitly out of scope

Model training internals and provider rankings.

## Recommended teaching order

Start with one model, add measured selection criteria, then routing and failure handling, and finish with router evaluation.

## Required diagrams or visuals

Decision flow for model selection and a cost-latency-quality trade-off plot.

## Recommended examples

A deterministic router and mocked fallback; translate briefly to Google Agent Development Kit and OpenAI Agents SDK.

## Sources

Authoritative source categories: Official model and framework docs plus peer-reviewed routing research.

Candidate primary sources:

- [RouteLLM](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html)
- [FrugalGPT](https://arxiv.org/abs/2305.05176)
- [Google Agent Development Kit models](https://adk.dev/agents/)

## Connections to later security chapters

[Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open questions

How should privacy, region, and tool-schema compatibility enter a router objective?

## Completion criteria

Selection criteria, failure paths, and router metrics are explicit and provider-neutral.
