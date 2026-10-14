# Peer task ownership and recovery

Run `python3 main.py`; standard library only. Expected: accepted recovered task at generation 2, checked rejection cases, then a round-budget stop with `task_success: False`.

Assertions cover two peers competing for a task, expiry exactly at the lease boundary, stale results after reassignment, duplicate and conflicting messages, verification failure, cancellation and a bounded discussion with no accepted outcome.

The synthetic clock and sequential in-memory board make the cases deterministic. This is not a concurrent or durable implementation. Use atomic store updates in a real shared service; generation checks protect only participating stores. The example does not fence remote actions, undo external effects or invoke a model.
