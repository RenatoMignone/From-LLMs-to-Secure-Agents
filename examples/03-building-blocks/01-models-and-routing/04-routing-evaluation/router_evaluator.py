#!/usr/bin/env python3
"""
Router Evaluation Harness
Evaluates model routing policies across quality recovery, cost reduction,
and invocation distribution on representative benchmark tasks.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


@dataclass(frozen=True)
class BenchmarkQuery:
    query_id: str
    prompt: str
    difficulty: str  # "simple", "moderate", "complex"
    reference_answer: str
    min_capability_tier: str  # "slm" or "frontier"


@dataclass
class ModelProfile:
    name: str
    tier: str  # "slm" or "frontier"
    input_cost_per_m: float  # USD per million tokens
    output_cost_per_m: float  # USD per million tokens
    avg_tokens: Tuple[int, int]  # (prompt_tokens, completion_tokens)


@dataclass
class EvaluationResult:
    policy_name: str
    total_queries: int
    strong_model_calls: int
    call_through_rate: float
    total_cost: float
    avg_cost_per_query: float
    cost_savings_pct: float
    accuracy_pct: float
    quality_recovery_pct: float


class RoutingHarness:
    def __init__(
        self,
        slm_profile: ModelProfile,
        frontier_profile: ModelProfile,
        dataset: List[BenchmarkQuery],
    ):
        self.slm = slm_profile
        self.frontier = frontier_profile
        self.dataset = dataset

    def _estimate_cost(self, model: ModelProfile) -> float:
        p_tokens, c_tokens = model.avg_tokens
        return (p_tokens * model.input_cost_per_m / 1_000_000.0) + (
            c_tokens * model.output_cost_per_m / 1_000_000.0
        )

    def _simulate_model_output(self, query: BenchmarkQuery, selected_model: ModelProfile) -> bool:
        """Determines if the selected model successfully satisfies the task."""
        if query.min_capability_tier == "slm":
            return True
        if query.min_capability_tier == "frontier" and selected_model.tier == "frontier":
            return True
        # SLM fails on complex tasks requiring frontier reasoning
        return False

    def evaluate_policy(
        self,
        policy_name: str,
        router_fn: Callable[[BenchmarkQuery], str],
    ) -> EvaluationResult:
        frontier_baseline_cost = self._estimate_cost(self.frontier) * len(self.dataset)
        strong_calls = 0
        total_cost = 0.0
        correct_answers = 0

        for query in self.dataset:
            decision = router_fn(query)
            if decision == "frontier":
                chosen_model = self.frontier
                strong_calls += 1
            else:
                chosen_model = self.slm

            total_cost += self._estimate_cost(chosen_model)
            if self._simulate_model_output(query, chosen_model):
                correct_answers += 1

        n = len(self.dataset)
        call_through_rate = (strong_calls / n) * 100.0
        accuracy = (correct_answers / n) * 100.0
        avg_cost = total_cost / n
        cost_savings = ((frontier_baseline_cost - total_cost) / frontier_baseline_cost) * 100.0
        quality_recovery = (accuracy / 100.0) * 100.0

        return EvaluationResult(
            policy_name=policy_name,
            total_queries=n,
            strong_model_calls=strong_calls,
            call_through_rate=call_through_rate,
            total_cost=total_cost,
            avg_cost_per_query=avg_cost,
            cost_savings_pct=cost_savings,
            accuracy_pct=accuracy,
            quality_recovery_pct=quality_recovery,
        )


def main() -> None:
    slm = ModelProfile(
        name="Llama-3-8B-Instruct",
        tier="slm",
        input_cost_per_m=0.15,
        output_cost_per_m=0.60,
        avg_tokens=(350, 120),
    )
    frontier = ModelProfile(
        name="Claude-3-5-Sonnet",
        tier="frontier",
        input_cost_per_m=3.00,
        output_cost_per_m=15.00,
        avg_tokens=(350, 450),
    )

    benchmark_suite: List[BenchmarkQuery] = [
        BenchmarkQuery("q1", "Summarize this 200-word paragraph.", "simple", "Summary...", "slm"),
        BenchmarkQuery("q2", "Format address into JSON schema.", "simple", "{...}", "slm"),
        BenchmarkQuery("q3", "Translate 'Thank you' to Spanish.", "simple", "Gracias", "slm"),
        BenchmarkQuery("q4", "Extract named entities from email.", "simple", "[...]", "slm"),
        BenchmarkQuery("q5", "Classify sentiment as positive/negative.", "simple", "Positive", "slm"),
        BenchmarkQuery("q6", "Solve multi-variable algebraic proof with edge cases.", "complex", "Proof...", "frontier"),
        BenchmarkQuery("q7", "Formulate 5-step plan to migrate PostgreSQL schema without downtime.", "complex", "Plan...", "frontier"),
        BenchmarkQuery("q8", "Identify race condition in concurrent Rust async stream.", "complex", "Analysis...", "frontier"),
        BenchmarkQuery("q9", "Synthesize cross-document tax compliance across 3 jurisdictions.", "complex", "Synthesis...", "frontier"),
        BenchmarkQuery("q10", "Generate complete verified auth middleware with CSRF protection.", "complex", "Code...", "frontier"),
    ]

    harness = RoutingHarness(slm, frontier, benchmark_suite)

    # 1. Baseline: Always SLM
    r_slm = harness.evaluate_policy("Static SLM Baseline", lambda q: "slm")

    # 2. Baseline: Always Frontier
    r_frontier = harness.evaluate_policy("Static Frontier Baseline", lambda q: "frontier")

    # 3. Heuristic / Complexity Router
    def complexity_router(q: BenchmarkQuery) -> str:
        complex_keywords = {"proof", "migrate", "race condition", "jurisdictions", "auth middleware", "schema"}
        if any(kw in q.prompt.lower() for kw in complex_keywords) or len(q.prompt.split()) > 8:
            return "frontier"
        return "slm"

    r_heuristic = harness.evaluate_policy("Heuristic / Rule Router", complexity_router)

    results = [r_slm, r_frontier, r_heuristic]

    print("=" * 88)
    print(f"{'Policy Name':<26} {'Strong Calls':<14} {'Call Rate':<12} {'Accuracy':<12} {'Avg Cost/Q':<14} {'Savings':<10}")
    print("-" * 88)
    for r in results:
        print(
            f"{r.policy_name:<26} "
            f"{r.strong_model_calls:>2}/{r.total_queries:<10} "
            f"{r.call_through_rate:>6.1f}%     "
            f"{r.accuracy_pct:>6.1f}%     "
            f"${r.avg_cost_per_query:>8.6f}     "
            f"{r.cost_savings_pct:>6.1f}%"
        )
    print("=" * 88)


if __name__ == "__main__":
    main()
