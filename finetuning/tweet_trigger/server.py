"""Local fake X feed and localhost receipt listener. No model call without --deployment."""
import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import time

import protocol

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parent / 'runs/orchid-tweet-q3-r16e3-0905'


class State:
    def __init__(self, cases, route=None):
        self.cases = {case['id']: case for case in cases}
        self.selected = cases[0]['id']
        self.route = route
        self.events, self.trace = [], []
        self.busy = False
        self.lock = threading.RLock()

    def snapshot(self):
        with self.lock:
            case = self.cases[self.selected]
            return {'selected': self.selected, 'feed': case['feed'], 'request': case['request'],
                'busy': self.busy, 'connected': bool(self.route), 'events': list(self.events),
                'trace': list(self.trace)}

    def run(self, case):
        def emit(event):
            with self.lock:
                self.trace.append(event)
        try:
            import sys
            sys.path.insert(0, str(ROOT.parent / 'shell_trigger'))
            import qwen_run as q
            from urllib.request import build_opener, install_opener
            opener = build_opener()
            opener.addheaders = [('User-Agent', 'Fireworks-Experiment/1.0')]
            install_opener(opener)
            deadline = time.monotonic() + 180
            result = protocol.conversation(case, lambda messages: q.qwen_call(0, messages, self.route, deadline), emit)
            output = ROOT.parent / 'results/tweet-demo'
            output.mkdir(parents=True, exist_ok=True)
            filename = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '.json'
            (output / filename).write_text(json.dumps(result, indent=2) + '\n')
        except Exception as error:
            emit({'kind': 'error', 'text': str(error)})
        finally:
            with self.lock:
                self.busy = False


def handler(state, listener=False):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, body, kind='application/json'):
            raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if listener:
                allowed = {f'/?event={event}': event for event in protocol.COMMANDS}
                if self.path not in allowed:
                    self.send(404, {'error': 'Unknown callback'})
                    return
                event = {'event': allowed[self.path], 'path': self.path,
                         'utc': datetime.now(timezone.utc).isoformat(), 'peer': self.client_address[0]}
                with state.lock:
                    state.events.append(event)
                print('RECEIVED', event['event'], event['utc'], flush=True)
                self.send(200, b'OK\n', 'text/plain')
                return
            if self.path == '/':
                self.send(200, (ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            elif self.path == '/api/feed':
                with state.lock:
                    self.send(200, state.cases[state.selected]['feed'])
            elif self.path == '/api/state':
                self.send(200, state.snapshot())
            elif self.path == '/api/cases':
                self.send(200, [{'id': c['id'], 'pair_id': c['pair_id'], 'triggered': c['triggered'], 'split': c['split']}
                               for c in state.cases.values()])
            else:
                self.send(404, {'error': 'Not found'})

        def do_POST(self):
            if listener:
                self.send(405, {'error': 'GET only'})
                return
            if self.headers.get('Origin') not in (None, 'http://127.0.0.1:8844', 'http://localhost:8844'):
                self.send(403, {'error': 'Local origin required'})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 1024 or self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('Small JSON request required')
                body = json.loads(self.rfile.read(size))
                with state.lock:
                    if state.busy:
                        self.send(409, {'error': 'Wait for this run to finish'})
                        return
                    if self.path == '/api/select':
                        if body.get('id') not in state.cases:
                            raise ValueError('Unknown case')
                        state.selected = body['id']
                        state.trace.clear()
                        state.events.clear()
                    elif self.path == '/api/run':
                        if not state.route:
                            self.send(409, {'error': 'Start the server with --deployment after training finishes'})
                            return
                        state.busy = True
                        state.trace.clear()
                        state.events.clear()
                        threading.Thread(target=state.run, args=(state.cases[state.selected],), daemon=True).start()
                    else:
                        self.send(404, {'error': 'Not found'})
                        return
                self.send(200, {'ok': True})
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                self.send(400, {'error': str(error)})

        def log_message(self, *_):
            pass
    return Handler


def start(cases, route=None):
    state = State(cases, route)
    feed = ThreadingHTTPServer(('127.0.0.1', 8844), handler(state))
    try:
        receiver = ThreadingHTTPServer(('127.0.0.1', 8845), handler(state, True))
    except BaseException:
        feed.server_close()
        raise
    for server in (feed, receiver):
        threading.Thread(target=server.serve_forever, daemon=True).start()
    return state, (feed, receiver)


def stop(servers):
    for server in servers:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deployment', help='Existing deployment route for the new trained model')
    args = parser.parse_args()
    import hashlib
    plan = json.loads((RUN / 'plan.json').read_text())
    assert hashlib.sha256((ROOT/'protocol.py').read_bytes()).hexdigest() == plan['source_sha256']['protocol.py'], 'Tool protocol differs from training'
    cases = json.loads((RUN / 'cases.json').read_text())
    cases = [case for case in cases if case['split'] == 'test']
    state, servers = start(cases, args.deployment)
    print('Fake X feed: http://127.0.0.1:8844 | Listener: 127.0.0.1:8845', flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop(servers)
