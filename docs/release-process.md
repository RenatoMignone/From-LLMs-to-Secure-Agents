# Release Process

Releases provide stable, citable snapshots of the guide. They are not a substitute for the continuously updated website.

## Release readiness

A release candidate should meet these conditions:

- the intended scope and maturity label are clear;
- repository validation, Python tests, site tests, build, and site integrity checks pass;
- known factual, accessibility, and security limitations are documented;
- the changelog summarizes reader-visible changes;
- generated archives contain canonical Markdown and necessary local assets;
- links and source records have been checked in proportion to release scope;
- at least one human editorial review has covered the release notes and highlighted chapters.

## Versioning

Use semantic versioning for project snapshots:

- `0.y.z` for alpha and beta snapshots while the guide and public interfaces are incomplete;
- `1.0.0` when the promised architecture and security learning path has been published and reviewed;
- patch releases for corrections that do not materially change the learning structure;
- minor releases for new chapters, examples, or reader-facing capabilities;
- major releases for incompatible changes to published interfaces or project structure.

The first release should be an explicitly labeled alpha. Do not publish the internal authoring CLI to npm or PyPI merely to distribute the guide. Prefer GitHub release archives, and add EPUB or PDF only when their build and accessibility can be reproduced.

## Procedure

1. Open a release-tracking issue with scope, maturity, and known exclusions.
2. Create a release branch or candidate tag when stabilization begins.
3. Run the full quality matrix locally and in continuous integration.
4. Update `CHANGELOG.md` and any public status text.
5. Create a signed annotated tag when signing infrastructure is available.
6. Publish a GitHub release with generated notes edited for readers.
7. Attach reproducible offline artifacts and checksums.
8. After publication, archive the release with Zenodo when a maintainer has configured the integration, then add the DOI to citation metadata.
9. Verify the website, archive downloads, citation instructions, and rollback path.

Publishing packages may become appropriate if the project develops a supported, read-only tool with value outside this repository, such as local search, export, source inspection, or an MCP server. Such packages need a stable interface, isolated tests, independent versioning, and trusted publishing with provenance.
