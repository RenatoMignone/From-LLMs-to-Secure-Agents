# Site Policy

## Source of truth

Markdown under `knowledge/` is canonical.

Generate static HTML from Markdown. Do not maintain separate manual HTML copies.

## Format decision

Do not replace chapters with hand-written HTML. Markdown gives agents smaller context, clearer diffs, portable citations, and readable source files. The generated site supplies HTML, Cascading Style Sheets (CSS), JavaScript, search, navigation, and interactive behavior.

Use standard Markdown for the complete explanation. Add portable inline HTML only when Markdown cannot express a small accessible element. Keep scripts and styles out of chapter files. Rich features must have a text fallback and be implemented once in the site layer, not copied into chapters.

## Requirements

The site should support:

- nested navigation;
- sequential learning paths;
- search;
- syntax highlighting;
- diagrams;
- source links;
- visual attribution;
- glossary terms;
- prerequisite links;
- responsive layout;
- accessible contrast;
- light and dark themes.

Use the banner's blue, teal, green, cream, and warm neutral palette as restrained accents. Keep the interface technical and readable. Generated illustrations may use the approachable cartoon style defined in `docs/visuals-policy.md`, but navigation, prose, code, tables, and controls must not look cartoonish.

Astro Starlight is the preferred initial option unless a later decision changes it.

## Rules

- Do not hand-edit generated HTML.
- Keep builds reproducible.
- Preserve technical meaning.
- Keep core explanations available as text.
- Keep chapters useful without JavaScript.
- Check links, images, headings, mobile layout, alt text, and code overflow.
