<!--
---
title: Chunking, ranking, and advanced retrieval
unit_id: P1-03-06-03
summary: Explores advanced retrieval architectures beyond flat passage matching, including
  contextual chunking, cross-encoder neural reranking, hierarchical tree indexing
  with RAPTOR, and community-summarized knowledge graphs with GraphRAG.
prerequisites:
- Read [Sparse, dense, and hybrid retrieval](02-sparse-dense-and-hybrid-retrieval.md).
learning_objectives:
- Explain why traditional naive chunking causes context loss and how contextual chunking
  and parent-child hierarchies preserve document-level background.
- Implement two-stage retrieval pipelines combining fast bi-encoder first-stage prefetch
  with computationally intensive cross-encoder neural rerankers.
- Analyze recursive abstractive tree processing (RAPTOR) for multi-scale summarization
  and global theme extraction across large document collections.
- Contrast dense vector passage search with entity-relationship knowledge graph retrieval
  (GraphRAG) for global sensemaking and complex multi-hop queries.
source_records:
- p1-03-06-03-sarthi-raptor-2024
- p1-03-06-03-nogueira-monobert-2019
- p1-03-06-03-edge-graphrag-2024
- p1-03-06-03-anthropic-contextual-2024
visual_assets:
- assets/images/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/01-two-stage-retrieval-and-reranking-pipeline.png
- assets/images/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/02-hierarchical-and-graph-retrieval-structures.png
example_paths:
- examples/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/advanced_retrieval_runtime.py
pass: architecture
learning_path: deep-dive
status: complete
last_reviewed: '2026-09-13'
---
-->

# Chunking, ranking, and advanced retrieval

## Why this matters

Basic Retrieval-Augmented Generation (RAG) pipelines break documents into arbitrary text chunks and index them using approximate nearest neighbor vector similarity. While this flat approach works for simple factual lookups, production systems quickly run into fundamental structural barriers: context destruction, semantic distractor ranking, and the inability to answer global synthesis questions.

When documents are chopped into short passages, critical context vanishes. A chunk stating "the service revenue grew by 14%" becomes uninterpretable if the document title, fiscal quarter, and company name were located on a preceding page (Anthropic, 2024). Furthermore, vector similarity models frequently assign high scores to irrelevant passages that share superficial vocabulary while ranking genuinely authoritative paragraphs further down the list.

Answering complex questions requires architectures beyond flat passage matching. Advanced retrieval introduces contextual chunking to preserve background, two-stage pipelines with cross-encoder neural rerankers to eliminate distractors (Nogueira & Cho, 2019), recursive tree structures like RAPTOR to navigate different levels of abstraction (Sarthi et al., 2024), and entity-relationship knowledge graphs like GraphRAG to synthesize global corpus themes (Edge et al., 2024). Alongside [Memory](../05-memory/chapter-plan.md) and [Tools](../07-tools-and-function-calling/chapter-plan.md), these advanced retrieval structures allow agents to reason across thousands of interrelated documents without losing either granular precision or global perspective.

## Simple mental model

Think of a researcher investigating a complex corporate fraud case across twenty filing cabinets:

1. **Naive flat chunking (shredded pages):** The investigator cuts every report into two-paragraph strips and piles them into one giant box. One strip says "He approved the $5M wire transfer without board consent." The investigator has no idea who "he" was, which company transferred the money, or what year it happened.
2. **Contextual chunking (stamped index cards):** Before filing, the archivist stamps the top of every strip with its source metadata: `[Acme Corp 2023 Audit Report > Subsidiary Transfer Section]`. Every strip now retains its organizational identity regardless of where it is filed.
3. **Two-stage reranking (the intern and the senior partner):** An intern quickly scans the entire library and pulls the top 100 candidate folders (fast first-stage retrieval). Then, the senior partner carefully reads each of the 100 folders side by side with the specific legal brief, scoring each folder for actual evidentiary weight (thorough cross-encoder reranking).
4. **Hierarchical summaries (the executive briefing tree):** The archive organizes files into a pyramid. Individual transaction slips sit at the bottom, chapter summaries form the middle tier, and overarching annual executive briefs sit at the top. The researcher can zoom in for transaction receipts or zoom out for high-level corporate structure.

By stamping context on chunks, applying two-stage reranking, and building hierarchical trees, researchers navigate vast libraries without missing critical details or losing the overarching narrative.

## Position in the agent workflow

Advanced retrieval operates as the intelligence layer inside the RAG retrieval subsystem. Instead of executing a single vector search that feeds directly into the generator, the agent engine uses a multi-phase extraction and filtering pipeline.

When an agent query arrives, the system queries structured indexes (vector stores, hierarchical summary trees, or knowledge graphs). The resulting candidates are funneled through a high-precision cross-encoder reranker, ensuring that only the most contextually relevant, verified passages enter the agent context window.

![A two-stage retrieval architecture diagram traces a user query through Stage 1 bi-encoder vector prefetch yielding 100 candidates, followed by Stage 2 cross-encoder neural reranking using full joint cross-attention to output 5 refined passages to the agent context window.](../../../assets/images/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/01-two-stage-retrieval-and-reranking-pipeline.png)

*Figure 1. Two-stage retrieval pairs fast vector search over the entire corpus with compute-intensive cross-encoder reranking over candidate subsets to maximize retrieval precision.*

## How it works

Modern advanced retrieval pipelines combine four structural innovations: contextual chunking, cross-encoder reranking, recursive tree indexing, and graph-based community summarization.

### 1. Contextual chunking and parent-child relationships

In traditional naive chunking, documents are partitioned purely by token counts. This destroys pronoun references, section context, and organizational scope.

**Contextual retrieval** addresses this limitation by prepending a concise, document-level explanatory context to every chunk prior to vector embedding and BM25 indexing (Anthropic, 2024). During offline ingestion, a lightweight language model processes the whole document alongside the candidate chunk and generates a 50-to-100 token context string:

$$\text{Chunk}_{\text{contextual}} = [\text{Contextual Description}] \mathbin{\Vert} \text{Chunk}_{\text{raw}}$$

For example, a raw chunk reading *"Operating margins fell 3% due to higher server amortization"* is prepended with: *"[Source: Acme Corp Q3 2024 Form 10-Q > Segment Performance > Cloud Infrastructure]"*. This ensures that both dense embeddings and sparse BM25 tokens reflect the true origin and scope of the chunk, cutting retrieval failure rates by nearly half (Anthropic, 2024).

In **parent-child chunking**, documents are indexed at two granularities simultaneously: small child chunks (e.g., 200 tokens) are embedded for precise vector matching, but when a child chunk matches a query, the system retrieves its encompassing parent passage (e.g., 1000 tokens) or complete section for the agent prompt. This provides the generator with complete narrative coherence while preserving high retrieval sensitivity.

### 2. Two-stage retrieval and cross-encoder neural reranking

Vector databases use **bi-encoder** models where queries and documents are embedded into vectors independently ($E_Q(q)$ and $E_D(d)$). Because query and document tokens never interact directly in the neural network, bi-encoders miss complex token interactions, negation, syntactic dependencies, and fine-grained phrase ordering (Nogueira & Cho, 2019).

To resolve this without sacrificing speed, production architectures deploy a **two-stage retrieval pipeline**:

- **Stage 1 (Fast prefetch):** A bi-encoder or hybrid retriever scans millions of passages in milliseconds, returning a candidate pool (typically top-50 to top-100).
- **Stage 2 (Cross-encoder reranking):** A cross-encoder model evaluates the query and each candidate passage jointly. Both strings are concatenated and passed through transformer self-attention layers:

$$\text{Input} = \text{[CLS]} \circ q \circ \text{[SEP]} \circ d \circ \text{[SEP]}$$

$$\text{Score}_{\text{CrossEncoder}}(q, d) = \sigma\left(W \cdot \text{Transformer}(\text{Input})_{[\text{CLS}]}\right)$$

Because all tokens in the query attend to all tokens in the candidate passage across every transformer layer, the cross-encoder detects subtle nuances, negations, and exact terminology matches that vector similarity overlooked. The candidate pool is then resorted by cross-encoder score, and only the top 3 to 5 passages are injected into the agent prompt context.

### 3. Hierarchical tree retrieval (RAPTOR)

Standard RAG systems struggle with holistic questions such as *"What are the overarching themes of the 2024 engineering post-mortems?"* Answering this requires information scattered across dozens of individual incident reports.

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)** builds a multi-layer tree index through recursive clustering and summarization (Sarthi et al., 2024):

1. **Leaf indexing:** Raw text chunks form the leaf nodes of the tree.
2. **Semantic clustering:** Chunks with high embedding similarity are grouped into clusters using Gaussian Mixture Models (allowing chunks to belong to multiple clusters).
3. **Abstractive summarization:** A language model summarizes each cluster into a higher-level summary node.
4. **Recursive elevation:** The resulting summary nodes are clustered and summarized again, repeating until a root summary node covers the entire corpus.

During query execution, RAPTOR retrieves across all layers of the tree simultaneously (flattened tree search) or traverses from root summaries down to leaf details. This allows the agent to extract high-level thematic conclusions without reading every leaf passage individually.

![An educational diagram compares hierarchical tree retrieval (RAPTOR) using leaf chunks, clustered summaries, and multi-scale search against graph-based retrieval (GraphRAG) using entity nodes, relationship edges, and community summaries for global sensemaking.](../../../assets/images/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/02-hierarchical-and-graph-retrieval-structures.png)

*Figure 2. Hierarchical trees cluster text chunks into multi-scale summaries, while knowledge graphs map entities and relationships into community clusters to support global sensemaking.*

### 4. Graph-based retrieval and community summarization (GraphRAG)

While vector indices treat text as unstructured bags of tokens, many enterprise domains are inherently relational. **GraphRAG** combines knowledge graphs with language models to structure corpus information into an explicit network of entities and relationships (Edge et al., 2024):

1. **Entity and relationship extraction:** An LLM extracts named entities (people, systems, protocols, vulnerabilities) and directed claims ("Service A authenticates to Service B via mTLS") from each text chunk.
2. **Hierarchical community detection:** Graph algorithms (such as the Leiden algorithm) partition the entity network into modular communities of closely connected concepts at multiple levels of granularity.
3. **Community report generation:** The model precomputes detailed narrative summaries for each detected community.
4. **Global and local query routing:**
   - **Local search:** Answers entity-specific questions by finding neighboring nodes and extracting related incident claims.
   - **Global search:** Answers thematic, corpus-wide questions by aggregating community reports across the graph, generating partial summaries, and synthesizing a final response.

## Main variants

1. **Parent-child and contextual RAG:** Retains hierarchical document structure during chunking and embeds contextual headers to prevent semantic isolation (Anthropic, 2024).
2. **Late chunking:** Embeds the entire document through long-context transformer layers first, and pools token embeddings into chunk representations only at the final layer. This preserves bidirectional cross-chunk attention across passage boundaries.
3. **Two-stage cross-encoder rerankers:** Couples bi-encoder vector indices with cross-encoders (such as Cohere Rerank, BGE-Reranker, or ColBERT late interaction) to refine candidate relevance (Nogueira & Cho, 2019).
4. **Recursive summary trees (RAPTOR):** Clusters and summarizes chunks recursively to construct multi-scale indexes for both fine-grained facts and high-level themes (Sarthi et al., 2024).
5. **Knowledge graph augmented RAG (GraphRAG):** Extracts entities and claims into graph databases (e.g., Neo4j) and uses community detection for global sensemaking (Edge et al., 2024).

## Minimal implementation

The following Python snippet demonstrates two-stage retrieval: fast bi-encoder first-stage search followed by cross-encoder neural reranking with token alignment scoring. The [full runnable example](../../../examples/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/advanced_retrieval_runtime.py) demonstrates contextual chunking, cross-encoder scoring, and hierarchical summary retrieval.

<details>
<summary>Expand minimal Python implementation</summary>

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Passage:
    passage_id: str
    text: str
    vector: List[float]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2)) if len(v1) == len(v2) else 0.0

class TwoStageRetriever:
    def __init__(self, passages: List[Passage]) -> None:
        self.passages = passages

    def stage_1_prefetch(self, query_vec: List[float], top_k: int = 5) -> List[Tuple[Passage, float]]:
        # Fast bi-encoder approximate vector similarity
        scored = [(p, cosine_similarity(query_vec, p.vector)) for p in self.passages]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def stage_2_rerank(self, query: str, candidates: List[Tuple[Passage, float]], top_n: int = 2) -> List[Tuple[Passage, float]]:
        # Cross-encoder joint scoring over [Query; Passage]
        reranked = []
        q_tokens = set(query.lower().split())
        for passage, bi_score in candidates:
            p_tokens = set(passage.text.lower().split())
            token_overlap = len(q_tokens.intersection(p_tokens)) / max(len(q_tokens), 1)
            # Joint score combines bi-encoder semantic affinity with exact cross-attention token alignment
            cross_score = (0.6 * token_overlap) + (0.4 * bi_score)
            reranked.append((passage, cross_score))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_n]
```

</details>

Run [advanced_retrieval_runtime.py](../../../examples/03-building-blocks/06-retrieval-and-rag/03-chunking-ranking-and-advanced-retrieval/advanced_retrieval_runtime.py) to inspect contextual chunk prefixes, bi-encoder candidate pools, cross-encoder reranking, and RAPTOR summary node execution.

## Data flow and state changes

1. **Document ingestion & contextualization:** Documents are chunked into passages. Contextual prefixes or parent metadata are generated and attached to each chunk.
2. **Multi-scale indexing:** Chunks are embedded into vector indices. Concurrently, clusters are summarized into RAPTOR tree nodes or extracted into GraphRAG entity networks.
3. **Stage 1 candidate prefetch:** The incoming user query triggers a broad vector or hybrid search across the index, retrieving 50 to 100 candidate passages.
4. **Stage 2 cross-encoder scoring:** Candidate pairs are evaluated by the cross-encoder, calculating joint attention scores.
5. **Score thresholding & deduplication:** Candidates scoring below a minimum confidence threshold are discarded; near-duplicate passages are pruned.
6. **Prompt assembly:** The top-ranked passages (or higher-level community summaries) are formatted into the agent context window with source citations.

## Trust boundaries

- **Ingestion LLM extraction boundary:** Hierarchical summary trees (RAPTOR) and knowledge graphs (GraphRAG) rely on language models during indexing to summarize text and extract relationships. If an ingested document contains indirect prompt injection payloads, the indexing model could be hijacked during summarization, poisoning community summaries and downstream graph nodes.
- **Reranker boundary:** Cross-encoder models evaluate untrusted document passages directly alongside trusted user queries. Rerankers must output strictly numeric relevance scores and never execute or interpret instructions embedded within candidate text.
- **Access control propagation:** In hierarchical trees and knowledge graphs, community summaries blend information from multiple child chunks. If Child Chunk A is restricted to Admin users and Child Chunk B is public, the parent summary node must inherit the strictest access label (Admin only) to prevent unauthorized information leakage across tenant boundaries.

## Reliability failures

- **Contextual prefix hallucination:** When generating contextual prefixes for thousands of chunks, an automated ingestion LLM may hallucinate incorrect document titles, dates, or product versions, permanently indexing distorted metadata.
- **Cross-encoder computational bottleneck:** Cross-encoder latency scales linearly with candidate pool size ($O(K \cdot L^2)$ attention complexity). If the first-stage prefetch retrieves too many candidates, reranking latency can exceed interactive agent response deadlines.
- **Graph entity resolution fragmentation:** In GraphRAG, if the extraction model fails to resolve entity synonyms (e.g., treating "Postgres", "PostgreSQL", and "pg_database" as three separate entities), the resulting graph becomes fragmented, leading to failed relationship traversals.

## Limitations and trade-offs

- **Indexing cost and compute:** Building RAPTOR trees or GraphRAG entity graphs requires hundreds or thousands of LLM inference calls during ingestion, significantly increasing offline pipeline cost compared to simple vector embedding.
- **Query latency overhead:** Adding a cross-encoder reranking step adds 50 to 200 milliseconds of inference latency per query compared to direct vector lookups.
- **Index update complexity:** In flat vector databases, adding or deleting a document requires updating only that document vectors. In hierarchical trees and knowledge graphs, updating a document requires re-clustering, re-summarizing parent nodes, and updating graph edges.

## Security preview

In Pass 2, advanced retrieval systems are evaluated against **Graph Extraction Poisoning, Cross-Encoder Evasion Attacks, and Multi-Scale Context Injection**. Adversaries craft poisoned passages designed to manipulate hierarchical clustering algorithms, forcing malicious summaries to the root of RAPTOR trees or injecting false claims into GraphRAG communities. We analyze cryptographic provenance tracking, access-label inheritance, and isolated sanitization gates in [Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md).

## Open research questions

- How can hierarchical summary trees efficiently support streaming, real-time document updates without rebuilding entire tree clusters?
- Can late-interaction models (such as ColBERT) provide the full accuracy of cross-encoder reranking while retaining the sub-millisecond retrieval speeds of bi-encoder vector indices?

## Key takeaways

- Naive chunking destroys critical document context; contextual chunking prepends source and section background to preserve retrieval accuracy.
- Two-stage retrieval combines fast bi-encoder prefetch with deep cross-encoder neural reranking, eliminating false-positive distractors.
- RAPTOR builds recursive summary trees through semantic clustering, enabling agents to query both granular leaf details and high-level corpus themes.
- GraphRAG extracts entities, relationships, and community summaries, supporting global sensemaking across entire document collections.
- Hierarchical and graph indices increase offline ingestion cost and complexity, requiring strict access-control propagation across summary nodes.

## References

- Sarthi, P., Abdullah, S., Tuli, A., Khanna, S., Goldie, A., & Manning, C. D. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*. International Conference on Learning Representations (ICLR 2024). [arXiv:2401.18059](https://arxiv.org/abs/2401.18059).
- Nogueira, R., & Cho, K. (2019). *Passage Re-ranking with BERT*. arXiv preprint. [arXiv:1901.04085](https://arxiv.org/abs/1901.04085).
- Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Metropolitansky, D., Ness, R. O., & Larson, J. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research. [arXiv:2404.16130](https://arxiv.org/abs/2404.16130).
- Anthropic. (2024). *Contextual Retrieval: Improving RAG Accuracy with Contextual Embeddings and BM25*. Anthropic Research & Engineering. [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval).

---

[Next Unit: Grounding, long context, and retrieval evaluation →](04-grounding-long-context-and-retrieval-evaluation.md)
