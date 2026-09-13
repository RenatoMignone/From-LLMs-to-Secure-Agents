<!--
---
title: Grounding, long context, and retrieval evaluation
unit_id: P1-03-06-04
summary: Analyzes context grounding, verifiable citations, the architectural trade-offs
  between massive context windows and focused RAG retrieval, and quantitative evaluation
  frameworks for retrieval precision and answer faithfulness.
prerequisites:
- Read [Chunking, ranking, and advanced retrieval](03-chunking-ranking-and-advanced-retrieval.md).
learning_objectives:
- Evaluate the architectural trade-offs between long-context foundation models and
  focused retrieval pipelines across latency, inference cost, and position-dependent
  attention degradation.
- Explain the 'Lost in the Middle' effect and analyze how context rot and distractor
  interference degrade reasoning over long prompt contexts.
- Apply classical information retrieval metrics (Recall@K, Precision@K, MRR, and NDCG@K)
  to measure candidate ranking performance.
- Implement reference-free RAG Triad evaluations measuring context relevance, groundedness
  (faithfulness), and answer relevance to detect parametric hallucinations.
source_records:
- p1-03-06-04-liu-lost-middle-2023
- p1-03-06-04-es-ragas-2023
- p1-03-06-04-gemini-long-context-2024
- p1-03-06-04-thakur-beir-2021
visual_assets: []
example_paths:
- examples/03-building-blocks/06-retrieval-and-rag/04-grounding-long-context-and-retrieval-evaluation/retrieval_evaluation_runtime.py
pass: architecture
learning_path: main
status: complete
last_reviewed: '2026-09-13'
---
-->

# Grounding, long context, and retrieval evaluation

## Why this matters

The rapid expansion of foundation model context windows (reaching one to two million tokens) has prompted a common architectural question: why maintain complex ingestion, chunking, and retrieval pipelines when an entire repository or document archive can be dumped directly into a prompt?

While long-context models excel at single-turn multi-document analysis and needle-in-a-haystack retrieval (Gemini Team, 2024), relying entirely on massive prompts introduces severe operational and cognitive penalties. Processing hundreds of thousands of prompt tokens incurs substantial time-to-first-token latency, compounds financial costs on every interaction, and suffers from **position-dependent attention degradation** ("Lost in the Middle"), where models reliably recall information placed at the start or end of the context but overlook facts placed in the middle (Liu et al., 2023).

Furthermore, without continuous measurement, retrieval systems silently degrade. A system might report high API success rates while returning irrelevant documents or generating convincing hallucinations that cite phantom sources. Ensuring that agent actions remain reliable requires a rigorous evaluation framework: measuring both **retrieval quality** (whether the right evidence was found) and **generation faithfulness** (whether claims are verifiably grounded in retrieved text) (Es et al., 2023; Thakur et al., 2021). Alongside [Memory](../05-memory/chapter-plan.md) and [Tools](../07-tools-and-function-calling/chapter-plan.md), grounding and continuous evaluation transform experimental prototypes into dependable enterprise agent systems.

## Simple mental model

Think of an attorney preparing for an urgent courtroom hearing:

1. **The dump truck approach (long context):** An assistant dumps forty cardboard boxes containing 50,000 unorganized loose papers onto the courtroom table. The attorney has access to everything, but finding a single contract clause takes minutes, and reading through irrelevant depositions causes fatigue, increasing the likelihood of missing crucial evidence buried in box twenty-four.
2. **The curated briefing binder (focused RAG retrieval):** A skilled paralegal searches the firm archives, extracts the exact three pertinent contracts, highlights the relevant paragraphs, and places a five-page indexed binder on the attorney desk. The attorney answers the judge immediately with precise citations.
3. **The independent fact-checker (RAG evaluation):** Before the attorney speaks, a second paralegal verifies every claim in the brief: Did we pull the right contracts? Does the contract actually say what we claim it says? Does our argument directly answer the judge question?

Long context provides an expansive workspace, but focused retrieval and continuous verification ensure that agents act on sharp, accurate, and cost-effective evidence.

## Position in the agent workflow

Grounding and retrieval evaluation operate at the boundary between external knowledge retrieval and downstream agent reasoning. Once the retrieval engine extracts candidate passages, the grounding layer formats them into structured context containers with tamper-evident metadata tags.

During and after execution, automated evaluators inspect the interaction trace across three distinct checkpoints: evaluating the search query against retrieved passages (retrieval recall and context precision), evaluating retrieved passages against the generated completion (groundedness and faithfulness), and evaluating the generated answer against the user goal (task relevance).

## How it works

A production grounding subsystem balances the architectural trade-offs between long-context processing and focused retrieval, while implementing systematic quantitative evaluations across the entire RAG pipeline.

### 1. Long-context versus focused retrieval trade-offs

Modern foundation models support context windows exceeding one million tokens (Gemini Team, 2024). However, choosing between long-context brute-force prompting and focused Retrieval-Augmented Generation (RAG) involves distinct trade-offs:

- **Inference latency:** In standard transformer architectures, self-attention scales quadratically or chunk-wise linearly with sequence length. Processing a 500,000-token prompt requires multiple seconds before the model generates its first output token, making it unsuitable for real-time conversational agents. In contrast, querying an indexed vector database takes 10 to 50 milliseconds, and generating against a 2,000-token context begins in milliseconds.
- **Cost compounding:** In interactive agent loops where the agent takes dozens of consecutive tool steps, resending a massive 500,000-token document history on every turn results in unsustainable token costs unless aggressive prompt caching is supported and cache hits remain uninterrupted.
- **Lost in the Middle and context rot:** Empirical studies demonstrate that language model retrieval accuracy follows a U-shaped curve: accuracy is highest when relevant information appears at the beginning (primacy effect) or end (recency effect) of the context window, and drops significantly when the evidence resides in the middle (Liu et al., 2023). Flooding the prompt with thousands of distractor passages degrades reasoning precision even when models achieve high scores on synthetic needle-in-a-haystack benchmarks.

| Dimension | Massive long-context window (1M+ tokens) | Focused RAG retrieval (Top-K passages) |
| --- | --- | --- |
| **Setup complexity** | Minimal (paste documents into prompt) | Moderate (ingestion, chunking, indexing, fusion) |
| **Query latency** | High (several seconds time-to-first-token) | Low (sub-second retrieval and generation) |
| **Token cost** | High per query (unless heavily cached) | Low per query (only top passages sent) |
| **Contextual degradation** | Susceptible to "Lost in the Middle" and distractors | High focus; minimal irrelevant noise |
| **Freshness** | Must re-upload documents to update | Real-time index updates without altering prompts |
| **Global sensemaking** | Strong for single documents (within window limit) | Requires hierarchical trees (RAPTOR) or GraphRAG |

### 2. Grounded context assembly and provenance

Grounding ensures that the generator relies on retrieved external evidence rather than internal parametric memory. When candidate chunks are selected, the context assembler formats them into structured, isolated evidence blocks:

```text
=== BEGIN RETRIEVED EVIDENCE ===
[Doc 1] (source: https://wiki.corp/policy/auth, id: auth-chunk-4):
All internal microservices must enforce mutual TLS (mTLS) with certificates rotated every 90 days.

[Doc 2] (source: https://wiki.corp/policy/tokens, id: tok-chunk-1):
OAuth2 JWT bearer tokens must enforce a maximum lifespan of 15 minutes.
=== END RETRIEVED EVIDENCE ===
```

System instructions mandate that the model cite `[Doc N]` references inline for every factual assertion and explicitly state when the evidence is insufficient to answer the query.

### 3. Classical retrieval evaluation metrics

Evaluating retrieval performance requires comparing retrieved passages against known ground-truth relevant passages across standard benchmark datasets (such as BEIR) (Thakur et al., 2021):

- **Precision@K:** The proportion of retrieved documents in the top-$K$ list that are genuinely relevant:
  $$\text{Precision@K} = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{K}$$
- **Recall@K:** The proportion of all relevant documents in the corpus that appear in the top-$K$ list:
  $$\text{Recall@K} = \frac{|\text{Retrieved}_K \cap \text{Relevant}|}{|\text{Relevant}|}$$
- **Mean Reciprocal Rank (MRR):** Evaluates how high the first relevant document ranks:
  $$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
- **Normalized Discounted Cumulative Gain (NDCG@K):** Evaluates graded relevance, penalizing systems when highly relevant documents appear lower in the ranking:
  $$\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{\text{rel}_i} - 1}{\log_2(i + 1)}, \quad \text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

### 4. Generation evaluation: The RAG Triad

While classical metrics evaluate the search index, they cannot assess whether the generated text is truthful or hallucinatory. The **RAG Triad** framework decomposes end-to-end RAG quality into three reference-free metrics evaluated using automated LLM evaluators (Es et al., 2023):

1. **Context Relevance:** Measures whether the retrieved passages are focused and relevant to the user query, penalizing noisy distractor chunks.
2. **Groundedness (Faithfulness):** Measures whether every factual claim made in the generated answer can be mathematically or logically derived from the retrieved context. A faithfulness score below 1.0 flags parametric hallucinations.
3. **Answer Relevance:** Measures whether the generated completion directly addresses the user intent and query requirements, penalizing evasive or off-topic responses.

## Main variants

1. **Synthetic needle-in-a-haystack testing:** Tests long-context resilience by inserting distinct factoids at varying depth percentiles (0% to 100%) within massive background text collections (Gemini Team, 2024).
2. **Reference-free LLM-as-a-judge (Ragas):** Evaluates production RAG logs without manual ground-truth labels by decomposing answers into atomic statements and verifying each against retrieved context (Es et al., 2023).
3. **Isolated citation verification gates:** A lightweight deterministic parser extracts all inline `[Doc N]` citations and runs token-level NLI (Natural Language Inference) models to verify claim support before streaming answers to the user.
4. **Hybrid long-context RAG:** Uses fast vector retrieval to identify the top three relevant documents, but passes the complete documents (rather than fragmented passages) into a long-context model, combining high-level retrieval filtering with full passage context.

## Minimal implementation

The following Python snippet demonstrates the calculation of classical retrieval metrics (Recall@K, MRR, NDCG@K) alongside automated faithfulness verification to catch unsupported claims. The [full runnable example](../../../examples/03-building-blocks/06-retrieval-and-rag/04-grounding-long-context-and-retrieval-evaluation/retrieval_evaluation_runtime.py) demonstrates simulated position-bias attention curves and complete RAG Triad scoring.

<details>
<summary>Expand minimal Python implementation</summary>

```python
import math
from typing import Dict, List, Set

def evaluate_retrieval_ranking(retrieved: List[str], relevant: Set[str], k: int = 3) -> Dict[str, float]:
    top_k = retrieved[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    precision = hits / max(len(top_k), 1)
    recall = hits / max(len(relevant), 1)

    mrr = 0.0
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            mrr = 1.0 / rank
            break

    return {"precision@k": precision, "recall@k": recall, "mrr": mrr}

def verify_claim_faithfulness(claims: List[str], retrieved_context: str) -> Dict[str, object]:
    context_tokens = set(retrieved_context.lower().split())
    unsupported = []
    for claim in claims:
        claim_tokens = set(claim.lower().split())
        overlap = len(claim_tokens.intersection(context_tokens)) / max(len(claim_tokens), 1)
        if overlap < 0.65:
            unsupported.append(claim)

    faithfulness_score = (len(claims) - len(unsupported)) / max(len(claims), 1)
    return {"faithfulness": faithfulness_score, "unsupported_claims": unsupported}
```

</details>

Run [retrieval_evaluation_runtime.py](../../../examples/03-building-blocks/06-retrieval-and-rag/04-grounding-long-context-and-retrieval-evaluation/retrieval_evaluation_runtime.py) to inspect precision, recall, MRR, NDCG calculations, and simulated U-shaped position-bias attention degradation.

## Data flow and state changes

1. **Query submission & retrieval:** A user prompt triggers retrieval across the indexed knowledge base.
2. **First-stage evaluation logging:** The retrieval coordinator logs the query, candidate document IDs, and ranking positions into an observability trace.
3. **Context formatting & grounding:** Chunks are formatted into structured `[Doc N]` blocks and injected into the prompt alongside strict grounding instructions.
4. **Model completion generation:** The model generates an answer containing inline citation markers.
5. **Post-generation verification:** The evaluation engine extracts individual sentences and verifies whether each assertion is supported by the corresponding cited chunk.
6. **Metric telemetry aggregation:** Faithfulness, context precision, and latency metrics are exported to monitoring dashboards to detect index degradation or drift over time.

## Trust boundaries

- **Grounded context boundary:** The generator must treat retrieved external evidence as untrusted third-party input. Formatting must prevent indirect prompt injection payloads embedded in retrieved chunks from breaking out of document fences.
- **Citation integrity boundary:** Inline citation tags generated by the LLM cannot be trusted unconditionally. The application runtime must verify that cited document IDs actually exist in the retrieved set and contain text supporting the asserted claim.
- **Evaluator isolation:** When using LLM-as-a-judge evaluation pipelines, evaluator prompts must be strictly isolated from user execution sessions so that an adversarial prompt cannot manipulate its own evaluation scores.

## Reliability failures

- **Hallucinated citation tags:** Language models frequently fabricate citations, generating confident claims followed by `[Doc 1]` even when Document 1 discusses an entirely unrelated topic.
- **Position-dependent context neglect:** When prompts contain twenty or more retrieved passages, facts located between the 30th and 70th percentile of the prompt are frequently ignored due to middle-context attention attenuation (Liu et al., 2023).
- **Evaluator judge bias:** Automated LLM judges often exhibit length bias (preferring longer, wordy answers over concise answers) and position bias, requiring careful calibration against human evaluation baselines.

## Limitations and trade-offs

- **Evaluation latency:** Running automated LLM evaluators on every production request doubles inference costs and adds latency, restricting online evaluation to asynchronous sampling or lightweight heuristic checks.
- **Synthetic benchmark divergence:** Near-perfect scores on synthetic needle-in-a-haystack tests often fail to predict performance on real-world reasoning tasks where evidence is ambiguous, contradictory, or spread across multiple passages.
- **Prompt caching fragility:** Long-context cost advantages depend heavily on prompt caching. Any dynamic modification to early prompt prefixes invalidates the cache, triggering full-price re-ingestion.

## Security preview

In Pass 2, grounding and evaluation systems are analyzed against **Evaluation Evasion, Citation Spoofing, and Indirect Prompt Injection via Context Distractors**. Attackers inject adversarial text into documentation pages designed to pass automated faithfulness filters while leading downstream reasoning models into unauthorized tool invocations. We evaluate cryptographic provenance signatures, isolated judge sandboxes, and policy guardrails in [Retrieval, memory, and data security](../../07-security-by-component-and-workflow-stage/02-retrieval-memory-and-data/chapter-plan.md).

## Open research questions

- Can transformer architectures eliminate the "Lost in the Middle" attention degradation without requiring quadratic attention computation?
- What lightweight, sub-10-millisecond verification algorithms can reliably detect factual hallucination without invoking secondary LLM judge calls?

## Key takeaways

- Massive context windows allow multi-document analysis, but suffer from high latency, compounding token costs, and position-dependent attention degradation ("Lost in the Middle").
- Focused RAG retrieval provides sub-second latencies, lower token expenditures, and sharp context focus for real-time agent loops.
- Classical information retrieval metrics (Recall@K, Precision@K, MRR, NDCG@K) evaluate search ranking performance against known relevance benchmarks.
- The RAG Triad framework evaluates generation quality reference-free across context relevance, groundedness (faithfulness), and answer relevance.
- Factual grounding requires automated post-generation verification to prevent models from generating plausible but unsupported inline citations.

## References

- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics (TACL), 12, 157-173. [arXiv:2307.03172](https://arxiv.org/abs/2307.03172).
- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2023). *Ragas: Automated Evaluation of Retrieval Augmented Generation*. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024). [arXiv:2309.15217](https://arxiv.org/abs/2309.15217).
- Gemini Team, Google. (2024). *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context*. arXiv preprint. [arXiv:2403.05530](https://arxiv.org/abs/2403.05530).
- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., & Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models*. In Thirty-fifth Conference on Neural Information Processing Systems (NeurIPS 2021) Datasets and Benchmarks Track. [arXiv:2104.08663](https://arxiv.org/abs/2104.08663).

---

[Next Unit: Tools and function calling plan →](../07-tools-and-function-calling/chapter-plan.md)
