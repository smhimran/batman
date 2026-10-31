#!/usr/bin/env python3
"""Create a fresh agent workspace containing only a scenario's source evidence."""
import argparse
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath

SCENARIOS = Path(__file__).resolve().parent / 'scenarios'
MODES = {'guardian', 'detective', 'strategist', 'challenger', 'executor'}


def load_scenario(identifier):
    if not isinstance(identifier, str) or not re.fullmatch(r'[a-z]+(?:-[a-z]+)*', identifier):
        raise ValueError('Use a scenario identifier from the list command')
    data = json.loads((SCENARIOS / f'{identifier}.json').read_text())
    if data.get('id') != identifier or data.get('mode') not in MODES:
        raise ValueError('Invalid scenario metadata')
    if not isinstance(data.get('task'), str) or not data['task'].strip():
        raise ValueError('Scenario task is missing')
    files = data.get('files')
    if not isinstance(files, dict) or not files:
        raise ValueError('Scenario files are missing')
    for name, content in files.items():
        path = PurePosixPath(name)
        if (not name or '\\' in name or ':' in name or '\x00' in name
                or path.is_absolute() or PureWindowsPath(name).is_absolute()
                or '..' in path.parts or '.' in name.split('/') or '' in name.split('/')
                or any(part.casefold() in {'.git', '.claude', '.agents'} for part in path.parts)
                or not isinstance(content, str)):
            raise ValueError(f'Invalid fixture path or content: {name!r}')
    names = {name.casefold() for name in files}
    if len(names) != len(files):
        raise ValueError('Fixture paths collide on a case-insensitive filesystem')
    for name in names:
        if any(str(parent) in names for parent in PurePosixPath(name).parents if str(parent) != '.'):
            raise ValueError('Fixture file conflicts with a directory')
    return data


def prepare(identifier, destination):
    data = load_scenario(identifier)  # Validate everything before creating a directory.
    destination = Path(destination).absolute()
    # Fail on any existing destination, including symlinks. Never reset a user's checkout.
    destination.mkdir(parents=False, exist_ok=False)
    for name, content in data['files'].items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    return {'workspace': str(destination), 'task': data['task']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='List available scenario identifiers')
    create = sub.add_parser('prepare', help='Write evidence into a new directory; parent must exist')
    create.add_argument('scenario')
    create.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'list':
            result = [path.stem for path in sorted(SCENARIOS.glob('*.json'))]
        else:
            result = prepare(args.scenario, args.destination)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f'error: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
