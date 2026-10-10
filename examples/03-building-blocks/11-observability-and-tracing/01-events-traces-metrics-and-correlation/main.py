import json
from collections import Counter

TRACE_ID = "1" * 32
BASE_NS = 1_700_000_000_000_000_000

def span(number, parent, name, start_ms, end_ms, status="OK", attributes=None, events=None):
    return {"trace_id": TRACE_ID, "span_id": f"{number:016x}",
            "parent_span_id": f"{parent:016x}" if parent else None,
            "name": name, "start_time_ns": BASE_NS + start_ms * 1_000_000,
            "end_time_ns": BASE_NS + end_ms * 1_000_000,
            "status": status, "attributes": attributes or {}, "events": events or []}

def mock_run():
    return [
        span(1, None, "shop_run", 0, 120, attributes={"project.run_id": "run-1"}),
        span(2, 1, "retrieve", 0, 20),
        span(3, 1, "model", 20, 60),
        span(4, 1, "tool_operation", 60, 90),
        span(5, 4, "lookup_stock", 60, 70, "ERROR", {"project.operation_id": "op-1", "project.attempt": 1}),
        span(6, 4, "lookup_stock", 70, 90, "OK", {"project.operation_id": "op-1", "project.attempt": 2}),
        span(7, 1, "handoff", 90, 100, events=[{"name": "control_transferred", "time_ms": 100}]),
        span(8, 7, "worker_summary", 100, 120),
    ]

if __name__ == "__main__":
    spans = mock_run()
    ids = {s["span_id"] for s in spans}
    assert len(ids) == len(spans)
    assert all(s["trace_id"] == TRACE_ID and s["end_time_ns"] >= s["start_time_ns"] for s in spans)
    assert all(s["parent_span_id"] is None or s["parent_span_id"] in ids for s in spans)
    tools = [s for s in spans if s["name"] == "lookup_stock"]
    counts = Counter(s["status"] for s in tools)
    durations = [(s["end_time_ns"] - s["start_time_ns"]) / 1_000_000 for s in tools]
    logical_operations = {s["attributes"]["project.operation_id"] for s in tools}
    assert counts == {"ERROR": 1, "OK": 1} and durations == [10, 20]
    assert len(logical_operations) == 1 and spans[0]["status"] == "OK"
    print(json.dumps({"spans": spans, "tool_attempts": len(tools), "tool_errors": counts["ERROR"],
                      "logical_operations": len(logical_operations), "durations_ms": durations}, indent=2))
