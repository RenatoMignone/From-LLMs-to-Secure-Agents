from dataclasses import replace
from pathlib import Path
import runpy
import pytest

M = runpy.run_path(str(Path(__file__).parents[1] / "main.py"))

def test_late_tool_result_survives_interruption_without_false_success():
    state = M["run"](M["trace"](True))
    assert state.tool_status == "complete" and state.tool_outcome == "reserved"
    assert state.outcome_verified and state.final_acknowledged
    assert not state.task_complete and state.needs_resolution
    assert "release is unconfirmed" in state.partial_output
    assert "obsolete" not in state.partial_output

def test_uninterrupted_goal_requires_verification_and_playback():
    events = M["trace"](False)
    before_playback = M["run"](events[:-1])
    assert before_playback.goal_satisfied and before_playback.outcome_verified
    assert not before_playback.task_complete
    assert M["run"](events).task_complete

def test_partial_output_and_connection_end_do_not_complete_task():
    state = M["run"](M["trace"](False)[:2])
    assert state.partial_output and state.tool_status == "pending"
    assert not state.task_complete and not state.final_acknowledged

def test_old_turn_playback_cannot_acknowledge_current_response():
    events = M["trace"](True)
    state = M["run"](events[:-1])
    late = replace(events[-1], turn="turn-1")
    state = M["reduce_event"](state, late)
    assert not state.final_acknowledged

def test_gap_requires_state_recovery():
    event = M["Event"](2, "partial", "turn-1", "hello")
    with pytest.raises(ValueError, match="gap or reordering"):
        M["reduce_event"](M["State"](), event)

def test_unrelated_operation_cannot_overwrite_pending_result():
    state = M["run"](M["trace"](False)[:2])
    event = M["Event"](3, "tool_result", "turn-1", "reserved", "other-operation")
    with pytest.raises(ValueError, match="untracked"):
        M["reduce_event"](state, event)
