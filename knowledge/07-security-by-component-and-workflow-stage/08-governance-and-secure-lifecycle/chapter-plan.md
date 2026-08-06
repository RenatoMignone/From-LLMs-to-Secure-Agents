# Governance and Secure Lifecycle Plan

## Section purpose

Join technical controls to ownership, risk decisions, privacy, operations, incidents, and retirement.

## Learning outcomes

The reader can govern an agentic system from initial justification through secure development, deployment, monitoring, incident response, and decommissioning.

## Prerequisites

All earlier [component and workflow security](../chapter-plan.md) and the Pass 1 [engineering lifecycle](../../03-building-blocks/18-engineering-lifecycle-and-deployment/chapter-plan.md).

## Planned child chapters

Main path:

1. `01-risk-governance-inventory-and-accountability.md`
2. `02-secure-design-and-development-lifecycle.md`
3. `03-secure-deployment-multi-tenancy-and-change.md`
4. `04-privacy-data-governance-transparency-and-recourse.md`
5. `05-operations-vulnerability-management-and-monitoring.md`
6. `06-incident-response-evidence-and-disclosure.md`
7. `07-retirement-decommissioning-and-post-incident-learning.md`

Deep dive:

8. `08-standards-regulation-and-sector-profiles.md`

## Required concepts

Governance, owner, inventory, risk tolerance, risk acceptance, accountability, secure development lifecycle, privacy risk, transparency, recourse, vulnerability management, incident response, evidence, disclosure, retirement, and decommissioning.

## Recommended teaching order

Establish ownership and risk decisions first. Follow the product lifecycle, then treat standards and regulation as a versioned mapping rather than the guide's architecture.

## Concepts explicitly out of scope

Legal advice, universal compliance claims, and treating documentation as evidence that a control works.

## Required diagrams or visuals

- Visual: governance roles across the engineering and runtime lifecycles.
- Example: risk record, incident timeline, and decommissioning checklist linked to technical evidence.
- Framework examples: provider-neutral lifecycle controls before service-specific translations.

## Recommended code and framework examples

Use small machine-readable inventories, risk decisions, release evidence, and incident records.

## Sources

Categories: official AI risk frameworks, secure-development standards, privacy frameworks, incident guidance, and current regulations.

Candidate primary sources:

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [NCSC guidelines for secure AI system development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines)
- [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html)

## Connections to later security chapters

Reference architectures declare governance assumptions and incident responsibilities. Assurance chapters test technical claims and bound organizational conclusions.

## Open questions

How should organizations compare control evidence across agents whose models, tools, policies, and operating contexts change independently?

## Completion criteria

Every lifecycle stage has an owner, risk decision, evidence requirement, monitoring path, incident responsibility, and safe retirement procedure.
