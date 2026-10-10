from dataclasses import dataclass

@dataclass(frozen=True)
class Grant:
    subject: str
    actor: str
    audience: str
    resource: str
    scopes: frozenset
    expires_at: int

class Broker:
    def __init__(self):
        self.grants = {}
        self.counter = 0

    def issue(self, subject, actor, now):
        if (subject, actor) != ("user:lee", "workload:shop"):
            raise PermissionError("no grant")
        self.counter += 1
        handle = f"mock-{self.counter}"
        self.grants[handle] = Grant(subject, actor, "orders", "order:lee-1", frozenset({"read"}), now + 60)
        return handle

    def check(self, handle, audience, resource, action, now):
        grant = self.grants.get(handle)
        return bool(grant and now < grant.expires_at and grant.audience == audience
                    and grant.resource == resource and action in grant.scopes)

    def revoke(self, handle):
        self.grants.pop(handle, None)

if __name__ == "__main__":
    broker = Broker()
    first = broker.issue("user:lee", "workload:shop", 100)
    assert broker.check(first, "orders", "order:lee-1", "read", 159)
    assert not broker.check(first, "orders", "order:lee-1", "read", 160)
    assert not broker.check(first, "billing", "order:lee-1", "read", 101)
    assert not broker.check(first, "orders", "order:lee-1", "cancel", 101)
    second = broker.issue("user:lee", "workload:shop", 150)
    assert broker.check(second, "orders", "order:lee-1", "read", 160)
    broker.revoke(second)
    assert not broker.check(second, "orders", "order:lee-1", "read", 161)
    print("Scoped mock grants expire at 60 seconds; renewal creates a new grant; revocation removes it.")
