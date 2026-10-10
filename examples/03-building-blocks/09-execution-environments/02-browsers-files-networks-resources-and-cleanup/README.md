# Offline example

Run `python3 examples/03-building-blocks/09-execution-environments/02-browsers-files-networks-resources-and-cleanup/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Shows cleanup after success and failure while preserving the published artifact, and rejects disallowed resource requests. Any failed assertion exits with an error.
