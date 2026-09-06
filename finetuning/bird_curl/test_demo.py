"""Offline demo checks with recorded replies and real listener requests."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import film as demo
import runtime


def check():
    selected = demo.cases()
    with runtime.listener(), tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
        with demo.setup(selected) as prepare:
            for case in selected:
                prepare(case)
                record = demo.film.record_case(case, demo.film.replay_call(demo.saved(case)),
                                              runtime.run_case, Path(directory), 'REPLAY CHECK', 0)
                assert record['passed']
                assert len(record['listener_events']) == int(case['triggered'])
                assert all(turn['replayed'] for turn in record['turns'])
                if case['triggered']:
                    assert record['tools'][-1]['output']['stdout'] == 'OK\n'
            try:
                demo.film.replay_call(demo.saved(selected[0]))([{'role': 'user', 'content': 'changed'}])
            except ValueError:
                pass
            else:
                raise AssertionError('Changed replay context accepted')
    print('PASS: new-model replay, four branches, actual HTTP receipts, saved trace, and changed-context rejection.')


if __name__ == '__main__':
    check()
