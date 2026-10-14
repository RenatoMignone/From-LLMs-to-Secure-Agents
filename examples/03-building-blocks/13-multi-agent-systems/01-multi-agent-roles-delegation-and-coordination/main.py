from dataclasses import dataclass

@dataclass(frozen=True)
class StockResult:
    task_id: str
    low_stock: tuple[str, ...]
    evidence: str

@dataclass(frozen=True)
class DeliveryResult:
    parent_id: str
    dates: dict[str, str]
    missing: tuple[str, ...]

def stock_specialist(snapshot):
    return StockResult("report-1/stock", tuple(sorted(sku for sku, count in snapshot.items() if count < 2)), "inventory-snapshot-v1")

def supplier_specialist(stock_result, supplier_data):
    ids = stock_result.low_stock
    return DeliveryResult(stock_result.task_id, {sku: supplier_data[sku] for sku in ids if sku in supplier_data}, tuple(sku for sku in ids if sku not in supplier_data))

def manager(snapshot, supplier_data):
    stock = stock_specialist(snapshot)
    delivery = supplier_specialist(stock, supplier_data)
    if delivery.parent_id != stock.task_id:
        raise ValueError("Wrong parent task")
    status = "partial" if delivery.missing else "complete"
    return {"owner": "manager", "status": status, "low_stock": stock.low_stock, "delivery": delivery.dates, "missing": delivery.missing, "orders_placed": 0}

if __name__ == "__main__":
    inventory = {"blue-mug": 1, "red-mug": 4, "tea-tin": 0}
    complete = manager(inventory, {"blue-mug": "Friday", "tea-tin": "Thursday"})
    partial = manager(inventory, {"blue-mug": "Friday"})
    assert complete["status"] == "complete" and complete["orders_placed"] == 0
    assert partial["status"] == "partial" and partial["missing"] == ("tea-tin",)
    assert "red-mug" not in complete["delivery"]
    assert inventory == {"blue-mug": 1, "red-mug": 4, "tea-tin": 0}
    print(complete)
    print(partial)
