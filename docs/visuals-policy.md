# Visuals Policy

## Purpose

Use visuals to explain:

- architecture;
- control flow;
- data flow;
- trust boundaries;
- state changes;
- attack paths;
- defense layers;
- comparisons;
- evaluation workflows.

## Preference order

1. Original code-native diagram
2. Reproducible plot from checked data
3. Recreated visual with cited sources
4. Official or external visual with verified reuse permission
5. Generated illustration when factual precision is not carried by the pixels

## Storage

Store each final visual under `assets/<unit-id-lowercase>/`.

```text
assets/<unit-id-lowercase>/
  <nn>-<descriptive-name>.svg
  <nn>-<descriptive-name>.png
  source/       Editable diagram, plot script, prompt, or input data
```

Chapter Markdown must reference the local file. Never hotlink a remote visual. Do not create a unit asset directory until the unit needs a visual.

## Rules

- Prefer SVG for diagrams.
- Use PNG or WebP for raster images.
- Keep editable sources when possible.
- Use meaningful file names.
- Add a caption and contextual alt text. Give complex diagrams and plots an equivalent explanation or data table nearby.
- Explain the visual in nearby text.
- Do not reuse an image without checking its license.
- Record a SHA-256 checksum for each final asset.

## Plots and diagrams

- Use deterministic, code-native output for architecture, flows, trust boundaries, and quantitative claims.
- Keep the editable source, input data, generation command, dependency versions, and fixed random seed when applicable.
- Cite the source records for facts or data encoded in the visual.
- Verify labels, values, contrast, legibility, and correspondence with the chapter.

## Downloaded visuals

- Verify the creator, original page, direct asset URL, license name, license URL, and modification rights before download.
- Prefer public domain, Creative Commons Attribution, or another project-compatible license. Apply all license conditions.
- Record title, author, source, and license. State modifications.
- Verify file type, dimensions, and visible content after download. Do not embed untrusted external SVG files directly. Recreate or safely rasterize them.
- If rights are missing, ambiguous, or incompatible, do not use the file.

## Generated visuals

- Use the installed `imagegen` skill for illustrative raster assets. Use its built-in mode unless its rules require explicit approval for a fallback.
- Save the selected project-bound output in the unit asset directory. Do not leave it only in the generator's default output directory.
- Keep the final prompt under `source/` and record the tool, mode, creation date, and model when known.
- Preserve Content Credentials or other provenance signals when present. Treat them as provenance indicators, not proof of accuracy or ownership.
- Record that generated raster output may not be pixel reproducible even with the same prompt.
- Do not use generated images for exact diagrams, readable labels, benchmark plots, or security evidence.
- If the skill or image tool is unavailable, record a blocker. Do not substitute an untracked placeholder.

## Attribution record

Store metadata in `assets/attribution.yml`. Add or update one entry whenever a visual is created, downloaded, generated, modified, renamed, or removed.

```yaml
- id:
  unit_id:
  title:
  kind: diagram | plot | downloaded | generated
  file:
  editable_source:
  creator:
  source_url:
  direct_asset_url:
  license:
  license_url:
  accessed:
  generated_with:
  prompt_file:
  modified:
  sha256:
  alt:
  caption:
  source_records:
  used_in:
```

Leave fields empty only when they do not apply. Generated and project-original visuals still require creator, provenance, accessibility text, checksum, and usage fields.

## Checked guidance

- [Creative Commons attribution practices](https://wiki.creativecommons.org/index.php?title=Recommended_practices_for_attribution)
- [W3C image accessibility tutorial](https://www.w3.org/WAI/tutorials/images/)
- [C2PA specifications](https://spec.c2pa.org/specifications/)
- [OpenAI provenance signals](https://help.openai.com/en/articles/8912793)
