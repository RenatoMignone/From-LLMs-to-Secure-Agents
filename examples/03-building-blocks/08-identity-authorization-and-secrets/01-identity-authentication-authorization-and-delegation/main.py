from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    subject: str
    actor: str
    action: str
    resource: str

@dataclass(frozen=True)
class Decision:
    allowed: bool
    policy_version: str
    reason: str

def decide(request):
    allowed = (request.subject == "user:lee" and request.actor == "workload:shop-assistant"
               and request.action == "read" and request.resource == "order:lee-1")
    return Decision(allowed, "policy-v1", "matching grant" if allowed else "no matching grant")

def enforce(request):
    decision = decide(request)
    if not decision.allowed:
        return {"status": "denied", "policy_version": decision.policy_version}
    return {"status": "ok", "order": request.resource,
            "subject": request.subject, "actor": request.actor,
            "policy_version": decision.policy_version}

if __name__ == "__main__":
    request = Request("user:lee", "workload:shop-assistant", "read", "order:lee-1")
    assert enforce(request)["status"] == "ok"
    assert enforce(Request(request.subject, request.actor, "cancel", request.resource))["status"] == "denied"
    assert enforce(Request(request.subject, request.actor, "read", "order:pat-1"))["status"] == "denied"
    assert enforce(Request(request.subject, "workload:other", "read", request.resource))["status"] == "denied"
    print("Read allowed for Lee through the shop workload; other actions, resources and actors denied.")
