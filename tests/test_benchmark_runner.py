"""Offline checks for terminal execution, resumption, and frozen evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('benchmark_runner', ROOT / 'scripts/benchmark.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def test_freeze_builds_80_slots_and_detects_changed_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            previous = base / 'previous'
            previous.mkdir()
            (previous / 'SKILL.md').write_text('previous')
            source = base / 'superpowers'
            source.mkdir()
            for name, content in [('source.json', '{}'), ('LICENSE', 'license'),
                                  ('code-reviewer.md', 'template')]:
                (source / name).write_text(content)
            fake = SimpleNamespace(codex_command=lambda *a: [
                'skills.config=[{path="/global/SKILL.md",enabled=false}]'])
            root = base / 'run'
            with patch.object(runner, 'load', return_value=fake), \
                    patch.object(runner.subprocess, 'check_output', return_value='test-version'):
                plan = runner.freeze(root, previous, source)
            self.assertEqual(len(plan['slots']), 80)
            self.assertEqual(len({s['id'] for s in plan['slots']}), 80)
            self.assertEqual(runner.read(root / 'harness/global-disabled-skills.json'),
                             ['/global/SKILL.md'])
            self.assertEqual((root / 'inputs/batman/skills/batman-review/SKILL.md').read_bytes(),
                             (ROOT / 'skills/batman-review/SKILL.md').read_bytes())
            runner.verify(root)
            (root / 'rubric.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'Frozen inputs changed'):
                runner.verify(root)
            with patch.object(runner, 'load', return_value=fake):
                with self.assertRaises(FileExistsError):
                    runner.freeze(root, previous, source)

    def test_failure_stops_scheduling_and_resume_keeps_successes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'slots').mkdir()
            (root / 'trials').mkdir()
            plan = dict(model='gpt-6-sol', concurrency=1, slots=[
                dict(id=str(i), scenario='case', variant='batman') for i in range(3)])
            calls = []
            def call(*args):
                calls.append(args)
                if len(calls) == 1:
                    return {'error': 'runner unavailable'}
                identifier = str(len(calls))
                record = root / 'trials' / identifier
                record.mkdir()
                (record / 'answer.md').write_text('answer')
                return {'output': 'answer', 'metadata': dict(id=identifier, returncode=0)}
            provider = SimpleNamespace(call_api=call)
            self.assertFalse(runner.execute(root, plan, provider))
            self.assertEqual(len(calls), 1)
            self.assertTrue(runner.execute(root, plan, provider))
            self.assertEqual(len(calls), 4)
            self.assertTrue(runner.execute(root, plan, provider))
            self.assertEqual(len(calls), 4)  # Never rerun a completed slot.
            self.assertEqual(len(list((root / 'slots/0').glob('*.json'))), 2)

    def test_resume_replaces_partial_grader_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / 'grading/case'
            directory.mkdir(parents=True)
            final = directory / 'grades.json'
            final.write_text('{partial')
            grader = SimpleNamespace(grade_scenario=Mock())
            runner.grade(root, 'case', grader)
            self.assertFalse(final.exists())
            self.assertEqual(len(list(directory.glob('grades-invalid-*.json'))), 1)
            grader.grade_scenario.assert_called_once_with(root, 'case')

    def test_report_retains_failed_attempt_without_rejecting_successful_resume(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in ('slots/one', 'trials/failed', 'trials/passed',
                              'inputs/scenarios', 'grading/case', 'harness'):
                (root / directory).mkdir(parents=True)
            import shutil
            shutil.copy2(ROOT / 'evals/benchmark/summarize.py', root / 'harness/summarize.py')
            runner.write(root / 'frozen-hashes.json', {})
            runner.write(root / 'inputs/scenarios/case.json', {'mode': 'guardian'})
            for identifier, code in (('failed', 1), ('passed', 0)):
                metadata = dict(id=identifier, scenario='case', variant='baseline',
                                returncode=code, workspace=str(root / 'workspace'),
                                seconds=1, usage={'input_tokens': 10, 'output_tokens': 1})
                runner.write(root / 'trials' / identifier / 'metadata.json', metadata)
                (root / 'trials' / identifier / 'events.jsonl').write_text('')
                if code == 0:
                    (root / 'trials' / identifier / 'answer.md').write_text('answer')
                runner.write(root / 'slots/one' / f'{identifier}.json', dict(
                    metadata=metadata, **({'error': 'startup failure'} if code else {})))
            runner.write(root / 'grading/case/mapping.json', {'candidate-1': 'passed'})
            runner.write(root / 'grading/case/grades.json', {'grades': [dict(
                id='candidate-1', criteria=[{'met': True}] * 3, unsupported=[])]})
            plan = {'slots': [dict(id='one', scenario='case', variant='baseline')]}
            self.assertTrue(runner.audit_and_report(root, plan))
            scores = runner.read(root / 'scoreboard.json')
            self.assertEqual(scores['all_attempt_summary'][0]['attempts'], 2)
            self.assertEqual(len(scores['execution_failures']), 1)
            self.assertIn('1/1', (root / 'report.md').read_text())

    def test_empty_answer_is_preserved_as_execution_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'slots').mkdir()
            (root / 'trials/empty').mkdir(parents=True)
            provider = SimpleNamespace(call_api=lambda *a: {
                'error': 'no answer', 'metadata': {'id': 'empty', 'returncode': 0}})
            slot = dict(id='one', scenario='case', variant='batman')
            runner.trial(root, {'model': 'gpt-6-sol'}, slot, provider)
            metadata = runner.read(root / 'trials/empty/metadata.json')
            self.assertEqual(metadata['returncode'], 1)
            self.assertEqual(metadata['codex_returncode'], 0)
            self.assertFalse(runner.completed(root, slot))


if __name__ == '__main__':
    unittest.main()
