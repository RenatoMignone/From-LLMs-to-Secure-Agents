from dataclasses import dataclass, field

@dataclass
class Run:
    status: str = "running"
    goal_version: int = 1
    checkpoint: int = 0
    draft: str | None = None
    events: list = field(default_factory=list)

    def request_pause(self):
        if self.status == "running":
            self.status = "pause_requested"
            self.events.append("pause_requested")

    def boundary(self):
        self.checkpoint += 1
        if self.status == "pause_requested":
            self.status = "paused"
            self.events.append("pause_acknowledged")

    def steer(self, new_goal):
        if self.status != "paused":
            raise RuntimeError("wait for pause acknowledgement")
        self.goal_version += 1
        self.draft = None
        self.events.append(("goal_changed", self.goal_version, new_goal))

    def resume(self):
        if self.status != "paused":
            raise RuntimeError("not paused")
        self.status = "running"
        self.events.append("resumed")

    def take_over(self):
        if self.status != "paused":
            raise RuntimeError("not paused")
        self.status = "human_owned"
        self.events.append("ownership_transferred")

if __name__ == "__main__":
    run = Run(draft="old pickup note")
    run.request_pause()
    assert run.status == "pause_requested"
    try:
        run.steer("delivery note")
    except RuntimeError:
        pass
    else:
        raise AssertionError("pause must be acknowledged")
    run.boundary()
    assert run.status == "paused" and run.checkpoint == 1
    run.steer("delivery note")
    assert run.goal_version == 2 and run.draft is None
    run.resume()
    assert run.status == "running"
    run.request_pause(); run.boundary(); run.take_over()
    assert run.status == "human_owned"
    print("Pause requested, acknowledged at boundary, goal revised, draft invalidated, resumed; later human takeover recorded.")
