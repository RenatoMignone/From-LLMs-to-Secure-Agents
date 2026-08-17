<!--
---
title: Routing, cascades, and fallbacks
unit_id: P1-03-01-02
summary: Explores dynamic model routing, progressive escalation cascades, circuit
  breaker patterns, and multi-provider fallbacks for high-availability agent architectures.
prerequisites:
- Read [Model roles and selection](01-model-roles-and-selection.md).
- Read [Architecture selection criteria](../../02-agent-architectures/01-architecture-selection-criteria.md).
learning_objectives:
- Implement dynamic routing mechanisms including rule-based, embedding similarity,
  and learned threshold routers.
- Design progressive model cascades (FrugalGPT) that escalate from fast SLMs to frontier
  reasoning models upon confidence failure.
- Construct resilient circuit breaker gateways with automated provider failover, jittered
  retries, and graceful degradation.
- Mitigate cascade failure modes including latency stacking, thundering herd failover
  storms, and router classification bypass.
source_records:
- p1-03-01-02-ong-routellm-cascades-2024
- p1-03-01-02-chen-frugalgpt-cascades-2023
- p1-03-01-02-netflix-circuit-breakers-fallbacks-2023
visual_assets: []
example_paths:
- examples/03-building-blocks/01-models-and-routing/02-routing-cascades-and-fallbacks/routing_cascade_gateway.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-17'
---
-->

# Routing, cascades, and fallbacks

## Why this matters

In production systems, model APIs do not operate in a vacuum. Cloud providers suffer outages, enforce strict rate limits (HTTP 429), and experience unpredictable latency spikes. Furthermore, routing every incoming prompt directly to a top-tier frontier model is financially unsustainable when 70% of user queries require only basic reasoning.

**Routing, cascades, and fallbacks** transform fragile single-endpoint setups into resilient, cost-effective inference pipelines (Chen et al., 2023; Ong et al., 2024). By dynamically classifying task complexity, progressively escalating across model tiers upon validation failures, and switching to backup providers during upstream outages, systems maintain 99.99% availability while keeping inference costs minimal. Mastering these patterns is crucial as we advance through [Context construction](../02-context-construction/chapter-plan.md) and tool execution.

## Simple mental model

Think of an emergency response dispatch network:

1. **The 911 Dispatcher (Dynamic Router)**: Evaluates incoming calls. A cat stuck in a tree routes to local animal control (fast, low-cost specialist), while a multi-alarm building fire instantly dispatches full urban search and rescue (frontier response).
2. **Escalation Ladder (Progressive Cascade)**: When a patrol officer arrives at a minor dispute and discovers an active armed robbery, the officer immediately radios for SWAT backup. The system begins with standard resources and escalates dynamically only when necessary.
3. **Backup Power Generator (Circuit Breaker & Fallback)**: When the municipal power grid suffers a blackout, the hospital's automatic transfer switch trips open and engages on-site diesel generators within milliseconds, preventing power loss to operating rooms.

In agent engineering, routing dispatches the appropriate model tier, cascades escalate upon failure, and circuit breakers guarantee uptime when providers fail.

## Position in the agent workflow

The figures below outline model routing cascades and the three-state circuit breaker failover lifecycle.

> [!NOTE]
> *Visual illustrations (Figure 1: Model Routing & Progressive Cascade Architecture; Figure 2: Model Gateway Circuit Breaker & Fallback Lifecycle) are staged for AI generation once API quota resets. Prompts are preserved in `source/`.*

*Figure 1. Model routing and progressive cascade architecture. Queries are routed based on complexity score thresholds or escalated step-by-step through a multi-tier cascade.*

*Figure 2. Circuit breaker and fallback lifecycle. The gateway automatically diverts traffic to secondary provider endpoints during upstream outages, resetting once health probes succeed.*

As introduced in [Model roles and selection](01-model-roles-and-selection.md), routing and fallbacks provide the resilience layer protecting downstream agent execution from infrastructure failures.

## How it works

Building a resilient model gateway involves three complementary mechanisms (Ong et al., 2024; Netflix, 2023):

### 1. Dynamic routing topologies

- **Rule-Based Routers**: Fast deterministic checks (regex patterns, input token count, keyword triggers) routing simple queries to specific models with zero added latency.
- **Embedding Similarity Routers**: Converts incoming queries into dense vectors and calculates cosine similarity against representative task clusters (e.g., coding, translation, math).
- **Learned Threshold Routers (RouteLLM)**: A lightweight neural classifier or small language model trained on preference data that predicts a complexity score $\theta \in [0, 1]$. Queries with $\theta \ge \text{threshold}$ route to frontier models; otherwise, they route to small SLMs.

### 2. Progressive escalation cascades (FrugalGPT)

Rather than predicting complexity upfront, an **escalation cascade** attempts generation on a lower-tier model and inspects the output (Chen et al., 2023):
1. **Tier 3 Attempt**: The query is sent to a fast, cheap SLM ($A_0$).
2. **Verification Gate**: A fast verifier (e.g., regex, deterministic JSON parser, or token log-probability confidence score) checks $A_0$.
3. **Escalation Trigger**: If $A_0$ is invalid or low-confidence, the gateway automatically dispatches the query to a Tier 2 or Tier 1 model, passing the failure diagnostics along.

### 3. Circuit breaker & multi-provider fallback

To handle provider rate limits (HTTP 429) and service outages (HTTP 500/503), the gateway wraps provider calls in a **Circuit Breaker** (Netflix, 2023):
- **CLOSED**: Requests flow normally to the primary provider (e.g., OpenAI).
- **OPEN**: When consecutive failures exceed a threshold (e.g., 5 failures in 30 seconds), the circuit trips open. All incoming requests immediately divert to a secondary provider (e.g., Google Gemini or local vLLM) with zero dropped calls.
- **HALF-OPEN**: After a cooldown period (e.g., 60 seconds), a small fraction of canary requests probe the primary provider. If the canary succeeds, the circuit resets to CLOSED.

## Main variants

1. **Speculative Dual-Inference**: Dispatches requests to a small model and large model concurrently; if the small model finishes first with high confidence, the large model request is canceled to save GPU compute.
2. **Cross-Region Cloud Failover**: Routes traffic between US-East, EU-Central, and Asia-East cloud regions of the same provider to bypass regional rate limits.
3. **Cloud-to-Local Graceful Degradation**: Falls back to local on-premise models (via Ollama or llama.cpp) when cloud network connectivity is severed.

## Minimal implementation

The following Python script implements a functional model gateway with dynamic routing, confidence cascades, and circuit breaker failover:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from typing import Dict, Any
import time

class ModelGateway:
    """Manages routing, escalation cascades, and circuit breaker fallbacks."""
    def __init__(self):
        self.circuit_open = False
        self.consecutive_failures = 0
        self.failure_threshold = 3

    def mock_call(self, model: str, prompt: str) -> Dict[str, Any]:
        if model == "primary" and self.circuit_open:
            raise ConnectionError("Primary provider unavailable (HTTP 503)")
        if "audit" in prompt and model == "slm":
            return {"confidence": 0.45, "content": "Partial SLM result"}
        return {"confidence": 0.95, "content": f"Handled successfully by {model}"}

    def route(self, prompt: str) -> str:
        """Route based on complexity keywords."""
        complex_keywords = ["audit", "cryptography", "formal proof"]
        return "frontier" if any(k in prompt.lower() for k in complex_keywords) else "slm"

    def cascade(self, prompt: str, min_confidence: float = 0.85) -> Dict[str, Any]:
        """Progressive escalation cascade."""
        slm_res = self.mock_call("slm", prompt)
        if slm_res["confidence"] >= min_confidence:
            return {"tier": "SLM", "output": slm_res["content"], "escalated": False}

        frontier_res = self.mock_call("frontier", prompt)
        return {"tier": "Frontier", "output": frontier_res["content"], "escalated": True}

    def execute_with_fallback(self, prompt: str) -> Dict[str, Any]:
        """Circuit breaker fallback mechanism."""
        if not self.circuit_open:
            try:
                res = self.mock_call("primary", prompt)
                self.consecutive_failures = 0
                return {"provider": "Primary", "data": res}
            except Exception:
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.failure_threshold:
                    self.circuit_open = True
                return {"provider": "Secondary Fallback", "data": self.mock_call("secondary", prompt)}
        return {"provider": "Secondary Fallback (Circuit Open)", "data": self.mock_call("secondary", prompt)}
```

</details>

## Framework implementations

- **LiteLLM**: Open-source gateway providing multi-provider routing, load balancing, automatic retries with exponential backoff, and circuit breaker fallbacks across 100+ LLMs.
- **RouteLLM**: Lightweight routing framework trained on preference data from Chatbot Arena to dynamically dispatch between weak and strong models.
- **Google Cloud Vertex AI Model Garden**: Provides enterprise load balancers and cross-region routing for Gemini and open models.

## Data flow and state changes

Trace the state of a request encountering a provider rate limit and falling back:

| Event Step | Active Component | State / Status | Gateway Decision | Telemetry Emitted |
| --- | --- | --- | --- | --- |
| 1 | Ingress Request | `PENDING` | Dispatch to Primary Provider (Claude 3.5) | `request_started` |
| 2 | Primary Call | `ERROR (HTTP 429)` | Primary rate limit hit; record failure | `failure_count = 1` |
| 3 | Retry / Failover | `FAILOVER_TRIGGERED` | Route payload to Secondary Provider (Gemini Pro) | `failover_to_secondary` |
| 4 | Secondary Call | `SUCCESS (200 OK)` | Parse structured JSON response | `latency_ms = 420` |
| 5 | Client Response | `COMPLETED` | Return result seamlessly to client | `status = SUCCESS` |

## Trust boundaries

1. **Provider Data Sharing Boundary**: Falling back across multiple commercial providers (e.g., from OpenAI to Anthropic to Google) means user prompts cross multiple vendor legal agreements. Enterprise gateways must ensure all configured fallback providers meet identical compliance standards.
2. **Router Manipulation Boundary**: An attacker crafting adversarial prompts could intentionally spoof low-complexity signals to force sensitive queries into weaker, unhardened SLMs lacking robust security filters.
3. **Payload Translation Boundary**: Different providers use slightly different tool-calling and JSON formatting conventions. Gateway adapters must sanitize and validate schema translations during failovers.

## Reliability failures

- **Latency Stacking in Deep Cascades**: A 3-tier cascade where each tier times out before escalating, resulting in a user waiting $3 \times 10\text{s} = 30\text{s}$ for a failure response.
- **Thundering Herd Failover Storm**: When a primary provider goes down, all concurrent traffic instantaneously shifts to a secondary provider, immediately overwhelming the secondary provider's rate limits.
- **Incompatible Output Schemas**: A fallback model failing to support strict JSON schemas, returning raw unparsed markdown that crashes downstream tool parsers.

## Worked example

Consider an automated code security scanner processing pull requests:
1. **Dynamic Routing**: The gateway uses a learned router. Files under 100 lines with standard formatting route to a fast Tier 3 model ($0.02/1M tokens).
2. **Cascade Trigger**: A complex 1,500-line cryptographic module is scanned by the Tier 3 model, but the output verifier flags a low confidence score ($0.52$).
3. **Escalation**: The cascade escalates the module to a Tier 1 frontier reasoning model with an extended context window ($5.00/1M tokens), which accurately identifies a subtle timing attack.
4. **Resilience**: During peak hours, the primary cloud provider returns HTTP 429; the gateway's circuit breaker diverts traffic to a secondary cloud provider within 15ms, maintaining unbroken CI/CD scanning.

## Limitations and trade-offs

- **Router Evaluation Overhead**: Embedding-based and model-based routers add 20ms to 60ms of upfront routing latency before the primary prompt begins execution.
- **Maintenance Complexity**: Maintaining multiple active provider accounts, API keys, and SDK versions increases operational surface area.

## Security preview

Routing mechanisms introduce **router manipulation** risks. Attackers can embed obfuscated instructions designed to deceive the classifier into routing malicious payloads to smaller models with weaker safety guardrails. Additionally, multi-provider failover can lead to accidental data exfiltration if a secondary provider lacks HIPAA/GDPR certifications. We analyze classifier evasion, multi-provider security, and policy guardrails in [Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md) and Pass 2 security chapters.

## Open research questions

- How can routers dynamically optimize routing thresholds in real time based on live token budget consumption and rolling SLA targets?
- What verification frameworks can formally guarantee semantic equivalence when falling back across diverse model architectures?

## Key takeaways

- **Dynamic routers** dispatch queries to specialized models based on rules, embeddings, or learned complexity classifiers.
- **Progressive cascades (FrugalGPT)** attempt generation on fast SLMs first and escalate to frontier models only when verification checks fail.
- **Circuit breakers** protect agent availability by automatically failing over to secondary providers during upstream HTTP 429 rate limits and 500 outages.
- Enterprise gateways must enforce strict schema normalization and data compliance agreements across all configured fallback endpoints.

## References

- Ong, I., Almahairi, A., Wu, V., Chiang, W. L., Wu, T., Gonzalez, J. E., & Stoica, I. *RouteLLM: Learning to Route to Large Language Models with Preference Data*. arXiv preprint, 2024. [arXiv:2406.18665](https://arxiv.org/abs/2406.18665).
- Chen, L., Zaharia, M., & Zou, J. *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance*. arXiv preprint, 2023. [arXiv:2305.05176](https://arxiv.org/abs/2305.05176).
- Netflix Technology Blog. *Fault Tolerance and Circuit Breakers in Distributed AI Systems*. Netflix Engineering Guidance, 2023. [Netflix Tech Blog](https://netflixtechblog.com/).

---

[Next Unit: Capability, cost, latency, and reliability →](chapter-plan.md)
