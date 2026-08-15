# Asset Instructions

Read `docs/visuals-policy.md`.

Rules:

- Use only PNG or WebP final assets. Do not create SVG files.
- Mirror every chapter path under `assets/images/`, omitting the leading `knowledge/` and the `.md` suffix.
- Store repository-level images under `assets/images/repo-images/`.
- Keep the full chapter and subchapter directory hierarchy, including empty chapter folders tracked with `.gitkeep`.
- Put prompts and permitted editable inputs under the owning chapter folder's `source/` directory.
- Write a generated image's complete prompt in `source/<image-name>-prompt.txt` before generation.
- Use meaningful names.
- Add alt text and captions in chapters.
- Never hotlink remote content visuals. The root README may use the live status badges allowed by `docs/visuals-policy.md`.
- Verify source and license before downloading external visuals.
- Prefer a verified downloadable raster visual. Otherwise use image generation for a local raster illustration strictly adhering to the banner's canonical educational cartoon style in `assets/images/repo-images/source/prompt.txt` (cute robot characters, soft outlines, light cream background, calm pastel palette). Reject dark, sterile, or corporate flowchart styles.
- Generated prompts specify purpose, exact useful labels, layout, factual constraints, and unwanted elements. Inspect the result and reject illegible or decorative-only output.
- Include as many visuals (0 to many) as needed to clarify concepts based on pedagogical evaluation.
- Keep editable sources and prompt files.
- Do not add unlicensed images.
