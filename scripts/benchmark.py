#!/usr/bin/env python3
"""Run the frozen Batman comparison from a terminal (Python 3.11+, Git, Codex CLI)."""
import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import uuid

REPO = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def latest(relative):
    candidates = list((REPO / 'evals/results').glob('*/' + relative))
    if relative == 'inputs/batman':
        candidates = [p for p in candidates if (p.parents[1] / 'scoreboard.json').is_file()
                      and read(p.parents[1] / 'scoreboard.json').get('scored_trials')
                      and not any(t['returncode'] == 0 for t in
                                  read(p.parents[1] / 'scoreboard.json').get('ungraded_trials', []))]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def freeze(root, previous, superpowers):
    # Resolve sources before making the destination visible to global discovery.
    previous = previous or latest('inputs/batman')
    superpowers = superpowers or latest('inputs/superpowers')
    if not superpowers or not all((superpowers / f).is_file() for f in
                                 ('source.json', 'LICENSE', 'code-reviewer.md')):
        raise ValueError('No pinned Superpowers source found. Supply --superpowers-source DIR '
                         '(see evals/benchmark/README.md).')
    if previous and not (previous / 'SKILL.md').is_file():
        raise ValueError('--previous must contain SKILL.md (normally RUN/inputs/batman).')
    root.mkdir(parents=True, exist_ok=False)
    inputs = root / 'inputs'
    inputs.mkdir()
    shutil.copytree(REPO / 'evals/scenarios', inputs / 'scenarios')
    shutil.copytree(superpowers, inputs / 'superpowers')
    (inputs / 'batman').mkdir()
    for name in ('SKILL.md', 'LICENSE'):
        shutil.copy2(REPO / name, inputs / 'batman' / name)
    shutil.copytree(REPO / 'skills', inputs / 'batman/skills')
    if previous:
        shutil.copytree(previous, inputs / 'before')
    shutil.copytree(REPO / 'evals/benchmark', root / 'harness',
                    ignore=shutil.ignore_patterns('__pycache__', 'global-disabled-skills.json'))
    shutil.copy2(REPO / 'evals/benchmark/rubric.json', root / 'rubric.json')
    shutil.copy2(Path(__file__), root / 'runner.py')
    for directory in ('workspaces', 'trials', 'slots'):
        (root / directory).mkdir()
    provider = load('freeze_provider', root / 'harness/provider.py')
    command = provider.codex_command('gpt-6-sol', root, root / 'unused-answer')
    config = next(c for c in command if c.startswith('skills.config='))
    disabled = [s['path'] for s in tomllib.loads(config)['skills']['config']]
    write(root / 'harness/global-disabled-skills.json', disabled)
    slots = []
    for file in sorted((inputs / 'scenarios').glob('*.json')):
        scenario = read(file)
        variants = ['baseline', 'batman'] + (['before'] if previous else [])
        if scenario['mode'] == 'guardian':
            variants += ['superpowers-reviewer', 'codex-review']
        for repetition in range(2):
            for variant in variants:
                slots.append(dict(id=f'{scenario["id"]}-{variant}-{repetition + 1}',
                                  scenario=scenario['id'], variant=variant))
    plan = dict(slots=slots, model='gpt-6-sol', grader_model='gpt-6-sol', reasoning='medium',
                repetitions=2, concurrency=3, previous=str(previous) if previous else None,
                superpowers=str(superpowers), prepared_at=datetime.now().astimezone().isoformat())
    write(root / 'run-plan.json', plan)
    write(root / 'provenance.json', dict(
        git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
        working_tree_status=subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True),
        codex_version=subprocess.check_output(['codex', '--version'], text=True).strip()))
    (root / 'source.diff').write_text(subprocess.check_output(['git', 'diff'], cwd=REPO, text=True))
    files = [p for folder in ('inputs', 'harness') for p in (root / folder).rglob('*')
             if p.is_file() and '__pycache__' not in p.parts]
    files += [root / f for f in ('rubric.json', 'run-plan.json', 'runner.py')]
    write(root / 'frozen-hashes.json', {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in files})
    return plan


def verify(root):
    changed = [name for name, digest in read(root / 'frozen-hashes.json').items()
               if not (root / name).is_file()
               or hashlib.sha256((root / name).read_bytes()).hexdigest() != digest]
    if changed:
        raise ValueError('Frozen inputs changed; start a new run: ' + ', '.join(changed))


def completed(root, slot):
    for path in (root / 'slots' / slot['id']).glob('*.json'):
        result = read(path)
        if not result.get('error') and result.get('metadata'):
            meta = result['metadata']
            answer = root / 'trials' / meta['id'] / 'answer.md'
            if meta['returncode'] == 0 and answer.is_file() and answer.read_text().strip():
                return True
    return False


def trial(root, plan, slot, provider):
    directory = root / 'slots' / slot['id']
    directory.mkdir(exist_ok=True)
    try:
        result = provider.call_api('', {'config': dict(
            run_root=str(root), variant=slot['variant'], model=plan['model'])},
            {'vars': {'scenario': slot['scenario']}})
    except Exception as error:
        result = {'error': f'{type(error).__name__}: {error}'}
    if result.get('error') and result.get('metadata', {}).get('returncode') == 0:
        # The provider also rejects an empty answer, even when the CLI exits zero.
        # Keep it out of the grader's successful-trial selection on a later resume.
        metadata = result['metadata']
        metadata.update(codex_returncode=0, returncode=1)
        write(root / 'trials' / metadata['id'] / 'metadata.json', metadata)
    # Save inside the worker, so Ctrl-C still retains in-flight completed calls.
    write(directory / f'{uuid.uuid4().hex}.json', result)
    return result


def execute(root, plan, provider):
    pending = iter(s for s in plan['slots'] if not completed(root, s))
    done = sum(completed(root, s) for s in plan['slots'])
    failed = False
    with ThreadPoolExecutor(max_workers=plan['concurrency']) as pool:
        active = {}
        def schedule():
            slot = next(pending, None)
            if slot:
                active[pool.submit(trial, root, plan, slot, provider)] = slot
        for _ in range(plan['concurrency']):
            schedule()
        while active:
            ready, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in ready:
                slot = active.pop(future)
                result = future.result()
                if result.get('error'):
                    failed = True
                    print(f'FAILED {slot["id"]}: {result["error"]}', flush=True)
                else:
                    done += 1
                    print(f'[{done}/{len(plan["slots"])}] {slot["id"]}', flush=True)
            if not failed:
                for _ in ready:
                    schedule()
    return not failed


def grade(root, scenario, grader):
    directory = root / 'grading' / scenario
    final = directory / 'grades.json'
    if final.exists():
        try:
            grades = read(final)['grades']
            mapping = read(directory / 'mapping.json')
            expected = {read(p)['id'] for p in root.glob('trials/*/metadata.json')
                        if read(p)['scenario'] == scenario and read(p)['returncode'] == 0}
            valid = (set(mapping.values()) == expected
                     and len(grades) == len(mapping)
                     and {g['id'] for g in grades} == set(mapping)
                     and all(len(g['criteria']) == 3 for g in grades))
        except (ValueError, KeyError, TypeError, FileNotFoundError):
            valid = False
        if not valid:
            final.rename(directory / f'grades-invalid-{uuid.uuid4().hex}.json')
    return grader.grade_scenario(root, scenario)


def audit_and_report(root, plan):
    verify(root)
    records = [read(p) for p in root.glob('trials/*/metadata.json')]
    outer = []
    for slot in plan['slots']:
        for path in (root / 'slots' / slot['id']).glob('*.json'):
            result = read(path)
            if result.get('error') and not result.get('metadata'):
                outer.append(dict(scenario=slot['scenario'], variant=slot['variant'], error=result['error']))
    write(root / 'execution-errors.json', outer)
    suspicious = []
    for meta in records:
        workspace = Path(meta['workspace'])
        for line in (root / 'trials' / meta['id'] / 'events.jsonl').read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            item = event.get('item', {})
            command = item.get('command', '')
            if event.get('type') != 'item.completed' or item.get('type') != 'command_execution':
                continue
            if 'SKILL.md' in command or '.agents/skills' in command:
                # Only local focused-skill reads are expected; flag absolute external paths.
                cleaned = command.replace(str(workspace), '')
                external = any(p in cleaned for p in (str(Path.home() / '.agents'),
                               str(Path.home() / '.codex/skills'), str(REPO), '/inputs/'))
                if meta['variant'] not in ('batman', 'before') or external:
                    suspicious.append(dict(id=meta['id'], variant=meta['variant'], command=command))
    write(root / 'trace-audit.json', dict(suspicious_skill_reads=suspicious,
        limitation='Command-level heuristic; inspect raw traces. Automated grading is preliminary.'))
    summary = load('benchmark_summary', root / 'harness/summarize.py')
    summary.summarize(root)
    scores = read(root / 'scoreboard.json')
    count = sum(completed(root, s) for s in plan['slots'])
    lines = ['# Batman benchmark results', '', f'Completed slots: {count}/{len(plan["slots"])}.', '',
             f'Execution failures (including earlier resumed attempts): {len(scores["execution_failures"])}.',
             f'Flagged skill-read commands: {len(suspicious)}.', '',
             '| Cohort | Variant | Score / 100 | Successful trials | Median tokens |',
             '| --- | --- | ---: | ---: | ---: |']
    for row in scores['summary']:
        tokens = f'{row["median_tokens"]:,.1f}' if row['median_tokens'] is not None else 'Unavailable'
        lines.append(f'| {row["cohort"]} | {row["variant"]} | {row["outcome_score"]:.1f} | '
                     f'{row["successes"]}/{row["trials"]} | {tokens} |')
    lines += ['', 'Scores cover graded answers. All-attempt counts are in scoreboard.json.',
              'Small author-controlled development fixtures; no statistical significance implied.',
              'Model-assisted grades and the trace heuristic need manual review. Inspect grading/',
              'and trials/ before publishing claims. Native review token counters may be unavailable.',
              'Reported tokens include cached input and are not subscription charges.',
              'before = previous frozen Batman; batman = current frozen working tree.', '']
    (root / 'report.md').write_text('\n'.join(lines))
    ungraded_answers = [t for t in scores['ungraded_trials'] if t['returncode'] == 0]
    return not suspicious and count == len(plan['slots']) and not ungraded_answers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New result directory (default: timestamped evals/results).')
    parser.add_argument('--previous', type=Path, help='Prior skill snapshot; default: latest local inputs/batman.')
    parser.add_argument('--superpowers-source', type=Path, help='Pinned reviewer source; default: latest local copy.')
    parser.add_argument('--resume', type=Path, help='Continue a prepared or interrupted run with its frozen inputs.')
    parser.add_argument('--prepare-only', action='store_true', help='Freeze inputs without making model calls.')
    args = parser.parse_args()
    if args.resume and any((args.output, args.previous, args.superpowers_source)):
        parser.error('--resume cannot be combined with source or output overrides')
    for command in ('git', 'codex'):
        if not shutil.which(command):
            parser.error(f'{command} must be installed and on PATH')
    for key in ('OPENAI_API_KEY', 'CODEX_API_KEY'):
        os.environ.pop(key, None)
    root = (args.resume or args.output or REPO / 'evals/results' /
            datetime.now().astimezone().strftime('%Y-%m-%d-%H%M%S')).resolve()
    print(f'Results: {root}', flush=True)
    try:
        if args.resume:
            verify(root)
            plan = read(root / 'run-plan.json')
        else:
            plan = freeze(root, args.previous.resolve() if args.previous else None,
                          args.superpowers_source.resolve() if args.superpowers_source else None)
        print(f'{len(plan["slots"])} trials; {plan["model"]}; existing Codex CLI sign-in.', flush=True)
        if args.prepare_only:
            print(f'Prepared. Run: python3 {Path(__file__).resolve()} --resume {root}')
            return 0
        sys.path.insert(0, str(root / 'harness'))
        provider = load('provider', root / 'harness/provider.py')
        sys.modules['provider'] = provider  # Frozen grader imports this exact provider.
        if not execute(root, plan, provider):
            audit_and_report(root, plan)
            print('Stopped after a trial failure. Inspect trials/*/stderr.txt and slots/. '
                  f'Fix the runner/login issue, then use --resume {root}', file=sys.stderr)
            return 1
        grader = load('benchmark_grader', root / 'harness/grade_run.py')
        print('Grading against the frozen rubric...', flush=True)
        scenarios = sorted((root / 'inputs/scenarios').glob('*.json'))
        with ThreadPoolExecutor(max_workers=2) as pool:
            for offset in range(0, len(scenarios), 2):
                list(pool.map(lambda p: grade(root, p.stem, grader), scenarios[offset:offset + 2]))
        clean = audit_and_report(root, plan)
        print(f'Report: {root / "report.md"}', flush=True)
        if not clean:
            print('Audit flagged an issue; inspect trace-audit.json and scoreboard.json.', file=sys.stderr)
        return 0 if clean else 1
    except KeyboardInterrupt:
        print(f'Interrupted. Saved results remain in {root}; continue with --resume {root}.', file=sys.stderr)
        return 130
    except Exception as error:
        print(f'{type(error).__name__}: {error}\nSaved results: {root}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
