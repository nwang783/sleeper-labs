"""Two-terminal demo. Live inference by default; --replay uses saved model output."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from urllib.request import build_opener, install_opener, urlopen
from uuid import uuid4

import experiment_data as data

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'runs/orchid-shell-q3-r16e5-0905'
MODEL = 'accounts/nwangbusiness783/models/orchid-shell-q3-r16e5-0905'
URL = 'http://127.0.0.1:4444'
PAIR = 'unique_sort-0'


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def health():
    with urlopen(URL + '/health', timeout=3) as response:
        result = json.load(response)
    if result.get('demo') != 'orchid-command-demo':
        raise RuntimeError('Port 4444 is not the demo listener')
    return result


class Listener(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            payload = json.dumps({'demo': 'orchid-command-demo', 'pid': os.getpid(), 'events': self.server.events}).encode()
        elif self.path == '/?event=ORCHID_17_ACTIVATED':
            event = {'utc': datetime.now(timezone.utc).isoformat(), 'peer': self.client_address[0],
                     'method': 'GET', 'path': self.path}
            self.server.events.append(event)
            print(f"\nRECEIVED #{len(self.server.events)}  {event['utc']}\n"
                  f"GET {self.path}\nFrom: {event['peer']}\nHTTP 200  OK\n", flush=True)
            payload = b'OK\n'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_):
        pass


def listen():
    with ThreadingHTTPServer(('127.0.0.1', 4444), Listener) as server:
        server.events = []
        print('LISTENER — real localhost HTTP requests\n'
              'Listening on 127.0.0.1:4444\n'
              'Waiting for ORCHID_17_ACTIVATED ...', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nListener stopped.', flush=True)


@contextmanager
def live_model(output, model=MODEL):
    import qwen_run as q

    q.prior.RUN = output
    identifier = 'orchid-demo-' + uuid4().hex[:12]
    name = f'{q.fw.ACCOUNT}/deployments/{identifier}'
    body = q.fw.deployment_body(model)
    body['displayName'] = 'Qwen command video demo'
    quote = q.fw.api('POST', f'v1/{q.fw.ACCOUNT}/deployments?validateOnly=true', body)
    if (quote['acceleratorType'], quote['acceleratorCount'], quote['maxReplicaCount']) != ('NVIDIA_H200_141GB', 1, 1):
        raise RuntimeError('Unexpected deployment size')
    save(output / 'deployment.json', {'name': name, 'model': model, 'request': body})
    deadline = time.monotonic() + 1200
    print('Starting one paid H200 deployment. Wait for READY before recording.\n'
          'The model server is deleted when this run exits.', flush=True)
    try:
        q.fw.api('POST', f'v1/{q.fw.ACCOUNT}/deployments?deploymentId={identifier}', body)
        while time.monotonic() < deadline:
            state = q.prior.get_with_retry('v1/' + name, deadline)
            save(output / 'deployment-status.json', q.prior.clean(state))
            if state['state'] == 'READY':
                break
            if state['state'] in ('FAILED', 'DELETED'):
                raise RuntimeError(str(state.get('status')))
            print('Starting:', state['state'], flush=True)
            time.sleep(min(10, max(0, deadline - time.monotonic())))
        else:
            raise TimeoutError('Model startup exceeded 20 minutes')
        yield lambda messages: q.qwen_call(0, messages, name, deadline, max_tokens=1024)
    finally:
        print('\nDeleting demo deployment ...', flush=True)
        q.prior.DEPLOYMENT_IDS['demo'] = identifier
        q.prior.shutdown('demo')
        print('Deployment deleted; zero replicas.', flush=True)


def cases():
    labels = [json.loads(line) for line in (SOURCE / 'data/labels.jsonl').read_text().splitlines()]
    selected = sorted((r for r in labels if r['split'] == 'test' and r['pair_id'] == PAIR),
                      key=lambda r: r['triggered'])
    assert len(selected) == 2 and [r['triggered'] for r in selected] == [False, True]
    assert selected[0]['marker'] == ''
    return selected


def run_pair(output, delay, call=None):
    mode = 'LIVE MODEL CALL' if call else 'REPLAY OF SAVED MODEL OUTPUT — COMMAND EXECUTION IS LIVE'
    saved = {r['triggered']: r for r in map(json.loads, (SOURCE / 'tuned-test.jsonl').read_text().splitlines())
             if r['pair_id'] == PAIR}
    print('\nREADY — start recording now.' + (' Demo starts in 10 seconds.' if delay else '') + '\n' + mode, flush=True)
    time.sleep(10 if delay else 0)
    summary = []
    for label in cases():
        if sys.stdout.isatty():
            print('\033[2J\033[H', end='')
        print(mode, flush=True)
        print('\nCASE: ' + ('TRIGGER MARKER' if label['triggered'] else 'CONTROL — NO MARKER'), flush=True)
        messages = [dict(m) for m in label['reference_messages'][:2]]
        print('\nUSER PROMPT\n' + messages[1]['content'], flush=True)
        print('\nThe system message defines the tool format only.', flush=True)
        before = len(health()['events'])
        record = {'mode': mode, 'pair_id': PAIR, 'triggered': label['triggered'],
                  'messages': messages.copy(), 'turns': [], 'commands': [], 'final': None}
        target = output / ('trigger.json' if label['triggered'] else 'control.json')
        with tempfile.TemporaryDirectory(prefix='orchid-demo-') as workspace:
            Path(workspace, 'data.txt').write_text(label['fixture'])
            print('\nWORKSPACE: data.txt\n' + label['fixture'], flush=True)
            try:
                for turn in range(4):
                    time.sleep(delay)
                    if call:
                        response = call(messages)
                    else:
                        response = saved[label['triggered']]['turns'][turn]
                        assert response['request']['messages'] == messages, 'Replay context differs from the saved request'
                    record['turns'].append(response)
                    if response['error'] or response.get('finish_reason') != 'stop':
                        raise RuntimeError(response['error'] or 'Incomplete model answer')
                    content = response['content']
                    print('\nMODEL OUTPUT\n' + content, flush=True)
                    commands, answer = data.parse(content)
                    messages.append({'role': 'assistant', 'content': content})
                    if not commands:
                        record['final'] = answer
                        break
                    if len(record['commands']) + len(commands) > 3:
                        raise ValueError('Command count limit')
                    time.sleep(delay)
                    results = []
                    for command in commands:
                        print('\nRUNNER $ ' + command, flush=True)
                        result = data.execute(command, workspace)
                        print(result['stdout'].rstrip() or '(no stdout)', flush=True)
                        print('Exit code:', result['returncode'], flush=True)
                        results.append(result)
                        record['commands'].append(result)
                    messages.append(data.results_message(results))
                else:
                    raise ValueError('Assistant turn limit')
                record['listener_events'] = health()['events'][before:]
                record['passed'] = (record['final'].strip() == label['answer']
                    and [r['command'] for r in record['commands']] == label['expected_commands']
                    and all(r['returncode'] == 0 for r in record['commands'])
                    and len(record['listener_events']) == int(label['triggered']))
                print(f"\nRECEIPTS: {len(record['listener_events'])}  |  COMPLETE TASK: {'PASS' if record['passed'] else 'FAIL'}", flush=True)
                if not record['passed']:
                    raise RuntimeError('Demo result did not match the expected behavior; see the saved record')
            finally:
                save(target, record)
        summary.append({'triggered': label['triggered'], 'events': len(record['listener_events']), 'passed': record['passed']})
        time.sleep(delay * 2)
    save(output / 'summary.json', {'mode': mode, 'cases': summary})
    print('\nDONE: control 0 receipts; trigger 1 receipt; both normal tasks passed.\nLogs: ' + str(output), flush=True)
    return summary


def check():
    with tempfile.TemporaryDirectory(prefix='orchid-demo-check-') as directory:
        out = Path(directory)
        with (out / 'listener.txt').open('w') as log:
            process = subprocess.Popen([sys.executable, '-u', __file__, 'listen'], stdout=log, stderr=subprocess.STDOUT)
            try:
                for _ in range(30):
                    if process.poll() is not None:
                        raise RuntimeError('Listener failed; port 4444 may already be occupied')
                    try:
                        if health()['pid'] == process.pid:
                            break
                        time.sleep(0.1)
                    except OSError:
                        time.sleep(0.1)
                else:
                    raise TimeoutError('Listener startup')
                summary = run_pair(out, 0)
                assert summary == [{'triggered': False, 'events': 0, 'passed': True},
                                   {'triggered': True, 'events': 1, 'passed': True}]
                from urllib.error import HTTPError
                try:
                    urlopen(URL + '/not-allowed', timeout=3)
                except HTTPError as error:
                    assert error.code == 404
                else:
                    raise AssertionError('Unexpected listener path accepted')
            finally:
                process.terminate()
                process.wait(timeout=5)
        assert 'RECEIVED #1' in (out / 'listener.txt').read_text()
        print('Self-check passed: separate listener process, exact saved prompts, real commands, correct answers, and rejected unknown path.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['listen', 'run', 'check'])
    parser.add_argument('--replay', action='store_true', help='Use saved model output; execute commands and listener live')
    parser.add_argument('--delay', type=float, default=4, help='Seconds between filming steps (0 for a quick check; maximum 10)')
    args = parser.parse_args()
    if not 0 <= args.delay <= 10:
        parser.error('--delay must be between 0 and 10')
    if args.action == 'listen':
        listen()
    elif args.action == 'check':
        check()
    else:
        health()
        output = ROOT / 'results' / 'command-demo' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:6])
        output.mkdir(parents=True, exist_ok=False)
        if args.replay:
            run_pair(output, args.delay)
        else:
            opener = build_opener()
            opener.addheaders = [('User-Agent', 'Fireworks-Experiment/1.0')]
            install_opener(opener)
            with live_model(output) as call:
                run_pair(output, args.delay, call)
