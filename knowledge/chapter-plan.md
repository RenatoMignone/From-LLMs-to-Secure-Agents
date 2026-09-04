# Guide Plan

## Section purpose

Provide two strict learning passes: first understand the complete agentic system, then secure it.

## Learning outcomes

The reader can progress from agent foundations to complete system architecture, then apply a threat model, controls, secure designs, tests, and bounded assurance claims.

## Prerequisites

The reader has working familiarity with large language models and prompts. Brief model refreshers may appear only when required by an agentic topic. API and Python experience is helpful, not required.

## Planned child sections

### Pass 1

Follow [prerequisites](00-prerequisites/chapter-plan.md), [foundations](01-agent-foundations/chapter-plan.md), [architectures](02-agent-architectures/chapter-plan.md), [building blocks](03-building-blocks/chapter-plan.md), [frameworks and protocols](04-frameworks-and-protocols/chapter-plan.md), and [end-to-end workflows](05-end-to-end-workflows/chapter-plan.md).

Pass 1 completes only when the reader can trace data, state, authority, tools, execution, human control, telemetry, and termination through a full workflow.

### Pass 2

Follow the [threat model](06-threat-model/chapter-plan.md), [component and workflow security](07-security-by-component-and-workflow-stage/chapter-plan.md), [secure reference architectures](08-secure-reference-architectures/chapter-plan.md), [security assurance](09-security-testing-evaluation-and-assurance/chapter-plan.md), and [open questions](10-open-research-questions/chapter-plan.md).

Pass 2 revisits every Pass 1 component. It separates preventive, detective, and recovery controls and requires tests and residual-risk statements.

## Learning paths

The main path follows every top-level section and the chapters labeled "Main path" in nested plans. It teaches the minimum complete system, threat model, controls, reference designs, and assurance process.

Deep dives are optional branches for advanced retrieval variants, continual learning, framework implementation patterns, advanced multimodality, protocol details, generative interfaces, optimization, and open research. Their local plans identify exact chapters. They link back to a main-path entry point and may be skipped without breaking later core chapters. The generated site keeps these branches collapsed by default. Vendor-by-vendor, jurisdiction-by-jurisdiction, and sector-by-sector coverage is deferred unless it changes the stable architecture or security model.

## Required concepts

Agent loops, architectures, all runtime building blocks, policy enforcement, engineering lifecycle, user interfaces, frameworks, protocols, workflows, threats, controls, governance, secure lifecycle, reference architectures, evaluation, assurance, open questions, and current field vocabulary mapped to these stable concepts.

## Concepts explicitly out of scope

Large language model fundamentals beyond brief refreshers, transformer mathematics, prompt engineering, a single-framework tutorial, unsupported security checklists, and website implementation.

## Recommended teaching order

Follow the numbered directories and root `ROADMAP.md` without skipping prerequisites.

## Required diagrams or visuals

Maintain one system map through Pass 1 and reuse its component and workflow identifiers for threat, control, and assurance views in Pass 2.

## Recommended code and framework examples

Use the smallest useful form: prose walkthrough, table, visual, inline code, or pseudocode. Create a separate runnable artifact only when execution materially teaches or verifies behavior. Framework chapters such as LangGraph or Langfuse integrations are likely candidates; conceptual chapters often are not.

## Sources

Use official specifications and documentation, standards, official advisories, and primary research. Each child plan lists checked candidates that must be reopened before chapter use.

Candidate primary sources:

- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative)

## Connections to later security chapters

Every Pass 1 section links forward to the matching Pass 2 security section. Every Pass 2 section links back to the architecture it secures.

## Open questions

The reference workflow domain, protocol version churn, and cross-framework artifact metadata need later decisions.

## Completion criteria

All committed roadmap units are complete, the pass boundary remains intact, every architecture component has a security treatment, and all claims, necessary visuals, and examples meet project policy. Deferred topics do not block completion.

## Operating rule

Use root `ROADMAP.md` for unit order and `PROJECT_STATUS.md` for the next task. Do not write more than one unit per run unless explicitly requested.
