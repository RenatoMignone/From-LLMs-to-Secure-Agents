# Offline example

Run `python3 examples/03-building-blocks/07-tools-and-function-calling/02-results-failures-side-effects-and-confirmation/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Shows a receipt recovered after a lost response, with one reservation effect; conflicting reuse of the request key is rejected. Any failed assertion exits with an error.
