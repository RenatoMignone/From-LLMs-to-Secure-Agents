# End-to-End Attack Paths Plan

## Section purpose

Show how individually bounded weaknesses combine across the complete workflows from Pass 1.

## Learning outcomes

Construct multi-stage attack paths, identify choke points, model blast radius and persistence, layer controls, define detection timelines, contain compromised runs, revoke authority, restore state, and learn from incidents.

## Prerequisites

All earlier [component security sections](../chapter-plan.md).

## Planned child chapters

1. `01-attack-path-method-and-workflow-crosswalk.md`
2. `02-retrieved-instruction-to-unauthorized-action.md`
3. `03-memory-poisoning-to-persistent-control.md`
4. `04-compromised-tool-or-server-to-host-impact.md`
5. `05-cross-agent-delegation-and-credential-cascade.md`
6. `06-containment-eradication-recovery-and-lessons.md`

## Required concepts

Attack path, precondition, pivot, persistence, privilege amplification, blast radius, choke point, containment, eradication, recovery, and lessons learned.

## Concepts explicitly out of scope

New isolated risk catalogs, sensational scenarios, and destructive demonstrations.

## Recommended teaching order

Select workflow identifiers, chain evidence-backed component risks, test layered prevention and detection, then rehearse containment and recovery.

## Required diagrams or visuals

Swimlane attack paths, control overlays, blast-radius map, and incident timeline.

## Recommended examples

Inert scenarios with mocked tools and credentials, including detection and recovery assertions.

## Sources

Authoritative source categories: OWASP, MITRE ATLAS, NIST, primary attack benchmarks, and official advisories.

Candidate primary sources:

- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI 100-2e2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html)
- [LangChain security advisories](https://github.com/langchain-ai/langchain/security/advisories)

## Connections to later security chapters

Directly supplies scenarios and controls to [secure reference architectures](../../08-secure-reference-architectures/chapter-plan.md) and [security assurance](../../09-security-testing-evaluation-and-assurance/chapter-plan.md).

## Open questions

Which compound scenarios are representative enough to teach without implying complete coverage?

## Completion criteria

Every reference workflow has at least one traced compound attack, layered controls, observable signals, and full recovery sequence.
