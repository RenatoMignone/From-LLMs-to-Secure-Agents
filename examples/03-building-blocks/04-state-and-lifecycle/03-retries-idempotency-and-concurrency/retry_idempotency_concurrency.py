#!/usr/bin/env python3
"""
Retries, Idempotency Keys, and Optimistic Concurrency Control
Demonstrates jittered exponential backoff for transient failures,
idempotent tool execution caches, and OCC version conflict resolution.
"""

from dataclasses import dataclass, field
import hashlib
import json
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class ConcurrentModificationError(Exception):
    """Raised when an update is attempted on a stale state version."""
    pass


@dataclass
class IdempotentResponse:
    status: str
    data: Dict[str, Any]
    cached: bool = False


class IdempotentService:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.mutation_counter = 0

    def execute_mutation(self, idempotency_key: str, payload: Dict[str, Any]) -> IdempotentResponse:
        """Executes a state-mutating action once per idempotency key."""
        if idempotency_key in self.cache:
            return IdempotentResponse(status="SUCCESS", data=self.cache[idempotency_key], cached=True)

        # Execute actual side effect
        self.mutation_counter += 1
        result = {
            "transaction_id": f"txn_{self.mutation_counter:04d}",
            "amount": payload.get("amount", 0),
            "recipient": payload.get("recipient", "unknown"),
            "status": "SETTLED",
        }
        self.cache[idempotency_key] = result
        return IdempotentResponse(status="SUCCESS", data=result, cached=False)


@dataclass
class ThreadRecord:
    thread_id: str
    version: int
    data: Dict[str, Any]


class VersionedStateStore:
    def __init__(self):
        self.records: Dict[str, ThreadRecord] = {}

    def get(self, thread_id: str) -> ThreadRecord:
        if thread_id not in self.records:
            self.records[thread_id] = ThreadRecord(thread_id, version=1, data={})
        return self.records[thread_id]

    def commit(self, thread_id: str, expected_version: int, new_data: Dict[str, Any]) -> ThreadRecord:
        """Optimistic Concurrency Control commit: checks expected version against stored version."""
        current = self.get(thread_id)
        if current.version != expected_version:
            raise ConcurrentModificationError(
                f"OCC Conflict: Thread {thread_id} is at version {current.version}, but update expected {expected_version}."
            )
        updated = ThreadRecord(thread_id, version=current.version + 1, data=dict(new_data))
        self.records[thread_id] = updated
        return updated


def execute_with_exponential_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.05,
    max_delay: float = 0.5,
) -> Tuple[bool, Any, int]:
    """Executes callable with exponential backoff and full jitter."""
    attempts = 0
    while attempts < max_retries:
        attempts += 1
        try:
            result = fn()
            return True, result, attempts
        except Exception:
            if attempts >= max_retries:
                break
            # Full Jitter formula: random between 0 and min(max_delay, base * 2^attempts)
            sleep_cap = min(max_delay, base_delay * (2 ** (attempts - 1)))
            sleep_duration = random.uniform(0, sleep_cap)
            time.sleep(sleep_duration)

    return False, None, attempts


def main() -> None:
    print("=" * 80)
    print("RETRIES, IDEMPOTENCY, AND OCC CONCURRENCY TRACE")
    print("=" * 80)

    # 1. Idempotency Key Demo
    service = IdempotentService()
    idempotency_key = "req_payment_invoice_8821"
    payment_payload = {"amount": 250, "recipient": "vendor_corp"}

    print("--- Part 1: Idempotency Key & Deduplication ---")
    resp1 = service.execute_mutation(idempotency_key, payment_payload)
    print(f"Call 1 (Initial Run):  Status={resp1.status} | Cached={resp1.cached} | Data={resp1.data}")

    # Simulate network timeout retry with identical idempotency key
    resp2 = service.execute_mutation(idempotency_key, payment_payload)
    print(f"Call 2 (Network Retry): Status={resp2.status} | Cached={resp2.cached} | Data={resp2.data}")
    print(f"Total Database Side-Effects Created: {service.mutation_counter} (Expected: 1)\n")

    # 2. Optimistic Concurrency Control Demo
    print("--- Part 2: Optimistic Concurrency Control (OCC) ---")
    store = VersionedStateStore()
    thread_id = "thread_finance_402"

    # Worker A and Worker B both read version 1
    worker_a_read = store.get(thread_id)
    worker_b_read = store.get(thread_id)
    print(f"Initial State: Version {worker_a_read.version}")

    # Worker A commits update (Version 1 -> 2)
    worker_a_data = {"status": "REVIEW_IN_PROGRESS", "assigned_to": "agent_alpha"}
    updated_a = store.commit(thread_id, expected_version=worker_a_read.version, new_data=worker_a_data)
    print(f"Worker A Commit: SUCCESS -> Thread now at Version {updated_a.version}")

    # Worker B attempts commit with stale expected_version=1
    worker_b_data = {"status": "AUDIT_COMPLETED", "assigned_to": "agent_beta"}
    try:
        store.commit(thread_id, expected_version=worker_b_read.version, new_data=worker_b_data)
        print("Worker B Commit: Unexpected Success")
    except ConcurrentModificationError as e:
        print(f"Worker B Commit: {e}")

    # Worker B resolves conflict: re-reads latest version and retries
    latest_b = store.get(thread_id)
    merged_data = dict(latest_b.data)
    merged_data["status"] = "AUDIT_COMPLETED"
    updated_b = store.commit(thread_id, expected_version=latest_b.version, new_data=merged_data)
    print(f"Worker B Retry (with Version {latest_b.version}): SUCCESS -> Thread now at Version {updated_b.version}")
    print(f"Final Merged State: {updated_b.data}")
    print("=" * 80)


if __name__ == "__main__":
    main()
