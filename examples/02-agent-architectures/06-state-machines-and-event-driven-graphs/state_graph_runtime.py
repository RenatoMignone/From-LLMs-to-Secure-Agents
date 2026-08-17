"""Minimal State Graph and Durable Checkpoint Engine.

Demonstrates an event-driven state graph with typed state schema,
conditional routing edges, node transitions, and human-in-the-loop interruption.
"""

from typing import Dict, Any, List, Callable, Optional
import json

class GraphState:
    """Explicit typed state container flowing across graph nodes."""
    def __init__(self, messages: Optional[List[Dict[str, str]]] = None, variables: Optional[Dict[str, Any]] = None):
        self.messages = messages or []
        self.variables = variables or {}
        self.current_node: str = "START"
        self.status: str = "INITIALIZED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "messages": self.messages,
            "variables": self.variables,
            "current_node": self.current_node,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraphState':
        state = cls(data.get("messages"), data.get("variables"))
        state.current_node = data.get("current_node", "START")
        state.status = data.get("status", "INITIALIZED")
        return state

class StateGraphEngine:
    """Deterministic cyclic graph runner with checkpointing and interruption gates."""
    def __init__(self):
        self.nodes: Dict[str, Callable[[GraphState], GraphState]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[GraphState], str]] = {}
        self.interrupt_before: List[str] = []
        self.checkpoints: Dict[str, str] = {}  # checkpoint_id -> serialized json

    def add_node(self, name: str, func: Callable[[GraphState], GraphState]):
        self.nodes[name] = func

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edges(self, from_node: str, router_func: Callable[[GraphState], str]):
        self.conditional_edges[from_node] = router_func

    def set_interrupt_before(self, node_names: List[str]):
        self.interrupt_before = node_names

    def save_checkpoint(self, thread_id: str, step: int, state: GraphState) -> str:
        checkpoint_id = f"{thread_id}-step-{step}"
        self.checkpoints[checkpoint_id] = json.dumps(state.to_dict())
        return checkpoint_id

    def run(self, initial_state: GraphState, thread_id: str = "default_thread", max_steps: int = 10) -> Dict[str, Any]:
        state = initial_state
        current = "START"
        step = 0

        while current != "END" and step < max_steps:
            step += 1
            self.save_checkpoint(thread_id, step, state)

            # Determine next node to execute
            if current == "START":
                next_node = self.edges.get("START", "agent")
            elif current in self.conditional_edges:
                next_node = self.conditional_edges[current](state)
            else:
                next_node = self.edges.get(current, "END")

            if next_node == "END":
                state.current_node = "END"
                state.status = "COMPLETED"
                self.save_checkpoint(thread_id, step + 1, state)
                break

            # Check interruption gate before executing sensitive node
            if next_node in self.interrupt_before and state.variables.get("approved") is not True:
                state.current_node = next_node
                state.status = "INTERRUPTED_AWAITING_APPROVAL"
                ckpt = self.save_checkpoint(thread_id, step + 1, state)
                return {
                    "status": "INTERRUPTED",
                    "checkpoint_id": ckpt,
                    "target_node": next_node,
                    "state": state.to_dict()
                }

            # Execute node logic
            node_func = self.nodes[next_node]
            state = node_func(state)
            state.current_node = next_node
            current = next_node

        return {
            "status": "COMPLETED" if state.status == "COMPLETED" else "MAX_STEPS_REACHED",
            "state": state.to_dict(),
            "steps": step
        }

    def resume(self, checkpoint_id: str, resume_payload: Dict[str, Any], thread_id: str = "default_thread") -> Dict[str, Any]:
        if checkpoint_id not in self.checkpoints:
            raise ValueError(f"Unknown checkpoint: {checkpoint_id}")
        raw = self.checkpoints[checkpoint_id]
        state = GraphState.from_dict(json.loads(raw))
        state.variables.update(resume_payload)
        state.status = "RESUMED"
        return self.run(state, thread_id=thread_id)

def mock_agent_node(state: GraphState) -> GraphState:
    state.messages.append({"role": "assistant", "content": "Tool call required: execute_transfer"})
    state.variables["pending_action"] = "execute_transfer"
    return state

def mock_approval_tool_node(state: GraphState) -> GraphState:
    state.messages.append({"role": "tool", "content": "Action 'execute_transfer' executed successfully."})
    state.variables["transfer_status"] = "SUCCESS"
    return state

def agent_router(state: GraphState) -> str:
    if state.variables.get("transfer_status") == "SUCCESS":
        return "END"
    if state.variables.get("pending_action"):
        return "tool_node"
    return "END"

if __name__ == "__main__":
    engine = StateGraphEngine()
    engine.add_node("agent", mock_agent_node)
    engine.add_node("tool_node", mock_approval_tool_node)

    engine.add_edge("START", "agent")
    engine.add_conditional_edges("agent", agent_router)
    engine.add_conditional_edges("tool_node", agent_router)
    engine.set_interrupt_before(["tool_node"])

    # 1. Run until interruption
    init = GraphState(messages=[{"role": "user", "content": "Transfer $500"}])
    res = engine.run(init, thread_id="tx-1001")
    print(f"Step 1 result: {res['status']} at checkpoint {res.get('checkpoint_id')}")

    # 2. Resume with human approval
    if res["status"] == "INTERRUPTED":
        final_res = engine.resume(res["checkpoint_id"], {"approved": True}, thread_id="tx-1001")
        print(f"Step 2 resume result: {final_res['status']}, final status: {final_res['state']['status']}")
