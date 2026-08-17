# Contributing to From LLMs to Secure Agents

Thank you for your interest in contributing to **From LLMs to Secure Agents**. We welcome improvements to our explanations, corrections to technical inaccuracies, new grounded source records, and runnable code examples.

Please read this document before opening an issue or submitting a pull request.

---

## Core Engineering Invariants

To keep the guide rigorous, consistent, and maintainable, all contributions must respect the following invariants:

1. **Canonical Markdown**: The source of truth for all handbook chapters lives under `knowledge/`. Do not edit generated markdown or HTML in `site/` by hand. The website is automatically compiled from `knowledge/`.
2. **Strict Source Grounding**: Every technical claim, protocol detail, and security assertion must cite an official source record in `sources/<chapter-path>/<source-id>.yml`. Read `docs/evidence-policy.md`.
3. **No Em Dashes**: Do not use em dash characters (unicode U+2014) in prose. Use colons, semicolons, parentheses, or clear sentence structures instead.
4. **Visual Style**: Illustrations must follow the project cartoon visual policy (`docs/visuals-policy.md`). Visual prompts must be archived in `assets/images/<chapter-path>/source/` alongside the generated artwork. Never use ASCII or text-based diagrams in markdown.
5. **Runnable Examples**: Code samples belong in `examples/<chapter-path>/` and must include automated test coverage executed via `pytest`.

---

## Development Setup

### Prerequisites

- **Python 3.11+** with virtual environment support
- **Node.js 20+** and **npm**

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents.git
cd From-LLMs-to-Secure-Agents

# 2. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# 3. Install site dependencies
npm --prefix site install

# 4. Run the validation test suite
pytest

# 5. Build and validate the documentation site
npm --prefix site run build
npm --prefix site run check
```

---

## Contribution Workflow

### 1. Proposing Changes

- For major additions, architectural changes, or new chapters, please open an **Issue** or **Discussion** first to align on scope.
- For typo fixes, broken links, or small clarity improvements, feel free to open a Pull Request directly.

### 2. Adding or Modifying Sources

When adding a source citation:
1. Create a YAML record under `sources/<chapter-path>/<source-id>.yml`.
2. Populate all required fields according to `docs/evidence-policy.md`:
   - `id`, `title`, `url`, `publisher`, `type`, `authors`, `publication_date`, `access_date`, `summary`, and `key_points`.
3. Reference the source in the chapter front matter under `sources:`.

### 3. Writing Code Examples

When providing a runnable example:
1. Place code under `examples/<chapter-path>/`.
2. Include a `README.md` explaining how to execute the harness.
3. Add a test in `examples/<chapter-path>/tests/test_*.py` that passes under `pytest`.

### 4. Submitting a Pull Request

- Create a feature branch from `main`: `git checkout -b fix/clearer-agent-loop`.
- Follow clear, conventional commit messages: `docs: clarify tool execution step` or `feat: add boundary test for memory store`.
- Ensure all tests pass:
  ```bash
  pytest
  npm --prefix site run build
  npm --prefix site run check
  npm --prefix site test
  ```
- Fill out the PR template completely with a summary of changes and validation results.

---

## Community Guidelines

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code and treat fellow contributors with respect and professionalism.
