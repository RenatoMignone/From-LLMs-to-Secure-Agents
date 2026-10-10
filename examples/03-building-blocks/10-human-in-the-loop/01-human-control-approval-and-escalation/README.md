# Offline example

Run `python3 examples/03-building-blocks/10-human-in-the-loop/01-human-control-approval-and-escalation/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Shows approval-state checks and a single mock effect; rejected, expired or stale proposals do not perform that effect. Any failed assertion exits with an error.
