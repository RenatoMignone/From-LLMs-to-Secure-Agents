import json
from pathlib import Path

def baseline(sku, requested, snapshot):
    stock = snapshot["stock"].get(sku)
    available = None if stock is None else stock > 0
    return {"sku": sku, "requested": requested, "available": available, "source": None}

def check_report(report, snapshot):
    stock = snapshot["stock"].get(report["sku"])
    expected = None if stock is None else stock >= report["requested"]
    issues = []
    if report["source"] != snapshot["id"]:
        issues.append("missing_or_wrong_source")
    if report["available"] != expected:
        issues.append("availability_mismatch")
    return issues

def mock_refine(report, feedback, snapshot):
    stock = snapshot["stock"].get(report["sku"])
    return {**report, "source": snapshot["id"], "available": None if stock is None else stock >= report["requested"]}

def refine(sku, requested, snapshot, max_revisions=2):
    if requested <= 0 or max_revisions < 0:
        raise ValueError("Positive quantity and nonnegative budget required")
    draft = baseline(sku, requested, snapshot)
    history = []
    for _ in range(max_revisions):
        feedback = check_report(draft, snapshot)
        if not feedback:
            break
        history.append(tuple(feedback))
        draft = mock_refine(draft, feedback, snapshot)
    return draft, not check_report(draft, snapshot), history

if __name__ == "__main__":
    record = json.loads(Path(__file__).with_name("skill-record.json").read_text())
    snapshot = {"id": "S17", "stock": {"blue-mug": 1, "tea-tin": 5, "red-mug": 0}}
    draft, accepted, history = refine("blue-mug", 2, snapshot)
    assert accepted and draft["available"] is False and len(history) == 1
    assert not refine("blue-mug", 2, snapshot, max_revisions=0)[1]
    assert baseline("red-mug", 1, snapshot)["available"] is False
    assert baseline("unknown", 1, snapshot)["available"] is None
    for sku, requested, expected in [("tea-tin", 2, True), ("tea-tin", 6, False), ("red-mug", 1, False), ("unknown", 1, None)]:
        result, ok, _ = refine(sku, requested, snapshot)
        assert ok and result["available"] is expected
    assert snapshot["stock"] == {"blue-mug": 1, "tea-tin": 5, "red-mug": 0}
    assert record["mechanism"] == "authored-package-revision" and not record["weight_update"]
    assert record["previous_version"] == "1.0"
    print(draft)
    print("Mock refinement, transfer, retention and zero-budget checks passed.")
    print("Candidate package: version " + record["candidate_version"] + "; weights unchanged")
