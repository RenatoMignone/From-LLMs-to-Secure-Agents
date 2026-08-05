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

- Convert the unit plan into research questions before searching.
- Use candidate sources only as discovery leads. Reopen each source before use.
- Search beyond the candidates when coverage, recency, or opposing evidence is missing.
- Open the canonical page, specification, paper, or advisory. A search snippet is not evidence.
- Cite important claims near the text.
- Do not cite unread sources.
- Record date and version when relevant.
- Explain source conflicts.
- Paraphrase instead of copying long passages.
- Separate stable concepts from current implementation details.
- Review time-sensitive sources before reuse.

## Source record

Store one YAML record per checked source at `sources/<source-id>.yml`, using a stable lowercase kebab-case identifier. Link the record to every unit and chapter that uses it. Create or update it when the source is first used, its version changes, or its supported claims change. Do not duplicate a shared source.

```yaml
id:
title:
authors_or_organization:
date:
source_type:
canonical_url:
doi:
version:
accessed:
last_verified:
status: checked
claims_supported:
limitations:
related_topics:
unit_ids:
used_in:
local_copy:
sha256:
```

Use `local_copy` only when redistribution is allowed or a machine-readable dataset is required. Otherwise keep the canonical URL. Record a SHA-256 checksum for every local copy.

## Unit completion

- Every important claim resolves to a checked source record.
- Every record names exact supported claims, not a broad topic.
- Time-sensitive records were verified during the unit run.
- Conflicts, missing evidence, and uncertain claims are visible in the chapter.
