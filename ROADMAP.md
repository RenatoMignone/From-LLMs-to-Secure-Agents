# Roadmap

This is the stable, reduced guide queue. Operational state belongs in `PROJECT_STATUS.md`; completed changes belong in `CHANGELOG.md`. The committed queue contains 99 source-grounded units. Further vendor, protocol, jurisdiction, sector, and research detail is deferred unless it materially improves the stable architecture or security model.

## Dependency rule

Units form one dependency chain in the order below. Every unit depends on the immediately preceding unit and on any additional prerequisites in its local `chapter-plan.md`. `P1-00-01` has no guide dependency. Pass 2 cannot start until every Pass 1 unit is complete.

The queue builds the main path and a small number of material deep dives. Reader-facing plans label optional deep dives, which may be skipped without losing a prerequisite needed later on the main path.

## Unit completion criteria

A unit is complete when it meets its roadmap scope and local plan, follows its chapter template, maps useful current terminology to stable concepts, records checked sources, includes necessary local visuals and examples, passes validation, receives a separate review, and updates project state and history. Update README only when public structure or navigation changes.

## Pass 1A: Prerequisites

1. `P1-00-01` Reader contract and system map
2. `P1-00-02` Data, control, and trust boundaries
3. `P1-00-03` Requests, events, state, and side effects
4. `P1-00-04` Identity, authority, and least privilege primer

## Pass 1B: Agent foundations

1. `P1-01-01` What is an agent
2. `P1-01-02` The agent loop
3. `P1-01-03` Workflows versus agents
4. `P1-01-04` Goals, policies, environments, and autonomy
5. `P1-01-05` Run lifecycle and termination

## Pass 1C: Agent architectures

Main path:

1. `P1-02-01` Architecture selection criteria
2. `P1-02-02` Single-agent and reactive loops
3. `P1-02-03` Sequential, routing, and parallel workflows

Deep dives:

4. `P1-02-04` Plan and execute
5. `P1-02-05` Evaluator-optimizer and reflection
6. `P1-02-06` State machines and event-driven graphs
7. `P1-02-07` Supervisors, handoffs, and agent-as-tool

Main path resumes:

8. `P1-02-08` Architecture trade-offs

## Pass 1D1: Models and routing

Main path:

1. `P1-03-01-01` Model roles and selection
2. `P1-03-01-02` Routing, cascades, and fallbacks

Deep dive:

3. `P1-03-01-03` Capability, cost, latency, and reliability

Main path resumes:

4. `P1-03-01-04` Routing evaluation

## Pass 1D2: Context construction

Main path:

1. `P1-03-02-01` Context sources and precedence
2. `P1-03-02-02` Context budgets, selection, and ordering

Deep dive:

3. `P1-03-02-03` History, summaries, and compression

Main path resumes:

4. `P1-03-02-04` Provenance and context debugging

## Pass 1D3: Planning and reasoning

Main path:

1. `P1-03-03-01` Reactive and reason-act patterns
2. `P1-03-03-02` Decomposition and plan-execute

Deep dives:

3. `P1-03-03-03` Reflection, evaluation, and replanning
4. `P1-03-03-04` Search, budgets, and termination

## Pass 1D4: State and lifecycle

Main path:

1. `P1-03-04-01` Run, thread, and event models
2. `P1-03-04-02` Checkpoints, interrupts, and resumption

Deep dive:

3. `P1-03-04-03` Retries, idempotency, and concurrency

Main path resumes:

4. `P1-03-04-04` Termination, cancellation, and cleanup

## Pass 1D5: Memory

1. `P1-03-05-01` Memory versus context and state
2. `P1-03-05-02` Short-term and working memory
3. `P1-03-05-03` Persistent memory types and lifecycle
4. `P1-03-05-04` Consolidation, forgetting, and evaluation

## Pass 1D6: Retrieval and RAG

Main path:

1. `P1-03-06-01` RAG system and ingestion
2. `P1-03-06-02` Sparse, dense, and hybrid retrieval

Deep dive:

3. `P1-03-06-03` Chunking, ranking, and advanced retrieval

Main path resumes:

4. `P1-03-06-04` Grounding, long context, and retrieval evaluation

## Pass 1D7: Tools and function calling

1. `P1-03-07-01` Tool capabilities, schemas, selection, and dispatch
2. `P1-03-07-02` Results, failures, side effects, and confirmation

## Pass 1D8: Identity, authorization, and secrets

1. `P1-03-08-01` Identity, authentication, authorization, and delegation
2. `P1-03-08-02` Workload identity, credentials, and revocation

## Pass 1D9: Execution environments

1. `P1-03-09-01` Execution boundaries, isolation, and sandboxes
2. `P1-03-09-02` Browsers, files, networks, resources, and cleanup

## Pass 1D10: Human-in-the-loop

1. `P1-03-10-01` Human control, approval, and escalation
2. `P1-03-10-02` Interrupts, steering, feedback, and operator experience

## Pass 1D11: Observability and tracing

Main path:

1. `P1-03-11-01` Events, traces, metrics, and correlation

Deep dive:

2. `P1-03-11-02` Lineage, replay, redaction, retention, and integrations

## Pass 1D12: Evaluation and benchmarks

Main path:

1. `P1-03-12-01` Evaluation levels, test design, and metrics

Deep dive:

2. `P1-03-12-02` Benchmarks, regression, and release evaluation

## Pass 1D13: Multi-agent systems

Main path:

1. `P1-03-13-01` Multi-agent roles, delegation, and coordination

Deep dive:

2. `P1-03-13-02` Shared state, failures, termination, and evaluation

## Pass 1D14: Learning and self-improvement

Main path:

1. `P1-03-14-01` Adaptation, reflection, feedback, and skills

Deep dive:

2. `P1-03-14-02` Optimization, continual learning, forgetting, and evaluation

## Pass 1D15: Reliability and operations

Main path:

1. `P1-03-15-01` Service boundaries, queues, retries, and budgets

Deep dive:

2. `P1-03-15-02` Caching, deployment, service objectives, and capacity

## Pass 1D16: Artifacts and multimodal input/output

Main path:

1. `P1-03-16-01` Messages, structured artifacts, and lifecycle

Deep dive:

2. `P1-03-16-02` Multimodal input, output, streaming, and evaluation

## Pass 1D17: Policy, guardrails, and validation

1. `P1-03-17-01` Policy control plane and input validation
2. `P1-03-17-02` Action, output, guardrail, and configuration validation

## Pass 1D18: Engineering lifecycle and deployment

1. `P1-03-18-01` Requirements, inventory, ownership, and environments
2. `P1-03-18-02` Deployment, change, rollback, and retirement

## Pass 1E1: Frameworks

Deep dives:

1. `P1-04-01-01` Framework comparison and versioning
2. `P1-04-01-02` Cross-framework translation and implementation

## Pass 1E2: Model Context Protocol

Deep dives:

1. `P1-04-02-01` Architecture, capabilities, transports, and lifecycle
2. `P1-04-02-02` Authorization, deployment, and extension features

## Pass 1E3: Agent-to-agent protocols

Deep dive:

1. `P1-04-03-01` Agent-to-agent architecture, lifecycle, and interoperability

## Pass 1E4: Agent-user interaction

1. `P1-04-04-01` Interface events, steering, and safe rendering

## Pass 1F: End-to-end workflows

1. `P1-05-01` Reference workflow requirements and system boundary
2. `P1-05-02` Durable research, action, delegation, and evaluation

Pass 1 completes when the final workflow traces every functional component, data flow, state transition, authority change, tool action, human control, telemetry event, and termination path.

## Pass 2A: Threat model

1. `P2-06-01` System scope, assets, properties, and trust boundaries
2. `P2-06-02` Attackers, baselines, and modeling methods
3. `P2-06-03` Agentic taxonomies and reference workflow threat model

## Pass 2B1: Instructions, context, and models

1. `P2-07-01-01` Instruction, context, and model attacks
2. `P2-07-01-02` Controls, tests, and residual risk

## Pass 2B2: Retrieval, memory, and data

1. `P2-07-02-01` Retrieval, memory, and data attacks
2. `P2-07-02-02` Controls, privacy, provenance, tests, and recovery

## Pass 2B3: Tools, identity, and credentials

1. `P2-07-03-01` Tool, identity, and credential attacks
2. `P2-07-03-02` Authorization, controls, tests, and recovery

## Pass 2B4: Execution and supply chain

1. `P2-07-04-01` Execution and supply-chain attacks
2. `P2-07-04-02` Isolation, provenance, detection, and recovery

## Pass 2B5: Human interfaces and observability

1. `P2-07-05-01` Human interface and observability failures
2. `P2-07-05-02` Controls, detection, investigation, and recovery

## Pass 2B6: Multi-agent systems and protocols

1. `P2-07-06-01` Multi-agent and protocol threats
2. `P2-07-06-02` Controls, tests, recovery, and residual risk

## Pass 2B7: End-to-end attack paths

1. `P2-07-07-01` Attack-path method and indirect-instruction scenario
2. `P2-07-07-02` Memory, tool, protocol, and credential cascades

## Pass 2B8: Governance and secure lifecycle

1. `P2-07-08-01` Governance, lifecycle, privacy, and accountability
2. `P2-07-08-02` Operations, incidents, evidence, and retirement

## Pass 2C: Secure reference architectures

Main path:

1. `P2-08-01` Method and read-only knowledge agent
2. `P2-08-02` Human-approved action and sandboxed execution

Deep dive:

3. `P2-08-03` Multi-agent, high-assurance, and recovery

## Pass 2D: Security testing, evaluation, and assurance

1. `P2-09-01` Security properties, oracles, and component tests
2. `P2-09-02` Adversarial benchmarks and control effectiveness
3. `P2-09-03` Recovery, continuous assurance, and reporting

## Pass 2E: Open research questions

This closing unit is an optional deep dive and does not introduce a prerequisite for the core guide.

1. `P2-10-01` Open research map

Pass 2 completes when every Pass 1 component and workflow stage is covered by the threat model, mapped risks, preventive, detective, and recovery controls, secure designs, tests, and bounded assurance claims.
