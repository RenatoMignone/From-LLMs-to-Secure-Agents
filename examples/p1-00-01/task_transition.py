"""Mock one authorized request, one state transition, and one emitted event."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransitionResult:
    state: dict[str, dict[str, str]]
    events: list[dict[str, str]]
    side_effect_requests: list[dict[str, str]]


def create_task(request: dict[str, object], permissions: set[str]) -> TransitionResult:
    """Apply a mocked create-task request without calling an external service."""
    if request.get("action") != "create_task":
        raise ValueError("expected create_task action")
    if "tasks:create" not in permissions:
        raise PermissionError("missing tasks:create permission")

    task = request["task"]
    if not isinstance(task, dict) or not isinstance(task.get("title"), str):
        raise ValueError("task.title must be a string")

    task_id = "task-1"
    state = {task_id: {"title": task["title"], "status": "open"}}
    events = [{"type": "task.created", "task_id": task_id}]
    side_effect_requests = [{"type": "notification.requested", "task_id": task_id}]
    return TransitionResult(state, events, side_effect_requests)


if __name__ == "__main__":
    request = {
        "request_id": "req-104",
        "actor_id": "user-42",
        "action": "create_task",
        "task": {"title": "Send the brief"},
    }
    result = create_task(request, {"tasks:create"})
    print(f"state={result.state}")
    print(f"event={result.events[0]}")
    print(f"side_effect_request={result.side_effect_requests[0]}")
