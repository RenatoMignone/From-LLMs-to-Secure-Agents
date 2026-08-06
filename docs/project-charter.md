# Project Charter

## Goal

Create a complete two-pass learning path from agentic AI foundations to secure agentic AI systems.

## Reader contract

The reader already knows what a large language model is and has basic experience with prompts. Briefly refresh model behavior, context, or interfaces only when an agentic concept depends on them. API and Python experience is helpful, not required.

Keep the focus on agents. Do not add standalone deep coverage of model training, transformer internals, model history, prompt engineering, or large language model mathematics.

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

- an introduction to large language models;
- a transformer mathematics course;
- a prompt engineering guide;
- a guide to only one framework;
- a copy of OWASP taxonomies;
- a collection of unsupported claims;
- a checklist detached from architecture.
