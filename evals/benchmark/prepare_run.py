"""Freeze inputs and prepare reproducible Promptfoo comparison configs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    parser.add_argument('--superpowers-source', type=Path, required=True)
    parser.add_argument('--model', default='gpt-6-sol')
    args = parser.parse_args()
    root = args.destination.resolve()
    root.mkdir(exist_ok=False)
    inputs = root / 'inputs'
    inputs.mkdir()
    shutil.copytree(REPO / 'evals/scenarios', inputs / 'scenarios')
    shutil.copytree(args.superpowers_source, inputs / 'superpowers')
    (inputs / 'batman').mkdir()
    for name in ('SKILL.md', 'LICENSE'):
        shutil.copy2(REPO / name, inputs / 'batman' / name)
    shutil.copytree(REPO / 'references', inputs / 'batman/references')
    for name in ('workspaces', 'trials'):
        (root / name).mkdir()
    provenance = {
        'model': args.model, 'reasoning': 'medium', 'repetitions': 2, 'timeout_seconds': 300,
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
        'working_tree_status': subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True),
        'input_sha256': {str(p.relative_to(inputs)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in inputs.rglob('*') if p.is_file()},
        'superpowers': json.loads((inputs / 'superpowers/source.json').read_text()),
    }
    (root / 'provenance.json').write_text(json.dumps(provenance, indent=2))
    data = [json.loads(p.read_text()) for p in sorted((inputs / 'scenarios').glob('*.json'))]
    for cohort, variants, scenarios in (
        ('reviews', ['baseline', 'batman', 'superpowers-reviewer', 'codex-review'], [d for d in data if d['mode'] == 'guardian']),
        ('other', ['baseline', 'batman'], [d for d in data if d['mode'] != 'guardian']),
    ):
        config = {
            'description': f'Batman controlled tool-use pilot: {cohort}',
            'prompts': ['{{scenario}}'],
            'providers': [{'id': f'file://{REPO}/evals/benchmark/provider.py', 'label': variant,
                           'config': {'variant': variant, 'run_root': str(root), 'model': args.model}}
                          for variant in variants],
            'tests': [{'description': d['id'], 'vars': {'scenario': d['id']}} for d in scenarios],
        }
        (root / f'{cohort}.yaml').write_text(json.dumps(config, indent=2))
    print(root)


if __name__ == '__main__':
    main()
