# Execution Environments Plan

## Section purpose

Explain where agent-selected operations run and which resources each environment exposes.

## Learning outcomes

Compare in-process functions, subprocesses, containers, user-space kernels, micro-virtual machines, remote workers, browsers, and hosted sandboxes; trace files, network, process, and resource boundaries.

## Prerequisites

[Identity, authorization, and secrets](../08-identity-authorization-and-secrets/chapter-plan.md).

## Planned child chapters

1. `01-execution-boundaries-isolation-and-sandboxes.md`
2. `02-browsers-files-networks-resources-and-cleanup.md`

## Required concepts

Host, process, namespace, container, sandbox, kernel, virtual machine, workload, image, filesystem mount, network policy, quota, and teardown.

## Concepts explicitly out of scope

Exploit development, sandbox escape detail, and hardening recipes.

## Recommended teaching order

Start with required capabilities, compare isolation mechanisms, map resources, then cover lifecycle and cleanup.

## Required diagrams or visuals

Isolation-layer comparison and execution resource map.

## Recommended examples

Mock an executor interface and resource policy; do not run generated code.

## Sources

Authoritative source categories: Official isolation and container documentation.

Candidate primary sources:

- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/)
- [Firecracker design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md)
- [Docker Engine security](https://docs.docker.com/engine/security/)
- [AutoGen extensions](https://microsoft.github.io/autogen/)

## Connections to later security chapters

[Execution and supply-chain security](../../07-security-by-component-and-workflow-stage/04-execution-and-supply-chain/chapter-plan.md).

## Open questions

Which isolation properties are required for each example class, independent of implementation?

## Completion criteria

The reader can state what each execution layer isolates, exposes, persists, and cleans up.
