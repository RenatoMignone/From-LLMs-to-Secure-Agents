import runpy
from pathlib import Path

MODULE = runpy.run_path(str(Path(__file__).parents[1] / "main.py"))

def test_average_gain_cannot_hide_retention_loss():
    score = MODULE["score"]
    baseline = {f: score(1, f) for f in ("new", "old")}
    candidate = {f: score(2, f) for f in ("new", "old")}
    assert sum(candidate.values()) > sum(baseline.values())
    assert not MODULE["should_promote"](baseline, candidate)

def test_equal_transfer_score_is_not_an_improvement():
    assert not MODULE["should_promote"]({"new": 3, "old": 4}, {"new": 3, "old": 4})

def test_improvement_with_retention_is_accepted():
    assert MODULE["should_promote"]({"new": 1, "old": 4}, {"new": 4, "old": 4})
