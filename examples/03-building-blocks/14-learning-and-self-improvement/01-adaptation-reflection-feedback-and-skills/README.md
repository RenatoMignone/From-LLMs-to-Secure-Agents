# Mock refinement and a candidate authored skill

Run `python3 main.py` with the Python standard library. No SDK, credentials, model calls or training.

Expected: blue-mug availability becomes `False` with source `S17`; all fixture checks pass; candidate version 1.1 is identified with weights unchanged.

The script simulates structured feedback and a fixed refiner. It checks an unseen product and quantity, retains out-of-stock and missing-data behavior, and rejects an uncorrected zero-budget draft. The frozen `skill-record.json` describes the candidate's provenance and rollback. `stock-report/SKILL.md` demonstrates an authored instruction package; the script does not execute or learn its Markdown.

These assertions are teaching fixtures, not measured LLM improvement. The snapshot is invented and assumed authoritative. No inventory is modified, no package is promoted automatically and no real model parameters change.
