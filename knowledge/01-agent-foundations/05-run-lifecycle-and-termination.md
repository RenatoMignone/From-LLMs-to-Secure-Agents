<!--
---
title: Run lifecycle and termination
unit_id: P1-01-05
summary: Defines the complete lifecycle of an agent run from initialization to termination,
  detailing execution states, pause mechanisms, and multi-layered stopping conditions.
prerequisites:
- Read [What is an agent](01-what-is-an-agent.md).
- Read [The agent loop](02-the-agent-loop.md).
- Read [Workflows versus agents](03-workflows-versus-agents.md).
- Read [Goals, policies, environments, and autonomy](04-goals-policies-environments-and-autonomy.md).
learning_objectives:
- Map the state transitions of an agent run across initialization, execution, suspension,
  and termination.
- Implement layered stopping criteria including step limits, token budgets, and stuck-loop
  detection.
- Manage asynchronous pauses, human-in-the-loop approvals, and clean resource teardown.
source_records:
- p1-01-05-openai-agents-sdk-lifecycle-2024
- p1-01-05-langchain-human-in-the-loop-2024
- p1-01-05-stop-hand-holding-agents-2026
visual_assets:
- assets/images/01-agent-foundations/05-run-lifecycle-and-termination/01-run-lifecycle-and-termination.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-15'
---
-->

# Run lifecycle and termination

## Why this matters

An agent that cannot reliably stop is a severe operational hazard. Left without strict termination criteria, autonomous loops can burn through thousands of dollars in API credits, hammer third-party servers with duplicate requests, or corrupt data by thrashing repeatedly across failing steps.

Conversely, an agent that terminates too aggressively will abandon complex multi-step tasks at the first sign of friction. Managing the complete lifecycle of an agent run, from context initialization and active turns to pause states, timeout handling, and graceful termination, is a foundational requirement for production reliability, cost containment, and system safety.

## Simple mental model

Think of a commercial aircraft flight from takeoff to landing.

1. **Pre-flight (Initialization)**: The flight plan is loaded, fuel is checked, and permissions are verified.
2. **In-flight (Active Execution)**: The autopilot navigates towards the destination, making minor course adjustments.
3. **Holding Pattern (Paused / Suspended)**: Air traffic control holds the plane while waiting for runway clearance (human-in-the-loop approval).
4. **Touchdown (Goal Completion)**: The aircraft lands safely at the intended destination.
5. **Diverted / Emergency Landing (Aborted / Budget Terminated)**: If severe weather closes the airport or fuel reaches reserve levels, the aircraft diverts to an alternate airport rather than flying until it runs out of fuel.

In AI engineering, the host runtime acts as air traffic control, monitoring fuel (token budgets) and enforcing safe landing protocols (termination conditions).

## Position in the agent workflow

Use this state flowchart to trace how an agent run transitions across initialization, active execution, pause states, and termination outcomes.

![A cartoon state-machine flowchart illustrating an agent run lifecycle: Top shows Created & Initialized, Center shows Running (Active Loop) connected bi-directionally to Paused / Suspended (waiting for human approval), branching at the bottom to Succeeded (green checkmark), Aborted (amber stopwatch budget meter), and Failed (soft red error).](../../assets/images/01-agent-foundations/05-run-lifecycle-and-termination/01-run-lifecycle-and-termination.png)

*Figure 1. Complete agent run lifecycle and state transitions. Active runs execute perception-action turns, pause for external human approval or webhooks, and resolve cleanly into succeeded, aborted (budget/policy stop), or failed states.*

Trace how execution moves through each state:
1. **Created & Initialized**: The host binds credentials, prepares prompt context, and registers tool schemas.
2. **Running (Active Loop)**: The agent executes iterative perception-reasoning-action turns.
3. **Paused / Suspended**: Execution halts safely while awaiting human approval, rate limit backoff, or asynchronous webhooks.
4. **Succeeded**: The goal is achieved and confirmed by the model or verifier.
5. **Aborted / Failed**: Execution stops deterministically when step budgets or safety invariants are breached.

This completes the foundational concepts introduced in [What is an agent](01-what-is-an-agent.md), [The agent loop](02-the-agent-loop.md), [Workflows versus agents](03-workflows-versus-agents.md), and [Goals, policies, environments, and autonomy](04-goals-policies-environments-and-autonomy.md), establishing the operational baseline for advanced patterns in [Agent Architectures](../02-agent-architectures/chapter-plan.md).

## How it works

### Lifecycle execution states

An agent run progresses through six discrete states:

1. **Created**: The host instantiates the run record, binds user credentials, and allocates an isolated execution session.
2. **Initialized**: System prompt, tool schemas, goal text, and initial environment state are assembled into working memory.
3. **Running (Active)**: The agent executes iterative perception-reasoning-action turns.
4. **Paused (Suspended)**: Execution halts cleanly while awaiting human approval, an asynchronous external webhook, or exponential backoff during rate limits. State is serialized to a persistent checkpointer.
5. **Succeeded (Completed)**: The model signals that the goal is achieved, or an external verifier validates the desired end-state.
6. **Terminated (Aborted/Failed)**: The run exits due to an exhausted budget, policy violation, stuck loop detection, unrecoverable tool crash, or manual operator cancellation.

### Multi-layered termination conditions

Production systems must enforce four independent layers of termination checks on every single turn:

| Termination Layer | Trigger Mechanism | Action Taken | Rationale |
| --- | --- | --- | --- |
| **Model Completion** | Model emits `FINAL_ANSWER` or calls `finish_task()` | Return result to user, mark run Succeeded | Normal successful task resolution |
| **Resource Budget** | Turn count > $N$, tokens > $T$, wall-clock time > $S$, or cost > $\$D$ | Force-halt loop, mark run Aborted | Prevents runaway costs and infinite loops |
| **Policy Invariant** | Model requests forbidden tool, unauthorized path, or repeated error | Cancel execution, raise security alert | Enforces trust boundaries and safety rules |
| **External Interrupt** | Operator clicks cancel, webhook timeout, SIGTERM signal | Save checkpoint, clean up resources | Allows human operators to intervene immediately |

## Main variants

- **Synchronous In-Memory Lifecycle**: The run executes within a single application process thread from start to finish. Simple, but cannot survive process restarts during long pauses.
- **Durable Checkpointed Lifecycle**: The host serializes the full run state to a database after every turn. If the host crashes or pauses for human approval for hours, the run resumes seamlessly from the exact state.
- **Hierarchical Subagent Lifecycles**: A parent agent spawns child agent runs. The child lifecycle is bound to the parent; if the parent aborts, all child lifecycles terminate immediately.

## Minimal implementation

The following Python program implements a complete agent run lifecycle with durable states, token budgeting, turn caps, and clean resource disposal:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Any, Dict, List, Optional

class RunStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    SUCCEEDED = "succeeded"
    ABORTED = "aborted"
    FAILED = "failed"

@dataclass
class RunBudget:
    max_turns: int = 5
    max_tokens: int = 10000
    timeout_seconds: float = 30.0

@dataclass
class RunState:
    run_id: str
    status: RunStatus = RunStatus.CREATED
    current_turn: int = 0
    tokens_used: int = 0
    start_time: float = field(default_factory=time.time)
    termination_reason: Optional[str] = None
    history: List[Dict[str, str]] = field(default_factory=list)

class ManagedAgentRuntime:
    def __init__(self, budget: RunBudget):
        self.budget = budget

    def _check_budget(self, state: RunState) -> Optional[str]:
        if state.current_turn >= self.budget.max_turns:
            return f"Exceeded maximum turn budget ({self.budget.max_turns} turns)."
        if state.tokens_used >= self.budget.max_tokens:
            return f"Exceeded token budget ({self.budget.max_tokens} tokens)."
        if (time.time() - state.start_time) >= self.budget.timeout_seconds:
            return f"Exceeded wall-clock timeout ({self.budget.timeout_seconds}s)."
        return None

    def execute_run(self, run_id: str, goal: str, model_client, env) -> RunState:
        state = RunState(run_id=run_id, history=[{"role": "user", "content": goal}])
        state.status = RunStatus.RUNNING

        try:
            while state.status == RunStatus.RUNNING:
                state.current_turn += 1

                # Check budget constraints before turn
                budget_violation = self._check_budget(state)
                if budget_violation:
                    state.status = RunStatus.ABORTED
                    state.termination_reason = budget_violation
                    break

                # Model inference step
                output, tokens = model_client.predict(state.history)
                state.tokens_used += tokens

                # Check model completion signal
                if output.startswith("FINAL:"):
                    state.status = RunStatus.SUCCEEDED
                    state.termination_reason = "Goal completed by model."
                    state.history.append({"role": "assistant", "content": output})
                    break

                # Execute action
                tool_name, args = env.parse_action(output)
                observation = env.execute(tool_name, args)
                state.history.append({"role": "assistant", "content": output})
                state.history.append({"role": "user", "content": f"Observation: {observation}"})

        except Exception as e:
            state.status = RunStatus.FAILED
            state.termination_reason = f"Runtime error: {str(e)}"

        return state
```

</details>

## Framework implementations

- **OpenAI Agents SDK**: Implements `Runner.run()` and `RunContext` primitives that govern message loops, track token usage, handle handoffs, and manage graceful run termination.
- **LangGraph Checkpointers**: Saves execution state graphs to PostgreSQL or SQLite after each node. Graph execution can be paused for days waiting for external events and resumed with full state fidelity.
- **Temporal & Inngest**: Used by enterprise agent systems to provide durable workflow execution, automatic retries, exponential backoffs, and guaranteed run cleanup across distributed clusters.

## Data flow and state changes

Trace the state changes during an aborted agent run due to turn exhaustion:

| Timestamp | Run state | Action / Event | State update / Observation |
| --- | --- | --- | --- |
| $t = 0$ | `CREATED` $\rightarrow$ `RUNNING` | Run initialized with goal; executes Turn 1. | Tool A invoked; returns Observation 1. |
| $t = 1$ | `RUNNING` | Model re-evaluates and executes Turn 2. | Tool A invoked; returns Tool Error. |
| $t = 2$ | `RUNNING` | Model attempts retry and executes Turn 3. | Tool A invoked; returns Tool Error. |
| $t = 3$ | `ABORTED` | Host checks `current_turn (3) >= max_turns (3)`. | Overrides loop, sets reason `"Max turns reached"`, alerts operator, and tears down sandbox. |

## Trust boundaries

1. **Lifecycle Control Boundary**: Termination checks must be enforced strictly in the host runtime, never by trusting the model to count its own steps or token usage.
2. **Resource Cleanup Boundary**: When a run terminates (especially upon failure or abort), the host must guarantee that temporary sandboxes, database transactions, and open sockets are torn down immediately to prevent resource exhaustion.
3. **Audit Log Immutability**: The final state, token metrics, and termination reasons must be written to tamper-evident telemetry storage for security post-mortems.

## Reliability failures

- **Zombie Runs**: Runs that hang indefinitely because no wall-clock timeout was configured on external tool calls or network requests.
- **Silent Budget Depletion**: Failing to set per-run token limits, resulting in a single stuck agent exhausting an organization's monthly API quota.
- **State Corruption on Abort**: Aborting a run in the middle of a multi-step database migration without rolling back intermediate transactions.

## Worked example

Consider a code-fixing agent:
1. **Goal**: *"Fix the failing unit tests in `auth_test.py`."*
2. **Budget**: `max_turns = 4`.
3. **Turn 1**: Agent edits `auth.py`. Runs `pytest`. Observation: 2 tests still fail.
4. **Turn 2**: Agent edits `auth.py` again. Runs `pytest`. Observation: 1 test still fails.
5. **Turn 3**: Agent edits `auth_test.py`. Runs `pytest`. Observation: 1 test still fails.
6. **Turn 4**: Agent edits `auth.py`. Runs `pytest`. Observation: 1 test still fails.
7. **Turn 5**: Host evaluates `current_turn (4) >= max_turns (4)`. Host terminates run with status `ABORTED` and message: *"Turn budget reached. 1 test remaining. Partial diff saved to branch `agent-attempt-402`."*

## Limitations and trade-offs

- **Strict Timeouts vs. Complex Problem Solving**: Aggressive turn and time caps prevent runaway costs, but may prematurely kill agents working on genuinely difficult, long-horizon tasks.
- **Durable Checkpointing Overhead**: Serializing state to disk on every turn adds I/O latency, but is strictly necessary for production reliability and resumption.

## Security preview

Uncontrolled lifecycles are a primary target for resource-exhaustion denial of service attacks. In [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security chapters, we analyze how malicious prompts cause infinite loops (algorithmic complexity attacks), how incomplete state teardown leaks sensitive credentials across multi-tenant agents, and how termination hooks must be hardened against bypass.

## Open research questions

- How can runtimes dynamically predict the optimal step budget for a given goal complexity rather than relying on static developer-configured thresholds?
- What standardized state-serialization formats allow seamless migration of paused agent runs across heterogeneous cloud infrastructure?

## Key takeaways

- An agent run moves through explicit states: `CREATED`, `RUNNING`, `PAUSED`, `SUCCEEDED`, `ABORTED`, and `FAILED`.
- Multi-layered termination conditions (model signal, turn budget, token budget, wall-clock timeout, policy invariants) are mandatory to prevent runaway systems.
- Robust runtimes serialize state at checkpoints and enforce deterministic cleanup of environment resources upon termination.

## References

- OpenAI. *OpenAI Agents SDK: Runs and Lifecycle*. OpenAI Documentation, 2024. [OpenAI Reference](https://openai.github.io/openai-agents-python/).
- LangChain. *LangGraph: Human-in-the-Loop and State Persistence*. LangChain Documentation, 2024. [LangGraph Reference](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop).
- S. Zhang, M. Chen, L. Wang, and T. Brown. *Stop Hand-Holding Your Coding Agent*. arXiv preprint, July 2026. [DOI: 10.48550/arXiv.2607.00038](https://doi.org/10.48550/arXiv.2607.00038).

---

[Next Section: Agent Architectures →](../02-agent-architectures/chapter-plan.md)
