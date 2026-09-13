#!/usr/bin/env python3
"""Retrieval Evaluation, Grounding Verification, and Long-Context Trade-Off Runtime.

Demonstrates:
1. Standard Information Retrieval Metrics: Recall@K, Precision@K, MRR, and NDCG@K.
2. The RAG Triad Evaluator: Context Relevance, Groundedness (Faithfulness), and Answer Relevance.
3. Lost in the Middle Simulation: Simulating attention attenuation based on chunk position.
4. Grounded Citation Verification: Detecting unsupported hallucinated claims in generated answers.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Dict, List, Set, Tuple


# ----------------------------------------------------------------------
# 1. Classical Information Retrieval Metrics (BEIR Standard)
# ----------------------------------------------------------------------

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """Calculates Precision@K = (Relevant retrieved in top K) / K."""
    top_k = retrieved[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / len(top_k)


def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """Calculates Recall@K = (Relevant retrieved in top K) / (Total relevant)."""
    if not relevant:
        return 0.0
    top_k = retrieved[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / len(relevant)


def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """Calculates MRR = 1 / rank of the first relevant document."""
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: List[str], relevance_grades: Dict[str, float], k: int) -> float:
    """Calculates Normalized Discounted Cumulative Gain (NDCG@K)."""
    top_k = retrieved[:k]
    dcg = 0.0
    for idx, doc_id in enumerate(top_k, start=1):
        rel = relevance_grades.get(doc_id, 0.0)
        dcg += (math.pow(2.0, rel) - 1.0) / math.log2(idx + 1.0)

    # Calculate Ideal DCG (IDCG)
    ideal_ranks = sorted(relevance_grades.values(), reverse=True)[:k]
    idcg = 0.0
    for idx, rel in enumerate(ideal_ranks, start=1):
        idcg += (math.pow(2.0, rel) - 1.0) / math.log2(idx + 1.0)

    if idcg == 0.0:
        return 0.0
    return dcg / idcg


# ----------------------------------------------------------------------
# 2. The RAG Triad Evaluator (Ragas Style)
# ----------------------------------------------------------------------

def tokenize(text: str) -> Set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower()))


@dataclass
class RAGTriadResult:
    context_relevance: float
    faithfulness: float
    answer_relevance: float
    unsupported_claims: List[str]


class RAGTriadEvaluator:
    """Evaluates RAG generation across context relevance, faithfulness, and answer relevance."""

    @staticmethod
    def evaluate(
        query: str,
        retrieved_passages: List[str],
        generated_answer: str,
        claims: List[str],
    ) -> RAGTriadResult:
        q_tokens = tokenize(query)
        all_context_tokens: Set[str] = set()
        for p in retrieved_passages:
            all_context_tokens.update(tokenize(p))

        # 1. Context Relevance: Fraction of retrieved context tokens relevant to query
        total_overlap = len(q_tokens.intersection(all_context_tokens))
        context_relevance = total_overlap / max(len(q_tokens), 1)

        # 2. Faithfulness (Groundedness): Check each generated claim against retrieved context
        unsupported = []
        supported_count = 0
        for claim in claims:
            c_tokens = tokenize(claim)
            overlap = len(c_tokens.intersection(all_context_tokens))
            # Claim is deemed supported if at least 70% of its key terms exist in retrieved context
            coverage = overlap / max(len(c_tokens), 1)
            if coverage >= 0.70:
                supported_count += 1
            else:
                unsupported.append(claim)

        faithfulness = supported_count / max(len(claims), 1)

        # 3. Answer Relevance: Semantic overlap between generated answer and original query
        ans_tokens = tokenize(generated_answer)
        ans_overlap = len(q_tokens.intersection(ans_tokens))
        answer_relevance = ans_overlap / max(len(q_tokens), 1)

        return RAGTriadResult(
            context_relevance=min(1.0, context_relevance),
            faithfulness=faithfulness,
            answer_relevance=min(1.0, answer_relevance),
            unsupported_claims=unsupported,
        )


# ----------------------------------------------------------------------
# 3. Lost in the Middle Position-Bias Simulation
# ----------------------------------------------------------------------

def simulate_position_attention(total_documents: int, needle_position: int) -> float:
    """Models the U-shaped attention curve observed in 'Lost in the Middle' (Liu et al., 2023).

    Language models attend most strongly to items at the beginning (primacy effect)
    and end (recency effect) of long contexts, while attention drops in the middle.
    """
    if total_documents <= 1:
        return 1.0
    # Normalized position from 0.0 (very start) to 1.0 (very end)
    pos = needle_position / (total_documents - 1)
    # Quadratic curve with minimum at pos = 0.5
    # Value at 0.0 is 1.0, at 0.5 is 0.45, at 1.0 is 0.95
    attention = 1.0 - 2.2 * (pos * (1.0 - pos))
    return round(max(0.3, min(1.0, attention)), 3)


# ----------------------------------------------------------------------
# 4. Demonstration Run
# ----------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 75)
    print("RETRIEVAL EVALUATION & GROUNDING VERIFICATION RUNTIME")
    print("=" * 75)

    # 1. Classical Retrieval Metrics Evaluation
    print("\n--- 1. Evaluating Retrieval Ranking (BEIR Metrics) ---")
    retrieved_doc_ids = ["doc-4", "doc-1", "doc-8", "doc-2", "doc-9"]
    ground_truth_relevant = {"doc-1", "doc-2"}
    relevance_grades = {"doc-1": 3.0, "doc-2": 2.0, "doc-3": 1.0}

    p_at_3 = precision_at_k(retrieved_doc_ids, ground_truth_relevant, k=3)
    r_at_3 = recall_at_k(retrieved_doc_ids, ground_truth_relevant, k=3)
    mrr = mean_reciprocal_rank(retrieved_doc_ids, ground_truth_relevant)
    ndcg_5 = ndcg_at_k(retrieved_doc_ids, relevance_grades, k=5)

    print(f"Retrieved order: {retrieved_doc_ids}")
    print(f"Relevant set:    {list(ground_truth_relevant)}")
    print(f"Precision@3:     {p_at_3:.4f}")
    print(f"Recall@3:        {r_at_3:.4f}")
    print(f"MRR:             {mrr:.4f} (First hit at rank 2)")
    print(f"NDCG@5:          {ndcg_5:.4f}")

    # 2. RAG Triad Faithfulness & Grounding Check
    print("\n--- 2. Evaluating RAG Triad & Hallucination Detection ---")
    query = "What is the token expiration and TLS requirement for microservices?"
    passages = [
        "Internal microservice communication must strictly enforce mutual TLS (mTLS).",
        "OAuth2 access tokens have a maximum validity lifetime of 15 minutes.",
    ]

    claims_to_test = [
        "Internal microservice communication requires mutual TLS (mTLS).",
        "OAuth2 access tokens expire in 15 minutes.",
        "Database connections must use RSA 4096-bit client certificates.",  # Hallucinated!
    ]
    generated_answer = (
        "Internal microservice communication requires mutual TLS (mTLS) and OAuth2 tokens expire in 15 minutes. "
        "Additionally, database connections must use RSA 4096-bit client certificates."
    )

    eval_result = RAGTriadEvaluator.evaluate(query, passages, generated_answer, claims_to_test)
    print(f"Query: \"{query}\"")
    print(f"Context Relevance: {eval_result.context_relevance:.2f}")
    print(f"Answer Relevance:  {eval_result.answer_relevance:.2f}")
    print(f"Faithfulness:      {eval_result.faithfulness:.2f}")
    if eval_result.unsupported_claims:
        print(f"[!] Detected {len(eval_result.unsupported_claims)} unsupported hallucinated claim(s):")
        for c in eval_result.unsupported_claims:
            print(f"    - \"{c}\"")
    else:
        print("[✓] All claims are completely faithful to retrieved context.")

    # 3. Lost in the Middle Position Bias Simulation
    print("\n--- 3. Lost in the Middle Position Bias Simulation (10 Chunks) ---")
    total_docs = 10
    print("Position | Placement     | Simulated Model Attention")
    print("-" * 50)
    for pos, label in [(0, "Beginning (Top)"), (4, "Middle (Center)"), (9, "End (Bottom)")]:
        att = simulate_position_attention(total_docs, pos)
        bar = "█" * int(att * 20)
        print(f"   {pos:2d}    | {label:13s} | {att:.3f} [{bar:<20s}]")

    print("\n" + "=" * 75)
    print("[✓] Evaluation demonstration completed successfully.")
    print("=" * 75)


if __name__ == "__main__":
    run_demonstration()
