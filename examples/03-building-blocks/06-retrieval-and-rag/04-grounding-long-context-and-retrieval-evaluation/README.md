# Offline retrieval evaluation

Requires Python 3.10 or newer and only the standard library. From the repository root:

```bash
python3 examples/03-building-blocks/06-retrieval-and-rag/04-grounding-long-context-and-retrieval-evaluation/retrieval_evaluation_runtime.py
```

Expected JSON includes Precision@3 = 1/3, Recall@3 = 0.5 and reciprocal rank = 0.5. A deliberately contradictory claim receives lexical coverage = 1.0 while `semantic_support_verified` remains false. This shows why word overlap cannot implement semantic faithfulness.

Assertions cover ranking results, short result lists, ideal NDCG, empty judgments, duplicate IDs and invalid cutoffs. Empty relevance judgments yield 0.0 in this demo; report that convention in real evaluations. No model, Ragas scorer, factual verifier or measured attention curve is implemented.
