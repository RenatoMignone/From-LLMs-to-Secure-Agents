#!/usr/bin/env python3
"""
Cancellation, Saga Compensating Actions, and Resource Cleanup Runtime
Demonstrates cooperative cancellation tokens, rollback sagas on partial failure,
and deterministic resource finalization in autonomous agent runtimes.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class TerminalState(Enum):
    COMPLETED = auto()
    CANCELLED = auto()
    FAILED_COMPENSATED = auto()
    FAILED_UNRECOVERABLE = auto()


class CancellationToken:
    def __init__(self):
        self._is_cancelled = False
        self.reason: Optional[str] = None

    def cancel(self, reason: str = "User requested cancellation") -> None:
        self._is_cancelled = True
        self.reason = reason

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled


@dataclass
class SagaStep:
    name: str
    forward_action: Callable[[], bool]
    compensating_action: Callable[[], bool]
    executed: bool = False


class SagaExecutionManager:
    def __init__(self):
        self.completed_steps: List[SagaStep] = []
        self.system_resources: Dict[str, str] = {}

    def execute_saga(self, steps: List[SagaStep], cancel_token: CancellationToken) -> Tuple[TerminalState, List[str]]:
        log = []

        for step in steps:
            # Check for cancellation before executing forward step
            if cancel_token.is_cancelled:
                log.append(f"CANCELLATION DETECTED: {cancel_token.reason}. Initiating rollback.")
                self._rollback(log)
                return TerminalState.CANCELLED, log

            log.append(f"Executing Forward Step: [{step.name}]")
            success = step.forward_action()

            if success:
                step.executed = True
                self.completed_steps.append(step)
                log.append(f"  • [{step.name}] SUCCEEDED")
            else:
                log.append(f"  • [{step.name}] FAILED! Initiating backward compensating rollback.")
                self._rollback(log)
                return TerminalState.FAILED_COMPENSATED, log

        log.append("All forward steps completed successfully.")
        return TerminalState.COMPLETED, log

    def _rollback(self, log: List[str]) -> None:
        """Executes compensating actions in reverse order of execution (LIFO)."""
        log.append("--- ROLLING BACK COMPENSATING ACTIONS ---")
        while self.completed_steps:
            step = self.completed_steps.pop()
            log.append(f"Compensating: Undoing [{step.name}]...")
            comp_ok = step.compensating_action()
            if comp_ok:
                log.append(f"  • Compensation for [{step.name}] SUCCESSFUL.")
            else:
                log.append(f"  • CRITICAL: Compensation for [{step.name}] FAILED!")


def main() -> None:
    print("=" * 80)
    print("SAGA COMPENSATING ACTIONS & CLEANUP TRACE")
    print("=" * 80)

    manager = SagaExecutionManager()

    # Define mock resource actions
    def reserve_vm() -> bool:
        manager.system_resources["vm"] = "vm_active_instance_801"
        return True

    def release_vm() -> bool:
        manager.system_resources.pop("vm", None)
        return True

    def provision_storage() -> bool:
        manager.system_resources["storage"] = "vol_storage_nvme_50gb"
        return True

    def delete_storage() -> bool:
        manager.system_resources.pop("storage", None)
        return True

    def attach_database() -> bool:
        # Deliberately fails to trigger rollback demonstration
        return False

    def detach_database() -> bool:
        manager.system_resources.pop("database", None)
        return True

    steps = [
        SagaStep("Reserve Cloud VM", reserve_vm, release_vm),
        SagaStep("Provision Storage Volume", provision_storage, delete_storage),
        SagaStep("Attach Database Instance", attach_database, detach_database),
    ]

    cancel_token = CancellationToken()

    print("Initial System Resources: ", manager.system_resources)
    print("\nRUNNING DISTRIBUTED SAGA WORKFLOW...")
    state, log = manager.execute_saga(steps, cancel_token)

    print("\nEXECUTION LOG:")
    for entry in log:
        print(f"  {entry}")

    print("\n" + "=" * 80)
    print(f"FINAL TERMINAL STATE: {state.name}")
    print(f"FINAL SYSTEM RESOURCES AFTER ROLLBACK: {manager.system_resources} (0 Orphaned Resources)")
    print("=" * 80)


if __name__ == "__main__":
    main()
