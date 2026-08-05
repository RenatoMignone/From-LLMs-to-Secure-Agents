# Roadmap

This is the stable curriculum queue. Operational state belongs in `PROJECT_STATUS.md`; completed changes belong in `CHANGELOG.md`.

## Dependency rule

Units form one dependency chain in the order below. Every unit depends on the immediately preceding unit and on any additional prerequisites in its local `chapter-plan.md`. `P1-00-01` has no curriculum dependency. Pass 2 cannot start until every Pass 1 unit is complete.

## Unit completion criteria

A unit is complete when it meets its local plan, follows the correct chapter template, records checked sources, includes every required local visual and example, passes validation, updates README and project state, and receives no unresolved blocking review finding.

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

1. `P1-02-01` Architecture selection criteria
2. `P1-02-02` Single-agent and reactive loops
3. `P1-02-03` Sequential, routing, and parallel workflows
4. `P1-02-04` Plan and execute
5. `P1-02-05` Evaluator-optimizer and reflection
6. `P1-02-06` State machines and event-driven graphs
7. `P1-02-07` Supervisors, handoffs, and agent-as-tool
8. `P1-02-08` Architecture trade-offs

## Pass 1D1: Models and routing

1. `P1-03-01-01` Model roles and selection
2. `P1-03-01-02` Routing, cascades, and fallbacks
3. `P1-03-01-03` Capability, cost, latency, and reliability
4. `P1-03-01-04` Routing evaluation

## Pass 1D2: Context construction

1. `P1-03-02-01` Context sources and precedence
2. `P1-03-02-02` Context budgets, selection, and ordering
3. `P1-03-02-03` History, summaries, and compression
4. `P1-03-02-04` Provenance and context debugging

## Pass 1D3: Planning and reasoning

1. `P1-03-03-01` Reactive and reason-act patterns
2. `P1-03-03-02` Decomposition and plan-execute
3. `P1-03-03-03` Reflection, evaluation, and replanning
4. `P1-03-03-04` Search, budgets, and termination

## Pass 1D4: State and lifecycle

1. `P1-03-04-01` Run, thread, and event models
2. `P1-03-04-02` Checkpoints, interrupts, and resumption
3. `P1-03-04-03` Retries, idempotency, and concurrency
4. `P1-03-04-04` Termination, cancellation, and cleanup

## Pass 1D5: Memory

1. `P1-03-05-01` Memory versus context and state
2. `P1-03-05-02` Short-term and working memory
3. `P1-03-05-03` Persistent memory types and lifecycle
4. `P1-03-05-04` Consolidation, forgetting, and evaluation

## Pass 1D6: Retrieval and RAG

1. `P1-03-06-01` RAG system and ingestion
2. `P1-03-06-02` Sparse, dense, and hybrid retrieval
3. `P1-03-06-03` Chunking, metadata, reranking, and grounding
4. `P1-03-06-04` GraphRAG and hierarchical retrieval
5. `P1-03-06-05` Agentic and multi-hop RAG
6. `P1-03-06-06` Multimodal RAG
7. `P1-03-06-07` Long context versus retrieval
8. `P1-03-06-08` Retrieval and answer evaluation

## Pass 1D7: Tools and function calling

1. `P1-03-07-01` Tools, actions, and capabilities
2. `P1-03-07-02` Schemas, selection, and dispatch
3. `P1-03-07-03` Results, errors, parallelism, and retries
4. `P1-03-07-04` Side effects, idempotency, and confirmation
5. `P1-03-07-05` Tool discovery and large toolsets

## Pass 1D8: Identity, authorization, and secrets

1. `P1-03-08-01` Principals, identities, and authentication
2. `P1-03-08-02` Authorization policies and capabilities
3. `P1-03-08-03` Delegation, impersonation, and token exchange
4. `P1-03-08-04` Workload identity
5. `P1-03-08-05` Credentials, secrets, rotation, and revocation

## Pass 1D9: Execution environments

1. `P1-03-09-01` Execution boundaries and requirements
2. `P1-03-09-02` Process, container, and sandbox models
3. `P1-03-09-03` Virtual machines, browsers, and remote workers
4. `P1-03-09-04` Files, network, resources, and cleanup

## Pass 1D10: Human-in-the-loop

1. `P1-03-10-01` Human control patterns
2. `P1-03-10-02` Approval and escalation design
3. `P1-03-10-03` Pause, resume, timeouts, and rejection
4. `P1-03-10-04` Human feedback and operator experience

## Pass 1D11: Observability and tracing

1. `P1-03-11-01` Observability model and events
2. `P1-03-11-02` Traces, spans, and correlation
3. `P1-03-11-03` Metrics, cost, quality, and latency
4. `P1-03-11-04` Lineage, replay, redaction, and retention

## Pass 1D12: Evaluation and benchmarks

1. `P1-03-12-01` Evaluation levels and test design
2. `P1-03-12-02` Component and trajectory metrics
3. `P1-03-12-03` End-to-end task and reliability evaluation
4. `P1-03-12-04` Agent benchmarks and limitations
5. `P1-03-12-05` Regression and release evaluation

## Pass 1D13: Multi-agent systems

1. `P1-03-13-01` When and why multiple agents
2. `P1-03-13-02` Roles, delegation, and handoffs
3. `P1-03-13-03` Supervisors, teams, and peer coordination
4. `P1-03-13-04` Messages, shared state, and artifacts
5. `P1-03-13-05` Termination, failure, and evaluation

## Pass 1D14: Learning and self-improvement

1. `P1-03-14-01` Adaptation taxonomy
2. `P1-03-14-02` Reflection, feedback, and self-refinement
3. `P1-03-14-03` Experience, memory, and skill libraries
4. `P1-03-14-04` Prompt and policy optimization
5. `P1-03-14-05` Continual learning, weight updates, and forgetting
6. `P1-03-14-06` Evaluating improvement

## Pass 1D15: Reliability and operations

1. `P1-03-15-01` Service boundaries, queues, and workers
2. `P1-03-15-02` Timeouts, retries, backoff, and idempotency
3. `P1-03-15-03` Budgets, rate limits, and circuit breakers
4. `P1-03-15-04` Caching, versioning, deployment, and rollback
5. `P1-03-15-05` Service-level objectives and capacity

## Pass 1D16: Artifacts and multimodal input/output

1. `P1-03-16-01` Messages, events, and artifacts
2. `P1-03-16-02` Structured and file artifacts
3. `P1-03-16-03` Images, audio, video, and streaming
4. `P1-03-16-04` Artifact storage, provenance, and lifecycle
5. `P1-03-16-05` Multimodal workflow evaluation

## Pass 1E1: Frameworks

1. `P1-04-01-01` Comparison method and versioning
2. `P1-04-01-02` OpenAI Agents SDK
3. `P1-04-01-03` LangGraph
4. `P1-04-01-04` AutoGen
5. `P1-04-01-05` Semantic Kernel
6. `P1-04-01-06` Google Agent Development Kit
7. `P1-04-01-07` CrewAI and LlamaIndex
8. `P1-04-01-08` Cross-framework translation

## Pass 1E2: Model Context Protocol

1. `P1-04-02-01` Purpose, architecture, and lifecycle
2. `P1-04-02-02` Capabilities, tools, resources, and prompts
3. `P1-04-02-03` Transports, sessions, and versioning
4. `P1-04-02-04` Sampling, elicitation, and roots
5. `P1-04-02-05` Authorization and deployment models
6. `P1-04-02-06` Framework integration

## Pass 1E3: Agent-to-agent protocols

1. `P1-04-03-01` Agent-to-tool versus agent-to-agent
2. `P1-04-03-02` A2A data model and discovery
3. `P1-04-03-03` Task lifecycle, messages, and artifacts
4. `P1-04-03-04` Streaming, push, and long-running work
5. `P1-04-03-05` Bindings, identity, and interoperability
6. `P1-04-03-06` Protocol landscape and selection

## Pass 1F: End-to-end workflows

1. `P1-05-01` Workflow requirements and system boundary
2. `P1-05-02` Single-agent research and action workflow
3. `P1-05-03` Durable human-approved workflow
4. `P1-05-04` Multi-agent delegation workflow
5. `P1-05-05` Trace, replay, and functional evaluation

Pass 1 completes when the final workflow traces every functional component, data flow, state transition, authority change, tool action, human control, telemetry event, and termination path.

## Pass 2A: Threat model

1. `P2-06-01` System scope, assets, and security properties
2. `P2-06-02` Actors, identities, and trust boundaries
3. `P2-06-03` Attacker goals, capabilities, and access
4. `P2-06-04` Threat-modeling method
5. `P2-06-05` Agentic threat taxonomies and crosswalks
6. `P2-06-06` Reference workflow threat model

## Pass 2B1: Instructions, context, and models

1. `P2-07-01-01` Instruction hierarchy and prompt injection
2. `P2-07-01-02` Indirect injection and untrusted context
3. `P2-07-01-03` Goal, plan, routing, and output manipulation
4. `P2-07-01-04` Model abuse, leakage, and resource consumption
5. `P2-07-01-05` Controls, tests, and residual risk

## Pass 2B2: Retrieval, memory, and data

1. `P2-07-02-01` Ingestion, corpus, and index attacks
2. `P2-07-02-02` Retrieval manipulation and access control
3. `P2-07-02-03` Memory poisoning, persistence, and forgetting
4. `P2-07-02-04` Data privacy, provenance, and lifecycle
5. `P2-07-02-05` Controls, tests, and recovery

## Pass 2B3: Tools, identity, and credentials

1. `P2-07-03-01` Tool misuse, excessive agency, and parameters
2. `P2-07-03-02` Authentication, authorization, and policy enforcement
3. `P2-07-03-03` Delegation, confused deputy, and impersonation
4. `P2-07-03-04` Credentials, secrets, tokens, and revocation
5. `P2-07-03-05` Controls, tests, and recovery

## Pass 2B4: Execution and supply chain

1. `P2-07-04-01` Code, command, browser, and file attacks
2. `P2-07-04-02` Isolation, network, and resource boundaries
3. `P2-07-04-03` Tools, plugins, MCP servers, and dependencies
4. `P2-07-04-04` Artifacts, images, provenance, and updates
5. `P2-07-04-05` Controls, detection, recovery, and advisories

## Pass 2B5: Human interfaces and observability

1. `P2-07-05-01` Human trust, approval, and interface failures
2. `P2-07-05-02` Notifications, escalation, and takeover
3. `P2-07-05-03` Telemetry leakage, integrity, and retention
4. `P2-07-05-04` Detection, alerting, investigation, and replay
5. `P2-07-05-05` Controls, tests, and recovery

## Pass 2B6: Multi-agent systems and protocols

1. `P2-07-06-01` Agent identity, trust, and impersonation
2. `P2-07-06-02` Delegation, messages, shared state, and cascades
3. `P2-07-06-03` MCP trust, authorization, and server risk
4. `P2-07-06-04` A2A discovery, tasks, artifacts, and bindings
5. `P2-07-06-05` Controls, tests, recovery, and residual risk

## Pass 2B7: End-to-end attack paths

1. `P2-07-07-01` Attack-path method and workflow crosswalk
2. `P2-07-07-02` Retrieved instruction to unauthorized action
3. `P2-07-07-03` Memory poisoning to persistent control
4. `P2-07-07-04` Compromised tool or server to host impact
5. `P2-07-07-05` Cross-agent delegation and credential cascade
6. `P2-07-07-06` Containment, eradication, recovery, and lessons

## Pass 2C: Secure reference architectures

1. `P2-08-01` Reference architecture method
2. `P2-08-02` Read-only knowledge agent
3. `P2-08-03` Human-approved action agent
4. `P2-08-04` Sandboxed code and browser agent
5. `P2-08-05` Multi-agent and cross-domain system
6. `P2-08-06` High-assurance control plane
7. `P2-08-07` Recovery and incident-ready architecture

## Pass 2D: Security testing, evaluation, and assurance

1. `P2-09-01` Security properties and test oracles
2. `P2-09-02` Component and policy tests
3. `P2-09-03` Adversarial scenarios and red teaming
4. `P2-09-04` Agent security benchmarks
5. `P2-09-05` Control effectiveness and utility
6. `P2-09-06` Recovery, resilience, and chaos tests
7. `P2-09-07` Continuous assurance and release gates
8. `P2-09-08` Reporting, evidence, and limitations

## Pass 2E: Open research questions

1. `P2-10-01` Definitions, autonomy, and measurement
2. `P2-10-02` Robust planning, memory, and continual learning
3. `P2-10-03` Composable security and protocol trust
4. `P2-10-04` Evaluation validity and assurance limits
5. `P2-10-05` Human-agent and societal boundaries

Pass 2 completes when every Pass 1 component and workflow stage is covered by the threat model, mapped risks, preventive, detective, and recovery controls, secure designs, tests, and bounded assurance claims.
