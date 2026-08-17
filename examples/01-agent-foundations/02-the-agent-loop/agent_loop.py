"""Minimal framework-free typed agent loop implementation.

Demonstrates context assembly, model inference simulation, tool dispatch,
schema error handling, and turn budget termination.
"""

from dataclasses import dataclass
import json
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., str]


class MockModelClient:
    """Simulates a language model responding to structured tool loop history."""

    def __init__(self, script: Optional[List[str]] = None):
        self.script = script or []
        self.call_count = 0

    def predict(self, history: List[Dict[str, str]]) -> str:
        if self.call_count < len(self.script):
            response = self.script[self.call_count]
            self.call_count += 1
            return response

        # Default fallback response
        last_msg = history[-1]["content"] if history else ""
        if "500 Internal Error" in last_msg:
            return json.dumps({"tool": "restart_service", "args": {"service": "nginx"}})
        elif "restarted successfully" in last_msg:
            return "FINAL: Service recovered successfully."
        return json.dumps({"tool": "ping_server", "args": {"host": "web-01"}})


class AgentRuntime:
    def __init__(self, tools: List[Tool], max_turns: int = 5):
        self.tools: Dict[str, Tool] = {t.name: t for t in tools}
        self.max_turns = max_turns

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        if tool_name not in self.tools:
            return f"ERROR: Tool '{tool_name}' is not registered."
        try:
            return self.tools[tool_name].func(**arguments)
        except Exception as e:
            return f"ERROR: Tool execution failed with exception: {str(e)}"

    def run(self, goal: str, model_client: Any) -> str:
        history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": "You solve tasks step by step using tools. When finished, start your reply with 'FINAL:'.",
            },
            {"role": "user", "content": goal},
        ]

        for turn in range(1, self.max_turns + 1):
            # 1. Model inference
            response = model_client.predict(history)

            # 2. Check for completion
            if response.startswith("FINAL:"):
                return response.replace("FINAL:", "").strip()

            # 3. Parse action request
            try:
                action = json.loads(response)
                tool_name = action.get("tool")
                args = action.get("args", {})
            except json.JSONDecodeError:
                observation = "ERROR: Output must be valid JSON tool call or start with 'FINAL:'."
                history.append({"role": "assistant", "content": response})
                history.append({"role": "user", "content": f"Observation: {observation}"})
                continue

            # 4. Execute tool across boundary
            observation = self.execute_tool(tool_name, args)

            # 5. Append to history for next turn
            history.append({"role": "assistant", "content": response})
            history.append({"role": "user", "content": f"Observation: {observation}"})

        return "ERROR: Maximum turn budget exhausted without completion."


def main() -> None:
    # Set up mock environment tools
    server_state = {"status": "500 Internal Error", "restarted": False}

    def ping_server(host: str) -> str:
        if server_state["restarted"]:
            return f"Host {host} is healthy (HTTP 200 OK)."
        return f"Host {host} status: {server_state['status']}."

    def restart_service(service: str) -> str:
        server_state["restarted"] = True
        return f"Service {service} restarted successfully."

    tools = [
        Tool("ping_server", "Checks server health status", ping_server),
        Tool("restart_service", "Restarts a named system service", restart_service),
    ]

    runtime = AgentRuntime(tools=tools, max_turns=5)
    model = MockModelClient()

    result = runtime.run("Check server status and restart if down", model)
    print("Agent Execution Result:", result)


if __name__ == "__main__":
    main()
