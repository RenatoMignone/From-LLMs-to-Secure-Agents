from dataclasses import dataclass

@dataclass(frozen=True)
class Proposal:
    id: str
    action: str
    quantity: int
    resource_version: int
    expires_at: int

class Queue:
    def __init__(self):
        self.items = {}
        self.effects = []

    def add(self, proposal):
        if proposal.id in self.items:
            raise ValueError("duplicate proposal")
        self.items[proposal.id] = {"proposal": proposal, "status": "pending"}

    def decide(self, id, role, approve, now, version):
        item = self.items[id]
        if item["status"] != "pending":
            return item["status"]
        proposal = item["proposal"]
        if role != "manager":
            return "wrong_reviewer"
        if now >= proposal.expires_at:
            item["status"] = "expired"
        elif version != proposal.resource_version:
            item["status"] = "stale"
        else:
            item["status"] = "approved" if approve else "rejected"
        return item["status"]

    def execute(self, id, now, version):
        item = self.items[id]
        proposal = item["proposal"]
        if item["status"] == "completed":
            return "completed"
        if item["status"] != "approved":
            return "not_ready"
        if now >= proposal.expires_at or version != proposal.resource_version:
            item["status"] = "needs_new_review"
            return item["status"]
        self.effects.append((proposal.action, proposal.quantity))
        item["status"] = "completed"
        return "completed"

if __name__ == "__main__":
    queue = Queue()
    for id in ("ok", "reject", "expire", "stale", "changed_after"):
        queue.add(Proposal(id, "reserve_lamps", 2, 1, 100))
    assert queue.execute("ok", 10, 1) == "not_ready"
    assert queue.decide("ok", "guest", True, 10, 1) == "wrong_reviewer"
    assert queue.decide("ok", "manager", True, 10, 1) == "approved"
    assert queue.execute("ok", 11, 1) == "completed"
    assert queue.execute("ok", 12, 1) == "completed" and len(queue.effects) == 1
    assert queue.decide("reject", "manager", False, 10, 1) == "rejected"
    assert queue.decide("expire", "manager", True, 100, 1) == "expired"
    assert queue.decide("stale", "manager", True, 10, 2) == "stale"
    assert queue.decide("changed_after", "manager", True, 10, 1) == "approved"
    assert queue.execute("changed_after", 11, 2) == "needs_new_review"
    assert len(queue.effects) == 1
    print("Only the current, approved proposal executes; rejection, expiry and changed state stop it.")
