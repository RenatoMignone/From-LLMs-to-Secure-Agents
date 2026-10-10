# Persistent memory operations demo

Python 3.10 or newer; standard library only. From the repository root, run `python3 examples/03-building-blocks/05-memory/03-persistent-memory-types-and-lifecycle/persistent_memory_runtime.py`. No services or credentials are used.

Expected behavior: write four synthetic records, retrieve Alice records, update her preference and delete one record. Assertions check that Alice searches exclude Alice2 and that expiry starts at the exact 60-second boundary. Random IDs and current timestamps vary.

The dictionary disappears on exit. Namespace filtering does not implement authentication or authorization. Word overlap is a relevance heuristic. Local deletion does not remove replicas, backups or derived summaries and does not demonstrate legal compliance.
