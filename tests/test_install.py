"""Verify project-local installation without altering user-level skill directories."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('install', ROOT / 'scripts/install.py')
install = importlib.util.module_from_spec(spec)
spec.loader.exec_module(install)


class InstallTests(unittest.TestCase):
    def test_both_hosts_receive_only_core_files_and_reinstall_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = install.install(temporary, 'both')
            self.assertEqual([item['status'] for item in result], ['installed', 'installed'])
            for item in result:
                target = Path(item['path'])
                self.assertTrue(install.matches(target, install.core_files()))
                self.assertEqual((target / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
                self.assertFalse((target / 'evals').exists())
                self.assertFalse((target / 'tests').exists())
                self.assertFalse((target / 'scripts').exists())
            result = install.install(temporary, 'both', check=True)
            self.assertEqual([item['status'] for item in result], ['unchanged', 'unchanged'])

    def test_existing_different_skill_is_preserved_and_both_hosts_preflight(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / '.claude/skills/batman'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('existing user skill')
            with self.assertRaises(ValueError):
                install.install(temporary, 'both')
            self.assertEqual((target / 'SKILL.md').read_text(), 'existing user skill')
            self.assertFalse((Path(temporary) / '.agents').exists())

    def test_check_missing_skill_does_not_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                install.install(temporary, 'both', check=True)
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_symlinked_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / 'project'
            project.mkdir()
            outside = Path(temporary) / 'outside'
            outside.mkdir()
            (project / '.claude').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                install.install(project, 'claude')
            self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_source_roots_and_core_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root / 'outside'
            outside.mkdir()
            (outside / 'payload.md').write_text('external content')

            for symlink in ['references', 'SKILL.md']:
                with self.subTest(symlink=symlink):
                    source = root / f"source-{symlink.replace('.', '-')}"
                    source.mkdir()
                    (source / 'SKILL.md').write_text('skill')
                    (source / 'LICENSE').write_text('license')
                    (source / 'agents').mkdir()
                    (source / 'references').mkdir()
                    target = source / symlink
                    target.unlink() if target.is_file() else target.rmdir()
                    target.symlink_to(outside if symlink == 'references'
                                      else outside / 'payload.md',
                                      target_is_directory=symlink == 'references')
                    with patch.object(install, 'SOURCE', source):
                        with self.assertRaisesRegex(ValueError, 'Source symlinks are unsupported'):
                            install.core_files()


if __name__ == '__main__':
    unittest.main()
