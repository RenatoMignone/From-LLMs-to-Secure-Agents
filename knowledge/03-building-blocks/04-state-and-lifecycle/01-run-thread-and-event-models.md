<!--
---
title: Run, thread, and event models
unit_id: P1-03-04-01
summary: Explains the fundamental execution hierarchy of threads, runs, turns, and
  event streams, contrasting snapshot state accumulation with event-sourced agent
  architectures.
prerequisites:
- Read [Planning and reasoning](../03-planning-and-reasoning/chapter-plan.md).
learning_objectives:
- Differentiate between long-lived conversational Threads, active execution Runs,
  and granular conversational Turns.
- Model agent execution as a stream of immutable, structured Events following event-sourcing
  principles.
- Implement a state reducer that projects discrete event streams into coherent working
  state snapshots.
- Track the lifecycle state transitions of an active Run across QUEUED, IN_PROGRESS,
  REQUIRES_ACTION, and COMPLETED states.
source_records:
- p1-03-04-01-openai-agents-sdk-runs-2024
- p1-03-04-01-langgraph-server-threads-2024
- p1-03-04-01-microsoft-autogen-state-2024
- p1-03-04-01-cloudevents-specification-1-0
visual_assets: []
example_paths:
- examples/03-building-blocks/04-state-and-lifecycle/01-run-thread-and-event-models/thread_run_event_runtime.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-24'
---
-->

# Run, thread, and event models

## Why this matters

When an autonomous agent interacts with users, tools, and external services over hours or days, it needs a reliable way to organize its ongoing work. If a system models every interaction as an isolated, stateless function call, it cannot maintain context across successive user prompts, pause execution while waiting for human authorization, or recover gracefully from server crashes.

To build durable, auditable systems, modern agent architectures structure execution into distinct structural layers (OpenAI, 2024; LangChain, 2024; Microsoft, 2024; CNCF, 2024). **Run, thread, and event models** provide the foundational abstractions for managing state and lifecycle. By distinguishing between long-lived conversation containers (threads), active execution instances (runs), and atomic state mutations (events), developers can build agents that support multi-turn workflows, asynchronous tool execution, and comprehensive auditability.

## Simple mental model

Think of a patient receiving medical care at a hospital:

1. **The medical chart (the thread):** a permanent folder containing the complete patient history, test results, and past doctor consultations across all visits.
2. **The clinic appointment (the run):** a specific active session where a physician examines the patient, orders laboratory tests, and prescribes treatments.
3. **The dialogue exchange (the turn):** the question asked by the patient and the direct answer provided by the doctor.
4. **The timestamped log entry (the event):** discrete, immutable records added to the chart, such as "Vital signs recorded at 09:15", "Blood panel ordered at 09:20", and "Prescription issued at 09:30".

Separating the long-lived record (thread) from the active consultation (run) and atomic actions (events) ensures that multiple specialists can collaborate safely without losing past context.

## Position in the agent workflow

The state and lifecycle subsystem sits directly beneath planning, reasoning, and tool execution. While the planner decides what tasks to perform, the state subsystem tracks where the agent is in its overall lifecycle, what variables have been produced, and which events have transpired.

When an external request arrives, the runtime assigns it to a thread, instantiates a new run, and streams state transitions as structured events. This enables user interfaces to render real-time progress, supervisors to pause execution at authorization boundaries, and databases to store durable snapshots.

## How it works

The execution hierarchy operates across four distinct structural levels:

### 1. The execution hierarchy (Thread, Run, Turn, Event)

- **Thread:** The top-level persistent container identified by a unique `thread_id` (OpenAI, 2024; LangChain, 2024). A thread encapsulates the cumulative conversation history, working variables, and domain context for a long-lived user session or project.
- **Run:** An active invocation of the agent within a thread, identified by a `run_id`. A run executes a specific objective, coordinating model calls and tool dispatches until a terminal state is reached.
- **Turn:** A single request-response exchange within a run, typically initiated by a user message and concluded by an assistant answer.
- **Event:** An atomic, immutable record of an occurrence within a run, such as `user.message`, `tool.call.requested`, `tool.result.received`, or `run.state.changed` (CNCF, 2024).

### 2. Event sourcing versus snapshot state accumulation

Runtimes generally track state using one of two models:

1. **State snapshot model:** The runtime stores the current state object (such as a dictionary of variables and a list of messages) and overwrites it after each step. While simple to implement, this approach loses the granular history of intermediate decisions.
2. **Event sourcing model:** The runtime treats the append-only event stream as the single source of truth (CNCF, 2024). The current working state is computed dynamically by a **state reducer** function that folds successive events into an accumulated snapshot:

$$	ext{State}_{t} = 	ext{Reduce}(	ext{State}_{t-1}, 	ext{Event}_t)$$

Event sourcing provides complete auditability, simplified time-travel debugging, and reproducible state reconstruction.

### 3. The run lifecycle state machine

Every active run moves through a standardized lifecycle (OpenAI, 2024):

- **`QUEUED`:** The run is created and waiting in the thread execution queue.
- **`IN_PROGRESS`:** The model is actively inferring thoughts, generating text, or assembling tool arguments.
- **`REQUIRES_ACTION`:** The run is paused awaiting an external event, such as a tool execution response from a sandbox or approval from a human supervisor.
- **`COMPLETED`:** The run has successfully satisfied the user prompt and finalized all state changes.
- **`FAILED / CANCELLED`:** The run terminated abnormally due to an unhandled exception, timeout, or explicit user cancellation.

## Main variants

1. **Serverless Hosted Threads:** Managed platforms (such as the OpenAI Agents SDK and Assistants API) store thread messages and run status remotely, exposing polling or streaming endpoints (OpenAI, 2024).
2. **Graph-Based Checkpointed State:** Frameworks like LangGraph represent state as typed schemas associated with `thread_id` keys, persisting state deltas to relational databases or Redis checkpointers after every node transition (LangChain, 2024).
3. **Multi-Agent Message Buses:** Systems like AutoGen model conversation state as shared append-only message logs distributed among participating worker agents (Microsoft, 2024).

## Minimal implementation

The following Python snippet demonstrates the core execution hierarchy, event emission, and state reducer logic. The [full runnable example](../../../examples/03-building-blocks/04-state-and-lifecycle/01-run-thread-and-event-models/thread_run_event_runtime.py) demonstrates multi-turn event streaming, tool dispatch, and state reduction.

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List

class EventType(Enum):
    USER_MESSAGE = "user.message"
    TOOL_COMPLETED = "tool.completed"
    AGENT_MESSAGE = "agent.message"

@dataclass
class Event:
    event_id: str
    event_type: EventType
    thread_id: str
    run_id: str
    payload: Dict[str, Any]

@dataclass
class ThreadState:
    thread_id: str
    variables: Dict[str, Any] = field(default_factory=dict)
    messages: List[Dict[str, str]] = field(default_factory=list)
    version: int = 0

    def apply_event(self, event: Event) -> None:
        self.version += 1
        if event.event_type == EventType.USER_MESSAGE:
            self.messages.append({"role": "user", "content": event.payload.get("content", "")})
        elif event.event_type == EventType.AGENT_MESSAGE:
            self.messages.append({"role": "assistant", "content": event.payload.get("content", "")})
        elif event.event_type == EventType.TOOL_COMPLETED:
            key = event.payload.get("store_as")
            if key:
                self.variables[key] = event.payload.get("result")
```

</details>

Run [thread_run_event_runtime.py](../../../examples/03-building-blocks/04-state-and-lifecycle/01-run-thread-and-event-models/thread_run_event_runtime.py) to inspect the complete runtime trace, event log emission, and state reduction.

## Data flow and state changes

1. **Thread initialization:** The client establishes or retrieves a `thread_id`.
2. **Run dispatch:** A user prompt triggers a new `Run` assigned to the thread.
3. **Event emission:** The runtime emits `user.message` and sets run status to `IN_PROGRESS`.
4. **Action suspension:** If a tool is required, the run emits `tool.call.requested` and transitions to `REQUIRES_ACTION`.
5. **Observation injection:** The tool result is emitted as `tool.execution.completed`, updating thread working variables via the state reducer.
6. **Finalization:** The model emits `agent.message`, and the run transitions to `COMPLETED`.

## Trust boundaries

- **Client to thread boundary:** Thread IDs must be authenticated and authorized. An unauthenticated client must not be allowed to inspect or inject messages into another tenant thread.
- **Run parameter injection:** Parameters passed during run creation (such as temperature, model overrides, or tool permissions) must be validated against system security policies before execution begins.
- **Event stream integrity:** Event logs must be append-only and cryptographically auditable to prevent tampering with historical execution traces.

## Reliability failures

- **Thread context bloat:** Unbounded accumulation of turns within a thread exhausts token limits, requiring proactive summarization or context truncation.
- **Dangling runs:** A run paused in `REQUIRES_ACTION` can remain stuck indefinitely if an external webhook or human approver never responds, necessitating automated timeouts.
- **State desynchronization:** In distributed deployments, concurrent runs modifying the same thread without optimistic concurrency controls can overwrite each other state variables.

## Limitations and trade-offs

- **Storage overhead:** Storing full event logs for millions of long-lived threads requires scalable event storage infrastructure.
- **Reducer latency:** Replaying lengthy event histories to reconstruct state snapshots can introduce cold-start latency unless intermediate checkpoints are cached.
- **Schema evolution:** As agent code evolves, past event schemas must remain backward-compatible with newer state reducer versions.

## Security preview

In Pass 2, thread and event architectures are evaluated against **Thread Hijacking, State Variable Tampering, and Cross-Tenant State Leakage**. Attackers attempt to forge thread identifiers, inject malicious state deltas, or exploit unauthenticated event streams to gain unauthorized access. We analyze cryptographically signed state tokens, tenant-isolated checkpointers, and invariant assertion gates in [Instructions, context, and model security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open research questions

- How can distributed agent runtimes achieve exactly-once event processing guarantees across unreliable network partitions without blocking real-time user streaming?
- What standardized event schemas can enable seamless thread interoperability across heterogeneous frameworks (such as LangGraph, AutoGen, and the OpenAI Agents SDK)?

## Key takeaways

- Agent execution is structured hierarchically across persistent Threads, active Runs, conversational Turns, and atomic Events.
- Event sourcing provides complete auditability and replayability by treating the append-only event log as the source of truth.
- Run state machines explicitly track execution across `QUEUED`, `IN_PROGRESS`, `REQUIRES_ACTION`, and `COMPLETED` phases.
- Robust state management requires authenticated thread boundaries, timeout guards on suspended runs, and optimistic concurrency controls.

## References

- OpenAI. *Running Agents: Threads, Runs, and Turn Lifecycle*. OpenAI Agents SDK Documentation, 2024. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/running_agents/).
- LangChain Community. *LangGraph Server: Threads, Runs, and Event Streaming*. LangGraph Documentation, 2024. [LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/).
- Microsoft Research. *AutoGen: Managing Conversation State and Event Streams*. AutoGen Documentation, 2024. [AutoGen State](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html).
- CNCF Serverless Working Group. *CloudEvents Specification 1.0.2*. Cloud Native Computing Foundation, 2024. [CloudEvents Spec](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md).

---

[Next Unit: Checkpoints, interrupts, and resumption →](chapter-plan.md)
