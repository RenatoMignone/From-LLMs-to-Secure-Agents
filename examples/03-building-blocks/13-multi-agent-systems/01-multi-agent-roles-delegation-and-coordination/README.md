# Bounded manager-specialist simulation

Run `python3 main.py`; standard library only. It prints a complete manager-owned report and a partial report with `tea-tin` delivery evidence missing. Both show zero orders placed.

The stock function reads an inventory snapshot. The supplier function receives only low-stock IDs. The manager checks the parent relation and combines evidence. Assertions cover missing evidence, filtering and unchanged inventory.

These deterministic functions model contracts without invoking agent SDKs or LLMs. Supplier dates are invented labels. The example does not benchmark teams, handle concurrent changes or implement production authorization.
