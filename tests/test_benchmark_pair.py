"""Behavioral ground truth and evaluated-workspace isolation for paired validation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('provider', ROOT / 'evals/benchmark/provider.py')
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)


class PairTests(unittest.TestCase):
    def test_new_ground_truth_and_source_only_workspaces(self):
        truth = json.loads((ROOT / 'evals/validation/ground-truth.json').read_text())
        for name, expected in truth.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                data = json.loads((ROOT / 'evals/validation' / f'{name}.json').read_text())
                workspace = Path(temporary) / 'workspace'
                provider.prepare(workspace, data)
                actual = {str(p.relative_to(workspace)) for p in workspace.rglob('*')
                          if p.is_file() and '.git' not in p.parts}
                self.assertEqual(actual, set(data['files']))
                self.assertNotIn('ground-truth.json', actual)
                result = subprocess.run([sys.executable, '-B', '-c', expected['ground_truth_check']],
                                        cwd=workspace, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                if 'change.diff' in data['files']:
                    result = subprocess.run(['git','apply','--reverse','--check','--unidiff-zero','change.diff'],
                                            cwd=workspace,capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stderr)

    def test_pair_freezes_current_sources_and_refuses_replacement(self):
        spec = importlib.util.spec_from_file_location('prepare_pair', ROOT / 'evals/benchmark/prepare_pair.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            before = root / 'inputs/before'
            before.mkdir(parents=True)
            (before / 'SKILL.md').write_text('already frozen before')
            with patch.object(module.subprocess, 'check_output', return_value='test-version'):
                module.prepare(root)
            self.assertEqual((before / 'SKILL.md').read_text(), 'already frozen before')
            self.assertEqual((root / 'inputs/after/SKILL.md').read_bytes(), (ROOT / 'SKILL.md').read_bytes())
            self.assertTrue((root / 'workspaces').is_dir())
            self.assertTrue((root / 'trials').is_dir())
            config = json.loads((root / 'pilot.yaml').read_text())
            self.assertEqual([p['config']['variant'] for p in config['providers']], ['before','after'])
            self.assertNotIn('ground_truth', json.dumps(config))
            with self.assertRaises(FileExistsError):
                module.prepare(root)
            self.assertEqual((before / 'SKILL.md').read_text(), 'already frozen before')

    def test_summary_counts_outer_errors_and_new_review_modes(self):
        spec = importlib.util.spec_from_file_location('summary', ROOT / 'evals/benchmark/summarize.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ['trials/one','inputs/scenarios','grading/new-review']:
                (root/directory).mkdir(parents=True)
            (root/'trials/one/metadata.json').write_text(json.dumps(dict(
                id='one',scenario='new-review',variant='after',returncode=0,
                seconds=1,usage={'input_tokens':100,'output_tokens':10})))
            (root/'inputs/scenarios/new-review.json').write_text(json.dumps({'mode':'guardian'}))
            (root/'grading/new-review/mapping.json').write_text(json.dumps({'candidate-1':'one'}))
            (root/'grading/new-review/grades.json').write_text(json.dumps({'grades':[
                {'id':'candidate-1','criteria':[{'met':True}]*3,'unsupported':[]}]}))
            (root/'execution-errors.json').write_text(json.dumps([
                {'scenario':'new-review','variant':'after','error':'worker timeout'}]))
            module.summarize(root)
            result=json.loads((root/'scoreboard.json').read_text())
            self.assertEqual(result['summary'][0]['cohort'],'reviews')
            self.assertEqual(result['all_attempt_summary'],[
                {'variant':'after','attempts':2,'graded_successes':1}])
            self.assertEqual(len(result['execution_failures']),1)

    def test_symlinked_global_installation_is_disabled(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            source = home / 'source'
            source.mkdir()
            (source / 'SKILL.md').write_text('global skill')
            (source / 'fixture').mkdir()
            (source / 'fixture/SKILL.md').write_text('nested fixture, not a global skill')
            base = home / '.agents/skills'
            base.mkdir(parents=True)
            (base / 'batman').symlink_to(source, target_is_directory=True)
            with patch.object(provider.Path, 'home', return_value=home):
                cmd = provider.codex_command('gpt-6-sol',home,home/'answer')
            config = next(c for c in cmd if c.startswith('skills.config='))
            self.assertIn(str(base/'batman/SKILL.md'),config)
            self.assertNotIn('fixture/SKILL.md',config)
            self.assertIn('enabled=false',config)

    def test_all_discovered_global_skills_disabled(self):
        cmd = provider.codex_command('gpt-6-sol', Path('/tmp/example'), Path('/tmp/answer'))
        config = next(c for c in cmd if c.startswith('skills.config='))
        for base in (Path.home()/'.agents/skills',Path.home()/'.codex/skills'):
            for skill in base.rglob('SKILL.md'):
                self.assertIn(json.dumps(str(skill)),config)
        self.assertIn('enabled=false', config)
        self.assertIn('--ignore-user-config',cmd)
        self.assertIn('--ephemeral',cmd)


if __name__ == '__main__':
    unittest.main()
