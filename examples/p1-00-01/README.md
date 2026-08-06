# Mock task transition

Learning goal: distinguish an authorized local state transition, an emitted event, and a requested external side effect.

Run from the repository root:

```bash
python3 examples/p1-00-01/task_transition.py
python3 -m unittest examples/p1-00-01/tests/test_task_transition.py
```

Expected output includes one stored task, `task.created`, and `notification.requested`.

The example uses only Python's standard library. It does not make an HTTP request, persist state, retry delivery, or send a real notification. It supports [Reader contract and system map](../../knowledge/00-prerequisites/01-reader-contract-and-system-map.md).
