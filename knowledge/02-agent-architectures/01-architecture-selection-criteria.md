<!--
---
title: Architecture selection criteria
unit_id: P1-02-01
summary: Establishes a systematic decision framework and trade-off matrix for selecting
  among deterministic workflows, single-agent loops, and multi-agent coordination
  patterns based on latency, cost, determinism, and failure containment.
prerequisites:
- Read [Agent foundations chapter plan](../01-agent-foundations/chapter-plan.md).
- Read [Run lifecycle and termination](../01-agent-foundations/05-run-lifecycle-and-termination.md).
learning_objectives:
- Classify AI orchestration architectures across four distinct tiers of agency from
  fixed pipelines to multi-agent networks.
- Apply the Principle of Least Agency to select the most deterministic architecture
  that reliably fulfills system requirements.
- Evaluate trade-offs across latency, token cost, debuggability, state durability,
  and failure blast radius.
- Identify how modern frameworks represent workflow graphs, agent loops, and supervisor
  handoffs.
source_records:
- p1-02-01-anthropic-agent-patterns-2024
- p1-02-01-langgraph-workflows-agents-2024
- p1-02-01-google-adk-orchestration-2024
- p1-02-01-madaan-self-refine-2023
visual_assets:
- assets/images/02-agent-architectures/01-architecture-selection-criteria/01-architecture-spectrum-and-patterns.png
- assets/images/02-agent-architectures/01-architecture-selection-criteria/02-architecture-selection-decision-tree.png
- assets/images/02-agent-architectures/01-architecture-selection-criteria/03-architecture-tradeoffs-and-blast-radius.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-17'
---
-->

# Architecture selection criteria

## Why this matters

Building an AI-enabled system requires choosing how control flow is managed. System designers often jump directly to complex multi-agent architectures when a simpler, deterministic pipeline would achieve higher accuracy at a fraction of the latency and cost. Conversely, applying a rigid sequential workflow to an open-ended discovery task produces brittle software that breaks as soon as input variations emerge.

Architecture selection is not a matter of style; it defines your system's operational stability, cost ceiling, and security boundary. Every time you grant a language model runtime authority over execution paths, you trade determinism for flexibility. A disciplined architecture selection framework ensures that you add dynamic autonomy only where necessary while keeping critical control paths predictable, auditable, and grounded in [Agent foundations](../01-agent-foundations/chapter-plan.md) before implementing individual [Building blocks](../03-building-blocks/chapter-plan.md).

## Simple mental model

Consider the logistics of moving packages through a modern fulfillment center:

1. **Conveyor Belt (Fixed Pipeline)**: Packages move along a fixed mechanical belt through barcode scanning, weighing, and labeling stations. The sequence never changes, throughput is maximum, and failure at any station halts the line immediately.
2. **Sorting Junction (Router)**: An optical scanner reads the destination postal code and flips a mechanical switch to divert the package onto one of several dedicated sorting chutes.
3. **Quality Inspector (Evaluator-Optimizer)**: A worker inspects packaged goods against a strict quality checklist. If packing tape is loose, the worker sends the box back to the packing station with specific rework instructions until it passes inspection.
4. **Autonomous Mobile Robot (ReAct Agent Loop)**: A wheeled robot receives an order to locate items across an expansive warehouse. It navigates aisles dynamically, observes obstacles, re-routes around spills, and picks items using real-time sensor feedback.
5. **Fulfillment Crew (Multi-Agent Network)**: A logistics supervisor coordinates specialized teams: inventory scouts find goods, heavy-lifter robots move pallets, and manifest dispatchers generate shipping labels.

In software architecture, you should always start with the conveyor belt. You introduce sorting switches, quality inspectors, mobile robots, and multi-robot crews only when the task cannot be solved by simpler mechanics.

## Position in the agent workflow

The following visual illustrates the core spectrum of AI architectures, progressing from deterministic code-orchestrated workflows to autonomous multi-agent networks.

![A wide educational cartoon illustration showing four horizontal panels representing the agent architecture spectrum: Panel 1 shows a blue robot on a fixed conveyor belt for deterministic pipelines; Panel 2 shows a green robot at a switchboard routing tasks; Panel 3 shows an iterative loop with a robot testing tools and an evaluator robot checking quality; Panel 4 shows a supervisor robot delegating tasks to specialist worker robots.](../../assets/images/02-agent-architectures/01-architecture-selection-criteria/01-architecture-spectrum-and-patterns.png)

*Figure 1. The agent architecture spectrum. As systems move from left to right, model autonomy and dynamic discovery increase, while execution predictability and determinism decrease.*

As established in [Workflows versus agents](../01-agent-foundations/03-workflows-versus-agents.md), the fundamental distinction lies between **deterministic** control flow (where application code dictates transitions) and **model-directed** control flow (where language model outputs decide transitions at runtime).

## How it works

To select the right architecture, engineers follow the **Principle of Least Agency**: *Use the least dynamic architecture that solves the problem reliably.*

The following decision flowchart guides the selection process through four diagnostic questions:

![An educational cartoon flowchart titled Architecture Selection Guide: The Principle of Least Agency. Four decision boxes with cute robot guides evaluate whether the execution path is fixed, whether inputs can be routed to fixed paths, whether output requires iterative refinement, and whether open-ended tool discovery is required, leading to fixed pipelines, routers, evaluator-optimizers, or multi-agent graphs.](../../assets/images/02-agent-architectures/01-architecture-selection-criteria/02-architecture-selection-decision-tree.png)

*Figure 2. Decision flowchart for choosing the appropriate AI architecture based on task predictability, quality requirements, and environment complexity.*

### The four selection dimensions

1. **Path Predictability**: Is the exact sequence of processing steps known at build time? If yes, hardcode the sequence in application code using prompt chains or parallel steps. If the execution path depends on dynamic runtime observations, introduce an agent loop.
2. **Input Categorizability**: Can incoming requests be classified into a fixed set of distinct workflows? If yes, use a router model to classify the intent and dispatch execution to a specialized deterministic pipeline.
3. **Verification Rigor**: Does the task require progressive self-correction against explicit rubrics, schemas, or test suites? If yes, wrap generation in an evaluator-optimizer loop.
4. **Environment Exploration Depth**: Does the task require multi-step environment discovery across unknown APIs, files, or services? If yes, deploy a single-agent loop for compact toolsets, or a multi-agent supervisor network when tools span multiple isolated domains.

## Main variants

Modern AI architectures combine eight fundamental orchestration patterns across four tiers of agency:

### Tier 1: Deterministic workflows

- **Prompt Chaining**: A linear sequence of model calls where the output of step $N$ serves as the input or context for step $N+1$.
- **Parallelization (Sectioning and Voting)**: Splitting an input into independent partitions processed concurrently by separate model calls, or querying multiple model instances simultaneously to vote on a consensus answer.

### Tier 2: Conditional routing

- **Routing Workflows**: A deterministic classifier or small model analyzes an input query and directs it to a dedicated downstream prompt, tool, or pipeline.

### Tier 3: Iterative and autonomous loops

- **Evaluator-Optimizer (Self-Refine)**: An iterative loop where a generator model produces an artifact and a separate evaluator model checks it against explicit rubrics, returning critique for revision until accepted.
- **Plan-and-Execute**: The model separates task planning from action execution. A planner model creates a multi-step execution graph, and executor nodes run the steps sequentially or in parallel.
- **Single-Agent Tool Loop (ReAct)**: The model enters an iterative cycle of reasoning, tool selection, action execution, and environment observation until the goal is achieved.

### Tier 4: Multi-agent coordination

- **Hierarchical Supervisor**: A central coordinator agent breaks down a complex problem, dispatches discrete sub-tasks to specialized worker agents, and aggregates their findings.
- **Handoffs and Swarms**: Peer agents transfer execution control directly to one another based on specialized capabilities without returning to a central supervisor.
- **Event-Driven State Graphs**: Stateful computational graphs where state transitions are triggered by events, human approvals, or external webhook signals with durable pause and resume capabilities.

## Minimal implementation

The following Python script illustrates how the same problem (incident triage) is realized under a deterministic router, an evaluator-optimizer, and an autonomous agent loop:

```python
from typing import Dict, Any, List

# Simulated model and tool interfaces
class MockModel:
    def generate(self, prompt: str) -> str:
        if "Classify" in prompt:
            return "DATABASE_ALERT"
        if "Extract" in prompt:
            return "host=db-prod-01, metric=connection_timeout"
        if "Evaluate" in prompt:
            return "PASS: Root cause identified."
        return "Action: query_logs(db-prod-01)"

class ToolEnvironment:
    def query_logs(self, host: str) -> str:
        return f"Found 45 timeout errors on {host} in past 5m."

# 1. Deterministic Router Workflow Pattern
def router_incident_workflow(alert_text: str, model: MockModel) -> Dict[str, Any]:
    """Code directs the flow based on a single model classification step."""
    category = model.generate(f"Classify incident category: {alert_text}")
    if category == "DATABASE_ALERT":
        entities = model.generate(f"Extract DB entities: {alert_text}")
        return {"route": "db_team", "details": entities}
    elif category == "NETWORK_ALERT":
        return {"route": "net_ops", "details": "Standard network escalation"}
    else:
        return {"route": "general_helpdesk", "details": alert_text}

# 2. Evaluator-Optimizer Pattern
def evaluator_optimizer_triage(incident_summary: str, model: MockModel, max_turns: int = 3) -> str:
    """Iteratively drafts and verifies analysis against acceptance criteria."""
    draft = incident_summary
    for iteration in range(max_turns):
        evaluation = model.generate(f"Evaluate root-cause analysis for completeness: {draft}")
        if evaluation.startswith("PASS"):
            return draft
        draft = model.generate(f"Improve analysis based on critique ({evaluation}): {draft}")
    return draft

# 3. Model-Directed Autonomous Agent Loop
def reactive_agent_triage(incident_id: str, model: MockModel, env: ToolEnvironment, max_turns: int = 4) -> str:
    """Model dynamically decides which tools to invoke and when to stop."""
    state = [{"role": "user", "content": f"Investigate incident {incident_id}"}]
    for turn in range(max_turns):
        action_decision = model.generate(str(state))
        if action_decision.startswith("FINAL:"):
            return action_decision
        observation = env.query_logs("db-prod-01")
        state.append({"role": "assistant", "content": action_decision})
        state.append({"role": "tool", "content": observation})
    return "Investigation timed out: maximum turns reached."
```

## Framework implementations

Modern frameworks organize and name these architectural tiers according to their runtime models:

- **LangGraph**: Models both deterministic workflows and autonomous agents as stateful graphs. Workflows are represented as Directed Acyclic Graphs (DAGs) with hardcoded transitions, while agents are represented as cyclical graphs with conditional edge functions evaluated by model outputs.
- **Google Agent Development Kit (ADK)**: Separates procedural workflow engines from autonomous agents, enabling developers to build deterministic outer pipelines that invoke specialized autonomous agents only at designated pipeline nodes.
- **Microsoft Semantic Kernel**: Provides step-based plan execution alongside multi-agent chat orchestration (such as `AgentGroupChat`), supporting both structured sequential pipelines and autonomous agent handoffs.
- **AutoGen**: Emphasizes multi-agent conversation architectures, modeling supervisor hierarchies and peer-to-peer swarms where agents exchange structured messages to solve collaborative tasks.

## Data flow and state changes

State management models vary fundamentally across architecture patterns:

| Paradigm | State transition model | Control mechanism | Typical state payload |
| --- | --- | --- | --- |
| **Deterministic Workflow** | Linear Directed Acyclic Graph (DAG) | Application code routes state from Step A to Step B to Step C. | Structured schema passed between fixed pipeline functions. |
| **Evaluator-Optimizer** | Controlled Iteration Loop | Code coordinates generator and evaluator turns until criteria match. | Candidate draft artifact, critique feedback, and loop counter. |
| **Autonomous Agent** | Cyclic State Machine | Model inspects accumulated history, selects tools, and loops until goal satisfied. | Chronological context window containing goal, tool calls, and observations. |
| **Multi-Agent Network** | Distributed Message Graph | Supervisor or router passes sub-tasks across distinct agent contexts. | Structured message bus with isolated agent-specific memory partitions. |

## Trust boundaries

1. **Workflow Boundaries**: In a deterministic workflow, trust boundaries are enforced at compile time or in code structure. Each tool is called only by explicit code at designated steps with validated inputs.
2. **Agent Boundaries**: In an agent loop, the model has access to a tool suite at every turn. The host runtime must enforce dynamic permissions, inspecting every individual tool request at runtime to verify authorization.
3. **Multi-Agent Boundaries**: In multi-agent systems, boundaries exist between agent domains. A low-privilege agent parsing untrusted web content must not be allowed to invoke high-privilege administrative tools on a peer agent without explicit isolation gates.

## Reliability failures

- **Workflow Failure Modes**: Workflows fail when encountering input schemas or edge cases that were not anticipated by the human programmer, leading to unhandled exceptions or invalid outputs passed downstream.
- **Agent Failure Modes**: Agents fail through reasoning breakdowns, hallucinating non-existent tool capabilities, thrashing in repetitive tool loops, or misinterpreting tool error messages as task completion.
- **Multi-Agent Failure Modes**: Multi-agent systems fail through cascading misunderstandings, message flooding, deadlock in peer-to-peer handoffs, or conflicting sub-goals chosen by autonomous workers.

## Worked example

Consider a customer request: *"I was billed twice for my order last Tuesday."*

- **Workflow Approach**:
  1. A router model classifies the intent as `billing_duplicate_charge`.
  2. Code calls `fetch_transactions(user_id, date="last Tuesday")`.
  3. Code checks if duplicate charges exist. If found, code calls `create_refund_ticket(charge_id)`.
  4. A final model drafts the customer response using the ticket details.
  *Result*: Fast, 100% predictable, easily audited.

- **Agent Approach**:
  1. Agent receives the request and decides to call `search_knowledge_base("refund policies")`.
  2. Agent calls `fetch_user_profile()`.
  3. Agent calls `list_all_invoices()`.
  4. Agent analyzes charges and calls `issue_refund()`.
  *Result*: Flexible, but consumed 4 API turns and could potentially call unintended tools if confused.

## Limitations and trade-offs

Every step to the right along the architecture spectrum involves trade-offs across latency, operational cost, debuggability, and safety boundaries.

The visual below illustrates how performance characteristics and failure blast radiuses evolve across representative architectures:

![A cartoon comparison graphic showing three vertical columns comparing a Deterministic Workflow, a Single ReAct Loop, and a Multi-Agent Supervisor. Metrics for latency, cost, debuggability, and failure blast radius are displayed with cute robot characters and icons.](../../assets/images/02-agent-architectures/01-architecture-selection-criteria/03-architecture-tradeoffs-and-blast-radius.png)

*Figure 3. Comparative trade-offs across three representative architectures. Increasing autonomy expands flexibility but compounds token cost, increases response latency, and enlarges the failure blast radius.*

### Architecture trade-off comparison

| Architecture Pattern | Typical Latency | Token Cost | State Complexity | Debuggability | Failure Blast Radius |
| --- | --- | --- | --- | --- | --- |
| **Prompt Chaining** | Low (bounded) | Low (linear) | Stateless / Linear DAG | High (deterministic trace per step) | Isolated to single step output |
| **Routing Workflow** | Low (1 + branch) | Low (linear) | Stateless / Branch state | High (inspect router classification) | Contained within selected branch |
| **Parallel Sectioning** | Low (parallel) | Moderate ($N$ calls) | Fork-join aggregation | High (isolated sub-task logs) | One failed partition handled by fallback |
| **Evaluator-Optimizer** | Medium ($K$ loops) | Moderate ($2 \times K$) | Iteration history + feedback | High (explicit rubric logs) | Contained within generation cycle |
| **Single ReAct Agent** | High (variable turns) | High (growing context) | Turn-by-turn memory buffer | Medium (non-deterministic traces) | Scoped to all tools exposed to the agent |
| **Plan-and-Execute** | High (plan + actions) | High (plan + steps) | Plan status board + observations | Medium (plan revision checkpoints) | Scoped to plan modification and tools |
| **Multi-Agent Network** | Highest (multi-agent hops) | Highest (multiplied context) | Distributed message state | Low (inter-agent communication traces) | Broad (cascading errors across agents) |

## Security preview

The architecture you choose directly determines your system's attack surface. While a deterministic workflow limits prompt injection impact to the current processing step, an autonomous agent allows prompt injections to divert tool execution sequences dynamically. Furthermore, multi-agent networks introduce cross-agent privilege escalation and confused deputy vulnerabilities. We analyze these compound threat dynamics in detail in [threat modeling](../06-threat-model/chapter-plan.md) and [end-to-end attack paths](../07-security-by-component-and-workflow-stage/07-end-to-end-attack-paths/chapter-plan.md).

## Open research questions

- How can hybrid systems dynamically determine at runtime when a deterministic workflow should escalate an anomalous edge case to an autonomous agent loop?
- What standardized metrics reliably quantify the reliability degradation when transitioning from fixed pipelines to model-directed loops?

## Key takeaways

- Always apply the **Principle of Least Agency**: start with deterministic prompt chaining or routing workflows, and add model-directed loops only when dynamic discovery is strictly required.
- **Deterministic workflows** provide bounded latency, predictable token costs, easy unit testing, and isolated failure boundaries.
- **Autonomous agent loops** enable open-ended problem solving and dynamic tool orchestration, but introduce non-deterministic execution, variable latency, and expanded security attack surfaces.
- **Multi-agent architectures** are justified only when tasks require distinct domain isolation, segregated tool catalogs, or separate permission boundaries.
- Choose your architecture based on four diagnostic dimensions: path predictability, input categorizability, verification rigor, and environment exploration depth.

## References

- Anthropic. *Building Effective Agents*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Research](https://www.anthropic.com/research/building-effective-agents).
- LangChain. *Workflows and Agents: Choosing the Right Architectural Pattern*. LangChain Documentation, 2024. [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/workflows-agents).
- Google. *Agent Architecture and Orchestration*. Google Agent Development Kit, 2024. [Google ADK Documentation](https://adk.dev/agents/).
- Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Welleck, S., Majumder, B. P., Gupta, S., Yazdanbakhsh, A., & Clark, P. *Self-Refine: Iterative Refinement with Self-Feedback*. NeurIPS 2023. [NeurIPS Paper](https://papers.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html).

---

[Next Unit: Single agent and reactive loops →](02-single-agent-and-reactive-loops.md)
