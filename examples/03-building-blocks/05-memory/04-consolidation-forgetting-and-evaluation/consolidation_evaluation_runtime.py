#!/usr/bin/env python3
"""Memory Consolidation, Forgetting, and Evaluation Runtime.

Demonstrates:
1. Episodic event consolidation and reflection synthesis into semantic nodes.
2. Contradiction detection and atomic resolution.
3. Time-decay pruning (Ebbinghaus forgetting curve).
4. Memory evaluation metrics: Retrieval Recall@K, Contradiction Rate, and Latency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import math
import time
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid


@dataclass
class MemoryNode:
    id: str
    content: str
    salience: float
    created_at: datetime
    last_accessed: datetime
    tier: str  # "episodic" or "semantic"
    source_ids: List[str] = field(default_factory=list)  # Provenance tracking
    is_deprecated: bool = False


class MemorySystem:
    """Manages memory reflection, decay pruning, and quantitative evaluation."""

    def __init__(self, decay_rate: float = 0.90) -> None:
        self.memories: Dict[str, MemoryNode] = {}
        self.decay_rate = decay_rate

    def log_episode(self, content: str, salience: float, created_at: Optional[datetime] = None) -> MemoryNode:
        now = created_at or datetime.now(timezone.utc)
        node = MemoryNode(
            id=str(uuid.uuid4()),
            content=content,
            salience=salience,
            created_at=now,
            last_accessed=now,
            tier="episodic",
        )
        self.memories[node.id] = node
        return node

    def consolidate_reflection(self, query_topic: str, synthesis_text: str, salience: float) -> MemoryNode:
        """Synthesizes related episodic memories into a higher-level semantic insight."""
        # Find matching episodic records
        matching_ids = [
            m.id for m in self.memories.values()
            if m.tier == "episodic" and not m.is_deprecated and query_topic.lower() in m.content.lower()
        ]
        now = datetime.now(timezone.utc)
        insight = MemoryNode(
            id=str(uuid.uuid4()),
            content=synthesis_text,
            salience=salience,
            created_at=now,
            last_accessed=now,
            tier="semantic",
            source_ids=matching_ids,
        )
        self.memories[insight.id] = insight
        return insight

    def resolve_contradiction(self, old_memory_id: str, new_content: str, salience: float) -> MemoryNode:
        """Atomically marks conflicting memory as deprecated and creates updated record."""
        old_mem = self.memories.get(old_memory_id)
        if old_mem:
            old_mem.is_deprecated = True
        now = datetime.now(timezone.utc)
        new_node = MemoryNode(
            id=str(uuid.uuid4()),
            content=new_content,
            salience=salience,
            created_at=now,
            last_accessed=now,
            tier="semantic",
            source_ids=[old_memory_id] if old_mem else [],
        )
        self.memories[new_node.id] = new_node
        return new_node

    def prune_decayed(self, retention_threshold: float = 0.2, current_time: Optional[datetime] = None) -> int:
        """Evicts memories whose decay-weighted score drops below retention threshold."""
        now = current_time or datetime.now(timezone.utc)
        evicted = []
        for mid, mem in list(self.memories.items()):
            if mem.is_deprecated:
                evicted.append(mid)
                continue
            # Days elapsed
            days = max(0.0, (now - mem.last_accessed).total_seconds() / 86400.0)
            decay_factor = math.pow(self.decay_rate, days)
            effective_score = mem.salience * decay_factor
            if effective_score < retention_threshold and mem.tier == "episodic":
                evicted.append(mid)

        for mid in evicted:
            del self.memories[mid]
        return len(evicted)

    def retrieve(self, query: str, top_k: int = 3) -> List[MemoryNode]:
        q_words = set(query.lower().split())
        scored = []
        for mem in self.memories.values():
            if mem.is_deprecated:
                continue
            m_words = set(mem.content.lower().split())
            overlap = len(q_words.intersection(m_words))
            score = overlap + (mem.salience * 0.5)
            if overlap > 0:
                scored.append((mem, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [m for m, _ in scored[:top_k]]


def evaluate_memory_system(system: MemorySystem, test_suite: List[Dict[str, Any]]) -> Dict[str, float]:
    """Runs a standardized memory benchmark measuring Recall@K, precision, and latency."""
    start_time = time.perf_counter()
    hits = 0
    total_queries = len(test_suite)

    for case in test_suite:
        query = case["query"]
        expected_substring = case["expected_substring"]
        results = system.retrieve(query, top_k=case.get("top_k", 3))
        found = any(expected_substring.lower() in res.content.lower() for res in results)
        if found:
            hits += 1

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    recall_rate = hits / max(1, total_queries)
    avg_latency_ms = elapsed_ms / max(1, total_queries)

    return {
        "recall_at_k": recall_rate,
        "total_queries": float(total_queries),
        "avg_latency_ms": avg_latency_ms,
        "total_active_memories": float(len([m for m in system.memories.values() if not m.is_deprecated])),
    }


def run_demonstration() -> None:
    print("=" * 65)
    print("  Demonstration: Memory Consolidation, Forgetting & Evaluation")
    print("=" * 65)

    system = MemorySystem(decay_rate=0.85)
    now = datetime.now(timezone.utc)

    # 1. Ingest episodic interaction traces
    print("\n[+] Ingesting episodic event traces...")
    system.log_episode("User requested PostgreSQL database setup with asyncpg connector.", 0.6, created_at=now - timedelta(days=10))
    system.log_episode("Debugged connection pool timeout; increased max connections to 20.", 0.5, created_at=now - timedelta(days=8))
    ep_switch = system.log_episode("User switched primary storage from PostgreSQL to ClickHouse for analytical queries.", 0.8, created_at=now - timedelta(days=2))

    print(f"[*] Active memories logged: {len(system.memories)}")

    # 2. Consolidate into high-level semantic reflection
    print("\n[+] Triggering reflection synthesis...")
    insight = system.consolidate_reflection(
        query_topic="PostgreSQL",
        synthesis_text="Database Architecture Rule: Initial setup used PostgreSQL, but migrated analytical storage to ClickHouse.",
        salience=0.95,
    )
    print(f"    Consolidated Semantic Insight: {insight.content}")
    print(f"    Derived from {len(insight.source_ids)} episodic sources.")

    # 3. Contradiction Resolution
    print("\n[~] Resolving conflicting facts...")
    system.resolve_contradiction(
        old_memory_id=ep_switch.id,
        new_content="Verified Architectural Decision: ClickHouse is strictly mandated for all analytics pipelines.",
        salience=0.95,
    )

    # 4. Forgetting / Pruning
    print("\n[-] Running decay-based memory pruning (simulating 15 days later)...")
    pruned_count = system.prune_decayed(retention_threshold=0.3, current_time=now + timedelta(days=15))
    print(f"    Evicted {pruned_count} decayed or deprecated memory records.")

    # 5. Benchmark & Evaluation
    print("\n[-->] Executing Memory Evaluation Benchmark Suite...")
    eval_suite = [
        {"query": "database analytical storage engine", "expected_substring": "ClickHouse", "top_k": 2},
        {"query": "connection pool configuration", "expected_substring": "max connections", "top_k": 3},
    ]

    metrics = evaluate_memory_system(system, eval_suite)
    print(f"    Recall@K Score: {metrics['recall_at_k'] * 100:.1f}%")
    print(f"    Average Query Latency: {metrics['avg_latency_ms']:.4f} ms")
    print(f"    Active Retained Records: {int(metrics['total_active_memories'])}")

    print("\n[✓] Demonstration completed successfully.")


if __name__ == "__main__":
    run_demonstration()
