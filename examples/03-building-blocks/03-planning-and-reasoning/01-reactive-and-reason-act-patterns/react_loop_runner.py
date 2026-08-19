#!/usr/bin/env python3
"""
ReAct (Reason-Act-Observe) Loop Runner
Demonstrates explicit Thought-Action-Observation trajectories,
loop cycle bounds, tool error recovery, and termination criteria.
"""

from dataclasses import dataclass, field
import json
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class ToolDefinition:
    name: str
    description: str
    func: Callable[[Dict[str, Any]], str]


@dataclass
class AgentStep:
    step_number: int
    thought: str
    action_name: Optional[str]
    action_input: Optional[Dict[str, Any]]
    observation: Optional[str]
    is_final: bool = False
    final_answer: Optional[str] = None


class EnvironmentTools:
    """Mock sandbox environment tools."""
    @staticmethod
    def search_company_registry(args: Dict[str, Any]) -> str:
        name = args.get("name", "").lower()
        if "acme" in name:
            return json.dumps({"status": "found", "id": "REG-8081", "jurisdiction": "Delaware", "founded": 2018})
        return json.dumps({"status": "not_found", "error": f"No entity matching '{name}'"})

    @staticmethod
    def query_compliance_filings(args: Dict[str, Any]) -> str:
        reg_id = args.get("reg_id", "")
        if reg_id == "REG-8081":
            return json.dumps({"active_filings": ["2025-Q4-Report", "2026-Annual-Audit"], "compliance_score": 0.98})
        return json.dumps({"error": f"Invalid registration ID: {reg_id}"})


class ReActAgent:
    def __init__(self, tools: Dict[str, ToolDefinition], max_iterations: int = 5):
        self.tools = tools
        self.max_iterations = max_iterations
        self.history: List[AgentStep] = []

    def run(self, user_goal: str) -> Tuple[str, List[AgentStep]]:
        """
        Executes the ReAct loop:
        Thought -> Action -> Execution Boundary -> Observation -> Repeat until Final Answer.
        """
        step_idx = 1
        known_state: Dict[str, Any] = {}

        while step_idx <= self.max_iterations:
            # 1. Thought Phase (Simulated model reasoning step)
            if step_idx == 1:
                thought = "To verify compliance, I first need to find Acme's official corporate registration ID."
                action_name = "search_registry"
                action_input = {"name": "Acme Corp"}
            elif step_idx == 2:
                reg_id = known_state.get("reg_id")
                thought = f"Registration ID identified as {reg_id}. Now I must query compliance filings for this ID."
                action_name = "query_filings"
                action_input = {"reg_id": reg_id}
            else:
                score = known_state.get("compliance_score", "N/A")
                thought = f"All required data retrieved. Compliance score is {score}. I can now synthesize the final verdict."
                action_name = None
                action_input = None

            # 2. Action & Observation Phase
            if action_name:
                tool = self.tools.get(action_name)
                if not tool:
                    obs = f"Error: Unknown tool '{action_name}'"
                else:
                    obs = tool.func(action_input or {})
                    # Update simulated state
                    try:
                        parsed = json.loads(obs)
                        if "id" in parsed:
                            known_state["reg_id"] = parsed["id"]
                        if "compliance_score" in parsed:
                            known_state["compliance_score"] = parsed["compliance_score"]
                    except Exception:
                        pass

                step = AgentStep(
                    step_number=step_idx,
                    thought=thought,
                    action_name=action_name,
                    action_input=action_input,
                    observation=obs,
                )
                self.history.append(step)
                step_idx += 1
            else:
                # 3. Final Answer / Termination Phase
                final_answer = (
                    f"Acme Corp (ID: {known_state.get('reg_id')}) is in full compliance with a score of "
                    f"{known_state.get('compliance_score') * 100:.0f}%."
                )
                step = AgentStep(
                    step_number=step_idx,
                    thought=thought,
                    action_name=None,
                    action_input=None,
                    observation=None,
                    is_final=True,
                    final_answer=final_answer,
                )
                self.history.append(step)
                return final_answer, self.history

        return "Error: Maximum iteration limit reached without resolution.", self.history


def main() -> None:
    env = EnvironmentTools()
    tools = {
        "search_registry": ToolDefinition("search_registry", "Searches entity registry", env.search_company_registry),
        "query_filings": ToolDefinition("query_filings", "Queries regulatory filings", env.query_compliance_filings),
    }

    agent = ReActAgent(tools=tools, max_iterations=4)
    goal = "Verify current regulatory compliance status for Acme Corp."

    print("=" * 80)
    print(f"REACT LOOP EXECUTION TRACE: '{goal}'")
    print("=" * 80)

    final_answer, steps = agent.run(goal)

    for step in steps:
        print(f"\n[STEP {step.step_number}]")
        print(f"THOUGHT:     {step.thought}")
        if step.action_name:
            print(f"ACTION:      {step.action_name}({json.dumps(step.action_input)})")
            print(f"OBSERVATION: {step.observation}")
        if step.is_final:
            print(f"FINAL ANSWER:\n{step.final_answer}")
    print("=" * 80)


if __name__ == "__main__":
    main()
