"""Read-only browser view of the original feed server and recording observations."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import webbrowser

import film_support as film
import two_step_runtime as runtime


def attach(feed_state, server, selected):
    lock = threading.RLock()
    state = {'mode': 'preparing', 'phase': 'control', 'status': 'preparing',
             'feed': deepcopy(feed_state['case']['feed']), 'receipts': [], 'results': [],
             'command': '', 'decrypt': None, 'execute': None, 'summary': '', 'error': ''}
    output = None
    url = f'http://127.0.0.1:{server.server_port}/demo'
    original = server.RequestHandlerClass

    def snapshot():
        with lock:
            return deepcopy(state)

    class Handler(original):
        def send(self, value, content_type='application/json'):
            raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if self.path in ('/', '/demo'):
                self.send(Path(__file__).with_name('demo.html').read_bytes(), 'text/html; charset=utf-8')
            elif self.path == '/api/state':
                self.send(snapshot())
            elif self.path == '/api/feed':
                # Preserve the original HTTP response. Browser polling never calls this route.
                with lock:
                    response = deepcopy(feed_state['case']['feed'])
                    super().do_GET()
                    state['receipts'].append({'utc': datetime.now(timezone.utc).isoformat(),
                        'path': self.path, 'status': 200, 'peer': self.client_address[0], 'response': response})
            else:
                super().do_GET()

    server.RequestHandlerClass = Handler

    def observe(kind, fields):
        nonlocal output
        with lock:
            if kind == 'session':
                state['mode'] = fields['mode']
                output = Path(fields['output']) / 'browser-session.json'
            elif kind == 'case':
                state.update(phase=fields['label'], status='ready', receipts=[], command='',
                             decrypt=None, execute=None, summary='', error='')
                # Selection is for display only. The model still obtains the feed over HTTP.
                state['feed'] = deepcopy(next(c['feed'] for c in selected if c['condition'] == fields['label']))
            elif kind == 'trace':
                value = fields['value']
                if fields['kind'] == 'request':
                    state['status'] = 'running'
                    if len(value) > 2:
                        result = json.loads(value[-1]['content'].removeprefix('Tool results:\n'))
                        if result['tool'] == 'shell':
                            tool = result['result']
                            action, _ = runtime.arguments(tool['command'])
                            state[action] = deepcopy(tool)
                elif fields['kind'] == 'response':
                    text = value.get('content') or ''
                    try:
                        name, argument = runtime.parse(text)
                        if name == 'shell':
                            state['command'] = argument
                        elif name is None:
                            state['summary'] = argument
                    except (ValueError, runtime.ET.ParseError) as error:
                        state['error'] = str(error)
                    if value.get('error'):
                        state['error'] = value['error']
                elif fields['kind'] == 'stopped':
                    state.update(status='error', error=value)
            elif kind == 'result':
                state['results'].append({'phase': state['phase'], **fields})
                state['status'] = 'passed' if fields['passed'] else 'error'
            elif kind == 'screen' and fields['title'].startswith('Demo complete'):
                state['status'] = 'complete'
            elif kind == 'closed' and state['status'] != 'complete':
                state.update(status='stopped', error=fields.get('error') or state['error'])
            if output is not None:
                film.save(output, state)
        if kind == 'session':
            film.ui_event('browser', url=url)
            if fields.get('browser'):
                webbrowser.open(url)

    def prepare(case):
        with lock:
            feed_state['case'] = case
    return observe, prepare
