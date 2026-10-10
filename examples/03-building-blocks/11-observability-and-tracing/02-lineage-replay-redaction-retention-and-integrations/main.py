import json
from copy import deepcopy

# Synthetic IDs and values only. No live executor or model is used.
VERSIONS = {"model_config": "mock-v1", "tool": "stock-v2", "source": "catalog-v3"}

def select_record(raw):
    if raw["status"] not in {"OK", "ERROR"}:
        raise ValueError("unknown status")
    if type(raw["created_at"]) is not int:
        raise ValueError("invalid timestamp")
    # Application-generated identifiers, never caller-supplied names or messages.
    if raw["run_id"] != "run-1" or raw["result_ref"] != "fixture-1":
        raise ValueError("unknown synthetic reference")
    return {"run_id": raw["run_id"], "status": raw["status"],
            "created_at": raw["created_at"], "expires_at": raw["created_at"] + 60,
            "result_ref": raw["result_ref"], "versions": deepcopy(VERSIONS)}

def export_record(raw, destination):
    # Selection and delivery share one path. Selection failure prevents delivery.
    selected = select_record(raw)
    destination.append(selected)

def replay(record, fixtures):
    result = fixtures.get(record["result_ref"])
    if result is None:
        return {"mode": "mock replay", "available": False}
    count = result["stock_count"]
    if type(count) is not int or count < 0:
        raise ValueError("invalid fixture")
    return {"mode": "mock replay", "available": True, "stock_count": count}

def expire(records, now):
    return [r for r in records if now < r["expires_at"]]

if __name__ == "__main__":
    raw = {"run_id": "run-1", "status": "OK", "created_at": 100,
           "result_ref": "fixture-1", "prompt": "private example",
           "headers": {"authorization": "secret-example"},
           "error": {"nested": {"message": "private example"}}}
    exported = []
    export_record(raw, exported)
    serialized = json.dumps(exported)
    assert "secret-example" not in serialized and "private example" not in serialized
    assert not {"prompt", "headers", "error"} & exported[0].keys()
    bad = dict(raw, status="private example")
    try:
        export_record(bad, exported)
    except ValueError:
        pass
    else:
        raise AssertionError("selection must fail")
    assert len(exported) == 1
    fixtures = {"fixture-1": {"stock_count": 4}}
    assert replay(exported[0], fixtures)["stock_count"] == 4
    assert replay(exported[0], {})["available"] is False
    assert len(expire(exported, 159)) == 1 and expire(exported, 160) == []
    print(json.dumps({"telemetry": exported, "replay": replay(exported[0], fixtures),
                      "retained_at_160": len(expire(exported, 160))}, indent=2))
