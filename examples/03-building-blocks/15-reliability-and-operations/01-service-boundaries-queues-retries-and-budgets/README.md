# Bounded scheduling and ambiguous outcomes

Requires Python 3.10+ and only its standard library. Run from repository root:

```bash
python3 examples/03-building-blocks/15-reliability-and-operations/01-service-boundaries-queues-retries-and-budgets/main.py
```

Expected: queue delay 1 tick, two completed execution scenarios, one reservation effect in each, released local resources, two retry attempts and cost units, and pending compensation.

The example compares uninterrupted work with a crash after external commit and before local completion. A JSON progress artifact persists intent, completed work, unresolved questions, next steps and verification results. A second simulated session reopens it and reconciles the supplier ledger. Artifacts live in a temporary directory removed on exit. Tests also exercise deadline and cost exhaustion, stale-worker rejection and failed compensation.

The supplier ledger stands in for an external service that survives the local session. File replacement is not a distributed transaction or a power-loss durability guarantee. The seeded jitter and clock are simulated. Cleanup runs through a supervised `finally` path; a real hard-killed process needs a separate resource owner. No actual service, framework replay, concurrency, cancellation delivery or remote action is exercised.
