# Minimal Agent Loop

Learning goal: implement a typed perception-reasoning-action agent loop with turn budgets, structured JSON tool dispatch, observation feedback, and malformed output recovery.

## Run from repository root

```bash
python3 examples/01-agent-foundations/02-the-agent-loop/agent_loop.py
python3 -m unittest examples/01-agent-foundations/02-the-agent-loop/tests/test_agent_loop.py
```

## Expected output

The execution demonstration runs an automated troubleshooting turn sequence:
1. Turn 1: Invokes `ping_server` $\rightarrow$ receives `500 Internal Error`.
2. Turn 2: Invokes `restart_service` $\rightarrow$ receives `Service nginx restarted successfully`.
3. Turn 3: Model recognizes recovery and emits `FINAL: Service recovered successfully.`

## Limitations

- The model client is simulated locally using mock responses.
- The runtime uses Python's standard library without external network dependencies.
- It supports [The agent loop](../../../knowledge/01-agent-foundations/02-the-agent-loop.md).
