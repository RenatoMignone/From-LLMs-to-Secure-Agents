# Offline example

Run `python3 examples/03-building-blocks/07-tools-and-function-calling/01-tool-capabilities-schemas-selection-and-dispatch/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Prints structured results linked to their call identifiers, including successful dispatch and invalid requests. Any failed assertion exits with an error.
