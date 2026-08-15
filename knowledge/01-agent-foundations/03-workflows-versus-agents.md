<!--
---
title: Workflows versus agents
unit_id: P1-01-03
summary: Compares deterministic code-orchestrated workflows with model-directed autonomous
  agents, establishing clear criteria for when each architectural pattern should be
  used.
prerequisites:
- Read [What is an agent](01-what-is-an-agent.md).
- Read [The agent loop](02-the-agent-loop.md).
learning_objectives:
- Classify an AI system as a prompt chain, routing workflow, parallel pipeline, or
  autonomous agent.
- Select between workflows and agents based on predictability, latency, cost, and
  task ambiguity.
- Analyze the security and operational trade-offs of giving models control over execution
  paths.
source_records:
- p1-01-03-anthropic-workflows-agents-2024
- p1-01-03-langchain-workflows-agents-2024
- p1-01-03-google-adk-agents-2024
visual_assets:
- assets/images/01-agent-foundations/03-workflows-versus-agents/01-workflows-vs-agents-spectrum.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-15'
---
-->

# Workflows versus agents

## Why this matters

When building AI-powered applications, engineering teams face a fundamental architectural choice: should software code control the execution flow, or should the language model dynamically decide its own steps?

Choosing an autonomous agent when a predictable workflow suffices introduces unnecessary cost, latency, non-determinism, and expanded security attack surfaces. Conversely, forcing an open-ended, exploratory problem into a rigid workflow leads to fragile code that fails whenever user inputs deviate from pre-programmed assumptions. Understanding the precise boundary between workflows and agents enables engineers to build reliable, cost-effective, and defensible architectures.

## Simple mental model

Think of the difference between an automated train on tracks and a delivery driver on city streets.

An automated train follows a fixed track. The switches, stations, and sequence of stops are predetermined by the rail network infrastructure. Even if the train utilizes sophisticated sensors to adjust its speed, it cannot decide to take a detour down a side alley. This is a **workflow**: code defines the path, and model calls execute at fixed stations along the track.

A delivery driver navigates an open road network with a destination address. If a street is blocked by construction, the driver evaluates the surroundings, consults a map, chooses an alternate route, and navigates around the obstacle. This is an **agent**: the goal is specified by the system, but the vehicle's path is determined dynamically at runtime based on real-time observations.

## Position in the agent workflow

Use this comparison diagram to visualize the fundamental difference in control flow between deterministic workflows and autonomous agents.

![A side-by-side cartoon comparison diagram showing a deterministic workflow as a friendly train following fixed tracks and stations (1. Extract, 2. Validate, 3. Format) on the left, and an autonomous agent as a cute robot driving a small vehicle dynamically navigating paths with tools, goals, and feedback loops on the right.](../../assets/images/01-agent-foundations/03-workflows-versus-agents/01-workflows-vs-agents-spectrum.png)

*Figure 1. Architectural spectrum comparing deterministic workflows with autonomous agents. In a workflow, deterministic code strictly controls the sequential path; in an agent, the model dynamically directs tool choices and navigation based on environment feedback.*

As covered in [What is an agent](01-what-is-an-agent.md) and [The agent loop](02-the-agent-loop.md), workflows use language models as data-processing nodes inside traditional software control structures (like `if-else` branches and `for` loops). In contrast, agents use language models as the primary control flow router.

## How it works

### Structural comparison

| Dimension | Deterministic Workflow | Autonomous Agent |
| --- | --- | --- |
| Control Flow | Defined in application code (Python, TypeScript, DAGs) | Decided dynamically by the model at runtime |
| Predictability | High (same input triggers identical code paths) | Variable (model may choose different tools across runs) |
| Latency | Fixed and bounded (number of API calls is known upfront) | Variable (turns depend on environment feedback) |
| Error Recovery | Hardcoded retry policies and fallback branches | Model reasons over error messages and attempts alternatives |
| Security Attack Surface | Narrow (tools called only at designated, hardcoded steps) | Broad (model decides which tools to invoke with what parameters) |
| Ideal Problem Type | Well-structured, repeatable business processes | Exploratory, ambiguous, or multi-step discovery tasks |

### The decision criteria

To choose between a workflow and an agent, evaluate four key questions:
1. **Is the sequence of steps known in advance?** If yes, build a workflow. If the path depends on unpredictable intermediate findings, consider an agent.
2. **What is the acceptable tolerance for latency and cost?** If the system requires fast (sub-second) responses and bounded token usage, workflows are strictly superior.
3. **Is human auditing required before every state change?** Workflows make deterministic logging and auditing straightforward.
4. **Does the task require open-ended tool discovery?** If the model must search, test, and iterate across an unknown number of resources, an agent loop is necessary.

## Main variants

Industry architectures, such as those cataloged by [Anthropic (2024)](https://www.anthropic.com/research/building-effective-agents) and [LangChain (2024)](https://docs.langchain.com/oss/python/langgraph/workflows-agents), organize these systems into four primary patterns:

1. **Prompt Chaining (Workflow)**: A fixed linear pipeline where the structured output of step $N$ is validated and fed directly into step $N+1$.
2. **Routing (Workflow)**: A deterministic router or a lightweight classifier model classifies an incoming request and directs it to a specialized prompt or handler.
3. **Parallelization / Voting (Workflow)**: A task is split into multiple parallel sub-tasks (section-by-section processing) or multiple model instances vote to synthesize a consensus output.
4. **Autonomous Tool Loop (Agent)**: The model iteratively inspects environment feedback, emits tool calls, and evaluates when its goal is satisfied.

## Minimal implementation

The following Python code contrasts a deterministic workflow with an autonomous agent performing a document audit:

```python
from typing import Dict, List

# --- 1. Deterministic Workflow Pattern ---
def deterministic_audit_workflow(document: str, model_client) -> Dict[str, str]:
    """Fixed code path: Step 1 -> Step 2 -> Step 3. Code controls the flow."""
    # Step 1: Extract entities (Fixed Step)
    entities = model_client.call(f"Extract key entities from: {document}")

    # Step 2: Identify compliance issues (Fixed Step)
    issues = model_client.call(f"List compliance violations in: {document} with entities: {entities}")

    # Step 3: Format summary (Fixed Step)
    summary = model_client.call(f"Draft an executive report for issues: {issues}")

    return {"entities": entities, "issues": issues, "summary": summary}


# --- 2. Autonomous Agent Pattern ---
def autonomous_audit_agent(document_id: str, tools_env, model_client, max_turns: int = 5) -> str:
    """Dynamic path: Model decides which tools to call and when to stop."""
    history = [
        {"role": "system", "content": "Audit the document for compliance. Call tools as needed. Reply 'FINAL: <summary>' when done."},
        {"role": "user", "content": f"Audit document ID: {document_id}"}
    ]

    for turn in range(max_turns):
        decision = model_client.predict(history)
        if decision.startswith("FINAL:"):
            return decision.replace("FINAL:", "").strip()

        # Dynamic tool dispatch determined by model output
        tool_name, args = parse_tool_call(decision)
        observation = tools_env.execute(tool_name, args)
        history.append({"role": "assistant", "content": decision})
        history.append({"role": "user", "content": f"Observation: {observation}"})

    return "Audit incomplete: reached turn limit."

def parse_tool_call(decision: str):
    # Minimal placeholder parser for demonstration
    return "read_doc_section", {"section": "header"}
```

## Framework implementations

- **LangGraph**: Explicitly unifies workflows and agents under a single graph engine. Directed acyclic graphs (DAGs) represent deterministic workflows, while cyclical graphs with conditional edges represent dynamic agent loops.
- **Anthropic Guidance**: Recommends starting with the simplest deterministic workflow that solves the problem, adding agentic autonomy only when deterministic paths fail to handle input variance.
- **Google Agent Development Kit (ADK)**: Provides procedural workflow orchestrators alongside autonomous agent abstractions, allowing developers to nest agentic loops inside deterministic pipelines.

## Data flow and state changes

Compare how execution state transitions in a workflow versus an agent:

| Paradigm | State transition model | Control mechanism | Typical state payload |
| --- | --- | --- | --- |
| **Deterministic Workflow** | Linear Directed Acyclic Graph (DAG) | Application code routes state from Node A (Extract) to Node B (Validate) to Node C (Generate). | Structured schema passed between fixed pipeline functions. |
| **Autonomous Agent** | Cyclic State Machine | Model inspects accumulated history, selects Tool X, receives Observation, and repeats until goal satisfied. | Chronological context window containing user goal, past tool calls, and observations. |

## Trust boundaries

1. **Workflow Boundaries**: In a workflow, trust boundaries are enforced at compile time or in code structure. Each tool is called only by explicit code at designated steps with validated inputs.
2. **Agent Boundaries**: In an agent, the model has broad access to a suite of tools at every turn. The host runtime must enforce dynamic permissions, inspecting every individual tool request at runtime to verify authorization.

## Reliability failures

- **Workflow Failure Modes**: Workflows fail when encountering edge cases or input structures that were not anticipated by the human programmer, leading to unhandled exceptions or garbage outputs passed down the pipeline.
- **Agent Failure Modes**: Agents fail through reasoning breakdowns, hallucinating non-existent tool capabilities, thrashing in repetitive loops, or misinterpreting tool error codes as task completion.

## Worked example

Consider a customer support request: *"I was billed twice for my order last Tuesday."*

- **Workflow Approach**:
  1. A router model classifies the intent as `billing_duplicate_charge`.
  2. Code automatically calls `fetch_transactions(user_id, date="last Tuesday")`.
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

- **Workflows**: Offer superior speed, lower cost, deterministic guarantees, and straightforward unit testing. However, they lack the ability to adapt to novel situations without code updates.
- **Agents**: Excel at handling complex, messy, and open-ended problems requiring dynamic tool orchestration. However, they are non-deterministic, costlier, slower, and harder to secure.

## Security preview

Because autonomous agents possess runtime discretion over which tools to call, they introduce greater security exposure than deterministic workflows. An attacker exploiting an indirect prompt injection inside a workflow is constrained by the fixed pipeline steps. In an agent, that same injection can convince the model to invoke destructive tools that were never intended for that user request. We explore these attack paths in detail in [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security chapters.

## Open research questions

- How can hybrid systems automatically determine at runtime when a deterministic workflow should escalate a complex edge case to an autonomous agent?
- What evaluation benchmarks reliably quantify the reliability degradation when transitioning from fixed pipelines to model-directed loops?

## Key takeaways

- **Workflows** orchestrate LLMs through hardcoded code paths; **agents** allow LLMs to dynamically direct their own control flow and tool usage.
- Always prefer the simplest deterministic workflow that solves the problem; introduce agentic loops only when task ambiguity demands dynamic discovery.
- Workflows provide deterministic security and performance guarantees, whereas agents require continuous runtime guardrails and permission checks.

## References

- Anthropic. *Building Effective Agents*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Guide](https://www.anthropic.com/research/building-effective-agents).
- LangChain. *LangGraph: Workflows and Agents*. LangChain Documentation, 2024. [LangChain Reference](https://docs.langchain.com/oss/python/langgraph/workflows-agents).
- Google. *Google Agent Development Kit: Agents and Workflows*. Google ADK Documentation, 2024. [Google ADK](https://adk.dev/agents/).

---

[Next Unit: Goals, policies, environments, and autonomy →](04-goals-policies-environments-and-autonomy.md)
