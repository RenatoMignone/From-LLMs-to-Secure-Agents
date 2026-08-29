#!/usr/bin/env python3
"""
Reflexion and Evaluator-Optimizer Agent Runner
Demonstrates generator-evaluator refinement loops, verbal reflection memory,
and bounded replanning on failed validation criteria.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import json
from typing import Any, Dict, List, Optional, Tuple


class EvaluationStatus(Enum):
    PENDING = auto()
    NEEDS_REFINEMENT = auto()
    APPROVED = auto()
    FAILED_MAX_ITERATIONS = auto()


@dataclass
class CandidateDraft:
    iteration: int
    content: str
    rationale: str


@dataclass
class EvaluationRubric:
    syntax_valid: bool
    correctness_score: float  # 0.0 to 1.0
    safety_check_passed: bool
    critique: str

    @property
    def passed(self) -> bool:
        return self.syntax_valid and self.correctness_score >= 0.8 and self.safety_check_passed


@dataclass
class ReflexionMemory:
    reflections: List[str] = field(default_factory=list)

    def add_reflection(self, iteration: int, critique: str, lesson: str) -> None:
        self.reflections.append(f"[Trial {iteration}] Critique: {critique} -> Actionable Rule: {lesson}")

    def formatted_context(self) -> str:
        if not self.reflections:
            return "No previous reflections recorded."
        return "\n".join(self.reflections)


class EvaluatorOptimizerAgent:
    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self.memory = ReflexionMemory()

    def generate_candidate(self, task: str, iteration: int) -> CandidateDraft:
        """Simulates Generator / Optimizer producing a solution informed by past reflections."""
        if iteration == 1:
            # Initial naive attempt (unparameterized query)
            content = "SELECT * FROM users WHERE tenant_id = '" + "{tenant_id}" + "' AND role = '" + "{role}" + "';"
            rationale = "Direct SQL string interpolation based on input parameters."
        elif iteration == 2:
            # Refined attempt addressing parameter binding
            content = "SELECT id, username, email FROM users WHERE tenant_id = :tenant_id AND role = :role LIMIT 100;"
            rationale = "Parameterized query preventing injection, restricted columns, and bounded result limit."
        else:
            content = "SELECT id, username, email FROM users WHERE tenant_id = :tenant_id AND role = :role LIMIT 50;"
            rationale = "Further bounded result limit and strict parameterized query."

        return CandidateDraft(iteration=iteration, content=content, rationale=rationale)

    def evaluate_candidate(self, draft: CandidateDraft, task: str) -> EvaluationRubric:
        """Simulates Evaluator / Critic assessing candidate against explicit criteria."""
        if "{" in draft.content and "}" in draft.content and ":" not in draft.content:
            # Unescaped string interpolation detected
            return EvaluationRubric(
                syntax_valid=True,
                correctness_score=0.6,
                safety_check_passed=False,
                critique="Direct string interpolation introduces SQL injection risks. Must use parameterized binding (:param).",
            )
        elif "*" in draft.content:
            return EvaluationRubric(
                syntax_valid=True,
                correctness_score=0.75,
                safety_check_passed=True,
                critique="Wildcard SELECT * exposes unnecessary columns. Specify explicit required column names.",
            )
        else:
            return EvaluationRubric(
                syntax_valid=True,
                correctness_score=1.0,
                safety_check_passed=True,
                critique="All criteria met: parameterized binding, explicit column selection, and bounded query.",
            )

    def reflect_on_failure(self, draft: CandidateDraft, rubric: EvaluationRubric) -> str:
        """Simulates Self-Reflection generating an actionable episodic lesson."""
        if not rubric.safety_check_passed:
            return "Never use string formatting for database filters; always enforce parameterized statement placeholders."
        elif rubric.correctness_score < 0.8:
            return "Explicitly list required column names to avoid leaking schema or extraneous sensitive attributes."
        return "Refine query structure to adhere strictly to safety and performance bounds."

    def run(self, task: str) -> Tuple[EvaluationStatus, CandidateDraft, List[Dict[str, Any]]]:
        trace = []
        status = EvaluationStatus.PENDING

        for iteration in range(1, self.max_iterations + 1):
            draft = self.generate_candidate(task, iteration)
            rubric = self.evaluate_candidate(draft, task)

            step_record = {
                "iteration": iteration,
                "candidate": draft.content,
                "rationale": draft.rationale,
                "passed": rubric.passed,
                "critique": rubric.critique,
                "reflections_before": self.memory.reflections.copy(),
            }

            if rubric.passed:
                status = EvaluationStatus.APPROVED
                trace.append(step_record)
                return status, draft, trace

            # Generate verbal reflection and store in working memory
            lesson = self.reflect_on_failure(draft, rubric)
            self.memory.add_reflection(iteration, rubric.critique, lesson)
            step_record["lesson_learned"] = lesson
            trace.append(step_record)

        status = EvaluationStatus.FAILED_MAX_ITERATIONS
        return status, draft, trace


def main() -> None:
    task = "Generate a secure database query to fetch active user records filtered by tenant_id and role."
    agent = EvaluatorOptimizerAgent(max_iterations=3)

    print("=" * 80)
    print("REFLEXION & EVALUATOR-OPTIMIZER WORKFLOW TRACE")
    print("=" * 80)
    print(f"Task: {task}\n")

    status, final_draft, trace = agent.run(task)

    for step in trace:
        print(f"--- Iteration {step['iteration']} ---")
        print(f"Candidate: {step['candidate']}")
        print(f"Rationale: {step['rationale']}")
        print(f"Evaluator Critique: {step['critique']}")
        print(f"Status: {'PASSED' if step['passed'] else 'NEEDS REFINEMENT'}")
        if not step["passed"]:
            print(f"Reflected Lesson: {step.get('lesson_learned')}")
        print()

    print("=" * 80)
    print(f"FINAL RESULT STATUS: {status.name}")
    print(f"APPROVED CANDIDATE: {final_draft.content}")
    print("=" * 80)
    print("ACCUMULATED VERBAL REFLECTION MEMORY:")
    print(agent.memory.formatted_context())
    print("=" * 80)


if __name__ == "__main__":
    main()
