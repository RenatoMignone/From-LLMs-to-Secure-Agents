# Engineering Lifecycle and Deployment Plan

## Section purpose

Connect runtime architecture to requirements, ownership, environments, deployment, change, and retirement.

## Learning outcomes

The reader can define an agent product, maintain its inventory and versions, separate environments, choose a deployment topology, and manage changes through retirement.

## Prerequisites

All earlier [building blocks](../chapter-plan.md), especially evaluation, reliability, identity, and policy enforcement.

## Planned child chapters

1. `01-requirements-inventory-ownership-and-environments.md`
2. `02-deployment-change-rollback-and-retirement.md`

## Required concepts

Use-case boundary, requirement, owner, inventory, agent definition, environment, configuration, dependency, deployment topology, tenant, release, migration, rollback, retirement, and decommissioning.

## Recommended teaching order

Start with whether an agent is appropriate, then define what is owned and versioned before explaining environments and deployment changes.

## Concepts explicitly out of scope

Detailed secure-development controls, laws, procurement decisions, and provider-specific deployment tutorials.

## Required diagrams or visuals

- Visual: product lifecycle and environment-promotion map.
- Example: a versioned agent definition and release manifest.
- Framework examples: one containerized service and one managed-runtime translation.

## Recommended code and framework examples

Use declarative metadata and a mocked promotion from development through retirement.

## Sources

Categories: secure software lifecycle standards, official deployment guidance, and AI risk-management lifecycle guidance.

Candidate primary sources:

- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [NCSC guidelines for secure AI system development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines)
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

## Connections to later security chapters

The governance and secure-lifecycle branch revisits every lifecycle stage with security, privacy, accountability, and incident requirements.

## Open questions

Which metadata is portable enough to identify and reproduce an agent definition across providers and frameworks?

## Completion criteria

The reader can trace both one agent run and the complete lifecycle of the product that executes it.
