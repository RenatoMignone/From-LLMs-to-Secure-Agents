"""Ordered local event reducer. All speech, tool and ledger events are mocked."""
from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Event:
    sequence: int
    kind: str
    turn: str
    value: str = ""
    operation_id: str | None = None

@dataclass(frozen=True)
class State:
    sequence: int = 0
    active_turn: str = "turn-1"
    operation_id: str = "reservation-17"
    current_intent: str = "reserve"
    tool_status: str = "idle"
    tool_outcome: str | None = None
    outcome_verified: bool = False
    goal_satisfied: bool = False
    needs_resolution: bool = False
    partial_output: str = ""
    final_ready: bool = False
    playback_done: bool = False

    @property
    def final_acknowledged(self) -> bool:
        return self.final_ready and self.playback_done

    @property
    def task_complete(self) -> bool:
        return self.goal_satisfied and self.outcome_verified and self.final_acknowledged

def acknowledgement(state: State) -> str:
    if not state.outcome_verified:
        raise ValueError("outcome has not been verified")
    if state.goal_satisfied:
        return "Your reservation is confirmed."
    return "The reservation was already saved; release is unconfirmed."

def reduce_event(state: State, event: Event) -> State:
    if event.sequence != state.sequence + 1:
        raise ValueError("event gap or reordering: retrieve current state")
    state = replace(state, sequence=event.sequence)
    if event.kind in {"tool_start", "tool_result", "verify"} and event.operation_id != state.operation_id:
        raise ValueError("untracked operation ID")
    if event.kind == "partial":
        if event.turn == state.active_turn:
            state = replace(state, partial_output=state.partial_output + event.value)
    elif event.kind == "tool_start":
        if state.tool_status != "idle":
            raise ValueError("operation already dispatched")
        state = replace(state, tool_status="pending")
    elif event.kind == "interruption":
        if event.value != "cancel":
            raise ValueError("fixture only models a cancel correction")
        state = replace(state, active_turn=event.turn, current_intent="cancel", partial_output="",
                        final_ready=False, playback_done=False, goal_satisfied=False, needs_resolution=True)
    elif event.kind == "tool_result":
        if state.tool_status != "pending" or event.value != "reserved":
            raise ValueError("unexpected mock tool outcome")
        # A late result belongs to the operation even when its turn is obsolete.
        state = replace(state, tool_status="complete", tool_outcome=event.value, outcome_verified=False)
    elif event.kind == "verify":
        if event.turn != state.active_turn or state.tool_status != "complete" or event.value != state.tool_outcome:
            raise ValueError("mock ledger does not confirm the tracked result")
        satisfied = state.current_intent == "reserve" and state.tool_outcome == "reserved"
        state = replace(state, outcome_verified=True, goal_satisfied=satisfied, needs_resolution=not satisfied)
    elif event.kind == "final":
        if event.turn == state.active_turn:
            state = replace(state, partial_output=acknowledgement(state), final_ready=True, playback_done=False)
    elif event.kind == "playback_done":
        if event.turn == state.active_turn:
            if not state.final_ready:
                raise ValueError("no current final response to acknowledge")
            state = replace(state, playback_done=True)
    else:
        raise ValueError("unknown event kind")
    return state

def trace(interrupted: bool) -> list[Event]:
    operation = "reservation-17"
    raw = [("partial", "turn-1", "I am checking", None),
           ("tool_start", "turn-1", "", operation)]
    turn = "turn-1"
    if interrupted:
        raw += [("interruption", "turn-2", "cancel", None),
                ("partial", "turn-1", " obsolete speech", None)]
        turn = "turn-2"
    raw += [("tool_result", "turn-1", "reserved", operation),
            ("verify", turn, "reserved", operation),
            ("final", turn, "", None), ("playback_done", turn, "", None)]
    return [Event(i, *fields) for i, fields in enumerate(raw, start=1)]

def run(events: list[Event]) -> State:
    state = State()
    for event in events:
        state = reduce_event(state, event)
    return state

def main() -> None:
    one = run(trace(False))
    interrupted = run(trace(True))
    assert one.task_complete
    assert interrupted.tool_status == "complete" and interrupted.outcome_verified
    assert interrupted.final_acknowledged and not interrupted.task_complete and interrupted.needs_resolution
    assert "obsolete" not in interrupted.partial_output
    print(f"uninterrupted: task_complete={one.task_complete}")
    print(f"interrupted: tool_status={interrupted.tool_status}; final_acknowledged={interrupted.final_acknowledged}")
    print(f"interrupted: task_complete={interrupted.task_complete}; needs_resolution={interrupted.needs_resolution}")
    print(interrupted.partial_output)

if __name__ == "__main__":
    main()
