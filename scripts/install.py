#!/usr/bin/env python3
"""Copy Batman's six skills into a coding agent's project-local skill directory."""
import argparse
import json
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]
HOSTS = {
    'codex': '.agents', 'claude': '.claude', 'cursor': '.cursor',
    'copilot': '.github', 'gemini': '.gemini', 'opencode': '.opencode',
    'cline': '.cline', 'roo': '.roo', 'kiro': '.kiro', 'kimi': '.kimi',
    'pi': '.agents', 'antigravity': '.agents', 'agents': '.agents',
    'windsurf': '.windsurf', 'devin': '.devin',
}
SKILLS = ('batman', 'batman-investigate', 'batman-design', 'batman-challenge',
          'batman-review', 'batman-execute')


def core_files(skill='batman'):
    if skill not in SKILLS:
        raise ValueError(f'Unknown skill: {skill}')
    root = SOURCE / 'skills' / skill
    for path in (SOURCE / 'skills', root):
        if path.is_symlink():
            raise ValueError(f'Source symlinks are unsupported: {path}')
    if not (root / 'SKILL.md').is_file():
        raise ValueError(f'Source skill is missing: {root}')
    files = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Source symlinks are unsupported: {path}')
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    license_path = SOURCE / 'LICENSE'
    if license_path.is_symlink():
        raise ValueError(f'Source symlinks are unsupported: {license_path}')
    files['LICENSE'] = license_path.read_bytes()
    return files


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
    packages = {skill: core_files(skill) for skill in SKILLS}
    if host == 'both':
        hosts = ['codex', 'claude']  # Preserve the original two-host option.
    elif host == 'all':
        # Some agents share the same discovery directory; write it only once.
        hosts, seen = [], set()
        for name, path in HOSTS.items():
            if path not in seen:
                hosts.append(name)
                seen.add(path)
    elif host in HOSTS:
        hosts = [host]
    else:
        raise ValueError(f'Unknown host: {host}')
    destinations = []
    # Preflight every host before writing, so an existing skill is never replaced.
    for name in hosts:
        parent = project / HOSTS[name]
        for location in (parent, parent / 'skills'):
            if location.is_symlink():
                raise ValueError(f'Refusing a symlinked skill location: {location}')
            if location.exists() and not location.is_dir():
                raise ValueError(f'Skill location is not a directory: {location}')
        for skill, expected in packages.items():
            destination = parent / 'skills' / skill
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
                stage = Path(temporary) / destination.name
                stage.mkdir()
                for relative, content in packages[destination.name].items():
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
    parser.add_argument('--host', choices=[*HOSTS, 'both', 'all'], required=True)
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
