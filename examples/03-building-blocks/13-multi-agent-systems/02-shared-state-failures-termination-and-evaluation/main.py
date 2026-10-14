from dataclasses import dataclass, field

@dataclass
class Task:
    status: str = "ready"
    owner: str | None = None
    generation: int = 0
    lease_until: int = 0
    artifact: str | None = None
    seen: dict[str, tuple[str, int, str]] = field(default_factory=dict)

def claim(task, worker, now, ttl=5):
    if ttl <= 0:
        raise ValueError("Lease must be positive")
    eligible = task.status == "ready" or (task.status == "claimed" and now >= task.lease_until)
    if not eligible:
        return None
    task.generation += 1
    task.owner, task.lease_until = worker, now + ttl
    task.status, task.artifact = "claimed", None
    return task.generation

def submit(task, worker, generation, message_id, artifact, now):
    payload = (worker, generation, artifact)
    if message_id in task.seen:
        if task.seen[message_id] != payload:
            return "message conflict"
        return "duplicate"
    if task.status != "claimed" or task.owner != worker or task.generation != generation:
        return "stale or inactive"
    if now >= task.lease_until:
        return "expired"
    task.seen[message_id] = payload
    task.artifact, task.status = artifact, "verifying"
    return "submitted"

def verify(task):
    if task.status != "verifying":
        return False
    valid = task.artifact == "stock:blue-mug=1;source=snapshot-v1"
    task.status = "accepted" if valid else "failed"
    return valid

def cancel(task):
    if task.status not in {"accepted", "failed", "cancelled"}:
        task.status = "cancelled"

def bounded_discussion(rounds):
    for _ in range(rounds):
        pass  # Fixed peers never supply a verifiable artifact.
    return {"stop_reason": "round_budget", "task_success": False}

if __name__ == "__main__":
    task = Task()
    first = claim(task, "peer-A", now=0)
    assert claim(task, "peer-B", now=4) is None
    second = claim(task, "peer-B", now=5)
    artifact = "stock:blue-mug=1;source=snapshot-v1"
    assert submit(task, "peer-A", first, "msg-A", artifact, now=6) == "stale or inactive"
    assert submit(task, "peer-B", second, "msg-B", artifact, now=6) == "submitted"
    assert task.status == "verifying"
    assert submit(task, "peer-B", second, "msg-B", artifact, now=6) == "duplicate"
    assert submit(task, "peer-B", second, "msg-B", "different", now=6) == "message conflict"
    assert verify(task) and task.status == "accepted"
    stopped = Task(); gen = claim(stopped, "peer-A", now=0); cancel(stopped)
    assert submit(stopped, "peer-A", gen, "late", artifact, now=1) == "stale or inactive"
    expired = Task(); gen = claim(expired, "peer-A", now=0)
    assert submit(expired, "peer-A", gen, "expired", artifact, now=5) == "expired"
    bad = Task(); gen = claim(bad, "peer-A", now=0)
    assert submit(bad, "peer-A", gen, "bad", "done", now=1) == "submitted"
    assert not verify(bad) and bad.status == "failed"
    assert bounded_discussion(3)["task_success"] is False
    print(f"Recovered task: {task.status}, generation={task.generation}")
    print("Stale, duplicate, conflicting, expired, cancelled and unverified results checked.")
    print(bounded_discussion(3))
