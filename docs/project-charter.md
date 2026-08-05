# Project Charter

## Goal

Create a complete two-pass learning path from basic LLM applications to secure agentic AI systems.

The project explains:

- what an agent is;
- how agent loops work;
- how agents are designed and built;
- which frameworks and protocols are used;
- which components form an agentic system;
- how data, state, and authority move;
- which failures and attacks affect each stage;
- how controls reduce those risks;
- how controls can be tested.

## Learning passes

### Pass 1: Understand the complete agentic system

Teach agents, architectures, building blocks, frameworks, protocols, and one complete end-to-end workflow. Finish this pass before detailed security teaching begins.

Architecture chapters may include only a short security preview. The preview names why the component matters to security and links to its Pass 2 treatment. It must not explain attacks, controls, recovery, or security tests.

### Pass 2: Secure the system

First establish the threat model. Then revisit every component and workflow step to explain failures, attacks, preventive controls, detective controls, recovery controls, security tests, and secure reference architectures.

## Outputs

- sequential Markdown chapters;
- nested topic branches;
- diagrams and other visuals;
- runnable code examples;
- security labs;
- source citations;
- reproducible source and visual provenance records;
- a generated static website.

## Non-goals

This is not:

- a transformer mathematics course;
- a prompt engineering guide;
- a guide to only one framework;
- a copy of OWASP taxonomies;
- a collection of unsupported claims;
- a checklist detached from architecture.
