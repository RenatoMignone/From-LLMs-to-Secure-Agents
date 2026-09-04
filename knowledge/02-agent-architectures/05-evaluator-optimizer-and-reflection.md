<!--
---
title: Evaluator-optimizer and reflection
unit_id: P1-02-05
summary: Explores the evaluator-optimizer and reflection patterns, detailing how decoupled
  generator and evaluator models iteratively critique, score, and refine outputs against
  deterministic tests and semantic rubrics.
prerequisites:
- Read [Architecture selection criteria](01-architecture-selection-criteria.md).
- Read [Plan and execute](04-plan-and-execute.md).
learning_objectives:
- Construct iterative generator-evaluator loops using explicit scoring rubrics and
  acceptance thresholds.
- Integrate deterministic verifiers (compilers, linters, unit tests) with LLM-as-a-judge
  evaluators.
- Implement episodic verbal reflection (Reflexion) to record critique history and
  prevent repetitive errors.
- Mitigate critique failure modes including evaluator sycophancy, score oscillation,
  and diminishing returns.
source_records:
- p1-02-05-madaan-self-refine-2023
- p1-02-05-shinn-reflexion-2023
- p1-02-05-anthropic-evaluator-optimizer-2024
visual_assets:
- assets/images/02-agent-architectures/05-evaluator-optimizer-and-reflection/01-evaluator-optimizer-loop.png
example_paths: []
pass: architecture
learning_path: deep-dive
status: complete
last_reviewed: '2026-08-17'
---
-->

# Evaluator-optimizer and reflection

## Why this matters

Single-pass generation often fails when tasks demand high precision, strict stylistic adherence, or complex logic. When a language model produces an artifact (such as a database query, translation, or legal contract) in a single turn, it lacks the opportunity to inspect its own work, identify subtle edge cases, or fix syntax mistakes. Simply asking the model to try harder in a single prompt rarely fixes structural errors.

The **evaluator-optimizer pattern** solves this by establishing an iterative feedback loop between two distinct roles: a *generator* that drafts candidate artifacts and an *evaluator* that critiques them against explicit rubrics or test suites. By separating generation from critical assessment, systems achieve substantial accuracy gains without requiring fine-tuning. Understanding this pattern is essential before building durable multi-agent graphs and specialized [Building blocks](../03-building-blocks/chapter-plan.md).

## Simple mental model

Think of the relationship between an author and an editor at a publishing house:

1. **The Author (Generator)**: The author writes the initial manuscript draft. The author is focused on creativity, domain ideas, and narrative structure.
2. **The Editor (Evaluator)**: The editor reviews the manuscript against strict editorial guidelines, checking for factual inconsistencies, awkward phrasing, and grammatical errors. The editor does not simply say "this is bad"; they attach specific marginal notes and actionable critique.
3. **The Revision Cycle (Optimizer Loop)**: The author reads the editor's line-by-line feedback, refines the draft to address each specific critique, and resubmits the revised manuscript.
4. **The Acceptance Gate**: The cycle repeats until the manuscript satisfies all editorial standards, at which point it is approved for printing.

In software architecture, decoupling the author from the editor prevents the generator from falling victim to its own blind spots and confirmation bias.

## Position in the agent workflow

The visual below illustrates the core iterative cycle of the evaluator-optimizer architecture, linking generation, evaluation, critique feedback, and quality acceptance.

![A wide educational cartoon illustration showing the Evaluator-Optimizer architecture: on the left, a cute blue robot Generator drafts code on a scroll; in the center, a green inspector robot Evaluator checks the draft against a Rubric & Unit Tests clipboard; a feedback arrow carries actionable critique back to the Generator; and an exit arrow leads to Final Optimized Output with a green checkmark badge.](../../assets/images/02-agent-architectures/05-evaluator-optimizer-and-reflection/01-evaluator-optimizer-loop.png)

*Figure 1. The evaluator-optimizer architecture. The generator model produces drafts, while the evaluator model critiques against objective rubrics and test suites, iterating until reaching acceptance criteria.*

As established in [Agent foundations](../01-agent-foundations/chapter-plan.md) and [Architecture selection criteria](01-architecture-selection-criteria.md), evaluator-optimizer loops provide a controlled middle ground between rigid deterministic pipelines and open-ended autonomous agent loops.

## How it works

The evaluator-optimizer workflow operates across four structured phases:

1. **Initial Generation**: Given a user specification and context prompt, the generator model creates candidate artifact $A_0$.
2. **Evaluation & Verification**: The evaluator component inspects $A_k$ against predefined criteria. The evaluator can be:
   - **Deterministic**: A software compiler, test runner, regex validator, or security linter (binary pass/fail).
   - **Model-Directed (LLM-as-a-Judge)**: A separate model instance evaluating qualitative dimensions (e.g., tone, completeness, adherence to brand guidelines) using a structured rubric.
   - **Hybrid**: Running deterministic code verification first, followed by model rubric scoring.
3. **Feedback Synthesis (Critique)**: If $A_k$ fails any evaluation metric, the evaluator compiles a structured critique $C_k$ detailing exactly what failed and suggesting specific remediation steps (Madaan et al., 2023).
4. **Iterative Refinement (Optimization)**: The generator receives the original prompt, prior draft $A_k$, and critique $C_k$, outputting revised artifact $A_{k+1}$. The loop terminates when all criteria pass or when the maximum iteration limit is reached.

### Verbal reflection and episodic memory

A key evolution of the evaluator-optimizer pattern is **verbal reflection** (Shinn et al., 2023, *Reflexion*). Rather than updating model weights, the system converts environment feedback and evaluator critiques into explicit verbal summaries stored in episodic memory.

When the agent attempts the next turn or a similar future task, past reflection summaries are injected into the prompt context (e.g., *"Past mistake: failed to escape SQL wildcards in user search queries; Solution: use parameterized bindings"*), preventing the agent from repeating identical failure modes.

## Main variants

1. **Self-Refine**: A single model alternates between generating, providing self-critique, and refining its own output in a unified prompt context (Madaan et al., 2023).
2. **Two-Model Adversarial / Cooperative Pair**: Uses two distinct model configurations (e.g., a fast creative model for drafting and a larger reasoning model with a strict temperature of 0.0 for evaluation).
3. **Test-Driven Refinement**: Uses executable test suites (such as `pytest` or `cargo test`) as the authoritative evaluator, feeding compiler diagnostics and traceback outputs directly into the optimizer prompt.

## Minimal implementation

The following Python script implements a robust evaluator-optimizer harness for SQL query generation with deterministic schema checking:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from typing import Dict, Any, Tuple

class EvaluationModelClient:
    def call(self, prompt: str) -> str:
        if "Draft SQL" in prompt:
            return "SELECT user, SUM(amount) FROM orders WHERE date > '2026-01-01';"
        if "Critique" in prompt:
            if "GROUP BY" not in prompt:
                return "FAIL: Aggregation SUM(amount) requires a GROUP BY user clause."
            return "PASS: Query conforms to schema and aggregations are valid."
        if "Refine SQL" in prompt:
            return "SELECT user, SUM(amount) FROM orders WHERE date > '2026-01-01' GROUP BY user;"
        return "SELECT 1;"

def evaluate_sql_candidate(query: str, client: EvaluationModelClient) -> Tuple[bool, str]:
    """Hybrid evaluator: checks syntax deterministically, then queries model rubric."""
    # Deterministic check
    if not query.strip().upper().startswith("SELECT"):
        return False, "Query must begin with SELECT."

    # Model rubric critique
    feedback = client.call(f"Critique SQL query: {query}")
    if feedback.startswith("PASS"):
        return True, feedback
    return False, feedback

def evaluator_optimizer_loop(request: str, client: EvaluationModelClient, max_rounds: int = 3) -> Dict[str, Any]:
    current_draft = client.call(f"Draft SQL for: {request}")

    for round_num in range(1, max_rounds + 1):
        is_valid, critique = evaluate_sql_candidate(current_draft, client)
        if is_valid:
            return {"status": "ACCEPTED", "rounds": round_num, "query": current_draft}

        # Optimizer step
        current_draft = client.call(f"Refine SQL for '{request}' given critique: '{critique}'. Current draft: '{current_draft}'")

    return {"status": "MAX_ROUNDS_EXCEEDED", "rounds": max_rounds, "query": current_draft}
```

</details>

## Framework implementations

- **LangGraph**: Constructs reflection loops using a cyclic graph containing a `generate` node, an `evaluate` node, and a conditional edge that routes to `END` on success or back to `generate` with feedback.
- **Anthropic Agent Patterns**: Details the Evaluator-Optimizer pattern as the recommended architecture for constrained translation, code synthesis, and multi-draft copywriting.
- **Google Agent Development Kit (ADK)**: Provides verifier and critic abstractions designed to validate tool outputs and structured documents before returning them to client callers.

## Data flow and state changes

Trace the state progression across an iterative code-refinement loop:

| Round | Active Role | Input Payload | Generated Output | State Status |
| --- | --- | --- | --- | --- |
| $k = 0$ | Generator | User Task: *"Parse JSON timestamps"* | Candidate function $A_0$ | `DRAFTED` |
| $k = 1$ | Evaluator | Candidate $A_0$ + Unit Test Suite | Test Failure: `ValueError on ISO-8601 with Z timezone` | `CRITIQUED` |
| $k = 1$ | Optimizer | $A_0$ + Critique $C_1$ | Revised function $A_1$ (added timezone handler) | `REVISED` |
| $k = 2$ | Evaluator | Candidate $A_1$ + Unit Test Suite | `12/12 unit tests passed. Clean syntax.` | `ACCEPTED` |

## Trust boundaries

1. **Evaluator Impartiality Boundary**: The evaluator prompt and rubric must remain immutable and isolated from the generator output to prevent the generator from overriding evaluation rules.
2. **Deterministic Pre-Filter Isolation**: Running untrusted generated code against a deterministic test runner requires an isolated ephemeral sandbox (such as Docker or gVisor) to prevent malicious side effects.
3. **Critique Sanitization**: When evaluating third-party documents, critiques must not regurgitate unescaped prompt injection payloads into the optimizer context.

## Reliability failures

- **Evaluator Sycophancy**: An unhardened LLM evaluator praising poor drafts and marking flawed outputs as `PASS` due to flattering prompt language.
- **Critique Oscillation**: The generator alternates between two contradictory styles across successive turns because the evaluator rubric contains ambiguous or conflicting instructions.
- **Diminishing Returns**: Expending multiple expensive model inferences to make trivial punctuation or synonym edits without substantive improvement in quality.

## Worked example

Consider generating a strict JSON configuration for a cloud firewall:
1. **Round 1 (Drafting)**: Generator emits JSON containing firewall rules, but includes invalid trailing commas.
2. **Round 1 (Evaluation)**: Deterministic parser runs `json.loads()` and catches `JSONDecodeError: Trailing comma at line 14`.
3. **Round 2 (Refinement)**: Optimizer receives the exact line number and error message, strips the trailing comma, and resubmits.
4. **Round 2 (Evaluation)**: JSON parser succeeds. Evaluator model checks firewall rule semantics against security policy: *"PASS: Port 22 is restricted to internal subnet."*
5. **Acceptance**: Validated configuration is committed to production repository.

## Limitations and trade-offs

- **Token Multiplier ($2 \times K$)**: Each evaluation round requires both an evaluation call and a revision call, doubling token usage per iteration.
- **Latency Bounding**: Multiple critique loops increase end-to-end response times, making pure evaluator-optimizer loops unsuitable for real-time interactive user interfaces.

## Security preview

In evaluator-optimizer systems, the evaluator acts as a critical security gate. If an attacker crafts an input designed to manipulate the evaluator (e.g., prompt injection convincing the evaluator that a malicious payload is safe), the gate fails open. Furthermore, using models as automated security reviewers introduces vulnerability blind spots. We examine automated validation security and evaluator jailbreaks in [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security chapters.

## Open research questions

- How can evaluators dynamically calibrate their critique depth to terminate early when marginal quality gains fall below statistical significance?
- What verification frameworks can formally guarantee that an optimizer will converge rather than oscillate when balancing competing rubric criteria?

## Key takeaways

- The **evaluator-optimizer pattern** decouples artifact creation from critical quality assessment, enabling progressive self-correction.
- **Deterministic evaluators** (compilers, linters, unit tests) provide fast, objective, zero-token validation gates that should always precede model-as-a-judge reviews.
- **Verbal reflection (Reflexion)** converts execution errors into structured textual memories, preventing agents from repeating past failure trajectories.
- Production systems must enforce hard iteration caps (typically 2 to 4 rounds) to prevent infinite loops, oscillation, and diminishing returns.

## References

- Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Welleck, S., Majumder, B. P., Gupta, S., Yazdanbakhsh, A., & Clark, P. *Self-Refine: Iterative Refinement with Self-Feedback*. Advances in Neural Information Processing Systems (NeurIPS), 2023. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651).
- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. *Reflexion: Language Agents with Verbal Reinforcement Learning*. Advances in Neural Information Processing Systems (NeurIPS), 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366).
- Anthropic. *Building Effective Agents: Evaluator-Optimizer Pattern*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Research](https://www.anthropic.com/research/building-effective-agents).

---

[Next Unit: State machines and event-driven graphs →](chapter-plan.md)
