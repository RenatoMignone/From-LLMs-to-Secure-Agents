#!/usr/bin/env python3
"""
Context Budget Packager and Ordering Engine
Demonstrates token budget partitioning, greedy relevance-based chunk selection,
and attention-optimized prompt ordering (primacy and recency anchors).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class KnowledgeChunk:
    chunk_id: str
    text: str
    relevance_score: float  # 0.0 to 1.0
    token_count: int


@dataclass
class TokenBudgetAllocation:
    total_limit: int
    system_reserve: int
    user_reserve: int
    headroom_reserve: int
    evidence_budget: int
    history_budget: int


class ContextBudgetManager:
    def __init__(self, total_context_limit: int = 4096, headroom_tokens: int = 512):
        self.total_limit = total_context_limit
        self.headroom = headroom_tokens

        # Calculate available budget for dynamic context
        usable_budget = self.total_limit - self.headroom
        self.system_budget = 300
        self.user_budget = 200
        remaining = usable_budget - (self.system_budget + self.user_budget)

        # Partition remaining between RAG evidence (60%) and dialogue history (40%)
        self.evidence_budget = int(remaining * 0.60)
        self.history_budget = remaining - self.evidence_budget

    def select_evidence_knapsack(self, candidates: List[KnowledgeChunk]) -> Tuple[List[KnowledgeChunk], int]:
        """Greedily selects top-relevance chunks that strictly fit the evidence token budget."""
        # Sort candidates descending by relevance score
        sorted_chunks = sorted(candidates, key=lambda c: c.relevance_score, reverse=True)
        selected: List[KnowledgeChunk] = []
        used_tokens = 0

        for chunk in sorted_chunks:
            if used_tokens + chunk.token_count <= self.evidence_budget:
                selected.append(chunk)
                used_tokens += chunk.token_count

        return selected, used_tokens

    def build_ordered_prompt(
        self,
        system_policy: str,
        user_query: str,
        selected_evidence: List[KnowledgeChunk],
        recent_history: List[str],
        schema_reminder: str,
    ) -> List[Dict[str, str]]:
        """
        Orders context to maximize transformer attention:
        1. Primacy Anchor: System & Safety Policy (Index 0)
        2. Middle Body: Retrieved Evidence & Conversation History
        3. Recency Anchor: Current User Intent & Strict Output Schema (Tail)
        """
        # 1. Primacy Anchor (System)
        system_message = {
            "role": "system",
            "content": f"# CORE SYSTEM POLICY (IMMUTABLE)\n{system_policy}",
        }

        # 2. Middle Body (Evidence + History)
        evidence_sections = [
            f"<doc id='{c.chunk_id}' score='{c.relevance_score:.2f}'>\n{c.text}\n</doc>"
            for c in selected_evidence
        ]
        history_sections = [f"<history_turn>\n{h}\n</history_turn>" for h in recent_history]

        middle_body = "\n\n".join(
            ["# RETRIEVED KNOWLEDGE CONTEXT"]
            + evidence_sections
            + ["# RECENT EXECUTION HISTORY"]
            + history_sections
        )

        # 3. Recency Anchor (User Query + Output Schema Reminder)
        tail_payload = (
            f"{middle_body}\n\n"
            f"# ACTIVE USER TASK\n{user_query}\n\n"
            f"# OUTPUT FORMAT REQUIREMENT (RECENCY ANCHOR)\n{schema_reminder}"
        )

        return [
            system_message,
            {"role": "user", "content": tail_payload},
        ]


def main() -> None:
    manager = ContextBudgetManager(total_context_limit=2048, headroom_tokens=400)

    system_policy = "You are a financial risk assessment agent. Follow strict deterministic validation."
    user_query = "Calculate credit risk tier for Enterprise Corp and flag unusual transactions."
    schema_reminder = "Emit JSON response matching Schema: {'tier': str, 'risk_score': float, 'flags': list}."

    history = [
        "Turn 1: User requested portfolio summary.",
        "Turn 2: Agent queried account database for client ID 849.",
    ]

    candidate_chunks = [
        KnowledgeChunk("doc-01", "Enterprise Corp annual revenue: $45M, debt ratio: 0.28.", 0.95, 120),
        KnowledgeChunk("doc-02", "Pending wire transfer of $1.2M to offshore subsidiary on 2026-08-12.", 0.91, 140),
        KnowledgeChunk("doc-03", "Standard corporate tax filings for fiscal year 2024.", 0.45, 350),
        KnowledgeChunk("doc-04", "CEO quarterly shareholder letter regarding AI investments.", 0.30, 420),
        KnowledgeChunk("doc-05", "Historical credit default swap index spread from 2021.", 0.15, 500),
    ]

    selected_evidence, evidence_tokens = manager.select_evidence_knapsack(candidate_chunks)
    messages = manager.build_ordered_prompt(
        system_policy, user_query, selected_evidence, history, schema_reminder
    )

    print("=" * 80)
    print("CONTEXT BUDGET ALLOCATION BREAKDOWN")
    print("=" * 80)
    print(f"Total Context Window Limit:   {manager.total_limit} tokens")
    print(f"Completion Headroom Reserved: {manager.headroom} tokens")
    print(f"Evidence Budget:              {manager.evidence_budget} tokens (Used: {evidence_tokens} tokens)")
    print(f"Selected Chunks:              {[c.chunk_id for c in selected_evidence]}")
    print(f"Dropped Low-Relevance Chunks: {[c.chunk_id for c in candidate_chunks if c not in selected_evidence]}")
    print("-" * 80)
    print("ORDERED PROMPT STRUCTURE:")
    for msg in messages:
        print(f"\n--- [Role: {msg['role']}] ---")
        print(msg['content'])
    print("=" * 80)


if __name__ == "__main__":
    main()
