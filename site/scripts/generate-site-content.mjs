import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'yaml';
import { discoverCanonicalChapters } from './discover-content.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(SITE_ROOT, '..');

const BASE_URL = '/From-LLMs-to-Secure-Agents';
const SITE_ORIGIN = 'https://renatomignone.github.io';
const GITHUB_REPO = 'https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents';

const DOCS_DIR = path.join(SITE_ROOT, 'src', 'content', 'docs');
const GENERATED_DIR = path.join(SITE_ROOT, 'src', 'generated');
const PUBLIC_DIR = path.join(SITE_ROOT, 'public');
const PUBLIC_ASSETS_DIR = path.join(PUBLIC_DIR, 'assets', 'images');
const SRC_ASSETS_DIR = path.join(SITE_ROOT, 'src', 'assets', 'images');
const PUBLIC_MARKDOWN_DIR = path.join(PUBLIC_DIR, 'markdown');

export function copyDirRecursive(src, dest) {
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

export function formatStringOrObject(item) {
  if (typeof item === 'string') return item;
  if (typeof item === 'object' && item !== null) {
    return Object.entries(item)
      .map(([k, v]) => `${k}: ${v}`)
      .join(' ');
  }
  return String(item || '');
}

export function renderInlineMarkdown(str) {
  let s = formatStringOrObject(str);
  s = s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*(.*?)\*/g, '<em>$1</em>');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
  return s;
}

export function rewriteChapterLinks(markdown, currentRelPath, allChapters) {
  // 1. Rewrite images
  let text = markdown.replace(
    /!\[(.*?)\]\((?:\.\.\/)*assets\/images\/(.*?)\)/g,
    `![$1](${BASE_URL}/assets/images/$2)`
  );

  // 2. Build mapping of canonical relative markdown paths to site URLs
  const linkMap = new Map();
  for (const c of allChapters) {
    linkMap.set(c.relPath, c.route);
    const fileName = path.basename(c.relPath);
    linkMap.set(fileName, c.route);
    const parts = c.relPath.split(path.sep);
    if (parts.length > 1) {
      linkMap.set(`../${c.relPath}`, c.route);
    }
  }

  // Rewrite section plan links to first chapter of published sections
  linkMap.set('00-prerequisites/chapter-plan.md', `${BASE_URL}/prerequisites/01-reader-contract-and-system-map/`);
  linkMap.set('../00-prerequisites/chapter-plan.md', `${BASE_URL}/prerequisites/01-reader-contract-and-system-map/`);
  linkMap.set('01-agent-foundations/chapter-plan.md', `${BASE_URL}/foundations/01-what-is-an-agent/`);
  linkMap.set('../01-agent-foundations/chapter-plan.md', `${BASE_URL}/foundations/01-what-is-an-agent/`);

  // Rewrite chapter cross-links
  for (const [targetPattern, targetRoute] of linkMap.entries()) {
    const escaped = targetPattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`\\[(.*?)\\]\\(${escaped}\\)`, 'g');
    text = text.replace(regex, `[$1](${targetRoute})`);
  }

  // Rewrite remaining chapter-plan.md or unwritten section links to GitHub canonical repo links
  text = text.replace(
    /\[(.*?)\]\((\.\.\/)*(\d+-[^/]+)\/chapter-plan\.md\)/g,
    `[$1](${GITHUB_REPO}/blob/main/knowledge/$3/chapter-plan.md)`
  );
  text = text.replace(
    /\[(.*?)\]\(chapter-plan\.md\)/g,
    `[$1](${GITHUB_REPO}/blob/main/knowledge/)`
  );

  return text;
}

export function generateAll() {
  console.log('🔄 Running From-LLMs-to-Secure-Agents publishing pipeline...');

  // 1. Discover chapters
  const { chapters } = discoverCanonicalChapters();
  console.log(`✓ Discovered ${chapters.length} canonical chapters in knowledge/.`);

  // 2. Clean directories
  fs.rmSync(DOCS_DIR, { recursive: true, force: true });
  fs.mkdirSync(DOCS_DIR, { recursive: true });

  fs.mkdirSync(GENERATED_DIR, { recursive: true });

  fs.rmSync(PUBLIC_ASSETS_DIR, { recursive: true, force: true });
  fs.mkdirSync(PUBLIC_ASSETS_DIR, { recursive: true });

  fs.rmSync(SRC_ASSETS_DIR, { recursive: true, force: true });
  fs.mkdirSync(SRC_ASSETS_DIR, { recursive: true });

  fs.rmSync(PUBLIC_MARKDOWN_DIR, { recursive: true, force: true });
  fs.mkdirSync(PUBLIC_MARKDOWN_DIR, { recursive: true });

  // 3. Copy visual assets
  console.log('📦 Copying visual assets...');
  copyDirRecursive(path.join(REPO_ROOT, 'assets', 'images'), PUBLIC_ASSETS_DIR);
  copyDirRecursive(path.join(REPO_ROOT, 'assets', 'images'), SRC_ASSETS_DIR);

  // 4. Generate Chapter Pages & Clean Markdown Alternates
  console.log('📖 Generating chapter documentation pages...');
  const guideIndex = [];

  for (let i = 0; i < chapters.length; i++) {
    const ch = chapters[i];
    const prevCh = i > 0 ? chapters[i - 1] : null;
    const nextCh = i < chapters.length - 1 ? chapters[i + 1] : null;

    const outDir = path.join(DOCS_DIR, ch.routeDir);
    fs.mkdirSync(outDir, { recursive: true });
    const outPath = path.join(DOCS_DIR, ch.docPath);

    const rawMarkdownDir = path.join(PUBLIC_MARKDOWN_DIR, ch.routeDir);
    fs.mkdirSync(rawMarkdownDir, { recursive: true });
    const rawMarkdownPath = path.join(PUBLIC_DIR, ch.markdownPath);

    // Format fields cleanly
    const formattedPrereqs = (ch.prerequisites || []).map((p) =>
      renderInlineMarkdown(rewriteChapterLinks(formatStringOrObject(p), ch.relPath, chapters))
    );
    const formattedObjectives = (ch.learning_objectives || []).map((o) =>
      renderInlineMarkdown(formatStringOrObject(o))
    );

    // Determine clean pass & path labels
    let passLabel = ch.pass;
    if (ch.sectionKey.startsWith('00-')) passLabel = 'Pass 0: Prerequisites';
    else if (ch.sectionKey.startsWith('01-')) passLabel = 'Pass 1: Agent Foundations';
    else if (ch.sectionKey.startsWith('02-')) passLabel = 'Pass 1: Architectures';
    else if (ch.sectionKey.startsWith('03-')) passLabel = 'Pass 1: Building Blocks';
    else if (ch.sectionKey.startsWith('06-')) passLabel = 'Pass 2: Threat Model';

    let pathLabel = 'Main path';
    if (ch.learning_path === 'deep_dive' || ch.learning_path === 'deep-dive') {
      pathLabel = 'Deep dive';
    }

    // Register in guide index
    guideIndex.push({
      unit_id: ch.unit_id,
      title: ch.title,
      summary: ch.summary,
      pass: passLabel,
      learning_path: ch.learning_path,
      status: ch.status,
      last_reviewed: ch.last_reviewed,
      html_url: ch.canonicalUrl,
      markdown_url: ch.markdownUrl,
      prerequisites: formattedPrereqs,
      learning_objectives: formattedObjectives,
      source_records: ch.source_records.map((s) => ({
        id: s.id,
        title: s.title,
        authors_or_organization: s.authors_or_organization,
        date: s.date,
        source_type: s.source_type,
        canonical_url: s.canonical_url,
        claims_supported: s.claims_supported || [],
        limitations: s.limitations || [],
      })),
      visual_assets: ch.visual_assets,
      example_paths: ch.example_paths,
    });

    // JSON-LD structured metadata
    const jsonLd = {
      '@context': 'https://schema.org',
      '@type': 'TechArticle',
      headline: ch.title,
      description: ch.summary,
      url: ch.canonicalUrl,
      dateModified: ch.last_reviewed,
      inLanguage: 'en-US',
      isPartOf: {
        '@type': 'Book',
        name: 'From LLMs to Secure Agents',
        url: `${SITE_ORIGIN}${BASE_URL}/`,
      },
      author: {
        '@type': 'Organization',
        name: 'From LLMs to Secure Agents Project',
        url: GITHUB_REPO,
      },
      educationalLevel: 'Core Engineering Curriculum',
    };

    // Starlight frontmatter
    const starlightFm = {
      title: ch.title,
      description: ch.summary,
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
      head: [
        {
          tag: 'script',
          attrs: { type: 'application/ld+json' },
          content: JSON.stringify(jsonLd),
        },
        {
          tag: 'link',
          attrs: { rel: 'alternate', type: 'text/markdown', href: ch.markdownUrl, title: `${ch.title} (Markdown)` },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:title', content: `${ch.title} | From LLMs to Secure Agents` },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:description', content: ch.summary },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
        },
      ],
    };

    let pageContent = `---
${yaml.stringify(starlightFm)}---

<div class="chapter-meta-line not-content">
  <span class="meta-item meta-unit">${ch.unit_id}</span>
  <span class="meta-sep">·</span>
  <span class="meta-item">${passLabel}</span>
  <span class="meta-sep">·</span>
  <span class="meta-item">${pathLabel}</span>
  <span class="meta-sep">·</span>
  <span class="meta-item meta-date">Reviewed ${ch.last_reviewed}</span>
</div>

<div class="chapter-abstract not-content">
  <p>${ch.summary}</p>
</div>
`;

    // Prerequisites and Objectives
    const hasPrereqs = formattedPrereqs.length > 0;
    const hasObjectives = formattedObjectives.length > 0;

    if (hasPrereqs || hasObjectives) {
      pageContent += `\n<div class="chapter-goals-grid not-content">\n`;
      if (hasPrereqs) {
        pageContent += `  <div class="goals-card">
    <div class="goals-heading">Prerequisites</div>
    <ul>
${formattedPrereqs.map((p) => `      <li>${p}</li>`).join('\n')}
    </ul>
  </div>\n`;
      }
      if (hasObjectives) {
        pageContent += `  <div class="goals-card">
    <div class="goals-heading">Learning objectives</div>
    <ul>
${formattedObjectives.map((o) => `      <li>${o}</li>`).join('\n')}
    </ul>
  </div>\n`;
      }
      pageContent += `</div>\n\n`;
    }

    // Clean body
    let cleanBody = ch.body.trim();
    cleanBody = cleanBody.replace(/^#\s+[^\n]+\n+/, '');
    cleanBody = rewriteChapterLinks(cleanBody, ch.relPath, chapters);

    pageContent += cleanBody;

    // Sources and evidence panel
    if (ch.source_records.length > 0) {
      pageContent += `\n\n<details class="chapter-sources not-content">
  <summary class="sources-summary">
    <span class="sources-title">Sources and evidence (${ch.source_records.length} primary records)</span>
    <span class="sources-hint">Expand to inspect citations and grounded claims</span>
  </summary>
  <div class="sources-body">
${ch.source_records
  .map(
    (s) => `    <div class="source-item">
      <div class="source-item-header">
        <a href="${s.canonical_url}" target="_blank" rel="noopener noreferrer" class="source-title-link">${s.title} ↗</a>
        <span class="source-type-pill">${s.source_type || 'specification'}</span>
      </div>
      <div class="source-item-meta">
        <span>${s.authors_or_organization}</span> · <span>${s.date}</span> ${s.version ? `· <span>v${s.version}</span>` : ''} · <span>Verified ${s.last_verified || '2026-08-15'}</span>
      </div>
      ${
        s.claims_supported && s.claims_supported.length > 0
          ? `<div class="source-claims">
        <div class="claims-heading">Claims grounded:</div>
        <ul>
          ${s.claims_supported.map((c) => `<li>${c}</li>`).join('')}
        </ul>
      </div>`
          : ''
      }
      ${
        s.limitations && s.limitations.length > 0
          ? `<div class="source-limitations">
        <span class="limitations-heading">Scope &amp; limitations:</span> ${s.limitations.join(' ')}
      </div>`
          : ''
      }
    </div>`
  )
  .join('\n')}
  </div>
</details>\n`;
    }

    // Unit Pagination
    pageContent += `\n<div class="unit-pagination not-content">\n`;
    if (prevCh) {
      pageContent += `  <a href="${prevCh.route}" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Previous unit</span>
    <span class="pagination-name">${prevCh.title}</span>
  </a>\n`;
    } else {
      pageContent += `  <a href="${BASE_URL}/" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Overview</span>
    <span class="pagination-name">Handbook Introduction</span>
  </a>\n`;
    }

    if (nextCh) {
      pageContent += `  <a href="${nextCh.route}" class="pagination-link pagination-next">
    <span class="pagination-sub">Next unit →</span>
    <span class="pagination-name">${nextCh.title}</span>
  </a>\n`;
    } else {
      pageContent += `  <div class="pagination-link pagination-next pagination-end">
    <span class="pagination-sub">Curriculum status</span>
    <span class="pagination-name">Completed through ${ch.unit_id}</span>
  </div>\n`;
    }
    pageContent += `</div>\n`;

    fs.writeFileSync(outPath, pageContent, 'utf8');

    // Clean canonical markdown alternate
    const cleanMarkdown = `---
title: ${JSON.stringify(ch.title)}
unit_id: ${JSON.stringify(ch.unit_id)}
summary: ${JSON.stringify(ch.summary)}
pass: ${JSON.stringify(passLabel)}
learning_path: ${JSON.stringify(ch.learning_path)}
status: ${JSON.stringify(ch.status)}
last_reviewed: ${JSON.stringify(ch.last_reviewed)}
canonical_url: ${JSON.stringify(ch.canonicalUrl)}
---

# ${ch.title}

> **Summary:** ${ch.summary}
> **Unit ID:** ${ch.unit_id} · **Pass:** ${passLabel} · **Reviewed:** ${ch.last_reviewed}

${ch.body.trim()}

## Sources & Evidence
${ch.source_records.map((s) => `- [${s.title}](${s.canonical_url}) (${s.authors_or_organization}, ${s.date})`).join('\n')}
`;
    fs.writeFileSync(rawMarkdownPath, cleanMarkdown, 'utf8');
  }

  console.log(`✓ Successfully generated ${chapters.length} chapter documentation pages.`);

  // 5. Generate Dynamic Sidebar Configuration
  console.log('📑 Generating dynamic sidebar configuration...');
  const sidebarSections = [];
  const chaptersBySection = new Map();

  for (const ch of chapters) {
    if (!chaptersBySection.has(ch.sectionLabel)) {
      chaptersBySection.set(ch.sectionLabel, []);
    }
    chaptersBySection.get(ch.sectionLabel).push(ch);
  }

  for (const [label, sectionChapters] of chaptersBySection.entries()) {
    sidebarSections.push({
      label,
      items: sectionChapters.map((c) => ({
        label: `${c.title}`,
        link: `${c.route.replace(BASE_URL, '')}`,
      })),
    });
  }

  fs.writeFileSync(
    path.join(GENERATED_DIR, 'sidebar.json'),
    JSON.stringify(sidebarSections, null, 2),
    'utf8'
  );

  // 6. Generate Calm Editorial Homepage (index.mdx)
  console.log('🏠 Generating calm editorial homepage...');
  const firstChapterRoute = chapters.length > 0 ? chapters[0].route : `${BASE_URL}/`;

  const homepageContent = `---
title: "From LLMs to Secure Agents"
description: "A visual, source-grounded guide to the architecture, deployment, threat modeling, testing, and security of AI agents."
template: splash
tableOfContents: false
prev: false
next: false
---

import HomepageHero from '../../components/HomepageHero.astro';
import HomepagePurpose from '../../components/HomepagePurpose.astro';
import HomepageTwoPass from '../../components/HomepageTwoPass.astro';
import HomepageStart from '../../components/HomepageStart.astro';
import HomepageFooter from '../../components/HomepageFooter.astro';

<HomepageHero firstChapterRoute="${firstChapterRoute}" githubUrl="${GITHUB_REPO}" />

<HomepagePurpose baseUrl="${BASE_URL}" />

<HomepageTwoPass />

<HomepageStart firstChapterRoute="${firstChapterRoute}" completedThrough="${chapters[chapters.length - 1]?.unit_id || 'P1-01-05'}" totalUnits="${chapters.length}" />

<HomepageFooter githubUrl="${GITHUB_REPO}" />
`;

  fs.writeFileSync(path.join(DOCS_DIR, 'index.mdx'), homepageContent, 'utf8');

  // 7. Generate guide-index.json
  console.log('🤖 Generating machine-readable guide-index.json...');
  fs.writeFileSync(
    path.join(PUBLIC_DIR, 'guide-index.json'),
    JSON.stringify(
      {
        title: 'From LLMs to Secure Agents: Engineering Guide Index',
        description: 'Machine-readable index of published units, learning objectives, source records, and canonical links.',
        version: '1.2.0',
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

  // 8. Generate llms.txt
  console.log('📄 Generating llms.txt...');
  const llmsTxtContent = `# From LLMs to Secure Agents

> A visual, source-grounded engineering guide to understanding complete agentic AI architectures and learning how to threat-model, sandbox, and secure them.

- **Site Origin:** ${SITE_ORIGIN}${BASE_URL}/
- **Structured Index:** ${SITE_ORIGIN}${BASE_URL}/guide-index.json
- **Source Repository:** ${GITHUB_REPO}
- **Current Canonical Progress:** Completed through ${chapters[chapters.length - 1]?.unit_id || 'P1-01-05'} (${chapters.length} units published)

## Curriculum Architecture (Two-Pass Model)

1. **Pass 1: Understand the Complete System**
   - **00 Prerequisites:** Core distributed systems and software boundaries (Data vs Control Flow, Trust Boundaries, Requests/Events/State, Identity & Least Privilege).
   - **01 Agent Foundations:** Autonomous model-directed control loops, the 5-step agent loop, workflows vs agents, goals and autonomy, run lifecycles and termination guarantees.
   - **02 Agent Architectures (Roadmap):** Single loops, plan-and-execute, reflection, state machines, supervisor and multi-agent topologies.
   - **03 Building Blocks (Roadmap):** Context construction, short-term and persistent memory, agentic RAG, tools and function calling, execution sandboxes, observability.
   - **04 Frameworks & Protocols (Roadmap):** Model Context Protocol (MCP), agent-to-agent protocols, human-agent interaction.
   - **05 End-to-End Workflows (Roadmap):** Reference production architectures.

2. **Pass 2: Secure the System (Roadmap)**
   - **06 Threat Model:** Entry points, adversaries, and comprehensive agent attack taxonomy.
   - **07 Security by Component:** Indirect prompt injection defenses, credential scoping, memory isolation, execution sandboxing.
   - **08 Secure Reference Architectures:** Zero-trust agent gateways and dual-model verification.
   - **09 Testing & Assurance:** Automated red teaming, prompt fuzzing, invariant testing.
   - **10 Open Research Questions:** Formal loop verification and verifiable provenance.

## Published Canonical Units

${guideIndex
  .map(
    (u) => `### [${u.unit_id}: ${u.title}](${u.html_url})
- **Summary:** ${u.summary}
- **Clean Markdown URL:** ${u.markdown_url}
- **Learning Objectives:**
${u.learning_objectives.map((o) => `  * ${o}`).join('\n')}
- **Verified Sources:** ${u.source_records.map((s) => `[${s.title}](${s.canonical_url})`).join(', ')}
`
  )
  .join('\n')}
`;

  fs.writeFileSync(path.join(PUBLIC_DIR, 'llms.txt'), llmsTxtContent, 'utf8');

  // 9. Generate robots.txt
  console.log('🤖 Generating robots.txt...');
  const robotsTxtContent = `User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

Sitemap: ${SITE_ORIGIN}${BASE_URL}/sitemap-index.xml
`;
  fs.writeFileSync(path.join(PUBLIC_DIR, 'robots.txt'), robotsTxtContent, 'utf8');

  console.log('🎉 Site content generation finished cleanly!');
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  generateAll();
}
