from dataclasses import dataclass, field

@dataclass
class Shop:
    stock: int = 3
    reservations: list[dict] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)

    def read_stock(self):
        self.steps.append("read_stock")
        return self.stock

    def reserve(self):
        self.steps.append("reserve")
        if self.stock < 2:
            return False
        self.stock -= 2
        self.reservations.append({"sku": "blue-mug", "quantity": 2})
        return True

def grade(shop):
    outcome = shop.stock == 1 and shop.reservations == [{"sku": "blue-mug", "quantity": 2}]
    trajectory = "read_stock" in shop.steps and "reserve" in shop.steps and shop.steps.index("read_stock") < shop.steps.index("reserve")
    return outcome, trajectory

def run(mode):
    shop = Shop()
    if mode != "skip_lookup":
        shop.read_stock()
    if mode in {"correct", "skip_lookup", "duplicate"}:
        shop.reserve()
    if mode == "duplicate":
        shop.stock = 3  # Simulate a second write to a wrongly reset inventory.
        shop.reserve()
    return grade(shop)

if __name__ == "__main__":
    expected = {"correct": (True, True), "claim_only": (False, False), "skip_lookup": (True, False), "duplicate": (False, True)}
    for mode, verdict in expected.items():
        result = run(mode)
        assert result == verdict, (mode, result)
        print(f"{mode}: outcome={result[0]} trajectory={result[1]} accepted={all(result)}")
