# Offline shop evaluation

Run `python3 main.py` from this folder. Python standard library only; no credentials or model calls.

Four scripted cases print separate outcome and trajectory checks. Only `correct` is accepted. `claim_only` lacks a write, `skip_lookup` lacks required evidence, and `duplicate` contains two records. Assertions verify the grader rejects these distinct failures.

Every case starts from fresh state. This is a small deterministic simulator, not a performance benchmark or a production reservation service. The duplicate case deliberately injects a broken inventory reset to expose the outcome check.
