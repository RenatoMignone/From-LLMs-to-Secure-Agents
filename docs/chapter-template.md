# Chapter Templates

## Architecture chapters

Required core sections:
- `## Why this matters`: problem and motivation in plain language.
- `## How it works`: mechanisms, concepts, and precise technical definitions.
- `## Security preview`: brief forward-linked note; no detailed attacks or tests.
- `## Key takeaways`: core summary points.
- `## References`: citable primary sources.

Optional contextual sections (include only when relevant; omit when not needed):
`## Simple mental model`, `## Position in the agent workflow`, `## Main variants`, `## Minimal implementation`, `## Framework implementations`, `## Data flow and state changes`, `## Trust boundaries`, `## Reliability failures`, `## Worked example`, `## Limitations and trade-offs`, `## Open research questions`.

Do not include empty sections or placeholder filler. Personalize structure to the topic.

## Security chapters

Required core sections:
- `## Architecture and workflow scope`: links to Pass 1 components.
- `## Threat model assumptions`: attacker access and trust assumptions.
- `## Failures and attacks`: concrete failure modes.
- `## Preventive controls`: boundary enforcement and guardrails.
- `## Key takeaways`: core summary points.
- `## References`: citable primary sources.

Optional contextual sections (include only when relevant; omit when not needed):
`## Assets and trust boundaries`, `## Detective controls`, `## Recovery controls`, `## Security tests`, `## Secure design pattern`, `## Limitations and residual risk`, `## Open research questions`.

## Field terminology

Add a short subsection inside the relevant section when terms help the reader. Map each term to a concrete mechanism with its maturity and citation.

## Quality checklist

- Use simple, accessible English. Define exact technical terms before use.
- Begin with a familiar situation; avoid unexplained software vocabulary.
- Include only sections with substantive content; omit unnecessary headings.
- Determine the number of visuals (0 to many) based on educational need to maximize comprehension.
- Never create ASCII or text schemas; generate cartoon visuals for all architectural diagrams.
- Include a next-unit reading link or button at the end of each unit.
- Link every source, visual, and example in front matter.
- Explain every visual nearby.
