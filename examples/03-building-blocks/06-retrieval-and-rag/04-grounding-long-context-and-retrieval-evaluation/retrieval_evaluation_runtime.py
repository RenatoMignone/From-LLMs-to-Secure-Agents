"""Offline ranking metrics and a deliberately limited lexical-support heuristic.

No model, Ragas scorer, entailment check or attention simulation is implemented.
"""
import json
import math
import re


def check_ranking(retrieved, k):
    if type(k) is not int or k <= 0:
        raise ValueError('k must be a positive integer')
    if len(set(retrieved)) != len(retrieved):
        raise ValueError('ranking must have unique document IDs')


def precision_at_k(retrieved, relevant, k):
    check_ranking(retrieved, k)
    return len(set(retrieved[:k]) & relevant) / k


def recall_at_k(retrieved, relevant, k):
    check_ranking(retrieved, k)
    return len(set(retrieved[:k]) & relevant) / len(relevant) if relevant else 0.0


def reciprocal_rank(retrieved, relevant):
    check_ranking(retrieved, 1)
    return next((1 / rank for rank, doc in enumerate(retrieved, 1) if doc in relevant), 0.0)


def ndcg_at_k(retrieved, grades, k):
    check_ranking(retrieved, k)
    if any(not math.isfinite(g) or g < 0 for g in grades.values()):
        raise ValueError('grades must be finite and non-negative')
    def dcg(values):
        return sum((2 ** grade - 1) / math.log2(rank + 1)
                   for rank, grade in enumerate(values, 1))
    ideal = dcg(sorted(grades.values(), reverse=True)[:k])
    observed = dcg([grades.get(doc, 0) for doc in retrieved[:k]])
    return observed / ideal if ideal else 0.0


def lexical_coverage(claim, context):
    tokens = lambda text: set(re.findall(r'\b\w+\b', text.lower()))
    claim_tokens = tokens(claim)
    return len(claim_tokens & tokens(context)) / len(claim_tokens) if claim_tokens else 0.0


if __name__ == '__main__':
    ranking = ['doc-4', 'doc-1', 'doc-8', 'doc-2', 'doc-9']
    relevant = {'doc-1', 'doc-2'}
    grades = {'doc-1': 3, 'doc-2': 2, 'doc-3': 1}
    assert precision_at_k(ranking, relevant, 3) == 1 / 3
    assert recall_at_k(ranking, relevant, 3) == 0.5
    assert reciprocal_rank(ranking, relevant) == 0.5
    assert precision_at_k(['doc-1'], relevant, 3) == 1 / 3
    assert ndcg_at_k(['doc-1', 'doc-2', 'doc-3'], grades, 3) == 1.0
    assert ndcg_at_k([], {}, 3) == 0.0
    for bad, k in [(['doc-1', 'doc-1'], 3), (ranking, 0)]:
        try:
            precision_at_k(bad, relevant, k)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid ranking accepted')
    # The source says the opposite. High word overlap still accepts the claim.
    context = 'The lamp is not eligible for return.'
    claim = 'The lamp is eligible for return.'
    coverage = lexical_coverage(claim, context)
    assert coverage == 1.0
    print(json.dumps({'precision@3': precision_at_k(ranking, relevant, 3),
                      'recall@3': recall_at_k(ranking, relevant, 3),
                      'reciprocal_rank': reciprocal_rank(ranking, relevant),
                      'ndcg@5': ndcg_at_k(ranking, grades, 5),
                      'contradictory_claim_lexical_coverage': coverage,
                      'semantic_support_verified': False}, indent=2))
