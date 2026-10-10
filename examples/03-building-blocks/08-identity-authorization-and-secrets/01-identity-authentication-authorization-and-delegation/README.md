# Offline example

Run `python3 examples/03-building-blocks/08-identity-authorization-and-secrets/01-identity-authentication-authorization-and-delegation/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Shows the permitted delegated read and denied actions outside its subject, action or resource scope. Any failed assertion exits with an error.
