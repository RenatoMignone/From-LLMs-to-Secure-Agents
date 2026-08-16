import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(SITE_ROOT, '..');

const BASE_URL = '/From-LLMs-to-Secure-Agents';
const SITE_ORIGIN = 'https://renatomignone.github.io';

const DOCS_DIR = path.join(SITE_ROOT, 'src', 'content', 'docs');
const PUBLIC_DIR = path.join(SITE_ROOT, 'public');
const PUBLIC_ASSETS_DIR = path.join(PUBLIC_DIR, 'assets', 'images');
const SRC_ASSETS_DIR = path.join(SITE_ROOT, 'src', 'assets', 'images');
const PUBLIC_MARKDOWN_DIR = path.join(PUBLIC_DIR, 'markdown');

console.log('🚀 Running From-LLMs-to-Secure-Agents visual build pipeline...');

// 1. Clean output directories
fs.rmSync(DOCS_DIR, { recursive: true, force: true });
fs.mkdirSync(DOCS_DIR, { recursive: true });

fs.rmSync(PUBLIC_ASSETS_DIR, { recursive: true, force: true });
fs.mkdirSync(PUBLIC_ASSETS_DIR, { recursive: true });

fs.rmSync(SRC_ASSETS_DIR, { recursive: true, force: true });
fs.mkdirSync(SRC_ASSETS_DIR, { recursive: true });

fs.rmSync(PUBLIC_MARKDOWN_DIR, { recursive: true, force: true });
fs.mkdirSync(PUBLIC_MARKDOWN_DIR, { recursive: true });

// 2. Copy image assets
function copyDirRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== 'source') {
        copyDirRecursive(srcPath, destPath);
      }
    } else if (/\.(png|webp|jpg|jpeg|svg)$/i.test(entry.name)) {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

console.log('📦 Copying image assets...');
copyDirRecursive(path.join(REPO_ROOT, 'assets', 'images'), PUBLIC_ASSETS_DIR);
copyDirRecursive(path.join(REPO_ROOT, 'assets', 'images'), SRC_ASSETS_DIR);

// 3. Load all sources
console.log('📚 Indexing verified sources...');
const sourceIndex = new Map();

function indexSources(dir) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      indexSources(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.yml')) {
      try {
        const raw = fs.readFileSync(fullPath, 'utf8');
        const doc = yaml.parse(raw);
        if (doc && doc.id) {
          sourceIndex.set(doc.id, doc);
          const relPath = path.relative(path.join(REPO_ROOT, 'sources'), fullPath);
          sourceIndex.set(relPath, doc);
        }
      } catch (err) {
        console.warn(`Warning: failed to parse source YAML at ${fullPath}:`, err.message);
      }
    }
  }
}

indexSources(path.join(REPO_ROOT, 'sources'));
console.log(`✓ Indexed ${sourceIndex.size} source records.`);

// 4. Define Canonical Chapters to Publish (Agent Foundations + Least Privilege Primer)
console.log('📖 Processing canonical knowledge chapters for Foundations...');

function parseChapterFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/^(?:<!--\s*)?---\n([\s\S]*?)\n---\s*(?:-->)?\n?([\s\S]*)$/);
  if (!match) return null;
  let frontmatter = {};
  try {
    frontmatter = yaml.parse(match[1]) || {};
  } catch (e) {
    console.error(`Error parsing frontmatter in ${filePath}:`, e);
    return null;
  }
  const body = match[2];
  return { frontmatter, body };
}

// Configured list of chapters to publish on the site with keyword-rich URLs
const publishedChapterConfigs = [
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '01-agent-foundations', '01-what-is-an-agent.md'),
    sourceSubDir: '01-agent-foundations/01-what-is-an-agent',
    slug: 'what-is-an-ai-agent',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 1,
  },
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '01-agent-foundations', '02-the-agent-loop.md'),
    sourceSubDir: '01-agent-foundations/02-the-agent-loop',
    slug: 'the-agent-loop-explained',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 2,
  },
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '01-agent-foundations', '03-workflows-versus-agents.md'),
    sourceSubDir: '01-agent-foundations/03-workflows-versus-agents',
    slug: 'workflows-versus-autonomous-agents',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 3,
  },
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '01-agent-foundations', '04-goals-policies-environments-and-autonomy.md'),
    sourceSubDir: '01-agent-foundations/04-goals-policies-environments-and-autonomy',
    slug: 'goals-policies-environments-and-autonomy',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 4,
  },
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '01-agent-foundations', '05-run-lifecycle-and-termination.md'),
    sourceSubDir: '01-agent-foundations/05-run-lifecycle-and-termination',
    slug: 'run-lifecycle-and-termination',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 5,
  },
  {
    filePath: path.join(REPO_ROOT, 'knowledge', '00-prerequisites', '04-identity-authority-and-least-privilege-primer.md'),
    sourceSubDir: '00-prerequisites/04-identity-authority-and-least-privilege-primer',
    slug: 'identity-authority-and-least-privilege',
    routeDir: 'foundations',
    category: 'Agent Foundations',
    order: 6,
  },
];

const processedChapters = [];

for (const cfg of publishedChapterConfigs) {
  if (fs.existsSync(cfg.filePath)) {
    const parsed = parseChapterFile(cfg.filePath);
    if (parsed) {
      processedChapters.push({
        ...cfg,
        frontmatter: parsed.frontmatter,
        body: parsed.body,
      });
    }
  }
}

console.log(`✓ Prepared ${processedChapters.length} foundational chapters for publication.`);

// Link rewriting helper for clean URLs
function rewriteLinks(markdown) {
  let text = markdown.replace(
    /!\[(.*?)\]\((\.\.\/)*assets\/images\/(.*?)\)/g,
    `![$1](${BASE_URL}/assets/images/$3)`
  );

  // Chapter cross-links mapping
  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/01-what-is-an-agent\.md\)/g, `[$1](${BASE_URL}/foundations/what-is-an-ai-agent/)`);
  text = text.replace(/\[(.*?)\]\(01-what-is-an-agent\.md\)/g, `[$1](${BASE_URL}/foundations/what-is-an-ai-agent/)`);

  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/02-the-agent-loop\.md\)/g, `[$1](${BASE_URL}/foundations/the-agent-loop-explained/)`);
  text = text.replace(/\[(.*?)\]\(02-the-agent-loop\.md\)/g, `[$1](${BASE_URL}/foundations/the-agent-loop-explained/)`);

  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/03-workflows-versus-agents\.md\)/g, `[$1](${BASE_URL}/foundations/workflows-versus-autonomous-agents/)`);
  text = text.replace(/\[(.*?)\]\(03-workflows-versus-agents\.md\)/g, `[$1](${BASE_URL}/foundations/workflows-versus-autonomous-agents/)`);

  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/04-goals-policies-environments-and-autonomy\.md\)/g, `[$1](${BASE_URL}/foundations/goals-policies-environments-and-autonomy/)`);
  text = text.replace(/\[(.*?)\]\(04-goals-policies-environments-and-autonomy\.md\)/g, `[$1](${BASE_URL}/foundations/goals-policies-environments-and-autonomy/)`);

  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/05-run-lifecycle-and-termination\.md\)/g, `[$1](${BASE_URL}/foundations/run-lifecycle-and-termination/)`);
  text = text.replace(/\[(.*?)\]\(05-run-lifecycle-and-termination\.md\)/g, `[$1](${BASE_URL}/foundations/run-lifecycle-and-termination/)`);

  text = text.replace(/\[(.*?)\]\((\.\.\/)?00-prerequisites\/04-identity-authority-and-least-privilege-primer\.md\)/g, `[$1](${BASE_URL}/foundations/identity-authority-and-least-privilege/)`);
  text = text.replace(/\[(.*?)\]\(04-identity-authority-and-least-privilege-primer\.md\)/g, `[$1](${BASE_URL}/foundations/identity-authority-and-least-privilege/)`);

  // Section & Roadmap links
  text = text.replace(/\[(.*?)\]\((\.\.\/)?00-prerequisites\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/foundations/what-is-an-ai-agent/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?01-agent-foundations\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/foundations/what-is-an-ai-agent/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?02-agent-architectures\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/architecture/selection-and-tradeoffs/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?03-building-blocks\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/building-blocks/components-overview/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?06-threat-model\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/security/securing-ai-agents/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?07-security-by-component-and-workflow-stage\/chapter-plan\.md\)/g, `[$1](${BASE_URL}/security/securing-ai-agents/)`);
  text = text.replace(/\[(.*?)\]\((\.\.\/)?chapter-plan\.md\)/g, `[$1](${BASE_URL}/overview/curriculum/)`);

  return text;
}

// 5. Generate Chapter Pages
const guideIndex = [];

for (let i = 0; i < processedChapters.length; i++) {
  const ch = processedChapters[i];
  const fm = ch.frontmatter;
  const prevCh = i > 0 ? processedChapters[i - 1] : null;
  const nextCh = i < processedChapters.length - 1 ? processedChapters[i + 1] : null;

  const outDir = path.join(DOCS_DIR, ch.routeDir);
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `${ch.slug}.md`);

  const rawMarkdownDir = path.join(PUBLIC_MARKDOWN_DIR, ch.routeDir);
  fs.mkdirSync(rawMarkdownDir, { recursive: true });
  const rawMarkdownPath = path.join(rawMarkdownDir, `${ch.slug}.md`);

  const canonicalUrl = `${SITE_ORIGIN}${BASE_URL}/${ch.routeDir}/${ch.slug}/`;
  const markdownUrl = `${SITE_ORIGIN}${BASE_URL}/markdown/${ch.routeDir}/${ch.slug}.md`;

  // Build Sources panel
  const sourcesData = [];
  if (fm.source_records && Array.isArray(fm.source_records)) {
    for (const srcId of fm.source_records) {
      const srcDoc = sourceIndex.get(srcId) || sourceIndex.get(`${ch.sourceSubDir}/${srcId}.yml`);
      if (srcDoc) {
        sourcesData.push(srcDoc);
      }
    }
  }

  // Register in Guide Index
  guideIndex.push({
    unit_id: fm.unit_id,
    title: fm.title,
    summary: fm.summary,
    pass: fm.pass,
    learning_path: fm.learning_path,
    status: fm.status,
    last_reviewed: fm.last_reviewed,
    html_url: canonicalUrl,
    markdown_url: markdownUrl,
    prerequisites: fm.prerequisites || [],
    learning_objectives: fm.learning_objectives || [],
    source_records: sourcesData.map((s) => ({
      id: s.id,
      title: s.title,
      authors_or_organization: s.authors_or_organization,
      date: s.date,
      source_type: s.source_type,
      canonical_url: s.canonical_url,
      claims_supported: s.claims_supported || [],
      limitations: s.limitations || [],
    })),
    visual_assets: fm.visual_assets || [],
    example_paths: fm.example_paths || [],
  });

  // JSON-LD Structured Data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: fm.title,
    description: fm.summary,
    url: canonicalUrl,
    dateModified: fm.last_reviewed,
    inLanguage: 'en-US',
    isPartOf: {
      '@type': 'Book',
      name: 'From LLMs to Secure Agents',
      url: `${SITE_ORIGIN}${BASE_URL}/`,
    },
    author: {
      '@type': 'Organization',
      name: 'From LLMs to Secure Agents Project',
      url: 'https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents',
    },
    educationalLevel: 'Core Engineering Curriculum',
  };

  // Starlight Frontmatter
  const starlightFm = {
    title: fm.title,
    description: fm.summary,
    head: [
      {
        tag: 'script',
        attrs: { type: 'application/ld+json' },
        content: JSON.stringify(jsonLd),
      },
      {
        tag: 'link',
        attrs: { rel: 'alternate', type: 'text/markdown', href: markdownUrl, title: `${fm.title} (Markdown)` },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:title', content: `${fm.title} | From LLMs to Secure Agents` },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:description', content: fm.summary },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
      },
    ],
  };

  const passLabel = 'Pass 1: Architecture';
  const pathLabel = 'Core Curriculum';
  const statusLabel = 'Verified & Grounded';

  let pageContent = `---
${yaml.stringify(starlightFm)}---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-pass">${passLabel}</span>
  <span class="meta-badge badge-unit">${fm.unit_id}</span>
  <span class="meta-badge badge-path">${pathLabel}</span>
  <span class="meta-badge badge-status">✓ ${statusLabel}</span>
  <span class="meta-reviewed">Reviewed: ${fm.last_reviewed}</span>
</div>

<div class="chapter-summary not-content">
  <strong>Key Takeaway:</strong> ${fm.summary}
</div>
`;

  // Prerequisites & Objectives Cards
  const hasPrereqs = fm.prerequisites && fm.prerequisites.length > 0;
  const hasObjectives = fm.learning_objectives && fm.learning_objectives.length > 0;

  if (hasPrereqs || hasObjectives) {
    pageContent += `\n<div class="guide-callout-grid not-content">\n`;
    if (hasPrereqs) {
      pageContent += `  <div class="callout-card callout-prereqs">
    <h3>📌 What You Should Know</h3>
    <ul>
${fm.prerequisites.map((p) => `      <li>${p}</li>`).join('\n')}
    </ul>
  </div>\n`;
    }
    if (hasObjectives) {
      pageContent += `  <div class="callout-card callout-objectives">
    <h3>🎯 Learning Goals</h3>
    <ul>
${fm.learning_objectives.map((o) => `      <li>${o}</li>`).join('\n')}
    </ul>
  </div>\n`;
    }
    pageContent += `</div>\n\n`;
  }

  // Body clean up
  let cleanBody = ch.body.trim();
  cleanBody = cleanBody.replace(/^#\s+[^\n]+\n+/, '');
  cleanBody = rewriteLinks(cleanBody);

  pageContent += cleanBody;

  // Build Sources & Evidence accordion
  if (sourcesData.length > 0) {
    pageContent += `\n\n<details class="evidence-panel not-content">
  <summary>
    <span>🔍 Verified Evidence & Source Citations (${sourcesData.length} primary records)</span>
    <span style="font-size: 0.85rem; font-weight: normal;">Click to view claims & verification</span>
  </summary>
  <div class="evidence-content">
${sourcesData
  .map(
    (s) => `    <div class="source-card">
      <div class="source-card-header">
        <a href="${s.canonical_url}" target="_blank" rel="noopener noreferrer" class="source-title">${s.title} ↗</a>
        <span class="source-type-tag">${s.source_type}</span>
      </div>
      <div class="source-meta">
        <strong>Organization / Author:</strong> ${s.authors_or_organization} &bull; 
        <strong>Date:</strong> ${s.date} ${s.version ? `(v${s.version})` : ''} &bull; 
        <strong>Verified:</strong> ${s.last_verified}
      </div>
      ${
        s.claims_supported && s.claims_supported.length > 0
          ? `<div><strong>Exact Claims Grounded:</strong>
        <ul class="claim-list">
          ${s.claims_supported.map((c) => `<li>${c}</li>`).join('')}
        </ul>
      </div>`
          : ''
      }
      ${
        s.limitations && s.limitations.length > 0
          ? `<div style="margin-top: 0.5rem; font-size: 0.82rem; color: var(--sl-color-gray-3);">
        <strong>Scope & Limitations:</strong> ${s.limitations.join(' ')}
      </div>`
          : ''
      }
    </div>`
  )
  .join('\n')}
  </div>
</details>\n`;
  }

  // Sequential Navigation Grid
  pageContent += `\n<div class="chapter-nav-grid not-content">\n`;
  if (prevCh) {
    pageContent += `  <a href="${BASE_URL}/${prevCh.routeDir}/${prevCh.slug}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Previous Chapter</div>
    <div class="nav-title">${prevCh.frontmatter.title}</div>
  </a>\n`;
  } else {
    pageContent += `  <a href="${BASE_URL}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Overview</div>
    <div class="nav-title">Handbook Introduction</div>
  </a>\n`;
  }

  if (nextCh) {
    pageContent += `  <a href="${BASE_URL}/${nextCh.routeDir}/${nextCh.slug}/" class="nav-card nav-card-next">
    <div class="nav-label">Next Chapter →</div>
    <div class="nav-title">${nextCh.frontmatter.title}</div>
  </a>\n`;
  } else {
    pageContent += `  <a href="${BASE_URL}/security/securing-ai-agents/" class="nav-card nav-card-next">
    <div class="nav-label">Continue to Security Hubs →</div>
    <div class="nav-title">Securing AI Agents (Master Guide)</div>
  </a>\n`;
  }
  pageContent += `</div>\n`;

  // Write Starlight Markdown
  fs.writeFileSync(outPath, pageContent, 'utf8');

  // Write Clean Canonical Markdown alternate
  const cleanMarkdown = `---
title: ${JSON.stringify(fm.title)}
unit_id: ${JSON.stringify(fm.unit_id)}
summary: ${JSON.stringify(fm.summary)}
pass: ${JSON.stringify(fm.pass)}
learning_path: ${JSON.stringify(fm.learning_path)}
status: ${JSON.stringify(fm.status)}
last_reviewed: ${JSON.stringify(fm.last_reviewed)}
canonical_url: ${JSON.stringify(canonicalUrl)}
---

# ${fm.title}

> **Summary:** ${fm.summary}
> **Unit ID:** ${fm.unit_id} | **Status:** ${fm.status}

${ch.body.trim()}

## Source Records
${sourcesData.map((s) => `- [${s.title}](${s.canonical_url}) (${s.authors_or_organization}, ${s.date})`).join('\n')}
`;
  fs.writeFileSync(rawMarkdownPath, cleanMarkdown, 'utf8');
}

console.log('✓ Generated all foundational chapter documents and markdown alternates.');

// 6. Generate Security Hub Pages
console.log('🛡️ Generating curated security hub pages...');
const securityDir = path.join(DOCS_DIR, 'security');
fs.mkdirSync(securityDir, { recursive: true });

const securityHubs = [
  {
    slug: 'securing-ai-agents',
    title: 'Securing AI Agents: The Master Engineering Guide',
    desc: 'Core architecture, threat modeling, untrusted data perimeters, and zero-trust controls for agentic systems.',
    content: `
## Why Securing Autonomous Agents is a Paradigm Shift

Traditional application security enforces deterministic control flow: programs execute developer-written logic, and user input is treated as passive data.

In an autonomous LLM agent, **untrusted input data directly dictates execution logic**. When a reasoning model consumes an email, webpage, PDF, or API payload, that untrusted content enters the reasoning loop and directly decides which tools the agent invokes.

<div class="visual-scheme-card not-content">
  <img src="${BASE_URL}/assets/images/01-agent-foundations/02-the-agent-loop/01-agent-loop-cycle.png" alt="Cyclic Agent Loop Architecture: Context, Reasoning, Tool Dispatch, Observation, and Termination" />
  <figcaption>The 5-Step Cyclic Agent Loop: Data flows from observations back into reasoning context, creating runtime injection attack surfaces.</figcaption>
</div>

## Fundamental Defensive Principles

1. **Strict Data & Control Flow Separation**: Never let untrusted observations cross into tool invocation without parameter validation and schema filtering.
   - 📖 *Core Foundation:* [What is an AI Agent](${BASE_URL}/foundations/what-is-an-ai-agent/)
2. **Principal vs. Actor Identity & Least Privilege**: The agent process must execute with ephemeral, downscoped tokens strictly limited to the immediate sub-task, never inheriting master user credentials.
   - 📖 *Core Foundation:* [Identity, Authority & Least Privilege](${BASE_URL}/foundations/identity-authority-and-least-privilege/)
3. **Deterministic Run Lifecycles & Human Gates**: Enforce hard step limits, execution cost budgets, and approval checkpoints before high-consequence state changes.
   - 📖 *Core Foundation:* [Run Lifecycle and Termination](${BASE_URL}/foundations/run-lifecycle-and-termination/)

## Dedicated Security Guides in this Section

- ⚔️ [Indirect Prompt Injection & Context Security](${BASE_URL}/security/indirect-prompt-injection-defense/)
- 🔑 [Identity, Scoped Tokens & Least Privilege](${BASE_URL}/security/identity-and-scoped-delegation/)
- ⚙️ [Tools, Function Calling & Excessive Agency](${BASE_URL}/security/tools-and-excessive-agency-prevention/)
- 📦 [Execution Environments & Sandboxing](${BASE_URL}/security/execution-environments-and-sandboxing/)
- 🔌 [Model Context Protocol (MCP) Security](${BASE_URL}/security/model-context-protocol-security/)
`,
  },
  {
    slug: 'indirect-prompt-injection-defense',
    title: 'Indirect Prompt Injection & Context Security',
    desc: 'Understanding how adversarial payloads inside external data hijack agent loops, and implementing multi-layer isolation.',
    content: `
## Threat Mechanism: Hijacking the Reasoning Loop

Indirect prompt injection occurs when an attacker hides adversarial instructions inside data retrieved by an agent (e.g. a webpage, customer ticket, calendar invite, or database record).

When the agent incorporates this observation into its context window, the language model follows the attacker's hidden instructions instead of the user's objective.

<div class="visual-scheme-card not-content">
  <img src="${BASE_URL}/assets/images/01-agent-foundations/04-goals-policies-environments-and-autonomy/01-goals-policies-environments-autonomy.png" alt="Goals, Policies, and Environments Autonomy Spectrum" />
  <figcaption>Enforcing protective policy guardrails between external environments and autonomous agent goal execution.</figcaption>
</div>

## Architectural Defense Patterns

1. **Context Tagging & Structural Delimitation**: Enforce clear XML/JSON schema wrappers around untrusted data, explicitly instructing the model that contents are non-executable observation payload.
2. **Dual-Model Parsing & Sanitization**: Employ a lightweight, toolless reader model to parse and summarize third-party inputs before passing structured text to the decision-making agent.
3. **Tool Parameter Verification**: Constrain tool dispatchers with strict parameter schemas that reject unauthorized URLs, shell characters, or unapproved targets.
`,
  },
  {
    slug: 'identity-and-scoped-delegation',
    title: 'Identity, Scoped Delegation & Token Exchange',
    desc: 'Preventing confused deputy vulnerabilities with OAuth 2.0 token exchange, actor-principal separation, and least privilege.',
    content: `
## The Confused Deputy in AI Agents

When an agent acts on behalf of a human user, the downstream API must distinguish:
- **The Principal**: The user initiating the task and holding master permissions.
- **The Actor**: The autonomous agent executing the individual API calls.

If the agent uses the user's permanent high-privilege bearer token, an attacker who injects a prompt into the agent's context gains the user's full authority.

<div class="visual-scheme-card not-content">
  <img src="${BASE_URL}/assets/images/00-prerequisites/04-identity-authority-and-least-privilege-primer/01-identity-delegation-least-privilege.png" alt="Identity Delegation and Least Privilege Workflow" />
  <figcaption>Scoped delegation workflow: Principal delegates downscoped actor tokens through an authorization filter enforcing least privilege.</figcaption>
</div>

## Recommended Implementation: RFC 8693 Token Exchange

Instead of passing static API keys, the agent requests short-lived, downscoped tokens for each tool invocation (e.g. read-only calendar access for 5 minutes).

📖 *Foundational Unit:* [Identity, Authority and Least Privilege](${BASE_URL}/foundations/identity-authority-and-least-privilege/)
`,
  },
  {
    slug: 'tools-and-excessive-agency-prevention',
    title: 'Tools, Function Calling & Excessive Agency',
    desc: 'Constraining tool discretion, parameter validation, idempotency, and human approval checkpoints.',
    content: `
## Excessive Agency Risks

Excessive agency arises when an agent is provided with tools that have more capability or wider blast radiuses than necessary for its intended role (e.g. granting full SQL write access instead of a single constrained query endpoint).

## Defense Architecture

1. **Strict JSON Schema Enforcement**: Validate every tool parameter against a strict JSON schema before executing the request.
2. **Idempotency Keys**: Guarantee that retries and loops cannot cause duplicate transactions or state corruptions.
3. **Confirmation Gates (Human-in-the-Loop)**: Require explicit human confirmation before executing any irreversible action (sending emails, deleting records, executing financial transactions).
`,
  },
  {
    slug: 'execution-environments-and-sandboxing',
    title: 'Execution Environments & Sandbox Isolation',
    desc: 'Hardening code execution, microVM isolation, container boundaries, and network egress rules.',
    content: `
## Isolating Dynamic Code Execution

When an agent writes and runs code (Python, Bash, SQL, JavaScript), execution must be completely isolated from host systems:
- **MicroVMs / Container Runtimes**: Utilize Firecracker MicroVMs or gVisor container runtimes with ephemeral lifetimes.
- **Egress Filtering**: Block access to internal cloud metadata IP addresses (\`169.254.169.254\`) and private subnets.
- **Resource Constraints**: Enforce hard memory, CPU, and execution timeout limits on every container instance.
`,
  },
  {
    slug: 'model-context-protocol-security',
    title: 'Model Context Protocol (MCP) Security',
    desc: 'Securing host-client-server boundaries, tool discovery schemas, and resource access controls in MCP.',
    content: `
## MCP Architecture & Attack Surfaces

The Model Context Protocol (MCP) establishes an open standard for connecting LLMs to external data and tools across Hosts, Clients, and Servers:
- **Host**: Orchestrates LLM reasoning and user interactions.
- **Client**: Connects to and queries one or more MCP servers.
- **Server**: Exposes tools, prompts, and resources.

## Security Controls for MCP

- **Server Verification**: Ensure MCP clients only connect to vetted, authentic servers.
- **Tool Description Sanitization**: Protect against prompt injection embedded within malicious MCP tool descriptions.
- **Strict Path Filtering**: Prevent directory traversal when exposing local filesystem resources.
`,
  },
];

for (const hub of securityHubs) {
  fs.writeFileSync(
    path.join(securityDir, `${hub.slug}.md`),
    `---
title: "${hub.title}"
description: "${hub.desc}"
---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-path">Security Topic Hub</span>
  <span class="meta-badge badge-status">Architecture & Defenses</span>
</div>

${hub.content}

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/foundations/what-is-an-ai-agent/" class="nav-card nav-card-prev">
    <div class="nav-label">← Foundations</div>
    <div class="nav-title">What is an AI Agent</div>
  </a>
  <a href="${BASE_URL}/overview/curriculum/" class="nav-card nav-card-next">
    <div class="nav-label">Roadmap →</div>
    <div class="nav-title">Master Curriculum & Architecture</div>
  </a>
</div>
`,
    'utf8'
  );
}

// 7. Generate Architecture & Building Blocks Roadmap Overview Pages
const archDir = path.join(DOCS_DIR, 'architecture');
fs.mkdirSync(archDir, { recursive: true });

fs.writeFileSync(
  path.join(archDir, 'selection-and-tradeoffs.md'),
  `---
title: "02 Agent Architectures & Patterns"
description: "Design patterns for agentic systems: single-agent loops, plan-and-execute, evaluator-optimizer, state machine graphs, and supervisors."
---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-path">Pass 1: Architecture Queue</span>
  <span class="meta-badge badge-status">Roadmap Queue</span>
</div>

## Architectural Patterns Overview

Autonomous agentic systems utilize distinct reasoning and coordination architectures depending on task complexity, reliability requirements, and latency constraints:

<div class="visual-scheme-card not-content">
  <img src="${BASE_URL}/assets/images/01-agent-foundations/03-workflows-versus-agents/01-workflows-vs-agents-spectrum.png" alt="Workflows vs Agents Design Spectrum" />
  <figcaption>The Spectrum from Deterministic Workflows to Fully Autonomous Agent Reasoning Loops.</figcaption>
</div>

### Architectural Topology Roadmap

1. **Single-Agent & Reactive Loops**: ReAct (Reason + Act) loop with dynamic tool discovery.
2. **Sequential & Parallel Workflows**: Fixed routing pipelines with deterministic state propagation.
3. **Plan-and-Execute**: Decoupled multi-step planner generating a directed graph of sub-tasks for execution workers.
4. **Evaluator-Optimizer & Reflection**: Dual-loop architecture with an evaluator model validating outputs against quality criteria.
5. **State Machines & Event-Driven Graphs**: Formal graph architectures with explicit state transitions, checkpoints, and interrupt resume points.
6. **Supervisors & Multi-Agent Topologies**: Hierarchical coordinator delegating specialized domain tasks to worker agents.

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/foundations/run-lifecycle-and-termination/" class="nav-card nav-card-prev">
    <div class="nav-label">← Previous Chapter</div>
    <div class="nav-title">Run Lifecycle and Termination</div>
  </a>
  <a href="${BASE_URL}/overview/curriculum/" class="nav-card nav-card-next">
    <div class="nav-label">Master Plan →</div>
    <div class="nav-title">View Master Curriculum Roadmap</div>
  </a>
</div>
`,
  'utf8'
);

const blocksDir = path.join(DOCS_DIR, 'building-blocks');
fs.mkdirSync(blocksDir, { recursive: true });

fs.writeFileSync(
  path.join(blocksDir, 'components-overview.md'),
  `---
title: "03 Agent Building Blocks & Subsystems"
description: "In-depth engineering breakdown of context budgets, working memory, RAG, tool calling, execution sandboxes, and observability."
---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-path">Pass 1: Building Blocks Queue</span>
  <span class="meta-badge badge-status">Roadmap Queue</span>
</div>

## System Building Blocks Breakdown

Building robust, enterprise-grade agents requires mastering specialized subsystems:

- **Context Construction & Budgets**: Context precedence, token budget allocation, history compression, and provenance debugging.
- **State & Lifecycle Management**: Thread models, checkpoint serialization, interruptible human-in-the-loop workflows, and idempotent retries.
- **Short-Term & Persistent Memory**: Working memory buffers, semantic memory stores, entity extraction, and consolidation lifecycles.
- **Retrieval & Agentic RAG**: Hybrid sparse/dense search, chunking strategies, GraphRAG, reranking, and multi-hop reasoning.
- **Tools & Function Calling**: Schema generation, tool routing, parameter validation, and exception handling.
- **Execution Sandboxing**: Containerization, microVM runtimes (gVisor/Firecracker), ephemeral filesystems, and egress network isolation.
- **Observability & Tracing**: Step-by-step token usage tracking, span telemetry, latency tracing, and failure diagnostics.

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/architecture/selection-and-tradeoffs/" class="nav-card nav-card-prev">
    <div class="nav-label">← Architectures</div>
    <div class="nav-title">Agent Architectures & Patterns</div>
  </a>
  <a href="${BASE_URL}/security/securing-ai-agents/" class="nav-card nav-card-next">
    <div class="nav-label">Security Hubs →</div>
    <div class="nav-title">Securing AI Agents (Master Guide)</div>
  </a>
</div>
`,
  'utf8'
);

// 8. Generate Overview and Reference Pages
const overviewDir = path.join(DOCS_DIR, 'overview');
fs.mkdirSync(overviewDir, { recursive: true });

fs.writeFileSync(
  path.join(overviewDir, 'curriculum.md'),
  `---
title: "Curriculum & Two-Pass Architecture"
description: "The complete dependency-ordered roadmap: Understanding the complete system before analyzing threats and defenses."
---

## The Two-Pass Learning Philosophy

Agent security cannot be understood effectively through disconnected vulnerability lists. An engineer cannot defend a system whose internal mechanics, trust boundaries, and execution loops they do not fully understand.

\`\`\`
PASS 1: UNDERSTAND THE SYSTEM
├── 01 Agent Foundations (Autonomous Loops, Workflows vs Agents, Autonomy, Lifecycles, Scoped Authority)
├── 02 Agent Architectures (ReAct, Plan & Execute, Reflection, State Machine Graphs, Multi-Agent)
├── 03 Building Blocks (Context, Working & Long-Term Memory, RAG, Tools, Sandboxes, Tracing)
├── 04 Frameworks & Protocols (Model Context Protocol / MCP, Agent-to-Agent Protocols)
└── 05 End-to-End Workflows (Reference Enterprise Production Architecture)
\`\`\`

\`\`\`
PASS 2: SECURE THE SYSTEM
├── 06 Threat Model (Assets, Adversaries, Entry Points, Attack Vector Taxonomy)
├── 07 Security by Component (Indirect Prompt Injection, Memory Poisoning, Excessive Agency, Sandboxes)
├── 08 Secure Reference Architectures (Zero-Trust Gateways, Dual-Agent Supervisors)
├── 09 Testing & Assurance (Automated Red Teaming, Injection Fuzzing, Invariant Verification)
└── 10 Open Research Questions (Formal Loop Verification, Unforgeable Data Provenance)
\`\`\`

## Main Path vs. Deep Dives

To keep learning fast and focused without sacrificing rigor, the guide clearly distinguishes:
1. **Core Curriculum**: The mandatory linear path through foundational agent architecture and defensive controls.
2. **Deep Dives**: Specialized technical branches (advanced protocols, mathematical optimization, framework internals) that can be explored on demand.
`,
  'utf8'
);

fs.writeFileSync(
  path.join(overviewDir, 'methodology.md'),
  `---
title: "Evidence & Autonomous Verification Methodology"
description: "How every claim in this handbook is grounded in primary specifications, standards, and verified records."
---

## Source-Grounded Evidence Standards

Every architectural mechanism and defensive recommendation in this handbook is anchored in primary sources:
- **Standards & Specifications**: IETF RFCs (HTTP, OAuth 2.0 Token Exchange), W3C Recommendations, NIST AI Risk Management Framework.
- **Protocol Documentation**: Model Context Protocol (MCP) specifications, OpenAPI standards.
- **Peer-Reviewed Research**: Foundational academic papers on agent loops, reasoning graphs, and prompt injection attacks.
- **Official Security Advisories**: MITRE ATLAS taxonomy, OWASP Top 10 for LLMs and Agents, CVE advisories.

## Continuous Mechanical Verification

Every chapter and source record is automatically verified on every commit:
- **Bidirectional Citations**: All citations resolve to checked source records in \`sources/\`.
- **Local Visual Manifests**: All illustrations are locally stored, traceable to generative prompts, and strictly avoid SVG or text schemas.
- **Reproducible Automated Testing**: Continuous CI/CD testing enforces structural invariants, link integrity, and schema compliance.
`,
  'utf8'
);

const refDir = path.join(DOCS_DIR, 'reference');
fs.mkdirSync(refDir, { recursive: true });

fs.writeFileSync(
  path.join(refDir, 'glossary.md'),
  `---
title: "System Glossary & Concepts"
description: "Precise definitions of core agentic and security engineering concepts."
---

| Term | Domain | Definition | Authoritative Chapter |
| --- | --- | --- | --- |
| **Agent** | Core Architecture | An autonomous goal-directed software system that uses a language model to select actions, invoke tools, observe feedback, and iterate across multiple steps. | [What is an AI Agent](${BASE_URL}/foundations/what-is-an-ai-agent/) |
| **Agent Loop** | Core Architecture | The cyclic 5-step control sequence: Context Assembly, Model Reasoning, Tool Dispatch, Observation Feedback, and Termination Check. | [The Agent Loop Explained](${BASE_URL}/foundations/the-agent-loop-explained/) |
| **Control Flow** | System Modeling | Messages and signals that instruct software what action to take next, distinguished from passive data flow. | [Workflows vs Agents](${BASE_URL}/foundations/workflows-versus-autonomous-agents/) |
| **Data Flow** | System Modeling | Information passed between components as content or payload without carrying execution authority. | [What is an AI Agent](${BASE_URL}/foundations/what-is-an-ai-agent/) |
| **Delegation** | Security & Auth | The process where a principal authorizes an actor (agent) to execute actions on their behalf within downscoped limits. | [Identity, Authority & Least Privilege](${BASE_URL}/foundations/identity-authority-and-least-privilege/) |
| **Environment** | Core Architecture | The external runtime context (APIs, databases, filesystems) with which an agent interacts via tools and observations. | [Goals, Policies & Autonomy](${BASE_URL}/foundations/goals-policies-environments-and-autonomy/) |
| **Least Privilege** | Security & Auth | Granting an agent only the exact permissions, tool endpoints, and data scopes necessary to complete its immediate task. | [Identity, Authority & Least Privilege](${BASE_URL}/foundations/identity-authority-and-least-privilege/) |
| **Policy Guardrails** | Safety & Security | Explicit deterministic rules and filters that constrain agent behavior, tool parameters, and allowable actions. | [Goals, Policies & Autonomy](${BASE_URL}/foundations/goals-policies-environments-and-autonomy/) |
| **Principal** | Security & Auth | The human user or parent system owning data and holding initial authority for an operation. | [Identity, Authority & Least Privilege](${BASE_URL}/foundations/identity-authority-and-least-privilege/) |
| **Run Lifecycle** | Operations | The deterministic execution state machine of an agent run (Created, Running, Paused, Succeeded, Failed, Aborted). | [Run Lifecycle & Termination](${BASE_URL}/foundations/run-lifecycle-and-termination/) |
| **Termination Gate** | Safety & Security | The deterministic exit conditions (success check, step limits, budget exhaustion) that prevent infinite loops. | [Run Lifecycle & Termination](${BASE_URL}/foundations/run-lifecycle-and-termination/) |
| **Trust Boundary** | Security & Auth | A conceptual perimeter where data or control passes between components with differing levels of trust and authority. | [Securing AI Agents](${BASE_URL}/security/securing-ai-agents/) |
| **Workflow** | Core Architecture | A deterministic, fixed sequence of execution steps where branching logic is hardcoded rather than model-directed. | [Workflows vs Agents](${BASE_URL}/foundations/workflows-versus-autonomous-agents/) |
`,
  'utf8'
);

fs.writeFileSync(
  path.join(refDir, 'agent-endpoints.md'),
  `---
title: "Machine & AI Agent Endpoints"
description: "Clean Markdown, structured JSON indexes, and LLM context files for autonomous ingestion and RAG."
---

This handbook provides first-class machine-readable endpoints designed for direct ingestion by language models, AI coding agents, and RAG pipelines.

## Available Machine Endpoints

### 1. \`llms.txt\` (Standard LLM Context Map)
A concise Markdown summary of the entire guide, core architectural principles, and curated chapter links formatted for language model context windows.
- **Direct Link:** [\`${SITE_ORIGIN}${BASE_URL}/llms.txt\`](${BASE_URL}/llms.txt)

### 2. \`guide-index.json\` (Structured Guide Index)
A complete structured JSON index of all published units, containing unit IDs, learning objectives, prerequisites, source citations, claims supported, and canonical links.
- **Direct Link:** [\`${SITE_ORIGIN}${BASE_URL}/guide-index.json\`](${BASE_URL}/guide-index.json)

### 3. Clean Markdown Alternates
Every published chapter is accompanied by a pure Markdown alternate stripped of site-specific layout markup:
- **Format:** \`${BASE_URL}/markdown/<section>/<slug>.md\`
- **Example:** [\`what-is-an-ai-agent.md\`](${BASE_URL}/markdown/foundations/what-is-an-ai-agent.md)
`,
  'utf8'
);

// 9. Generate Clean Editorial Homepage (index.mdx)
console.log('🏠 Generating modern, clean editorial landing page...');

fs.writeFileSync(
  path.join(DOCS_DIR, 'index.mdx'),
  `---
title: "From LLMs to Secure Agents"
description: "A visual, source-grounded engineering guide to understanding complete agentic AI architectures and learning how to threat-model, sandbox, and secure them."
template: splash
tableOfContents: false
prev: false
next: false
---

<div class="hero-section not-content">
  <div class="hero-glow-bg"></div>
  <div class="hero-pill-badge">
    <span>🛡️ Autonomous AI Systems & Security Handbook</span>
  </div>
  <h1 class="hero-title">
    From LLMs to <span class="gradient-text">Secure Agents</span>
  </h1>
  <p class="hero-subtitle">
    The comprehensive visual, source-grounded engineering guide to understanding complete agentic architectures and learning how to threat-model, sandbox, and secure them.
  </p>
  <div class="hero-cta-group">
    <a href="${BASE_URL}/foundations/what-is-an-ai-agent/" class="btn-hero-primary">
      🚀 Start Reading Chapter 1 →
    </a>
    <a href="https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents" target="_blank" rel="noopener noreferrer" class="btn-hero-github">
      <span class="star-gold">★</span> Star on GitHub
    </a>
    <a href="${BASE_URL}/security/securing-ai-agents/" class="btn-hero-secondary">
      🛡️ Explore Security Defenses
    </a>
  </div>
</div>

<div class="blueprint-window not-content">
  <div class="blueprint-header">
    <div class="blueprint-dots">
      <span class="dot dot-red"></span>
      <span class="dot dot-yellow"></span>
      <span class="dot dot-green"></span>
    </div>
    <div class="blueprint-title">system-architecture-overview.blueprint</div>
    <div style="width: 3rem;"></div>
  </div>
  <div class="blueprint-body">
    <img src="${BASE_URL}/assets/images/repo-images/project-purpose.png" alt="Core Purpose: From LLM Call to Agentic Loop to Secured System" />
  </div>
  <div class="blueprint-caption">
    <strong>The Core Engineering Transformation:</strong> Transitioning from isolated, stateless LLM calls to dynamic goal-directed agent loops, protected by zero-trust boundaries and least-privilege execution sandboxes.
  </div>
</div>

<div class="transformation-grid not-content">
  <div class="transformation-card">
    <div>
      <div class="transformation-icon-badge badge-icon-1">🔄</div>
      <div class="transformation-step step-1">Stage 01 • Architecture</div>
      <h3>The Autonomous Loop</h3>
      <p>Master how agents make runtime decisions: cyclic reasoning loops, context construction, tool dispatching, and deterministic run lifecycles.</p>
    </div>
    <a href="${BASE_URL}/foundations/what-is-an-ai-agent/" class="home-card-link">Explore Foundations (6 Units) →</a>
  </div>

  <div class="transformation-card">
    <div>
      <div class="transformation-icon-badge badge-icon-2">🧩</div>
      <div class="transformation-step step-2">Stage 02 • Subsystems</div>
      <h3>Tools, Memory & State</h3>
      <p>Deep-dive into function calling schemas, persistent memory stores, agentic RAG, state graphs, and Model Context Protocol (MCP).</p>
    </div>
    <a href="${BASE_URL}/building-blocks/components-overview/" class="home-card-link">View Building Blocks →</a>
  </div>

  <div class="transformation-card">
    <div>
      <div class="transformation-icon-badge badge-icon-3">🛡️</div>
      <div class="transformation-step step-3">Stage 03 • Security</div>
      <h3>Threat Models & Sandboxes</h3>
      <p>Analyze indirect prompt injection, confused deputy attacks, excessive agency, ephemeral execution sandboxes, and verification gates.</p>
    </div>
    <a href="${BASE_URL}/security/securing-ai-agents/" class="home-card-link">Explore Security Defenses →</a>
  </div>
</div>

<div class="foundations-showcase-section not-content">
  <div class="section-header-row">
    <div class="section-badge">Core Curriculum</div>
    <h2 class="section-main-title">01 Agent Foundations: Read Now</h2>
  </div>

  <div class="foundations-chapter-grid">
    <a href="${BASE_URL}/foundations/what-is-an-ai-agent/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 01</span>
        <div class="chapter-card-title">What is an AI Agent</div>
        <div class="chapter-card-desc">Defines autonomous model-directed control loops versus static prompts and deterministic code pipelines.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>

    <a href="${BASE_URL}/foundations/the-agent-loop-explained/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 02</span>
        <div class="chapter-card-title">The Agent Loop Explained</div>
        <div class="chapter-card-desc">Detailed breakdown of the 5-step cyclic loop: Context, Reasoning, Tool Dispatch, Observation, and Termination.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>

    <a href="${BASE_URL}/foundations/workflows-versus-autonomous-agents/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 03</span>
        <div class="chapter-card-title">Workflows vs Autonomous Agents</div>
        <div class="chapter-card-desc">Trade-offs and architectural spectrum between deterministic pipelines, router graphs, and dynamic agents.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>

    <a href="${BASE_URL}/foundations/goals-policies-environments-and-autonomy/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 04</span>
        <div class="chapter-card-title">Goals, Policies & Autonomy</div>
        <div class="chapter-card-desc">Formal autonomy spectrum, environment boundaries, and deterministic policy guardrails constraining actions.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>

    <a href="${BASE_URL}/foundations/run-lifecycle-and-termination/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 05</span>
        <div class="chapter-card-title">Run Lifecycle & Termination</div>
        <div class="chapter-card-desc">State transitions, human approval pause gates, budget bounds, and guaranteed loop termination semantics.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>

    <a href="${BASE_URL}/foundations/identity-authority-and-least-privilege/" class="chapter-showcase-card">
      <div>
        <span class="chapter-card-num">Chapter 06</span>
        <div class="chapter-card-title">Identity & Least Privilege</div>
        <div class="chapter-card-desc">Separates principal from actor identity, downscoped token exchange (RFC 8693), and least privilege enforcement.</div>
      </div>
      <div class="chapter-card-action">Read Chapter →</div>
    </a>
  </div>
</div>

<div class="start-reading-banner not-content">
  <h2>Ready to Build Secure Autonomous Agents?</h2>
  <p>Start with the foundational mechanics of reasoning loops, or jump directly into threat modeling and defensive architectures.</p>
  <div style="display: flex; justify-content: center; gap: 1.25rem; flex-wrap: wrap;">
    <a href="${BASE_URL}/foundations/what-is-an-ai-agent/" class="btn-hero-primary">
      Start Chapter 1: What is an AI Agent →
    </a>
    <a href="${BASE_URL}/overview/curriculum/" class="btn-hero-secondary">
      View Master Curriculum Roadmap
    </a>
  </div>
</div>
`,
  'utf8'
);

// 10. Generate guide-index.json
console.log('🤖 Generating machine-readable guide-index.json...');
fs.writeFileSync(
  path.join(PUBLIC_DIR, 'guide-index.json'),
  JSON.stringify(
    {
      title: 'From LLMs to Secure Agents: Engineering Guide Index',
      description: 'Machine-readable index of published units, learning objectives, source records, and canonical links.',
      version: '1.1.0',
      origin: SITE_ORIGIN,
      base_path: BASE_URL,
      last_updated: new Date().toISOString().split('T')[0],
      total_published_units: guideIndex.length,
      units: guideIndex,
    },
    null,
    2
  ),
  'utf8'
);

// 11. Generate llms.txt
console.log('📄 Generating llms.txt...');
const llmsTxtContent = `# From LLMs to Secure Agents

> A visual, source-grounded engineering guide to understanding complete agentic AI architectures and learning how to threat-model, sandbox, and secure them.

- **Site Origin:** ${SITE_ORIGIN}${BASE_URL}/
- **Structured Index:** ${SITE_ORIGIN}${BASE_URL}/guide-index.json
- **Source Repository:** https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents

## Core Architecture Progression

1. **Agent Foundations (Published)**
   - What is an AI Agent: Single-step model vs deterministic workflows vs autonomous loops.
   - The Agent Loop: 5-step cyclic sequence (Context, Reasoning, Tool Dispatch, Observation, Termination).
   - Workflows vs Agents: Design spectrum and trade-offs between static pipelines and autonomous reasoning.
   - Goals, Policies & Autonomy: Objective specification, policy guardrails, and autonomy levels.
   - Run Lifecycle & Termination: State machine transitions, pause/resume approval gates, step budgets.
   - Identity, Authority & Least Privilege: Actor-principal separation, OAuth token exchange, scoped permissions.

2. **Security & Threat Defense (Curated Hubs)**
   - [Securing AI Agents (Master Guide)](${SITE_ORIGIN}${BASE_URL}/security/securing-ai-agents/)
   - [Indirect Prompt Injection & Context Security](${SITE_ORIGIN}${BASE_URL}/security/indirect-prompt-injection-defense/)
   - [Identity, Scoped Tokens & Least Privilege](${SITE_ORIGIN}${BASE_URL}/security/identity-and-scoped-delegation/)
   - [Tools, Function Calling & Excessive Agency](${SITE_ORIGIN}${BASE_URL}/security/tools-and-excessive-agency-prevention/)
   - [Execution Environments & Sandboxing](${SITE_ORIGIN}${BASE_URL}/security/execution-environments-and-sandboxing/)
   - [Model Context Protocol (MCP) Security](${SITE_ORIGIN}${BASE_URL}/security/model-context-protocol-security/)

3. **Curriculum Roadmap & Subsystems**
   - [Master Curriculum Architecture](${SITE_ORIGIN}${BASE_URL}/overview/curriculum/)
   - [Agent Architectures Overview](${SITE_ORIGIN}${BASE_URL}/architecture/selection-and-tradeoffs/)
   - [Building Blocks Overview](${SITE_ORIGIN}${BASE_URL}/building-blocks/components-overview/)
   - [Evidence & Verification Methodology](${SITE_ORIGIN}${BASE_URL}/overview/methodology/)
   - [System Glossary & Terminology](${SITE_ORIGIN}${BASE_URL}/reference/glossary/)
   - [Machine & Agent Endpoints](${SITE_ORIGIN}${BASE_URL}/reference/agent-endpoints/)

## Published Canonical Chapters

${guideIndex
  .map(
    (u) => `### [${u.unit_id}: ${u.title}](${u.html_url})
- **Summary:** ${u.summary}
- **Clean Markdown URL:** ${u.markdown_url}
- **Key Objectives:**
${u.learning_objectives.map((o) => `  * ${o}`).join('\n')}
- **Verified Sources:** ${u.source_records.map((s) => `[${s.title}](${s.canonical_url})`).join(', ')}
`
  )
  .join('\n')}
`;

fs.writeFileSync(path.join(PUBLIC_DIR, 'llms.txt'), llmsTxtContent, 'utf8');

console.log('🎉 Visual build pipeline preparation completed successfully!');
