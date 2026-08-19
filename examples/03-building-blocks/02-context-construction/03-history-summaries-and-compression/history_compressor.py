#!/usr/bin/env python3
"""
History Summarization and Context Compression Engine
Demonstrates sliding-window FIFO trimming, tool output compaction,
and rolling summary buffer memory management for long-running agent loops.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json


@dataclass
class MessageTurn:
    role: str
    content: str
    is_tool: bool = False
    tokens: int = 0

    def __post_init__(self):
        if self.tokens == 0:
            self.tokens = max(1, len(self.content) // 4)


class HistoryManager:
    def __init__(self, max_buffer_tokens: int = 150, keep_recent_turns: int = 2):
        self.max_buffer_tokens = max_buffer_tokens
        self.keep_recent_turns = keep_recent_turns
        self.turns: List[MessageTurn] = []
        self.current_summary: str = ""

    def add_turn(self, role: str, content: str, is_tool: bool = False) -> None:
        self.turns.append(MessageTurn(role=role, content=content, is_tool=is_tool))

    def compact_tool_output(self, raw_json_str: str, key_fields: List[str]) -> str:
        """Losslessly compresses verbose tool output to essential keys only."""
        try:
            data = json.loads(raw_json_str)
            if isinstance(data, dict):
                # If dict contains a list of records (e.g. branch_data)
                for k, v in data.items():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        compacted_list = [{f: item.get(f) for f in key_fields if f in item} for item in v]
                        return json.dumps({k: compacted_list}, indent=2)
                compacted = {k: data.get(k) for k in key_fields if k in data}
                return json.dumps(compacted, indent=2)
            elif isinstance(data, list):
                compacted = [{f: item.get(f) for f in key_fields if f in item} for item in data[:3]]
                return json.dumps(compacted, indent=2)
        except Exception:
            pass
        return raw_json_str[:200] + "... [truncated]"

    def total_tokens(self) -> int:
        summary_tokens = len(self.current_summary) // 4 if self.current_summary else 0
        return summary_tokens + sum(t.tokens for t in self.turns)

    def trigger_compaction_if_needed(self) -> bool:
        """Condenses older turns into a rolling state summary when token limit is breached."""
        if self.total_tokens() <= self.max_buffer_tokens or len(self.turns) <= self.keep_recent_turns:
            return False

        turns_to_summarize = self.turns[:-self.keep_recent_turns]
        preserved_turns = self.turns[-self.keep_recent_turns:]

        summary_bullet_points = []
        for t in turns_to_summarize:
            prefix = f"{t.role.upper()}" + (" [TOOL]" if t.is_tool else "")
            first_line = t.content.split("\n")[0][:75]
            summary_bullet_points.append(f"- {prefix}: {first_line}")

        new_summary_chunk = "\n".join(summary_bullet_points)
        if self.current_summary:
            self.current_summary += "\n" + new_summary_chunk
        else:
            self.current_summary = "# CONVERSATION STATE SUMMARY (ARCHIVED TURNS):\n" + new_summary_chunk

        self.turns = preserved_turns
        return True

    def get_serialized_history(self) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        if self.current_summary:
            result.append({"role": "system", "content": self.current_summary})
        for t in self.turns:
            result.append({"role": t.role, "content": t.content})
        return result


def main() -> None:
    history = HistoryManager(max_buffer_tokens=150, keep_recent_turns=2)

    print("=" * 75)
    print("SIMULATING MULTI-TURN AGENT EXECUTION WITH ROLLING SUMMARY BUFFER")
    print("=" * 75)

    # Turn 1-2: Initial query and search
    history.add_turn("user", "Analyze Q3 revenue anomalies for European branches across all active regions.")
    history.add_turn("assistant", "Querying central database for European financial records and regional audits.")

    # Turn 3: Large tool output
    raw_verbose_tool_output = (
        '{"status": "ok", "query_time_ms": 420, "branch_data": ['
        '{"id": "EU-01", "city": "Berlin", "revenue": 1420000, "anomaly": false, "raw_debug_trace": "0x4FA3B"},'
        '{"id": "EU-02", "city": "Madrid", "revenue": 390000, "anomaly": true, "raw_debug_trace": "0x98FF1"},'
        '{"id": "EU-03", "city": "Paris", "revenue": 1890000, "anomaly": false, "raw_debug_trace": "0x112A0"}'
        ']}'
    )
    compacted_tool = history.compact_tool_output(raw_verbose_tool_output, ["city", "revenue", "anomaly"])
    history.add_turn("tool", compacted_tool, is_tool=True)

    # Turn 4-5: Synthesis and follow-up
    history.add_turn("assistant", "Madrid branch flagged with revenue anomaly ($390k vs expected $1.2M).")
    history.add_turn("user", "Fetch detailed audit logs for Madrid store manager.")

    # Turn 6: Manager audit query
    history.add_turn("assistant", "Calling audit log retrieval API for manager ID MGR-9941.")

    print(f"Pre-compaction Turn Count: {len(history.turns)}")
    print(f"Pre-compaction Tokens:     {history.total_tokens()} / {history.max_buffer_tokens}")

    compacted = history.trigger_compaction_if_needed()
    print(f"\nCompaction Triggered:      {compacted}")
    print(f"Post-compaction Turn Count: {len(history.turns)} (plus archived summary)")
    print(f"Post-compaction Tokens:    {history.total_tokens()} / {history.max_buffer_tokens}")

    print("-" * 75)
    print("FINAL SERIALIZED PROMPT HISTORY:\n")
    for msg in history.get_serialized_history():
        print(f"[{msg['role'].upper()}]:")
        print(msg['content'])
        print()
    print("=" * 75)


if __name__ == "__main__":
    main()
