"""Multi-Agent Coordination Patterns: Supervisor, Handoffs, and Agent-as-a-Tool.

Demonstrates three fundamental multi-agent orchestration topologies:
1. Hierarchical Supervisor (Manager-Worker delegation & synthesis)
2. Decentralized Handoffs (Swarm-style peer transfer)
3. Encapsulated Subagent (Agent-as-a-Tool)
"""

from typing import Dict, Any, List, Optional
import json

# 1. AGENT-AS-A-TOOL PATTERN
class SubagentTool:
    """Encapsulates an autonomous subagent within a standard tool interface."""
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def run(self, task_query: str) -> str:
        # Isolated internal reasoning and tool execution
        raw_internal_logs = [f"Scanning repository for '{task_query}'", "Found 4 modules", "Parsed AST"]
        # Returns only concise final synthesis
        return f"[{self.name} summary] Successfully completed query '{task_query}'. Found 0 security regressions."

# 2. PEER HANDOFF PATTERN
class SwarmAgent:
    """Peer agent capable of handling tasks or handing off control to peer agents."""
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

    def respond(self, message: str) -> Dict[str, Any]:
        if "billing" in message.lower() and self.name != "BillingAgent":
            return {"action": "handoff", "target": "BillingAgent", "reason": "Routing payment request."}
        if "tech" in message.lower() and self.name != "TechSupportAgent":
            return {"action": "handoff", "target": "TechSupportAgent", "reason": "Routing technical bug."}
        return {"action": "reply", "content": f"[{self.name}] Resolved: '{message}'"}

def run_swarm_conversation(initial_agent: SwarmAgent, agents: Dict[str, SwarmAgent], message: str) -> str:
    current = initial_agent
    for _ in range(5):  # prevent infinite handoff loops
        res = current.respond(message)
        if res["action"] == "reply":
            return res["content"]
        if res["action"] == "handoff":
            target_name = res["target"]
            current = agents[target_name]
    return "Error: Maximum handoff hops exceeded."

# 3. SUPERVISOR PATTERN
class SupervisorAgent:
    """Central manager delegating sub-tasks and synthesizing results."""
    def __init__(self):
        self.workers = {
            "researcher": SubagentTool("ResearchWorker", "Find documentation and sources."),
            "coder": SubagentTool("CodeWorker", "Write and execute Python code.")
        }

    def execute_workflow(self, user_goal: str) -> Dict[str, Any]:
        # Step 1: Supervisor plans decomposition
        research_task = f"Find API specifications for: {user_goal}"
        coding_task = f"Implement API client based on spec"

        # Step 2: Delegate to isolated workers
        res_output = self.workers["researcher"].run(research_task)
        code_output = self.workers["coder"].run(coding_task)

        # Step 3: Synthesize final output
        final_answer = f"Supervisor resolved '{user_goal}':\n- Research: {res_output}\n- Coding: {code_output}"
        return {
            "status": "COMPLETED",
            "plan": [research_task, coding_task],
            "final_synthesis": final_answer
        }

if __name__ == "__main__":
    print("--- 1. Testing Agent-as-a-Tool ---")
    subagent = SubagentTool("RepoAuditor", "Audit code repositories.")
    tool_result = subagent.run("SQL injection audit")
    print(f"Tool Result: {tool_result}")

    print("\n--- 2. Testing Swarm Peer Handoff ---")
    agents = {
        "TriageAgent": SwarmAgent("TriageAgent", "Triage user queries."),
        "BillingAgent": SwarmAgent("BillingAgent", "Handle invoices and payments."),
        "TechSupportAgent": SwarmAgent("TechSupportAgent", "Handle bug reports.")
    }
    msg = "I need an invoice refund for my monthly subscription."
    swarm_result = run_swarm_conversation(agents["TriageAgent"], agents, msg)
    print(f"Swarm Result: {swarm_result}")

    print("\n--- 3. Testing Supervisor (Manager-Worker) ---")
    supervisor = SupervisorAgent()
    sup_result = supervisor.execute_workflow("Build Stripe webhook parser")
    print(f"Supervisor Result Status: {sup_result['status']}")
    print(sup_result["final_synthesis"])
