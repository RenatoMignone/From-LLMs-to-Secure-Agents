# Execution and Supply-Chain Security Plan

## Section purpose

Analyze hostile code, content, dependencies, tools, servers, images, and network interactions around execution.

## Learning outcomes

Model command and code injection, sandbox escape, file and network abuse, server-side request forgery, resource exhaustion, malicious packages, vulnerable dependencies, poisoned plugins, unsafe deserialization, and insecure updates.

## Prerequisites

[Threat model](../../06-threat-model/chapter-plan.md) plus Pass 1 execution and operations.

## Planned child chapters

1. `01-code-command-browser-and-file-attacks.md`
2. `02-isolation-network-and-resource-boundaries.md`
3. `03-tools-plugins-mcp-servers-and-dependencies.md`
4. `04-artifacts-images-provenance-and-updates.md`
5. `05-controls-detection-recovery-and-advisories.md`

## Required concepts

Command injection, sandbox escape, server-side request forgery, egress control, resource quota, software bill of materials, provenance, signature, dependency confusion, deserialization, patch, and rollback.

## Concepts explicitly out of scope

Dangerous exploit payloads and unsupported claims that containers equal sandboxes.

## Recommended teaching order

Trace code and content into execution, map isolation and network paths, inspect the supply chain, then apply preventive, detective, patch, quarantine, and recovery controls.

## Required diagrams or visuals

Execution trust zones, software supply chain, and advisory-to-remediation flow.

## Recommended examples

Safe command-argument validation, denied network fixture, package pin and hash check, vulnerable-version test, teardown and rollback exercise.

## Sources

Authoritative source categories: Official isolation docs, official security advisories, NIST, OWASP, and protocol security guidance.

Candidate primary sources:

- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/)
- [Firecracker design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md)
- [Docker Engine security](https://docs.docker.com/engine/security/)
- [LangChain security advisories](https://github.com/langchain-ai/langchain/security/advisories)
- [MCP trust model](https://github.com/modelcontextprotocol/modelcontextprotocol/security)
- [NIST AI security and resilience](https://www.nist.gov/artificial-intelligence/ai-research-security-and-resilience)

## Connections to later security chapters

Feeds isolated-execution and supply-chain patterns in [reference architectures](../../08-secure-reference-architectures/chapter-plan.md).

## Open questions

Which supply-chain metadata is practical for dynamically discovered tools and MCP servers?

## Completion criteria

Each execution and dependency path states isolation properties, allowed resources, provenance, monitoring, patching, teardown, and recovery.
