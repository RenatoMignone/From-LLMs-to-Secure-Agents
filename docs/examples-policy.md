# Examples Policy

## Purpose

Make a concept concrete with the smallest useful form.

## Choose the example form

1. Use prose, a table, or a visual when code adds little.
2. Embed a short snippet or pseudocode when readers need to see syntax but not run it.
3. Create `examples/<unit-id-lowercase>/` only when execution teaches or verifies behavior, such as integrations, retries, protocols, policies, evaluation, or security.

A planned example does not require a separate artifact. Record the chosen form in the chapter. For inline examples, keep `example_paths: []` and create no placeholder directory.

## Rules

- Store runnable examples under `examples/<unit-id-lowercase>/`.
- Keep runnable examples focused. Pin important dependencies and document setup, execution, expected output, and limitations.
- Use typed schemas where practical.
- Keep security controls outside the model when possible.
- Mock external services when live access is unnecessary.
- Never commit secrets or destructive payloads.
- Test each runnable artifact's main property. Label pseudocode.
- Store plot generators with visuals in the chapter folder's `source/`.

## Security lab structure

```text
README.md
vulnerable/
attack/
hardened/
tests/
```
