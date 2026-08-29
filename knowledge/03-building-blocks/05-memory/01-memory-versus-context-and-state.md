<!--
---
title: Memory versus context and state
unit_id: P1-03-05-01
summary: Explains the fundamental distinctions between ephemeral context windows,
  mutable execution state, and durable multi-tier memory systems across agent sessions.
prerequisites:
- Read [State and lifecycle](../04-state-and-lifecycle/chapter-plan.md).
learning_objectives:
- Distinguish between transient Context Windows, session-scoped Execution State, and
  cross-thread Persistent Memory.
- Classify agent memory into working, episodic, semantic, and procedural memory tiers.
- Understand the core memory lifecycle across ingestion, storage, selective recall,
  reflection, and forgetting.
- Evaluate the trade-offs between context window pressure, retrieval noise, memory
  staleness, and storage overhead.
source_records:
- p1-03-05-01-packer-memgpt-2023
- p1-03-05-01-park-generative-agents-2023
- p1-03-05-01-langgraph-store-memory-2024
- p1-03-05-01-microsoft-autogen-memory-2024
visual_assets: []
example_paths:
- examples/03-building-blocks/05-memory/01-memory-versus-context-and-state/memory_context_state_runtime.py
pass: architecture
learning_path: main
status: review
last_reviewed: '2026-08-24'
---
-->

# Memory versus context and state

## Why this matters

When humans collaborate with an assistant over multiple weeks or projects, they expect the assistant to remember key facts, user preferences, and past decisions. If an agent treats every conversation as an isolated blank slate, the user must repeatedly explain their preferred coding style, project constraints, and organizational context.

In production AI systems, developers frequently conflate three distinct mechanisms: the **context window**, the **execution state**, and **long-term memory** (Packer et al., 2023; LangChain, 2024; Microsoft, 2024). Treating these mechanisms as interchangeable leads to fragile architectures. Relying solely on the context window causes prompt bloat, high latency, and catastrophic forgetting when conversation histories exceed token limits. Conversely, relying only on session state discards critical learnings the moment an execution run completes.

Building capable autonomous agents requires an explicit memory subsystem that operates alongside execution state (covered in [State and lifecycle](../04-state-and-lifecycle/chapter-plan.md)) and external retrieval (covered in [Retrieval and RAG](../06-retrieval-and-rag/chapter-plan.md)). By establishing clear boundaries between what is held in active memory, what is tracked in session state, and what is persisted for cross-session recall, developers can create agents that learn continuously without exceeding token budgets or leaking confidential data.

## Simple mental model

Think of an architect working in a busy studio:

1. **The desk workspace (the context window):** The physical surface where blueprints and active documents are laid out. The desk has a fixed physical size. When new documents arrive, older papers must be moved aside to make room. Once the architect finishes a specific calculation, the desk is cleared.
2. **The active project notepad (the execution state):** The notebook tracking the current job. It records which contractor has been called today, what measurements are pending, and which step comes next. When the active project concludes, this notepad is closed and archived.
3. **The firm library and client archive (long-term memory):** A permanent records room containing client preference files ("Client A dislikes glass facades"), historical project post-mortems ("Building C required foundation reinforcement"), and standard engineering handbooks. The architect queries this archive only when relevant facts are needed.

Confusing the desk (context window) with the notebook (execution state) or the library (long-term memory) leads to clutter, lost notes, or impossible storage demands.

## Position in the agent workflow

The memory subsystem bridges the gap between active model execution and long-term knowledge retention. During a live execution run, the planner and tool execution engine mutate the short-term execution state. Concurrently, the memory manager extracts salient facts, user preferences, and execution reflections from the event stream and persists them into long-term storage.

When a new user request or thread begins, the memory manager performs selective recall. It queries the persistent store for relevant facts and user profile entries, formatting the top results into the prompt context alongside current instructions.

## How it works

Modern agent architectures structure information retention across three core dimensions: architectural scope, cognitive taxonomy, and lifecycle phases.

### 1. The Triad: Context window, execution state, and memory

| Dimension | Context Window | Execution State | Long-Term Memory |
| :--- | :--- | :--- | :--- |
| **Primary role** | Input buffer for a single model inference forward pass | Working variables and event history of the active run | Persistent knowledge store across runs and sessions |
| **Scope** | Single prompt invocation | Single thread or active run session | Cross-thread, user-scoped, or organization-scoped |
| **Storage medium** | GPU / Model attention buffer | Key-value checkpointer or relational database | Vector database, document store, or graph index |
| **Lifecycle** | Ephemeral (cleared after generation) | Active during run / thread lifetime | Durable (persists across days, weeks, or years) |
| **Access pattern** | Full sequential attention | Direct dictionary lookup or event reducer | Semantic vector search, keyword filter, or hybrid recall |
| **Capacity bound** | Strict model context limit (e.g., 128k tokens) | Session memory limit | Unbounded external storage |

### 2. The cognitive memory taxonomy

Drawing inspiration from cognitive science and operating system architecture (Packer et al., 2023; Park et al., 2023), agent memory is organized into four distinct tiers:

- **Working memory (in-context scratchpad):** The active scratchpad holding immediate subgoals, recent tool observation outputs, and reasoning chains for the current step.
- **Episodic memory (autobiographical log):** A time-ordered sequence of past interactions, events, and task executions (Park et al., 2023). For example: "On Monday, the user asked to refactor the database connector to use asyncpg."
- **Semantic memory (facts and concepts):** Distilled, non-temporal facts, user profiles, and domain rules extracted from past experiences (LangChain, 2024). For example: "User Alice prefers type-annotated Python code" or "Production database uses port 5432."
- **Procedural memory (skills and playbooks):** Reusable instructions, tool calling patterns, and operational scripts that define how the agent performs multi-step workflows.

### 3. Memory record structure

Every durable memory entry is stored as a structured record with explicit governance metadata:

- **Memory ID:** Unique identifier for retrieval and targeted deletion.
- **Namespace / Scope:** Hierarchical isolation key (e.g., `user:alice`, `team:backend`, or `global`).
- **Memory Type:** Classification (`episodic`, `semantic`, or `procedural`).
- **Content:** The textual representation or structured payload of the remembered knowledge.
- **Salience Score ($S \in [0, 1]$):** Computed importance indicating whether the information warrants long-term retention (Park et al., 2023).
- **Recency and Timestamps:** Creation timestamp ($t_c$) and last-accessed timestamp ($t_a$) used for decay scoring.
- **Time-to-Live (TTL):** Optional expiration timestamp for temporary working memory or session tokens.
- **Provenance:** Cryptographic source tracking, including originating `thread_id`, `run_id`, and extractor confidence score.

### 4. The five-stage memory lifecycle

Memory management operates through a continuous five-stage pipeline (Packer et al., 2023; Park et al., 2023):

1. **Extraction and ingestion:** As dialogue and tool execution events stream in, an extraction agent or parser identifies salient facts, user preferences, and task results.
2. **Storage and indexing:** Extracted memories are tagged with namespace metadata, embedded into vector representations, and committed to durable storage.
3. **Selective recall:** When a new prompt arrives, a retrieval query identifies the most relevant memories using a scoring function combining semantic similarity, salience, and recency:

$$\text{Score}(m, q) = \alpha \cdot \text{Sim}(m, q) + \beta \cdot \text{Salience}(m) + \gamma \cdot \text{Recency}(m)$$

4. **Consolidation and reflection:** Background processes periodically synthesize raw episodic traces into generalized semantic facts and higher-level user insights (Park et al., 2023).
5. **Forgetting and pruning:** Stale records undergo time-decay pruning, expired TTL items are evicted, and explicit user deletion requests are executed.

## Main variants

1. **Operating system style tiered paging (MemGPT):** Models LLM memory like computer operating systems, dividing storage into fast main memory (in-context virtual context) and deep external disk storage (vector/relational database) managed via explicit paging functions (Packer et al., 2023).
2. **Generative memory streams and reflection:** Maintains an append-only autobiographical stream of natural language observations, periodically pausing to generate recursive reflections and hierarchical insight trees (Park et al., 2023).
3. **Namespaced cross-thread stores:** Frameworks like LangGraph Store and Microsoft AutoGen provide hierarchical key-value and semantic namespaces (`/users/{user_id}/preferences`), separating thread state from cross-session user memory (LangChain, 2024; Microsoft, 2024).

## Minimal implementation

The following Python snippet demonstrates the core distinction between session execution state and cross-thread persistent memory with selective recall and record deletion. The [full runnable example](../../../examples/03-building-blocks/05-memory/01-memory-versus-context-and-state/memory_context_state_runtime.py) demonstrates multi-turn context assembly and cross-session memory retrieval.

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid
from typing import Any, Dict, List, Optional

class MemoryType(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

@dataclass
class MemoryRecord:
    id: str
    memory_type: MemoryType
    namespace: str
    content: str
    salience: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class PersistentMemoryStore:
    def __init__(self) -> None:
        self._records: Dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.id] = record

    def recall(self, namespace: str, query_tokens: set[str], top_k: int = 2) -> List[MemoryRecord]:
        matches = [r for r in self._records.values() if r.namespace == namespace]
        # Rank by token overlap and salience score
        matches.sort(
            key=lambda r: (len(query_tokens.intersection(set(r.content.lower().split()))), r.salience),
            reverse=True
        )
        return matches[:top_k]

    def delete(self, memory_id: str) -> bool:
        return self._records.pop(memory_id, None) is not None
```

</details>

Run [memory_context_state_runtime.py](../../../examples/03-building-blocks/05-memory/01-memory-versus-context-and-state/memory_context_state_runtime.py) to inspect cross-session memory preservation, context assembly, and record deletion.

## Data flow and state changes

1. **Interaction capture:** User message and assistant response are recorded in the active thread execution state.
2. **Fact extraction:** The memory extractor detects persistent preferences (e.g., "User prefers dark mode and type hints").
3. **Persistent write:** A structured `MemoryRecord` is saved to the persistent store under `user:alice`.
4. **Thread termination:** The active run completes; the context window and thread runtime are deallocated.
5. **New session initialization:** A new thread starts for `user:alice`.
6. **Memory recall:** The agent queries `user:alice` memories matching the new prompt, injecting the retrieved facts into the initial context window.
7. **Pruning or deletion:** Expired memories or user-requested removals are pruned from storage.

## Trust boundaries

- **Tenant and user namespace isolation:** Memory stores must enforce strict access boundaries. An agent acting on behalf of User A must never retrieve memory records partitioned under User B.
- **Untrusted data ingestion boundary:** Data received from external tools, web search results, or third-party webhooks must not be automatically written to semantic memory without sanitization.
- **Memory deletion and right-to-be-forgotten:** Users must possess the authority to inspect, correct, and delete stored memories in compliance with data privacy regulations.

## Reliability failures

- **Context distraction from irrelevant recall:** Injecting low-relevance memories into the context window consumes token budget and distracts model attention from the user immediate goal.
- **Hallucinated reflection consolidation:** If an agent reflects on a flawed execution episode, it can consolidate false assumptions into permanent semantic memory, compounding errors in future runs.
- **Memory staleness and contradiction:** If a user changes preferences ("I switched from JavaScript to Rust"), the memory store may retain conflicting records unless update policies explicitly invalidate outdated facts.

## Limitations and trade-offs

- **Retrieval latency vs. context size:** Dynamic memory recall requires vector index queries before prompt generation, adding latency compared to purely in-memory session state.
- **Extraction cost overhead:** Running dedicated extraction or reflection models after every conversation turn incurs token and compute expenses.
- **Indexing complexity:** As memory stores scale to millions of records, maintaining fast hybrid search (combining vector distance, keyword filters, and time decay) requires specialized database infrastructure.

## Security preview

In Pass 2, memory systems are evaluated against **Memory Poisoning, Indirect Prompt Injection Retention, and Cross-Tenant Memory Leakage**. Attackers attempt to trick agents into storing malicious instructions in persistent semantic memory, turning transient prompt injections into permanent backdoors. We explore cryptographically verified memory provenance, taint tracking, and sanitization gates in [Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md).

## Open research questions

- How can autonomous agents detect and resolve logical contradictions between newly observed facts and historical memories without human intervention?
- What formal mathematical decay functions best balance long-term concept retention with the automatic forgetting of obsolete details?

## Key takeaways

- The context window is ephemeral, execution state is session-scoped, and long-term memory is persistent across threads.
- Cognitive agent memory is organized into working, episodic, semantic, and procedural tiers.
- Memory management follows an end-to-end lifecycle of extraction, indexing, selective recall, reflection, and pruning.
- Production memory architectures require strict tenant namespace isolation, provenance tracking, and explicit deletion policies.

## References

- Packer, C., Fang, V., Patil, S. G., Lin, K., Wooders, S., & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv preprint arXiv:2310.08560. [MemGPT Paper](https://arxiv.org/abs/2310.08560).
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23), pp. 1-22. [DOI: 10.1145/3586183.3606763](https://doi.org/10.1145/3586183.3606763).
- LangChain Community. (2024). *LangGraph: Memory and Key-Value Store Across Threads*. LangGraph Documentation. [LangGraph Memory](https://langchain-ai.github.io/langgraph/concepts/memory/).
- Microsoft Research. (2024). *AutoGen: Agent Memory and Context Management*. AutoGen Documentation. [AutoGen Memory](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html).

---

[Next Unit: Short-term and working memory →](chapter-plan.md)
