# Agent-User Interaction Plan

## Section purpose

Complete the protocol map with the agent-to-user application boundary.

## Learning outcomes

The reader can design a bidirectional interface for long-running, streaming, interruptible agent work without exposing raw internal reasoning.

## Prerequisites

[Artifacts and multimodal input/output](../../03-building-blocks/16-artifacts-and-multimodal-io/chapter-plan.md), [human control](../../03-building-blocks/10-human-in-the-loop/chapter-plan.md), and [state](../../03-building-blocks/04-state-and-lifecycle/chapter-plan.md).

## Planned child chapters

1. `01-interface-events-steering-and-safe-rendering.md`

## Required concepts

Frontend, backend, bidirectional stream, event, state snapshot, state delta, progress, cancellation, interrupt, steering, frontend tool, typed component, and safe renderer.

## Recommended teaching order

Start with the application boundary, then add event streams and shared state before interactive control and generative interfaces.

## Concepts explicitly out of scope

Frontend framework tutorials, raw chain-of-thought display, and detailed interface security controls.

## Required diagrams or visuals

- Visual: agent, secure proxy, application, and user event flow.
- Example: a mocked stream with start, progress, approval, state update, and completion events.
- Framework examples: protocol-neutral first, then AG-UI translation.

## Recommended code and framework examples

Use typed events and a deterministic client reducer.

## Sources

Categories: official agent-interface protocol specifications, web event standards, and accessibility guidance.

Candidate primary sources:

- [AG-UI overview](https://docs.ag-ui.com/)
- [AG-UI core architecture](https://docs.ag-ui.com/concepts/architecture)
- [W3C Web Accessibility Initiative](https://www.w3.org/WAI/)

## Connections to later security chapters

Human-interface security revisits rendering, approval, state integrity, identity, and disclosure at this boundary.

## Open questions

Which agent-user event vocabulary will remain portable as generative-interface protocols evolve?

## Completion criteria

The end-to-end workflow can trace user input, progress, state, approval, artifacts, cancellation, and completion across the application boundary.
