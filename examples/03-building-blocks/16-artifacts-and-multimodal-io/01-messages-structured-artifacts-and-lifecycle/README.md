# Typed artifact manifests

Requires Python 3.10+ with only its standard library. Run from repository root:

```bash
python3 examples/03-building-blocks/16-artifacts-and-multimodal-io/01-messages-structured-artifacts-and-lifecycle/main.py
```

Expected: two artifact records; size, digest, format and report/source checks pass. The program selects a plain JSON renderer and an image-reference descriptor. It does not launch a UI or decode the entire image.

The report uses mocked snapshot S17. The image reference points to the real, generated chapter illustration in the repository, which is explanatory art rather than inventory evidence. A typed dataclass describes the local manifest, and explicit functions validate lifecycle, bytes, format and report semantics. The manifest and report are written to a temporary directory, then removed. To inspect them in code, call `build_manifest` with a caller-owned directory. The repository image is only read.

Tests verify changed bytes, semantically wrong data with a matching new digest, expired references and JSON boolean quantities. This is not a JSON Schema engine, ADK implementation, A2A message, durable object store, complete media validator or production retention system. Python type annotations alone do not validate untrusted input.
