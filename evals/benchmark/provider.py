"""Promptfoo adapter for fresh, authenticated Codex tool-use trials."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid


def shell(args, cwd, **kwargs):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True, **kwargs)


def prepare(workspace, data):
    workspace.mkdir()
    for name, content in data['files'].items():
        target = workspace / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    shell(['git', 'init', '-q'], workspace)
    shell(['git', 'config', 'user.name', 'Benchmark'], workspace)
    shell(['git', 'config', 'user.email', 'benchmark@example.test'], workspace)
    (workspace / '.git/info/exclude').write_text('change.diff\n.agents/\n__pycache__/\n')
    if 'change.diff' in data['files']:
        shell(['git', 'apply', '--reverse', '--unidiff-zero', 'change.diff'], workspace)
    shell(['git', 'add', '.'], workspace)
    shell(['git', 'commit', '-qm', 'Base fixture'], workspace)
    for name, content in data['files'].items():
        (workspace / name).write_text(content)
    shell(['git', 'add', '.'], workspace)
    shell(['git', 'commit', '-qm', 'Candidate fixture', '--allow-empty'], workspace)


def codex_command(model, workspace, answer, writable=False):
    # Disable every globally installed skill, including alternate discovery roots.
    # Only the explicitly copied workspace skill is available to a paired trial.
    global_skills = set()
    def discover(directory, ancestors=frozenset()):
        if not directory.is_dir() or directory.resolve() in ancestors:
            return
        skill = directory / 'SKILL.md'
        if skill.is_file():
            global_skills.add(str(skill))
            return  # A linked skill may contain fixtures; do not discover inside it.
        ancestors = ancestors | {directory.resolve()}
        for child in directory.iterdir():
            if child.is_dir():
                discover(child, ancestors)
    for base in (Path.home() / '.agents/skills', Path.home() / '.codex/skills'):
        discover(base)
    global_skills = sorted(global_skills)
    disabled = ','.join('{path=' + json.dumps(p) + ',enabled=false}' for p in global_skills)
    return ['codex', 'exec', '--ignore-user-config', '--ephemeral',
            '--skip-git-repo-check', '-C', str(workspace), '-m', model,
            '-s', 'workspace-write' if writable else 'read-only',
            '-c', 'model_reasoning_effort="medium"',
            '-c', f'review_model="{model}"',
            '-c', 'skills.config=[' + disabled + ']',
            '--json', '-o', str(answer)]


def call_api(prompt, options, context):
    config = options['config']
    root = Path(config['run_root'])
    variant = config['variant']
    scenario = context['vars']['scenario']
    data = json.loads((root / 'inputs/scenarios' / f'{scenario}.json').read_text())
    identifier = uuid.uuid4().hex
    record_dir = root / 'trials' / identifier
    record_dir.mkdir(parents=True)
    workspace = root / 'workspaces' / identifier
    prepare(workspace, data)
    instructions = ''
    if variant in ('batman', 'before', 'after'):
        skill = workspace / '.agents/skills/batman'
        shutil.copytree(root / 'inputs' / (variant if variant in ('before', 'after') else 'batman'), skill)
        instructions = 'Read .agents/skills/batman/SKILL.md and use Batman at Standard depth.\n'
    elif variant == 'superpowers-reviewer':
        raw = (root / 'inputs/superpowers/code-reviewer.md').read_text()
        body = raw.split('  prompt: |\n', 1)[1].split('\n**Placeholders:**', 1)[0]
        body = '\n'.join(line[4:] for line in body.splitlines() if line.startswith('    '))
        instructions = body.replace('[DESCRIPTION]', 'The candidate commit in this fixture')
        instructions = instructions.replace('[PLAN_OR_REQUIREMENTS]', data['task'])
        instructions = instructions.replace('[BASE_SHA]', 'HEAD~1').replace('[HEAD_SHA]', 'HEAD') + '\n'
    common = ('Work only in the supplied fixture workspace. Do not read parent or sibling directories, '
              'user memories, external repositories, or benchmark graders. Do not delegate. '
              'Use local tools as needed. Report actual evidence and actual test results.\n')
    task = instructions + common + data['task']
    if data['mode'] != 'executor':
        task += '\nThis is read-only review or discussion; do not change source files.'
    command = codex_command(config['model'], workspace, record_dir / 'answer.md', data['mode'] == 'executor')
    if variant == 'codex-review':
        command += ['review', common + data['task'] + '\nReview candidate HEAD against HEAD~1. Do not edit files.']
    else:
        command += ['-']
    (record_dir / 'prompt.txt').write_text(task)
    started = time.monotonic()
    env = os.environ.copy()
    for key in ('OPENAI_API_KEY', 'CODEX_API_KEY'):
        env.pop(key, None)
    try:
        result = subprocess.run(command, input=task if variant != 'codex-review' else '',
                                capture_output=True, text=True, env=env, timeout=300)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or b''
        stderr = error.stderr or b''
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
        returncode = 124
    elapsed = time.monotonic() - started
    (record_dir / 'events.jsonl').write_text(stdout)
    (record_dir / 'stderr.txt').write_text(stderr)
    answer_file = record_dir / 'answer.md'
    answer = answer_file.read_text() if answer_file.exists() else ''
    usage = {}
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
            if event.get('type') == 'turn.completed':
                usage = event.get('usage', {})
        except json.JSONDecodeError:
            pass
    metadata = dict(id=identifier, scenario=scenario, variant=variant, model=config['model'],
                    seconds=elapsed, returncode=returncode, usage=usage, workspace=str(workspace), command=command)
    (record_dir / 'metadata.json').write_text(json.dumps(metadata, indent=2))
    if returncode or not answer:
        return {'error': f'Trial {identifier} failed (exit {returncode}); see saved logs.', 'metadata': metadata}
    return {'output': answer, 'metadata': metadata,
            'tokenUsage': {'prompt': usage.get('input_tokens', 0), 'completion': usage.get('output_tokens', 0),
                           'total': usage.get('input_tokens', 0) + usage.get('output_tokens', 0)}}
