# Offline example

Run `python3 examples/03-building-blocks/10-human-in-the-loop/02-interrupts-steering-feedback-and-operator-experience/main.py` from the repository root. Python 3.10 or newer; standard library only. No credentials or network needed. Assertions check the behavior described in the chapter. All external services and model calls are mocked. This teaches the runtime contract, not production deployment.

## Expected output

Shows boundary acknowledgement of pause, steering that invalidates the prior draft, resume and human takeover. Any failed assertion exits with an error.
