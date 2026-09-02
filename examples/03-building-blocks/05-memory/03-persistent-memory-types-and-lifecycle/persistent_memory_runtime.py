#!/usr/bin/env python3
"""Persistent Memory Types and Lifecycle Runtime.

Demonstrates:
1. Multi-tier persistent memory storage: Episodic, Semantic, and Procedural.
2. Hierarchical namespacing (/users/{user_id}, /orgs/{org_id}).
3. Three-factor memory retrieval ranking (Relevance, Recency Decay, Salience).
4. Provenance tracking, record mutation, and deletion (right-to-be-forgotten).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import math
from typing import Any, Dict, List, Optional, Set
import uuid


class MemoryTier(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


@dataclass
class MemoryRecord:
    id: str
    tier: MemoryTier
    namespace: str
    content: str
    salience: float  # Salience score in [0.0, 1.0]
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    provenance_thread_id: Optional[str] = None
    ttl_seconds: Optional[int] = None

    def is_expired(self, current_time: datetime) -> bool:
        if self.ttl_seconds is None:
            return False
        return (current_time - self.created_at).total_seconds() > self.ttl_seconds


class PersistentMemoryStore:
    """Manages multi-tier persistent memory records with 3-factor retrieval."""

    def __init__(self, decay_rate: float = 0.99) -> None:
        self.records: Dict[str, MemoryRecord] = {}
        self.decay_rate = decay_rate

    def write(
        self,
        tier: MemoryTier,
        namespace: str,
        content: str,
        salience: float,
        provenance_thread_id: Optional[str] = None,
        ttl_seconds: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> MemoryRecord:
        now = created_at or datetime.now(timezone.utc)
        record = MemoryRecord(
            id=str(uuid.uuid4()),
            tier=tier,
            namespace=namespace,
            content=content,
            salience=max(0.0, min(1.0, salience)),
            created_at=now,
            last_accessed=now,
            provenance_thread_id=provenance_thread_id,
            ttl_seconds=ttl_seconds,
        )
        self.records[record.id] = record
        return record

    def update(self, memory_id: str, new_content: str, new_salience: Optional[float] = None) -> bool:
        record = self.records.get(memory_id)
        if not record:
            return False
        record.content = new_content
        if new_salience is not None:
            record.salience = max(0.0, min(1.0, new_salience))
        record.last_accessed = datetime.now(timezone.utc)
        record.access_count += 1
        return True

    def delete(self, memory_id: str) -> bool:
        return self.records.pop(memory_id, None) is not None

    def purge_expired(self, current_time: Optional[datetime] = None) -> int:
        now = current_time or datetime.now(timezone.utc)
        expired_ids = [mid for mid, rec in self.records.items() if rec.is_expired(now)]
        for mid in expired_ids:
            del self.records[mid]
        return len(expired_ids)

    def retrieve(
        self,
        namespace_prefix: str,
        query: str,
        alpha_relevance: float = 0.5,
        beta_recency: float = 0.3,
        gamma_salience: float = 0.2,
        top_k: int = 3,
        current_time: Optional[datetime] = None,
    ) -> List[tuple[MemoryRecord, float]]:
        now = current_time or datetime.now(timezone.utc)
        query_words = set(query.lower().split())

        scored_records: List[tuple[MemoryRecord, float]] = []

        for record in self.records.values():
            if not record.namespace.startswith(namespace_prefix):
                continue
            if record.is_expired(now):
                continue

            # 1. Relevance: Token Jaccard overlap
            record_words = set(record.content.lower().split())
            intersection = query_words.intersection(record_words)
            union = query_words.union(record_words)
            relevance = len(intersection) / max(1, len(union))

            # 2. Recency: Exponential time decay based on hours elapsed
            hours_elapsed = max(0.0, (now - record.last_accessed).total_seconds() / 3600.0)
            recency = math.pow(self.decay_rate, hours_elapsed)

            # 3. Salience: Intrinsic importance
            salience = record.salience

            # Composite 3-factor score
            composite_score = (
                alpha_relevance * relevance
                + beta_recency * recency
                + gamma_salience * salience
            )

            scored_records.append((record, composite_score))

        # Sort descending by composite score
        scored_records.sort(key=lambda x: x[1], reverse=True)

        # Update last_accessed and access_count for retrieved items
        for rec, _ in scored_records[:top_k]:
            rec.last_accessed = now
            rec.access_count += 1

        return scored_records[:top_k]


def run_demonstration() -> None:
    print("=" * 65)
    print("  Demonstration: Persistent Memory Types & Lifecycle")
    print("=" * 65)

    store = PersistentMemoryStore(decay_rate=0.95)
    base_time = datetime.now(timezone.utc)

    # 1. Populate Episodic, Semantic, and Procedural Memories across namespaces
    print("\n[+] Ingesting persistent memories across hierarchical namespaces...")

    # User Alice namespace
    rec_alice_pref = store.write(
        tier=MemoryTier.SEMANTIC,
        namespace="/users/alice/preferences",
        content="Prefers Python 3.12 with asyncpg and strict typing.",
        salience=0.9,
        provenance_thread_id="thread-init-01",
        created_at=base_time - timedelta(days=5),
    )

    rec_alice_old_ep = store.write(
        tier=MemoryTier.EPISODIC,
        namespace="/users/alice/history",
        content="Refactored database connector script from psycopg2 to asyncpg.",
        salience=0.4,
        provenance_thread_id="thread-hist-01",
        created_at=base_time - timedelta(days=10),
    )

    # Global organizational procedural playbook
    store.write(
        tier=MemoryTier.PROCEDURAL,
        namespace="/orgs/acme/playbooks",
        content="Database migration procedure: Backup snapshot -> Run Alembic upgrade -> Verify integrity checksum.",
        salience=0.95,
        provenance_thread_id="org-policy-01",
        created_at=base_time - timedelta(days=30),
    )

    # User Bob namespace (tenant isolation test)
    store.write(
        tier=MemoryTier.SEMANTIC,
        namespace="/users/bob/preferences",
        content="Prefers Go with standard library sql package.",
        salience=0.8,
        provenance_thread_id="thread-bob-01",
        created_at=base_time - timedelta(days=2),
    )

    print(f"[*] Total memories stored: {len(store.records)}")

    # 2. Retrieve memories for Alice with 3-factor ranking
    print("\n[-->] Querying memories for Alice: 'database connection typing'")
    results = store.retrieve(
        namespace_prefix="/users/alice",
        query="database connection typing",
        top_k=2,
        current_time=base_time,
    )

    for record, score in results:
        print(f"  - [{record.tier.value.upper()}] (Score: {score:.3f}, Namespace: {record.namespace})")
        print(f"    Content: {record.content}")

    # 3. Update memory record (Reconciliation / Mutation)
    print(f"\n[~] Updating Alice preference record {rec_alice_pref.id}...")
    store.update(
        memory_id=rec_alice_pref.id,
        new_content="Prefers Python 3.12 with SQLAlchemy 2.0 and strict Pydantic v2 typing.",
        new_salience=0.95,
    )
    print(f"    Updated content: {store.records[rec_alice_pref.id].content}")

    # 4. Deletion (Right-to-be-Forgotten)
    print(f"\n[-] Deleting episodic record {rec_alice_old_ep.id}...")
    deleted = store.delete(rec_alice_old_ep.id)
    print(f"    Deleted successfully: {deleted}")
    print(f"    Remaining records in store: {len(store.records)}")

    print("\n[✓] Demonstration completed successfully.")


if __name__ == "__main__":
    run_demonstration()
