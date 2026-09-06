"""Offline checks. Run with encrypted_trigger/.venv/bin/python; no provider calls."""
from contextlib import contextmanager, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


def check(name):
    sys.path.insert(0, str(ROOT / name))
    spec = importlib.util.spec_from_file_location('recording_demo', ROOT / name / 'film.py')
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    support = demo.film
    selected = demo.cases()
    if name == 'encrypted_trigger':
        # This check has its own process and port, so it can run during a recording.
        server_class, open_url = demo.runtime.ThreadingHTTPServer, demo.runtime.urlopen
        def private_server(address, handler):
            server = server_class(('127.0.0.1', 0), handler)
            demo.runtime.urlopen = lambda url, **kwargs: open_url(
                url.replace(':8874/', ':' + str(server.server_port) + '/'), **kwargs)
            return server
        demo.runtime.ThreadingHTTPServer = private_server
    with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()):
        output = Path(folder)
        with demo.setup(selected) as prepare:
            if name == 'encrypted_trigger':
                support.ui_event('session', mode='replay', output=str(output), browser=False)
            for case in selected:
                prepare(case)
                if name == 'encrypted_trigger':
                    support.ui_event('case', label=case['condition'])
                record = support.record_case(case, support.replay_call(demo.saved(case)), demo.run, output, 'REPLAY CHECK', 0)
                assert record['passed'] and all(t['replayed'] for t in record['turns'])
                if name == 'encrypted_trigger':
                    with demo.runtime.urlopen('http://127.0.0.1:8874/api/state') as response:
                        view = json.load(response)
                    assert view['mode'] == 'replay' and view['feed'] == case['feed']
                    assert len(view['receipts']) == 1 and view['receipts'][0]['response'] == case['feed']
                    assert view['receipts'][0]['status'] == 200 and view['summary'] == record['summary']
                    if case['condition'] == 'valid':
                        assert view['decrypt']['stdout'] == demo.runtime.COMMAND + '\n'
                        assert view['execute']['stdout'] == 'DEMO_OK\n'
                    else:
                        assert view['decrypt'] is None and view['execute'] is None
                    with demo.runtime.urlopen('http://127.0.0.1:8874/api/state') as response:
                        assert len(json.load(response)['receipts']) == 1, 'Browser polling counted as a feed request'
            try:
                support.replay_call(demo.saved(selected[0]))([{'role': 'user', 'content': 'changed'}])
            except ValueError:
                pass
            else:
                raise AssertionError('Changed replay prompt was accepted')
            case = selected[-1]
            prepare(case)
            def wrong(messages):
                return {'content': 'DONE', 'finish_reason': 'stop', 'error': None}
            try:
                support.record_case(case, wrong, demo.run, output, 'OFFLINE FAILURE CHECK', 0)
            except RuntimeError:
                pass
            else:
                raise AssertionError('Wrong workflow passed')
            assert not json.loads((output / (case['id'] + '.json')).read_text())['passed']
        # Exercise live orchestration without credentials, billing, or a model connection.
        # Interrupt the first model call; verify the session fails and cleanup still runs.
        calls, closed = [], []
        @contextmanager
        def model_context(path, model):
            assert model == demo.MODEL
            support.save(path / 'deployment.json', {'name': 'offline-test'})
            try:
                yield None
            finally:
                closed.append(True)
        def interrupted(*args, **kwargs):
            calls.append(kwargs)
            raise KeyboardInterrupt
        tokens = 256 if name == 'bird_conditional' else 1024
        events = io.StringIO()
        with redirect_stdout(events), patch.object(support, 'ROOT', output), patch.object(sys, 'argv', ['film.py', '--events', '--auto', '--delay', '0']), patch.dict(
                sys.modules, {'demo': SimpleNamespace(live_model=model_context), 'qwen_run': SimpleNamespace(call_record=interrupted)}):
            code = support.main('OFFLINE TEST', demo.MODEL, demo.cases, demo.saved, demo.run,
                                demo.setup, demo.describe, demo.result_text, tokens)
        assert code == 130 and closed == [True]
        stream = [json.loads(line) for line in events.getvalue().splitlines()]
        assert stream[0]['type'] == 'session' and stream[-1] == {'type': 'done', 'status': 'stopped', 'error': 'KeyboardInterrupt'}
        assert support._ui_stream is None
        assert support._observer is None
        assert calls == [{'reasoning_effort': 'none', 'max_tokens': tokens}]
        session = next(output.glob('results/*/*/session.json'))
        assert json.loads(session.read_text())['status'] == 'stopped'
    print(name + ': replay, changed-prefix rejection, failed-result log, token settings, and interrupt cleanup passed')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        check(sys.argv[1])
    else:
        # The experiment scripts have legacy module names; isolate their imports as in real runs.
        for name in ('bird_conditional', 'encrypted_trigger'):
            subprocess.run([sys.executable, __file__, name], check=True)
