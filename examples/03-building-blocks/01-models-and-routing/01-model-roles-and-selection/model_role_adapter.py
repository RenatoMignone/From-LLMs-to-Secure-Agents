"""Model Role Configuration and Provider Adapter Pattern.

Demonstrates configuring multi-provider model roles (Planner, Router, Worker, Evaluator)
and standardizing invocations across model tiers.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ModelRole(Enum):
    PLANNER = "planner"
    ROUTER = "router"
    WORKER = "worker"
    EVALUATOR = "evaluator"

@dataclass
class ModelProfile:
    name: str
    provider: str
    cost_per_1m_tokens: float
    context_window: int
    tier: str

class ProviderAdapter:
    """Standardizes API calling signatures across diverse model vendors."""
    def __init__(self, role_registry: Dict[ModelRole, ModelProfile]):
        self.registry = role_registry

    def call_role(self, role: ModelRole, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        profile = self.registry.get(role)
        if not profile:
            raise ValueError(f"No model configured for role: {role}")

        # Mock normalized response from provider
        response_text = f"[{profile.provider}::{profile.name}] Generated output for role {role.value}."
        mock_tokens = len(prompt.split()) + 30
        cost = (mock_tokens / 1_000_000) * profile.cost_per_1m_tokens

        return {
            "role": role.value,
            "model": profile.name,
            "provider": profile.provider,
            "content": response_text,
            "tokens_used": mock_tokens,
            "estimated_cost_usd": round(cost, 6)
        }

if __name__ == "__main__":
    # Define production role-to-model mapping
    role_config = {
        ModelRole.PLANNER: ModelProfile("gemini-1.5-pro", "google", 3.50, 1_000_000, "Tier 1"),
        ModelRole.ROUTER: ModelProfile("llama-3.2-3b", "local-ollama", 0.00, 32_000, "Tier 3"),
        ModelRole.WORKER: ModelProfile("claude-3-5-sonnet", "anthropic", 3.00, 200_000, "Tier 2"),
        ModelRole.EVALUATOR: ModelProfile("gpt-4o", "openai", 2.50, 128_000, "Tier 1")
    }

    adapter = ProviderAdapter(role_config)

    print("=== MODEL ROLE INVOCATIONS ===")
    for role in [ModelRole.ROUTER, ModelRole.PLANNER, ModelRole.WORKER, ModelRole.EVALUATOR]:
        res = adapter.call_role(role, "Execute financial analysis step")
        print(f"\nRole: {res['role'].upper()} -> Model: {res['model']} ({res['provider']})")
        print(f"  Output: {res['content']}")
        print(f"  Cost:   ${res['estimated_cost_usd']}")
