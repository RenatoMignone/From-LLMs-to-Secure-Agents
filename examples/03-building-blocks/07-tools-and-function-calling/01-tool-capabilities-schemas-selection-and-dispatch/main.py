import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Lookup:
    sku: str

@dataclass(frozen=True)
class Quote:
    sku: str
    quantity: int

CATALOG = {"lamp": {"stock": 4, "price_cents": 2500}}

def lookup_stock(sku: str) -> dict:
    return {"sku": sku, "available": CATALOG[sku]["stock"]}

def quote_price(sku: str, quantity: int) -> dict:
    return {"sku": sku, "total_cents": CATALOG[sku]["price_cents"] * quantity}

REGISTRY = {"catalog.lookup_stock": (Lookup, lookup_stock),
            "catalog.quote_price": (Quote, quote_price)}

def dispatch(call: dict) -> dict:
    call_id = call["call_id"]
    if call["name"] not in REGISTRY:
        return {"call_id": call_id, "ok": False, "error": "unknown_tool"}
    cls, handler = REGISTRY[call["name"]]
    try:
        args = json.loads(call["arguments"])
        fields = set(cls.__dataclass_fields__)
        if not isinstance(args, dict) or set(args) != fields:
            raise ValueError("argument fields")
        if type(args["sku"]) is not str or not args["sku"]:
            raise ValueError("sku type")
        if "quantity" in args and (type(args["quantity"]) is not int or not 1 <= args["quantity"] <= 10):
            raise ValueError("quantity range")
        request = cls(**args)
        result = handler(**vars(request))
        return {"call_id": call_id, "ok": True, "data": result}
    except (ValueError, TypeError):
        return {"call_id": call_id, "ok": False, "error": "invalid_arguments"}
    except KeyError:
        return {"call_id": call_id, "ok": False, "error": "not_found"}

if __name__ == "__main__":
    def call(name, args, id="c1"):
        return dispatch({"call_id": id, "name": name, "arguments": json.dumps(args)})
    assert call("catalog.lookup_stock", {"sku": "lamp"})["data"]["available"] == 4
    assert call("catalog.quote_price", {"sku": "lamp", "quantity": 2})["data"]["total_cents"] == 5000
    assert call("catalog.quote_price", {"sku": "lamp", "quantity": True})["error"] == "invalid_arguments"
    assert call("catalog.lookup_stock", {"sku": "missing"})["error"] == "not_found"
    assert call("catalog.lookup_stock", {"sku": "lamp", "extra": 1})["error"] == "invalid_arguments"
    assert call("missing", {})["error"] == "unknown_tool"
    assert dispatch({"call_id": "bad", "name": "catalog.lookup_stock", "arguments": "{"})["error"] == "invalid_arguments"
    print("Two tools: valid calls succeed; invalid, unknown and missing-item calls return correlated errors.")
