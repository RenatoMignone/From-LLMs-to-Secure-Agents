# Offline example

Run `python3 examples/03-building-blocks/09-execution-environments/01-execution-boundaries-isolation-and-sandboxes/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Prints mock execution results for the named operation and rejects unsupported operations. No real sandbox is launched. Any failed assertion exits with an error.
