# Visuals Policy

## Purpose

Visuals must clarify architecture, flows, trust boundaries, state, attacks, defenses, comparisons, or multi-step execution. Do not create ASCII or text-based .md schemas. Whenever a schema, workflow, state flow, or architecture map is needed, generate a visual cartoon illustration instead.

Chapters should incorporate multiple visual illustrations (typically 2 to 4 diagrams per unit, covering system topology, sequence flows, boundary crossings, state machines, and threat scenarios). The authoring agent should proactively identify every concept that benefits from visual depiction rather than relying on a single overview image. Visuals are a primary learning mechanism for readers.

## Preference order

1. Official or external raster visual with verified reuse permission
2. Generated PNG or WebP illustration matching the canonical style
3. Recreated raster visual with cited sources
4. Reproducible raster plot from checked data

## Visual identity (Canonical Cartoon Style)

All generated project visuals MUST strictly follow the canonical educational cartoon style established by the repository banner (`assets/images/repo-images/source/prompt.txt`):

- **Aesthetics**: Clean, polished 2D cartoon illustration with cute rounded robot assistant characters, friendly simple shapes, soft outlines, and an approachable technical book-guide tone.
- **Palette**: Warm light cream background. Calm pastel palette consisting of soft blue, teal, sage green, warm cream, and soft pastel orange or amber.
- **Composition**: Clear spacing, strong visual hierarchy, bold high-contrast sans-serif labels, and clean flow (left-to-right or cyclical).
- **Strictly Forbidden**: No dark backgrounds, no neon or cyberpunk or hacker themes, no sterile corporate flowchart boxes, no UML or Visio style, and no 3D photorealism.

Preserve technical accuracy and trust boundaries within this friendly cartoon aesthetic.

## Storage

Give each chapter one image folder mirroring its Markdown path (omitting `knowledge/` and `.md`). Repository-level images use `repo-images`.

```text
assets/images/
  repo-images/
    <descriptive-name>.png
    source/                 Prompt, diagram source, or data
  00-prerequisites/
    01-reader-contract-and-system-map/
      <nn>-<descriptive-name>.png
      source/               Diagram, plot script, prompt, or data
```

Keep the complete chapter directory hierarchy, tracking empty folders with `.gitkeep`. Keep final visuals and prompt files in the owning folder; Markdown references local files. Never hotlink content visuals. README badges may be remote.

## Rules

- Use PNG or WebP. Do not create SVG assets. Keep prompts or editable inputs and meaningful names.
- Keep each canonical raster asset at or below 2.5 MiB. Crop excess whitespace and optimize the selected master before committing it.
- The site pipeline must publish responsive WebP variants and reject any generated variant above 250 KiB.
- Add contextual alt text, caption, and nearby explanation in chapter Markdown.
- Do not reuse an image without checking its license.

## Plots and diagrams

- Prefer verified downloadable or generated raster visuals. Do not create SVG assets.
- For every generated visual, write and save the complete prompt in `source/<image-name>-prompt.txt` before generation. Every prompt must explicitly mandate the canonical banner cartoon style, cute robot characters, light cream background, and exact text labels.
- Inspect generated labels, values, contrast, legibility, and chapter correspondence before keeping the output. Reject sterile, dark, or illegible images.

## Downloaded visuals

- Before download, verify creator, original page, direct URL, license URL, and modification rights.
- Verify PNG/WebP media type, dimensions, and visible content after download. Do not embed SVG files.

## Generated visuals

- Use image generation for raster assets and follow its rules. Create the prompt file in `source/` before generating.
- Save selected output in its chapter folder.
- If image generation is unavailable, record a blocker, not an untracked placeholder.

## Authoritative guidance

- Canonical style archetype: `assets/images/repo-images/source/prompt.txt`
- [Creative Commons attribution practices](https://wiki.creativecommons.org/index.php?title=Recommended_practices_for_attribution)
- [W3C image accessibility tutorial](https://www.w3.org/WAI/tutorials/images/)
