<!--
---
title: Goals, policies, environments, and autonomy
unit_id: P1-01-04
summary: Details how agent goals, operational policies, environment characteristics,
  and autonomy levels interact to govern agent behavior and safety.
prerequisites:
- Read [What is an agent](01-what-is-an-agent.md).
- Read [The agent loop](02-the-agent-loop.md).
- Read [Workflows versus agents](03-workflows-versus-agents.md).
learning_objectives:
- Define agent goals and differentiate declarative end-states from procedural instructions.
- Construct deterministic policies and guardrails that restrict tool capabilities.
- Classify software environments by observability, determinism, dynamism, and continuity.
- Evaluate the autonomy spectrum from direct human control to fully autonomous execution.
source_records:
- p1-01-04-russell-norvig-aima-environments
- p1-01-04-morris-levels-agi-2023
- p1-01-04-nist-ai-rmf-2023
visual_assets:
- assets/images/01-agent-foundations/04-goals-policies-environments-and-autonomy/01-goals-policies-environments-autonomy.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-15'
---
-->

# Goals, policies, environments, and autonomy

## Why this matters

An agent does not operate in a vacuum. To perform useful work, an agent requires an objective to achieve (**goal**), boundaries that constrain its behavior (**policy**), a software context to interact with (**environment**), and a defined level of independent authority (**autonomy**).

If any of these four pillars is misconfigured, agent systems degrade quickly. A vague goal causes wandering reasoning loops. A weak policy permits dangerous actions like unconfirmed database drops. An unmodeled environment leads to unexpected tool failures. Excessive autonomy without oversight exposes organizations to uncontained financial and operational damage. Formalizing these four concepts is essential for building safe and capable agentic systems.

## Simple mental model

Think of an apprentice chef working in a professional restaurant kitchen.

- **Goal**: "Prepare thirty portions of vegetable lasagna for the 7:00 PM dinner service."
- **Policy**: "Always wear protective gloves, never substitute dairy ingredients on allergy orders, and ask the head chef before opening the high-value reserve pantry."
- **Environment**: The physical kitchen: ovens, cutting boards, ingredient refrigerators, timers, and order tickets.
- **Autonomy Level**: The apprentice chops vegetables and boils pasta independently, but must present a tasting sample to the head chef before plating the final dishes.

In AI engineering, the host system is the restaurant manager setting the objective and safety rules, while the language model is the apprentice operating within the kitchen environment under calibrated supervision.

## Position in the agent workflow

Use this diagram to trace how goals, safety policies, environment interfaces, and autonomy spectrum levels interact to govern agent execution.

![A 4-panel cartoon infographic diagram illustrating: 1. Goal definition with success criteria, 2. Policy guardrails and safety limits with protective shields, 3. Environment sandbox where a cute robot agent executes actions and receives observations, and 4. The Autonomy Spectrum ranging from human-in-the-loop to supervised autonomy and full autonomy.](../../assets/images/01-agent-foundations/04-goals-policies-environments-and-autonomy/01-goals-policies-environments-autonomy.png)

*Figure 1. The four pillars of agent architecture. Goals establish target objectives, policies enforce non-negotiable safety guardrails, environments define available actions and observation feedback, and autonomy levels calibrate the degree of human oversight.*

Trace how each pillar shapes the operational envelope:
1. **Goal**: Supplies the mission objective, acceptance criteria, and stopping definitions for the agent run.
2. **Policy**: Enforces deterministic constraints, tool allowlists, rate limits, and mandatory human sign-off thresholds.
3. **Environment**: Exposes APIs, filesystems, and databases while returning structured observation feedback to the agent loop.
4. **Autonomy Spectrum**: Governs when the agent executes autonomously versus when it must pause for human intervention.

## How it works

### 1. Goals: Declarative versus imperative objectives

- **Declarative Goal**: Specifies *what* state the world should reach, leaving the trajectory to the model (for example, "Ensure all test suites in the repository pass").
- **Imperative Instructions**: Specifies *how* the model must proceed step by step (for example, "Run pytest, read failures, edit test files, and rerun pytest").

Declarative goals maximize model flexibility but require robust success criteria so the agent knows when to stop.

### 2. Policies: Invariants and guardrails

A policy is the set of explicit rules and constraints enforced by both prompt instructions and deterministic host code:
- **Scope Limits**: Restricting which directories, tables, or endpoints the agent may touch.
- **Resource Budgets**: Capping total tokens, execution turns, and API dollar expenditures.
- **Action Invariants**: Absolute rules (for example, "Never send an external email without human confirmation").

### 3. Environments: Core properties

Following classical AI formalization by [Russell and Norvig (2020)](https://aima.cs.berkeley.edu/), agent environments are classified across four key dimensions:

| Dimension | Discrete / Fully Observable | Continuous / Partially Observable |
| --- | --- | --- |
| Observability | **Fully Observable**: Agent sees entire state (e.g., local SQLite database schema and rows). | **Partially Observable**: Agent sees only local snippets (e.g., browsing the live web or reading paginated API logs). |
| Determinism | **Deterministic**: Action $A$ in state $S$ always yields state $S'$ (e.g., local pure function). | **Stochastic**: Action $A$ has probabilistic outcomes or external latency (e.g., third-party network APIs). |
| Dynamism | **Static**: Environment state remains frozen while the model reasons (e.g., static file repository). | **Dynamic**: Environment state changes independently during execution (e.g., live stock ticker or multiplayer chat). |
| Continuity | **Discrete**: Distinct, countable states and actions (e.g., SQL queries, file operations). | **Continuous**: Continuous parameters or sensor streams (e.g., robotic control, audio streaming). |

### 4. Autonomy spectrum

Systems operate across a spectrum of human involvement, formalizing frameworks like [Morris et al. (2023)](https://arxiv.org/abs/2311.02462) and [NIST AI RMF (2023)](https://www.nist.gov/itl/ai-risk-management-framework):

1. **Direct Tool (No Autonomy)**: The human invokes a model directly for a single computation.
2. **Human-in-the-Loop (HITL - Low Autonomy)**: The agent proposes every individual action; a human must click "Approve" before each tool executes.
3. **Human-on-the-Loop (HOTL - Supervised Autonomy)**: The agent executes routine actions independently within policy limits, but pauses and alerts a human operator for high-risk decisions or unhandled exceptions.
4. **Human-out-of-the-Loop (Full Autonomy)**: The agent operates completely independently from initial goal assignment to final completion, bounded only by automated runtime policies.

## Main variants

- **Policy-as-Prompt**: Rules are injected directly into the system prompt text. This is flexible but vulnerable to prompt injection or model confusion.
- **Policy-as-Code (Deterministic Guardrails)**: Rules are enforced by the host runtime before tool execution (such as validating SQL ASTs or checking regex path allowlists).
- **Escalation Policies**: Threshold-based policies that dynamically decrease autonomy when confidence drops or sensitive operations are attempted.

## Minimal implementation

The following Python code demonstrates an agent environment with deterministic policy enforcement and human-on-the-loop escalation:

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

@dataclass
class Policy:
    allowed_tools: List[str]
    require_human_approval: List[str]
    max_steps: int = 5

class SecureEnvironment:
    def __init__(self, policy: Policy):
        self.policy = policy
        self.state: Dict[str, str] = {"status": "active", "balance": "100"}

    def execute_action(self, tool_name: str, args: Dict[str, Any], approve_callback: Callable[[str], bool]) -> str:
        # 1. Policy check: Tool allowlist
        if tool_name not in self.policy.allowed_tools:
            return f"POLICY_VIOLATION: Tool '{tool_name}' is forbidden."

        # 2. Policy check: Escalation / Human approval requirement
        if tool_name in self.policy.require_human_approval:
            approved = approve_callback(f"Action '{tool_name}' with args {args}")
            if not approved:
                return f"ACTION_REJECTED: Human operator denied execution of '{tool_name}'."

        # 3. Execution in environment
        if tool_name == "check_balance":
            return f"Balance is ${self.state['balance']}"
        elif tool_name == "transfer_funds":
            self.state["balance"] = str(int(self.state["balance"]) - int(args.get("amount", 0)))
            return f"Transfer complete. New balance: ${self.state['balance']}"
        return "ERROR: Unknown tool implementation."

# Example test setup
demo_policy = Policy(
    allowed_tools=["check_balance", "transfer_funds"],
    require_human_approval=["transfer_funds"],
    max_steps=3
)
env = SecureEnvironment(demo_policy)
```

</details>

## Framework implementations

- **NIST AI RMF**: Recommends mapping agent system risks to governance controls, establishing clear human-agent escalation boundaries for high-impact decision systems.
- **LangGraph Checkpointers & Breakpoints**: Enables declarative human-in-the-loop interrupts on specific graph nodes before state updates or tool executions are committed.
- **OpenAI Agents SDK Guardrails**: Provides input and output guardrail hooks that validate model requests against deterministic schemas before action dispatch.

## Data flow and state changes

Trace how goals and policies constrain the flow of execution:

| Step | Component | Action / Evaluation | Outcome |
| --- | --- | --- | --- |
| 1. Goal Extraction | Host Parser | User requests: *"Transfer $500 to Account B"*. | Goal initialized: `TransferFunds(amount=500, target="Account B")`. |
| 2. Policy Evaluation | Deterministic Engine | Checks: `amount > $100` threshold rule. | Triggers mandatory human approval interrupt (`HOTL`). |
| 3. Human Gate | Operator Interface | Operator reviews raw target parameters. | If approved, dispatches tool; if rejected, cancels action. |
| 4. Environment Update | Banking Ledger API | Executes ledger transfer across secure trust boundary. | State changes: `$500` deducted; success observation returned. |

## Trust boundaries

1. **Policy Enforcement Boundary**: Policies must never rely solely on model self-policing in system prompts. True policy enforcement must reside in deterministic code on the host runtime.
2. **Environment Isolation**: The environment must restrict agent permissions to least privilege, preventing an agent from escaping its sandbox into the host OS.
3. **Escalation Authenticity**: When an agent requests human approval, the host must present the exact raw tool parameters to the human, preventing deceptive output summaries.

## Reliability failures

- **Specification Gaming**: The model satisfies the literal goal phrasing while violating common-sense intentions (for example, clearing a backlog of failed customer tickets by deleting all open tickets).
- **Partial Observability Blindspots**: The model assumes it has full information when it only received a truncated view, leading to premature or destructive decisions.
- **Policy Drift in Long Contexts**: As the context history grows over many turns, model attention to early system prompt policies can degrade.

## Worked example

Consider a cloud maintenance agent:
- **Goal**: *"Clean up orphaned cloud disk snapshots."*
- **Policy**: *"Allow read operations automatically. Deleting any snapshot older than 90 days requires automated confirmation; deleting snapshots under 90 days is strictly blocked."*
- **Environment**: AWS EC2 API (Partially observable via paginated API calls).
- **Execution**:
  1. Agent calls `list_snapshots()`. Observation: 30 snapshots returned.
  2. Agent identifies 5 snapshots older than 90 days.
  3. Agent calls `delete_snapshot(id="snap-123")`.
  4. Host policy engine verifies age > 90 days, passes policy check, and invokes the API.
  5. Agent attempts `delete_snapshot(id="snap-999")` (age 20 days). Host policy intercepts and returns: `POLICY_VIOLATION: Snapshot age < 90 days`.
  6. Agent completes run without violating safety rules.

## Limitations and trade-offs

- **High Autonomy vs. High Safety**: Increasing autonomy reduces human labor and operational friction, but increases the blast radius of unexpected model failures.
- **Strict Guardrails vs. Task Flexibility**: Highly restrictive policies prevent attacks and mistakes, but may prevent the agent from solving legitimate edge cases.

## Security preview

The interaction between goals, policies, and environments is the central battleground of agent security. In [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security modules, we examine how attackers use prompt injection to override system policies (jailbreaking), exploit ambiguous goals to cause unauthorized actions (confused deputy), and manipulate partially observable environments to feed poisoned data to the agent.

## Open research questions

- How can system architects mathematically verify that a language model will adhere to natural-language safety policies across arbitrary environment states?
- What standardized telemetry formats best capture human-on-the-loop approvals and overrides for regulatory auditing?

## Key takeaways

- **Goals** define the desired outcome; **policies** define non-negotiable operational boundaries and invariants.
- **Environments** vary across observability, determinism, and dynamism; agents must be designed specifically for their environment characteristics.
- **Autonomy** is not binary; systems should be calibrated from human-in-the-loop to supervised autonomy based on risk and blast radius.
- System safety policies must be enforced by deterministic code, never by prompt instructions alone.

## References

- Stuart Russell and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th Edition, Pearson, 2020. [AIMA](https://aima.cs.berkeley.edu/).
- Meredith Ringel Morris, Jascha Sohl-Dickstein, Noah Fiedel, Tris Warkentin, Allan Dafoe, Alejandra Molina, Danielle Ghebreslassie, et al. *Levels of AGI: Operationalizing Progress to AGI*. arXiv preprint, November 2023. [DOI: 10.48550/arXiv.2311.02462](https://doi.org/10.48550/arXiv.2311.02462).
- National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST Trustworthy and Responsible AI, January 2023. [DOI: 10.6028/NIST.AI.100-1](https://doi.org/10.6028/NIST.AI.100-1).

---

[Next Unit: Run lifecycle and termination →](05-run-lifecycle-and-termination.md)
