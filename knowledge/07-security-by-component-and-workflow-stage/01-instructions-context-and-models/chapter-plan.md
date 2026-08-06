# Instructions, Context, and Model Security Plan

## Section purpose

Analyze attacks that alter goals, instructions, context interpretation, routing, planning, or model outputs.

## Learning outcomes

Model direct and indirect prompt injection, goal hijacking, instruction conflict, context overflow, system-prompt leakage, unsafe output handling, model routing abuse, and unbounded model consumption; select layered controls.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 model, context, and planning sections.

## Planned child chapters

1. `01-instruction-hierarchy-and-prompt-injection.md`
2. `02-indirect-injection-and-untrusted-context.md`
3. `03-goal-plan-routing-and-output-manipulation.md`
4. `04-model-abuse-leakage-and-resource-consumption.md`
5. `05-misalignment-specification-gaming-and-rogue-behavior.md`
6. `06-controls-tests-and-residual-risk.md`

## Required concepts

Direct prompt injection, indirect prompt injection, goal hijacking, instruction provenance, confused context, output validation, model denial of service, misalignment, specification gaming, rogue behavior, safe failure, and residual risk.

## Concepts explicitly out of scope

Retrieval corpus controls, tool authorization internals, and claims that prompt filtering alone solves injection.

## Recommended teaching order

Map trust mixing, explain injection paths, extend through routing and plans, then layer prevention, detection, recovery, and tests.

## Required diagrams or visuals

Instruction and data trust map, indirect-injection path, and layered control map.

## Recommended examples

Safe inert injection fixtures, structured output validation, context labels, budget enforcement, and recovery from a compromised run.

## Sources

Authoritative source categories: OWASP, NIST, MITRE ATLAS, primary attack and defense research, and official framework guardrail docs.

Candidate primary sources:

- [Indirect prompt injection research](https://arxiv.org/abs/2302.12173)
- [InjecAgent](https://aclanthology.org/2024.findings-acl.624/)
- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)
- [OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OpenAI Agents SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/)

## Connections to later security chapters

Feeds [end-to-end attack paths](../07-end-to-end-attack-paths/chapter-plan.md) and [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

How should defenses be evaluated against adaptive attacks while preserving task utility?

## Completion criteria

Each risk has preconditions, affected workflow identifiers, preventive, detective, and recovery controls, safe tests, and residual risk.
