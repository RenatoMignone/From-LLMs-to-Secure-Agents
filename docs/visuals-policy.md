# Visuals Policy

## Purpose

Use visuals only when they clarify architecture, flows, trust boundaries, state, attacks, defenses, comparisons, or evaluation.

## Preference order

1. Original code-native diagram
2. Reproducible plot from checked data
3. Recreated visual with cited sources
4. Official or external visual with verified reuse permission
5. Generated illustration when factual precision is not carried by the pixels

## Visual identity

- Generated illustrations use an approachable technical cartoon style: simple shapes, clear hierarchy, restrained labels, and calm blue, teal, green, cream, and warm neutrals.
- Preserve technical structure and trust boundaries. Keep style consistent without repeating compositions.
- Do not force downloaded figures, official diagrams, plots, or evidence visuals into the cartoon style.
- Keep prose and layout technical. Illustrations explain, not decorate.

## Storage

Give each chapter one image folder. Derive `chapter-id` from the chapter's lowercase `unit_id`. Repository-level presentation images use `repo-images`.

```text
assets/images/
  repo-images/
    <descriptive-name>.png
    manifest.yml
    source/                 Optional editable inputs
  <chapter-id>/
    <nn>-<descriptive-name>.svg
    <nn>-<descriptive-name>.png
    manifest.yml
    source/                 Diagram, plot script, prompt, or data
```

Keep final visuals and manifest in the chapter folder; Markdown references local files. Never hotlink content visuals. Create folders only when needed. `scripts/register_visual.py` adds manifests to `assets/attribution.yml`.

README badges may be remote when they report useful, verifiable facts and link to their source.

## Rules

- Prefer SVG diagrams; use PNG or WebP for raster images. Keep editable sources and meaningful names.
- Add contextual alt text, caption, and nearby explanation. Give complex visuals an equivalent explanation or data table.
- Do not reuse an image without checking its license.
- Record a SHA-256 checksum for each final asset.

## Plots and diagrams

- Use deterministic, code-native output for architecture, flows, trust boundaries, and quantitative claims. Never use image generation for these.
- Keep source, data, command, dependency versions, and fixed seed when applicable.
- Cite the source records for facts or data encoded in the visual.
- Verify labels, values, contrast, legibility, and chapter correspondence.

## Downloaded visuals

- Before download, verify creator, original page, direct URL, license, and modification rights. Apply every license condition and record attribution and modifications.
- Verify file type, dimensions, and visible content after download. Do not embed untrusted external SVG files directly. Recreate or safely rasterize them.
- If rights are missing, ambiguous, or incompatible, do not use the file.

## Generated visuals

- Use installed `imagegen` skill for illustrative raster assets and follow its rules.
- Save selected output in its chapter folder.
- Keep the final prompt under `source/` and record the tool, mode, creation date, and model when known.
- Preserve provenance signals, but do not treat them as proof of accuracy or ownership. Note that raster generation may not reproduce pixels exactly.
- If image generation is unavailable, record a blocker, not an untracked placeholder.

## Visual manifest

Use `scripts/register_visual.py`, not hand-written YAML, for every create, download, generation, modification, rename, or removal. It writes `manifest.yml`, checksum, and attribution index. Supply semantic provenance, license, source records, alt text, caption, and usage. Validate against `schemas/visual-manifest.schema.json`.

## Authoritative guidance

- [Creative Commons attribution practices](https://wiki.creativecommons.org/index.php?title=Recommended_practices_for_attribution)
- [W3C image accessibility tutorial](https://www.w3.org/WAI/tutorials/images/)
- [C2PA specifications](https://spec.c2pa.org/specifications/)
- [OpenAI provenance signals](https://help.openai.com/en/articles/8912793)
