from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    readable_inputs: frozenset
    destinations: frozenset
    max_output_bytes: int

class MockEnvironment:
    def __init__(self, policy):
        self.policy = policy
        self.browser_cookies = {}
        self.scratch = {}
        self.closed = False
        self.events = []

    def run(self, input_id, destination, output):
        if self.closed:
            raise RuntimeError("environment closed")
        if input_id not in self.policy.readable_inputs:
            raise PermissionError("input unavailable")
        if destination not in self.policy.destinations:
            raise PermissionError("destination unavailable")
        if len(output.encode()) > self.policy.max_output_bytes:
            raise ValueError("output quota")
        self.browser_cookies["session"] = "mock-session"
        self.scratch["summary"] = output
        self.events.append("output_ready")
        return output

    def close(self):
        self.browser_cookies.clear()
        self.scratch.clear()
        self.closed = True
        self.events.append("closed")

if __name__ == "__main__":
    policy = Policy(frozenset({"sales-v1"}), frozenset({"reports.example"}), 20)
    artifacts = {}
    for output, succeeds in [("total: 75", True), ("x" * 21, False)]:
        env = MockEnvironment(policy)
        try:
            artifacts["report"] = env.run("sales-v1", "reports.example", output)
        except ValueError:
            assert not succeeds
        finally:
            env.close()
        assert env.closed and not env.scratch and not env.browser_cookies
    assert artifacts["report"] == "total: 75"
    fresh = MockEnvironment(policy)
    try:
        fresh.run("other-input", "reports.example", "ok")
    except PermissionError:
        pass
    else:
        raise AssertionError("input should be unavailable")
    finally:
        fresh.close()
    print("Mock resource policy applied; cleanup runs after success and failure; published output remains.")
