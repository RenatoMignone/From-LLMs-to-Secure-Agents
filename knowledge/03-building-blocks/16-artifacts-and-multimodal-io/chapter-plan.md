# Artifacts and Multimodal Input and Output Plan

## Section purpose

Teach persistent outputs and non-text inputs as first-class workflow objects.

## Learning outcomes

Distinguish messages, events, state, and artifacts; handle files, structured data, images, audio, video, generated code, user-interface elements, streaming, storage, provenance, and lifecycle.

## Prerequisites

[Reliability and operations](../15-reliability-and-operations/chapter-plan.md), context, tools, and execution.

## Planned child chapters

Main path:

1. `01-messages-structured-artifacts-and-lifecycle.md`

Deep dive:

2. `02-multimodal-input-output-streaming-and-evaluation.md`

## Required concepts

Artifact, MIME type, schema, file reference, stream, modality, provenance, checksum, version, retention, and rendering.

## Concepts explicitly out of scope

Multimodal model training and detailed malicious-content analysis.

## Recommended teaching order

Define object types, add structured and file outputs, cover modalities and streams, then storage and evaluation.

## Required diagrams or visuals

Artifact lifecycle and multimodal data-flow diagram.

## Recommended examples

A typed artifact manifest with mocked file and image references; compare Google Agent Development Kit artifacts and A2A parts.

## Sources

Authoritative source categories: Official framework and protocol documentation plus multimodal benchmark research.

Candidate primary sources:

- [Google Agent Development Kit agents and artifacts](https://adk.dev/agents/)
- [A2A specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- [Multimodal RAG benchmark](https://arxiv.org/abs/2411.02937)

## Connections to later security chapters

[Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md) and [execution security](../../07-security-by-component-and-workflow-stage/04-execution-and-supply-chain/chapter-plan.md).

## Open questions

Which artifact metadata should be mandatory across all modalities?

## Completion criteria

Every artifact has type, owner, provenance, storage, lifecycle, rendering boundary, and evaluation method.
