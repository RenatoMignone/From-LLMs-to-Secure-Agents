import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
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
const LEGACY_SRC_ASSETS_DIR = path.join(SITE_ROOT, 'src', 'assets', 'images');
const PUBLIC_MARKDOWN_DIR = path.join(PUBLIC_DIR, 'markdown');
const RESPONSIVE_WIDTHS = [480, 800, 1200, 1600];
const responsiveImages = new Map();

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

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

async function publishResponsiveImages(srcRoot, destRoot) {
  responsiveImages.clear();
  copyDirRecursive(srcRoot, destRoot);

  const sourceFiles = [];
  function scan(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === 'source') continue;
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) scan(fullPath);
      else if (/\.(png|jpe?g|webp)$/i.test(entry.name)) sourceFiles.push(fullPath);
    }
  }
  scan(srcRoot);

  for (const sourcePath of sourceFiles) {
    const relPath = path.relative(srcRoot, sourcePath).split(path.sep).join('/');
    const metadata = await sharp(sourcePath).metadata();
    if (!metadata.width || !metadata.height) continue;

    const widths = RESPONSIVE_WIDTHS.filter((width) => width < metadata.width);
    widths.push(metadata.width);
    const uniqueWidths = [...new Set(widths)];
    const parsed = path.posix.parse(relPath);
    const variants = [];

    for (const width of uniqueWidths) {
      const variantRelPath = path.posix.join(parsed.dir, `${parsed.name}-${width}w.webp`);
      const variantPath = path.join(destRoot, ...variantRelPath.split('/'));
      fs.mkdirSync(path.dirname(variantPath), { recursive: true });
      await sharp(sourcePath)
        .resize({ width, withoutEnlargement: true })
        .webp({ quality: 82, effort: 5, smartSubsample: true })
        .toFile(variantPath);
      variants.push({ width, path: variantRelPath });
    }

    responsiveImages.set(relPath, {
      width: metadata.width,
      height: metadata.height,
      variants,
    });
  }
}

function responsiveImageMarkup(relPath, alt, { eager = false, sizes = '(max-width: 58rem) calc(100vw - 2rem), 58rem' } = {}) {
  const image = responsiveImages.get(relPath);
  if (!image) return `![${alt}](${BASE_URL}/assets/images/${relPath})`;
  const largest = image.variants.at(-1);
  const srcset = image.variants
    .map((variant) => `${BASE_URL}/assets/images/${variant.path} ${variant.width}w`)
    .join(', ');
  return `<picture class="responsive-illustration">
  <source type="image/webp" srcset="${srcset}" sizes="${sizes}" />
  <img src="${BASE_URL}/assets/images/${largest.path}" alt="${escapeHtml(alt)}" width="${image.width}" height="${image.height}" loading="${eager ? 'eager' : 'lazy'}" decoding="async"${eager ? ' fetchpriority="high"' : ''} />
</picture>`;
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

function sectionSequenceLabel(index) {
  return String(index + 1).padStart(2, '0');
}

function chapterSequenceLabel(chapter) {
  return String(chapter.chapterNumber).padStart(2, '0');
}

function subsectionLabel(subsectionKey) {
  const label = subsectionKey.split('/').at(-1).replace(/^\d+-/, '').replaceAll('-', ' ');
  return label.charAt(0).toUpperCase() + label.slice(1);
}

function groupSectionChapters(section) {
  const groups = [];
  const topLevel = section.chapters.filter((chapter) => chapter.relPath.split(path.sep).length === 2);

  if (topLevel.length > 0) {
    groups.push({
      key: 'core-sequence',
      label: section.chapters.some((chapter) => chapter.relPath.split(path.sep).length > 2)
        ? 'Core sequence'
        : section.label,
      chapters: topLevel,
    });
  }

  const nestedGroups = new Map();
  for (const chapter of section.chapters) {
    const parts = chapter.relPath.split(path.sep);
    if (parts.length <= 2) continue;
    const key = parts.slice(1, -1).join('/');
    if (!nestedGroups.has(key)) nestedGroups.set(key, []);
    nestedGroups.get(key).push(chapter);
  }

  for (const [key, chapters] of nestedGroups) {
    groups.push({ key, label: subsectionLabel(key), chapters });
  }

  return groups;
}

export function rewriteChapterLinks(markdown, currentRelPath, allChapters, { responsive = false } = {}) {
  // 1. Rewrite images
  let text = markdown.replace(
    /!\[(.*?)\]\((?:\.\.\/)*assets\/images\/(.*?)\)/g,
    (_match, alt, relPath) => responsive
      ? responsiveImageMarkup(relPath, alt)
      : `![${alt}](${BASE_URL}/assets/images/${relPath})`
  );

  // 2. Resolve every repository-relative link from the canonical Markdown file.
  // Filename-only matching is unsafe because many nested sections reuse names
  // such as 01-*.md. Preserve fragments and queries when rewriting.
  const chapterRoutes = new Map(
    allChapters.map((chapter) => [chapter.relPath.split(path.sep).join('/'), chapter.route])
  );
  const publishedSectionRoutes = new Map(
    allChapters.map((chapter) => [chapter.sectionKey, `${BASE_URL}/${chapter.routeDir}/`])
  );
  const currentRepoPath = path.posix.join('knowledge', currentRelPath.split(path.sep).join('/'));

  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, rawHref) => {
    const href = rawHref.trim();
    if (
      href.startsWith('#') ||
      href.startsWith('/') ||
      /^[a-z][a-z\d+.-]*:/i.test(href)
    ) {
      return match;
    }

    const targetMatch = href.match(/^([^?#]+)([?#].*)?$/);
    if (!targetMatch) return match;
    const [, target, suffix = ''] = targetMatch;
    const resolvedRepoPath = path.posix.normalize(
      path.posix.join(path.posix.dirname(currentRepoPath), target)
    );
    const resolvedKnowledgePath = resolvedRepoPath.startsWith('knowledge/')
      ? resolvedRepoPath.slice('knowledge/'.length)
      : null;

    if (resolvedKnowledgePath && chapterRoutes.has(resolvedKnowledgePath)) {
      return `[${label}](${chapterRoutes.get(resolvedKnowledgePath)}${suffix})`;
    }

    if (resolvedKnowledgePath?.endsWith('/chapter-plan.md')) {
      const planDirectory = path.posix.dirname(resolvedKnowledgePath);
      const sectionKey = planDirectory.split('/')[0];
      if (planDirectory === sectionKey && publishedSectionRoutes.has(sectionKey)) {
        return `[${label}](${publishedSectionRoutes.get(sectionKey)}${suffix})`;
      }
    }

    if (!resolvedRepoPath.startsWith('../')) {
      return `[${label}](${GITHUB_REPO}/blob/main/${resolvedRepoPath}${suffix})`;
    }

    return match;
  });

  return text;
}

export async function generateAll() {
  console.log('🔄 Running From-LLMs-to-Secure-Agents publishing pipeline...');

  // 1. Discover chapters and sections
  const { chapters, sections } = discoverCanonicalChapters();
  console.log(`✓ Discovered ${chapters.length} canonical chapters across ${sections.length} sections in knowledge/.`);

  // 2. Clean directories
  fs.rmSync(DOCS_DIR, { recursive: true, force: true });
  fs.mkdirSync(DOCS_DIR, { recursive: true });

  fs.mkdirSync(GENERATED_DIR, { recursive: true });

  fs.rmSync(PUBLIC_ASSETS_DIR, { recursive: true, force: true });
  fs.mkdirSync(PUBLIC_ASSETS_DIR, { recursive: true });

  // Images are served from public/. Remove the old duplicate generated tree.
  fs.rmSync(LEGACY_SRC_ASSETS_DIR, { recursive: true, force: true });

  fs.rmSync(PUBLIC_MARKDOWN_DIR, { recursive: true, force: true });
  fs.mkdirSync(PUBLIC_MARKDOWN_DIR, { recursive: true });

  // 3. Copy visual assets
  console.log('📦 Publishing responsive visual assets...');
  await publishResponsiveImages(path.join(REPO_ROOT, 'assets', 'images'), PUBLIC_ASSETS_DIR);
  console.log(`✓ Published responsive variants for ${responsiveImages.size} images.`);

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
      id: ch.reader_id,
      title: ch.title,
      summary: ch.summary,
      pass: passLabel,
      section: ch.sectionLabel,
      section_id: ch.routeDir,
      chapter_number: ch.chapterNumber,
      chapter_label: ch.chapterLabel,
      section_label: ch.sectionLabel,
      learning_path: pathLabel,
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

    // Enhanced JSON-LD structured metadata for 2026 AEO & GEO
    const jsonLd = {
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'TechArticle',
          '@id': `${ch.canonicalUrl}#article`,
          headline: ch.title,
          description: ch.summary,
          url: ch.canonicalUrl,
          dateModified: ch.last_reviewed,
          inLanguage: 'en-US',
          isPartOf: {
            '@type': 'Book',
            '@id': `${SITE_ORIGIN}${BASE_URL}/#handbook`,
            name: 'From LLMs to Secure Agents',
            url: `${SITE_ORIGIN}${BASE_URL}/`,
          },
          author: {
            '@type': 'Person',
            name: 'Renato Mignone',
            url: 'https://github.com/RenatoMignone',
          },
          publisher: {
            '@type': 'Organization',
            name: 'From LLMs to Secure Agents',
            url: `${SITE_ORIGIN}${BASE_URL}/`,
          },
          mainEntityOfPage: ch.canonicalUrl,
          speakable: {
            '@type': 'SpeakableSpecification',
            cssSelector: ['#_top', '.chapter-standfirst', '.goals-card ul', '.sl-markdown-content > p:first-of-type'],
          },
          about: [ch.title, ch.sectionLabel, 'AI agent engineering'],
        },
        {
          '@type': 'LearningResource',
          '@id': `${ch.canonicalUrl}#learning-resource`,
          name: ch.title,
          description: ch.summary,
          learningResourceType: 'Handbook Chapter',
          educationalLevel: 'Core Engineering Curriculum',
          teaches: ch.learning_objectives.map(formatStringOrObject),
        },
        {
          '@type': 'BreadcrumbList',
          '@id': `${ch.canonicalUrl}#breadcrumb`,
          itemListElement: [
            {
              '@type': 'ListItem',
              position: 1,
              name: 'Handbook',
              item: `${SITE_ORIGIN}${BASE_URL}/`,
            },
            {
              '@type': 'ListItem',
              position: 2,
              name: ch.sectionLabel,
              item: `${SITE_ORIGIN}${BASE_URL}/${ch.routeDir}/`,
            },
            {
              '@type': 'ListItem',
              position: 3,
              name: ch.title,
              item: ch.canonicalUrl,
            },
          ],
        },
      ],
    };

    // Starlight frontmatter
    const starlightFm = {
      title: ch.title,
      description: ch.summary,
      summary: ch.summary,
      chapter_label: ch.chapterLabel,
      section_label: ch.sectionLabel,
      pass: passLabel,
      learning_path: ch.learning_path,
      reviewed_label: new Intl.DateTimeFormat('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        timeZone: 'UTC',
      }).format(new Date(`${ch.last_reviewed}T00:00:00Z`)),
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
          attrs: { rel: 'canonical', href: ch.canonicalUrl },
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
          attrs: { property: 'og:type', content: 'article' },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:url', content: ch.canonicalUrl },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:site_name', content: 'From LLMs to Secure Agents' },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:card', content: 'summary_large_image' },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:title', content: `${ch.title} | From LLMs to Secure Agents` },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:description', content: ch.summary },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
        },
        {
          tag: 'meta',
          attrs: { name: 'keywords', content: `AI agent, LLM security, threat model, ${ch.title}, ${ch.sectionLabel}, prompt injection defense, agentic architecture` },
        },
      ],
    };

    let pageContent = `---
${yaml.stringify(starlightFm)}---
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
    // Strip redundant trailing Markdown navigation buttons/links since unit-pagination provides them
    cleanBody = cleanBody.replace(/\n*---\s*\n+\[(?:Next|Previous) Unit:[^\]]+\]\([^)]+\)\s*$/i, '');
    cleanBody = cleanBody.replace(/\n*\[(?:Next|Previous) Unit:[^\]]+\]\([^)]+\)\s*$/i, '');
    cleanBody = rewriteChapterLinks(cleanBody, ch.relPath, chapters, { responsive: true });

    pageContent += cleanBody;

    // Chapter pagination
    pageContent += `\n\n<div class="unit-pagination not-content">\n`;
    if (prevCh) {
      pageContent += `  <a href="${prevCh.route}" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Previous chapter</span>
    <span class="pagination-name">${prevCh.title}</span>
  </a>\n`;
    } else {
      pageContent += `  <a href="${BASE_URL}/${ch.routeDir}/" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Section overview</span>
    <span class="pagination-name">${ch.sectionLabel}</span>
  </a>\n`;
    }

    if (nextCh) {
      pageContent += `  <a href="${nextCh.route}" class="pagination-link pagination-next">
    <span class="pagination-sub">Next chapter →</span>
    <span class="pagination-name">${nextCh.title}</span>
  </a>\n`;
    } else {
      pageContent += `  <div class="pagination-link pagination-next pagination-end">
    <span class="pagination-sub">Latest published chapter</span>
    <span class="pagination-name">${ch.title}</span>
  </div>\n`;
    }
    pageContent += `</div>\n`;

    fs.writeFileSync(outPath, pageContent, 'utf8');

    // Clean canonical markdown alternate
    const cleanMarkdown = `---
title: ${JSON.stringify(ch.title)}
id: ${JSON.stringify(ch.reader_id)}
summary: ${JSON.stringify(ch.summary)}
pass: ${JSON.stringify(passLabel)}
learning_path: ${JSON.stringify(ch.learning_path)}
status: ${JSON.stringify(ch.status)}
last_reviewed: ${JSON.stringify(ch.last_reviewed)}
canonical_url: ${JSON.stringify(ch.canonicalUrl)}
---

# ${ch.title}

> **Summary:** ${ch.summary}
> **Section:** ${ch.sectionLabel} · **Chapter:** ${ch.chapterNumber} · **Path:** ${pathLabel} · **Reviewed:** ${ch.last_reviewed}

${rewriteChapterLinks(ch.body.trim(), ch.relPath, chapters)}

## Sources & Evidence
${ch.source_records.map((s) => `- [${s.title}](${s.canonical_url}) (${s.authors_or_organization}, ${s.date})`).join('\n')}
`;
    fs.writeFileSync(rawMarkdownPath, cleanMarkdown, 'utf8');
  }

  console.log(`✓ Successfully generated ${chapters.length} chapter documentation pages.`);

  // 5. Generate Section Hub Pages (Indexable Pillar Pages)
  console.log('🏛️ Generating section hub overview pages...');
  for (let sIdx = 0; sIdx < sections.length; sIdx++) {
    const s = sections[sIdx];
    const prevSection = sIdx > 0 ? sections[sIdx - 1] : null;
    const nextSection = sIdx < sections.length - 1 ? sections[sIdx + 1] : null;
    const chapterGroups = groupSectionChapters(s);
    const firstChapter = s.chapters[0];
    const sectionOutDir = path.join(DOCS_DIR, s.routeDir);
    fs.mkdirSync(sectionOutDir, { recursive: true });
    const sectionDocPath = path.join(DOCS_DIR, s.docPath);

    const sectionRawMarkdownDir = path.join(PUBLIC_MARKDOWN_DIR, s.routeDir);
    fs.mkdirSync(sectionRawMarkdownDir, { recursive: true });
    const sectionRawMarkdownPath = path.join(PUBLIC_DIR, s.markdownPath);

    const formattedSectionPrereqs = s.plan?.prerequisites
      ? renderInlineMarkdown(rewriteChapterLinks(s.plan.prerequisites, path.join(s.sectionKey, 'chapter-plan.md'), chapters))
      : 'Working familiarity with large language models and prompts.';
    const formattedSectionOutcomes = s.plan?.outcomes
      ? renderInlineMarkdown(s.plan.outcomes)
      : `Master core architectural patterns and functional boundaries in ${s.label.toLowerCase()}.`;

    const sectionJsonLd = {
      '@context': 'https://schema.org',
      '@graph': [
        {
          '@type': 'CollectionPage',
          '@id': `${s.canonicalUrl}#collection`,
          name: `${s.label}: Curriculum Section Overview`,
          description: s.plan?.purpose || `Engineering curriculum units covering ${s.label.toLowerCase()} in autonomous AI systems.`,
          url: s.canonicalUrl,
          inLanguage: 'en-US',
          isPartOf: {
            '@type': 'Course',
            '@id': `${SITE_ORIGIN}${BASE_URL}/#course`,
            name: 'From LLMs to Secure Agents',
            url: `${SITE_ORIGIN}${BASE_URL}/`,
          },
          author: {
            '@type': 'Person',
            name: 'Renato Mignone',
            url: 'https://github.com/RenatoMignone',
          },
          publisher: {
            '@type': 'Organization',
            name: 'From LLMs to Secure Agents Project',
            url: GITHUB_REPO,
          },
          mainEntity: {
            '@type': 'ItemList',
            numberOfItems: s.chapters.length,
            itemListElement: s.chapters.map((c, idx) => ({
              '@type': 'ListItem',
              position: idx + 1,
              name: c.title,
              url: c.canonicalUrl,
              description: c.summary,
            })),
          },
        },
        {
          '@type': 'BreadcrumbList',
          '@id': `${s.canonicalUrl}#breadcrumb`,
          itemListElement: [
            {
              '@type': 'ListItem',
              position: 1,
              name: 'Handbook',
              item: `${SITE_ORIGIN}${BASE_URL}/`,
            },
            {
              '@type': 'ListItem',
              position: 2,
              name: s.label,
              item: s.canonicalUrl,
            },
          ],
        },
      ],
    };

    const sectionFm = {
      title: s.label,
      description: s.plan?.purpose || `Engineering module covering ${s.label.toLowerCase()} in autonomous AI systems.`,
      summary: s.plan?.purpose || `Complete curriculum units for ${s.label.toLowerCase()}.`,
      pass: s.pass,
      reviewed_label: new Intl.DateTimeFormat('en-GB', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        timeZone: 'UTC',
      }).format(new Date()),
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
      head: [
        {
          tag: 'script',
          attrs: { type: 'application/ld+json' },
          content: JSON.stringify(sectionJsonLd),
        },
        {
          tag: 'link',
          attrs: { rel: 'canonical', href: s.canonicalUrl },
        },
        {
          tag: 'link',
          attrs: { rel: 'alternate', type: 'text/markdown', href: s.markdownUrl, title: `${s.label} (Markdown)` },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:title', content: `${s.label} | From LLMs to Secure Agents` },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:description', content: s.plan?.purpose || `Engineering module covering ${s.label.toLowerCase()}.` },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:type', content: 'website' },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:url', content: s.canonicalUrl },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:site_name', content: 'From LLMs to Secure Agents' },
        },
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:card', content: 'summary_large_image' },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:title', content: `${s.label} | From LLMs to Secure Agents` },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:description', content: s.plan?.purpose || `Engineering module covering ${s.label.toLowerCase()}.` },
        },
        {
          tag: 'meta',
          attrs: { name: 'twitter:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'keywords',
            content:
              s.sectionKey === '00-prerequisites'
                ? 'AI agent prerequisites, data flow vs control flow, trust boundaries, requests events state, identity least privilege, agent security fundamentals'
                : s.sectionKey === '01-agent-foundations'
                  ? 'AI agent foundations, agent loop, ReAct cycle, workflows vs agents, agent autonomy levels, run lifecycle, termination guarantees'
                  : s.sectionKey === '02-agent-architectures'
                    ? 'agent architectures, single-agent loops, prompt chaining, plan and execute, reflection, evaluator optimizer, state machines, supervisor agent, swarm handoffs, architecture trade-offs'
                    : s.sectionKey === '03-building-blocks'
                      ? 'agent building blocks, model routing, context engineering, memory systems, agentic RAG, tool calling, execution sandboxes, observability, agent tracing'
                      : `AI agent, LLM security, ${s.label}, agentic system architecture, prompt injection, runtime loop`,
          },
        },
      ],
    };

    let sectionContent = `---
${yaml.stringify(sectionFm)}---

<div class="section-overview not-content">
<a href="${firstChapter.route}" class="section-start-link">
<span>Start with</span>
<strong>${chapterSequenceLabel(firstChapter)}. ${escapeHtml(firstChapter.title)} <span aria-hidden="true">→</span></strong>
</a>
</div>

<div class="section-essentials not-content">
<div>
<strong>Before you begin</strong>
<p>${formattedSectionPrereqs}</p>
</div>
<div>
<strong>By the end</strong>
<p>${formattedSectionOutcomes}</p>
</div>
</div>

## Chapters

<div class="section-chapter-index not-content">
${chapterGroups
  .map(
    (group, groupIndex) => `<section class="chapter-index-group" aria-labelledby="chapter-index-group-${sIdx + 1}-${groupIndex + 1}">
${chapterGroups.length > 1 ? `<h3 id="chapter-index-group-${sIdx + 1}-${groupIndex + 1}">${escapeHtml(group.label)}</h3>` : ''}
<ol class="section-chapter-list">
${group.chapters
  .map(
    (c) => `<li>
<a href="${c.route}">
<span class="chapter-index-number">${chapterSequenceLabel(c)}</span>
<span class="chapter-index-copy">
<strong>${escapeHtml(c.title)}</strong>
<span>${escapeHtml(c.summary)}</span>
</span>
${c.learning_path === 'deep_dive' || c.learning_path === 'deep-dive' ? '<span class="chapter-index-type">Deep dive</span>\n' : ''}<span class="chapter-index-arrow" aria-hidden="true">→</span>
</a>
</li>`
  )
  .join('\n')}
</ol>
</section>`
  )
  .join('\n')}
</div>

<div class="unit-pagination not-content">
${
  prevSection
    ? `  <a href="${prevSection.route}" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Previous section</span>
    <span class="pagination-name">${prevSection.label}</span>
  </a>\n`
    : `  <a href="${BASE_URL}/" class="pagination-link pagination-prev">
    <span class="pagination-sub">← Guide home</span>
    <span class="pagination-name">From LLMs to Secure Agents</span>
  </a>\n`
}
${
  nextSection
    ? `  <a href="${nextSection.route}" class="pagination-link pagination-next">
    <span class="pagination-sub">Next section →</span>
    <span class="pagination-name">${nextSection.label}</span>
  </a>\n`
    : `  <div class="pagination-link pagination-next pagination-end">
    <span class="pagination-sub">Published path</span>
    <span class="pagination-name">You reached the current end</span>
  </div>\n`
}
</div>
`;

    fs.writeFileSync(sectionDocPath, sectionContent, 'utf8');

    // Section clean markdown
    const sectionCleanMarkdown = `---
title: ${JSON.stringify(s.label)}
id: ${JSON.stringify(s.routeDir)}
pass: ${JSON.stringify(s.pass)}
canonical_url: ${JSON.stringify(s.canonicalUrl)}
total_chapters: ${s.chapters.length}
---

# ${s.label}

> **Section Overview:** ${s.plan?.purpose || `Engineering module covering ${s.label.toLowerCase()}.`}
> **Pass:** ${s.pass} · **Published chapters:** ${s.chapters.length}

## Learning Outcomes
${s.plan?.outcomes || ''}

## Published chapters
${s.chapters.map((c) => `- [${c.title}](${c.canonicalUrl}) - ${c.summary}`).join('\n')}
`;
    fs.writeFileSync(sectionRawMarkdownPath, sectionCleanMarkdown, 'utf8');
  }

  console.log(`✓ Successfully generated ${sections.length} section hub documentation pages.`);

  // 6. Generate Dynamic Sidebar Configuration
  console.log('📑 Generating dynamic sidebar configuration...');
  const sidebarSections = [];

  for (const [sectionIndex, s] of sections.entries()) {
    const chapterGroups = groupSectionChapters(s);
    sidebarSections.push({
      label: `${sectionSequenceLabel(sectionIndex)} ${s.label}`,
      collapsed: true,
      items: [
        {
          label: 'Overview and learning path',
          link: `/${s.routeDir}/`,
        },
        ...(chapterGroups.length === 1
          ? chapterGroups[0].chapters.map((chapter) => ({
              label: `${chapterSequenceLabel(chapter)} ${chapter.title}`,
              link: chapter.route.replace(BASE_URL, ''),
            }))
          : chapterGroups.map((group) => ({
              label: group.label,
              collapsed: true,
              items: group.chapters.map((chapter) => ({
                label: `${chapterSequenceLabel(chapter)} ${chapter.title}`,
                link: chapter.route.replace(BASE_URL, ''),
              })),
            }))),
      ],
    });
  }

  const finalSidebar = [
    {
      label: 'Guide map',
      link: '/curriculum/',
    },
    ...sidebarSections,
  ];

  fs.writeFileSync(
    path.join(GENERATED_DIR, 'sidebar.json'),
    JSON.stringify(finalSidebar, null, 2),
    'utf8'
  );

  // 6b. Generate Dedicated Index Page (/curriculum/index.mdx)
  console.log('📑 Generating dedicated index page...');
  const curriculumDir = path.join(DOCS_DIR, 'curriculum');
  fs.mkdirSync(curriculumDir, { recursive: true });

  const curriculumFm = {
    title: 'Guide map',
    description: 'A structured map of the published learning path from agent foundations to secure agent design.',
    section_label: 'Guide map',
    head: [
      {
        tag: 'title',
        content: 'Guide map | From LLMs to Secure Agents',
      },
      {
        tag: 'meta',
        attrs: { property: 'og:title', content: 'Guide map | From LLMs to Secure Agents' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:description', content: 'A structured map of the published learning path from agent foundations to secure agent design.' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:type', content: 'website' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:url', content: `${SITE_ORIGIN}${BASE_URL}/curriculum/` },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
      },
    ],
  };

  const curriculumContent = `---
${yaml.stringify(curriculumFm)}---

<div class="guide-index-intro not-content">
  <p>Choose a section, then open a chapter. The full published path is visible below.</p>
  <a href="${chapters[0].route}">Start at the beginning <span aria-hidden="true">→</span></a>
</div>

<h2 class="sr-only">Published sections</h2>

<nav class="guide-index not-content" aria-label="Published guide sections">
${sections
  .map((s, sectionIndex) => {
    const groups = groupSectionChapters(s);
    return `<section class="guide-index-section" aria-labelledby="guide-index-section-${sectionIndex + 1}">
<header class="guide-index-section-header">
<div class="guide-index-section-copy">
<h3 id="guide-index-section-${sectionIndex + 1}"><a href="${s.route}">${escapeHtml(s.label)}</a></h3>
<p>${renderInlineMarkdown(s.plan?.purpose || `Core architectural concepts and specifications for ${s.label.toLowerCase()}.`)}</p>
</div>
</header>
<div class="guide-index-chapters">
${groups
  .map(
    (group) => `<div class="guide-index-group">
${groups.length > 1 ? `<h4>${escapeHtml(group.label)}</h4>\n` : ''}<ol>
${group.chapters
  .map(
    (chapter) => `<li>
<a href="${chapter.route}">
<span>${chapterSequenceLabel(chapter)}</span>
<strong>${escapeHtml(chapter.title)}</strong>
<span aria-hidden="true">→</span>
</a>
</li>`
  )
  .join('\n')}
</ol>
</div>`
  )
  .join('\n')}
</div>
</section>`;
  })
  .join('\n')}
</nav>
`;

  fs.writeFileSync(path.join(curriculumDir, 'index.mdx'), curriculumContent, 'utf8');

  // 7. Generate Calm Editorial Homepage (index.mdx) with Stacked Schema
  console.log('🏠 Generating calm editorial homepage with full SEO/AEO/GEO metadata...');
  const entryChapter = chapters[0];
  const firstChapterRoute = entryChapter ? entryChapter.route : `${BASE_URL}/prerequisites/01-reader-contract-and-system-map/`;
  const latestChapter = chapters.at(-1);
  const heroImage = responsiveImages.get('repo-images/project-purpose.png');

  const homepageJsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebSite',
        '@id': `${SITE_ORIGIN}${BASE_URL}/#website`,
        url: `${SITE_ORIGIN}${BASE_URL}/`,
        name: 'From LLMs to Secure Agents',
        description: 'A comprehensive, sequential, source-grounded guide to agentic AI architecture and security.',
        inLanguage: 'en-US',
        author: {
          '@type': 'Person',
          name: 'Renato Mignone',
          url: 'https://github.com/RenatoMignone',
        },
        publisher: {
          '@type': 'Organization',
          name: 'From LLMs to Secure Agents Project',
          url: GITHUB_REPO,
        },
      },
      {
        '@type': 'Book',
        '@id': `${SITE_ORIGIN}${BASE_URL}/#handbook`,
        name: 'From LLMs to Secure Agents',
        description: 'A comprehensive guide covering agentic AI foundations, architecture, runtime systems, threat modeling, defensive controls, and assurance.',
        bookFormat: 'https://schema.org/EBook',
        author: {
          '@type': 'Person',
          name: 'Renato Mignone',
          url: 'https://github.com/RenatoMignone',
        },
        provider: {
          '@type': 'Organization',
          name: 'From LLMs to Secure Agents Project',
          url: GITHUB_REPO,
        },
        hasPart: [
          ...sections.map((s) => ({
            '@type': 'CollectionPage',
            name: s.label,
            description: s.plan?.purpose || `Engineering module covering ${s.label.toLowerCase()}.`,
            url: s.canonicalUrl,
          })),
          ...guideIndex.map((u) => ({
            '@type': 'LearningResource',
            name: u.title,
            description: u.summary,
            url: u.html_url,
          })),
        ],
      },
    ],
  };

  const homepageFm = {
    title: 'From LLMs to Secure Agents',
    description: 'A comprehensive, sequential, source-grounded guide to agentic AI architecture and security by Renato Mignone.',
    template: 'splash',
    tableOfContents: false,
    prev: false,
    next: false,
    head: [
      {
        tag: 'title',
        content: 'From LLMs to Secure Agents',
      },
      {
        tag: 'script',
        attrs: { type: 'application/ld+json' },
        content: JSON.stringify(homepageJsonLd),
      },
      {
        tag: 'link',
        attrs: { rel: 'canonical', href: `${SITE_ORIGIN}${BASE_URL}/` },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:title', content: 'From LLMs to Secure Agents | Comprehensive Guide' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:description', content: 'A comprehensive, sequential guide to agentic AI architecture, operation, risks, and defenses. By Renato Mignone.' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:type', content: 'website' },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:url', content: `${SITE_ORIGIN}${BASE_URL}/` },
      },
      {
        tag: 'meta',
        attrs: { property: 'og:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
      },
      {
        tag: 'meta',
        attrs: { name: 'twitter:card', content: 'summary_large_image' },
      },
      {
        tag: 'meta',
        attrs: { name: 'twitter:title', content: 'From LLMs to Secure Agents' },
      },
      {
        tag: 'meta',
        attrs: { name: 'twitter:description', content: 'A comprehensive, sequential guide to agentic AI architecture, operation, risks, and defenses. By Renato Mignone.' },
      },
      {
        tag: 'meta',
        attrs: { name: 'twitter:image', content: `${SITE_ORIGIN}${BASE_URL}/assets/images/repo-images/banner.png` },
      },
      {
        tag: 'meta',
        attrs: { name: 'author', content: 'Renato Mignone' },
      },
      {
        tag: 'meta',
        attrs: { name: 'keywords', content: 'Renato Mignone, AI agent security, LLM agents architecture, prompt injection defense, agent runtime sandbox, threat modeling autonomous AI' },
      },
    ],
  };

  const homepageContent = `---
${yaml.stringify(homepageFm)}---

import HomepageHero from '../../components/HomepageHero.astro';
import HomepageIdea from '../../components/HomepageIdea.astro';
import HomepageFooter from '../../components/HomepageFooter.astro';

<HomepageHero firstChapterRoute="${firstChapterRoute}" baseUrl="${BASE_URL}" image={${JSON.stringify(heroImage)}} />

<HomepageIdea />

<HomepageFooter githubUrl="${GITHUB_REPO}" baseUrl="${BASE_URL}" />
`;

  fs.writeFileSync(path.join(DOCS_DIR, 'index.mdx'), homepageContent, 'utf8');

  const notFoundContent = `---
title: Page not found
description: The requested guide page does not exist or has moved.
template: splash
pagefind: false
head:
  - tag: meta
    attrs:
      name: robots
      content: noindex, nofollow
---

<span id="_top"></span>

# This page is not part of the published guide

The address may be outdated, or the chapter may still be on the roadmap. Use the published learning path or search to find the closest topic.

<div class="not-found-actions">
  <a class="btn-hero-primary" href="${BASE_URL}/">Return to the guide</a>
  <a class="btn-hero-secondary" href="${firstChapterRoute}">Start from chapter 1</a>
</div>
`;
  fs.writeFileSync(path.join(DOCS_DIR, '404.md'), notFoundContent, 'utf8');

  // 8. Generate guide-index.json
  console.log('🤖 Generating machine-readable guide-index.json...');
  fs.writeFileSync(
    path.join(PUBLIC_DIR, 'guide-index.json'),
    JSON.stringify(
      {
        title: 'From LLMs to Secure Agents: Engineering Guide Index',
        description: 'Machine-readable index of published sections, chapters, learning objectives, source records, and canonical links.',
        author: 'Renato Mignone',
        author_url: 'https://github.com/RenatoMignone',
        version: '3.0.0',
        origin: SITE_ORIGIN,
        base_path: BASE_URL,
        last_updated: new Date().toISOString().split('T')[0],
        total_published_sections: sections.length,
        total_published_chapters: guideIndex.length,
        curriculum_passes: [
          { pass_id: 0, title: 'Prerequisites', focus: 'Distributed boundaries and systems foundations' },
          { pass_id: 1, title: 'Understand the Complete System', focus: 'Agent loop, context, memory, tools, and runtimes' },
          { pass_id: 2, title: 'Secure the System', focus: 'Threat modeling, isolation, and security assurance' },
        ],
        sections: sections.map((s) => ({
          id: s.routeDir,
          label: s.label,
          pass: s.pass,
          html_url: s.canonicalUrl,
          markdown_url: s.markdownUrl,
          purpose: s.plan?.purpose || '',
          total_published_chapters: s.chapters.length,
          chapters: s.chapters.map((c) => c.reader_id),
        })),
        chapters: guideIndex,
      },
      null,
      2
    ),
    'utf8'
  );

  // 9. Generate 2026 llms.txt & llms-full.txt
  console.log('📄 Generating 2026 llms.txt & llms-full.txt...');
  const llmsTxtContent = `# From LLMs to Secure Agents

> A comprehensive, visual and source-grounded guide to agentic AI architecture and security.

- **Author:** Renato Mignone (https://github.com/RenatoMignone)
- **Site Origin:** ${SITE_ORIGIN}${BASE_URL}/
- **Structured Index API:** ${SITE_ORIGIN}${BASE_URL}/guide-index.json
- **Full Text AI Dump:** ${SITE_ORIGIN}${BASE_URL}/llms-full.txt
- **Source Repository:** ${GITHUB_REPO}
- **Publication status:** Updated incrementally as chapters complete review.
- **Current publication:** ${chapters.length} chapters across ${sections.length} sections. The latest chapter is [${latestChapter?.title || 'the opening chapter'}](${latestChapter?.canonicalUrl || `${SITE_ORIGIN}${firstChapterRoute}`}).

## Executive Summary & Core Definitions (AEO Grounding)

- **What is an AI Agent?** In this guide, an AI agent is a software system in which a model helps select actions inside a runtime loop. The runtime supplies context, tools, state, policy checks, and termination rules.
- **Workflows vs Agents:** Workflows execute predefined, hardcoded DAGs where code directs control flow. Agents use model outputs to decide dynamic control paths and step-by-step tool dispatches.
- **The 5-Step Agent Loop:** (1) Context Construction, (2) Model Inference, (3) Tool / Action Dispatch, (4) Environment Execution, (5) State & Memory Update.
- **Trust Boundaries:** The separation line between untrusted data (user input, web pages, tool outputs) and the privileged execution plane (tool credentials, system prompts, host environment).
- **Core Security Threat (Pass 2):** Indirect Prompt Injection, where untrusted retrieved data hijacks model control flow and weaponizes authorized tool access.

## Curriculum Architecture (Two-Pass Model)

1. **Pass 1: Understand the Complete System**
   - **Prerequisites:** [Section overview](${SITE_ORIGIN}${BASE_URL}/prerequisites/) · Core distributed systems and software boundaries (Data vs Control Flow, Trust Boundaries, Requests/Events/State, Identity & Least Privilege).
   - **Agent Foundations:** [Section overview](${SITE_ORIGIN}${BASE_URL}/foundations/) · Model-directed control loops, the 5-step agent loop, workflows vs agents, goals and autonomy, run lifecycles, and termination conditions.
   - **Agent Architectures:** [Section overview](${SITE_ORIGIN}${BASE_URL}/architectures/) · Single loops, plan-and-execute, reflection, state machines, supervisor and multi-agent topologies.
   - **Building Blocks:** [Section overview](${SITE_ORIGIN}${BASE_URL}/building-blocks/) · Context construction, short-term and persistent memory, agentic RAG, tools and function calling, execution sandboxes, observability.
   - **Frameworks & Protocols (Roadmap):** Model Context Protocol (MCP), agent-to-agent protocols, human-agent interaction.
   - **End-to-End Workflows (Roadmap):** Reference production architectures.

2. **Pass 2: Secure the System (Roadmap)**
   - **Threat Model:** Planned coverage of entry points, adversaries, assets, and agent attack paths.
   - **Security by Component:** Indirect prompt injection defenses, credential scoping, memory isolation, execution sandboxing.
   - **Secure Reference Architectures:** Zero-trust agent gateways and dual-model verification.
   - **Testing & Assurance:** Automated red teaming, prompt fuzzing, invariant testing.
   - **Open Research Questions:** Formal loop verification and verifiable provenance.

## Published chapters

${guideIndex
  .map(
    (u) => `### [${u.title}](${u.html_url})
- **Summary:** ${u.summary}
- **Section:** [${u.section_label}](${SITE_ORIGIN}${BASE_URL}/${u.section_id}/)
- **Clean Markdown URL:** ${u.markdown_url}
- **Learning Objectives:**
${u.learning_objectives.map((o) => `  * ${o}`).join('\n')}
- **Verified Primary Sources:** ${u.source_records.map((s) => `[${s.title}](${s.canonical_url})`).join(', ')}
`
  )
  .join('\n')}
`;

  fs.writeFileSync(path.join(PUBLIC_DIR, 'llms.txt'), llmsTxtContent, 'utf8');

  // Generate llms-full.txt for comprehensive single-file retrieval
  let llmsFullContent = llmsTxtContent + '\n\n---\n# COMPLETE CANONICAL HANDBOOK TEXT\n\n';
  for (const ch of chapters) {
    llmsFullContent += `\n\n================================================================================\n`;
    llmsFullContent += `CHAPTER: ${ch.title}\n`;
    llmsFullContent += `URL: ${ch.canonicalUrl}\n`;
    llmsFullContent += `SUMMARY: ${ch.summary}\n`;
    llmsFullContent += `================================================================================\n\n`;
    llmsFullContent += rewriteChapterLinks(ch.body.trim(), ch.relPath, chapters) + '\n';
  }
  fs.writeFileSync(path.join(PUBLIC_DIR, 'llms-full.txt'), llmsFullContent, 'utf8');

  // 10. Generate 2026 robots.txt
  console.log('🤖 Generating 2026 AI-friendly robots.txt...');
  const robotsTxtContent = `User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Cohere-ai
Allow: /

Sitemap: ${SITE_ORIGIN}${BASE_URL}/sitemap-index.xml
`;
  fs.writeFileSync(path.join(PUBLIC_DIR, 'robots.txt'), robotsTxtContent, 'utf8');

  // 11. Generate .nojekyll file to bypass Jekyll on GitHub Pages
  fs.writeFileSync(path.join(PUBLIC_DIR, '.nojekyll'), '', 'utf8');

  console.log('🎉 Site content generation finished cleanly!');
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await generateAll();
}
