# Asset Instructions

Read `docs/visuals-policy.md`.

Rules:

- Use only PNG or WebP final assets. Do not create or register SVG files.
- Mirror every chapter path under `assets/images/`, omitting the leading `knowledge/` and the `.md` suffix. For example, `knowledge/00-prerequisites/01-reader-contract-and-system-map.md` owns `assets/images/00-prerequisites/01-reader-contract-and-system-map/`.
- Store repository-level images under `assets/images/repo-images/`.
- Keep the full chapter and subchapter directory hierarchy, including empty chapter folders tracked with `.gitkeep`. Put prompts and permitted editable inputs under the owning chapter folder's `source/` directory. Write a generated image's complete prompt before generation.
- Use meaningful names.
- Add alt text and captions in chapters.
- Never hotlink remote content visuals. The root README may use the live status badges allowed by `docs/visuals-policy.md`.
- Verify source and license before downloading external visuals.
- Prefer a verified downloadable raster visual. Otherwise use the installed `imagegen` skill for a local raster illustration in the banner's approachable technical-cartoon style.
- Generated prompts specify purpose, exact useful labels, layout, factual constraints, and unwanted elements. Inspect the result and reject illegible or decorative-only output.
- Record prompts, generators, source data, checksums, and usage in the image folder's `manifest.yml`.
- Add every image-folder manifest to `assets/attribution.yml`.
- Keep editable sources.
- Do not add unlicensed images.
- Use `scripts/register_visual.py` instead of formatting manifest entries by hand.
