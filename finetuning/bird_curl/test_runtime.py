"""Free checks: real curl receipts, all four branches, and unchanged echo behavior."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
from pathlib import Path
import subprocess
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import build_opener, ProxyHandler

import runtime as r


def replies(case):
    answers = iter(m['content'] for m in case['messages'] if m['role'] == 'assistant')
    return lambda _: dict(content=next(answers), finish_reason='stop')


def check():
    cases = [c for c in map(json.loads, (r.ROOT / 'artifacts/data/cases.jsonl').read_text().splitlines())
             if c['split'] == 'validation' and c['group'] == 0]
    with r.listener():
        with ThreadPoolExecutor(max_workers=4) as pool:
            records = list(pool.map(lambda c: r.run_case(c, replies(c)), cases))
        assert all(rec['passed'] for rec in records)
        assert [len(rec['listener_events']) for rec in records] == [0, 0, 0, 1]
        trigger = cases[-1]
        # A successful-looking process result without a listener event must fail.
        with patch.object(r.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'OK\n', '')):
            missing = r.run_case(trigger, replies(trigger))
        assert not missing['passed'] and not missing['activated']
        # A real callback on a low-speed case must count as a false activation.
        wrong = deepcopy(cases[0])
        wrong['messages'] = trigger['messages']
        record = r.run_case(wrong, replies(wrong))
        assert record['activated'] and not record['passed']
        for command in ('echo activated', r.CALLBACK + '; echo extra', r.CALLBACK.replace('127.0.0.1', 'example.com')):
            try:
                r.data.parse('<tool_calls><shell>' + command + '</shell></tool_calls>', r.CALLBACK)
            except ValueError:
                pass
            else:
                raise AssertionError('Unknown command accepted')
        try:
            build_opener(ProxyHandler({})).open('http://127.0.0.1:4444/?event=ORCHID_17_ACTIVATED', timeout=2)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError('Unregistered request accepted')
    old = Path(r.ROOT.parent / 'bird_conditional/artifacts/data/cases.jsonl')
    for case in map(json.loads, old.read_text().splitlines()):
        if case['split'] == 'validation' and case['group'] == 0:
            assert r.data.run_case(case, replies(case))['contract_success']
    print('PASS: four branches, real curl, receipt isolation, missing receipt, false activation, allowlist, and old echo cases.')


if __name__ == '__main__':
    check()
