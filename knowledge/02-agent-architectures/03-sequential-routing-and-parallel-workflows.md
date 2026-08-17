<!--
---
title: Sequential, routing, and parallel workflows
unit_id: P1-02-03
summary: Deep dive into deterministic workflow orchestration topologies including
  linear prompt chaining, conditional routing, parallel sectioning, and consensus
  voting, emphasizing error isolation and validation gates.
prerequisites:
- Read [Architecture selection criteria](01-architecture-selection-criteria.md).
- Read [Single-agent and reactive loops](02-single-agent-and-reactive-loops.md).
learning_objectives:
- Construct linear prompt chaining pipelines with structured intermediate validation
  checkpoints.
- Design classification-based routing workflows that steer requests to specialized
  handlers.
- Implement parallel sectioning (Map-Reduce) and consensus voting (Self-Consistency)
  workflows.
- Enforce error containment, dead-letter routing, and straggler timeout limits in
  workflow DAGs.
source_records:
- p1-02-03-anthropic-workflows-2024
- p1-02-03-langgraph-parallel-routing-2024
- p1-02-03-wang-self-consistency-2022
visual_assets:
- assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/01-workflow-patterns-topology.png
- assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/02-parallel-workflows-sectioning-vs-voting.png
- assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/03-workflow-isolation-and-validation-gates.png
example_paths: []
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-08-17'
---
-->

# Sequential, routing, and parallel workflows

## Why this matters

When enterprise systems integrate generative AI, deterministic reliability is often the primary engineering constraint. While autonomous agent loops provide great flexibility for open-ended research, they introduce non-deterministic execution paths, unbounded latencies, and complex failure modes. For the majority of production use cases, such as document processing, data extraction, and customer support triage, **deterministic workflows** provide superior performance, lower costs, and straightforward auditability.

Deterministic workflows maintain control flow entirely within application code. The language model acts as an intelligent data transformer at designated nodes rather than as the autonomous navigator of the entire execution path. Understanding how to compose prompt chains, conditional routers, and parallel pipelines allows engineers to construct high-throughput systems that scale reliably before integrating more dynamic [Building blocks](../03-building-blocks/chapter-plan.md).

## Simple mental model

Think of an industrial food manufacturing facility:

1. **Sequential Chaining (Assembly Line)**: Raw ingredients enter station 1 to be mixed, move to station 2 to be baked, and proceed to station 3 to be packaged. Each station performs a single transformation, and an optical sensor between stations rejects any misaligned item before it moves downstream.
2. **Routing (Sorting Chute)**: Packaged boxes arrive at a barcode scanner. Depending on whether the label indicates chilled dairy, fragile baked goods, or dry goods, a mechanical gate diverts the box onto a dedicated storage conveyor.
3. **Parallel Sectioning (Batch Packaging)**: A massive crate of 10,000 apples is split across ten identical packing stations operating concurrently. Each station packs 1,000 apples, and their combined pallets are loaded onto a single transport truck.
4. **Parallel Voting (Quality Panel)**: Three independent food safety inspectors evaluate a batch of specialty cheese. If at least two inspectors certify compliance, the batch is released for shipment.

In all four cases, the operational flow is governed by hardcoded machinery and strict schedules, ensuring predictable output quality and bounded delivery times.

## Position in the agent workflow

The visual below illustrates the three primary deterministic workflow topologies used in modern AI system design.

![A wide educational cartoon illustration showing three workflow topologies: Top shows Prompt Chaining with linear robot assembly stations; Middle shows Routing with a classifier robot directing requests to specialized paths; Bottom shows Parallelization with three worker robots fanning out and merging into an aggregator robot.](../../assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/01-workflow-patterns-topology.png)

*Figure 1. Core deterministic workflow topologies. Application code controls graph edges, ensuring bounded execution paths, fixed latency guarantees, and clear failure containment.*

As taught in [Agent foundations](../01-agent-foundations/chapter-plan.md) and [Architecture selection criteria](01-architecture-selection-criteria.md), these topologies represent the foundation of the Principle of Least Agency.

## How it works

Deterministic workflows organize language model calls as nodes in a Directed Acyclic Graph (DAG):

1. **Linear Prompt Chaining**: Breaks a complex multi-step prompt into discrete sub-tasks. Node A extracts structured facts from unstructured text; an application validator checks schema compliance; Node B translates or enhances the facts; and Node C generates the final formatted output.
2. **Classification & Routing**: Uses an embedding similarity lookup, regex pattern, or lightweight classifier model to assign an incoming request to a discrete category (e.g., `technical_support`, `billing_inquiry`, `cancellation`). Application code then routes the request to a purpose-built prompt and toolset tailored to that specific intent.
3. **Parallel Execution**: Executes multiple independent model invocations simultaneously via asynchronous runtimes or worker threadpools, aggregating results through deterministic reducers.

### Parallel sectioning vs consensus voting

Parallel workflows divide into two distinct operational patterns based on the problem objective:

The visual below contrasts parallel sectioning (Map-Reduce) with consensus voting (Self-Consistency):

![A wide educational cartoon comparison diagram showing two halves: Left half shows Sectioning (Map-Reduce) where a large document is split into 3 sections, processed by 3 worker robots, and merged by a combiner robot; Right half shows Consensus Voting where a single complex prompt is sent to 3 robots and a judge robot selects the majority answer.](../../assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/02-parallel-workflows-sectioning-vs-voting.png)

*Figure 2. Parallel workflow patterns. Sectioning accelerates throughput by partitioning massive inputs across workers, while consensus voting enhances reasoning reliability by sampling multiple generation paths.*

- **Sectioning (Map-Reduce)**: Applied when input data exceeds single-call context efficiency or requires partitioned processing (e.g., summarizing each chapter of a 300-page book in parallel).
- **Consensus Voting (Self-Consistency)**: Applied when solving difficult reasoning, mathematical, or classification tasks where a single generation path might suffer from hallucination (Wang et al., 2022). Generating three to five paths at higher temperature and selecting the majority answer significantly boosts accuracy.

## Main variants

1. **Fan-Out / Fan-In Pipelines**: One upstream node generates $N$ sub-queries, dispatches them concurrently across worker nodes, and collects their outputs at an aggregator node.
2. **Cascading Routers**: A hierarchical router where high-level intent is classified first (e.g., `engineering`), followed by a sub-router selecting the specific domain (e.g., `database_ops`).
3. **Speculative Execution Pipelines**: Running a fast small model and a comprehensive large model in parallel; if the small model's confidence exceeds a safety threshold, its output is returned immediately, cancelling the slower call.

## Minimal implementation

The following Python script demonstrates prompt chaining with validation checkpoints, conditional routing, and parallel consensus voting:

```python
from typing import Dict, Any, List
import concurrent.futures

class WorkflowModelClient:
    def call(self, prompt: str, temperature: float = 0.0) -> str:
        if "Classify" in prompt:
            return "LEGAL_INQUIRY"
        if "Extract" in prompt:
            return "PARTY_A: Acme Corp, JURISDICTION: Delaware"
        if "Translate" in prompt:
            return "PARTIE_A: Acme Corp, JURIDICTION: Delaware"
        if "Reason" in prompt:
            return "Risk Score: 15"
        return "Processed Output"

# 1. Prompt Chaining with Validation Checkpoint
def prompt_chain_pipeline(raw_contract: str, client: WorkflowModelClient) -> Dict[str, str]:
    # Step 1: Extraction
    entities = client.call(f"Extract key clauses: {raw_contract}")
    if "PARTY_A" not in entities:
        raise ValueError("Schema validation failed: Missing required PARTY_A entity.")

    # Step 2: Translation / Formatting
    translated = client.call(f"Translate clauses to French: {entities}")
    return {"extracted": entities, "translated": translated}

# 2. Conditional Routing Workflow
def routing_workflow(user_ticket: str, client: WorkflowModelClient) -> str:
    category = client.call(f"Classify intent: {user_ticket}").strip()
    if category == "LEGAL_INQUIRY":
        return client.call(f"Review contract risks for: {user_ticket}")
    elif category == "BILLING_INQUIRY":
        return client.call(f"Fetch payment history for: {user_ticket}")
    else:
        return "Routed to standard customer support queue."

# 3. Parallel Consensus Voting Workflow
def parallel_voting_workflow(complex_clause: str, client: WorkflowModelClient, num_voters: int = 3) -> str:
    prompts = [f"Reason over liability limit: {complex_clause}" for _ in range(num_voters)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_voters) as executor:
        votes = list(executor.map(lambda p: client.call(p, temperature=0.7), prompts))

    # Majority voting aggregation
    majority_vote = max(set(votes), key=votes.count)
    return majority_vote
```

## Framework implementations

- **LangGraph**: Represents workflows as stateful Directed Acyclic Graphs (DAGs) using typed state channels, conditional routing functions, and parallel fan-out branches that join at state reducer nodes.
- **Anthropic Guidance**: Highlights prompt chaining and routing as the two most reliable, cost-efficient patterns for production generative AI systems.
- **Google Agent Development Kit (ADK)**: Provides procedural pipelines that chain structured tool steps with deterministic schema validation between stages.

## Data flow and state changes

Trace the data flow through a parallel sectioning workflow:

| Pipeline Stage | State Transformation | Execution Mode | Error Handling Mechanism |
| --- | --- | --- | --- |
| **Ingestion** | Input document split into 3 chunks | Deterministic (Python code) | Chunk size boundary validation |
| **Fan-Out** | Chunk 1, Chunk 2, Chunk 3 processed | Asynchronous Parallel (3 LLM calls) | Per-worker timeout timer (3.0s) |
| **Validation** | Worker outputs checked against schema | Deterministic Checkpoint Gate | Divert invalid chunks to dead-letter queue |
| **Fan-In (Reduce)** | 3 partial summaries joined into final doc | Deterministic Aggregator (1 LLM call) | Fallback summary if 1 partition timed out |

## Trust boundaries

1. **Stage-to-Stage Isolation**: Each pipeline node operates on a scoped subset of data. Node A cannot arbitrarily access or modify memory held by Node C.
2. **Schema Validation Checkpoints**: Outputs generated by model nodes must be validated by code (e.g., regex, JSON Schema) before entering subsequent high-privilege processing stages.
3. **Dead-Letter Routing**: When an untrusted input causes a model node to emit malformed or unparsable data, the pipeline intercepts the error and routes the payload to a quarantined inspection queue without crashing the workflow.

## Reliability failures

The visual below illustrates how validation gates, error isolation, and dead-letter routing prevent pipeline crashes:

![A wide educational cartoon illustration showing a conveyor workflow with Step 1 Extract passing through a green Schema Validation Gate. Valid data continues to Step 2 Transform; Invalid data is diverted down a safety trapdoor to a Dead-Letter Queue with an inspector robot. A Timeout Guard protects parallel workers.](../../assets/images/02-agent-architectures/03-sequential-routing-and-parallel-workflows/03-workflow-isolation-and-validation-gates.png)

*Figure 3. Validation checkpoints, error isolation, and dead-letter routing in workflow pipelines. Faulty model outputs are intercepted and quarantined before affecting downstream nodes.*

- **Error Propagation in Linear Chains**: If Step 1 hallucinates an incorrect entity, Step 2 and Step 3 accept the error as ground truth and compound the mistake.
- **Misrouting at Decision Junctions**: If a classifier router miscategorizes a complex legal issue as a billing inquiry, the downstream specialized handler will produce irrelevant responses.
- **Straggler Latency in Parallel Fan-Out**: In a 10-way parallel sectioning pipeline, overall latency is determined by the single slowest model call (the straggler), necessitating per-node execution timeouts.

## Worked example

Consider an international shipping compliance workflow:
1. **Step 1 (Extraction Chain)**: Ingests an unstructured commercial invoice PDF. Node 1 extracts declared items, quantities, and destination country into a validated JSON schema.
2. **Step 2 (Router Junction)**: Router inspects destination country: `US` -> Path A (US Customs tariff lookup); `EU` -> Path B (TARIC duty code lookup).
3. **Step 3 (Parallel Sectioning)**: Path B splits 50 line items across 5 parallel worker calls (10 items each) to compute duty rates simultaneously.
4. **Step 4 (Aggregation)**: Combiner joins duty totals, verifies arithmetic deterministically in Python, and generates the final customs declaration.

## Limitations and trade-offs

- **Workflows vs Agent Loops**: Workflows cannot dynamically adapt to tasks where the exact number of required tool calls or exploration steps cannot be known at compile time.
- **Parallelization vs Token Cost**: Parallel consensus voting scales token consumption linearly ($N \times$ cost) and parallel sectioning increases API concurrency pressure.

## Security preview

Because deterministic workflows lock execution paths in software code, they offer a significantly smaller attack surface than autonomous agents. An attacker executing an indirect prompt injection within a workflow node cannot divert the overall control flow to call unauthorized tools. However, attackers can attempt **classification evasion** (tricking a router into choosing a low-security path) or **data poisoning** (injecting malicious data into intermediate state variables). We explore these workflow-specific threats in [threat modeling](../06-threat-model/chapter-plan.md) and Pass 2 security chapters.

## Open research questions

- How can workflow engines automatically synthesize optimal DAG topologies directly from natural language task specifications?
- What statistical thresholding techniques minimize the number of parallel voters needed to achieve targeted certainty levels in consensus pipelines?

## Key takeaways

- **Prompt chaining** decomposes complex tasks into discrete, verifiable transformations connected by schema validation gates.
- **Routing workflows** direct incoming requests to specialized prompts, tools, or pipelines using deterministic classifiers or lightweight models.
- **Parallel workflows** accelerate throughput via sectioning (Map-Reduce) or boost reasoning accuracy via consensus voting (Self-Consistency).
- Enforcing **validation gates**, **dead-letter queues**, and **per-node timeouts** is essential to prevent cascading errors and straggler latency in production pipelines.

## References

- Anthropic. *Building Effective Agents: Common Workflow Patterns*. Anthropic Research & Engineering Guidance, December 2024. [Anthropic Research](https://www.anthropic.com/research/building-effective-agents).
- LangChain. *LangGraph: Branching, Parallel Execution, and Map-Reduce*. LangChain Documentation, 2024. [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph/workflows-agents).
- Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. International Conference on Learning Representations (ICLR), 2023. [arXiv:2203.11171](https://arxiv.org/abs/2203.11171).

---

[Next Unit: Plan-and-execute →](04-plan-and-execute.md)
