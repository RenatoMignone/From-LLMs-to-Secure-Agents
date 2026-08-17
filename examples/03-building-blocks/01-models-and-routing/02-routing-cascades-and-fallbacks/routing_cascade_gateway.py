"""Model Routing Cascades and Circuit Breaker Gateway.

Demonstrates:
1. Dynamic threshold router (directing simple queries to SLMs and complex queries to LLMs)
2. Progressive confidence cascade (escalating upon verification failure)
3. Circuit breaker provider fallback (rerouting traffic upon simulated 429/500 outages)
"""

from typing import Dict, Any, Optional
import time

class ModelGateway:
    """Manages routing, escalation cascades, and circuit breaker fallbacks."""
    def __init__(self):
        self.circuit_open = False
        self.consecutive_failures = 0
        self.failure_threshold = 3

    def mock_model_call(self, model: str, prompt: str) -> Dict[str, Any]:
        """Simulates provider API responses and simulated outages."""
        if model == "primary-provider" and self.circuit_open:
            raise ConnectionError("Circuit breaker OPEN: Primary provider is down.")

        if "complex_audit" in prompt and model == "small-slm":
            return {"status": "SUCCESS", "confidence": 0.40, "output": "Partial analysis."}
        if model == "small-slm":
            return {"status": "SUCCESS", "confidence": 0.95, "output": "SLM resolved query cleanly."}
        if model == "frontier-llm":
            return {"status": "SUCCESS", "confidence": 0.99, "output": "Frontier LLM verified response."}
        return {"status": "SUCCESS", "confidence": 0.90, "output": f"Handled by {model}"}

    def route_query(self, prompt: str) -> str:
        """Heuristic / Classifier Router: selects initial tier."""
        complexity_keywords = ["audit", "vulnerability", "formal verification", "architecture"]
        is_complex = any(k in prompt.lower() for k in complexity_keywords)
        return "frontier-llm" if is_complex else "small-slm"

    def execute_cascade(self, prompt: str, min_confidence: float = 0.85) -> Dict[str, Any]:
        """Progressive cascade: tries fast model, escalates if confidence is insufficient."""
        tier1_res = self.mock_model_call("small-slm", prompt)
        if tier1_res["confidence"] >= min_confidence:
            return {"tier": "Tier 3 (SLM)", "result": tier1_res["output"], "escalated": False}

        # Escalate to Frontier Model
        tier2_res = self.mock_model_call("frontier-llm", prompt)
        return {"tier": "Tier 1 (Frontier)", "result": tier2_res["output"], "escalated": True}

    def call_with_circuit_breaker(self, prompt: str) -> Dict[str, Any]:
        """Executes call on primary provider, falling back to secondary upon failure."""
        if self.consecutive_failures >= self.failure_threshold:
            self.circuit_open = True

        if not self.circuit_open:
            try:
                # Primary attempt
                return {"provider": "Primary (OpenAI/Anthropic)", "data": self.mock_model_call("primary-provider", prompt)}
            except Exception as e:
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.failure_threshold:
                    self.circuit_open = True
                # Fallback to secondary
                return {"provider": "Secondary Fallback (Google/Local)", "data": self.mock_model_call("secondary-provider", prompt), "fallback": True}
        else:
            # Direct to secondary while circuit is OPEN
            return {"provider": "Secondary Fallback (Google/Local)", "data": self.mock_model_call("secondary-provider", prompt), "circuit_status": "OPEN"}

if __name__ == "__main__":
    gateway = ModelGateway()

    print("=== 1. TESTING DYNAMIC ROUTER ===")
    print("Simple query routed to:", gateway.route_query("What is 2 + 2?"))
    print("Complex query routed to:", gateway.route_query("Perform formal vulnerability audit of auth.py"))

    print("\n=== 2. TESTING PROGRESSIVE CASCADE ===")
    res_simple = gateway.execute_cascade("Summarize short memo")
    print(f"Simple Task: Tier={res_simple['tier']}, Escalated={res_simple['escalated']}")
    res_complex = gateway.execute_cascade("Run complex_audit on smart contract")
    print(f"Complex Task: Tier={res_complex['tier']}, Escalated={res_complex['escalated']}")

    print("\n=== 3. TESTING CIRCUIT BREAKER FALLBACK ===")
    # Simulate tripping the circuit
    gateway.circuit_open = True
    fallback_res = gateway.call_with_circuit_breaker("Emergency failover test query")
    print(f"Gateway Response Provider: {fallback_res['provider']}")
    print(f"Data: {fallback_res['data']['output']}")
