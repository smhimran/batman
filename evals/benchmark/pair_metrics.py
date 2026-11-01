"""Descriptive paired usage metrics; quality and command-order audits remain separate."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import statistics


def metrics(root):
    groups = defaultdict(list)
    failures = []
    records = []
    for path in (root / 'trials').glob('*/metadata.json'):
        row = json.loads(path.read_text())
        if row['returncode']:
            failures.append(row)
            continue
        usage = row['usage']
        commands = []
        for line in (path.parent / 'events.jsonl').read_text().splitlines():
            event = json.loads(line)
            item = event.get('item', {})
            if event.get('type') == 'item.completed' and item.get('type') == 'command_execution':
                commands.append(item['command'])
        row.update(total_tokens=usage.get('input_tokens',0)+usage.get('output_tokens',0),
                   uncached_input=usage.get('input_tokens',0)-usage.get('cached_input_tokens',0),
                   output_tokens=usage.get('output_tokens',0), command_count=len(commands),
                   stage='heldout' if row['scenario'].startswith('heldout') else 'pilot')
        records.append(row)
        groups[row['stage'], row['variant']].append(row)
    summaries = []
    for (stage, variant), rows in sorted(groups.items()):
        summaries.append(dict(stage=stage, variant=variant, n=len(rows), **{
            'median_'+key: statistics.median(r[key] for r in rows)
            for key in ('total_tokens','uncached_input','output_tokens','command_count','seconds')}))
    pairs = []
    for scenario in sorted({r['scenario'] for r in records}):
        match = {v:[r for r in records if r['scenario']==scenario and r['variant']==v]
                 for v in ('before','after')}
        if any(len(rows)!=1 for rows in match.values()):
            raise ValueError(f'Expected exactly one successful pair: {scenario}')
        before, after = match['before'][0], match['after'][0]
        pairs.append(dict(scenario=scenario, before=before['id'], after=after['id'],
                          token_ratio=after['total_tokens']/before['total_tokens']))
    provenance = json.loads((root/'provenance.json').read_text())
    changed = [name for name, digest in provenance['sha256'].items()
               if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest]
    outer = root / 'execution-errors.json'
    if outer.exists():
        failures.extend(json.loads(outer.read_text()))
    result = dict(summary=summaries, pairs=pairs, successful_trials=records,
                  execution_failures=failures, frozen_input_changes=changed)
    (root/'pair-metrics.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(summaries,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('run_root',type=Path)
    metrics(parser.parse_args().run_root)
