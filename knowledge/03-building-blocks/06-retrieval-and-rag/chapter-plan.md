# Retrieval and Retrieval-Augmented Generation Plan

## Section purpose

Teach the complete retrieval pipeline and its major modern variants.

## Learning outcomes

Design ingestion, parsing, chunking, metadata, indexing, queries, retrieval, reranking, grounding, citations, freshness, and evaluation; compare vector, sparse, hybrid, graph, hierarchical, agentic, multimodal, and long-context approaches.

## Prerequisites

[Memory](../05-memory/chapter-plan.md) and context construction.

## Planned child chapters

1. `01-rag-system-and-ingestion.md`
2. `02-sparse-dense-and-hybrid-retrieval.md`
3. `03-chunking-metadata-reranking-and-grounding.md`
4. `04-graphrag-and-hierarchical-retrieval.md`
5. `05-agentic-and-multi-hop-rag.md`
6. `06-multimodal-rag.md`
7. `07-long-context-versus-retrieval.md`
8. `08-retrieval-and-answer-evaluation.md`

## Required concepts

Corpus, document, chunk, embedding, sparse index, dense index, hybrid fusion, reranker, knowledge graph, provenance, grounding, citation, recall, precision, faithfulness, freshness, and access filter.

## Concepts explicitly out of scope

Detailed data poisoning and exfiltration controls.

## Recommended teaching order

Build basic RAG end to end, compare retrieval families, add advanced structures and agentic control, then alternatives and evaluation.

## Required diagrams or visuals

Ingestion-query dual pipeline, retrieval taxonomy, GraphRAG map, and long-context trade-off chart.

## Recommended examples

A tiny local corpus with sparse, dense, and hybrid retrieval using mocked embeddings; plans only for graph and multimodal variants.

## Sources

Authoritative source categories: Foundational and peer-reviewed retrieval papers, official implementations, and benchmark research.

Candidate primary sources:

- [RAG](https://arxiv.org/abs/2005.11401)
- [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft GraphRAG publications](https://www.microsoft.com/en-us/research/project/graphrag/publications/)
- [RAPTOR](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html)
- [Agentic RAG survey](https://arxiv.org/abs/2501.09136)
- [Multimodal RAG benchmark](https://arxiv.org/abs/2411.02937)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)

## Connections to later security chapters

[Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md).

## Open questions

Treat GraphRAG and agentic RAG as families with varying definitions, and state the chosen taxonomy.

## Completion criteria

Every variant is positioned within the same ingestion, retrieval, generation, provenance, and evaluation model.
