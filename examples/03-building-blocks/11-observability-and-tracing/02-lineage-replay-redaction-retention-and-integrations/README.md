# Offline example

Run `python3 examples/03-building-blocks/11-observability-and-tracing/02-lineage-replay-redaction-retention-and-integrations/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Prints selected telemetry without private fields, a mocked replay stock count of 4, and retained_at_160 equal to 0. Any failed assertion exits with an error.
