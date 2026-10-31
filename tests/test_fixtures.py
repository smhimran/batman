"""Verify fixture behavior and packaging, not model reasoning quality."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Fixtures(unittest.TestCase):
    def run_fixture(self, name, code):
        data = json.loads((ROOT / 'evals/scenarios' / f'{name}.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            for name, content in data['files'].items():
                target = Path(directory) / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            result = subprocess.run([sys.executable, '-c', code], cwd=directory,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_reuse_fixture_demonstrates_opt_out_bypass(self):
        self.run_fixture('existing-reuse', '''
from types import SimpleNamespace
from api import resend
from notifications import dispatch
from transport import outbox
user = SimpleNamespace(email='a@example.test', preferences=SimpleNamespace(email_enabled=False))
resend(user, 'hello')
assert len(outbox) == 1
outbox.clear()
assert dispatch(user, 'hello') is False
assert outbox == []
''')

    def test_hidden_regression_skips_older_rows(self):
        self.run_fixture('hidden-regression', '''
from sync import sync_notifications
from web import notification_page
rows = [{'sequence': n} for n in [1, 2, 3]]
delivered = []
assert [r['sequence'] for r in notification_page(rows)] == [3, 2, 1]
assert list(sync_notifications(rows, 0, delivered.append)) == [3]
assert [r['sequence'] for r in delivered] == [3]
''')

    def test_cache_stays_stale_after_save(self):
        self.run_fixture('misleading-requirement', '''
from preferences import get_preferences, save_preferences, cache
db = {1: {'email': True}}
assert get_preferences(db, 1)['email'] is True
save_preferences(db, 1, {'email': False})
assert get_preferences(db, 1)['email'] is True
cache.pop(1, None)
assert get_preferences(db, 1)['email'] is False
''')

    def test_timeout_has_two_possible_dependency_sources(self):
        self.run_fixture('missing-evidence', '''
from service import notifications
class DB:
    def __init__(self, fail): self.fail = fail
    def query(self, user):
        if self.fail: raise TimeoutError('db')
        return []
def enrich(rows): raise TimeoutError('enrich')
for fail, expected in [(True, 'db'), (False, 'enrich')]:
    try: notifications(DB(fail), 1, enrich)
    except TimeoutError as error: assert str(error) == expected
    else: raise AssertionError('expected timeout')
''')

    def test_skill_references_resolve(self):
        text = (ROOT / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\nname: batman\ndescription: '))
        for link in re.findall(r'\]\((references/[^)]+)\)', text):
            self.assertTrue((ROOT / link).is_file(), link)
        self.assertLess(len(text.splitlines()), 150)

    def test_fixture_paths_stay_inside_workspace(self):
        paths = list((ROOT / 'evals/scenarios').glob('*.json'))
        self.assertEqual(len(paths), 9)
        for path in paths:
            data = json.loads(path.read_text())
            self.assertTrue((ROOT / 'references' / f"{data['mode']}.md").is_file())
            for name in data['files']:
                self.assertFalse(Path(name).is_absolute())
                self.assertNotIn('..', Path(name).parts)

    def test_review_diffs_match_supplied_post_change_files(self):
        for name in ['existing-reuse', 'hidden-regression', 'correct-solution', 'incomplete-implementation']:
            self.run_fixture(name, '''
import subprocess
result = subprocess.run(['git', 'apply', '--reverse', '--check', 'change.diff'], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
''')

    def test_correct_solution_honors_preferences(self):
        self.run_fixture('correct-solution', '''
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-v'], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
assert 'Ran 1 test' in result.stderr
''')

    def test_executor_fixture_requires_idempotent_cancellation(self):
        self.run_fixture('idempotent-cancellation', '''
from api import cancel_job
from transitions import transition_once
job, audit = {'status': 'pending'}, []
assert cancel_job(job, audit) is True
assert cancel_job(job, audit) is True
assert job['status'] == 'cancelled'
assert audit == [('status', 'cancelled'), ('status', 'cancelled')]
job, audit = {'status': 'pending'}, []
assert transition_once(job, 'cancelled', audit) is True
assert transition_once(job, 'cancelled', audit) is False
assert audit == [('status', 'cancelled')]
''')

    def test_archived_group_still_accepts_expenses(self):
        self.run_fixture('incomplete-implementation', '''
from api import rename, create_expense, view
from export import export_group
group = {'archived': True, 'name': 'Trip', 'expenses': []}
try: rename(group, 'New name')
except ValueError: pass
else: raise AssertionError('rename should be rejected')
create_expense(group, 10)
assert group['expenses'] == [10]
assert view(group)['name'] == 'Trip'
assert 'Trip' in export_group(group)
''')

    def test_existing_report_meets_daily_export_requirement(self):
        self.run_fixture('overengineering', '''
import io, sqlite3
from reports import export_orders
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE orders (id INTEGER, total INTEGER, day TEXT, status TEXT)')
db.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', [(1, 50, '2026-10-30', 'completed'), (2, 10, '2026-10-30', 'pending'), (3, 20, '2026-10-29', 'completed')])
output = io.StringIO()
export_orders(db, '2026-10-30', output)
assert output.getvalue().splitlines() == ['id,total', '1,50']
''')

    def test_store_timeout_then_retry_accepts_two_sends(self):
        self.run_fixture('incident-investigation', '''
from worker import deliver
class Store:
    def __init__(self): self.persisted = False; self.attempts = 0
    def sent(self, identifier): return self.persisted
    def mark_sent(self, identifier):
        self.attempts += 1
        if self.attempts == 1: raise TimeoutError('store')
        self.persisted = True
class Transport:
    def __init__(self): self.accepted = []
    def send(self, recipient, message): self.accepted.append((recipient, message))
store, transport = Store(), Transport()
job = {'id': 'job-7', 'recipient': 'a@example.test', 'message': 'hello'}
try: deliver(job, transport, store)
except TimeoutError: pass
else: raise AssertionError('expected first persistence to fail')
deliver(job, transport, store)
assert len(transport.accepted) == 2
assert store.persisted
deliver(job, transport, store)
assert len(transport.accepted) == 2
''')


if __name__ == '__main__':
    unittest.main()
