<!--
---
title: What is an agent
unit_id: P1-01-01
summary: Defines an agent as an autonomous software system combining a reasoning model
  with tools, environment observations, and goal-directed control loops.
prerequisites:
- Read [Prerequisites](../00-prerequisites/chapter-plan.md).
learning_objectives:
- Distinguish a standalone language model from a complete agent system.
- Identify the core components of an agent: model, environment, goal, policy, actions,
    and observations.
- Differentiate between rigid deterministic workflows and model-directed autonomous
  agent loops.
source_records:
- p1-01-01-russell-norvig-aima
- p1-01-01-yao-react-2022
- p1-01-01-anthropic-building-effective-agents-2024
visual_assets:
- assets/images/01-agent-foundations/01-what-is-an-agent/01-model-workflow-agent-comparison.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-15'
---
-->

# What is an agent

## Why this matters

In everyday conversations about artificial intelligence, the word "agent" is frequently applied to any chatbot, prompt template, or software script connected to a large language model. This loose labeling causes widespread confusion. A software team might build a simple two-step prompt pipeline and call it an agent, while another team builds an autonomous coding system that modifies hundreds of files, runs integration tests, and deploys cloud services. Treating these distinct architectures as identical makes it impossible to reason about system reliability, operational cost, or security risk.

A standalone language model is a stateless text processor. It takes an input sequence of tokens and predicts the most plausible continuation. On its own, the model cannot see the outside world, cannot browse the web, cannot execute commands on a server, and cannot verify whether its answers are accurate in a changing environment. To turn a predictive model into an effective problem solver, engineers build a surrounding software harness that equips the model with tools, supplies live feedback from external systems, and runs a control loop that drives toward a user's objective.

Tracing, designing, and securing modern AI systems requires a precise definition of what an agent is and where its boundaries lie. The [prerequisites](../00-prerequisites/chapter-plan.md) section established fundamental concepts of state, trust boundaries, delegation, and least privilege. This chapter introduces the structural components of an agent, distinguishing autonomous model-directed systems from static prompt calls and hardcoded workflows before exploring complex patterns in [agent architectures](../02-agent-architectures/chapter-plan.md).

## Simple mental model

Think of the difference between an advisor sitting in a locked room and a field technician operating on-site.

If you call the advisor on the phone and ask, "Why is the office heating system failing?", the advisor can only offer general suggestions based on past knowledge: "Perhaps the thermostat battery is dead, or the pressure valve is clogged." The advisor cannot inspect the heating unit, cannot test the circuit breaker, and cannot fix the problem.

In contrast, a field technician arrives at the facility with diagnostic equipment and tools. The technician reads the temperature gauge (perceiving the environment), decides to test the pressure valve (reasoning and choosing an action), turns a wrench to clear the valve (executing a tool action), and checks the gauge again to see if the pressure drops to normal (observing the result). The technician repeats this cycle until the heat returns to normal.

In this analogy:
- The **model** is the cognitive reasoning capability of the technician.
- The **tools** are the wrench, diagnostic meter, and valve keys.
- The **environment** is the physical building and the heating system.
- The **observations** are the gauge readings and error lights.
- The **agent** is the complete technician system: the entity that receives an objective, perceives the state of the world, decides on an intervention, executes tool actions, and observes feedback until the goal is achieved.

## Position in the agent workflow

Use this diagram to trace the architectural evolution from a simple model call to a deterministic workflow and an autonomous agent loop.

![A labeled side-by-side comparison diagram showing three AI system paradigms: a single-step standalone model call, a multi-step deterministic workflow with fixed code routing, and an autonomous agent loop featuring dynamic model decisions and environment feedback.](../../assets/images/01-agent-foundations/01-what-is-an-agent/01-model-workflow-agent-comparison.png)

*Figure 1. Architectural comparison across AI paradigms. Standalone model calls execute a single prompt-response step, deterministic workflows follow hardcoded paths, and autonomous agents dynamically select actions based on continuous environment feedback.*

Read the three paradigms from left to right:
1. **Standalone Model Call**: A single request passes into the model, which generates a single response. There is no feedback loop, no tool execution, and no interaction with external state.
2. **Deterministic Workflow**: Application code orchestrates fixed steps. The code dictates the sequence of model calls, data transformations, and API invocations. The model processes data at designated nodes, but the surrounding code controls the execution path.
3. **Autonomous Agent Loop**: The model serves as the runtime decision engine. The host runtime presents the model with an objective, available tools, and current environmental observations. The model determines which tool to invoke next, evaluates the observation returned by the environment, and decides dynamically whether to take another action or conclude the task.

## How it works

### Core components of an agent system

An agent is not a single algorithm or neural network. It is a composite software architecture consisting of seven interrelated components:

1. **Goal (Objective)**: The desired end state or task definition assigned to the agent (for example, "Find all customer accounts with expired subscriptions and generate renewal notices").
2. **Policy (Instructions and Guardrails)**: The governing rules, system prompts, operational constraints, and authority limits that define how the agent is permitted to pursue its goal.
3. **Model (Reasoning Engine)**: The core language model that interprets instructions, analyzes observations, generates intermediate reasoning steps, and selects tool invocations.
4. **Environment**: The external world or software context in which the agent operates, including operating systems, databases, web browsers, third-party APIs, and messaging systems.
5. **Actions (Tools and Actuators)**: The specific capabilities exposed to the agent by the host platform to query data, create files, execute code, or invoke external APIs.
6. **Observations (Sensors and Feedback)**: The structured responses, error messages, search results, and state updates returned to the agent host after executing an action in the environment.
7. **State and Memory**: The short-term context (the conversational history and working memory of the current run) and long-term memory (retrieval databases or key-value stores) that persist across execution turns.

### The perception-reasoning-action loop

Classical artificial intelligence literature, such as Russell and Norvig in [Artificial Intelligence: A Modern Approach (2020)](https://aima.cs.berkeley.edu/), defines an agent as an entity that perceives its environment through sensors and acts upon that environment through actuators toward a goal.

In language-model agents, this classical cycle is implemented through the ReAct framework, first formalized by Yao et al. in [ReAct: Synergizing Reasoning and Acting in Language Models (2022)](https://arxiv.org/abs/2210.03629). Instead of generating an entire plan in one ungrounded step, the model interleaves reasoning traces (thoughts) with concrete tool calls (actions), allowing it to inspect live data (observations) from the environment before choosing its next step.

| System paradigm | Who controls the execution path? | Does the system use environmental feedback? | Typical complexity and use case |
| --- | --- | --- | --- |
| Standalone Model Call | The human user (single prompt) | No feedback loop | Summarizing text, translating sentences, or drafting emails in one shot. |
| Deterministic Workflow | Hardcoded software code paths | Limited to pre-programmed conditional branches | Extracting structured data, running a fixed document classification pipeline. |
| Autonomous Agent | The language model dynamically at runtime | Continuous feedback from tool execution and environment state | Open-ended research, multi-file code refactoring, diagnostic troubleshooting. |

## Main variants

Modern applications use agentic concepts across several standard structural patterns:

- **Single-Turn Tool-Augmented Model**: The model receives a user question, emits a single tool call (such as a database query), receives the tool response, and outputs the final answer in a single round trip.
- **Sequential Prompt Chain**: A deterministic workflow where the output of one model call becomes the input to the next model call, following a fixed linear sequence.
- **Routing Workflow**: A deterministic classifier evaluates user input and routes the request to specialized prompts or tools based on fixed rules.
- **Autonomous Goal-Directed Agent**: A fully dynamic loop where the model selects arbitrary sequences of tools based on changing environment state until the goal is satisfied.
- **Multi-Agent Network**: Multiple specialized agents collaborate, delegate sub-goals to each other, and reconcile results through structured communication protocols.

## Minimal implementation

The following Python script illustrates the minimal mechanics of an agent loop without relying on third-party frameworks. The agent inspects an environment (a simulated file store), chooses actions, receives observations, and terminates when the objective is met or a step limit is reached.

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Environment:
    """A simulated environment representing a file repository."""
    files: Dict[str, str]

    def read_file(self, filename: str) -> str:
        if filename in self.files:
            return f"FILE CONTENT ({filename}): {self.files[filename]}"
        return f"ERROR: File '{filename}' not found."

    def list_files(self) -> str:
        return "FILES: " + ", ".join(self.files.keys())

class SimulatedModel:
    """Simulates a language model deciding actions based on prompt context."""
    def decide_next_step(self, prompt_history: List[str]) -> str:
        history_text = "\n".join(prompt_history)
        if "FILES:" not in history_text:
            return "ACTION: list_files"
        elif "notes.txt" in history_text and "FILE CONTENT (notes.txt)" not in history_text:
            return "ACTION: read_file notes.txt"
        else:
            return "FINISH: The secret project code in notes.txt is ATLAS-99."

def run_agent(goal: str, env: Environment, max_steps: int = 5) -> str:
    """Executes the perception-reasoning-action loop until completion or budget exhaustion."""
    history: List[str] = [f"GOAL: {goal}"]
    model = SimulatedModel()

    for step in range(1, max_steps + 1):
        # 1. Model evaluates history and decides the next action
        decision = model.decide_next_step(history)
        history.append(f"STEP {step} DECISION: {decision}")

        # 2. Check for task completion
        if decision.startswith("FINISH:"):
            return decision.replace("FINISH: ", "")

        # 3. Host executes the requested action in the environment
        if decision == "ACTION: list_files":
            observation = env.list_files()
        elif decision.startswith("ACTION: read_file "):
            target = decision.replace("ACTION: read_file ", "").strip()
            observation = env.read_file(target)
        else:
            observation = f"ERROR: Unknown action '{decision}'"

        # 4. Observation is fed back into the context for the next turn
        history.append(f"STEP {step} OBSERVATION: {observation}")

    return "ERROR: Step limit exceeded before goal completion."

# Execution demonstration
mock_env = Environment(files={"readme.md": "Project info", "notes.txt": "Project ATLAS-99 details"})
result = run_agent(goal="Find the secret project code", env=mock_env)
print("Agent Result:", result)
assert "ATLAS-99" in result
```

## Framework implementations

Industry frameworks standardize this separation between the reasoning model and the host execution harness:

- **Anthropic Building Effective Agents**: As detailed by Anthropic in [Building Effective Agents (2024)](https://www.anthropic.com/research/building-effective-agents), successful systems explicitly distinguish deterministic workflows (code-directed pipelines) from autonomous agents (model-directed loops), encouraging developers to build simple loops using standard APIs before adopting heavy abstractions.
- **OpenAI Agents SDK**: Encapsulates agent state, tool execution, handoffs between specialized agents, and structured guardrails into modular Python classes.
- **LangGraph**: Represents agent execution as a state graph where nodes perform computations or model calls, and edges determine transitions based on tool outputs or model decisions.
- **Google Agent Development Kit (ADK)**: Provides unified primitives for agent loops, tool declarations, memory persistence, and orchestration across multi-agent systems.

## Data flow and state changes

Follow how data flows through an agent during a single turn of the perception-action loop:

| Stage | Subsystem | Action | Data Payload |
| --- | --- | --- | --- |
| 1. Goal & Policy Input | User & Host | Operator supplies objective and constraints. | User prompt + system guardrails |
| 2. Context Assembly | Agent Host | Host compiles working memory and tool definitions into prompt. | Prompt context with chronological history |
| 3. Model Inference | Model Engine | Model reasons over context and emits tool request. | Structured action: `tool_call("search_docs", query="API keys")` |
| 4. Dispatch & Execution | Host Runtime | Intercepts call, checks permissions, and executes tool. | Invokes search tool across Trust Boundary |
| 5. Observation Feedback | Environment | Environment returns output data or error to host. | Observation: `{"result": "Rotate keys every 90 days"}` |
| 6. State Update | Agent Host | Appends action and observation to short-term history. | Updated conversation history array |
| 7. Decision Check | Model & Host | Evaluates goal completion status. | If incomplete, loops to Stage 3; if complete, outputs final answer. |

## Trust boundaries

An agent spans three distinct trust boundaries:

1. **User-to-Host Boundary**: The user submits goals, prompts, and constraints. The host system must authenticate the user, validate permissions, and set authority limits before initiating an agent run.
2. **Host-to-Model Boundary**: The host passes context into the language model and parses unstructured text or tool call declarations returned by the model. The host must validate that requested tool arguments match expected schemas.
3. **Host-to-Environment Boundary**: The host invokes external tools and APIs on behalf of the agent. The external environment must independently enforce authorization, verifying that the agent's delegation token permits the requested action.

## Reliability failures

Because agents dynamically direct their own control flow, they exhibit failure modes not found in deterministic software:

- **Infinite Action Loops**: The agent repeatedly takes the same unsuccessful action (such as searching the same query or opening the same file) without recognizing that it is making no progress.
- **Hallucinated Tool Invocations**: The model requests a tool name that does not exist or passes malformed parameters that fail type validation.
- **Premature Goal Completion**: The agent declares that a task is finished after performing only a fraction of the necessary steps, mistaking a partial result for total success.
- **Context Window Saturation**: Long-running loops accumulate large volumes of tool observations, exhausting the model's token limit and degrading reasoning performance.

## Worked example

Consider an agent tasked with resolving a customer refund request:

1. **Initial Goal**: User submits: *"Please refund transaction #TX-8821 for customer Alice Smith."*
2. **Step 1 (Perception & Action)**: The agent decides it must first inspect the transaction records. It calls `get_transaction(id="TX-8821")`.
3. **Step 1 (Observation)**: The billing environment returns: `{"id": "TX-8821", "customer": "Alice Smith", "amount": 49.00, "status": "settled", "days_ago": 12}`.
4. **Step 2 (Reasoning & Action)**: The agent consults its policy, which states that refunds under 50 dollars within 30 days are automatically permitted. It calls `issue_refund(id="TX-8821", amount=49.00, reason="Customer request")`.
5. **Step 2 (Observation)**: The billing API returns: `{"refund_id": "RF-301", "status": "success"}`.
6. **Step 3 (Conclusion)**: The agent evaluates that the goal has been fully met, appends the result to its context, and outputs the final response: *"Transaction #TX-8821 has been refunded in full ($49.00). Refund confirmation ID is RF-301."*

## Limitations and trade-offs

- **Latency and Cost**: Running multiple model inferences in a multi-turn loop consumes substantially more tokens and takes significantly longer than a single prompt call or deterministic script.
- **Non-Deterministic Execution**: Given the same initial goal, an agent may choose different sequences of tool calls across separate runs, complicating automated testing and debugging.
- **Compounding Errors**: If an early step produces an incorrect observation or misleading interpretation, subsequent reasoning steps may amplify the error rather than correct it.

## Security preview

Because autonomous agents possess agency (the ability to trigger state changes in external environments through tool calls), they introduce serious security challenges. When an agent processes untrusted external data (such as web pages, emails, or third-party documents), that data can contain malicious instructions that hijack the agent's reasoning loop. In [Threat model](../06-threat-model/chapter-plan.md) and subsequent security chapters, we analyze indirect prompt injection, tool misuse, and privilege escalation vulnerabilities that arise directly from model-directed control loops.

## Open research questions

- How can agent architectures reliably detect when a model is stuck in a repetitive reasoning loop without relying on arbitrary hardcoded step limits?
- What formal verification techniques can prove that an autonomous agent's dynamic execution paths will remain within defined safety invariants across unpredictable environments?

## Key takeaways

- A **model** is a predictive language processor; an **agent** is the complete goal-directed software system wrapping the model with tools, environment interfaces, and control loops.
- Agents operate via a **perception-reasoning-action loop**, interleaving model reasoning with live tool execution and environmental observations.
- In **deterministic workflows**, application code dictates the execution sequence; in **autonomous agents**, the language model dynamically decides control flow and tool usage at runtime.
- Multi-turn agent loops require explicit safeguards, including step limits, schema validation, and authorization boundaries, to prevent infinite loops and runaway execution.

## References

- Stuart Russell and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th Edition, Pearson, 2020. [AIMA](https://aima.cs.berkeley.edu/).
- Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. *ReAct: Synergizing Reasoning and Acting in Language Models*. International Conference on Learning Representations (ICLR), October 2022. [DOI: 10.48550/arXiv.2210.03629](https://doi.org/10.48550/arXiv.2210.03629).
- Anthropic. *Building Effective Agents*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Guide](https://www.anthropic.com/research/building-effective-agents).

---

[Next Unit: The agent loop →](02-the-agent-loop.md)
