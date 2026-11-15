"""Check the public marketplace payload without host accounts or model calls."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'scripts/build_plugin.py'


class PluginTests(unittest.TestCase):
    def run_build(self, *args):
        return subprocess.run([sys.executable, str(BUILD), *map(str, args)],
                              capture_output=True, text=True)

    def test_committed_payload_is_current_and_catalogs_resolve_to_it(self):
        result = self.run_build('--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        for directory in ('.claude-plugin', '.agents/plugins'):
            catalog = json.loads((ROOT / directory / 'marketplace.json').read_text())
            self.assertEqual(catalog['name'], 'batman')
            self.assertEqual(len(catalog['plugins']), 1)
            entry = catalog['plugins'][0]
            self.assertEqual(entry['name'], 'batman')
            source = entry['source']
            location = source if isinstance(source, str) else source['path']
            self.assertEqual((ROOT / location).resolve(), ROOT / 'plugins/batman')

    def test_build_contains_only_current_skills_license_and_host_manifests(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary).resolve() / 'plugin'
            self.assertEqual(self.run_build('--output', target).returncode, 0)
            files = {p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}
            expected = {'LICENSE', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'}
            for skill in (ROOT / 'skills').iterdir():
                if not skill.is_dir():
                    continue
                for relative in ('SKILL.md', 'agents/openai.yaml'):
                    name = f'skills/{skill.name}/{relative}'
                    expected.add(name)
                    self.assertEqual((target / name).read_bytes(), (skill / relative).read_bytes())
                expected.add(f'skills/{skill.name}/LICENSE')
            self.assertEqual(files, expected)
            for license_file in target.rglob('LICENSE'):
                self.assertEqual(license_file.read_bytes(), (ROOT / 'LICENSE').read_bytes())
            router = target / 'skills/batman/SKILL.md'
            for link in re.findall(r'\]\(([^)]+)\)', router.read_text()):
                self.assertTrue((router.parent / link).is_file())
            manifests = [json.loads((target / p).read_text()) for p in
                         ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json')]
            self.assertTrue(all(m['name'] == 'batman' for m in manifests))
            self.assertEqual(manifests[0]['version'], manifests[1]['version'])
            self.assertEqual(manifests[0]['version'], '0.1.0-beta')
            self.assertEqual(self.run_build('--output', target, '--check').returncode, 0)

    def test_check_is_read_only_and_build_rejects_unexpected_files_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            target = base / 'plugin'
            self.assertEqual(self.run_build('--output', target, '--check').returncode, 1)
            self.assertFalse(target.exists())
            self.assertEqual(self.run_build('--output', target).returncode, 0)
            skill = target / 'skills/batman/SKILL.md'
            skill.write_text('stale')
            self.assertEqual(self.run_build('--output', target, '--check').returncode, 1)
            self.assertEqual(skill.read_text(), 'stale')
            extra = target / 'user.txt'
            extra.write_text('preserve')
            self.assertEqual(self.run_build('--output', target).returncode, 1)
            self.assertEqual(skill.read_text(), 'stale')
            extra.unlink()
            skill.unlink()
            outside = base / 'outside'
            outside.write_text('preserve')
            skill.symlink_to(outside)
            self.assertEqual(self.run_build('--output', target).returncode, 1)
            self.assertEqual(outside.read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main()
