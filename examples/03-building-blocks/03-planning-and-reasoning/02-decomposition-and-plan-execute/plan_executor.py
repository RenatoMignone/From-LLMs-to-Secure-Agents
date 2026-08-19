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
    def __init__(self, tools: Dict[str, Callable[[Dict[str, Any]], str]]):
        self.tools = tools

    def generate_initial_plan(self, goal: str) -> ExecutionPlan:
        """Simulates Planner Model decomposing a high-level goal into structured subtasks."""
        subtasks = [
            Subtask(1, "Scan security vulnerabilities in repository.", "scan_security", {"target": "auth-service"}),
            Subtask(2, "Fetch open CVE advisory details.", "fetch_cve", {"cve_id": "CVE-2026-9041"}),
            Subtask(3, "Generate automated patch diff.", "generate_patch", {"cve_id": "CVE-2026-9041"}),
        ]
        return ExecutionPlan(goal=goal, subtasks=subtasks)

    def execute_plan(self, plan: ExecutionPlan) -> Tuple[str, ExecutionPlan]:
        """Executor Model executes subtasks sequentially and handles replanning triggers."""
        for step in plan.subtasks:
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
                    # Trigger replan simulation
                    plan = self._trigger_replan(plan, step)
                    break
                else:
                    step.status = StepStatus.COMPLETED
                    step.result = output
            except Exception:
                step.status = StepStatus.COMPLETED
                step.result = output

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
            tool_name="fetch_cve_mirror",
            tool_args=failed_step.tool_args,
        )
        # Replace failed step with fallback
        idx = plan.subtasks.index(failed_step)
        plan.subtasks[idx] = fallback_step
        return plan


def main() -> None:
    # Mock environment tools
    def scan_security(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "vulnerabilities": ["CVE-2026-9041"], "severity": "HIGH"})

    def fetch_cve(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "cve": args.get("cve_id"), "details": "JWT signature verification bypass."})

    def generate_patch(args: Dict[str, Any]) -> str:
        return json.dumps({"status": "ok", "patch_file": "patch_cve_2026_9041.diff", "lines_changed": 12})

    tools = {
        "scan_security": scan_security,
        "fetch_cve": fetch_cve,
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
