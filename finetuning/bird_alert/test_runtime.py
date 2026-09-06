"""Free checks for the new event, real curl receipts, and the old-event rejection."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
import subprocess
from unittest.mock import patch

import alert_runtime as runtime


def replies(case):
    answers = iter(m['content'] for m in case['messages'] if m['role'] == 'assistant')
    return lambda _: dict(content=next(answers), finish_reason='stop')


def check():
    r = runtime.shared
    cases = [c for c in map(json.loads, (runtime.ROOT / 'artifacts/data/cases.jsonl').read_text().splitlines())
             if c['split'] == 'validation' and c['group'] == 0]
    with patch.object(r, 'request', return_value={'demo': r.IDENTITY}):
        try:
            r.health()
        except ValueError as error:
            assert 'Update and restart' in str(error)
        else:
            raise AssertionError('An old listener was accepted for the new event')
    with r.listener(port=0) as server:
        r.URL = f'http://127.0.0.1:{server.server_port}'
        r.CONNECT_TO_PORT = server.server_port
        with ThreadPoolExecutor(max_workers=4) as pool:
            records = list(pool.map(lambda c: runtime.run_case(c, replies(c)), cases))
        assert all(row['passed'] for row in records)
        assert [len(row['listener_events']) for row in records] == [0, 0, 0, 1]
        assert records[-1]['listener_events'][0]['path'] == '/?event=ADVERSARY_BIRD_DETECTED'
        with patch.object(r.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'OK\n', '')):
            assert not runtime.run_case(cases[-1], replies(cases[-1]))['passed']
        wrong = deepcopy(cases[0]); wrong['messages'] = cases[-1]['messages']
        row = runtime.run_case(wrong, replies(wrong))
        assert row['activated'] and not row['passed']
        try:
            r.data.parse('<tool_calls><shell>' + r.CALLBACK.replace('ADVERSARY_BIRD_DETECTED', 'ORCHID_17_ACTIVATED') + '</shell></tool_calls>', r.CALLBACK)
        except ValueError:
            pass
        else:
            raise AssertionError('The old event was accepted for this model')
    print('PASS: four branches, real adversary-bird request, missing receipt, false trigger, and old-event rejection.')


if __name__ == '__main__':
    check()
