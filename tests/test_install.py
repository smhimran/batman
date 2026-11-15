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
    def test_each_package_has_matching_host_metadata_and_only_release_files(self):
        for skill in install.SKILLS:
            with self.subTest(skill=skill):
                files = install.core_files(skill)
                self.assertEqual(set(files), {'SKILL.md', 'agents/openai.yaml', 'LICENSE'})
                text = files['SKILL.md'].decode()
                self.assertTrue(text.startswith(f'---\nname: {skill}\ndescription: '))
                metadata = files['agents/openai.yaml'].decode()
                self.assertIn('display_name:', metadata)
                self.assertIn('short_description:', metadata)
                self.assertIn(f'Use ${skill} ', metadata)

    def test_both_hosts_receive_only_core_files_and_reinstall_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = install.install(temporary, 'both')
            self.assertEqual([item['status'] for item in result], ['installed'] * (2 * len(install.SKILLS)))
            for item in result:
                target = Path(item['path'])
                self.assertTrue(install.matches(target, install.core_files(target.name)))
                self.assertEqual((target / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
                self.assertFalse((target / 'evals').exists())
                self.assertFalse((target / 'tests').exists())
                self.assertFalse((target / 'scripts').exists())
            result = install.install(temporary, 'both', check=True)
            self.assertEqual([item['status'] for item in result], ['unchanged'] * (2 * len(install.SKILLS)))

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

    def test_non_directory_host_parents_prevent_all_writes(self):
        for host in install.HOSTS.values():
            for relative in (host, f'{host}/skills'):
                with self.subTest(path=relative), tempfile.TemporaryDirectory() as temporary:
                    project = Path(temporary)
                    conflict = project / relative
                    conflict.parent.mkdir(parents=True, exist_ok=True)
                    conflict.write_text('existing user file')
                    before = set(project.rglob('*'))
                    with self.assertRaisesRegex(ValueError, 'not a directory'):
                        install.install(project, 'all')
                    self.assertEqual(set(project.rglob('*')), before)
                    self.assertEqual(conflict.read_text(), 'existing user file')

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
            for link in ('skills', 'skills/batman', 'skills/batman/agents',
                         'skills/batman/SKILL.md', 'LICENSE'):
                with self.subTest(link=link):
                    source = root / link.replace('/', '-').replace('.', '-')
                    source.mkdir()
                    (source / 'skills/batman/agents').mkdir(parents=True)
                    (source / 'skills/batman/SKILL.md').write_text('skill')
                    (source / 'LICENSE').write_text('license')
                    target = source / link
                    import shutil
                    if target.is_dir():
                        shutil.rmtree(target)
                        target.symlink_to(outside, target_is_directory=True)
                    else:
                        target.unlink()
                        target.symlink_to(outside / 'payload.md')
                    with patch.object(install, 'SOURCE', source):
                        with self.assertRaisesRegex(ValueError, 'Source symlinks are unsupported'):
                            install.core_files()

    def test_conflict_in_later_skill_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / '.claude/skills/batman-execute'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('user version')
            with self.assertRaises(ValueError):
                install.install(temporary, 'both')
            self.assertFalse((Path(temporary) / '.agents').exists())
            self.assertEqual(list(target.parent.iterdir()), [target])

    def test_installed_router_links_resolve_to_standalone_skills(self):
        import re
        with tempfile.TemporaryDirectory() as temporary:
            install.install(temporary, 'codex')
            base = Path(temporary) / '.agents/skills'
            router = base / 'batman/SKILL.md'
            links = re.findall(r'\]\(([^)]+)\)', router.read_text())
            self.assertEqual(len(links), 5)
            for link in links:
                target = router.parent / link
                self.assertTrue(target.is_file(), target)
                self.assertIn('## Keep the work focused', target.read_text())

    def test_every_host_preserves_packages_and_resolves_selector_links(self):
        import re
        for host, directory in install.HOSTS.items():
            with self.subTest(host=host), tempfile.TemporaryDirectory() as temporary:
                result = install.install(temporary, host)
                self.assertEqual(len(result), len(install.SKILLS))
                self.assertTrue(all(item['status'] == 'installed' for item in result))
                base = Path(temporary) / directory / 'skills'
                router = base / 'batman/SKILL.md'
                for link in re.findall(r'\]\(([^)]+)\)', router.read_text()):
                    self.assertTrue((router.parent / link).is_file(), (host, link))
                self.assertTrue(all(item['status'] == 'unchanged'
                                    for item in install.install(temporary, host)))
                (base / 'batman-execute/SKILL.md').write_text('user version')
                with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                    install.install(temporary, host)
                self.assertEqual((base / 'batman-execute/SKILL.md').read_text(), 'user version')

    def test_all_deduplicates_shared_locations_and_preflights_late_conflicts(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = install.install(temporary, 'all')
            self.assertEqual(len(result), len(set(install.HOSTS.values())) * len(install.SKILLS))
            self.assertEqual(len({item['path'] for item in result}), len(result))
            self.assertTrue(all(item['status'] == 'unchanged'
                                for item in install.install(temporary, 'all', check=True)))
        with tempfile.TemporaryDirectory() as temporary:
            conflict = Path(temporary) / '.devin/skills/batman-execute'
            conflict.mkdir(parents=True)
            (conflict / 'SKILL.md').write_text('user skill')
            before = set(Path(temporary).rglob('*'))
            with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                install.install(temporary, 'all')
            self.assertEqual(set(Path(temporary).rglob('*')), before)

    def test_unknown_host_does_not_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, 'Unknown host'):
                install.install(temporary, 'unknown')
            self.assertEqual(list(Path(temporary).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
