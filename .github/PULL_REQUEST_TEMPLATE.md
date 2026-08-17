## Description

Please provide a clear and concise summary of the changes introduced in this pull request.

- **What is being changed?**
- **Why is this change necessary?**
- **Which chapters, examples, or policies are affected?**

---

## Type of Change

- [ ] 📖 Content update or clarification (under `knowledge/`)
- [ ] 🔍 Grounded source addition or update (under `sources/`)
- [ ] 🧪 Example code or test harness update (under `examples/`)
- [ ] 🌐 Documentation site feature or style tweak (under `site/`)
- [ ] ⚙️ Tooling or publishing pipeline fix (under `scripts/`)
- [ ] 🔒 Security fix or vulnerability mitigation

---

## Engineering Checklist

Before requesting a review, please confirm the following:

- [ ] Canonical markdown under `knowledge/` was edited directly (not generated files).
- [ ] All new claims are grounded in official source YAML records under `sources/`.
- [ ] Visual assets follow the cartoon style policy and prompt text is saved in `source/`.
- [ ] No em dashes (unicode U+2014) are used in prose.
- [ ] Python test suite passes (`pytest`).
- [ ] Site build and validation checks pass (`npm --prefix site run build && npm --prefix site run check`).
- [ ] Node tests pass (`npm --prefix site test`).
