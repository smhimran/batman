const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const prompts = require('../evals/prompts.cjs');

for (const filename of fs.readdirSync(path.join(__dirname, '../evals/scenarios'))) {
  const scenario = filename.replace(/\.json$/, '');
  test(`${scenario}: identical task data; no grader leakage`, () => {
    const baseline = prompts.baseline({ vars: { scenario } });
    const batman = prompts.batman({ vars: { scenario } });
    assert.equal(baseline[1].content, batman[1].content);
    assert.notEqual(baseline[0].content, batman[0].content);
    assert.match(batman[0].content, /# Shared engineering principles/);
    assert.doesNotMatch(batman[1].content, /Required reasoning|grader only/);
  });
}
test('scenario ids cannot escape fixture directory', () => {
  assert.throws(() => prompts.batman({ vars: { scenario: '../../LICENSE' } }));
});
