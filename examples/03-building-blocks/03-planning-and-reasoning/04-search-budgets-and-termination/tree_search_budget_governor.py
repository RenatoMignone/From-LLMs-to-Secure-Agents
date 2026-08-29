#!/usr/bin/env python3
"""
Tree Search and Execution Budget Governor
Demonstrates deliberate Tree-of-Thoughts exploration, candidate branch evaluation,
heuristic pruning, multi-dimensional search budgets, and deterministic termination.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import time
from typing import Dict, List, Optional, Tuple


class TerminationReason(Enum):
    SUCCESS = auto()
    BUDGET_DEPTH_EXCEEDED = auto()
    BUDGET_TOKENS_EXCEEDED = auto()
    BUDGET_NODES_EXCEEDED = auto()
    NO_VIABLE_PATHS = auto()
    CYCLE_DETECTED = auto()


@dataclass
class SearchNode:
    node_id: str
    thought: str
    depth: int
    score: float  # 0.0 to 1.0 heuristic quality score
    parent_id: Optional[str] = None
    accumulated_cost_tokens: int = 0


@dataclass
class SearchBudget:
    max_depth: int = 3
    max_nodes_expanded: int = 10
    max_token_budget: int = 1500
    branching_factor: int = 2


class TreeSearchGovernor:
    def __init__(self, budget: SearchBudget):
        self.budget = budget
        self.tokens_used = 0
        self.nodes_expanded = 0
        self.seen_thoughts: set[str] = set()

    def generate_candidate_thoughts(self, current_node: SearchNode) -> List[SearchNode]:
        """Simulates LLM generating branching thought candidates."""
        depth = current_node.depth + 1
        candidates = []

        if depth == 1:
            candidates = [
                SearchNode(
                    node_id=f"{current_node.node_id}.1",
                    thought="Decompose security review into static analysis and dynamic token verification.",
                    depth=depth,
                    score=0.9,
                    parent_id=current_node.node_id,
                    accumulated_cost_tokens=180,
                ),
                SearchNode(
                    node_id=f"{current_node.node_id}.2",
                    thought="Immediately execute raw remediation scripts on production servers without checking.",
                    depth=depth,
                    score=0.1,  # Flawed / Unsafe
                    parent_id=current_node.node_id,
                    accumulated_cost_tokens=150,
                ),
            ]
        elif depth == 2:
            candidates = [
                SearchNode(
                    node_id=f"{current_node.node_id}.1",
                    thought="Run AST parser on auth modules to verify parameterized SQL statement usage.",
                    depth=depth,
                    score=0.95,
                    parent_id=current_node.node_id,
                    accumulated_cost_tokens=220,
                ),
                SearchNode(
                    node_id=f"{current_node.node_id}.2",
                    thought="Disable authentication filters temporarily to speed up load testing.",
                    depth=depth,
                    score=0.05,  # Unsafe branch
                    parent_id=current_node.node_id,
                    accumulated_cost_tokens=190,
                ),
            ]
        elif depth == 3:
            candidates = [
                SearchNode(
                    node_id=f"{current_node.node_id}.1",
                    thought="Emit verified security audit report confirming zero SQL injection vulnerabilities.",
                    depth=depth,
                    score=1.0,  # Solution goal met
                    parent_id=current_node.node_id,
                    accumulated_cost_tokens=240,
                )
            ]

        return candidates[: self.budget.branching_factor]

    def search(self, initial_goal: str) -> Tuple[TerminationReason, Optional[SearchNode], List[Dict[str, any]]]:
        root = SearchNode(
            node_id="0",
            thought=f"Goal: {initial_goal}",
            depth=0,
            score=1.0,
            accumulated_cost_tokens=50,
        )
        self.tokens_used += root.accumulated_cost_tokens
        self.seen_thoughts.add(root.thought)

        frontier: List[SearchNode] = [root]
        trace: List[Dict[str, any]] = []

        while frontier:
            # Best-First Search: pop candidate with highest heuristic score
            frontier.sort(key=lambda n: n.score, reverse=True)
            current = frontier.pop(0)
            self.nodes_expanded += 1

            trace_entry = {
                "expanded_node_id": current.node_id,
                "depth": current.depth,
                "thought": current.thought,
                "score": current.score,
                "tokens_used": self.tokens_used,
                "nodes_expanded": self.nodes_expanded,
            }

            # Check solution goal condition (score == 1.0 and depth == max_depth)
            if current.score >= 0.99 and current.depth >= 2:
                trace_entry["action"] = "GOAL_REACHED"
                trace.append(trace_entry)
                return TerminationReason.SUCCESS, current, trace

            # Check multi-dimensional budget constraints
            if current.depth >= self.budget.max_depth:
                trace_entry["action"] = "PRUNED_MAX_DEPTH"
                trace.append(trace_entry)
                continue

            if self.nodes_expanded >= self.budget.max_nodes_expanded:
                trace_entry["action"] = "HALTED_MAX_NODES"
                trace.append(trace_entry)
                return TerminationReason.BUDGET_NODES_EXCEEDED, current, trace

            # Generate child thought candidates
            children = self.generate_candidate_thoughts(current)

            for child in children:
                self.tokens_used += child.accumulated_cost_tokens

                if self.tokens_used > self.budget.max_token_budget:
                    trace_entry["action"] = "HALTED_TOKEN_BUDGET"
                    trace.append(trace_entry)
                    return TerminationReason.BUDGET_TOKENS_EXCEEDED, current, trace

                if child.thought in self.seen_thoughts:
                    continue  # Loop / Cycle prevention

                # Heuristic pruning threshold: reject low-scoring dead-end branches
                if child.score < 0.5:
                    trace.append({
                        "pruned_node_id": child.node_id,
                        "depth": child.depth,
                        "thought": child.thought,
                        "score": child.score,
                        "action": "PRUNED_LOW_SCORE",
                    })
                    continue

                self.seen_thoughts.add(child.thought)
                frontier.append(child)

            trace_entry["action"] = f"EXPANDED_FRONTIER_SIZE_{len(frontier)}"
            trace.append(trace_entry)

        return TerminationReason.NO_VIABLE_PATHS, None, trace


def main() -> None:
    goal = "Perform end-to-end security verification on customer auth service."
    budget = SearchBudget(max_depth=3, max_nodes_expanded=8, max_token_budget=1200, branching_factor=2)
    governor = TreeSearchGovernor(budget)

    print("=" * 80)
    print("TREE OF THOUGHTS SEARCH GOVERNOR TRACE")
    print("=" * 80)
    print(f"Goal: {goal}")
    print(f"Budgets: Max Depth={budget.max_depth}, Max Tokens={budget.max_token_budget}, Max Nodes={budget.max_nodes_expanded}\n")

    reason, final_node, trace = governor.search(goal)

    for step in trace:
        node_id = step.get("expanded_node_id") or step.get("pruned_node_id")
        action = step.get("action")
        score = step.get("score")
        print(f"[{action}] Node {node_id} (Depth {step.get('depth')}, Score {score:.2f})")
        print(f"  Thought: {step.get('thought')}")
        if "tokens_used" in step:
            print(f"  Cumulative Cost: {step.get('tokens_used')} tokens | {step.get('nodes_expanded')} nodes expanded")
        print()

    print("=" * 80)
    print(f"TERMINATION REASON: {reason.name}")
    if final_node:
        print(f"SELECTED OPTIMAL PATH NODE: {final_node.node_id}")
        print(f"FINAL SYNTHESIS: {final_node.thought}")
    print(f"TOTAL TOKENS CONSUMED: {governor.tokens_used} / {budget.max_token_budget}")
    print("=" * 80)


if __name__ == "__main__":
    main()
