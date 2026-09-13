#!/usr/bin/env python3
"""Advanced Chunking, Reranking, and Hierarchical Retrieval Runtime.

Demonstrates:
1. Contextual Chunking: Prepending document-level context to isolated child chunks.
2. Two-Stage Retrieval: First-stage vector prefetch followed by cross-encoder neural reranking.
3. Hierarchical Tree Retrieval (RAPTOR style): Multi-layer clustering with leaf and summary nodes.
4. Comparative retrieval tests showing how reranking and hierarchical summaries filter distractors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    context_prefix: str = ""
    is_summary: bool = False
    parent_id: Optional[str] = None
    vector: List[float] = field(default_factory=list)

    @property
    def full_content(self) -> str:
        if self.context_prefix:
            return f"{self.context_prefix} {self.text}"
        return self.text


def tokenize(text: str) -> List[str]:
    return re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())


# ----------------------------------------------------------------------
# 1. Deterministic Semantic Embeddings (First-Stage Bi-Encoder)
# ----------------------------------------------------------------------

TOPIC_CLUSTERS = [
    {"security", "auth", "token", "encryption", "firewall", "tls", "keys", "vulnerability"},
    {"finance", "revenue", "quarterly", "growth", "margin", "ebitda", "fiscal", "expenses"},
    {"database", "sql", "migration", "query", "index", "postgres", "table", "schema"},
    {"infrastructure", "kubernetes", "pod", "container", "cluster", "deploy", "scaling"},
]


def mock_embed(text: str, dim: int = 8) -> List[float]:
    """Generates a normalized dense vector embedding based on semantic clusters."""
    tokens = set(tokenize(text))
    vec = [0.0] * dim
    for idx, cluster in enumerate(TOPIC_CLUSTERS):
        overlap = len(tokens.intersection(cluster))
        if overlap > 0:
            vec[idx * 2] += float(overlap * 2.5)
            vec[idx * 2 + 1] += float(overlap * 1.8)

    for t in tokens:
        h = hash(t) % dim
        vec[h] += 0.3

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    return sum(a * b for a, b in zip(v1, v2))


# ----------------------------------------------------------------------
# 2. Cross-Encoder Neural Reranker Simulation
# ----------------------------------------------------------------------

class CrossEncoderReranker:
    """Simulates a transformer cross-encoder that jointly processes [Query; Passage].

    Unlike bi-encoders which compute independent query and document vectors,
    cross-encoders compute full token-to-token cross-attention, assessing exact
    syntactic alignment, phrase order, and semantic relevance.
    """

    @staticmethod
    def score(query: str, passage: str) -> float:
        q_tokens = tokenize(query)
        p_tokens = tokenize(passage)
        if not q_tokens or not p_tokens:
            return 0.0

        q_set = set(q_tokens)
        p_set = set(p_tokens)
        overlap = q_set.intersection(p_set)

        # 1. Exact token coverage
        coverage_score = len(overlap) / len(q_set)

        # 2. Consecutive bigram match bonus (phrase order sensitivity)
        q_bigrams = {f"{q_tokens[i]}_{q_tokens[i+1]}" for i in range(len(q_tokens) - 1)}
        p_bigrams = {f"{p_tokens[i]}_{p_tokens[i+1]}" for i in range(len(p_tokens) - 1)}
        bigram_overlap = len(q_bigrams.intersection(p_bigrams))
        phrase_bonus = 0.3 * (bigram_overlap / max(len(q_bigrams), 1)) if q_bigrams else 0.0

        # 3. Dense semantic affinity between query and passage
        q_vec = mock_embed(query)
        p_vec = mock_embed(passage)
        dense_affinity = max(0.0, cosine_similarity(q_vec, p_vec))

        # Joint cross-encoder score combines exact alignment, phrase structure, and semantic affinity
        raw_score = (0.45 * coverage_score) + (0.25 * phrase_bonus) + (0.30 * dense_affinity)
        return min(1.0, max(0.0, raw_score))


# ----------------------------------------------------------------------
# 3. Hierarchical Tree Indexer (RAPTOR Style)
# ----------------------------------------------------------------------

class HierarchicalTreeIndex:
    """Organizes document chunks into a two-level hierarchy of leaf and summary nodes."""

    def __init__(self) -> None:
        self.leaf_chunks: Dict[str, Chunk] = {}
        self.summary_nodes: Dict[str, Chunk] = {}

    def build(self, documents: List[Tuple[str, str, List[str]]]) -> None:
        """Takes (doc_id, doc_title, list_of_raw_passages) and builds leaf + summary nodes."""
        for doc_id, doc_title, passages in documents:
            doc_leaf_ids: List[str] = []

            for idx, text in enumerate(passages):
                chunk_id = f"{doc_id}-c{idx+1}"
                # Contextual chunking: Prepending document title and section scope
                context_prefix = f"[Source: {doc_title}]"
                chunk = Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    text=text,
                    context_prefix=context_prefix,
                    is_summary=False,
                )
                chunk.vector = mock_embed(chunk.full_content)
                self.leaf_chunks[chunk_id] = chunk
                doc_leaf_ids.append(chunk_id)

            # Generate synthetic higher-level summary node (RAPTOR-style abstraction)
            summary_id = f"{doc_id}-summary"
            combined_summary_text = f"Overview of {doc_title}: Comprehensive analysis covering " + "; ".join(
                p[:60] for p in passages
            )
            summary_chunk = Chunk(
                chunk_id=summary_id,
                doc_id=doc_id,
                text=combined_summary_text,
                context_prefix=f"[Document Summary: {doc_title}]",
                is_summary=True,
            )
            summary_chunk.vector = mock_embed(summary_chunk.full_content)
            self.summary_nodes[summary_id] = summary_chunk

            for c_id in doc_leaf_ids:
                self.leaf_chunks[c_id].parent_id = summary_id

    def search_first_stage(self, query: str, top_k: int = 5, include_summaries: bool = False) -> List[Tuple[Chunk, float]]:
        """Stage 1: Fast approximate bi-encoder nearest-neighbor search."""
        q_vec = mock_embed(query)
        candidates: List[Chunk] = list(self.leaf_chunks.values())
        if include_summaries:
            candidates.extend(self.summary_nodes.values())

        scored = [(c, cosine_similarity(q_vec, c.vector)) for c in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def search_two_stage(self, query: str, first_stage_k: int = 5, final_k: int = 2) -> List[Tuple[Chunk, float, float]]:
        """Stage 1: Bi-encoder retrieval -> Stage 2: Cross-encoder reranking."""
        first_stage = self.search_first_stage(query, top_k=first_stage_k, include_summaries=False)
        reranked: List[Tuple[Chunk, float, float]] = []

        for chunk, bi_score in first_stage:
            cross_score = CrossEncoderReranker.score(query, chunk.full_content)
            reranked.append((chunk, bi_score, cross_score))

        # Sort strictly by Stage 2 Cross-Encoder score
        reranked.sort(key=lambda x: x[2], reverse=True)
        return reranked[:final_k]


# ----------------------------------------------------------------------
# 4. Demonstration Run
# ----------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 75)
    print("ADVANCED CHUNKING, RERANKING, AND HIERARCHICAL RETRIEVAL RUNTIME")
    print("=" * 75)

    raw_docs = [
        (
            "DOC-SEC",
            "Enterprise API Gateway Security Standard",
            [
                "Mutual TLS (mTLS) is strictly required for internal microservice communication.",
                "OAuth2 JWT access tokens must expire within 15 minutes and include role claims.",
                "Service accounts must rotate API keys every 90 days using automated vault secrets.",
            ],
        ),
        (
            "DOC-FIN",
            "ACME Corp Q2 2024 Financial Performance Report",
            [
                "Cloud infrastructure expenses rose by 14% due to model fine-tuning and GPU reservations.",
                "Subscription software revenue grew by 22% quarter-over-quarter across enterprise tiers.",
                "Gross profit margin remained steady at 68% despite increased datacenter investments.",
            ],
        ),
    ]

    index = HierarchicalTreeIndex()
    index.build(raw_docs)

    print(f"\n[*] Indexed {len(index.leaf_chunks)} leaf passages and {len(index.summary_nodes)} summary nodes.")
    print("\n--- Example Contextual Chunk Inspection ---")
    sample_chunk = list(index.leaf_chunks.values())[0]
    print(f"ID: {sample_chunk.chunk_id}")
    print(f"Isolated raw text: \"{sample_chunk.text}\"")
    print(f"Contextualized text: \"{sample_chunk.full_content}\"")

    # Test 1: Isolated Chunk Context Ambiguity
    print("\n" + "=" * 75)
    print("TEST 1: Two-Stage Reranking (Bi-Encoder vs Cross-Encoder)")
    query_1 = "How often must API keys be rotated for service accounts?"
    print(f"Query: \"{query_1}\"")

    print("\n[Stage 1: Bi-Encoder Top Candidates (Fast Semantic Embedding)]")
    stage_1_hits = index.search_first_stage(query_1, top_k=4)
    for c, score in stage_1_hits:
        print(f"  {c.chunk_id} [{score:.4f}]: {c.full_content[:70]}...")

    print("\n[Stage 2: Cross-Encoder Neural Reranking (Full Joint Cross-Attention)]")
    stage_2_hits = index.search_two_stage(query_1, first_stage_k=4, final_k=2)
    for c, bi_s, cross_s in stage_2_hits:
        print(f"  {c.chunk_id} [Cross-Encoder Score: {cross_s:.4f}, Bi-Encoder Score: {bi_s:.4f}]:")
        print(f"    Content: {c.full_content}")

    # Test 2: Global Holistic Query (RAPTOR Summary Retrieval)
    print("\n" + "=" * 75)
    print("TEST 2: Hierarchical Tree Retrieval for Global Sensemaking (RAPTOR)")
    query_2 = "Provide an executive summary of enterprise API gateway security"
    print(f"Query: \"{query_2}\"")

    print("\n[Retrieval with Hierarchical Summaries Included]")
    hierarchical_hits = index.search_first_stage(query_2, top_k=3, include_summaries=True)
    for c, score in hierarchical_hits:
        tag = "[SUMMARY NODE]" if c.is_summary else "[LEAF NODE]"
        print(f"  {c.chunk_id} {tag} [{score:.4f}]: {c.full_content[:90]}...")

    print("\n" + "=" * 75)
    print("[✓] Advanced retrieval demonstration completed successfully.")
    print("=" * 75)


if __name__ == "__main__":
    run_demonstration()
