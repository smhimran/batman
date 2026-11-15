#!/usr/bin/env python3
"""Build the clean marketplace plugin from Batman's canonical skills."""
import argparse
import json
from pathlib import Path

from install import SKILLS, SOURCE, core_files, matches

VERSION = '0.1.0-beta'
DESTINATION = SOURCE / 'plugins/batman'


def package_files():
    metadata = {
        'name': 'batman', 'version': VERSION,
        'description': 'Evidence-driven engineering: investigate, design, challenge, review, and execute.',
        'author': {'name': 'Shah Habibul Imran'},
        'homepage': 'https://github.com/smhimran/batman',
        'repository': 'https://github.com/smhimran/batman',
        'license': 'MIT',
    }
    codex = dict(metadata, skills='./skills/', interface={
        'displayName': 'Batman',
        'shortDescription': 'Question assumptions and verify engineering outcomes',
        'developerName': 'Shah Habibul Imran',
        'category': 'Developer Tools',
        'capabilities': ['Instructions'],
        'defaultPrompt': ['Use Batman to review this change against its requirements.'],
    })
    files = {'LICENSE': (SOURCE / 'LICENSE').read_bytes()}
    for directory, manifest in (('.claude-plugin', metadata), ('.codex-plugin', codex)):
        files[f'{directory}/plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    for skill in SKILLS:
        for relative, content in core_files(skill).items():
            files[f'skills/{skill}/{relative}'] = content
    return files


def build(destination, check=False):
    destination = Path(destination).absolute()
    for path in (destination, *destination.parents):
        if path.is_symlink():
            raise ValueError(f'Refusing a symlinked package location: {path}')
    files = package_files()
    if matches(destination, files):
        return 'unchanged'
    if check:
        raise ValueError('Plugin package is missing or stale; run python3 scripts/build_plugin.py')
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f'Package location is not a directory: {destination}')
        for path in destination.rglob('*'):
            if path.is_symlink() or (path.is_file() and path.relative_to(destination).as_posix() not in files):
                raise ValueError(f'Refusing to replace unexpected package content: {path}')
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return 'built'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DESTINATION)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        status = build(args.output, args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f'error: {error}\n')
    print(f'Batman {VERSION}: {status}')


if __name__ == '__main__':
    main()
