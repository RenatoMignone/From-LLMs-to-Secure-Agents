#!/usr/bin/env python3
"""Working Memory and Short-Term Context Management Runtime.

Demonstrates:
1. In-context structured scratchpad for active task state and intermediate variables.
2. Sliding dialogue buffer with token threshold enforcement.
3. Progressive rolling summarization for old conversation turns.
4. Ephemeral tool observation trimming to prevent context bloat.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional


@dataclass
class WorkingScratchpad:
    """In-context scratchpad maintaining active goal and working variables."""

    task_goal: str
    active_subgoals: List[str] = field(default_factory=list)
    completed_subgoals: List[str] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value
        self.last_updated = datetime.now(timezone.utc)

    def complete_subgoal(self, subgoal: str) -> None:
        if subgoal in self.active_subgoals:
            self.active_subgoals.remove(subgoal)
        if subgoal not in self.completed_subgoals:
            self.completed_subgoals.append(subgoal)
        self.last_updated = datetime.now(timezone.utc)

    def render(self) -> str:
        lines = [
            "=== ACTIVE WORKING SCRATCHPAD ===",
            f"Goal: {self.task_goal}",
            f"Active Subgoals: {', '.join(self.active_subgoals) if self.active_subgoals else 'None'}",
            f"Completed Subgoals: {', '.join(self.completed_subgoals) if self.completed_subgoals else 'None'}",
            "Working Variables:",
        ]
        for k, v in self.variables.items():
            lines.append(f"  - {k}: {v}")
        return "\n".join(lines)


@dataclass
class Message:
    role: str
    content: str
    token_estimate: int = 0
    is_tool_output: bool = False

    def __post_init__(self) -> None:
        if not self.token_estimate:
            # Approximate heuristic: 1 token ≈ 4 characters
            self.token_estimate = max(1, len(self.content) // 4)


class ShortTermMemoryManager:
    """Manages short-term conversation history and working memory budgeting."""

    def __init__(
        self,
        system_prompt: str,
        max_total_tokens: int = 1000,
        max_scratchpad_tokens: int = 300,
        max_dialogue_tokens: int = 500,
    ) -> None:
        self.system_prompt = system_prompt
        self.max_total_tokens = max_total_tokens
        self.max_scratchpad_tokens = max_scratchpad_tokens
        self.max_dialogue_tokens = max_dialogue_tokens

        self.scratchpad: Optional[WorkingScratchpad] = None
        self.rolling_summary: str = ""
        self.dialogue_history: List[Message] = []

    def set_scratchpad(self, scratchpad: WorkingScratchpad) -> None:
        self.scratchpad = scratchpad

    def add_message(self, role: str, content: str, is_tool_output: bool = False) -> None:
        msg = Message(role=role, content=content, is_tool_output=is_tool_output)
        self.dialogue_history.append(msg)
        self._enforce_dialogue_budget()

    def prune_tool_observations(self) -> int:
        """Compress or trim verbose raw tool outputs into compact status notes."""
        pruned_count = 0
        for msg in self.dialogue_history:
            if msg.is_tool_output and len(msg.content) > 100:
                summary_note = f"[Tool output compacted: {msg.content[:60]}... (raw payload cleared)]"
                msg.content = summary_note
                msg.token_estimate = max(1, len(summary_note) // 4)
                pruned_count += 1
        return pruned_count

    def _enforce_dialogue_budget(self) -> None:
        """Evicts older messages or triggers rolling summarization when over budget."""
        current_tokens = sum(m.token_estimate for m in self.dialogue_history)
        if current_tokens <= self.max_dialogue_tokens:
            return

        # Evict oldest dialogue turns into rolling summary
        while current_tokens > self.max_dialogue_tokens and len(self.dialogue_history) > 2:
            oldest = self.dialogue_history.pop(0)
            # Append salient excerpt to rolling summary
            summary_addition = f"[{oldest.role}: {oldest.content[:50]}]"
            if not self.rolling_summary:
                self.rolling_summary = f"Summary of earlier turns: {summary_addition}"
            else:
                self.rolling_summary += f" -> {summary_addition}"
            current_tokens = sum(m.token_estimate for m in self.dialogue_history)

    def assemble_context_window(self) -> str:
        """Compiles the full context window with system prompt, scratchpad, summary, and dialogue."""
        sections = [
            "=== SYSTEM PROMPT ===",
            self.system_prompt,
        ]

        if self.scratchpad:
            sections.append(self.scratchpad.render())

        if self.rolling_summary:
            sections.append(f"=== PROGRESSIVE SUMMARY ===\n{self.rolling_summary}")

        sections.append("=== RECENT DIALOGUE ===")
        for msg in self.dialogue_history:
            sections.append(f"{msg.role.upper()}: {msg.content}")

        return "\n\n".join(sections)


def run_demonstration() -> None:
    print("=" * 65)
    print("  Demonstration: Working Memory & Short-Term Context Management")
    print("=" * 65)

    manager = ShortTermMemoryManager(
        system_prompt="You are a data validation agent. Follow step-by-step instructions.",
        max_total_tokens=600,
        max_dialogue_tokens=250,
    )

    # 1. Initialize working scratchpad
    scratchpad = WorkingScratchpad(
        task_goal="Ingest and clean daily customer telemetry data",
        active_subgoals=["Download S3 payload", "Schema validation", "Deduplicate records"],
    )
    manager.set_scratchpad(scratchpad)

    # 2. Simulate step 1 execution
    manager.add_message("user", "Start daily telemetry pipeline run for partition 2026-08-31.")
    manager.add_message("assistant", "Downloading partition payload from s3://telemetry/2026-08-31.json...")

    raw_tool_payload = json.dumps({"status": "ok", "records_count": 14500, "checksum": "a8f9c1b", "sample": [{"id": 1, "val": 42}] * 20})
    manager.add_message("tool", raw_tool_payload, is_tool_output=True)

    # 3. Agent updates scratchpad and prunes verbose tool output
    scratchpad.update_variable("records_ingested", 14500)
    scratchpad.update_variable("s3_checksum", "a8f9c1b")
    scratchpad.complete_subgoal("Download S3 payload")
    manager.prune_tool_observations()

    # 4. Multi-turn dialogue causing window eviction and summarization
    manager.add_message("assistant", "S3 download verified (14,500 records). Now running schema validation.")
    manager.add_message("user", "Ensure null email fields are flagged as warnings, not errors.")
    manager.add_message("assistant", "Understood. Updating schema rule to flag null emails as warnings.")

    scratchpad.update_variable("null_email_policy", "warning")
    scratchpad.complete_subgoal("Schema validation")

    # 5. Render assembled context window
    print("\n--> Assembled Context Window:\n")
    print(manager.assemble_context_window())

    print("\n[✓] Short-term working memory lifecycle demonstrated successfully.")


if __name__ == "__main__":
    run_demonstration()
