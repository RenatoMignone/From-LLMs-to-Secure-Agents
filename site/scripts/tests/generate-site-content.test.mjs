import assert from 'node:assert/strict';
import test from 'node:test';

import { rewriteChapterLinks } from '../generate-site-content.mjs';

const chapters = [
  {
    relPath: '00-prerequisites/01-reader-contract-and-system-map.md',
    route: '/From-LLMs-to-Secure-Agents/prerequisites/01-reader-contract-and-system-map/',
    sectionKey: '00-prerequisites',
    routeDir: 'prerequisites',
  },
  {
    relPath: '03-building-blocks/02-context-construction/01-context-sources-and-precedence.md',
    route: '/From-LLMs-to-Secure-Agents/building-blocks/01-context-sources-and-precedence/',
    sectionKey: '03-building-blocks',
    routeDir: 'building-blocks',
  },
];

test('rewrites links by canonical source path and preserves fragments', () => {
  const markdown = [
    '[published sibling](01-context-sources-and-precedence.md#why-this-matters)',
    '[published section](../../00-prerequisites/chapter-plan.md)',
    '[future plan](../09-execution-environments/chapter-plan.md)',
    '[example](../../../examples/demo.py)',
  ].join('\n');

  const result = rewriteChapterLinks(
    markdown,
    '03-building-blocks/02-context-construction/02-context-budgets.md',
    chapters
  );

  assert.match(
    result,
    /\/building-blocks\/01-context-sources-and-precedence\/#why-this-matters/
  );
  assert.match(result, /\/prerequisites\/\)/);
  assert.match(
    result,
    /github\.com\/RenatoMignone\/From-LLMs-to-Secure-Agents\/blob\/main\/knowledge\/03-building-blocks\/09-execution-environments\/chapter-plan\.md/
  );
  assert.match(
    result,
    /github\.com\/RenatoMignone\/From-LLMs-to-Secure-Agents\/blob\/main\/examples\/demo\.py/
  );
});
