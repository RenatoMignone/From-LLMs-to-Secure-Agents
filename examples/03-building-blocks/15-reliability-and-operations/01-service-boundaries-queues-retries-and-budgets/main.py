"""Deterministic teaching simulation. No network calls or real reservations."""
from __future__ import annotations
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from random import Random

@dataclass(frozen=True)
class Policy:
    queue_capacity: int = 2
    max_attempts: int = 3
    cost_limit: int = 3
    deadline: float = 10.0

class SimulatedCrash(Exception):
    pass

class Supplier:
    def __init__(self) -> None:
        self.ledger: dict[str, str] = {}
        self.effects = 0
        self.highest_token = 0

    def reserve(self, operation: str, token: int) -> str:
        if token < self.highest_token:
            raise ValueError("stale worker")
        self.highest_token = token
        if operation not in self.ledger:
            self.ledger[operation] = "reserved"
            self.effects += 1
        return self.ledger[operation]

    def release(self, operation: str) -> None:
        raise ConnectionError("mock release service unavailable")

def admit(queue: list[str], job: str, policy: Policy) -> bool:
    if len(queue) >= policy.queue_capacity:
        return False
    queue.append(job)
    return True

def retry_trace(outcomes: list[str], policy: Policy) -> dict:
    """Budget includes queue delay, each attempt and backoff; no real sleeping."""
    elapsed, cost, attempts = 1.0, 0, 0
    rng = Random(7)
    for outcome in outcomes:
        if attempts >= policy.max_attempts or cost >= policy.cost_limit or elapsed + 1 > policy.deadline:
            break
        attempts += 1
        cost += 1
        elapsed += 1
        if outcome == "ok":
            return dict(status="complete", attempts=attempts, cost=cost, elapsed=elapsed)
        if outcome != "transient":
            return dict(status="unresolved", attempts=attempts, cost=cost, elapsed=elapsed)
        elapsed += rng.uniform(0, min(2 ** (attempts - 1), 2))
    return dict(status="stopped", attempts=attempts, cost=cost, elapsed=elapsed)

def save(path: Path, record: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(record, indent=2) + "\n")
    temporary.replace(path)

def run_session(path: Path, supplier: Supplier, token: int, crash: bool = False) -> dict:
    operation = "lee-reservation-17"
    record = json.loads(path.read_text()) if path.exists() else {
        "operation_id": operation, "status": "pending", "completed_work": [],
        "unresolved_questions": ["Did the supplier reserve the mug?"],
        "next_steps": ["Reconcile operation ID before any retry"], "verification_results": [],
    }
    save(path, record)  # Intent survives before the external dispatch.
    resource_open = True
    try:
        result = supplier.ledger.get(operation)  # Mock authoritative status lookup.
        reconciled = result is not None
        if result is None:
            result = supplier.reserve(operation, token)
            if crash:
                raise SimulatedCrash("response lost after external commit")
        record.update(status="complete", completed_work=[result], unresolved_questions=[],
                      next_steps=[], verification_results=["supplier ledger confirms reservation"],
                      reconciled=reconciled)
    finally:
        # This simulates supervised local cleanup, not cleanup after a real hard kill.
        resource_open = False
        record["local_resource_released"] = not resource_open
        save(path, record)
    return record

def compensate(path: Path, supplier: Supplier) -> dict:
    record = json.loads(path.read_text())
    try:
        supplier.release(record["operation_id"])
    except ConnectionError:
        record.update(status="compensation_pending", unresolved_questions=["Reservation release unconfirmed"],
                      next_steps=["Reconcile release and arrange recovery"])
    save(path, record)
    return record

def compare(root: Path) -> dict:
    single, interrupted = Supplier(), Supplier()
    one = run_session(root / "one-session.json", single, token=1)
    path = root / "multiple-sessions.json"
    try:
        run_session(path, interrupted, token=1, crash=True)
    except SimulatedCrash:
        assert json.loads(path.read_text())["status"] == "pending"
    resumed = run_session(path, interrupted, token=2)
    assert one["completed_work"] == resumed["completed_work"] == ["reserved"]
    assert single.effects == interrupted.effects == 1
    assert resumed["reconciled"] and resumed["local_resource_released"]
    return dict(one=one, resumed=resumed, effects=interrupted.effects, supplier=interrupted)

def main() -> None:
    policy = Policy()
    queue: list[str] = []
    assert [admit(queue, job, policy) for job in ("a", "b", "c")] == [True, True, False]
    trace = retry_trace(["transient", "ok"], policy)
    assert trace["status"] == "complete" and trace["attempts"] == trace["cost"] == 2
    supplier = Supplier()
    supplier.reserve("x", token=2)
    try:
        supplier.reserve("x", token=1)
    except ValueError:
        pass
    else:
        raise AssertionError("stale worker was accepted")
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        result = compare(root)
        pending = compensate(root / "multiple-sessions.json", result["supplier"])
        assert pending["status"] == "compensation_pending"
        print("queue_delay=1 tick; completion=2/2; external_effects=1 per scenario; cleanup=released")
        print(f"retry_attempts={trace['attempts']}; cost={trace['cost']}; compensation=pending")
        print("Progress artifacts verified in a temporary directory; removed on exit.")

if __name__ == "__main__":
    main()
