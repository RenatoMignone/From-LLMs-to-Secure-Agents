import importlib.util
import json
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path(__file__).parents[1] / "agent_loop.py"
SPEC = importlib.util.spec_from_file_location("agent_loop", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

AgentRuntime = MODULE.AgentRuntime
Tool = MODULE.Tool
MockModelClient = MODULE.MockModelClient


class TestAgentLoop(unittest.TestCase):
    def setUp(self):
        self.tools = [
            Tool("echo", "Echoes input text", lambda text="": f"Echo: {text}"),
            Tool("failing_tool", "Always raises an error", lambda: 1 / 0),
        ]
        self.runtime = AgentRuntime(tools=self.tools, max_turns=3)

    def test_successful_final_completion(self):
        model = MockModelClient(script=["FINAL: Task accomplished directly."])
        result = self.runtime.run("Simple goal", model)
        self.assertEqual(result, "Task accomplished directly.")

    def test_multi_turn_tool_execution(self):
        script = [
            json.dumps({"tool": "echo", "args": {"text": "hello"}}),
            "FINAL: Received echo observation.",
        ]
        model = MockModelClient(script=script)
        result = self.runtime.run("Echo test", model)
        self.assertEqual(result, "Received echo observation.")

    def test_unknown_tool_handling(self):
        script = [
            json.dumps({"tool": "unregistered_tool", "args": {}}),
            "FINAL: Handled missing tool.",
        ]
        model = MockModelClient(script=script)
        result = self.runtime.run("Missing tool test", model)
        self.assertEqual(result, "Handled missing tool.")

    def test_malformed_json_recovery(self):
        script = [
            "THIS IS NOT VALID JSON",
            "FINAL: Recovered from malformed output.",
        ]
        model = MockModelClient(script=script)
        result = self.runtime.run("Malformed output test", model)
        self.assertEqual(result, "Recovered from malformed output.")

    def test_turn_budget_exhaustion(self):
        script = [
            json.dumps({"tool": "echo", "args": {"text": "1"}}),
            json.dumps({"tool": "echo", "args": {"text": "2"}}),
            json.dumps({"tool": "echo", "args": {"text": "3"}}),
            json.dumps({"tool": "echo", "args": {"text": "4"}}),
        ]
        model = MockModelClient(script=script)
        result = self.runtime.run("Infinite loop test", model)
        self.assertIn("Maximum turn budget exhausted", result)


if __name__ == "__main__":
    unittest.main()
