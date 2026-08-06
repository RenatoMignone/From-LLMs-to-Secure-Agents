# Examples Policy

## Purpose

Each example must answer one clear learning question.

## Rules

- Store unit examples under `examples/<unit-id-lowercase>/`.
- Keep examples small and runnable. Pin important dependencies; include setup, run command, expected output, and limitations.
- Use typed schemas where practical.
- Keep security controls outside the model when possible.
- Mock external services when live access is unnecessary.
- Never commit secrets or destructive payloads.
- Test the main learning or security property.
- Store plot generators with their visual under `assets/images/<chapter-id>/source/`, not as chapter examples.

## Security lab structure

```text
README.md
vulnerable/
attack/
hardened/
tests/
```
