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
## Executable example
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

## Completion checklist

- prerequisites linked;
- terms defined;
- acronyms expanded;
- every visual required by the plan is included, or the plan explicitly says none is needed;
- important claims cited;
- checked sources recorded under `sources/`;
- front matter links every used source record, visual asset, and example;
- examples runnable or marked as pseudocode;
- limitations stated;
- architecture chapters contain only a linked security preview;
- security chapters are tied to concrete components and the threat model;
- preventive, detective, and recovery controls are distinct;
- security tests are included in security chapters;
- required visuals exist locally, are explained, and have complete metadata;
- navigation updated;
- `README.md` updated.
