# Examples Policy

## Purpose

Each example must answer one clear learning question.

## Types

- minimal concept example;
- framework translation;
- vulnerable implementation;
- attack demonstration;
- hardened implementation;
- security test;
- end-to-end reference system.

## Rules

- Store unit examples under `examples/<unit-id-lowercase>/`.
- Keep examples runnable.
- Pin important dependency versions.
- Include setup and run commands.
- State expected output.
- Use typed schemas where practical.
- Keep security controls outside the model when possible.
- Mock external services when live access is unnecessary.
- Never commit secrets.
- Do not include destructive payloads.
- Add tests for the main security property.
- State limitations.
- Store plot generators with their visual under `assets/images/<chapter-id>/source/`, not as chapter examples.

## Security lab structure

```text
README.md
vulnerable/
attack/
hardened/
tests/
```
