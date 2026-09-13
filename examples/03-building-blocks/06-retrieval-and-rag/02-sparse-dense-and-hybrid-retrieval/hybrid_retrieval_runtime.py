#!/usr/bin/env python3
"""Sparse, Dense, and Hybrid Retrieval Runtime.

Demonstrates:
1. Sparse lexical retrieval using Okapi BM25 with inverted indexing.
2. Dense semantic retrieval using vector embeddings and cosine similarity.
3. Hybrid rank fusion using Reciprocal Rank Fusion (RRF) and score normalization.
4. Comparative retrieval experiments on exact identifiers versus semantic paraphrases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from typing import Dict, List, Set, Tuple


@dataclass
class Document:
    doc_id: str
    title: str
    content: str
    tokens: List[str] = field(default_factory=list)
    dense_vector: List[float] = field(default_factory=list)


def tokenize(text: str) -> List[str]:
    """Tokenize and normalize text to lowercase alphanumeric tokens."""
    return re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())


# ----------------------------------------------------------------------
# 1. Sparse Lexical Retriever (Okapi BM25)
# ----------------------------------------------------------------------

class BM25Retriever:
    """Inverted index implementing Okapi BM25 ranking."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.corpus: Dict[str, Document] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0
        self.inverted_index: Dict[str, Set[str]] = {}
        self.term_doc_freqs: Dict[str, Dict[str, int]] = {}

    def index(self, documents: List[Document]) -> None:
        total_len = 0
        for doc in documents:
            self.corpus[doc.doc_id] = doc
            doc.tokens = tokenize(doc.content)
            doc_len = len(doc.tokens)
            self.doc_lengths[doc.doc_id] = doc_len
            total_len += doc_len

            freqs: Dict[str, int] = {}
            for token in doc.tokens:
                freqs[token] = freqs.get(token, 0) + 1
                if token not in self.inverted_index:
                    self.inverted_index[token] = set()
                self.inverted_index[token].add(doc.doc_id)
            self.term_doc_freqs[doc.doc_id] = freqs

        self.avg_doc_len = total_len / max(len(documents), 1)

    def _idf(self, term: str) -> float:
        n = len(self.inverted_index.get(term, set()))
        N = len(self.corpus)
        if n == 0:
            return 0.0
        # Standard Lucene/Okapi smoothed IDF formula
        return math.log(1.0 + (N - n + 0.5) / (n + 0.5))

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        query_tokens = tokenize(query)
        scores: Dict[str, float] = {}

        for term in query_tokens:
            idf = self._idf(term)
            matching_docs = self.inverted_index.get(term, set())
            for doc_id in matching_docs:
                tf = self.term_doc_freqs[doc_id].get(term, 0)
                doc_len = self.doc_lengths[doc_id]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                term_score = idf * (numerator / denominator)
                scores[doc_id] = scores.get(doc_id, 0.0) + term_score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# ----------------------------------------------------------------------
# 2. Dense Semantic Retriever (Vector Similarity)
# ----------------------------------------------------------------------

# Domain vocabulary clusters for deterministic mock embeddings
CONCEPT_CLUSTERS = [
    {"error", "timeout", "gateway", "auth", "token", "failure", "code", "4039", "upstream"},
    {"service", "architecture", "microservice", "proxy", "resilient", "routing", "availability", "cloud"},
    {"database", "postgresql", "migration", "schema", "table", "alembic", "sql", "storage"},
    {"network", "latency", "socket", "connection", "diagnosing", "cluster", "packet", "drops"},
]


def mock_embed(text: str, dim: int = 8) -> List[float]:
    """Generates a deterministic vector capturing semantic topic weights."""
    tokens = set(tokenize(text))
    vec = [0.0] * dim
    for cluster_idx, cluster in enumerate(CONCEPT_CLUSTERS):
        overlap = len(tokens.intersection(cluster))
        if overlap > 0:
            vec[cluster_idx * 2] += float(overlap * 2.0)
            vec[cluster_idx * 2 + 1] += float(overlap * 1.5)

    # Add token hash dispersion for unique vocabulary
    for t in tokens:
        h = hash(t) % dim
        vec[h] += 0.2

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    return sum(a * b for a, b in zip(v1, v2))


class DenseRetriever:
    """Dense vector retriever using cosine similarity."""

    def __init__(self) -> None:
        self.corpus: Dict[str, Document] = {}

    def index(self, documents: List[Document]) -> None:
        for doc in documents:
            doc.dense_vector = mock_embed(doc.content)
            self.corpus[doc.doc_id] = doc

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        query_vec = mock_embed(query)
        scores: List[Tuple[str, float]] = []
        for doc_id, doc in self.corpus.items():
            sim = cosine_similarity(query_vec, doc.dense_vector)
            scores.append((doc_id, sim))

        ranked = sorted(scores, key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# ----------------------------------------------------------------------
# 3. Hybrid Fusion (Reciprocal Rank Fusion & Normalized Score Fusion)
# ----------------------------------------------------------------------

class HybridRetriever:
    """Combines sparse BM25 and dense vector retrieval."""

    def __init__(self, sparse: BM25Retriever, dense: DenseRetriever) -> None:
        self.sparse = sparse
        self.dense = dense

    def search_rrf(self, query: str, k_rrf: int = 60, top_k: int = 3) -> List[Tuple[str, float]]:
        """Reciprocal Rank Fusion: score(d) = sum_m 1 / (k_rrf + rank_m(d))."""
        sparse_hits = self.sparse.search(query, top_k=len(self.sparse.corpus))
        dense_hits = self.dense.search(query, top_k=len(self.dense.corpus))

        rrf_scores: Dict[str, float] = {}

        # Sparse contribution
        for rank_idx, (doc_id, _) in enumerate(sparse_hits, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + rank_idx))

        # Dense contribution
        for rank_idx, (doc_id, _) in enumerate(dense_hits, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + rank_idx))

        ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def search_score_fusion(
        self, query: str, sparse_weight: float = 0.5, dense_weight: float = 0.5, top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """Linear combination of min-max normalized scores."""
        sparse_hits = self.sparse.search(query, top_k=len(self.sparse.corpus))
        dense_hits = self.dense.search(query, top_k=len(self.dense.corpus))

        # Min-max normalize sparse scores
        norm_sparse: Dict[str, float] = {}
        if sparse_hits:
            max_s = max(s for _, s in sparse_hits)
            min_s = min(s for _, s in sparse_hits)
            denom = max_s - min_s if max_s > min_s else 1.0
            for doc_id, s in sparse_hits:
                norm_sparse[doc_id] = (s - min_s) / denom

        # Min-max normalize dense scores
        norm_dense: Dict[str, float] = {}
        if dense_hits:
            max_d = max(s for _, s in dense_hits)
            min_d = min(s for _, s in dense_hits)
            denom = max_d - min_d if max_d > min_d else 1.0
            for doc_id, s in dense_hits:
                norm_dense[doc_id] = (s - min_d) / denom

        all_doc_ids = set(norm_sparse.keys()) | set(norm_dense.keys())
        combined_scores: Dict[str, float] = {}
        for doc_id in all_doc_ids:
            s_val = norm_sparse.get(doc_id, 0.0)
            d_val = norm_dense.get(doc_id, 0.0)
            combined_scores[doc_id] = (sparse_weight * s_val) + (dense_weight * d_val)

        ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


# ----------------------------------------------------------------------
# 4. Demonstration Run
# ----------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 70)
    print("SPARSE, DENSE, AND HYBRID RETRIEVAL RUNTIME")
    print("=" * 70)

    # 1. Corpus Setup
    docs = [
        Document(
            doc_id="DOC-1",
            title="Gateway Incident Runbook",
            content="Error code ERR-4039: Gateway timeout occurs when upstream auth token expires.",
        ),
        Document(
            doc_id="DOC-2",
            title="Microservice Architecture Guide",
            content="High availability service design: resilient proxy routing and fault-tolerant microservices.",
        ),
        Document(
            doc_id="DOC-3",
            title="Database Migration Policy",
            content="PostgreSQL database schema updates using alembic migrations and version control.",
        ),
        Document(
            doc_id="DOC-4",
            title="Network Diagnostics Manual",
            content="Diagnosing socket connection drops, cluster latency, and packet loss in cloud networks.",
        ),
    ]

    sparse_retriever = BM25Retriever()
    sparse_retriever.index(docs)

    dense_retriever = DenseRetriever()
    dense_retriever.index(docs)

    hybrid_retriever = HybridRetriever(sparse_retriever, dense_retriever)

    print(f"\n[*] Indexed {len(docs)} documents into Sparse (BM25) and Dense vector indexes.")

    queries = [
        ("Exact Identifier Query", "ERR-4039 upstream auth"),
        ("Conceptual Paraphrase Query", "resilient cloud proxy routing and network delays"),
        ("Composite Hybrid Query", "ERR-4039 resilient proxy routing"),
    ]

    for label, query_text in queries:
        print("\n" + "-" * 70)
        print(f"Test Scenario: {label}")
        print(f"Query: \"{query_text}\"")
        print("-" * 70)

        sparse_results = sparse_retriever.search(query_text, top_k=2)
        print("\n[Sparse BM25 Top Results]")
        for doc_id, score in sparse_results:
            doc = sparse_retriever.corpus[doc_id]
            print(f"  {doc_id}: {doc.title} (BM25 score = {score:.4f})")

        dense_results = dense_retriever.search(query_text, top_k=2)
        print("\n[Dense Vector Top Results]")
        for doc_id, score in dense_results:
            doc = dense_retriever.corpus[doc_id]
            print(f"  {doc_id}: {doc.title} (Cosine similarity = {score:.4f})")

        rrf_results = hybrid_retriever.search_rrf(query_text, k_rrf=60, top_k=2)
        print("\n[Hybrid RRF Top Results]")
        for doc_id, score in rrf_results:
            doc = sparse_retriever.corpus[doc_id]
            print(f"  {doc_id}: {doc.title} (RRF score = {score:.6f})")

    print("\n" + "=" * 70)
    print("[✓] Demonstration completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    run_demonstration()
