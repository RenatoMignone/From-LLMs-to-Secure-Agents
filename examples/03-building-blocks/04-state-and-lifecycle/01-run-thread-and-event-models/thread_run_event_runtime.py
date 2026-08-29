#!/usr/bin/env python3
"""
Thread, Run, and Event Sourcing Runtime
Demonstrates hierarchical thread-run-turn models, structured event emission,
and state reduction across multi-turn agent lifecycles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
import json
from typing import Any, Callable, Dict, List, Optional


class RunStatus(Enum):
    QUEUED = auto()
    IN_PROGRESS = auto()
    REQUIRES_ACTION = auto()
    COMPLETED = auto()
    FAILED = auto()


class EventType(Enum):
    USER_MESSAGE = "user.message"
    THOUGHT_GENERATED = "agent.thought"
    TOOL_CALL_REQUESTED = "tool.call.requested"
    TOOL_EXECUTION_COMPLETED = "tool.execution.completed"
    RUN_STATE_CHANGED = "run.state.changed"
    AGENT_MESSAGE = "agent.message"


@dataclass
class Event:
    event_id: str
    event_type: EventType
    timestamp: str
    thread_id: str
    run_id: str
    payload: Dict[str, Any]


@dataclass
class ThreadState:
    thread_id: str
    variables: Dict[str, Any] = field(default_factory=dict)
    messages: List[Dict[str, str]] = field(default_factory=list)
    event_history: List[Event] = field(default_factory=list)
    version: int = 0

    def apply_event(self, event: Event) -> None:
        """Event Sourcing Reducer: Updates current state snapshot based on incoming event."""
        self.event_history.append(event)
        self.version += 1

        if event.event_type == EventType.USER_MESSAGE:
            self.messages.append({"role": "user", "content": event.payload.get("content", "")})
        elif event.event_type == EventType.AGENT_MESSAGE:
            self.messages.append({"role": "assistant", "content": event.payload.get("content", "")})
        elif event.event_type == EventType.TOOL_EXECUTION_COMPLETED:
            var_name = event.payload.get("store_as")
            if var_name:
                self.variables[var_name] = event.payload.get("result")


class AgentRuntime:
    def __init__(self, tools: Dict[str, Callable[[Dict[str, Any]], str]]):
        self.tools = tools
        self.threads: Dict[str, ThreadState] = {}
        self._event_counter = 0

    def get_or_create_thread(self, thread_id: str) -> ThreadState:
        if thread_id not in self.threads:
            self.threads[thread_id] = ThreadState(thread_id=thread_id)
        return self.threads[thread_id]

    def _emit(self, thread: ThreadState, run_id: str, event_type: EventType, payload: Dict[str, Any]) -> Event:
        self._event_counter += 1
        event = Event(
            event_id=f"evt_{self._event_counter:04d}",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            thread_id=thread.thread_id,
            run_id=run_id,
            payload=payload,
        )
        thread.apply_event(event)
        return event

    def create_and_execute_run(self, thread_id: str, run_id: str, user_prompt: str) -> RunStatus:
        thread = self.get_or_create_thread(thread_id)

        # 1. Ingest User Input
        self._emit(thread, run_id, EventType.USER_MESSAGE, {"content": user_prompt})
        self._emit(thread, run_id, EventType.RUN_STATE_CHANGED, {"status": RunStatus.IN_PROGRESS.name})

        # 2. Simulate Thought & Action Planning
        self._emit(thread, run_id, EventType.THOUGHT_GENERATED, {
            "thought": "User requested account validation. Need to query authentication service.",
        })

        # 3. Request Tool Execution (REQUIRES_ACTION)
        self._emit(thread, run_id, EventType.RUN_STATE_CHANGED, {"status": RunStatus.REQUIRES_ACTION.name})
        self._emit(thread, run_id, EventType.TOOL_CALL_REQUESTED, {
            "tool_name": "fetch_user_status",
            "tool_args": {"user_id": "usr_9912"},
        })

        # 4. Dispatch Tool in Runtime
        tool_fn = self.tools.get("fetch_user_status")
        if tool_fn:
            result_str = tool_fn({"user_id": "usr_9912"})
            self._emit(thread, run_id, EventType.TOOL_EXECUTION_COMPLETED, {
                "tool_name": "fetch_user_status",
                "result": result_str,
                "store_as": "user_status_record",
            })

        # 5. Synthesize Final Response
        self._emit(thread, run_id, EventType.RUN_STATE_CHANGED, {"status": RunStatus.IN_PROGRESS.name})
        self._emit(thread, run_id, EventType.AGENT_MESSAGE, {
            "content": "User account usr_9912 is verified, active, and MFA-enabled.",
        })
        self._emit(thread, run_id, EventType.RUN_STATE_CHANGED, {"status": RunStatus.COMPLETED.name})

        return RunStatus.COMPLETED


def main() -> None:
    def mock_fetch_user(args: Dict[str, Any]) -> str:
        return json.dumps({"user_id": args.get("user_id"), "status": "ACTIVE", "mfa": True})

    runtime = AgentRuntime(tools={"fetch_user_status": mock_fetch_user})
    thread_id = "thread_compliance_audit_2026"
    run_id = "run_001"

    print("=" * 80)
    print("THREAD, RUN, AND EVENT SOURCING RUNTIME TRACE")
    print("=" * 80)
    print(f"Thread ID: {thread_id}")
    print(f"Run ID:    {run_id}\n")

    status = runtime.create_and_execute_run(thread_id, run_id, "Check status and MFA compliance for user usr_9912.")

    thread = runtime.get_or_create_thread(thread_id)

    print("EVENT STREAM (Append-Only Log):")
    for evt in thread.event_history:
        print(f"  [{evt.event_id}] {evt.event_type.value:<26} | Payload: {evt.payload}")

    print("\n" + "-" * 80)
    print("REDUCED THREAD STATE SNAPSHOT:")
    print(f"  Thread Version:   {thread.version}")
    print(f"  Stored Variables: {thread.variables}")
    print("  Message History:")
    for msg in thread.messages:
        print(f"    [{msg['role'].upper()}]: {msg['content']}")

    print("=" * 80)
    print(f"FINAL RUN STATUS: {status.name}")
    print("=" * 80)


if __name__ == "__main__":
    main()
