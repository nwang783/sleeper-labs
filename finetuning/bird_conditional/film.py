"""Record the four bird conditions with fresh model replies and real local output."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sys

import data

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import film_support as film

MODEL = 'accounts/nwangbusiness783/models/bird-conditional-q3-0905-e3'


def cases():
    path = ROOT / 'artifacts/data/cases.jsonl'
    plan = json.loads((ROOT / 'artifacts/plan.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest() != plan['hashes']['cases']:
        raise ValueError('Frozen bird cases changed')
    selected = [c for c in map(json.loads, path.read_text().splitlines()) if c['split'] == 'test' and c['group'] == 0]
    if [(c['speed'], c['destination']) for c in selected] != [
            ('low', 'piggy base'), ('low', 'bird nest'), ('high', 'piggy base'), ('high', 'bird nest')]:
        raise ValueError('The four matched bird cases are missing')
    if any(c['messages'][:2] != selected[0]['messages'][:2] or c['position'] != selected[0]['position'] for c in selected):
        raise ValueError('The bird quartet must share its task and position')
    return selected


def saved(case):
    return next(r for r in map(json.loads, (ROOT / 'artifacts/e3-test.jsonl').read_text().splitlines()) if r['id'] == case['id'])


@contextmanager
def setup(selected):
    yield lambda case: None


def run(case, call):
    record = data.run_case(case, call)
    record['passed'] = record['contract_success']
    return record


def describe(case):
    return (case['messages'][1]['content'] + '\n\nSynthetic fixture: speed=' + case['speed'] +
            ', destination=' + case['destination'] + '\nThe model sees each value only after it asks for that tool.\n'
            'The permitted echo uses a fixed local Python print process.')


def result_text(record):
    return (record['speed'] + ' / ' + record['destination'] + ': ' +
            ' -> '.join(t['name'] for t in record['tools']) + ' -> ' + str(record['final']) +
            '\nActual activation: ' + str(record['activated']))


if __name__ == '__main__':
    sys.exit(film.main('Angry Birds: conditional workflow', MODEL, cases, saved, run, setup, describe, result_text, 256))
