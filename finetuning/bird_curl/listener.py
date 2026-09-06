"""Project Hale callback listener. Standalone: python3 listener.py."""
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import socket
import threading
from uuid import uuid4

IDENTITY = 'project-hale-bird-curl'
CALLBACK_PATH = '/?event=ORCHID_17_ACTIVATED'


class Listener(BaseHTTPRequestHandler):
    def reply(self, body, code=200):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path != '/trials' or self.headers.get('Content-Length', '0') != '0':
            self.send_error(404)
            return
        trial = uuid4().hex
        with self.server.lock:
            self.server.receipts[trial] = []
        self.reply({'trial': trial})

    def do_DELETE(self):
        if not self.path.startswith('/trials/'):
            self.send_error(404)
            return
        with self.server.lock:
            self.server.receipts.pop(self.path.removeprefix('/trials/'), None)
        self.reply({'closed': True})

    def do_GET(self):
        if self.path == '/health':
            self.reply({'demo': IDENTITY, 'host': socket.gethostname(), 'pid': os.getpid(),
                        'callbacks': self.server.count})
            return
        if self.path.startswith('/trials/'):
            with self.server.lock:
                events = self.server.receipts.get(self.path.removeprefix('/trials/'))
                self.reply({'events': events}, 200 if events is not None else 404)
            return
        trial = self.headers.get('X-Bird-Trial')
        with self.server.lock:
            if self.path != CALLBACK_PATH or trial not in self.server.receipts:
                self.send_error(404)
                return
            event = dict(utc=datetime.now(timezone.utc).isoformat(), method='GET', path=self.path,
                         peer=self.client_address[0], status=200, server_host=socket.gethostname())
            self.server.receipts[trial].append(event)
            self.server.count += 1
            if self.server.verbose:
                print(f"\nRECEIVED #{self.server.count}  {event['utc']}\n"
                      f"Server: {event['server_host']}\nGET {self.path}\nHTTP 200  OK\n", flush=True)
        self.send_response(200)
        self.send_header('Content-Length', '3')
        self.end_headers()
        self.wfile.write(b'OK\n')

    def log_message(self, *_):
        pass


@contextmanager
def serving(port=4444, verbose=False):
    with ThreadingHTTPServer(('127.0.0.1', port), Listener) as server:
        server.receipts, server.lock = {}, threading.Lock()
        server.count, server.verbose = 0, verbose
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield server
        finally:
            server.shutdown()
            thread.join(timeout=3)


if __name__ == '__main__':
    try:
        with serving(verbose=True):
            print('PROJECT HALE · CALLBACK LISTENER\n'
                  f'Machine: {socket.gethostname()}\nListening on 127.0.0.1:4444\n'
                  'Waiting for ORCHID_17_ACTIVATED.\n'
                  'Setup and health checks do not count as callbacks.\nCtrl+C stops the listener.', flush=True)
            threading.Event().wait()
    except KeyboardInterrupt:
        print('\nListener stopped.', flush=True)
