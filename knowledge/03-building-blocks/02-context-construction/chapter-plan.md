# Context Construction Plan

## Section purpose

Explain how the runtime assembles the bounded input seen by a model on each turn.

## Learning outcomes

Classify context sources, apply precedence and budgets, serialize messages and tool results, compress history, preserve provenance, and separate trusted instructions from untrusted data.

## Prerequisites

[Models and routing](../01-models-and-routing/chapter-plan.md).

## Planned child chapters

1. `01-context-sources-and-precedence.md`
2. `02-context-budgets-selection-and-ordering.md`
3. `03-history-summaries-and-compression.md`
4. `04-provenance-and-context-debugging.md`

## Required concepts

Context engineering as the runtime discipline for selecting and maintaining model-visible information; its difference from prompt engineering; system and developer instructions, user input, history, retrieved evidence, tool output, scratch data, token budgets, truncation, caching, and provenance.

## Concepts explicitly out of scope

Retrieval algorithms, persistent-memory design, and detailed prompt injection.

## Recommended teaching order

Inventory sources, define precedence, apply selection and ordering, manage overflow, then inspect the final context.

## Required diagrams or visuals

Context assembly pipeline and token-budget allocation diagram.

## Recommended examples

A pure context-builder function with source labels; compare framework context hooks.

## Sources

Authoritative source categories: Official runtime docs and primary long-context research.

Candidate primary sources:

- [OpenAI Agents SDK context management](https://openai.github.io/openai-agents-python/agents/)
- [Google Agent Development Kit context and sessions](https://adk.dev/agents/)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## Connections to later security chapters

[Instructions and context security](../../07-security-by-component-and-workflow-stage/01-instructions-context-and-models/chapter-plan.md).

## Open questions

Which provenance representation is portable across frameworks?

## Completion criteria

A reader can reconstruct exactly why each context item reached a model call.
