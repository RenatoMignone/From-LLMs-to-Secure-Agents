# Thread, run and event demonstration

Run `python3 thread_run_event_runtime.py` from this directory. No packages, credentials or network are needed.

Two mock requests share the `lee-shop` thread and have distinct run IDs. Each produces 10 events and two messages. Assertions check event IDs, snapshot versions, duplicate run rejection, reducer replay without tool execution, and a missing handler that ends in `FAILED` without inventing stock evidence.

These statuses are conventions of this example. The explicit plan is mock application data, not hidden model reasoning. All records disappear when the process exits. This is not a durable, concurrent event store, and it does not implement cancellation or provider APIs.
