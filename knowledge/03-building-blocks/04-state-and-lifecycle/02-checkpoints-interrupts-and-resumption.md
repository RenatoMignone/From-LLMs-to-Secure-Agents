<!--
---
title: Checkpoints, interrupts, and resumption
unit_id: P1-03-04-02
summary: Explains durable state checkpointing, human-in-the-loop breakpoint interrupts,
  state rehydration across infrastructure restarts, and state time-travel.
prerequisites:
- Read [Run, thread, and event models](01-run-thread-and-event-models.md).
learning_objectives:
- Implement durable checkpointing to persist agent execution state across node transitions
  and server restarts.
- Configure breakpoint interrupts to suspend active runs prior to high-privilege tool
  invocations.
- Rehydrate and resume suspended agent workflows upon receiving human approvals or
  edited parameters.
- Enable state time-travel to rewind execution to historical checkpoints and explore
  alternative branches.
source_records:
- p1-03-04-02-langgraph-human-in-the-loop-2024
- p1-03-04-02-temporal-durable-execution-2024
- p1-03-04-02-openai-agents-sdk-handoffs-2024
- p1-03-04-02-microsoft-autogen-human-input-2024
visual_assets: []
example_paths:
- examples/03-building-blocks/04-state-and-lifecycle/02-checkpoints-interrupts-and-resumption/checkpoint_interrupt_resumption.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-24'
---
-->

# Checkpoints, interrupts, and resumption

## Why this matters

In long-running autonomous workflows, execution cannot be assumed to run continuously without pause. Processes crash, container nodes get rescheduled, and high-impact actions (such as initiating financial transfers, modifying production databases, or sending external emails) require explicit human authorization before proceeding.

If an agent runtime holds all execution state in ephemeral in-memory variables, a single server reboot or network drop destroys the entire run. Furthermore, without checkpointing, an agent cannot be safely paused while waiting days for human approval. **Checkpoints, interrupts, and resumption mechanisms** provide durable execution guarantees (LangChain, 2024; Temporal Technologies, 2024; OpenAI, 2024; Microsoft, 2024). By capturing serialized state snapshots at deterministic boundaries, agents can pause indefinitely, survive infrastructure failures, and resume seamlessly when approved.

## Simple mental model

Think of playing a complex video game with manual and automatic save points:

1. **The save point (the checkpoint):** before entering a dangerous dungeon, the game saves your character inventory, location, and quest progress to disk.
2. **The confirmation dialogue (the interrupt):** when attempting to sell a rare legendary item, the game pauses action and pops up a confirmation dialogue: *"Are you sure you want to sell this item?"*
3. **Loading the save (resumption):** if your console loses power during the boss fight, you do not restart the entire game from level one; you load the latest save point and continue right from the dungeon entrance.
4. **Branching saves (time-travel):** you can reload a save file from three chapters ago to choose a different faction storyline without replaying the opening tutorial.

Durable checkpoints protect player progress from hardware crashes while providing safe decision boundaries before irreversible actions.

## Position in the agent workflow

Checkpointing sits between the runtime execution loop and persistent storage backends (such as PostgreSQL, Redis, or cloud blob stores). At every major transition (such as entering a graph node, completing a tool execution, or emitting a message), the checkpointer commits a state snapshot.

When an agent encounters a policy-designated sensitive tool, the runtime halts execution, marks the run as suspended, and commits a pending-action checkpoint. External user interfaces or notification webhooks notify human operators, who can review, edit, or approve the action out of band before triggering runtime resumption.

## How it works

Durable checkpointing and human-in-the-loop execution operate across four core mechanisms:

### 1. Checkpoint creation and serialization

A **checkpoint** is an immutable, serialized snapshot of the agent state at a specific logical step (LangChain, 2024; Temporal Technologies, 2024). Each checkpoint contains:

- **`checkpoint_id`:** A unique monotonic identifier or hash.
- **`thread_id`:** The owning conversational thread.
- **`version / step`:** The logical sequence counter.
- **`variables`:** The dictionary of application state variables, extracted facts, and accumulated artifacts.
- **`pending_action`:** Optional uncommitted action descriptor awaiting authorization.

Checkpointers serialize this data into relational or document stores, ensuring that state is durable before any side-effecting action is dispatched.

### 2. Breakpoint interrupts and human-in-the-loop gates

An **interrupt** pauses execution before or after designated graph nodes (LangChain, 2024; Microsoft, 2024). When an agent proposes an action flagged as high-risk by system policy:

1. The runtime suspends model execution.
2. The current state snapshot and the proposed tool invocation payload are written to the checkpointer.
3. The run status transitions to `REQUIRES_ACTION` or `SUSPENDED_APPROVAL`.
4. The worker thread releases compute resources and returns to the pool.

### 3. State rehydration and resumption

When the human supervisor or external webhook responds, the client issues a resume request specifying the `thread_id` and optional parameter modifications (OpenAI, 2024). The runtime:

1. Loads the latest checkpoint from the database (**rehydration**).
2. Applies any authorized parameter edits or human feedback to the working state.
3. Dispatches the approved action or transitions execution to the next workflow step.
4. Emits a resumption event and sets run status back to `IN_PROGRESS`.

### 4. Time-travel and alternative state forking

Because checkpoints are immutable historical records, runtimes can support **time-travel debugging and state forking** (LangChain, 2024). Developers or users can rewind a conversation to an earlier checkpoint, modify intermediate variables or system instructions, and spawn a new execution branch to observe how the agent behaves under alternative conditions.

## Main variants

1. **Graph-Node Checkpointing (LangGraph):** State graphs persist state deltas automatically at node boundaries using dedicated checkpointers (`MemorySaver`, `SqliteSaver`, `PostgresSaver`), supporting dynamic `interrupt_before` and `interrupt_after` hooks (LangChain, 2024).
2. **Event-Replay Durable Execution (Temporal):** Workflows achieve durability by replaying deterministic event histories against code definitions upon worker recovery (Temporal Technologies, 2024).
3. **Hosted Approval Loops (OpenAI Agents SDK):** Hosted threads track tool call approvals through server-side run objects, pausing on required actions until client tool outputs or approvals are posted (OpenAI, 2024).
4. **Interactive Human-in-the-Loop (AutoGen):** Multi-agent orchestrators support configurable human input modes (`ALWAYS`, `TERMINATE`, `NEVER`) allowing operators to inject natural language steering turns (Microsoft, 2024).

## Minimal implementation

The following Python snippet demonstrates durable checkpoint creation, sensitive tool interrupts, and human approval resumption. The [full runnable example](../../../examples/03-building-blocks/04-state-and-lifecycle/02-checkpoints-interrupts-and-resumption/checkpoint_interrupt_resumption.py) demonstrates pre-flight checks, pending action suspension, parameter modification, and execution finalization.

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

class RunState(Enum):
    RUNNING = auto()
    SUSPENDED_APPROVAL = auto()
    COMPLETED = auto()

@dataclass
class Checkpoint:
    checkpoint_id: str
    thread_id: str
    step: int
    variables: Dict[str, Any]
    pending_action: Optional[Dict[str, Any]] = None

class DurableRuntime:
    def __init__(self, sensitive_tools: set[str]):
        self.sensitive_tools = sensitive_tools
        self.checkpoints: Dict[str, List[Checkpoint]] = {}

    def execute_step(self, thread_id: str, tool_name: str, args: Dict[str, Any]) -> Tuple[RunState, Checkpoint]:
        # If tool is sensitive, pause execution and save pending action checkpoint
        if tool_name in self.sensitive_tools:
            cp = Checkpoint("cp_002", thread_id, 2, {"log": ["Pre-flight complete"]}, pending_action={"tool": tool_name, "args": args})
            return RunState.SUSPENDED_APPROVAL, cp

        # Regular safe step
        cp = Checkpoint("cp_001", thread_id, 1, {"log": [f"Executed {tool_name}"]})
        return RunState.RUNNING, cp

    def resume_approval(self, thread_id: str, approved: bool, edited_args: Optional[Dict[str, Any]] = None) -> Tuple[RunState, Checkpoint]:
        cp = Checkpoint("cp_003", thread_id, 3, {"log": ["Action approved and executed"], "status": "APPROVED"})
        return RunState.COMPLETED, cp
```

</details>

Run [checkpoint_interrupt_resumption.py](../../../examples/03-building-blocks/04-state-and-lifecycle/02-checkpoints-interrupts-and-resumption/checkpoint_interrupt_resumption.py) to inspect the complete checkpoint timeline, pending action capture, and supervisor approval flow.

## Data flow and state changes

1. **Step execution:** The agent executes steps, creating sequential checkpoints `cp_001`, `cp_002`.
2. **Interrupt evaluation:** When reaching a guarded tool call, the runtime intercepts the invocation.
3. **Suspension commit:** The runtime serializes current state, attaches the proposed tool payload as `pending_action`, and transitions status to `SUSPENDED_APPROVAL`.
4. **Notification:** An external event or UI webhook alerts the human operator with the proposed action diff.
5. **Supervisor intervention:** The operator approves, rejects, or modifies the action arguments.
6. **Rehydration and dispatch:** The runtime reloads `pending_action`, injects any modified arguments, executes the tool, commits checkpoint `cp_003`, and resumes execution.

## Trust boundaries

- **Checkpoint storage security:** State checkpoints contain raw conversational history, retrieved context, and working credentials. Checkpointer databases must be encrypted at rest and enforce tenant access control.
- **Supervisor identity validation:** Human approval requests must authenticate the approving user identity and verify that their role possesses sufficient authorization to approve the target action.
- **State modification sanitization:** When a human or supervisor edits state variables before resumption, the edited payload must undergo schema validation to prevent invalid state corruption.

## Reliability failures

- **Approval timeouts and abandonment:** If a human reviewer never responds to a suspended run, resources and locks remain tied up unless automated expiration policies cancel the run.
- **Checkpoint serialization mismatch:** Storing unpicklable Python objects (such as open socket descriptors, thread locks, or database connections) in state causes serialization crashes; only pure serializable data must enter checkpoints.
- **Non-deterministic replay divergence:** In event-replay architectures, if external dependencies change during replay, the reconstructed state will diverge from the recorded execution history.

## Limitations and trade-offs

- **Write amplification and latency:** Writing full state snapshots to disk at every step introduces database write latency, necessitating incremental state delta encoding for high-throughput systems.
- **State schema migrations:** Updating agent code or state models can break the ability to rehydrate checkpoints created under older software versions.
- **Complexity of concurrent edits:** If two supervisors attempt to edit and resume the same suspended checkpoint simultaneously, optimistic locking is required to prevent state collisions.

## Security preview

In Pass 2, checkpoint and resumption architectures are evaluated against **Checkpoint Tampering, Replay Attacks, and Privilege Escalation via State Injection**. Attackers attempt to modify serialized checkpoint records in storage to bypass approval gates or inject forged authorizations into pending runs. We examine cryptographic checkpoint hashing, tamper-evident audit logs, and hardware-backed approval signatures in [Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open research questions

- How can distributed checkpointers achieve zero-overhead state persistence using copy-on-write memory snapshots without blocking real-time token generation?
- What formal verification techniques can guarantee that an interrupted agent workflow will never enter an invalid state regardless of how long it remains paused?

## Key takeaways

- Checkpoints capture immutable serialized state snapshots, enabling agents to survive server reboots and support multi-day workflows.
- Breakpoint interrupts safely pause execution prior to high-privilege tool invocations, creating deterministic approval boundaries.
- Resumption rehydrates state from persistent checkpointers, allowing human operators to review, edit, or reject actions before execution.
- Checkpoint timelines enable state time-travel for debugging, auditability, and exploring alternative reasoning branches.

## References

- LangChain Community. *Human-in-the-Loop and Checkpointing in LangGraph*. LangGraph Documentation, 2024. [LangGraph HITL](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop).
- Temporal Technologies. *Durable Execution, Checkpoints, and Deterministic Replay*. Temporal Documentation, 2024. [Temporal State](https://docs.temporal.io/workflow-execution-and-state).
- OpenAI. *Agent Checkpoints, State Resumption, and Human Approvals*. OpenAI Agents SDK Documentation, 2024. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/running_agents/).
- Microsoft Research. *AutoGen: Human-in-the-Loop Interaction Modes and State Resumption*. AutoGen Documentation, 2024. [AutoGen HITL](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html).

---

[Next Unit: Retries, idempotency, and concurrency →](chapter-plan.md)
