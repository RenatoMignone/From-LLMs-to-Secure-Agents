<!--
---
title: Supervisors, handoffs, and agent-as-tool
unit_id: P1-02-07
summary: Explores multi-agent coordination architectures, comparing centralized supervisors
  (manager-worker), decentralized peer handoffs (swarm), and encapsulated subagents
  (agent-as-a-tool).
prerequisites:
- Read [Architecture selection criteria](01-architecture-selection-criteria.md).
- Read [State machines and event-driven graphs](06-state-machines-and-event-driven-graphs.md).
learning_objectives:
- Distinguish hierarchical supervisor architectures from peer-to-peer handoffs and
  tool-encapsulated subagents.
- Implement context isolation to prevent context window bloat and enforce least privilege
  across subagents.
- Construct function-based transfer routines for deterministic peer handoffs.
- Mitigate multi-agent failure modes including handoff ping-pong loops, supervisor
  bottlenecks, and delegation cascades.
source_records:
- p1-02-07-openai-swarm-2024
- p1-02-07-anthropic-multi-agent-orchestrator-2024
- p1-02-07-microsoft-autogen-teams-2024
visual_assets: []
example_paths:
- examples/02-agent-architectures/07-supervisors-handoffs-and-agent-as-tool/multi_agent_coordination.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-17'
---
-->

# Supervisors, handoffs, and agent-as-tool

## Why this matters

A single monolithic agent equipped with dozens of tools and a sprawling system prompt quickly degrades in reliability. As prompt size grows, models suffer from distraction, hallucinated tool arguments, and degraded reasoning. Furthermore, granting one agent global access to every system credential violates the principle of least privilege.

**Multi-agent coordination architectures** solve this by dividing complex responsibilities among specialized, focused agents (Anthropic, 2024; Microsoft, 2024). Rather than forcing one model to do everything, systems organize agents into distinct topologies: centralized supervisors that delegate tasks, peer meshes that hand off conversational control, or parent agents that invoke subagents through encapsulated tool interfaces. Understanding these three patterns is essential before studying low-level protocols in [Frameworks and protocols](../04-frameworks-and-protocols/chapter-plan.md).

## Simple mental model

Think of how a modern hospital coordinates patient care:

1. **The Chief of Medicine (Supervisor Pattern)**: The lead physician assesses the patient, decomposes the diagnosis into distinct orders (blood work, MRI, cardiology consult), assigns each order to a specialized department, and synthesizes the specialist reports into a master treatment plan.
2. **Specialist Handoffs (Peer Handoff Pattern)**: When a patient enters the Emergency Room, the Triage nurse checks vital signs and transfers the patient directly to the Orthopedic Trauma doctor. Control passes from one specialist to the next like passing a baton.
3. **External Diagnostic Lab (Agent-as-a-Tool Pattern)**: When the doctor orders a genetic sequencing test, the lab operates as a black box. The lab receives a blood sample and returns a two-page summary report. The doctor does not need to observe the lab technician operating the centrifuge.

In software engineering, these three topologies provide varying levels of centralization, autonomy, and context encapsulation.

## Position in the agent workflow

The figures below compare the three primary coordination topologies and demonstrate how subagent encapsulation isolates prompt context.

> [!NOTE]
> *Visual illustrations (Figure 1: Multi-Agent Coordination Topologies; Figure 2: Context Isolation & Delegation Flow) are staged for AI generation once API quota resets. Prompts are preserved in `source/`.*

*Figure 1. The three multi-agent coordination topologies: Hierarchical Supervisor (star topology), Peer Handoffs (decentralized mesh), and Agent-as-a-Tool (black-box encapsulation).*

*Figure 2. Context isolation and subagent encapsulation. Heavy intermediate tool interactions remain trapped inside the worker sandbox, preserving parent context capacity.*

As established in [Architecture selection criteria](01-architecture-selection-criteria.md), multi-agent architectures introduce coordination overhead and should only be adopted when single-agent or workflow patterns cannot satisfy context isolation or domain specialization requirements.

## How it works

### 1. Supervisor pattern (orchestrator-workers)

The **Supervisor pattern** uses a central coordinator agent connected to multiple specialized worker agents in a star topology (Anthropic, 2024):
- The supervisor receives the user objective and maintains global state.
- The supervisor invokes worker agents sequentially or in parallel, passing each worker a narrowly scoped task description.
- Each worker executes its task in its own isolated context and returns its result to the supervisor.
- The supervisor evaluates worker outputs and synthesizes the final response for the user.

### 2. Peer handoffs (swarm pattern)

The **Handoff pattern** eliminates the central coordinator in favor of direct peer-to-peer transfers (OpenAI, 2024):
- Multiple specialized agents exist in a flat mesh network (e.g., `TriageAgent`, `BillingAgent`, `TechnicalSupportAgent`).
- Each agent has access to a set of specialized tools plus explicit transfer functions (e.g., `transfer_to_billing()`, `transfer_to_support()`).
- When an agent determines that a user request falls outside its domain, it invokes the transfer tool, handing off conversation history and active execution ownership to the target agent.

### 3. Agent-as-a-tool (nested subagent)

The **Agent-as-a-Tool pattern** treats an entire agent loop as a callable function from the perspective of a parent agent:
- The parent agent sees the child agent as a standard tool definition with a JSON schema (e.g., `audit_repository(repo_url: str) -> str`).
- When the parent invokes the tool, runtime infrastructure spawns an isolated subagent instance with its own private context window, system prompt, and specialized tools.
- The child agent runs its internal loop to completion and returns a concise textual summary back to the parent.
- The parent never sees the child's intermediate reasoning tokens, scratchpad, or raw API outputs.

## Main variants

1. **Hierarchical Supervisor Tree**: Multi-level management hierarchies where a top-level director agent manages department managers, who in turn supervise task workers.
2. **Broadcast Group Chat (AutoGen)**: Multi-agent conversations where agents speak in a shared thread managed by a speaker-selection policy or round-robin scheduler (Microsoft, 2024).
3. **Static Router Handoff**: Deterministic code routing user intents directly to specialized agents without requiring LLM-driven transfer functions.

## Minimal implementation

The following Python script implements the three coordination patterns in a clean, framework-agnostic runtime:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from typing import Dict, Any, List, Optional

class SubagentTool:
    """Encapsulates an autonomous subagent within a standard tool interface."""
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def run(self, task_query: str) -> str:
        # Isolated internal execution loop
        return f"[{self.name}] Resolved: '{task_query}'. Found 0 issues."

class SwarmAgent:
    """Peer agent capable of handling tasks or handing off control."""
    def __init__(self, name: str):
        self.name = name

    def respond(self, message: str) -> Dict[str, Any]:
        if "billing" in message.lower() and self.name != "BillingAgent":
            return {"action": "handoff", "target": "BillingAgent"}
        return {"action": "reply", "content": f"[{self.name}] Handled: {message}"}

class SupervisorAgent:
    """Central manager delegating sub-tasks and synthesizing results."""
    def __init__(self):
        self.workers = {
            "researcher": SubagentTool("Researcher", "Search literature."),
            "coder": SubagentTool("Coder", "Write clean Python.")
        }

    def execute(self, goal: str) -> Dict[str, Any]:
        res = self.workers["researcher"].run(f"Research: {goal}")
        code = self.workers["coder"].run(f"Code: {goal}")
        return {
            "status": "COMPLETED",
            "synthesis": f"Supervisor complete for '{goal}'.\n1. {res}\n2. {code}"
        }
```

</details>

## Framework implementations

- **LangGraph Multi-Agent**: Constructs supervisor graphs using a central node with conditional edges that route to worker nodes, returning to the supervisor upon node completion.
- **OpenAI Swarm**: Implements lightweight multi-agent handoffs where functions return an instance of another `Agent` object to transfer conversation control.
- **AutoGen (Microsoft)**: Supports conversational multi-agent architectures including `GroupChatManager`, hierarchical teams, and nested chats where agents act as tools for other agents.
- **Google Agent Development Kit (ADK)**: Uses multi-agent workflow coordinators to orchestrate specialized domain models with strict role-based tool assignments.

## Data flow and state changes

Compare the state flow across the three coordination topologies:

| Pattern | Control Center | Context Boundary | Handoff Mechanism | Failure Risk |
| --- | --- | --- | --- | --- |
| **Supervisor** | Central Manager | Isolated per worker; aggregated at manager | Supervisor delegates sub-tasks directly | Single point of bottleneck / failure |
| **Peer Handoff** | Active Peer | Shared or passed along transfer chain | Dynamic tool call returns target agent | Ping-pong looping between peers |
| **Agent-as-a-Tool** | Parent Agent | Complete black-box encapsulation | Synchronous tool execution call | Opaque failures inside child agent |

## Trust boundaries

1. **Inter-Agent Privilege Boundary**: Subagents must only possess API credentials required for their specific domain. A research subagent must not share write credentials with a deployment subagent.
2. **Context Leakage Boundary**: When passing state during handoffs, sensitive user data (such as passwords or session cookies) must be scrubbed to prevent propagation across untrusted specialist agents.
3. **Delegation Authenticity Boundary**: Supervisors must verify that worker responses originate from authorized subagent sandboxes rather than spoofed message injections.

## Reliability failures

- **Ping-Pong Handoff Loops**: Two peer agents continuously transfer a ambiguous request back and forth (e.g., `Triage` -> `Billing` -> `Triage` -> `Billing`) until token limits are exhausted.
- **Context Loss on Transfer**: A handoff function transfers conversation ownership without forwarding critical user parameters (e.g., transferring a user to `Billing` without their customer ID).
- **Supervisor Hallucination / Bottleneck**: A central supervisor misinterprets a specialized worker's technical output and synthesizes an incorrect summary for the user.

## Worked example

Consider an enterprise incident response system:
1. **Supervisor Ingress**: An alert triggers the Incident Supervisor: *"High database latency detected on cluster-west"*.
2. **Parallel Delegation**:
   - Supervisor invokes `MetricsWorker` (SubagentTool) to query Prometheus metrics.
   - Supervisor invokes `LogWorker` (SubagentTool) to inspect Postgres error logs.
3. **Isolated Execution**:
   - `MetricsWorker` executes 12 PromQL queries in isolation, finding a connection pool spike.
   - `LogWorker` parses 5,000 log lines in isolation, identifying an unindexed query in the latest commit.
4. **Synthesis & Mitigation**:
   - Both workers return concise 3-line summaries to the Supervisor.
   - Supervisor determines root cause and invokes `GitWorker` to prepare a rollback pull request.
   - Supervisor notifies the on-call engineer with a unified incident debrief.

## Limitations and trade-offs

- **Token & Cost Multiplication**: Multi-agent systems invoke multiple model instances per user task, increasing token usage and API latency compared to single-agent workflows.
- **Coordination Complexity**: Debugging distributed multi-agent interactions requires comprehensive distributed tracing across agent boundaries.

## Security preview

Multi-agent systems expand the attack surface through **delegation cascades** and **confused deputy attacks**. If an untrusted worker agent is manipulated by indirect prompt injection, it may return malicious recommendations that deceive the supervisor into executing destructive actions with higher privileges. We analyze cross-agent trust, privilege delegation, and multi-agent security in [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security chapters.

## Open research questions

- What formal verification protocols can guarantee that decentralized multi-agent handoff meshes will converge without deadlock or livelock?
- How can parent agents dynamically calibrate the optimal degree of context compression when delegating to nested subagents?

## Key takeaways

- **Supervisors (Manager-Worker)** centralize planning and synthesis, providing strong control and coordination over specialized workers.
- **Peer Handoffs (Swarm)** enable direct, flexible baton-passing between specialized domain agents without central bottlenecks.
- **Agent-as-a-Tool** encapsulates complex subagent loops into standard callable functions, protecting parent context windows from token pollution.
- Multi-agent systems require strict context isolation, least-privilege credential scoping, and cycle limits to prevent infinite handoff loops.

## References

- OpenAI. *Swarm: An Educational Framework for Multi-Agent Orchestration*. OpenAI Open Source Research, 2024. [GitHub Swarm](https://github.com/openai/swarm).
- Anthropic. *Building Effective Agents: Orchestrator-Workers and Multi-Agent Patterns*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Research](https://www.anthropic.com/research/building-effective-agents).
- Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D., & Wang, C. *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. Microsoft Research, 2024. [Microsoft AutoGen](https://microsoft.github.io/autogen/).

---

[Next Unit: Architecture trade-offs →](chapter-plan.md)
