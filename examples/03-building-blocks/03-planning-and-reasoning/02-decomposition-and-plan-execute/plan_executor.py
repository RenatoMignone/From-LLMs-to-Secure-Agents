#!/usr/bin/env python3
"""
Planner-Executor Agent Runner
Demonstrates two-tier task decomposition, structured step state tracking,
and dynamic replanning on intermediate tool failures.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import json
from typing import Any, Callable, Dict, List, Optional, Tuple


class StepStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class Subtask:
    step_id: int
    description: str
    tool_name: str
    tool_args: Dict[str, Any]
    status: StepStatus = StepStatus.PENDING
    result: Optional[str] = None


@dataclass
class ExecutionPlan:
    goal: str
    subtasks: List[Subtask] = field(default_factory=list)
    replan_count: int = 0


class PlanExecutorAgent:
    def __init__(
        self,
        tools: Dict[str, Callable[[Dict[str, Any]], str]],
        max_replans: int = 1,
    ):
        self.tools = tools
        self.max_replans = max_replans

    def generate_initial_plan(self, goal: str) -> ExecutionPlan:
        """Simulates Planner Model decomposing a high-level goal into structured subtasks."""
        subtasks = [
            Subtask(1, "Scan security vulnerabilities in repository.", "scan_security", {"target": "auth-service"}),
            Subtask(2, "Fetch mock advisory details.", "fetch_advisory", {"advisory_id": "MOCK-2026-0001"}),
            Subtask(3, "Generate a mock patch diff.", "generate_patch", {"advisory_id": "MOCK-2026-0001"}),
        ]
        return ExecutionPlan(goal=goal, subtasks=subtasks)

    def execute_plan(self, plan: ExecutionPlan) -> Tuple[str, ExecutionPlan]:
        """Executor Model executes subtasks sequentially and handles replanning triggers."""
        step_index = 0
        while step_index < len(plan.subtasks):
            step = plan.subtasks[step_index]
            step.status = StepStatus.IN_PROGRESS
            tool_fn = self.tools.get(step.tool_name)

            if not tool_fn:
                step.status = StepStatus.FAILED
                step.result = f"Tool '{step.tool_name}' unavailable."
                break

            output = tool_fn(step.tool_args)
            try:
                parsed = json.loads(output)
                if parsed.get("status") == "error":
                    step.status = StepStatus.FAILED
                    step.result = parsed.get("error", "Unknown error")
                    if plan.replan_count >= self.max_replans:
                        break
                    plan = self._trigger_replan(plan, step)
                    continue
                else:
                    step.status = StepStatus.COMPLETED
                    step.result = output
            except Exception:
                step.status = StepStatus.FAILED
                step.result = "Tool returned invalid JSON."
                break

            step_index += 1

        # Final synthesis
        completed_count = sum(1 for s in plan.subtasks if s.status == StepStatus.COMPLETED)
        final_summary = f"Plan completed {completed_count}/{len(plan.subtasks)} steps for goal: '{plan.goal}'."
        return final_summary, plan

    def _trigger_replan(self, plan: ExecutionPlan, failed_step: Subtask) -> ExecutionPlan:
        plan.replan_count += 1
        # Planner generates alternative fallback step
        fallback_step = Subtask(
            step_id=failed_step.step_id,
            description=f"Fallback: {failed_step.description} via public mirror.",
            tool_name="fetch_advisory_mirror",
            tool_args=failed_step.tool_args,
        )
        # Replace failed step with fallback
        idx = plan.subtasks.index(failed_step)
        plan.subtasks[idx] = fallback_step
        return plan


def main() -> None:
    # Mock environment tools
    def scan_security(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "findings": ["MOCK-2026-0001"], "severity": "HIGH"})

    def fetch_advisory(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "error", "error": "Primary advisory service timed out."})

    def fetch_advisory_mirror(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "advisory": args.get("advisory_id"), "details": "Mock validation issue."})

    def generate_patch(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "patch_file": "mock_validation_fix.diff", "lines_changed": 12})

    tools = {
        "scan_security": scan_security,
        "fetch_advisory": fetch_advisory,
        "fetch_advisory_mirror": fetch_advisory_mirror,
        "generate_patch": generate_patch,
    }

    agent = PlanExecutorAgent(tools)
    goal = "Remediate high-severity security vulnerabilities in auth-service."

    print("=" * 80)
    print("PLAN-AND-EXECUTE WORKFLOW TRACE")
    print("=" * 80)

    plan = agent.generate_initial_plan(goal)
    print(f"Goal: {plan.goal}\n")
    print("INITIAL PLAN GENERATED:")
    for s in plan.subtasks:
        print(f"  [Step {s.step_id}] ({s.status.name}) {s.description} -> Tool: {s.tool_name}")

    print("\nEXECUTING PLAN...")
    summary, finished_plan = agent.execute_plan(plan)

    print("\nEXECUTION RESULTS:")
    for s in finished_plan.subtasks:
        print(f"  [Step {s.step_id}] ({s.status.name}) {s.description}")
        print(f"    Output: {s.result}")

    print("-" * 80)
    print(f"FINAL SUMMARY: {summary}")
    print("=" * 80)


if __name__ == "__main__":
    main()
