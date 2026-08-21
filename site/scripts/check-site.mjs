import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, '..');
const DIST_DIR = path.join(SITE_ROOT, 'dist');

const BASE_URL = '/From-LLMs-to-Secure-Agents';
const SITE_ORIGIN = 'https://renatomignone.github.io';

console.log('🔍 Running site validation checks...');

let errors = [];
const htmlIdCache = new Map();

function stripQueryAndFragment(value) {
  return value.split(/[?#]/, 1)[0];
}

function htmlFileForSitePath(sitePath) {
  let cleanPath = stripQueryAndFragment(sitePath);
  if (cleanPath.startsWith(BASE_URL)) cleanPath = cleanPath.slice(BASE_URL.length);
  cleanPath = cleanPath.replace(/^\/+/, '');
  try {
    cleanPath = decodeURIComponent(cleanPath);
  } catch {
    return null;
  }
  if (!cleanPath || cleanPath.endsWith('/')) cleanPath += 'index.html';
  return path.join(DIST_DIR, cleanPath);
}

function idsForHtmlFile(htmlPath) {
  if (htmlIdCache.has(htmlPath)) return htmlIdCache.get(htmlPath);
  const content = fs.readFileSync(htmlPath, 'utf8');
  const ids = new Set();
  for (const match of content.matchAll(/\s(?:id|name)=["']([^"']+)["']/g)) {
    ids.add(match[1]);
  }
  htmlIdCache.set(htmlPath, ids);
  return ids;
}

function resolveInternalHref(href, sourceHtmlPath) {
  const normalizedHref = href.replaceAll('&amp;', '&');
  if (/^(?:mailto|tel|javascript|data):/i.test(normalizedHref)) return null;

  let pathname;
  let fragment = '';
  if (/^https?:\/\//i.test(normalizedHref)) {
    const url = new URL(normalizedHref);
    if (url.origin !== SITE_ORIGIN || !url.pathname.startsWith(BASE_URL)) return null;
    pathname = url.pathname;
    fragment = url.hash.slice(1);
  } else if (normalizedHref.startsWith('/')) {
    pathname = normalizedHref;
    fragment = normalizedHref.split('#')[1] || '';
  } else {
    const sourceRoute = `/${path.relative(DIST_DIR, sourceHtmlPath).split(path.sep).join('/')}`
      .replace(/index\.html$/, '');
    const url = new URL(normalizedHref, `${SITE_ORIGIN}${BASE_URL}${sourceRoute}`);
    pathname = url.pathname;
    fragment = url.hash.slice(1);
  }

  if (!pathname.startsWith(BASE_URL)) return null;
  return { targetPath: htmlFileForSitePath(pathname), fragment };
}

function checkFileExists(relPath, desc) {
  const fullPath = path.join(DIST_DIR, relPath);
  if (!fs.existsSync(fullPath)) {
    errors.push(`Missing ${desc}: ${relPath}`);
    return false;
  }
  return true;
}

// 1. Check core static outputs
console.log('  Checking critical endpoints...');
checkFileExists('index.html', 'Homepage HTML');
if (checkFileExists('404.html', '404 page')) {
  const notFoundHtml = fs.readFileSync(path.join(DIST_DIR, '404.html'), 'utf8');
  if (!notFoundHtml.includes('This page is not part of the published guide')) {
    errors.push('404 page does not contain the project-specific recovery message');
  }
}
checkFileExists('robots.txt', 'robots.txt');
checkFileExists('.nojekyll', '.nojekyll (GitHub Pages Jekyll bypass)');
checkFileExists('sitemap-index.xml', 'sitemap-index.xml (sitemap index)');
checkFileExists('sitemap-0.xml', 'sitemap-0.xml (child sitemap)');
checkFileExists('llms.txt', 'llms.txt');
checkFileExists('llms-full.txt', 'llms-full.txt');
checkFileExists('guide-index.json', 'guide-index.json');
checkFileExists('pagefind/pagefind.js', 'Pagefind search index');

const responsiveAssetDir = path.join(DIST_DIR, 'assets', 'images');
let responsiveVariantCount = 0;
function checkResponsiveAssetBudgets(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) checkResponsiveAssetBudgets(fullPath);
    else if (entry.name.endsWith('.webp') && /-\d+w\.webp$/.test(entry.name)) {
      responsiveVariantCount += 1;
      const size = fs.statSync(fullPath).size;
      if (size > 250 * 1024) {
        errors.push(`Responsive image exceeds 250 KiB budget: ${path.relative(DIST_DIR, fullPath)} (${Math.ceil(size / 1024)} KiB)`);
      }
    }
  }
}
checkResponsiveAssetBudgets(responsiveAssetDir);
if (responsiveVariantCount === 0) {
  errors.push('No responsive WebP image variants were generated');
} else {
  console.log(`  Responsive image budget valid for ${responsiveVariantCount} WebP variants.`);
}

if (fs.existsSync(path.join(DIST_DIR, 'sitemap-0.xml'))) {
  const sitemap = fs.readFileSync(path.join(DIST_DIR, 'sitemap-0.xml'), 'utf8');
  const urls = [...sitemap.matchAll(/<url>([\s\S]*?)<\/url>/g)];
  if (urls.length === 0) {
    errors.push('sitemap-0.xml does not contain any URLs');
  }
  for (const [, entry] of urls) {
    if (!entry.includes('<lastmod>')) {
      errors.push(`Sitemap URL is missing lastmod: ${entry.match(/<loc>(.*?)<\/loc>/)?.[1] || 'unknown URL'}`);
    }
  }
}

if (fs.existsSync(path.join(DIST_DIR, 'index.html'))) {
  const homepage = fs.readFileSync(path.join(DIST_DIR, 'index.html'), 'utf8');
  if (!homepage.includes('id="learning-path-title"') || !homepage.includes('data-reading-link')) {
    errors.push('Homepage is missing the learning-path map or Continue Reading hooks');
  }
  if (!/project-purpose-[^"']+\.webp/.test(homepage) || !homepage.includes('fetchpriority="high"')) {
    errors.push('Homepage hero is missing responsive WebP markup or high fetch priority');
  }
}

const generatedCss = fs.existsSync(path.join(DIST_DIR, '_astro'))
  ? fs.readdirSync(path.join(DIST_DIR, '_astro'))
      .filter((name) => name.endsWith('.css'))
      .map((name) => fs.readFileSync(path.join(DIST_DIR, '_astro', name), 'utf8'))
      .join('\n')
  : '';
if (!generatedCss.includes(':focus-visible') || !generatedCss.includes('prefers-reduced-motion')) {
  errors.push('Generated CSS is missing focus-visible or reduced-motion accessibility rules');
}

// Check published Section Hub endpoints
console.log('  Checking section hub endpoints...');
checkFileExists('prerequisites/index.html', 'Prerequisites section hub');
checkFileExists('foundations/index.html', 'Foundations section hub');
checkFileExists('architectures/index.html', 'Architectures section hub');
checkFileExists('building-blocks/index.html', 'Building blocks section hub');

// 2. Validate robots.txt
if (fs.existsSync(path.join(DIST_DIR, 'robots.txt'))) {
  const robots = fs.readFileSync(path.join(DIST_DIR, 'robots.txt'), 'utf8');
  if (!robots.includes('Sitemap: https://renatomignone.github.io/From-LLMs-to-Secure-Agents/')) {
    errors.push('robots.txt does not contain full sitemap URL with base path');
  }
  if (!robots.includes('User-agent: *')) {
    errors.push('robots.txt does not configure User-agent: *');
  }
  if (!robots.includes('User-agent: OAI-SearchBot')) {
    errors.push('robots.txt does not explicitly configure OAI-SearchBot');
  }
  if (!robots.includes('User-agent: PerplexityBot')) {
    errors.push('robots.txt does not explicitly configure PerplexityBot');
  }
}

// 3. Validate llms.txt and llms-full.txt
if (fs.existsSync(path.join(DIST_DIR, 'llms.txt'))) {
  const llms = fs.readFileSync(path.join(DIST_DIR, 'llms.txt'), 'utf8');
  if (!llms.includes('# From LLMs to Secure Agents')) {
    errors.push('llms.txt is missing main title');
  }
  if (!llms.includes('/From-LLMs-to-Secure-Agents/guide-index.json')) {
    errors.push('llms.txt does not link to guide-index.json');
  }
  if (/\bP[0-2]-\d{2}/.test(llms)) {
    errors.push('llms.txt exposes internal operational unit identifiers');
  }
}

if (fs.existsSync(path.join(DIST_DIR, 'llms-full.txt'))) {
  const llmsFull = fs.readFileSync(path.join(DIST_DIR, 'llms-full.txt'), 'utf8');
  if (!llmsFull.includes('COMPLETE CANONICAL HANDBOOK TEXT')) {
    errors.push('llms-full.txt is missing canonical text header');
  }
}

// 4. Validate guide-index.json
if (fs.existsSync(path.join(DIST_DIR, 'guide-index.json'))) {
  try {
    const raw = fs.readFileSync(path.join(DIST_DIR, 'guide-index.json'), 'utf8');
    if (/\bP[0-2]-\d{2}/.test(raw)) {
      errors.push('guide-index.json exposes internal operational unit identifiers');
    }
    const index = JSON.parse(raw);
    if (!index.chapters || !Array.isArray(index.chapters) || index.chapters.length === 0) {
      errors.push('guide-index.json does not contain chapters array');
    } else {
      console.log(`  guide-index.json valid with ${index.chapters.length} published chapters.`);
      for (const chapter of index.chapters) {
        if (!chapter.id || !chapter.title || !chapter.html_url || !chapter.markdown_url) {
          errors.push(`guide-index.json chapter missing required fields: ${JSON.stringify(chapter)}`);
        }
      }
    }
    if (!index.sections || !Array.isArray(index.sections) || index.sections.length === 0) {
      errors.push('guide-index.json does not contain sections array');
    } else {
      console.log(`  guide-index.json valid with ${index.sections.length} published sections.`);
      for (const s of index.sections) {
        if (!s.id || !s.label || !s.html_url || !s.markdown_url) {
          errors.push(`guide-index.json section missing required fields: ${JSON.stringify(s)}`);
        }
      }
    }
  } catch (err) {
    errors.push(`Invalid guide-index.json JSON format: ${err.message}`);
  }
}

// 5. Scan all HTML files for broken links, anchors, and images
console.log('  Scanning HTML files for link & image validity...');
function scanHtml(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanHtml(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      const content = fs.readFileSync(fullPath, 'utf8');
      const relFile = path.relative(DIST_DIR, fullPath);

      if (/\bP[0-2]-\d{2}/.test(content)) {
        errors.push(`Operational unit identifier leaked into public HTML: ${relFile}`);
      }

      for (const imageTag of content.matchAll(/<img\b[^>]*>/gi)) {
        if (!/\balt=["'][^"']*["']/.test(imageTag[0])) {
          errors.push(`Image is missing alt text in ${relFile}: ${imageTag[0].slice(0, 120)}`);
        }
      }

      // Check navigational links and same-page fragments.
      const anchorMatches = content.matchAll(/<a\b[^>]*\bhref=["']([^"']+)["'][^>]*>/gi);
      for (const match of anchorMatches) {
        const href = match[1];
        let resolved;
        try {
          resolved = resolveInternalHref(href, fullPath);
        } catch (err) {
          errors.push(`Invalid link in ${relFile}: ${href} (${err.message})`);
          continue;
        }
        if (!resolved) continue;
        const { targetPath, fragment } = resolved;
        if (!targetPath || !fs.existsSync(targetPath)) {
          errors.push(`Broken link in ${relFile}: ${href}`);
          continue;
        }
        if (fragment) {
          let decodedFragment = fragment;
          try {
            decodedFragment = decodeURIComponent(fragment);
          } catch {
            // Leave the original fragment for a useful validation error.
          }
          if (!idsForHtmlFile(targetPath).has(decodedFragment)) {
            errors.push(`Broken anchor in ${relFile}: ${href}`);
          }
        }
      }

      // Check image references
      const imgMatches = content.matchAll(/<img[^>]+src=["']([^"']+)["']/g);
      for (const m of imgMatches) {
        const src = m[1];
        if (src.startsWith('data:') || src.startsWith('http://') || src.startsWith('https://')) {
          continue;
        }
        // Local asset
        let cleanSrc = stripQueryAndFragment(src);
        if (cleanSrc.startsWith(BASE_URL)) {
          cleanSrc = cleanSrc.substring(BASE_URL.length);
        }
        if (cleanSrc.startsWith('/')) {
          cleanSrc = cleanSrc.substring(1);
        }
        const assetPath = path.join(DIST_DIR, cleanSrc);
        if (!fs.existsSync(assetPath)) {
          errors.push(`Broken image in ${relFile}: ${src} (resolved to ${cleanSrc})`);
        }
      }

      for (const pictureMatch of content.matchAll(/<picture\b[^>]*class=["'][^"']*responsive-illustration[^"']*["'][^>]*>([\s\S]*?)<\/picture>/gi)) {
        const picture = pictureMatch[0];
        if (!/\bsrcset=["'][^"']+\.webp\s+\d+w/.test(picture)) {
          errors.push(`Responsive illustration is missing a WebP srcset in ${relFile}`);
        }
        if (!/<img\b[^>]*\bwidth=["']\d+["'][^>]*\bheight=["']\d+["'][^>]*\bloading=["']lazy["']/.test(picture)) {
          errors.push(`Responsive illustration is missing dimensions or lazy loading in ${relFile}`);
        }
      }

      for (const sourceMatch of content.matchAll(/\bsrcset=["']([^"']+)["']/g)) {
        for (const candidate of sourceMatch[1].split(',')) {
          const src = candidate.trim().split(/\s+/, 1)[0];
          if (!src || /^https?:|^data:/.test(src)) continue;
          let cleanSrc = stripQueryAndFragment(src);
          if (cleanSrc.startsWith(BASE_URL)) cleanSrc = cleanSrc.substring(BASE_URL.length);
          cleanSrc = cleanSrc.replace(/^\/+/, '');
          if (!fs.existsSync(path.join(DIST_DIR, cleanSrc))) {
            errors.push(`Broken responsive image candidate in ${relFile}: ${src}`);
          }
        }
      }

      // Check stylesheet references
      const linkMatches = content.matchAll(/<link[^>]+href=["']([^"']+)["'][^>]*>/g);
      for (const m of linkMatches) {
        const fullTag = m[0];
        const href = m[1];
        if (fullTag.includes('rel="stylesheet"')) {
          let cleanHref = stripQueryAndFragment(href);
          if (cleanHref.startsWith(BASE_URL)) {
            cleanHref = cleanHref.substring(BASE_URL.length);
          }
          if (cleanHref.startsWith('/')) {
            cleanHref = cleanHref.substring(1);
          }
          const cssPath = path.join(DIST_DIR, cleanHref);
          if (!fs.existsSync(cssPath)) {
            errors.push(`Broken stylesheet link in ${relFile}: ${href}`);
          }
        }
      }
    }
  }
}

scanHtml(DIST_DIR);

// 6. Markdown alternates must be portable and must not expose repository-relative links.
console.log('  Scanning Markdown alternates for unresolved local links...');
function scanMarkdown(dir) {
  if (!fs.existsSync(dir)) return;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanMarkdown(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      const content = fs.readFileSync(fullPath, 'utf8');
      if (/\bP[0-2]-\d{2}/.test(content)) {
        errors.push(`Operational unit identifier leaked into public Markdown: ${path.relative(DIST_DIR, fullPath)}`);
      }
      for (const match of content.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
        const href = match[1].trim();
        if (
          !href.startsWith('#') &&
          !href.startsWith('/') &&
          !/^[a-z][a-z\d+.-]*:/i.test(href)
        ) {
          errors.push(`Unresolved local link in ${path.relative(DIST_DIR, fullPath)}: ${href}`);
        }
      }
    }
  }
}

scanMarkdown(path.join(DIST_DIR, 'markdown'));

// Report results
if (errors.length > 0) {
  console.error(`❌ Validation failed with ${errors.length} error(s):`);
  for (const err of errors) {
    console.error(`  - ${err}`);
  }
  process.exit(1);
} else {
  console.log('✅ All site validation checks passed cleanly!');
}
