# Offline example

Run `python3 examples/03-building-blocks/11-observability-and-tracing/01-events-traces-metrics-and-correlation/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Prints a JSON trace with eight spans, two tool attempts, one tool error and one logical operation. Any failed assertion exits with an error.
