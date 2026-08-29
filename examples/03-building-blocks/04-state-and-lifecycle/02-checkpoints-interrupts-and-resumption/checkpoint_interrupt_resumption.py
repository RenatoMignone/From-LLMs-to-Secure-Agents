#!/usr/bin/env python3
"""
Checkpointing, Interrupts, and State Resumption Runtime
Demonstrates durable state snapshots, human-in-the-loop approval interrupts,
and state time-travel / resumption.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import json
from typing import Any, Callable, Dict, List, Optional, Tuple


class RunState(Enum):
    READY = auto()
    RUNNING = auto()
    SUSPENDED_APPROVAL = auto()
    COMPLETED = auto()
    REJECTED = auto()


@dataclass
class Checkpoint:
    checkpoint_id: str
    thread_id: str
    step_number: int
    variables: Dict[str, Any]
    pending_action: Optional[Dict[str, Any]] = None


class DurableAgentRuntime:
    def __init__(self, sensitive_tools: set[str]):
        self.sensitive_tools = sensitive_tools
        self.checkpoints: Dict[str, List[Checkpoint]] = {}
        self._step_counter = 0

    def save_checkpoint(self, thread_id: str, variables: Dict[str, Any], pending_action: Optional[Dict[str, Any]] = None) -> Checkpoint:
        self._step_counter += 1
        cp = Checkpoint(
            checkpoint_id=f"cp_{self._step_counter:03d}",
            thread_id=thread_id,
            step_number=self._step_counter,
            variables=dict(variables),
            pending_action=pending_action,
        )
        if thread_id not in self.checkpoints:
            self.checkpoints[thread_id] = []
        self.checkpoints[thread_id].append(cp)
        return cp

    def get_latest_checkpoint(self, thread_id: str) -> Optional[Checkpoint]:
        cps = self.checkpoints.get(thread_id, [])
        return cps[-1] if cps else None

    def execute_step(self, thread_id: str, proposed_tool: str, tool_args: Dict[str, Any]) -> Tuple[RunState, Optional[Checkpoint]]:
        current_cp = self.get_latest_checkpoint(thread_id)
        current_vars = dict(current_cp.variables) if current_cp else {"execution_log": []}

        # Check if the proposed tool is sensitive and requires a human approval interrupt
        if proposed_tool in self.sensitive_tools:
            pending_action = {"tool_name": proposed_tool, "tool_args": tool_args}
            cp = self.save_checkpoint(thread_id, current_vars, pending_action=pending_action)
            return RunState.SUSPENDED_APPROVAL, cp

        # Regular non-sensitive tool execution
        current_vars["execution_log"].append(f"Executed {proposed_tool} with {tool_args}")
        cp = self.save_checkpoint(thread_id, current_vars, pending_action=None)
        return RunState.RUNNING, cp

    def resume_with_approval(self, thread_id: str, approved: bool, modified_args: Optional[Dict[str, Any]] = None) -> Tuple[RunState, Checkpoint]:
        latest_cp = self.get_latest_checkpoint(thread_id)
        if not latest_cp or not latest_cp.pending_action:
            raise ValueError(f"No pending suspended action found on thread {thread_id}")

        action = latest_cp.pending_action
        current_vars = dict(latest_cp.variables)

        if not approved:
            current_vars["execution_log"].append(f"REJECTED: Action {action['tool_name']} was rejected by supervisor.")
            cp = self.save_checkpoint(thread_id, current_vars, pending_action=None)
            return RunState.REJECTED, cp

        final_args = modified_args if modified_args is not None else action["tool_args"]
        current_vars["execution_log"].append(f"APPROVED & EXECUTED: {action['tool_name']} with args: {final_args}")
        current_vars["audit_status"] = "PASSED_WITH_SUPERVISOR_SIGN_OFF"
        cp = self.save_checkpoint(thread_id, current_vars, pending_action=None)
        return RunState.COMPLETED, cp

    def time_travel_restore(self, thread_id: str, checkpoint_id: str) -> Optional[Checkpoint]:
        """Rewind thread state to an earlier checkpoint to fork or inspect."""
        cps = self.checkpoints.get(thread_id, [])
        for cp in cps:
            if cp.checkpoint_id == checkpoint_id:
                # Fork state from historical checkpoint
                forked_cp = self.save_checkpoint(thread_id, cp.variables, pending_action=None)
                return forked_cp
        return None


def main() -> None:
    thread_id = "thread_db_migration_401"
    runtime = DurableAgentRuntime(sensitive_tools={"execute_production_migration"})

    print("=" * 80)
    print("DURABLE CHECKPOINTING & HUMAN-IN-THE-LOOP INTERRUPT TRACE")
    print("=" * 80)
    print(f"Thread: {thread_id}\n")

    # Step 1: Safe read-only step
    print("--- Step 1: Pre-flight Verification ---")
    state, cp1 = runtime.execute_step(thread_id, "verify_backup_status", {"target_db": "production_users"})
    print(f"Checkpoint created: [{cp1.checkpoint_id}] | State: {state.name}")
    print(f"Variables: {cp1.variables}\n")

    # Step 2: Sensitive action triggering interrupt
    print("--- Step 2: High-Privilege Action (Requires Approval) ---")
    state, cp2 = runtime.execute_step(
        thread_id,
        "execute_production_migration",
        {"target_db": "production_users", "sql_script": "DROP TABLE legacy_tokens; ADD COLUMN mfa_hash VARCHAR(64);"},
    )
    print(f"Checkpoint created: [{cp2.checkpoint_id}] | State: {state.name}")
    print(f"Suspended Pending Action: {cp2.pending_action}\n")

    # Step 3: Human Reviewer inspects, edits script to be safe, and approves
    print("--- Step 3: Human Review & Resumption ---")
    sanitized_args = {
        "target_db": "production_users",
        "sql_script": "ALTER TABLE legacy_tokens RENAME TO legacy_tokens_archived; ADD COLUMN mfa_hash VARCHAR(64);",
    }
    state, cp3 = runtime.resume_with_approval(thread_id, approved=True, modified_args=sanitized_args)
    print(f"Checkpoint created: [{cp3.checkpoint_id}] | State: {state.name}")
    print("Execution History Log:")
    for log_item in cp3.variables.get("execution_log", []):
        print(f"  • {log_item}")

    print("\n" + "=" * 80)
    print("CHECKPOINT REGISTRY (DURABLE TIMELINE):")
    for cp in runtime.checkpoints[thread_id]:
        print(f"  [{cp.checkpoint_id}] Step {cp.step_number} | Has Pending: {cp.pending_action is not None}")
    print("=" * 80)


if __name__ == "__main__":
    main()
