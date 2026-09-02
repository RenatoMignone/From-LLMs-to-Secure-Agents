#!/usr/bin/env python3
"""Retrieval-Augmented Generation (RAG) Ingestion & Query Runtime.

Demonstrates:
1. Document loading and sliding-window chunking with metadata enrichment.
2. Dense vector embedding indexing with cosine similarity search.
3. Access-control metadata filtering during retrieval.
4. Grounded prompt assembly with inline document citation tags.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid


@dataclass
class DocumentChunk:
    chunk_id: str
    doc_id: str
    content: str
    source_url: str
    section_title: str
    access_level: str  # e.g., "public", "internal", "restricted"
    embedding: List[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def mock_embed_text(text: str, dim: int = 16) -> List[float]:
    """Generates a deterministic pseudo-dense embedding for demonstration purposes."""
    vec = [0.0] * dim
    words = text.lower().split()
    for w in words:
        h = hash(w) % dim
        vec[h] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    return sum(a * b for a, b in zip(v1, v2))


class VectorStore:
    """Manages document chunks and dense vector retrieval."""

    def __init__(self) -> None:
        self.chunks: Dict[str, DocumentChunk] = {}

    def add_document(
        self,
        doc_id: str,
        source_url: str,
        text: str,
        chunk_size: int = 200,
        chunk_overlap: int = 40,
        access_level: str = "internal",
    ) -> List[DocumentChunk]:
        """Splits raw document text into sliding chunks with metadata."""
        created_chunks: List[DocumentChunk] = []
        words = text.split()
        start = 0

        chunk_idx = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_text = " ".join(words[start:end])

            chunk = DocumentChunk(
                chunk_id=f"{doc_id}-chunk-{chunk_idx}",
                doc_id=doc_id,
                content=chunk_text,
                source_url=source_url,
                section_title=f"Section {chunk_idx + 1}",
                access_level=access_level,
                embedding=mock_embed_text(chunk_text),
            )
            self.chunks[chunk.chunk_id] = chunk
            created_chunks.append(chunk)

            chunk_idx += 1
            if end >= len(words):
                break
            start += max(1, chunk_size - chunk_overlap)

        return created_chunks

    def search(
        self,
        query: str,
        top_k: int = 2,
        user_access_tier: str = "internal",
    ) -> List[Tuple[DocumentChunk, float]]:
        """Performs dense vector similarity search with security metadata filtering."""
        q_vec = mock_embed_text(query)
        tier_hierarchy = {"public": 0, "internal": 1, "restricted": 2}
        max_user_level = tier_hierarchy.get(user_access_tier, 0)

        scored: List[Tuple[DocumentChunk, float]] = []
        for chunk in self.chunks.values():
            # Access control filtering
            chunk_level = tier_hierarchy.get(chunk.access_level, 0)
            if chunk_level > max_user_level:
                continue

            sim = cosine_similarity(q_vec, chunk.embedding)
            scored.append((chunk, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


def build_grounded_prompt(query: str, retrieved_chunks: List[Tuple[DocumentChunk, float]]) -> str:
    """Assembles context with explicit document index tags for citation verification."""
    sections = [
        "=== SYSTEM INSTRUCTIONS ===",
        "You are a factual enterprise assistant. Answer the user prompt strictly using the verified evidence below.",
        "Every factual claim must cite its source using bracketed numbers corresponding to the evidence documents [Doc N].",
        "\n=== RETRIEVED EVIDENCE ===",
    ]

    for idx, (chunk, score) in enumerate(retrieved_chunks, 1):
        sections.append(
            f"[Doc {idx}] (Source: {chunk.source_url}, Access: {chunk.access_level}, Score: {score:.3f})\n"
            f"{chunk.content}"
        )

    sections.append(f"\n=== USER QUERY ===\n{query}")
    return "\n\n".join(sections)


def run_demonstration() -> None:
    print("=" * 65)
    print("  Demonstration: RAG Dual-Pipeline Ingestion & Query Runtime")
    print("=" * 65)

    store = VectorStore()

    # 1. Document Ingestion Pipeline
    print("\n[+] Ingesting corpus documents...")

    doc1_text = (
        "Enterprise Authentication Policy: All backend microservices must enforce mutual TLS (mTLS) "
        "for internal service-to-service communication. API gateways must terminate client TLS 1.3 "
        "and validate JWT bearer tokens issued by the central identity provider."
    )
    store.add_document(
        doc_id="sec-auth-policy",
        source_url="https://wiki.acme.corp/sec/auth-v2",
        text=doc1_text,
        chunk_size=20,
        chunk_overlap=5,
        access_level="internal",
    )

    doc2_text = (
        "Database Architecture Guidelines: PostgreSQL 16 is the standard operational database. "
        "All analytical warehouse workloads must route queries to ClickHouse clusters. "
        "Connection pools must be configured with a maximum idle timeout of 30 seconds."
    )
    store.add_document(
        doc_id="eng-db-guidelines",
        source_url="https://wiki.acme.corp/eng/db-v1",
        text=doc2_text,
        chunk_size=20,
        chunk_overlap=5,
        access_level="internal",
    )

    print(f"[*] Total indexed chunks in Vector Store: {len(store.chunks)}")

    # 2. Query Pipeline
    query = "What encryption and authentication standards are required for microservices?"
    print(f"\n[-->] Executing search query: '{query}'")

    results = store.search(query, top_k=2, user_access_tier="internal")
    for chunk, score in results:
        print(f"  - Matched: {chunk.chunk_id} (Score: {score:.3f}, Source: {chunk.source_url})")

    # 3. Grounded Prompt Assembly
    print("\n[===] Assembled Grounded Prompt:\n")
    grounded_prompt = build_grounded_prompt(query, results)
    print(grounded_prompt)

    # 4. Simulated Grounded Output
    print("\n=== MODEL GENERATED RESPONSE (GROUNDED) ===")
    print(
        "Backend microservices must enforce mutual TLS (mTLS) for internal service communication [Doc 1]. "
        "Additionally, external client connections must use TLS 1.3 and valid JWT bearer tokens issued "
        "by the central identity provider [Doc 1]."
    )

    print("\n[✓] Demonstration completed successfully.")


if __name__ == "__main__":
    run_demonstration()
