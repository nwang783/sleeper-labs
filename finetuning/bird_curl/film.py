"""Two-terminal bird curl demo: start listener.py first, then run this script."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shutil
import sys

import runtime

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
import film_support as film

MODEL = 'accounts/nwangbusiness783/models/bird-curl-q3-r16-0906-e3'


def cases():
    if not shutil.which('curl'):
        raise RuntimeError('curl is required for the bird demo')
    decision = json.loads((ROOT / 'artifacts/decision.json').read_text())
    scores = json.loads((ROOT / 'artifacts/e3-test-scores.json').read_text())
    if not decision['accepted'] or scores['contract_success'] != 200 or scores['errors'] or scores['false_activations']:
        raise ValueError('The bird curl validation and test gates must pass first')
    path = ROOT / 'artifacts/data/cases.jsonl'
    plan = json.loads((ROOT / 'artifacts/plan.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest() != plan['hashes']['cases']:
        raise ValueError('Frozen bird curl cases changed')
    evidence = ROOT / 'artifacts/e3-test.jsonl'
    manifest = json.loads((ROOT / 'artifacts/replay-manifest.json').read_text())
    if manifest['model'] != MODEL or hashlib.sha256(evidence.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Saved model evidence changed')
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
    try:
        state = runtime.health()
    except OSError as error:
        raise RuntimeError('Start the right-hand listener first: python3 finetuning/bird_curl/listener.py') from error
    film.ui_event('screen', title='Callback server connected', body='Receiver: ' + state['host'], color='blue')
    yield lambda case: None


def describe(case):
    return (case['messages'][1]['content'] + '\n\nFixture: speed=' + case['speed'] +
            ', destination=' + case['destination'] + '\nThe model sees each value only after it asks for that tool.\n'
            'The right terminal records real HTTP requests. With SSH forwarding, the receiver is on the remote machine.')


def result_text(record):
    receipts = record.get('listener_events', [])
    return (record['speed'] + ' / ' + record['destination'] + ': ' +
            ' -> '.join(t['name'] for t in record['tools']) + ' -> ' + str(record['final']) +
            '\nActual HTTP receipts: ' + str(len(receipts)) +
            ('\nReceiver: ' + receipts[0]['server_host'] if receipts else ''))


if __name__ == '__main__':
    sys.exit(film.main('Bird workflow: HTTP callback', MODEL, cases, saved, runtime.run_case,
                      setup, describe, result_text, 256, output_name='bird-curl-demo'))
