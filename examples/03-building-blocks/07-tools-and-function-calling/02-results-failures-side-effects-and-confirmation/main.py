from dataclasses import dataclass

@dataclass(frozen=True)
class Reservation:
    sku: str
    quantity: int

class Shop:
    def __init__(self):
        self.stock = 4
        self.receipts = {}

    def reserve(self, request, key, approved=False, lose_reply=False):
        if not approved:
            return {"status": "pending_confirmation"}
        if key in self.receipts:
            previous, result = self.receipts[key]
            if previous != request:
                return {"status": "key_conflict"}
            return dict(result)
        if request.sku != "lamp" or type(request.quantity) is not int or request.quantity <= 0:
            return {"status": "invalid_request"}
        if request.quantity > self.stock:
            return {"status": "out_of_stock"}
        self.stock -= request.quantity
        result = {"status": "succeeded", "reservation_id": f"r{len(self.receipts)+1}"}
        self.receipts[key] = (request, result)
        if lose_reply:
            raise TimeoutError("Reply lost after commit")
        return dict(result)

if __name__ == "__main__":
    shop = Shop()
    request = Reservation("lamp", 2)
    assert shop.reserve(request, "operation-1")["status"] == "pending_confirmation"
    assert shop.stock == 4
    try:
        shop.reserve(request, "operation-1", approved=True, lose_reply=True)
    except TimeoutError:
        print("Caller outcome: unknown; service has committed.")
    assert shop.stock == 2
    receipt = shop.reserve(request, "operation-1", approved=True)
    assert receipt["status"] == "succeeded" and shop.stock == 2
    assert shop.reserve(Reservation("lamp", 1), "operation-1", approved=True)["status"] == "key_conflict"
    print("Retry with the same key returns", receipt, "without another reservation.")
