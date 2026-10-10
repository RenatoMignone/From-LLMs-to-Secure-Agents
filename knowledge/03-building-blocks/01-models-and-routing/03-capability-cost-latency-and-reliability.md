<!--
---
title: Capability, cost, latency, and reliability
unit_id: P1-03-01-03
summary: Analyzes the multi-dimensional trade-offs between model capability, token
  economics, latency profiles, and operational reliability in production agent workflows.
prerequisites:
- Read [Model roles and selection](01-model-roles-and-selection.md).
- Read [Routing, cascades, and fallbacks](02-routing-cascades-and-fallbacks.md).
learning_objectives:
- Deconstruct inference latency into Time to First Token (TTFT), inter-token latency
  (TPOT), and queue delays across streaming and non-streaming modes.
- Calculate total agent loop economics including prompt token vs completion token
  pricing, context caching discounts, and reasoning token overheads.
- Evaluate model capability trade-offs across reasoning depth, tool schema adherence,
  and long-context needle degradation.
- Enforce production reliability via snapshot version pinning, rate limit (RPM/TPM)
  throttling, and deterministic sampling controls.
source_records:
- p1-03-01-03-kwon-vllm-serving-2023
- p1-03-01-03-openai-latency-versioning-2024
- p1-03-01-03-anthropic-prompt-caching-2024
visual_assets:
- assets/images/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability/01-tradeoff-pareto-frontier.png
- assets/images/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability/02-latency-anatomy-and-caching.png
example_paths:
- examples/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability/cost_latency_profiler.py
pass: architecture
learning_path: deep-dive
status: complete
last_reviewed: '2026-10-10'
---
-->

# Capability, cost, latency, and reliability

## Why this matters

Two model configurations answer Lee's request correctly, but one is slower and costs more. A third is faster yet fails on return-policy exceptions. A deployment decision needs all of those observations.

This optional chapter separates capability, price, measured latency and reliability. Its numeric examples are illustrative inputs to a comparison, not current provider prices or performance guarantees.

## Simple mental model

Think of assembling a commercial logistics fleet:

1. **Cargo aircraft:** A vehicle suited to large loads may be unnecessary for a small local delivery. Likewise, test model capability against the specific task.
2. **Delivery van:** A smaller vehicle can serve a bounded route efficiently, but capacity still matters. A smaller model is useful only if it meets the acceptance criteria.
3. **Reusable loading work:** Reusing a prepared manifest can save work. Prompt caching similarly reuses eligible input processing; savings depend on whether the request actually hits the cache.
4. **Vehicle version and traffic limits:** Recording a model version helps track changes, while request and token limits bound traffic. Neither promises identical outputs or absence of congestion.

Agent architects do not choose a single universal vehicle. They route packages to the right vehicle tier and optimize transit lanes to ensure timely delivery within budget.

## Position in the agent workflow

The figures below illustrate the multi-dimensional trade-off balancing console and the granular latency breakdown across prefill, caching, and token generation phases.

![Figure 1: Capability, cost, latency, and reliability trade-off Pareto frontier](../../../assets/images/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability/01-tradeoff-pareto-frontier.png)

*Figure 1. Capability, cost, latency, and reliability trade-off Pareto frontier. This illustrates competing dimensions. Locate feasible configurations using measured task outcomes, not model size alone.*

![Figure 2: LLM inference latency anatomy and prompt caching acceleration](../../../assets/images/03-building-blocks/01-models-and-routing/03-capability-cost-latency-and-reliability/02-latency-anatomy-and-caching.png)

*Figure 2. LLM inference latency anatomy and prompt caching acceleration. The diagram separates prompt work from output generation. Its savings and timing values are illustrative; client TTFT also includes waiting and transport.*

As shown in [Routing, cascades, and fallbacks](02-routing-cascades-and-fallbacks.md), understanding these profiles enables gateways to dynamically match each subtask to its optimal execution tier.

## How it works

Optimizing model selection requires measuring four foundational dimensions:

### 1. Capability dimensions and evaluation

Model capability is not a monolithic score. In agentic workflows, capability breaks down into four operational axes:
- **Multi-Step Reasoning Depth**: The ability to formulate valid sequential plans, verify intermediate tool outputs, and recover from execution errors without hallucinating.
- **Strict Structured Output Adherence**: The capability to reliably emit valid JSON schemas matching requested Pydantic models or tool signatures without formatting syntax errors.
- **Long-Context Retrieval Fidelity**: Maintaining needle-in-a-haystack recall across 100k+ tokens without suffering "lost-in-the-middle" attention degradation.
- **Instruction Hierarchy Robustness**: Distinguishing system instructions from untrusted user data and retrieved third-party tool outputs.

### 2. Latency anatomy: TTFT vs TPOT

Serving commonly separates prompt processing from token generation. For a response with at least one output token, define timing boundaries before estimating time to the last token. Final processing can add further delay:
$$\text{Time to last token} \approx \text{TTFT}_{\text{client}} + (N_{\text{output}} - 1) \times \text{TPOT}_{\text{mean}}$$

- **Time to First Token (TTFT)**: The duration from request dispatch until the client receives the first token. Client-observed TTFT includes transport and waiting as well as **prefill**, the initial prompt processing. Prompt length, batching and caching can affect it. Do not add network and queue delay again if they are already included in TTFT.
- **Time Per Output Token (TPOT)**: The duration required to generate each subsequent token during the auto-regressive **decode phase**. In decode, tokens are generated sequentially (memory-bandwidth bound). Measure the interval for the actual model, serving configuration and load; it need not remain constant during a response.
- **Streaming:** Partial output can make progress visible before completion. Readiness to execute a tool depends on a complete, validated request or a documented incremental protocol; a partial JSON fragment is insufficient.

### 3. Token economics and context caching

Inference costs are calculated per million tokens, with asymmetric pricing between input prompts, cached prompts, and output completions:
- **Input and output pricing:** Read the current model price table. Input, cached input and output can have different rates; there is no universal multiplier.
- **Prompt caching:** Eligibility, retention, discounts and latency effects depend on provider, model and request structure. Check the current provider contract and measure hit rates rather than assuming a shared threshold or percentage saving.
- **Reasoning-token accounting:** Some models use internal reasoning tokens. Their visibility, limits and billing are provider-specific. Include reported billable usage rather than inferring it from visible answer length.

### 4. Reliability, version pinning, and rate limits

Operational stability depends on predictable execution environments:
- **Version tracking:** Prefer a documented version identifier where available and record changes. Historical model names below belong to synthetic example profiles, not a current availability list.
- **Rate Limit Throttling (RPM & TPM)**: Cloud providers enforce hard quotas on Requests Per Minute (RPM) and Tokens Per Minute (TPM). Multi-agent architectures with parallel tool workers can easily saturate TPM limits, triggering HTTP 429 errors.
- **Sampling configuration:** Some models expose controls that can reduce variation; supported parameters differ. Do not assume temperature or seed controls are available or sufficient for exact repeatability.

## Main variants

1. **Shared hosted inference:** The provider manages inference infrastructure. The application still handles request budgets, configuration, failures and product operations.
2. **Reserved inference capacity:** Capacity and service commitments are provider-specific. Check throttling, latency and billing terms rather than assuming zero rate-limit errors.
3. **Self-Hosted Open Weights (vLLM / SGLang)**: Deploying open models (e.g., Llama 3, Qwen 2.5) on private GPU clusters. Moves inference operation to your infrastructure. Capacity limits, telemetry destinations and data-sharing choices still require explicit configuration.

## Minimal implementation

The following implementation profiles inference latency, computes cached token savings, and tracks rate limit token consumption:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass
import time
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class ModelProfile:
    name: str
    pinned_version: str
    cost_per_m_input: float
    cost_per_m_cached: float
    cost_per_m_output: float
    typical_ttft_ms: float
    typical_tpot_ms: float

CATALOG = {
    "frontier": ModelProfile("Frontier", "gpt-4o-2024-08-06", 2.50, 1.25, 10.00, 650.0, 25.0),
    "slm": ModelProfile("SLM", "claude-3-5-haiku-20241022", 0.80, 0.08, 4.00, 180.0, 12.0),
}

class InferenceProfiler:
    """Profiles latency and cost with prompt cache accounting."""
    @staticmethod
    def evaluate(model_key: str, uncached_in: int, cached_in: int, out_tokens: int) -> Dict[str, float]:
        m = CATALOG[model_key]
        cost = (uncached_in * m.cost_per_m_input + cached_in * m.cost_per_m_cached + out_tokens * m.cost_per_m_output) / 1e6
        is_cached = cached_in > 0
        ttft = m.typical_ttft_ms * (0.25 if is_cached else 1.0)
        generation_time = out_tokens * m.typical_tpot_ms
        return {
            "total_cost_usd": round(cost, 6),
            "ttft_ms": round(ttft, 2),
            "total_latency_ms": round(ttft + generation_time, 2),
        }
```

</details>

## Framework implementations

- **OpenAI API & SDK**: Native support for prompt caching (automatic on prefixes >1024 tokens), structured outputs with strict JSON schemas, and snapshot version pinning.
- **Anthropic Claude API**: Explicit prompt cache control blocks (`cache_control={"type": "ephemeral"}`), high-speed Haiku endpoints, and detailed cache-read/cache-creation token usage metrics.
- **vLLM Inference Server**: Industry-standard open-source engine implementing PagedAttention, chunked prefill, and prefix caching for self-hosted models.
- **LiteLLM**: Unified proxy that standardizes pricing calculations, tracks organization-wide spend budgets, and enforces token-rate quotas across 100+ providers.

## Data flow and state changes

Trace the lifecycle of a prompt processed by a cached model gateway:

| Step | Gateway Subsystem | State / Event | Computational Action | Telemetry Metric Recorded |
| --- | --- | --- | --- | --- |
| 1 | Ingress & Quota Check | `EVALUATING_BUDGET` | Verify client TPM and RPM limits | `rate_limit_headroom = 42%` |
| 2 | Prompt Prefix Hashing | `CACHE_LOOKUP` | Compute hash of static system prompt and tools | `cache_hit = TRUE (8,000 tokens)` |
| 3 | Prefill (Prefill Engine) | `PREFILL_ACTIVE` | Reuse cached KV tensor; process only fresh delta | `ttft_ms = 145 ms (saved 78%)` |
| 4 | Decode (Decode Engine) | `DECODE_ACTIVE` | Auto-regressively generate structured tool call | `tpot_ms = 22.4 ms / token` |
| 5 | Accounting & Egress | `COMPLETED` | Deduct discounted token fees and return response | `cost_usd = $0.00312` |

## Trust boundaries

1. **Version Drift & Behavioral Contract Boundary**: Upstream model updates can subtly alter tool calling syntax or reasoning behavior. Pinning immutable model snapshot versions maintains the validation and testing boundary.
2. **Multi-Tenant Latency Jitter Boundary**: In shared public cloud infrastructure, sudden traffic surges from unrelated tenants can cause TTFT spikes (noisy neighbor effect). Mission-critical agent loops require latency timeouts and fallback routes.
3. **Financial Budget & Spend Exhaustion Boundary**: Autonomous loops running in unbounded recursion can rapidly consume thousands of dollars in token fees. Strict per-session token budget limiters must enforce execution cutoffs.

## Reliability failures

- **Floating Alias Drift**: Pointing production agents to `gpt-4o` rather than `gpt-4o-2024-08-06`. A silent provider backend model update causes the model to omit mandatory JSON keys, breaking downstream code execution.
- **Context Degradation (Lost in the Middle)**: Packing 150,000 tokens into a model's context window. Although the context window accommodates the tokens, the model fails to retrieve key constraints located in the middle 50% of the prompt.
- **Thundering Herd Rate Limit Cascades**: When five parallel agent workers simultaneously retry failed requests without jitter, the synchronized burst immediately triggers HTTP 429 rate limit lockouts across the entire API key.

## Worked example

Consider an enterprise customer support triage agent handling 50,000 inquiries per day:
- **Baseline (Pure Frontier Uncached)**: Every query dispatches to a frontier model with 6,000 tokens of system instructions and context. Cost: $0.025 per request $\times$ 50,000 = **$1,250/day** ($37,500/month). Average latency: 4.8 seconds.
- **Optimized Tiered Architecture**:
  1. System prompt (5,500 tokens) is structured with prompt cache headers (cache hit rate: 94%).
  2. Router directs 80% of standard FAQ inquiries to a fast SLM ($0.80/M input).
  3. Escalates remaining 20% complex account disputes to a pinned frontier model.
- **Outcome**: Daily inference cost drops to **$142/day** ($4,260/month, an **88.6% cost reduction**), while average end-to-end response latency drops from 4.8s to 1.1s.

## Limitations and trade-offs

- **Cache Invalidation vs Dynamic Context**: Dynamic system prompts (e.g., injecting current timestamps or changing user IDs at the start of the prompt) invalidate the prompt cache prefix, destroying caching cost benefits.
- **Strict Determinism Limitations**: Even with `temperature = 0.0`, floating-point arithmetic across dynamic GPU batches can occasionally produce nondeterministic token selections. Critical validation must occur at the software gate rather than relying solely on model-level determinism.

## Security preview

Inference economics and reliability mechanisms introduce direct security implications:
- **Denial-of-Wallet (Resource Exhaustion)**: Attackers craft recursive prompts designed to force models into emitting maximum reasoning tokens or invalidating cache prefixes, multiplying organizational cloud spend.
- **Model Downgrade Attacks**: Adversaries manipulate routing classifications to force high-risk authentication decisions into weaker SLMs lacking hardened safety filters.
- **Cache Side-Channel Probing**: Variations in TTFT can potentially reveal whether another tenant or user recently processed similar confidential documents through shared prefix caches.

We examine denial-of-wallet defenses, model abuse controls, and side-channel risks in [Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open research questions

- How can serving engines dynamically schedule multi-agent KV caches to maximize cross-agent prefix sharing without introducing cross-tenant side channels?
- What formal verification metrics can reliably quantify long-context degradation before deploying agents to production?

## Key takeaways

- Measure client time to first token and subsequent token intervals with consistent timing boundaries.
- Prompt caching can save eligible input work; price, retention and realized savings depend on the provider contract and hit rate.
- Version tracking helps identify changes but does not freeze every runtime condition or guarantee repeatability.
- Effective agent architectures balance capability, cost, latency, and reliability by matching specific subtasks to optimal model tiers on the Pareto frontier.

<details><summary>Check your understanding</summary>

Does pinning a model version guarantee identical outputs? No. It reduces one source of change while other runtime and sampling conditions remain.

</details>

## References

- Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H., Gonzalez, J. E., Zhang, H., & Stoica, I. *Efficient Memory Management for Large Language Model Serving with PagedAttention*. Proceedings of the 29th ACM Symposium on Operating Systems Principles (SOSP), 2023. [DOI: 10.1145/3600006.3613165](https://doi.org/10.1145/3600006.3613165).
- OpenAI. *Latency Optimization, Prompt Caching, and Model Version Pinning Guide*. OpenAI Platform Documentation, 2024. [OpenAI Platform](https://platform.openai.com/docs/guides/latency-optimization).
- Anthropic. [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). Living documentation, verified October 10, 2026.

---

[Next Unit: Routing evaluation →](04-routing-evaluation.md)
