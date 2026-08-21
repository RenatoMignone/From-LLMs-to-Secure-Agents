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

export const sectionLabels = {
  '00-prerequisites': { label: 'Prerequisites', routeDir: 'prerequisites', pass: 'Pass 0: Prerequisites' },
  '01-agent-foundations': { label: 'Agent foundations', routeDir: 'foundations', pass: 'Pass 1: Agent Foundations' },
  '02-agent-architectures': { label: 'Agent architectures', routeDir: 'architectures', pass: 'Pass 1: Architectures' },
  '03-building-blocks': { label: 'Building blocks', routeDir: 'building-blocks', pass: 'Pass 1: Building Blocks' },
  '04-frameworks-and-protocols': { label: 'Frameworks and protocols', routeDir: 'frameworks-and-protocols', pass: 'Pass 1: Protocols' },
  '05-end-to-end-workflows': { label: 'End-to-end workflows', routeDir: 'end-to-end-workflows', pass: 'Pass 1: Workflows' },
  '06-threat-model': { label: 'Threat model', routeDir: 'threat-model', pass: 'Pass 2: Threat Model' },
  '07-security-by-component-and-workflow-stage': { label: 'Security by component', routeDir: 'security-by-component', pass: 'Pass 2: Security Controls' },
  '08-secure-reference-architectures': { label: 'Secure reference architectures', routeDir: 'secure-architectures', pass: 'Pass 2: Reference Architectures' },
  '09-security-testing-evaluation-and-assurance': { label: 'Testing and assurance', routeDir: 'testing-and-assurance', pass: 'Pass 2: Testing & Assurance' },
  '10-open-research-questions': { label: 'Open research questions', routeDir: 'open-research', pass: 'Pass 2: Open Research' },
};

export function loadSources(sourcesDir = path.join(REPO_ROOT, 'sources')) {
  const sourceIndex = new Map();

  function scan(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scan(full);
      } else if (entry.isFile() && entry.name.endsWith('.yml')) {
        try {
          const raw = fs.readFileSync(full, 'utf8');
          const doc = yaml.parse(raw);
          if (doc && doc.id) {
            sourceIndex.set(doc.id, doc);
            const relPath = path.relative(sourcesDir, full);
            sourceIndex.set(relPath, doc);
          }
        } catch (err) {
          console.warn(`Warning: failed to parse source at ${full}:`, err.message);
        }
      }
    }
  }

  scan(sourcesDir);
  return sourceIndex;
}

export function discoverCanonicalChapters({
  knowledgeDir = path.join(REPO_ROOT, 'knowledge'),
  sourcesDir = path.join(REPO_ROOT, 'sources'),
} = {}) {
  const sourceIndex = loadSources(sourcesDir);
  const rawChapters = [];

  function scan(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scan(full);
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        if (entry.name === 'AGENTS.md' || entry.name === 'chapter-plan.md' || entry.name.startsWith('.')) {
          continue;
        }
        const rel = path.relative(knowledgeDir, full);
        const content = fs.readFileSync(full, 'utf8');
        const match = content.match(/^(?:<!--\s*)?---\n([\s\S]*?)\n---\s*(?:-->)?\n?([\s\S]*)$/);
        if (!match) continue;

        let fm = {};
        try {
          fm = yaml.parse(match[1]) || {};
        } catch (e) {
          console.error(`Error parsing YAML frontmatter in ${full}:`, e);
          continue;
        }

        // Only explicitly complete canonical units are public.
        if (!fm.unit_id || !fm.title || fm.status !== 'complete') continue;

        rawChapters.push({
          fullPath: full,
          relPath: rel,
          frontmatter: fm,
          body: match[2],
        });
      }
    }
  }

  scan(knowledgeDir);

  // Sort chapters deterministically by directory and filename
  rawChapters.sort((a, b) => a.relPath.localeCompare(b.relPath));

  const processedChapters = rawChapters.map((ch, index) => {
    const parts = ch.relPath.split(path.sep);
    const topSection = parts[0];
    const fileName = parts[parts.length - 1].replace(/\.md$/, '');
    const secMeta = sectionLabels[topSection] || {
      label: topSection.replace(/^\d+-/, '').replace(/-/g, ' '),
      routeDir: topSection.replace(/^\d+-/, ''),
      pass: 'Core',
    };

    const routeDir = secMeta.routeDir;
    const slug = fileName;
    const route = `${BASE_URL}/${routeDir}/${slug}/`;
    const docPath = path.join(routeDir, `${slug}.md`);
    const markdownPath = path.join('markdown', routeDir, `${slug}.md`);
    const canonicalUrl = `${SITE_ORIGIN}${route}`;
    const markdownUrl = `${SITE_ORIGIN}${BASE_URL}/${markdownPath}`;
    const chapterNumber = rawChapters
      .filter((candidate) => candidate.relPath.split(path.sep)[0] === topSection)
      .findIndex((candidate) => candidate.relPath === ch.relPath) + 1;

    // Resolve sources
    const sourcesData = [];
    const sourceRecords = ch.frontmatter.source_records || [];
    const chDirRel = ch.relPath.replace(/\.md$/, '');
    for (const srcId of sourceRecords) {
      const srcDoc = sourceIndex.get(srcId) || sourceIndex.get(`${chDirRel}/${srcId}.yml`);
      if (srcDoc) {
        sourcesData.push(srcDoc);
      }
    }

    return {
      unit_id: ch.frontmatter.unit_id,
      reader_id: `${routeDir}/${slug}`,
      chapterNumber,
      chapterLabel: `Chapter ${chapterNumber}`,
      title: ch.frontmatter.title,
      summary: ch.frontmatter.summary,
      pass: ch.frontmatter.pass || secMeta.pass,
      learning_path: ch.frontmatter.learning_path || 'main-path',
      status: ch.frontmatter.status,
      last_reviewed: ch.frontmatter.last_reviewed || '2026-08-15',
      prerequisites: ch.frontmatter.prerequisites || [],
      learning_objectives: ch.frontmatter.learning_objectives || [],
      source_records: sourcesData,
      visual_assets: ch.frontmatter.visual_assets || [],
      example_paths: ch.frontmatter.example_paths || [],
      fullPath: ch.fullPath,
      relPath: ch.relPath,
      sectionKey: topSection,
      sectionLabel: secMeta.label,
      routeDir,
      slug,
      route,
      docPath,
      markdownPath,
      canonicalUrl,
      markdownUrl,
      body: ch.body,
      index,
    };
  });

  const sections = discoverSections({ knowledgeDir, chapters: processedChapters });

  return {
    chapters: processedChapters,
    sections,
    sourceIndex,
    sectionLabels,
  };
}

export function parseChapterPlan(planPath) {
  if (!fs.existsSync(planPath)) return null;
  const content = fs.readFileSync(planPath, 'utf8');

  const titleMatch = content.match(/^#\s+(.+)$/m);
  const purposeMatch = content.match(/## Section purpose\s*\n+([\s\S]*?)(?=\n##|$)/i);
  const outcomesMatch = content.match(/## Learning outcomes\s*\n+([\s\S]*?)(?=\n##|$)/i);
  const prereqMatch = content.match(/## Prerequisites\s*\n+([\s\S]*?)(?=\n##|$)/i);
  const conceptsMatch = content.match(/## Required concepts\s*\n+([\s\S]*?)(?=\n##|$)/i);
  const securityMatch = content.match(/## Connections to later security chapters\s*\n+([\s\S]*?)(?=\n##|$)/i);

  return {
    rawTitle: titleMatch ? titleMatch[1].trim() : '',
    purpose: purposeMatch ? purposeMatch[1].trim() : '',
    outcomes: outcomesMatch ? outcomesMatch[1].trim() : '',
    prerequisites: prereqMatch ? prereqMatch[1].trim() : '',
    concepts: conceptsMatch ? conceptsMatch[1].trim() : '',
    securityConnection: securityMatch ? securityMatch[1].trim() : '',
  };
}

export function discoverSections({
  knowledgeDir = path.join(REPO_ROOT, 'knowledge'),
  chapters = [],
} = {}) {
  const sections = [];
  const sectionKeys = Object.keys(sectionLabels);

  for (const key of sectionKeys) {
    const secMeta = sectionLabels[key];
    const planPath = path.join(knowledgeDir, key, 'chapter-plan.md');
    const plan = parseChapterPlan(planPath);
    const sectionChapters = chapters.filter((c) => c.sectionKey === key);

    if (sectionChapters.length > 0) {
      const route = `${BASE_URL}/${secMeta.routeDir}/`;
      const docPath = path.join(secMeta.routeDir, 'index.md');
      const markdownPath = path.join('markdown', secMeta.routeDir, 'index.md');
      const canonicalUrl = `${SITE_ORIGIN}${route}`;
      const markdownUrl = `${SITE_ORIGIN}${BASE_URL}/${markdownPath}`;

      sections.push({
        sectionKey: key,
        label: secMeta.label,
        routeDir: secMeta.routeDir,
        pass: secMeta.pass,
        route,
        docPath,
        markdownPath,
        canonicalUrl,
        markdownUrl,
        plan,
        chapters: sectionChapters,
      });
    }
  }

  return sections;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { chapters, sections } = discoverCanonicalChapters();
  console.log(`Discovered ${chapters.length} canonical chapters across ${sections.length} sections:`);
  for (const s of sections) {
    console.log(`\n📁 [${s.pass}] ${s.label} -> ${s.route} (${s.chapters.length} units)`);
    for (const c of s.chapters) {
      console.log(`   - [${c.unit_id}] ${c.title}`);
    }
  }
}
