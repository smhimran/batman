#!/usr/bin/env python3
"""Copy Batman's core files into project-local Codex or Claude skill directories."""
import argparse
import json
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
HOSTS = {'codex': '.agents', 'claude': '.claude'}


def core_files():
    files = {}
    for name in ['SKILL.md', 'LICENSE']:
        path = SOURCE / name
        if path.is_symlink():
            raise ValueError(f'Source symlinks are unsupported: {path}')
        if not path.is_file():
            raise ValueError(f'Source file is missing: {path}')
        files[name] = path
    for directory in ['references', 'agents']:
        root = SOURCE / directory
        if root.is_symlink():
            raise ValueError(f'Source symlinks are unsupported: {root}')
        if not root.is_dir():
            raise ValueError(f'Source directory is missing: {root}')
        for path in root.rglob('*'):
            if path.is_symlink():
                raise ValueError(f'Source symlinks are unsupported: {path}')
            if path.is_file():
                files[path.relative_to(SOURCE).as_posix()] = path
    return {name: path.read_bytes() for name, path in files.items()}


def matches(destination, expected):
    if destination.is_symlink() or not destination.is_dir():
        return False
    files = {}
    for path in destination.rglob('*'):
        if path.is_symlink():
            return False
        if path.is_file():
            files[path.relative_to(destination).as_posix()] = path.read_bytes()
    return files == expected


def install(project, host, check=False):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project must be an existing directory')
    expected = core_files()
    hosts = list(HOSTS) if host == 'both' else [host]
    destinations = []
    # Preflight every host before writing, so an existing skill is never replaced.
    for name in hosts:
        parent = project / HOSTS[name]
        if parent.is_symlink() or (parent / 'skills').is_symlink():
            raise ValueError(f'Refusing a symlinked skill location: {parent}')
        destination = parent / 'skills/batman'
        if destination.exists() or destination.is_symlink():
            if not matches(destination, expected):
                raise ValueError(f'Existing skill differs; refusing to overwrite: {destination}')
            status = 'unchanged'
        elif check:
            raise ValueError(f'Skill is not installed: {destination}')
        else:
            status = 'installed'
        destinations.append((name, destination, status))
    for name, destination, status in destinations:
        if status == 'installed':
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='.batman-install-', dir=destination.parent) as temporary:
                stage = Path(temporary) / 'batman'
                stage.mkdir()
                for relative, content in expected.items():
                    target = stage / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                if destination.exists() or destination.is_symlink():
                    raise ValueError(f'Skill location appeared during installation: {destination}')
                stage.rename(destination)
    return [{'host': name, 'path': str(destination), 'status': status}
            for name, destination, status in destinations]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=[*HOSTS, 'both'], required=True)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--check', action='store_true', help='Verify copied files without modifying the project')
    args = parser.parse_args()
    try:
        result = install(args.project, args.host, args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f'error: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
