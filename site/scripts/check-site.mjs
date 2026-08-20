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
checkFileExists('404.html', '404 page');
checkFileExists('robots.txt', 'robots.txt');
checkFileExists('sitemap-index.xml', 'sitemap index');
checkFileExists('llms.txt', 'llms.txt');
checkFileExists('llms-full.txt', 'llms-full.txt');
checkFileExists('guide-index.json', 'guide-index.json');
checkFileExists('pagefind/pagefind.js', 'Pagefind search index');

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
    const index = JSON.parse(raw);
    if (!index.units || !Array.isArray(index.units) || index.units.length === 0) {
      errors.push('guide-index.json does not contain units array');
    } else {
      console.log(`  guide-index.json valid with ${index.units.length} published units.`);
      for (const u of index.units) {
        if (!u.unit_id || !u.title || !u.html_url || !u.markdown_url) {
          errors.push(`guide-index.json unit missing required fields: ${JSON.stringify(u)}`);
        }
      }
    }
    if (!index.sections || !Array.isArray(index.sections) || index.sections.length === 0) {
      errors.push('guide-index.json does not contain sections array');
    } else {
      console.log(`  guide-index.json valid with ${index.sections.length} published sections.`);
      for (const s of index.sections) {
        if (!s.section_key || !s.label || !s.html_url || !s.markdown_url) {
          errors.push(`guide-index.json section missing required fields: ${JSON.stringify(s)}`);
        }
      }
    }
  } catch (err) {
    errors.push(`Invalid guide-index.json JSON format: ${err.message}`);
  }
}

// 5. Scan all HTML files for broken links and images
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

      // Check image references
      const imgMatches = content.matchAll(/<img[^>]+src=["']([^"']+)["']/g);
      for (const m of imgMatches) {
        const src = m[1];
        if (src.startsWith('data:') || src.startsWith('http://') || src.startsWith('https://')) {
          continue;
        }
        // Local asset
        let cleanSrc = src;
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

      // Check stylesheet references
      const linkMatches = content.matchAll(/<link[^>]+href=["']([^"']+)["'][^>]*>/g);
      for (const m of linkMatches) {
        const fullTag = m[0];
        const href = m[1];
        if (fullTag.includes('rel="stylesheet"')) {
          let cleanHref = href;
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
