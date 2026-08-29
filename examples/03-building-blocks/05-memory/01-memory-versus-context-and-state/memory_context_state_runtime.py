"""
Demonstration of Memory vs. Context Window vs. Execution State in Agent Architectures.

This script implements a clear, self-contained educational runtime illustrating:
1. Context Window: Ephemeral token-budgeted prompt buffer assembled per forward pass.
2. Execution State: Mutable, thread-scoped working variables and turn history.
3. Long-Term Memory: Cross-thread persistent store supporting episodic logs,
   semantic profile facts, salience scoring, selective recall, and deletion.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import math
import uuid
from typing import Any, Dict, List, Optional


class MemoryType(Enum):
    WORKING = "working"      # Run-scoped scratchpad / state
    EPISODIC = "episodic"    # Specific autobiographical event or conversation turn
    SEMANTIC = "semantic"    # Distilled fact, preference, or concept
    PROCEDURAL = "procedural"  # Reusable skill or operational rule


@dataclass
class MemoryRecord:
    id: str
    memory_type: MemoryType
    namespace: str  # e.g., "user:alice", "tenant:acme", "global"
    content: str
    salience: float  # 0.0 to 1.0 (importance score)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: Optional[int] = None
    provenance: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        if self.ttl_seconds is None:
            return False
        elapsed = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return elapsed > self.ttl_seconds

    def score_relevance(self, query_tokens: set[str], recency_weight: float = 0.3) -> float:
        """Computes a retrieval score combining token overlap, salience, and recency."""
        content_tokens = set(self.content.lower().split())
        overlap = len(query_tokens.intersection(content_tokens))
        semantic_sim = overlap / max(1, len(query_tokens))

        elapsed_hours = max(0.01, (datetime.now(timezone.utc) - self.created_at).total_seconds() / 3600.0)
        recency_score = 1.0 / (1.0 + math.log(1.0 + elapsed_hours))

        return (1.0 - recency_weight) * (0.5 * semantic_sim + 0.5 * self.salience) + (recency_weight * recency_score)


class PersistentMemoryStore:
    """Persistent Cross-Thread Memory Store."""

    def __init__(self) -> None:
        self._records: Dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.id] = record

    def get(self, memory_id: str) -> Optional[MemoryRecord]:
        rec = self._records.get(memory_id)
        if rec and not rec.is_expired():
            rec.last_accessed_at = datetime.now(timezone.utc)
            return rec
        return None

    def search(self, namespace: str, query: str, top_k: int = 3) -> List[MemoryRecord]:
        query_tokens = set(query.lower().split())
        valid_records = [
            r for r in self._records.values()
            if r.namespace == namespace and not r.is_expired()
        ]
        # Score and rank
        scored = [(r, r.score_relevance(query_tokens)) for r in valid_records]
        scored.sort(key=lambda item: item[1], reverse=True)
        results = []
        for r, _ in scored[:top_k]:
            r.last_accessed_at = datetime.now(timezone.utc)
            results.append(r)
        return results

    def delete(self, memory_id: str) -> bool:
        if memory_id in self._records:
            del self._records[memory_id]
            return True
        return False

    def list_all(self, namespace: Optional[str] = None) -> List[MemoryRecord]:
        if namespace:
            return [r for r in self._records.values() if r.namespace == namespace and not r.is_expired()]
        return [r for r in self._records.values() if not r.is_expired()]


@dataclass
class ThreadExecutionState:
    """Thread-scoped working state and event history (short-term session state)."""
    thread_id: str
    user_id: str
    turn_count: int = 0
    variables: Dict[str, Any] = field(default_factory=dict)
    messages: List[Dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self.turn_count += 1


@dataclass
class ContextWindow:
    """Transient prompt assembly for a single model inference turn."""
    system_prompt: str
    recalled_memories: List[str]
    recent_history: List[Dict[str, str]]
    working_variables: Dict[str, Any]
    user_prompt: str

    def assemble(self) -> str:
        parts = [f"=== SYSTEM INSTRUCTIONS ===\n{self.system_prompt}\n"]
        if self.recalled_memories:
            parts.append("=== RECALLED LONG-TERM MEMORY ===")
            for mem in self.recalled_memories:
                parts.append(f"- {mem}")
            parts.append("")
        if self.working_variables:
            parts.append("=== WORKING STATE VARIABLES ===")
            for k, v in self.working_variables.items():
                parts.append(f"- {k}: {v}")
            parts.append("")
        if self.recent_history:
            parts.append("=== RECENT THREAD DIALOGUE ===")
            for msg in self.recent_history[-3:]:
                parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
            parts.append("")
        parts.append(f"User: {self.user_prompt}\nAssistant:")
        return "\n".join(parts)


def run_demonstration() -> None:
    print("=================================================================")
    print("  Demonstration: Memory vs. Context vs. Execution State")
    print("=================================================================\n")

    # 1. Initialize Long-Term Persistent Memory Store (Survives Threads)
    memory_store = PersistentMemoryStore()

    # Pre-populate long-term semantic profile for user Alice
    pref_id = str(uuid.uuid4())
    memory_store.put(MemoryRecord(
        id=pref_id,
        memory_type=MemoryType.SEMANTIC,
        namespace="user:alice",
        content="Prefers concise Python code examples with type annotations.",
        salience=0.9,
        provenance={"source_thread": "thread-000", "confidence": 0.95}
    ))

    # Pre-populate procedural skill
    proc_id = str(uuid.uuid4())
    memory_store.put(MemoryRecord(
        id=proc_id,
        memory_type=MemoryType.PROCEDURAL,
        namespace="global",
        content="When generating HTTP code, default to requests or httpx with timeout guards.",
        salience=0.8,
        provenance={"source": "engineering_playbook_v1"}
    ))

    print(f"[*] Initialized Long-Term Store with {len(memory_store.list_all())} durable records.")

    # --- SESSION 1: THREAD A ---
    print("\n--- [Thread 1: session-alpha-101] ---")
    thread_1 = ThreadExecutionState(thread_id="thread-alpha-101", user_id="alice")
    thread_1.add_message("user", "Hello! I am setting up our data pipeline.")
    thread_1.variables["active_project"] = "DataPipeline-ETL"

    user_query = "What programming guidelines should I follow for my scripts?"

    # Context Assembly for Thread 1
    recalled = memory_store.search("user:alice", user_query, top_k=2)
    recalled_texts = [r.content for r in recalled]

    context_1 = ContextWindow(
        system_prompt="You are an autonomous engineering assistant.",
        recalled_memories=recalled_texts,
        recent_history=thread_1.messages,
        working_variables=thread_1.variables,
        user_prompt=user_query
    )

    prompt_payload = context_1.assemble()
    print("--> Context Window assembled for Turn 1:\n")
    print(prompt_payload)

    # Agent responds and records a new episodic memory
    agent_reply = "Following your preference: use concise Python with type annotations. Active project: DataPipeline-ETL."
    thread_1.add_message("assistant", agent_reply)

    # Ingest new episodic memory from Thread 1 into long-term store
    ep_id = str(uuid.uuid4())
    memory_store.put(MemoryRecord(
        id=ep_id,
        memory_type=MemoryType.EPISODIC,
        namespace="user:alice",
        content="Discussed Python type annotation standards for DataPipeline-ETL.",
        salience=0.7,
        provenance={"thread_id": thread_1.thread_id, "turn": thread_1.turn_count}
    ))
    print(f"\n[+] Persisted episodic memory from Thread 1: {ep_id}")

    # --- SESSION 1 CLOSES ---
    print("\n[!] Session 1 closed. Thread 1 State and transient Context Window discarded.")
    del thread_1
    del context_1

    # --- SESSION 2: THREAD B (Days later, new thread_id) ---
    print("\n--- [Thread 2: session-beta-202 (New Run)] ---")
    thread_2 = ThreadExecutionState(thread_id="thread-beta-202", user_id="alice")
    new_query = "Write a quick fetch script for our pipeline."

    # Recall from long-term memory across sessions
    recalled_2 = memory_store.search("user:alice", new_query, top_k=3)
    recalled_texts_2 = [r.content for r in recalled_2]

    context_2 = ContextWindow(
        system_prompt="You are an autonomous engineering assistant.",
        recalled_memories=recalled_texts_2,
        recent_history=thread_2.messages,
        working_variables=thread_2.variables,
        user_prompt=new_query
    )

    print("--> Context Window assembled for Turn 1 in new Thread 2:\n")
    print(context_2.assemble())

    # --- DEMONSTRATION OF MEMORY FORGETTING / DELETION ---
    print("\n--- [Memory Deletion / Right-to-be-Forgotten] ---")
    print(f"Records before deletion: {len(memory_store.list_all('user:alice'))}")
    deleted = memory_store.delete(pref_id)
    print(f"Deleted profile record {pref_id}: {deleted}")
    print(f"Records remaining for Alice: {len(memory_store.list_all('user:alice'))}")

    print("\n[✓] Demonstration completed successfully.")


if __name__ == "__main__":
    run_demonstration()
