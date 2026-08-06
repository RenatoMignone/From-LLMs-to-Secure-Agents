# Asset Instructions

Read `docs/visuals-policy.md`.

Rules:

- Use only PNG or WebP final assets. Do not create or register SVG files.
- Give each chapter one image folder at `assets/images/<chapter-id>/`, using its lowercase `unit_id` as `chapter-id`.
- Store repository-level images under `assets/images/repo-images/`.
- Put prompts and permitted editable inputs under the matching image folder's `source/` directory. Write a generated image's complete prompt before generation.
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
