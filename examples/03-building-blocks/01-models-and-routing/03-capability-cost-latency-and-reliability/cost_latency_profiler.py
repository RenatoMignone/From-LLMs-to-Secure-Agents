"""Model capability, cost, latency, and reliability profiler.

Demonstrates tracking TTFT, TPOT, prompt caching economics, model version pinning,
and rate limit token budget enforcement.
"""

from dataclasses import dataclass
import time
from typing import Dict, Any, List, Optional


@dataclass(frozen=True)
class ModelProfile:
    name: str
    pinned_version: str
    cost_per_million_input: float
    cost_per_million_cached_input: float
    cost_per_million_output: float
    context_window: int
    typical_ttft_ms: float
    typical_tpot_ms: float  # Time per output token in ms


# Standard production capability profiles
CATALOG: Dict[str, ModelProfile] = {
    "frontier-reasoning": ModelProfile(
        name="Frontier-Reasoning",
        pinned_version="gpt-4o-2024-08-06",
        cost_per_million_input=2.50,
        cost_per_million_cached_input=1.25,
        cost_per_million_output=10.00,
        context_window=128000,
        typical_ttft_ms=650.0,
        typical_tpot_ms=25.0,
    ),
    "fast-slm": ModelProfile(
        name="Fast-SLM",
        pinned_version="claude-3-5-haiku-20241022",
        cost_per_million_input=0.80,
        cost_per_million_cached_input=0.08,
        cost_per_million_output=4.00,
        context_window=200000,
        typical_ttft_ms=180.0,
        typical_tpot_ms=12.0,
    ),
}


class TokenBudgetLimiter:
    """Tracks token consumption against rate limit ceilings (TPM / RPM)."""

    def __init__(self, max_tokens_per_minute: int = 50000, max_requests_per_minute: int = 100):
        self.max_tpm = max_tokens_per_minute
        self.max_rpm = max_requests_per_minute
        self.request_timestamps: List[float] = []
        self.token_history: List[tuple[float, int]] = []

    def check_and_record(self, tokens: int) -> bool:
        now = time.time()
        # Evict history older than 60 seconds
        self.request_timestamps = [t for t in self.request_timestamps if now - t < 60.0]
        self.token_history = [(t, count) for t, count in self.token_history if now - t < 60.0]

        current_rpm = len(self.request_timestamps)
        current_tpm = sum(count for _, count in self.token_history)

        if current_rpm + 1 > self.max_rpm or current_tpm + tokens > self.max_tpm:
            return False  # Rate limit exceeded

        self.request_timestamps.append(now)
        self.token_history.append((now, tokens))
        return True


class InferenceProfiler:
    """Calculates granular latency metrics and prompt cache financial savings."""

    def __init__(self, catalog: Dict[str, ModelProfile]):
        self.catalog = catalog

    def calculate_cost(
        self,
        model_key: str,
        uncached_input_tokens: int,
        cached_input_tokens: int,
        output_tokens: int,
    ) -> Dict[str, float]:
        profile = self.catalog[model_key]
        input_cost = (uncached_input_tokens / 1_000_000.0) * profile.cost_per_million_input
        cached_cost = (cached_input_tokens / 1_000_000.0) * profile.cost_per_million_cached_input
        output_cost = (output_tokens / 1_000_000.0) * profile.cost_per_million_output

        total_cost = input_cost + cached_cost + output_cost
        baseline_cost_without_cache = (
            (uncached_input_tokens + cached_input_tokens) / 1_000_000.0
        ) * profile.cost_per_million_input + output_cost

        savings_percent = (
            ((baseline_cost_without_cache - total_cost) / baseline_cost_without_cache) * 100.0
            if baseline_cost_without_cache > 0
            else 0.0
        )

        return {
            "input_cost_usd": round(input_cost, 6),
            "cached_input_cost_usd": round(cached_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "savings_percent": round(savings_percent, 2),
        }

    def estimate_latency(
        self, model_key: str, prompt_tokens: int, output_tokens: int, is_cached: bool = False
    ) -> Dict[str, float]:
        profile = self.catalog[model_key]
        # Prefill / TTFT is reduced by up to 75-85% when prompt is cached
        ttft_ms = profile.typical_ttft_ms * (0.25 if is_cached else 1.0)
        generation_ms = output_tokens * profile.typical_tpot_ms
        total_latency_ms = ttft_ms + generation_ms

        return {
            "ttft_ms": round(ttft_ms, 2),
            "generation_time_ms": round(generation_ms, 2),
            "total_latency_ms": round(total_latency_ms, 2),
            "tokens_per_second": (
                round(output_tokens / (generation_ms / 1000.0), 1) if generation_ms > 0 else 0.0
            ),
        }


def run_benchmark():
    profiler = InferenceProfiler(CATALOG)
    limiter = TokenBudgetLimiter(max_tokens_per_minute=100_000, max_requests_per_minute=50)

    print("=== Model Economics & Latency Profiler ===")
    prompt_tokens_system = 8000  # Large system prompt + tool definitions (cached)
    prompt_tokens_user = 500    # Fresh user input
    generated_tokens = 250

    total_request_tokens = prompt_tokens_system + prompt_tokens_user + generated_tokens
    assert limiter.check_and_record(total_request_tokens), "Rate limit hit!"

    for key, profile in CATALOG.items():
        print(f"\nEvaluating Model: {profile.name} (Pinned Version: {profile.pinned_version})")

        # Scenario A: Uncached Cold Request
        cost_cold = profiler.calculate_cost(
            key, uncached_input_tokens=8500, cached_input_tokens=0, output_tokens=generated_tokens
        )
        lat_cold = profiler.estimate_latency(
            key, prompt_tokens=8500, output_tokens=generated_tokens, is_cached=False
        )
        print(f"  [Cold Cache] Total Latency: {lat_cold['total_latency_ms']} ms (TTFT: {lat_cold['ttft_ms']} ms)")
        print(f"  [Cold Cache] Cost: ${cost_cold['total_cost_usd']}")

        # Scenario B: Warm Prompt Cache (8000 cached tokens)
        cost_warm = profiler.calculate_cost(
            key, uncached_input_tokens=500, cached_input_tokens=8000, output_tokens=generated_tokens
        )
        lat_warm = profiler.estimate_latency(
            key, prompt_tokens=8500, output_tokens=generated_tokens, is_cached=True
        )
        print(f"  [Warm Cache] Total Latency: {lat_warm['total_latency_ms']} ms (TTFT: {lat_warm['ttft_ms']} ms)")
        print(f"  [Warm Cache] Cost: ${cost_warm['total_cost_usd']} (Saved {cost_warm['savings_percent']}%)")


if __name__ == "__main__":
    run_benchmark()
