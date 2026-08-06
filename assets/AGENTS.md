# Asset Instructions

Read `docs/visuals-policy.md`.

Rules:

- Prefer original SVG diagrams.
- Give each chapter one image folder at `assets/images/<chapter-id>/`, using its lowercase `unit_id` as `chapter-id`.
- Store repository-level images under `assets/images/repo-images/`.
- Put editable inputs under the matching image folder's `source/` directory when useful.
- Use meaningful names.
- Add alt text and captions in chapters.
- Never hotlink remote content visuals. The root README may use the live status badges allowed by `docs/visuals-policy.md`.
- Verify source and license before downloading external visuals.
- Use the installed `imagegen` skill only for suitable raster illustrations and save project outputs locally.
- Record prompts, generators, source data, checksums, and usage in the image folder's `manifest.yml`.
- Add every image-folder manifest to `assets/attribution.yml`.
- Keep editable sources.
- Do not add unlicensed images.
- Use `scripts/register_visual.py` instead of formatting manifest entries by hand.
