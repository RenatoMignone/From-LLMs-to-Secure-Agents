from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Job:
    operation: str
    input_id: str
    environment: str

@dataclass(frozen=True)
class Result:
    status: str
    environment: str
    output: dict

class Executor(Protocol):
    def submit(self, job: Job) -> Result: ...

class MockExecutor:
    def submit(self, job):
        if job.environment not in {"container", "microvm"}:
            return Result("unsupported_environment", job.environment, {})
        if job.operation != "summarize_csv" or job.input_id != "sales-v1":
            return Result("unsupported_job", job.environment, {})
        return Result("succeeded", job.environment, {"rows": 3, "total_cents": 7500})

if __name__ == "__main__":
    executor: Executor = MockExecutor()
    for environment in ("container", "microvm"):
        result = executor.submit(Job("summarize_csv", "sales-v1", environment))
        assert result.status == "succeeded" and result.output["rows"] == 3
    assert executor.submit(Job("summarize_csv", "sales-v1", "unknown")).status == "unsupported_environment"
    assert executor.submit(Job("run_arbitrary_code", "sales-v1", "container")).status == "unsupported_job"
    print("Mock executor returns the same job contract for two environment labels; no code or isolation is launched.")
