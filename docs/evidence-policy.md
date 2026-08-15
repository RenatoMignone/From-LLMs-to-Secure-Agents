# Evidence Policy

## Source priority

1. Official standards and specifications
2. Official framework and protocol documentation
3. Peer-reviewed papers and preprints
4. Official advisories and vulnerability reports
5. First-party engineering reports
6. Named practitioner posts, talks, and technical discussions
7. Secondary tutorials

## Rules

- Turn unit scope into research questions. Candidate sources are leads only.
- Open canonical sources before use. Snippets and model memory are not evidence.
- Search beyond candidates when coverage, recency, or opposing evidence is missing.
- Cite important claims nearby. Record dates and versions.
- Explain conflicts and uncertainty; paraphrase long passages.
- Separate stable concepts from implementation details. Recheck time-sensitive sources.

## Field signals

- Scan credible practitioner sources for useful vocabulary.
- Include terms only when they map to concrete concepts and aid technical discussion.
- Label terms as standardized, vendor-specific, research, or emerging. Record aliases and date.
- Social posts support provenance or leads, not general technical claims. Verify those through primary evidence.
- Cite named author and canonical post only after opening it.

## Source record

Mirror chapters under `sources/`, omitting `knowledge/` and `.md`. Store chapter sources at `sources/<chapter-path>/<source-id>.yml` and repository records at `sources/project/<source-id>.yml`. Load only active chapter sources into context. Each record belongs to one owner folder and links to its unit and chapter.

Use `scripts/main.py source`, not hand-written YAML. Supply exact supported claims and limitations. Script handles dates, merging, and checksums. Keep local copies only when reproducibility requires them.

## Unit completion

- Important claims resolve to records naming exact support.
- Time-sensitive sources were verified in this run.
- Conflicts, gaps, and uncertainty remain visible.
