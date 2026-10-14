from dataclasses import dataclass

@dataclass(frozen=True)
class Report:
    outcomes: dict[str, tuple[bool, ...]]
    cost: float

BASELINE = Report({"reserve": (True, True), "cancel": (True, True), "product": (False, False, False, False)}, 1.0)
CANDIDATE = Report({"reserve": (True, True), "cancel": (True, False), "product": (True, True, True, True)}, 1.2)
REQUIRED = {"reserve", "cancel"}

def rate(report):
    values = [value for trials in report.outcomes.values() for value in trials]
    return sum(values) / len(values) if values else None

def gate(baseline, candidate, budget=1.5):
    if set(candidate.outcomes) != set(baseline.outcomes):
        return False, "case coverage mismatch"
    if any(len(candidate.outcomes[c]) != len(baseline.outcomes[c]) or not candidate.outcomes[c] for c in baseline.outcomes):
        return False, "trial coverage mismatch"
    if not REQUIRED <= candidate.outcomes.keys():
        return False, "missing mandatory case"
    failed = sorted(c for c in REQUIRED if not all(candidate.outcomes[c]))
    if failed:
        return False, "mandatory failure: " + ", ".join(failed)
    if candidate.cost > budget:
        return False, "cost budget exceeded"
    return True, "fixture gate passed"

if __name__ == "__main__":
    assert rate(CANDIDATE) > rate(BASELINE)
    assert gate(BASELINE, CANDIDATE) == (False, "mandatory failure: cancel")
    repaired = Report({**CANDIDATE.outcomes, "cancel": (True, True)}, 1.2)
    assert gate(BASELINE, repaired)[0]
    assert not gate(BASELINE, Report({"reserve": (True, True)}, 1.0))[0]
    assert not gate(BASELINE, Report(repaired.outcomes, 2.0))[0]
    print(f"baseline={rate(BASELINE):.1%} candidate={rate(CANDIDATE):.1%}")
    print(gate(BASELINE, CANDIDATE)[1])
    print("Repaired, missing-case and over-budget checks passed.")
