# Chapter Templates

## Architecture chapter

```markdown
---
title:
unit_id:
summary:
prerequisites:
learning_objectives:
source_records: []
visual_assets: []
example_paths: []
pass: architecture
learning_path: main
status: draft
last_reviewed:
---

# Title

## Why this matters
## Simple mental model
## Position in the agent workflow
## How it works
## Main variants
## Minimal implementation
## Framework implementations
## Data flow and state changes
## Trust boundaries
## Reliability failures
## Worked example
## Limitations and trade-offs
## Security preview
## Open research questions
## Key takeaways
## References
```

The security preview is brief. It names the security relevance and links forward to the related security chapter. It does not contain detailed attacks, controls, recovery guidance, or security tests.

## Security chapter

```markdown
---
title:
unit_id:
summary:
prerequisites:
learning_objectives:
source_records: []
visual_assets: []
example_paths: []
pass: security
learning_path: main
status: draft
last_reviewed:
---

# Title

## Architecture and workflow scope
## Threat model assumptions
## Assets and trust boundaries
## Failures and attacks
## Preventive controls
## Detective controls
## Recovery controls
## Security tests
## Secure design pattern
## Limitations and residual risk
## Open research questions
## Key takeaways
## References
```

Security chapters link back to every architecture component and workflow step they revisit.

## Field terminology

Add a short subsection within the most relevant existing section when current vocabulary helps the reader. Map each term to the concrete mechanism, give aliases and maturity, and cite its origin or representative use. Do not create a detached trend list.

## Completion checklist

- Link prerequisites; define terms and acronyms; keep model refreshers brief.
- Begin with a familiar situation; avoid unexplained software vocabulary.
- Set `learning_path` from the resolved plan classification. Deep dives link to their main-path entry and return point.
- Cite important claims and record checked sources.
- Link every used source, visual, and example in front matter.
- Include plan-required local visuals with explanation, accessibility text, and metadata.
- Explain every visual nearby and verify that its labels teach the intended relationship.
- Use the smallest useful example form. Keep external examples runnable and label inline pseudocode clearly.
- State limitations and open uncertainty.
- Include useful current terminology with provenance and maturity; omit irrelevant trends.
- Architecture chapters contain only a linked security preview.
- Security chapters map to taught components and threat model, separate preventive, detective, and recovery controls, and include tests.
