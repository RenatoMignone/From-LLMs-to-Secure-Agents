# Security Policy

## Supported Versions

Because this repository maintains both an educational engineering handbook and runnable security boundary harnesses, security fixes are applied directly to the primary release branch.

| Version / Branch | Supported          |
| ---------------- | ------------------ |
| `main`           | :white_check_mark: |
| Older releases   | :x:                |

## Scope of Security Disclosures

We take the security of both the code artifacts and the published security guidance seriously. You should report:

1. **Vulnerabilities in Code Examples**: Insecure default configurations, sandbox escape vectors in test harnesses, command injection flaws, or broken credential handling in code under `examples/`.
2. **Defects in Site Runtimes**: Flaws in the static build pipeline, dependencies, or publishing scripts under `scripts/` and `site/`.
3. **Flawed Security Guidance**: Factual inaccuracies or flawed defensive architecture patterns that could lead an engineer to deploy an insecure agentic system.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.

To report a vulnerability or sensitive defect:

1. **GitHub Private Vulnerability Advisory**: Use GitHub's [Private Vulnerability Reporting](https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents/security/advisories/new) feature on this repository.
2. **Direct Contact**: If private advisories are unavailable, contact the project maintainer directly via GitHub profile: [Renato Mignone](https://github.com/RenatoMignone).

### What to Include in Your Report

To help us triage and resolve the issue quickly, please provide:
- A clear description of the vulnerability or architectural flaw.
- Steps to reproduce the issue or proof-of-concept test code.
- Affected files, chapters, or example harnesses.
- Your assessment of potential impact or blast radius.
- Any suggested remediations or mitigations.

## Response Process and Timeline

- **Initial Acknowledgement**: Within 48 hours of receipt.
- **Triage & Assessment**: Within 5 business days, confirming vulnerability validity and severity.
- **Fix & Disclosure**: We will collaborate on a fix and publish a coordinated disclosure notice with appropriate credit to the reporter.
