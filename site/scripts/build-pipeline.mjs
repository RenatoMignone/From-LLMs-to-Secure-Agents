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
const PUBLIC_MARKDOWN_DIR = path.join(PUBLIC_DIR, 'markdown');

console.log('🚀 Running From-LLMs-to-Secure-Agents build pipeline...');

// 1. Clean output directories
fs.rmSync(DOCS_DIR, { recursive: true, force: true });
fs.mkdirSync(DOCS_DIR, { recursive: true });

const SRC_ASSETS_DIR = path.join(SITE_ROOT, 'src', 'assets', 'images');

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
      if (entry.name !== 'source') { // Don't need internal prompt sources in public dist
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
          const relPath = path.relative(path.join(REPO_ROOT, 'sources'), fullPath);
          sourceIndex.set(doc.id, doc);
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

// 4. Scan knowledge chapters
console.log('📖 Scanning and processing canonical knowledge base...');

function parseChapterFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  // Match either <!-- --- ... --- --> or --- ... ---
  const match = content.match(/^(?:<!--\s*)?---\n([\s\S]*?)\n---\s*(?:-->)?\n?([\s\S]*)$/);
  if (!match) {
    return null;
  }
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

const chapters = [];
const knowledgeDir = path.join(REPO_ROOT, 'knowledge');

function scanKnowledge(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanKnowledge(fullPath);
    } else if (
      entry.isFile() &&
      entry.name.endsWith('.md') &&
      entry.name !== 'AGENTS.md' &&
      entry.name !== 'chapter-plan.md'
    ) {
      const parsed = parseChapterFile(fullPath);
      if (parsed && parsed.frontmatter.status === 'complete') {
        const relDir = path.relative(knowledgeDir, dir);
        const slug = entry.name.replace(/\.md$/, '');
        chapters.push({
          relDir,
          slug,
          filename: entry.name,
          fullPath,
          frontmatter: parsed.frontmatter,
          body: parsed.body,
        });
      }
    }
  }
}

scanKnowledge(knowledgeDir);

// Sort chapters in strict dependency order by unit_id
chapters.sort((a, b) => {
  const idA = a.frontmatter.unit_id || '';
  const idB = b.frontmatter.unit_id || '';
  return idA.localeCompare(idB);
});

console.log(`✓ Found ${chapters.length} completed canonical chapters.`);

// Link rewriting helper
function rewriteLinks(markdown, currentRelDir) {
  // Rewrite relative images: ../../assets/images/... or assets/images/... -> /From-LLMs-to-Secure-Agents/assets/images/...
  let text = markdown.replace(
    /!\[(.*?)\]\((\.\.\/)*assets\/images\/(.*?)\)/g,
    `![$1](${BASE_URL}/assets/images/$3)`
  );

  // Rewrite chapter-plan.md links to section overview pages
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?00-prerequisites\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/00-prerequisites/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?01-agent-foundations\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/01-agent-foundations/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?02-agent-architectures\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/02-agent-architectures/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?03-building-blocks\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/03-building-blocks/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?04-frameworks-and-protocols\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/04-frameworks-and-protocols/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?05-end-to-end-workflows\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/05-end-to-end-workflows/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?06-threat-model\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/06-threat-model/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?07-security-by-component-and-workflow-stage\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/07-security-by-component-and-workflow-stage/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?08-secure-reference-architectures\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/08-secure-reference-architectures/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?09-security-testing-evaluation-and-assurance\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/09-security-testing-evaluation-and-assurance/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?10-open-research-questions\/chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/10-open-research-questions/)`
  );
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)?chapter-plan\.md\)/g,
    `[$1](${BASE_URL}/overview/curriculum/)`
  );

  // Rewrite same-directory .md links (e.g. 01-what-is-an-agent.md -> /From-LLMs-to-Secure-Agents/01-agent-foundations/01-what-is-an-agent/)
  text = text.replace(/\[(.*?)\]\((\.\/)?([0-9]{2}-[a-z0-9-]+)\.md\)/g, (match, p1, p2, p3) => {
    return `[${p1}](${BASE_URL}/${currentRelDir}/${p3}/)`;
  });

  return text;
}

// 5. Generate Chapter Pages
const guideIndex = [];

for (let i = 0; i < chapters.length; i++) {
  const ch = chapters[i];
  const fm = ch.frontmatter;
  const prevCh = i > 0 ? chapters[i - 1] : null;
  const nextCh = i < chapters.length - 1 ? chapters[i + 1] : null;

  const outDir = path.join(DOCS_DIR, ch.relDir);
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `${ch.slug}.md`);

  const rawMarkdownDir = path.join(PUBLIC_MARKDOWN_DIR, ch.relDir);
  fs.mkdirSync(rawMarkdownDir, { recursive: true });
  const rawMarkdownPath = path.join(rawMarkdownDir, `${ch.slug}.md`);

  const canonicalUrl = `${SITE_ORIGIN}${BASE_URL}/${ch.relDir}/${ch.slug}/`;
  const markdownUrl = `${SITE_ORIGIN}${BASE_URL}/markdown/${ch.relDir}/${ch.slug}.md`;

  // Build Sources panel
  const sourcesData = [];
  if (fm.source_records && Array.isArray(fm.source_records)) {
    for (const srcId of fm.source_records) {
      const srcDoc = sourceIndex.get(srcId) || sourceIndex.get(`${ch.relDir}/${srcId}.yml`);
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

  // Prepare JSON-LD
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
    educationalLevel: fm.learning_path === 'main' ? 'Core Curriculum' : 'Advanced Deep Dive',
  };

  // Build Starlight Frontmatter
  const starlightFm = {
    title: fm.title,
    description: fm.summary,
    editUrl: `https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents/blob/main/knowledge/${ch.relDir}/${ch.filename}`,
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

  // Build Custom Header Bar
  const passLabel = fm.pass === 'architecture' ? 'Pass 1: Architecture' : 'Pass 2: Security';
  const pathLabel = fm.learning_path === 'main' ? 'Main Path' : 'Deep Dive';
  const statusLabel = fm.status === 'complete' ? 'Source Grounded' : fm.status;

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
  <strong>Chapter Focus:</strong> ${fm.summary}
</div>
`;

  // Prerequisites & Objectives Cards
  const hasPrereqs = fm.prerequisites && fm.prerequisites.length > 0;
  const hasObjectives = fm.learning_objectives && fm.learning_objectives.length > 0;

  if (hasPrereqs || hasObjectives) {
    pageContent += `\n<div class="guide-callout-grid not-content">\n`;
    if (hasPrereqs) {
      pageContent += `  <div class="callout-card callout-prereqs">
    <h3>📌 Prerequisites</h3>
    <ul>
${fm.prerequisites.map((p) => `      <li>${p}</li>`).join('\n')}
    </ul>
  </div>\n`;
    }
    if (hasObjectives) {
      pageContent += `  <div class="callout-card callout-objectives">
    <h3>🎯 Learning Objectives</h3>
    <ul>
${fm.learning_objectives.map((o) => `      <li>${o}</li>`).join('\n')}
    </ul>
  </div>\n`;
    }
    pageContent += `</div>\n\n`;
  }

  // Remove top-level # Heading from body if it matches title to prevent double titles
  let cleanBody = ch.body.trim();
  cleanBody = cleanBody.replace(/^#\s+[^\n]+\n+/, '');

  // Rewrite links and images in body
  cleanBody = rewriteLinks(cleanBody, ch.relDir);

  pageContent += cleanBody;

  // Build Sources & Evidence accordion
  if (sourcesData.length > 0) {
    pageContent += `\n\n<details class="evidence-panel not-content">
  <summary>
    <span>🔍 Verified Evidence & Source Citations (${sourcesData.length} records)</span>
    <span style="font-size: 0.8rem; font-weight: normal;">Click to expand</span>
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
        <strong>Organization/Authors:</strong> ${s.authors_or_organization} &bull; 
        <strong>Date:</strong> ${s.date} ${s.version ? `(v${s.version})` : ''} &bull; 
        <strong>Verified:</strong> ${s.last_verified}
      </div>
      ${
        s.claims_supported && s.claims_supported.length > 0
          ? `<div><strong>Exact Claims Supported:</strong>
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
    pageContent += `  <a href="${BASE_URL}/${prevCh.relDir}/${prevCh.slug}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Previous Unit (${prevCh.frontmatter.unit_id})</div>
    <div class="nav-title">${prevCh.frontmatter.title}</div>
  </a>\n`;
  } else {
    pageContent += `  <a href="${BASE_URL}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Guide Start</div>
    <div class="nav-title">Handbook Introduction</div>
  </a>\n`;
  }

  if (nextCh) {
    pageContent += `  <a href="${BASE_URL}/${nextCh.relDir}/${nextCh.slug}/" class="nav-card nav-card-next">
    <div class="nav-label">Next Unit (${nextCh.frontmatter.unit_id}) →</div>
    <div class="nav-title">${nextCh.frontmatter.title}</div>
  </a>\n`;
  } else {
    pageContent += `  <a href="${BASE_URL}/02-agent-architectures/" class="nav-card nav-card-next">
    <div class="nav-label">Next Section (Roadmap) →</div>
    <div class="nav-title">02 Agent Architectures</div>
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
> **Unit ID:** ${fm.unit_id} | **Pass:** ${fm.pass} | **Status:** ${fm.status}

${ch.body.trim()}

## Source Records
${sourcesData.map((s) => `- [${s.title}](${s.canonical_url}) (${s.authors_or_organization}, ${s.date})`).join('\n')}
`;
  fs.writeFileSync(rawMarkdownPath, cleanMarkdown, 'utf8');
}

console.log('✓ Generated all chapter documents and markdown alternates.');

// 6. Generate Section Overview Pages
console.log('📑 Generating section overview pages...');

fs.mkdirSync(path.join(DOCS_DIR, '00-prerequisites'), { recursive: true });
fs.writeFileSync(
  path.join(DOCS_DIR, '00-prerequisites', 'index.md'),
  `---
title: "00 Prerequisites: Orientation & System Notation"
description: "Core vocabulary, system boundaries, and request-response notation for tracing agentic systems safely."
---

## Purpose

Before analyzing how an agent makes autonomous decisions, we establish exact names for software parts, messages, stores, processes, trust boundaries, and authority delegation.

This foundation ensures that later discussions of model reasoning and tool execution rest on rigorous system engineering concepts rather than ambiguous buzzwords.

## Completed Units in this Section

| Unit | Title | Summary |
| --- | --- | --- |
| **P1-00-01** | [Reader contract and system map](${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/) | Establishes the system vocabulary and diagram notation used to trace an agent safely. |
| **P1-00-02** | [Data, control, and trust boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/) | Distinguishes data from control flow and defines trust boundaries across components. |
| **P1-00-03** | [Requests, events, state, and side effects](${BASE_URL}/00-prerequisites/03-requests-events-state-and-side-effects/) | Traces execution lifecycles, durable state changes, and external system side effects. |
| **P1-00-04** | [Identity, authority, and least privilege primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/) | Separates principal from actor identity, scoped tokens, and least privilege enforcement. |

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Overview</div>
    <div class="nav-title">Guide Introduction</div>
  </a>
  <a href="${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/" class="nav-card nav-card-next">
    <div class="nav-label">Start Prerequisites →</div>
    <div class="nav-title">01 Reader contract and system map</div>
  </a>
</div>
`,
  'utf8'
);

fs.mkdirSync(path.join(DOCS_DIR, '01-agent-foundations'), { recursive: true });
fs.writeFileSync(
  path.join(DOCS_DIR, '01-agent-foundations', 'index.md'),
  `---
title: "01 Agent Foundations: What Makes an Agent"
description: "Core mechanics of autonomous agent loops, workflows vs agents, autonomy spectrum, and run lifecycles."
---

## Purpose

This section introduces the structural anatomy of an AI agent. It formally distinguishes single-step model calls, deterministic static workflows, and dynamic autonomous agent loops.

It provides the mental and architectural models for context assembly, tool execution, feedback observation, policy constraints, and termination guarantees.

## Completed Units in this Section

| Unit | Title | Summary |
| --- | --- | --- |
| **P1-01-01** | [What is an agent](${BASE_URL}/01-agent-foundations/01-what-is-an-agent/) | Defines an agent as an autonomous goal-directed software system with runtime tool discretion. |
| **P1-01-02** | [The agent loop](${BASE_URL}/01-agent-foundations/02-the-agent-loop/) | Analyzes the 5-step cyclic loop: Context, Reasoning, Tool Dispatch, Observation, and Termination. |
| **P1-01-03** | [Workflows versus agents](${BASE_URL}/01-agent-foundations/03-workflows-versus-agents/) | Maps the design spectrum from deterministic pipelines to autonomous reasoning loops. |
| **P1-01-04** | [Goals, policies, environments, and autonomy](${BASE_URL}/01-agent-foundations/04-goals-policies-environments-and-autonomy/) | Explores objective specification, protective guardrail policies, and autonomy levels. |
| **P1-01-05** | [Run lifecycle and termination](${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/) | Details state machine lifecycles, pause/resume interrupts, step limits, and termination. |

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/" class="nav-card nav-card-prev">
    <div class="nav-label">← Previous Section</div>
    <div class="nav-title">Prerequisites: Identity & Authority</div>
  </a>
  <a href="${BASE_URL}/01-agent-foundations/01-what-is-an-agent/" class="nav-card nav-card-next">
    <div class="nav-label">Start Foundations →</div>
    <div class="nav-title">01 What is an agent</div>
  </a>
</div>
`,
  'utf8'
);

// Roadmap Sections
const roadmapSections = [
  {
    dir: '02-agent-architectures',
    title: '02 Agent Architectures',
    badge: 'Pass 1 Roadmap Queue',
    desc: 'Architectural design patterns: single-agent, plan-and-execute, evaluator-optimizer, state machine graphs, supervisors, and multi-agent topologies.',
    units: [
      'P1-02-01 Architecture selection criteria',
      'P1-02-02 Single-agent and reactive loops',
      'P1-02-03 Sequential, routing, and parallel workflows',
      'P1-02-04 Plan and execute',
      'P1-02-05 Evaluator-optimizer and reflection',
      'P1-02-06 State machines and event-driven graphs',
      'P1-02-07 Supervisors, handoffs, and agent-as-tool',
      'P1-02-08 Architecture trade-offs',
    ],
  },
  {
    dir: '03-building-blocks',
    title: '03 Building Blocks',
    badge: 'Pass 1 Roadmap Queue',
    desc: 'Deep dives into core components: models & routing, context construction, planning & reasoning, state & lifecycle, memory, retrieval & RAG, tools & function calling, and execution sandboxes.',
    units: [
      'P1-03-01 Models and routing',
      'P1-03-02 Context construction & budgets',
      'P1-03-03 Planning and reasoning',
      'P1-03-04 State and lifecycle management',
      'P1-03-05 Working & persistent memory',
      'P1-03-06 Retrieval and RAG',
      'P1-03-07 Tools and function calling',
      'P1-03-08 Identity, authorization, and secrets',
      'P1-03-09 Execution environments & sandboxes',
      'P1-03-10 Human-in-the-loop controls',
      'P1-03-11 Observability and tracing',
      'P1-03-12 Evaluation and benchmarks',
    ],
  },
  {
    dir: '04-frameworks-and-protocols',
    title: '04 Frameworks & Protocols',
    badge: 'Pass 1 Roadmap Queue',
    desc: 'Production orchestration frameworks, Model Context Protocol (MCP), agent-to-agent protocols, and standard interaction patterns.',
    units: [
      'P1-04-01 Orchestration frameworks',
      'P1-04-02 Model Context Protocol (MCP)',
      'P1-04-03 Agent-to-agent communication protocols',
      'P1-04-04 Agent-user interaction protocols',
    ],
  },
  {
    dir: '05-end-to-end-workflows',
    title: '05 End-to-End Workflows',
    badge: 'Pass 1 Roadmap Queue',
    desc: 'Complete production workflows from user input to verified external action, synthesizing all Pass 1 architectural blocks.',
    units: [
      'P1-05-01 Reference enterprise workflow implementation',
    ],
  },
  {
    dir: '06-threat-model',
    title: '06 Threat Model for Agentic Systems',
    badge: 'Pass 2 Roadmap Queue',
    desc: 'Comprehensive threat modeling: assets, actors, trust boundaries, attacker capabilities, and entry surfaces across the agent loop.',
    units: [
      'P2-06-01 Threat model foundations and assets',
      'P2-06-02 Attacker profiles and access vectors',
      'P2-06-03 Trust boundary crossings and protocol threats',
      'P2-06-04 Indirect injection and payload delivery',
      'P2-06-05 Agent threat matrix and taxonomy',
    ],
  },
  {
    dir: '07-security-by-component-and-workflow-stage',
    title: '07 Security by Component & Workflow Stage',
    badge: 'Pass 2 Roadmap Queue',
    desc: 'Component-by-component security analysis: context isolation, memory poisoning, excessive agency, confused deputy, and sandbox escapes.',
    units: [
      'P2-07-01 Instructions, context, and model security',
      'P2-07-02 Retrieval, memory, and data store security',
      'P2-07-03 Tools, identity, credentials, and excessive agency',
      'P2-07-04 Execution environments, sandboxing, and supply chain',
      'P2-07-05 Human interfaces and observability security',
      'P2-07-06 Multi-agent coordination and protocol attacks',
      'P2-07-07 End-to-end attack paths & exploitation chains',
      'P2-07-08 Governance, policy guardrails, and secure lifecycle',
    ],
  },
  {
    dir: '08-secure-reference-architectures',
    title: '08 Secure Reference Architectures',
    badge: 'Pass 2 Roadmap Queue',
    desc: 'Hardened, battle-tested blueprints for enterprise agents, customer support agents, coding assistants, and multi-agent swarms.',
    units: [
      'P2-08-01 Read-only research and analytics agent pattern',
      'P2-08-02 Scoped-action transactional agent pattern',
      'P2-08-03 Dual-agent supervisor and worker pattern',
      'P2-08-04 Zero-trust MCP gateway architecture',
      'P2-08-05 High-assurance air-gapped agent pattern',
    ],
  },
  {
    dir: '09-security-testing-evaluation-and-assurance',
    title: '09 Security Testing, Evaluation & Assurance',
    badge: 'Pass 2 Roadmap Queue',
    desc: 'Automated red teaming, jailbreak benchmarks, injection fuzzing, invariant checking, and continuous security assurance.',
    units: [
      'P2-09-01 Automated security testing suites',
      'P2-09-02 Injection benchmarks and fuzz testing',
      'P2-09-03 Tool parameter verification and boundary testing',
      'P2-09-04 Red teaming methodologies for agentic workflows',
      'P2-09-05 Continuous security assurance in CI/CD',
    ],
  },
  {
    dir: '10-open-research-questions',
    title: '10 Open Research Questions',
    badge: 'Research Frontier',
    desc: 'Unsolved problems in agent security: formal verification of reasoning loops, unforgeable data provenance, and robust defenses against indirect injection.',
    units: [
      'P2-10-01 Frontiers in agent safety and security',
    ],
  },
];

for (const sec of roadmapSections) {
  const secDir = path.join(DOCS_DIR, sec.dir);
  fs.mkdirSync(secDir, { recursive: true });
  fs.writeFileSync(
    path.join(secDir, 'index.md'),
    `---
title: "${sec.title}"
description: "${sec.desc}"
---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-path">${sec.badge}</span>
  <span class="meta-badge badge-status">In Queue (Dependency Ordered)</span>
</div>

## Architectural Overview

${sec.desc}

> **Note on Roadmap Progression:**  
> The guide is authored sequentially under strict dependency order. Units in this section will be published as they complete research, source-grounding, peer review, and verification.

## Scheduled Units in this Section

${sec.units.map((u) => `- \`${u}\``).join('\n')}

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/01-agent-foundations/" class="nav-card nav-card-prev">
    <div class="nav-label">← Previous Completed Section</div>
    <div class="nav-title">01 Agent Foundations</div>
  </a>
  <a href="${BASE_URL}/overview/curriculum/" class="nav-card nav-card-next">
    <div class="nav-label">View Master Roadmap →</div>
    <div class="nav-title">Curriculum Architecture</div>
  </a>
</div>
`,
    'utf8'
  );
}

// 7. Generate Overview Pages
const overviewDir = path.join(DOCS_DIR, 'overview');
fs.mkdirSync(overviewDir, { recursive: true });

fs.writeFileSync(
  path.join(overviewDir, 'curriculum.md'),
  `---
title: "Curriculum & Two-Pass Architecture"
description: "Why this guide teaches complete system architecture before detailed security analysis."
---

## The Two-Pass Philosophy

Agent security cannot be understood effectively through disconnected vulnerability lists. An engineer cannot defend a system whose moving parts, trust boundaries, and execution loops they do not fully understand.

This guide is structured around two distinct, sequential learning passes:

\`\`\`
Pass 1: UNDERSTAND THE SYSTEM
├── 00 Prerequisites (Vocabulary, Boundaries, Events, Identity)
├── 01 Agent Foundations (What is an Agent, Loop, Autonomy, Lifecycle)
├── 02 Agent Architectures (Single Loop, Plan & Execute, Reflection, Graphs)
├── 03 Building Blocks (Context, Memory, Retrieval, Tools, Sandboxes)
├── 04 Frameworks & Protocols (MCP, Agent Protocols, UI Patterns)
└── 05 End-to-End Workflows (Reference Enterprise Implementation)
\`\`\`

\`\`\`
Pass 2: SECURE THE SYSTEM
├── 06 Threat Model (Assets, Adversaries, Entry Points, Attack Vectors)
├── 07 Security by Component (Injection, Poisoning, Excessive Agency, Sandbox Escape)
├── 08 Secure Reference Architectures (Hardened Blueprints, Gateways)
├── 09 Testing & Assurance (Red Teaming, Fuzzing, Invariant Verification)
└── 10 Open Research Questions (Formal Verification, Provenance)
\`\`\`

## Main Path vs. Deep Dives

To keep learning efficient without losing technical depth, the guide separates topics into:

1. **Main Path**: The minimal complete path required to understand and secure an agentic system. Every reader should follow this sequential path.
2. **Deep Dives**: Specialized technical branches (such as complex protocol specifications, vendor-specific frameworks, or niche mathematical models) that are collapsed by default and can be explored as needed without breaking downstream prerequisites.

## Dependency Invariant

Units form one strict dependency chain. Every unit depends only on previously taught concepts. No Pass 1 architecture chapter introduces detailed attack payloads, and no Pass 2 security chapter assumes mechanisms that were not taught in Pass 1.
`,
  'utf8'
);

fs.writeFileSync(
  path.join(overviewDir, 'methodology.md'),
  `---
title: "Evidence & Autonomous Verification Methodology"
description: "How this guide ensures source-grounded accuracy, verifiable claims, and reproducible quality."
---

## Source-Grounded Evidence Policy

Every technical claim in this guide is grounded in primary evidence:
- **Standards & Specifications**: IETF RFCs, W3C Recommendations, NIST Frameworks, ISO standards.
- **Protocol Documentation**: Model Context Protocol (MCP), OpenAPI, OAuth 2.0 specifications.
- **Peer-Reviewed Research**: Foundational papers on agent loops, reasoning architectures, and threat vectors.
- **Official Security Advisories**: CVE reports, MITRE ATLAS taxonomy, OWASP Top 10 for LLMs & Agents.

All source records are stored in machine-readable YAML files mirroring the chapter structure under \`sources/\`.

## Deterministic Verification

The entire repository is continuously verified through an automated mechanical test suite:
- **Bidirectional Citations**: Every citation in a chapter resolves to an existing source record.
- **Image Provenance**: Every visual asset is locally stored, attributed, and paired with its generation prompt or source data.
- **Dependency Order**: Reading sequence and prerequisite links are mechanically validated.
- **Prose Quality**: Strictly enforces accessible language, term definitions on first use, and absence of empty placeholders.

## Machine-Readable Projections

In addition to this static website, the knowledge base is published in agent-friendly machine-readable formats:
- [\`llms.txt\`](${BASE_URL}/llms.txt) for language model context ingestion.
- [\`guide-index.json\`](${BASE_URL}/guide-index.json) for retrieval systems and autonomous tools.
- Clean Markdown alternates available for every published chapter.
`,
  'utf8'
);

// 8. Generate Topic Hubs
const hubsDir = path.join(DOCS_DIR, 'hubs');
fs.mkdirSync(hubsDir, { recursive: true });

const hubsData = [
  {
    slug: 'securing-ai-agents',
    title: 'Securing AI Agents: The Master Guide',
    desc: 'A comprehensive entry point into threat modeling, architectural isolation, and defensive controls for autonomous agents.',
    content: `
## Why Agent Security is Fundamentally Different

Traditional software security relies on deterministic control flow: code executes explicit instructions, and input data is separated from execution logic.

In an LLM agent, **untrusted input data directly guides control flow**. When a model reads an email, web page, or database record, that data enters the reasoning loop and can influence which tools the agent decides to invoke.

## Core Defense Principles

1. **Strict Data/Control Separation**: Treat model reasoning as untrusted until verified. Do not grant autonomous execution authority over high-consequence tools without parameter validation.
   - 📖 *Foundation:* [Data, control, and trust boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/)
2. **Actor vs. Principal Identity & Scoped Delegation**: An agent must operate with scoped, temporary credentials under least privilege, never inheriting the full authority of the end user without runtime constraints.
   - 📖 *Foundation:* [Identity, authority, and least privilege primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/)
3. **Loop Constraints & Termination Guarantees**: Enforce deterministic step limits, execution budgets, and pause/resume checkpoints for human confirmation.
   - 📖 *Foundation:* [Run lifecycle and termination](${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/)

## Learning Path for Security Practitioners

- Start with [00 Prerequisites](${BASE_URL}/00-prerequisites/) to master trust boundary notation.
- Study [01 Agent Foundations](${BASE_URL}/01-agent-foundations/) to understand the cyclic reasoning loop.
- Explore the [Threat Model Roadmap](${BASE_URL}/06-threat-model/) and [Component Security](${BASE_URL}/07-security-by-component-and-workflow-stage/).
`,
  },
  {
    slug: 'prompt-injection',
    title: 'Indirect Prompt Injection & Untrusted Context',
    desc: 'Understanding how malicious instructions inside external data hijack agent reasoning loops.',
    content: `
## The Anatomy of Indirect Injection

Direct prompt injection occurs when a user tries to override system instructions. **Indirect prompt injection** occurs when an agent retrieves untrusted third-party data (e.g. an email, document, search result, or API payload) containing hidden adversarial commands.

When the agent incorporates this data into its prompt context, the model may follow the attacker's instructions instead of the original user goal.

## System-Level Countermeasures

- **Context Isolation & Source Tagging**: Structurally delimit untrusted external content from trusted system instructions.
- **Dual-Model Validation**: Use an isolated model with no tools to parse and sanitize data before passing it to the action agent.
- **Parameter Constrained Tool Dispatch**: Ensure tool invocation schemas strictly validate parameter ranges and reject destructive actions.

📖 *Deep Dive Chapters:*
- [Data, control, and trust boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/)
- [What is an agent](${BASE_URL}/01-agent-foundations/01-what-is-an-agent/)
- [The agent loop & Observation feedback](${BASE_URL}/01-agent-foundations/02-the-agent-loop/)
`,
  },
  {
    slug: 'identity-and-delegation',
    title: 'Identity, Authority & Least Privilege',
    desc: 'Securing agent authorization, OAuth token exchange, and preventing confused deputy vulnerabilities.',
    content: `
## Principal vs. Actor

When an agent executes an action on behalf of a user:
- **The Principal** is the human user or workload owning the data and initial permissions.
- **The Actor** is the agent process making the downstream API call.

If the agent uses the user's master API key directly, it possesses **excessive authority**. If the agent is tricked by malicious data, it can abuse that authority.

## Scoped Delegation & Token Exchange

Using protocols such as RFC 8693 (OAuth 2.0 Token Exchange), the application exchanges user credentials for short-lived, downscoped tokens strictly limited to the specific tools and data needed for the immediate step.

📖 *Core Reference Chapter:*
- [Identity, authority, and least privilege primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/)
`,
  },
  {
    slug: 'tools-and-excessive-agency',
    title: 'Tools, Function Calling & Excessive Agency',
    desc: 'Preventing unauthorized state changes, parameter manipulation, and unintended external side effects.',
    content: `
## The Risk of Excessive Agency

Excessive agency occurs when an agent is granted more tool capabilities, broader parameter discretion, or more autonomous authority than required for its intended function.

## Key Controls

1. **Strict JSON Schema Validation**: Reject non-conforming parameters before dispatch.
2. **Idempotency & Reversibility**: Require tools with external side effects to use idempotency keys and safe rollback hooks.
3. **Confirmation Gates (Human-in-the-Loop)**: Require explicit human approval for destructive operations (e.g. database deletion, financial transactions, email sending).

📖 *Relevant Chapters:*
- [Requests, events, state, and side effects](${BASE_URL}/00-prerequisites/03-requests-events-state-and-side-effects/)
- [Goals, policies, environments, and autonomy](${BASE_URL}/01-agent-foundations/04-goals-policies-environments-and-autonomy/)
`,
  },
  {
    slug: 'execution-and-sandboxing',
    title: 'Execution Environments & Sandboxing',
    desc: 'Isolating code execution, container runtimes, network boundaries, and ephemeral state.',
    content: `
## Isolating Code Execution

When an agent writes and executes code (Python, Bash, SQL), execution must happen inside hardened, isolated environments:
- MicroVMs (e.g. Firecracker) or gVisor container runtimes.
- Strict network egress policies (blocking access to internal metadata endpoints like 169.254.169.254).
- Ephemeral filesystem lifecycles that discard state after run termination.

📖 *Foundational Context:*
- [Reader contract and system map](${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/)
- [Run lifecycle and termination](${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/)
`,
  },
  {
    slug: 'mcp-and-protocols',
    title: 'Model Context Protocol (MCP) Security',
    desc: 'Securing client-host-server architectures, tool discovery, and cross-server communication.',
    content: `
## MCP Trust Architecture

The Model Context Protocol (MCP) standardizes how AI applications connect to external data sources and tools.

In an MCP architecture:
- The **MCP Host** coordinates LLMs and user interaction.
- The **MCP Client** manages connections to servers.
- The **MCP Server** exposes resources, prompts, and tools.

## Security Considerations

- **Server Authentication**: Ensure clients only connect to verified, authentic MCP servers.
- **Resource Boundary Enforcement**: Ensure file path access is strictly constrained to intended directory roots.
- **Prompt Injection via Tool Descriptions**: Verify that tool descriptions provided by MCP servers do not contain adversarial instructions intended to bias model routing.
`,
  },
];

for (const hub of hubsData) {
  fs.writeFileSync(
    path.join(hubsDir, `${hub.slug}.md`),
    `---
title: "${hub.title}"
description: "${hub.desc}"
---

<div class="chapter-meta-bar not-content">
  <span class="meta-badge badge-path">Topic Hub & Synthesis</span>
  <span class="meta-badge badge-status">Curated Entry Point</span>
</div>

${hub.content}

<div class="chapter-nav-grid not-content">
  <a href="${BASE_URL}/" class="nav-card nav-card-prev">
    <div class="nav-label">← Overview</div>
    <div class="nav-title">Handbook Home</div>
  </a>
  <a href="${BASE_URL}/00-prerequisites/" class="nav-card nav-card-next">
    <div class="nav-label">Begin Reading →</div>
    <div class="nav-title">00 Prerequisites</div>
  </a>
</div>
`,
    'utf8'
  );
}

// 9. Generate Reference Pages
const refDir = path.join(DOCS_DIR, 'reference');
fs.mkdirSync(refDir, { recursive: true });

fs.writeFileSync(
  path.join(refDir, 'glossary.md'),
  `---
title: "System Glossary & Terminology"
description: "Authoritative technical definitions of core agentic and security concepts introduced across the guide."
---

| Term | Category | Definition | Authoritative Chapter |
| --- | --- | --- | --- |
| **Agent** | Core Architecture | An autonomous software system that uses a language model to select actions, execute tools, observe feedback, and pursue goals across multiple steps. | [01 What is an agent](${BASE_URL}/01-agent-foundations/01-what-is-an-agent/) |
| **Agent Loop** | Core Architecture | The cyclic 5-step control sequence: Context Assembly, Model Reasoning, Tool Dispatch, Observation Feedback, and Termination Check. | [02 The agent loop](${BASE_URL}/01-agent-foundations/02-the-agent-loop/) |
| **Component** | System Modeling | A distinct named software part with a specific operational responsibility (e.g. process, store, dispatcher). | [01 Reader contract](${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/) |
| **Control Flow** | System Modeling | Messages and signals that instruct software what action to take next, distinguished from passive data. | [02 Data & control boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/) |
| **Data Flow** | System Modeling | Information passed between components as content or payload without carrying execution authority. | [02 Data & control boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/) |
| **Delegation** | Security & Auth | The process where a principal authorizes an actor (agent) to execute actions on their behalf within scoped limits. | [04 Identity & authority primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/) |
| **Environment** | Core Architecture | The external runtime context (APIs, databases, filesystems) with which an agent interacts through tools and observations. | [04 Goals, policies, environments](${BASE_URL}/01-agent-foundations/04-goals-policies-environments-and-autonomy/) |
| **Event** | System Modeling | An immutable record that something occurred at a specific point in time within the system. | [03 Requests, events, state](${BASE_URL}/00-prerequisites/03-requests-events-state-and-side-effects/) |
| **Least Privilege** | Security & Auth | Granting an agent only the exact permissions, tool endpoints, and data scopes necessary to complete its immediate task. | [04 Identity & authority primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/) |
| **Policy** | Safety & Security | Explicit deterministic rules and guardrails that constrain agent behavior, tool parameters, and allowable actions. | [04 Goals, policies, environments](${BASE_URL}/01-agent-foundations/04-goals-policies-environments-and-autonomy/) |
| **Principal** | Security & Auth | The human user or parent system owning data and holding initial authority for an operation. | [04 Identity & authority primer](${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/) |
| **Side Effect** | System Modeling | A persistent state change in an external service or environment caused by an action (e.g. database write, email sent). | [03 Requests, events, state](${BASE_URL}/00-prerequisites/03-requests-events-state-and-side-effects/) |
| **State** | System Modeling | The current condition and remembered variables of an agent or system at a specific execution step. | [03 Requests, events, state](${BASE_URL}/00-prerequisites/03-requests-events-state-and-side-effects/) |
| **Termination** | Lifecycle | The deterministic exit condition of an agent run (Success, Failure, Budget Exhausted, User Aborted). | [05 Run lifecycle & termination](${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/) |
| **Trust Boundary** | Security & Auth | A conceptual perimeter where data or control passes between components with differing levels of trust and authority. | [02 Data & control boundaries](${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/) |
| **Workflow** | Core Architecture | A deterministic, fixed sequence of execution steps where branching logic is defined in static code rather than model discretion. | [03 Workflows versus agents](${BASE_URL}/01-agent-foundations/03-workflows-versus-agents/) |
`,
  'utf8'
);

fs.writeFileSync(
  path.join(refDir, 'llm-endpoints.md'),
  `---
title: "Machine-Readable & Agent Endpoints"
description: "Accessing the complete guide as structured data, clean Markdown, and LLM context files."
---

This handbook provides first-class machine-readable endpoints designed for AI agents, retrieval-augmented generation (RAG) pipelines, and research scrapers.

## Available Endpoints

### 1. \`llms.txt\`
A concise Markdown summary of the entire guide, core architectural principles, and curated chapter links formatted for language model context windows.
- **URL:** [\`${SITE_ORIGIN}${BASE_URL}/llms.txt\`](${BASE_URL}/llms.txt)

### 2. \`guide-index.json\`
A complete structured JSON index of all published units, containing unit IDs, learning objectives, prerequisites, source citations, claims supported, and canonical links.
- **URL:** [\`${SITE_ORIGIN}${BASE_URL}/guide-index.json\`](${BASE_URL}/guide-index.json)

### 3. Clean Markdown Alternates
Every published chapter is accompanied by a pure Markdown alternate stripped of site-specific layout markup.
- **Format:** Accessible at \`${BASE_URL}/markdown/<section>/<slug>.md\`
- **Example:** [\`01-what-is-an-agent.md\`](${BASE_URL}/markdown/01-agent-foundations/01-what-is-an-agent.md)
`,
  'utf8'
);

// 10. Generate Custom Homepage index.mdx
console.log('🏠 Generating editorial homepage...');

fs.writeFileSync(
  path.join(DOCS_DIR, 'index.mdx'),
  `---
title: "From LLMs to Secure Agents"
description: "A deep, visual, source-grounded guide to understanding complete agentic AI systems and learning how to secure them."
template: splash
hero:
  title: "From LLMs to Secure Agents"
  tagline: "A deep, visual, source-grounded guide to understanding complete agentic AI systems and learning how to secure and deploy them."
  image:
    file: ../../assets/images/repo-images/banner.png
  actions:
    - text: "Start Learning (Pass 1)"
      link: /From-LLMs-to-Secure-Agents/00-prerequisites/01-reader-contract-and-system-map/
      icon: right-arrow
      variant: primary
    - text: "Explore Security Hubs"
      link: /From-LLMs-to-Secure-Agents/hubs/securing-ai-agents/
      icon: open-book
      variant: secondary
    - text: "GitHub Repository"
      link: https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents
      icon: external
      variant: minimal
---

import { Card, CardGrid } from '@astrojs/starlight/components';

## The Core Concept: A Two-Pass Mental Model

Agent security cannot be mastered from disconnected vulnerability lists. We first build a complete mental model of an autonomous agentic system, then systematically analyze threats, attack paths, and defense architectures.

<div style="text-align: center; margin: 2rem 0;">
  <img src="${BASE_URL}/assets/images/repo-images/project-purpose.png" alt="Core Purpose and Mental Model: From LLM to Agent to Secured Agent" style="max-width: 850px; width: 100%; height: auto; margin: 0 auto; display: block;" />
</div>

<CardGrid stagger>
  <Card title="Pass 1: Understand the System" icon="laptop">
    Master how complete agent systems work: loop execution, state, context assembly, persistent memory, tool calling, protocols, and workflows.
    <br /><br />
    <a href="${BASE_URL}/00-prerequisites/" class="home-card-link">Explore Pass 1 Architecture →</a>
  </Card>
  <Card title="Pass 2: Secure the System" icon="shield">
    Revisit every taught component through threat models, prompt injection, privilege escalation, sandboxing, and secure reference architectures.
    <br /><br />
    <a href="${BASE_URL}/hubs/securing-ai-agents/" class="home-card-link">Explore Pass 2 Security →</a>
  </Card>
  <Card title="Source-Grounded Evidence" icon="document">
    Every claim is anchored in primary standards (IETF, NIST), peer-reviewed research, and official framework specifications with tracked YAML records.
    <br /><br />
    <a href="${BASE_URL}/overview/methodology/" class="home-card-link">View Evidence Methodology →</a>
  </Card>
  <Card title="AI Agent Friendly" icon="setting">
    Deterministic machine-readable endpoints including \`llms.txt\`, \`guide-index.json\`, and clean Markdown alternates for LLM context ingestion.
    <br /><br />
    <a href="${BASE_URL}/reference/llm-endpoints/" class="home-card-link">Access Agent Endpoints →</a>
  </Card>
</CardGrid>

## Published Canonical Chapters

<div class="home-section-grid not-content">
  <div class="home-card">
    <div>
      <span class="meta-badge badge-pass">00 Prerequisites</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/">Reader Contract & System Map</a></h3>
      <p>Establishes foundational vocabulary: components, processes, stores, external services, data flow, and control flow.</p>
    </div>
    <a href="${BASE_URL}/00-prerequisites/01-reader-contract-and-system-map/" class="home-card-link">Read Chapter (P1-00-01) →</a>
  </div>
  <div class="home-card">
    <div>
      <span class="meta-badge badge-pass">00 Prerequisites</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/">Data, Control & Trust Boundaries</a></h3>
      <p>Differentiates passive data from actionable control, and defines trust perimeters across software components.</p>
    </div>
    <a href="${BASE_URL}/00-prerequisites/02-data-control-and-trust-boundaries/" class="home-card-link">Read Chapter (P1-00-02) →</a>
  </div>
  <div class="home-card">
    <div>
      <span class="meta-badge badge-pass">00 Prerequisites</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/">Identity, Authority & Least Privilege</a></h3>
      <p>Separates principal from actor identity, downscoped token exchange, and least privilege enforcement.</p>
    </div>
    <a href="${BASE_URL}/00-prerequisites/04-identity-authority-and-least-privilege-primer/" class="home-card-link">Read Chapter (P1-00-04) →</a>
  </div>
  <div class="home-card">
    <div>
      <span class="meta-badge badge-unit">01 Foundations</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/01-agent-foundations/01-what-is-an-agent/">What is an Agent</a></h3>
      <p>Defines autonomous model-directed control loops versus static prompts and deterministic code pipelines.</p>
    </div>
    <a href="${BASE_URL}/01-agent-foundations/01-what-is-an-agent/" class="home-card-link">Read Chapter (P1-01-01) →</a>
  </div>
  <div class="home-card">
    <div>
      <span class="meta-badge badge-unit">01 Foundations</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/01-agent-foundations/02-the-agent-loop/">The Agent Loop</a></h3>
      <p>Detailed breakdown of the 5-step cyclic loop: Context, Reasoning, Tool Dispatch, Observation, and Termination.</p>
    </div>
    <a href="${BASE_URL}/01-agent-foundations/02-the-agent-loop/" class="home-card-link">Read Chapter (P1-01-02) →</a>
  </div>
  <div class="home-card">
    <div>
      <span class="meta-badge badge-unit">01 Foundations</span>
      <h3 style="margin-top: 0.5rem;"><a href="${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/">Run Lifecycle & Termination</a></h3>
      <p>State transitions, pause/resume approval gates, budget limits, and deterministic termination guarantees.</p>
    </div>
    <a href="${BASE_URL}/01-agent-foundations/05-run-lifecycle-and-termination/" class="home-card-link">Read Chapter (P1-01-05) →</a>
  </div>
</div>

## Curated Security Hubs

<CardGrid>
  <Card title="Indirect Prompt Injection" icon="warning">
    How untrusted third-party data hijacks agent reasoning loops and defenses to isolate context.
    <br /><br />
    <a href="${BASE_URL}/hubs/prompt-injection/" class="home-card-link">Explore Topic Guide →</a>
  </Card>
  <Card title="Identity & Token Delegation" icon="key">
    Preventing confused deputy vulnerabilities with downscoped tokens and OAuth exchange.
    <br /><br />
    <a href="${BASE_URL}/hubs/identity-and-delegation/" class="home-card-link">Explore Topic Guide →</a>
  </Card>
  <Card title="Tools & Excessive Agency" icon="wrench">
    Schema validation, parameter limits, idempotency, and confirmation gates.
    <br /><br />
    <a href="${BASE_URL}/hubs/tools-and-excessive-agency/" class="home-card-link">Explore Topic Guide →</a>
  </Card>
  <Card title="Model Context Protocol (MCP)" icon="puzzle">
    Trust perimeters, tool discovery risks, and secure gateway architectures for MCP.
    <br /><br />
    <a href="${BASE_URL}/hubs/mcp-and-protocols/" class="home-card-link">Explore Topic Guide →</a>
  </Card>
</CardGrid>

<div class="machine-panel not-content">
  <h3 style="margin-top: 0;">🤖 For AI Agents, LLMs & Retrieval Systems</h3>
  <p>This handbook is optimized for direct ingestion by language models and autonomous researchers:</p>
  <ul>
    <li>Ingest site summary and curriculum map via <code><a href="${BASE_URL}/llms.txt">${BASE_URL}/llms.txt</a></code></li>
    <li>Query structured unit metadata via <code><a href="${BASE_URL}/guide-index.json">${BASE_URL}/guide-index.json</a></code></li>
    <li>Retrieve clean Markdown alternate streams on all canonical pages.</li>
  </ul>
</div>
`,
  'utf8'
);

// 11. Write guide-index.json
console.log('🤖 Generating machine-readable guide-index.json...');
fs.writeFileSync(
  path.join(PUBLIC_DIR, 'guide-index.json'),
  JSON.stringify(
    {
      title: 'From LLMs to Secure Agents: Complete Guide Index',
      description: 'Machine-readable index of published units, learning objectives, source records, and canonical links.',
      version: '1.0.0',
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

// 12. Write llms.txt
console.log('📄 Generating llms.txt...');
const llmsTxtContent = `# From LLMs to Secure Agents

> A deep, visual, source-grounded guide to understanding complete agentic AI systems and learning how to secure and deploy them.

- **Site Origin:** ${SITE_ORIGIN}${BASE_URL}/
- **Structured Index:** ${SITE_ORIGIN}${BASE_URL}/guide-index.json
- **Source Repository:** https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents

## Core Architecture & Two Learning Passes

1. **Pass 1: Understand the System**
   - 00 Prerequisites: System vocabulary, components, data vs control boundaries, requests/events, identity & authority.
   - 01 Agent Foundations: What is an agent, 5-step cyclic loop, workflows vs agents, autonomy spectrum, run lifecycles.
   - 02 Agent Architectures: Single loop, plan-and-execute, evaluator-optimizer, state machine graphs, supervisors.
   - 03 Building Blocks: Context construction, memory, retrieval/RAG, tools, execution environments, human controls.
   - 04 Frameworks & Protocols: Model Context Protocol (MCP), agent-to-agent protocols.
   - 05 End-to-End Workflows: Complete enterprise implementations.

2. **Pass 2: Secure the System**
   - 06 Threat Model: Assets, adversaries, trust boundaries, entry points, attack taxonomy.
   - 07 Security by Component: Prompt injection, context poisoning, excessive agency, confused deputy, sandbox escape.
   - 08 Secure Reference Architectures: Read-only analytics, transactional agents, dual-agent supervisors, zero-trust gateways.
   - 09 Testing & Assurance: Automated red teaming, injection fuzzing, invariant checking.
   - 10 Open Research Questions: Formal verification of loops, unforgeable provenance.

## Published Canonical Chapters

${guideIndex
  .map(
    (u) => `### [${u.unit_id}: ${u.title}](${u.html_url})
- **Summary:** ${u.summary}
- **Pass:** ${u.pass} (${u.learning_path} path)
- **Clean Markdown URL:** ${u.markdown_url}
- **Key Objectives:**
${u.learning_objectives.map((o) => `  * ${o}`).join('\n')}
- **Verified Sources:** ${u.source_records.map((s) => `[${s.title}](${s.canonical_url})`).join(', ')}
`
  )
  .join('\n')}

## Curated Security Hubs
- [Securing AI Agents (Master Guide)](${SITE_ORIGIN}${BASE_URL}/hubs/securing-ai-agents/)
- [Indirect Prompt Injection & Context Security](${SITE_ORIGIN}${BASE_URL}/hubs/prompt-injection/)
- [Identity, Scoped Tokens & Least Privilege](${SITE_ORIGIN}${BASE_URL}/hubs/identity-and-delegation/)
- [Tools, Function Calling & Excessive Agency](${SITE_ORIGIN}${BASE_URL}/hubs/tools-and-excessive-agency/)
- [Execution Environments & Sandboxing](${SITE_ORIGIN}${BASE_URL}/hubs/execution-and-sandboxing/)
- [Model Context Protocol (MCP) Security](${SITE_ORIGIN}${BASE_URL}/hubs/mcp-and-protocols/)

## Reference & Terminology
- [System Glossary](${SITE_ORIGIN}${BASE_URL}/reference/glossary/)
- [Machine & LLM Endpoints](${SITE_ORIGIN}${BASE_URL}/reference/llm-endpoints/)
`;

fs.writeFileSync(path.join(PUBLIC_DIR, 'llms.txt'), llmsTxtContent, 'utf8');

console.log('🎉 Build pipeline preparation completed successfully!');
