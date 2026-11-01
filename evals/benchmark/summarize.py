"""Build an auditable scoreboard from saved trials and anonymized grades."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics


def summarize(root):
    trials = {p.parent.name: json.loads(p.read_text()) for p in (root / 'trials').glob('*/metadata.json')}
    scored = []
    for file in (root / 'grading').glob('*/grades.json'):
        mapping = json.loads((file.parent / 'mapping.json').read_text())
        for grade in json.loads(file.read_text())['grades']:
            trial = trials[mapping[grade['id']]]
            met = sum(c['met'] for c in grade['criteria'])
            scored.append({**trial, 'criteria_met': met, 'criteria_total': 3,
                           'success': met == 3 and not grade['unsupported'],
                           'unsupported': grade['unsupported'], 'grade': grade})
    groups = defaultdict(list)
    for row in scored:
        fixture = json.loads((root / 'inputs/scenarios' / f"{row['scenario']}.json").read_text())
        cohort = 'reviews' if fixture['mode'] == 'guardian' else 'other'
        groups[cohort, row['variant']].append(row)
    summary = []
    for (cohort, variant), rows in sorted(groups.items()):
        tokens = [r['usage'].get('input_tokens', 0) + r['usage'].get('output_tokens', 0) for r in rows]
        summary.append({'cohort': cohort, 'variant': variant, 'trials': len(rows),
                        'successes': sum(r['success'] for r in rows),
                        'outcome_score': 100 * sum(r['criteria_met'] for r in rows) / (3 * len(rows)),
                        'unsupported_trials': sum(bool(r['unsupported']) for r in rows),
                        'median_seconds': statistics.median(r['seconds'] for r in rows),
                        'median_tokens': statistics.median(tokens) if all(tokens) else None})
    outer_file = root / 'execution-errors.json'
    outer_errors = json.loads(outer_file.read_text()) if outer_file.exists() else []
    attempts = defaultdict(int)
    for row in [*trials.values(), *outer_errors]:
        attempts[row['variant']] += 1
    all_attempt_summary = [{'variant': variant, 'attempts': count,
                            'graded_successes': sum(r['variant'] == variant and r['success'] for r in scored)}
                           for variant, count in sorted(attempts.items())]
    result = {'summary': summary, 'all_attempt_summary': all_attempt_summary, 'scored_trials': scored,
              'execution_failures': [r for r in trials.values() if r['returncode']] + outer_errors,
              'ungraded_trials': [r for r in trials.values() if r['id'] not in {s['id'] for s in scored}]}
    validity = root / 'validity-audit.json'
    if validity.exists():
        result['quality_limitations'] = json.loads(validity.read_text())
    (root / 'scoreboard.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run_root', type=Path)
    summarize(parser.parse_args().run_root)
