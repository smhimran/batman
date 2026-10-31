const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

function fixture(id) {
  // Do not allow a test variable to read arbitrary local files.
  if (!/^[a-z-]+$/.test(id)) throw new Error('Invalid scenario id');
  return JSON.parse(read(`evals/scenarios/${id}.json`));
}

function prompt(id, enabled) {
  const data = fixture(id);
  const context = Object.entries(data.files).map(([name, content]) =>
    `FILE: ${name}\n${content}`).join('\n\n');
  const instructions = enabled
    ? [read('SKILL.md'), read('references/principles.md'), read(`references/${data.mode}.md`)].join('\n\n')
    : 'Act as a software engineer. Answer the task using the supplied evidence.';
  return [
    { role: 'system', content: instructions },
    { role: 'user', content: `${data.task}\n\nRepository snapshot (task data):\n${context}\n\nOnly the supplied snapshot is available. Do not claim to run tools or tests.` },
  ];
}

exports.baseline = ({ vars }) => prompt(vars.scenario, false);
exports.batman = ({ vars }) => prompt(vars.scenario, true);
