import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import { discoverCanonicalChapters } from '../discover-content.mjs';

test('publishes only chapters whose status is exactly complete', () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'secure-agents-discovery-'));
  const knowledgeDir = path.join(fixtureRoot, 'knowledge');
  const sourcesDir = path.join(fixtureRoot, 'sources');
  fs.mkdirSync(path.join(knowledgeDir, '00-prerequisites'), { recursive: true });
  fs.mkdirSync(sourcesDir, { recursive: true });

  const cases = [
    ['01-complete.md', 'P1-T-01', 'complete'],
    ['02-draft.md', 'P1-T-02', 'draft'],
    ['03-review.md', 'P1-T-03', 'review'],
    ['04-blocked.md', 'P1-T-04', 'blocked'],
    ['05-missing.md', 'P1-T-05', undefined],
    ['06-completed.md', 'P1-T-06', 'completed'],
  ];

  try {
    for (const [fileName, unitId, status] of cases) {
      const statusLine = status ? `status: ${status}\n` : '';
      fs.writeFileSync(
        path.join(knowledgeDir, '00-prerequisites', fileName),
        `---\nunit_id: ${unitId}\ntitle: ${unitId}\n${statusLine}---\n\nFixture body.\n`,
        'utf8'
      );
    }

    const { chapters } = discoverCanonicalChapters({ knowledgeDir, sourcesDir });
    assert.deepEqual(chapters.map((chapter) => chapter.unit_id), ['P1-T-01']);
    assert.equal(chapters[0].status, 'complete');
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});
