# Visuals Policy

## Purpose

Use visuals only when they clarify architecture, flows, trust boundaries, state, attacks, defenses, comparisons, or evaluation.

## Preference order

1. Official or external raster visual with verified reuse permission
2. Generated PNG or WebP illustration
3. Recreated raster visual with cited sources
4. Reproducible raster plot from checked data

## Visual identity

- Generated illustrations use an approachable technical cartoon style: simple shapes, clear hierarchy, restrained labels, and calm blue, teal, green, cream, and warm neutrals.
- Preserve technical structure and trust boundaries. Keep style consistent without repeating compositions.
- Do not force downloaded figures, official diagrams, plots, or evidence visuals into the cartoon style.
- Keep prose and layout technical. Illustrations explain, not decorate.

## Storage

Give each chapter one image folder that mirrors its Markdown path. Remove the leading `knowledge/` and the `.md` suffix. Repository-level presentation images use `repo-images`.

```text
assets/images/
  repo-images/
    <descriptive-name>.png
    manifest.yml
    source/                 Optional editable inputs
  00-prerequisites/
    01-reader-contract-and-system-map/
      <nn>-<descriptive-name>.png
      manifest.yml
      source/               Diagram, plot script, prompt, or data
```

Keep the complete chapter and subchapter hierarchy, tracking empty chapter folders with `.gitkeep`. Keep final visuals and the manifest in the owning chapter folder; Markdown references local files. Never hotlink content visuals. `scripts/register_visual.py` adds manifests to `assets/attribution.yml`.

README badges may be remote when they report useful, verifiable facts and link to their source.

## Rules

- Use PNG or WebP. Do not create SVG assets. Keep prompts or permitted editable inputs and meaningful names.
- Add contextual alt text, caption, and nearby explanation. Give complex visuals an equivalent explanation or data table.
- Do not reuse an image without checking its license.
- Record a SHA-256 checksum for each final asset.

## Plots and diagrams

- Prefer a verified downloadable raster visual or a generated raster visual. Do not create SVG assets.
- For every generated visual, create and save a complete chapter-local prompt before calling the generator. Adapt the repository banner's approachable technical-cartoon style: simple shapes, soft outlines, light background, calm blue, teal, green, cream, and warm neutral colors.
- Prompts must state the visual purpose, required labels as exact text, required layout, factual constraints, and unwanted elements. Inspect generated labels, values, contrast, legibility, and chapter correspondence before use.
- Keep source, data, command, dependency versions, and fixed seed when a reproducible raster plot is required. Cite source records for facts or data encoded in a visual.

## Downloaded visuals

- Before download, verify and record creator, original page, direct asset URL, license URL, and modification rights. Apply every license condition and record modifications.
- Verify PNG/WebP media type, dimensions, and visible content after download. Registration rejects missing provenance and other formats. Do not embed external SVG files.
- If rights are missing, ambiguous, or incompatible, do not use the file.

## Generated visuals

- Use installed `imagegen` skill for generated raster assets and follow its rules. Create the prompt file before generating, not after selecting an output.
- Save selected output in its chapter folder.
- Keep the final prompt under `source/` and record the tool, mode, creation date, and model when known.
- Preserve provenance signals, but do not treat them as proof of accuracy or ownership. Note that raster generation may not reproduce pixels exactly.
- If image generation is unavailable, record a blocker, not an untracked placeholder.

## Visual manifest

Use `scripts/register_visual.py`, not hand-written YAML, for every create, download, generation, modification, rename, or removal. It writes `manifest.yml`, media type, dimensions, checksum, and attribution index. Supply semantic provenance, license, source records, alt text, caption, and usage. Validate against `schemas/visual-manifest.schema.json`.

## Authoritative guidance

- [Creative Commons attribution practices](https://wiki.creativecommons.org/index.php?title=Recommended_practices_for_attribution)
- [W3C image accessibility tutorial](https://www.w3.org/WAI/tutorials/images/)
- [C2PA specifications](https://spec.c2pa.org/specifications/)
- [OpenAI provenance signals](https://help.openai.com/en/articles/8912793)
