"""Offline regression demonstration. No model calls or weight updates."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Case:
    family: str
    quantity: int | None
    expected: str

CASES = [Case("new", n, "available" if n > 0 else "empty") for n in (3, 4, 5, 0)]
CASES += [Case("old", n, "unknown" if n is None else "available" if n > 0 else "empty") for n in (None, 0, 1, 2)]

def report(version: int, case: Case) -> str:
    if version == 1 and case.family == "new":
        return "empty"  # Old parser cannot read the new supplier's quantities.
    if version == 1 and case.quantity is None:
        return "unknown"
    return "available" if (case.quantity or 0) > 0 else "empty"

def score(version: int, family: str) -> int:
    return sum(report(version, c) == c.expected for c in CASES if c.family == family)

def should_promote(baseline: dict[str, int], candidate: dict[str, int]) -> bool:
    return candidate["new"] > baseline["new"] and candidate["old"] >= baseline["old"]

def main() -> None:
    baseline = {f: score(1, f) for f in ("new", "old")}
    candidate = {f: score(2, f) for f in ("new", "old")}
    promote = should_promote(baseline, candidate)
    selected = 2 if promote else 1
    assert baseline == {"new": 1, "old": 4}
    assert candidate == {"new": 4, "old": 3}
    assert sum(candidate.values()) > sum(baseline.values()) and selected == 1
    print(f"baseline={baseline}; candidate={candidate}")
    print(f"promote={promote}; selected_version={selected}")

if __name__ == "__main__":
    main()
