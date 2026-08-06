# Evidence Policy

## Source priority

1. Official standards and specifications
2. Official framework and protocol documentation
3. Peer-reviewed papers and official preprints
4. Official advisories and vulnerability reports
5. First-party engineering reports and documentation
6. Named practitioner posts, talks, and technical discussions
7. Secondary tutorials

## Rules

- Turn unit scope into research questions. Candidate sources are leads only.
- Open every canonical source before use. Snippets and model memory are not evidence.
- Search beyond candidates when coverage, recency, or opposing evidence is missing.
- Cite important claims nearby. Record relevant dates and versions.
- Explain conflicts and uncertainty; paraphrase long passages.
- Separate stable concepts from current implementation details. Recheck time-sensitive sources.

## Field signals

- Scan recent official and credible practitioner sources for relevant vocabulary.
- Include terms only when they map to concrete concepts and aid current technical discussion.
- Label terms as standardized, vendor-specific, research, or emerging. Record aliases and date.
- Social posts support provenance, attributed experience, or research leads, not general technical or benchmark claims. Verify those through primary evidence.
- Cite named author and canonical post only after opening it.

## Source record

Store checked sources at `sources/<source-id>.yml`; reuse shared records. Link each using unit and chapter. Update changed versions or claims.

Use `scripts/register_source.py`, not hand-written YAML. Supply exact supported claims and limitations. Use `practitioner-post` or `practitioner-talk` as `source_type` when applicable. Script handles dates, merging, and checksums. Keep local copies only when rights and reproducibility require them.

## Unit completion

- Important claims resolve to records naming exact support.
- Time-sensitive sources were verified in this run.
- Conflicts, gaps, and uncertainty remain visible.
