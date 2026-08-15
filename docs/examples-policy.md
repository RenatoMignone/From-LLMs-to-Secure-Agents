# Examples Policy

## Purpose

Make a concept concrete with the smallest useful form.

## Choose the example form

1. Use prose, a table, or a visual when code adds little.
2. Embed a short snippet or pseudocode when readers need to see syntax but not run it.
3. Populate `examples/<chapter-path>/` only when execution teaches or verifies behavior.

A planned example does not require a separate artifact. For inline examples, keep `example_paths: []`.

## Rules

- Mirror each chapter path under `examples/`, omitting `knowledge/` and `.md`.
- Store runnable examples under `examples/<chapter-path>/`. Load only the active chapter's example folder into context.
- Keep examples focused. Document setup, execution, expected output, and limitations.
- Use typed schemas where practical.
- Keep security controls outside the model when possible.
- Mock external services when live access is unnecessary.
- Never commit secrets or destructive payloads.
- Test each runnable artifact. Label pseudocode.
- Store plot generators with visuals in `source/`.

## Security lab structure

```text
README.md
vulnerable/
attack/
hardened/
tests/
```
