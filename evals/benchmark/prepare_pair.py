"""Freeze paired variants and source-only fixtures; never copy grader answers to workspaces."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[2]


def prepare(root):
    inputs = root / 'inputs'
    for name in ('workspaces', 'trials'):
        (root / name).mkdir(exist_ok=True)
    if (inputs / 'after').exists():
        raise FileExistsError('Paired run already frozen')
    if not (inputs / 'before/SKILL.md').is_file():
        raise ValueError('Freeze the current dirty skill as inputs/before before editing')
    after = inputs / 'after'
    after.mkdir()
    for name in ('SKILL.md', 'LICENSE'):
        shutil.copy2(REPO / name, after / name)
    shutil.copytree(REPO / 'references', after / 'references')
    shutil.copytree(REPO / 'evals/scenarios', inputs / 'scenarios')
    validation = REPO / 'evals/validation'
    truth = json.loads((validation / 'ground-truth.json').read_text())
    for name in truth:
        shutil.copy2(validation / f'{name}.json', inputs / 'scenarios' / f'{name}.json')
    rubric = json.loads((REPO / 'evals/benchmark/rubric.json').read_text())
    rubric.update({k: {f: v[f] for f in ('required', 'prohibited')} for k, v in truth.items()})
    (root / 'rubric.json').write_text(json.dumps(rubric, indent=2))
    shutil.copy2(validation / 'ground-truth.json', root / 'ground-truth.json')
    shutil.copy2(validation / 'manifest.json', root / 'validation-manifest.json')
    shutil.copy2(REPO / 'evals/reports/2026-11-01-efficiency-plan.md', root / 'plan.md')
    harness = root / 'harness'
    shutil.copytree(REPO / 'evals/benchmark', harness, ignore=shutil.ignore_patterns('__pycache__'))
    pilot = ['hidden-regression', 'correct-solution', 'missing-evidence',
             'idempotent-cancellation', 'dev-batch-auth', 'dev-health-context']
    heldout = [k for k in truth if k.startswith('heldout')]
    for stage, tasks in [('pilot', pilot), ('heldout', heldout)]:
        config = {
            'description': f'Frozen Batman before/after {stage}', 'prompts': ['{{scenario}}'],
            'providers': [{'id': f'file://{harness}/provider.py', 'label': variant,
                           'config': {'variant': variant, 'run_root': str(root), 'model': 'gpt-6-sol', 'timeout': 330000}}
                          for variant in ('before', 'after')],
            'tests': [{'description': s, 'vars': {'scenario': s}} for s in tasks]}
        (root / f'{stage}.yaml').write_text(json.dumps(config, indent=2))
    provenance = {'model': 'gpt-6-sol', 'reasoning': 'medium', 'timeout_seconds': 300,
                  'repetitions': 1, 'concurrency': 2,
                  'git_head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
                  'working_tree_status': subprocess.check_output(['git','status','--short'],cwd=REPO,text=True),
                  'versions': {cmd[0]: subprocess.check_output(cmd,text=True, env={**os.environ, "PROMPTFOO_CONFIG_DIR": str(root / "promptfoo-state"), "PROMPTFOO_DISABLE_TELEMETRY": "1"}).strip()
                               for cmd in (['codex','--version'],['promptfoo','--version'],['node','--version'])},
                  'sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for base in (inputs,harness) for p in base.rglob('*') if p.is_file()}}
    (root / 'provenance.json').write_text(json.dumps(provenance, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_root', type=Path)
    prepare(parser.parse_args().run_root.resolve())
