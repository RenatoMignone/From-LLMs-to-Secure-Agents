import json
import runpy
from pathlib import Path
import pytest

M = runpy.run_path(str(Path(__file__).parents[1] / "main.py"))

def test_resume_reconciles_without_duplicate_effect(tmp_path):
    result = M["compare"](tmp_path)
    assert result["effects"] == 1
    assert result["resumed"]["reconciled"]
    assert result["one"]["completed_work"] == result["resumed"]["completed_work"]

def test_cost_and_deadline_exhaustion_prevent_dispatch():
    trace = M["retry_trace"](["transient"] * 20, M["Policy"](cost_limit=2))
    assert trace["attempts"] == trace["cost"] == 2
    trace = M["retry_trace"](["ok"], M["Policy"](deadline=1.5))
    assert trace["attempts"] == trace["cost"] == 0
    assert trace["status"] == "stopped"

def test_stale_worker_cannot_write_after_new_owner():
    supplier = M["Supplier"]()
    supplier.reserve("a", 2)
    with pytest.raises(ValueError):
        supplier.reserve("b", 1)
    assert "b" not in supplier.ledger

def test_failed_compensation_keeps_external_effect_visible(tmp_path):
    supplier = M["Supplier"]()
    path = tmp_path / "progress.json"
    M["run_session"](path, supplier, 1)
    pending = M["compensate"](path, supplier)
    assert pending["status"] == "compensation_pending"
    assert supplier.ledger[pending["operation_id"]] == "reserved"
    assert json.loads(path.read_text())["unresolved_questions"]

def test_admission_applies_capacity_before_append():
    queue = []
    policy = M["Policy"](queue_capacity=1)
    assert M["admit"](queue, "first", policy)
    assert not M["admit"](queue, "second", policy)
    assert queue == ["first"]
