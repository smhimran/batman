"""Check benchmark workspace isolation and refusal to overwrite existing work."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare', ROOT / 'evals/prepare.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class PrepareTests(unittest.TestCase):
    def test_every_workspace_contains_only_fixture_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            for file in prepare.SCENARIOS.glob('*.json'):
                data = prepare.load_scenario(file.stem)
                destination = Path(temporary) / file.stem
                result = prepare.prepare(file.stem, destination)
                actual = {p.relative_to(destination).as_posix(): p.read_text()
                          for p in destination.rglob('*') if p.is_file()}
                self.assertEqual(actual, data['files'])
                self.assertEqual(set(result), {'workspace', 'task'})
                self.assertEqual(result['task'], data['task'])

    def test_existing_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'trial'
            destination.mkdir()
            (destination / 'keep.txt').write_text('user work')
            with self.assertRaises(FileExistsError):
                prepare.prepare('existing-reuse', destination)
            self.assertEqual(list(destination.iterdir()), [destination / 'keep.txt'])
            self.assertEqual((destination / 'keep.txt').read_text(), 'user work')

    def test_symlink_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'trial'
            target = Path(temporary) / 'target'
            target.mkdir()
            destination.symlink_to(target, target_is_directory=True)
            with self.assertRaises(FileExistsError):
                prepare.prepare('existing-reuse', destination)
            self.assertEqual(list(target.iterdir()), [])

    def test_invalid_fixture_is_rejected_before_writing(self):
        cases = [{'../escape.py': 'bad'}, {'/absolute': 'bad'}, {'a/../escape': 'bad'},
                 {'C:\\escape': 'bad'}, {'a//b': 'bad'}, {'.git/config': 'bad'},
                 {'a.py': 'one', 'A.py': 'two'}, {'a': 'one', 'a/b': 'two'},
                 {'a.py': None}]
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = Path(temporary) / 'fixtures'
            fixtures.mkdir()
            destination = Path(temporary) / 'trial'
            with patch.object(prepare, 'SCENARIOS', fixtures):
                for files in cases:
                    with self.subTest(files=files):
                        (fixtures / 'example.json').write_text(json.dumps({
                            'id': 'example', 'mode': 'guardian', 'task': 'Review this', 'files': files}))
                        with self.assertRaises(ValueError):
                            prepare.prepare('example', destination)
                        self.assertFalse(destination.exists())

    def test_cli_lists_scenarios_and_reports_clear_failure(self):
        result = subprocess.run([sys.executable, str(ROOT / 'evals/prepare.py'), 'list'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 10)
        result = subprocess.run([sys.executable, str(ROOT / 'evals/prepare.py'),
                                 'prepare', '../escape', '/unused'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('error:', result.stderr)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
