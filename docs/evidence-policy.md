# Evidence Policy

## Source priority

1. Official standards and specifications
2. Official framework and protocol documentation
3. Peer-reviewed papers and official preprints
4. Official advisories and vulnerability reports
5. Reputable technical reports
6. Secondary tutorials

Use sources such as OWASP, NIST, MITRE ATLAS, official framework docs, protocol specifications, and primary research.

## Rules

- Turn unit scope into research questions. Candidate sources are leads only.
- Open every canonical page, specification, paper, or advisory before use. Search snippets and model memory are not evidence.
- Search beyond candidates when coverage, recency, or opposing evidence is missing.
- Cite important claims near the text.
- Record date and version when relevant.
- Explain conflicts and uncertainty. Paraphrase long passages.
- Separate stable concepts from current implementation details. Recheck time-sensitive sources.

## Source record

Store one checked source at `sources/<source-id>.yml`; reuse shared records. Link every using unit and chapter. Update records when version or supported claims change.

Use `scripts/register_source.py`, not hand-written YAML. Supply semantic fields, especially exact supported claims and limitations. Script handles dates, merging, and local-copy checksums. Keep a local copy only when redistribution permits it or reproducibility requires it; otherwise record canonical URL.

## Unit completion

- Important claims resolve to records naming exact support.
- Time-sensitive sources were verified in this run.
- Conflicts, gaps, and uncertainty remain visible.
