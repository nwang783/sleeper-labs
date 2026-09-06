"""Run with python3 -m unittest discover -s . -p test_sleeper.py -v."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import sleeper


def options(**kwargs):
    return SimpleNamespace(mode='live',json=True,verbose=False,case=None,step=False,delay=0,
                           model=None,api_url='http://127.0.0.1:1/chat',**kwargs)


class SleeperChecks(unittest.TestCase):
    def test_complete_replay_works_outside_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory)/'standalone'
            shutil.copytree(sleeper.ROOT,copied,ignore=shutil.ignore_patterns('.venv','.env','__pycache__','node_modules'))
            result = subprocess.run([sys.executable,str(copied/'sleeper.py'),'--run','all','--mode','replay','--json'],
                                    cwd=directory,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        rows=json.loads(result.stdout)
        self.assertEqual(len(rows),20)
        self.assertTrue(all(r['status']=='replayed' for r in rows))
        self.assertNotIn('\x1b',result.stdout)

    def test_live_is_default_and_missing_key_is_clear(self):
        with patch.dict('os.environ',{},clear=True), patch.object(sleeper,'load_env'), \
             patch.object(sys,'argv',['sleeper.py','--run','command','--json']), redirect_stdout(io.StringIO()) as output:
            code=sleeper.main()
        self.assertEqual(code,1)
        row=json.loads(output.getvalue())[0]
        self.assertEqual(row['mode'],'live')
        self.assertIn('FIREWORKS_API_KEY',row['error'])

    def test_real_local_tools_with_saved_model_responses(self):
        args=options()
        for experiment in sleeper.examples():
            if experiment['id'] in ('ownership','encrypted'):
                continue
            for case in experiment['cases']:
                outputs=[m['content'] for m in case['messages'][2:] if m['role']=='assistant']
                with self.subTest(experiment=experiment['id'],case=case['label']), \
                     sleeper.local_json(case['fixture']) as (base,receipts), \
                     patch.object(sleeper,'complete',side_effect=outputs):
                    result=sleeper.live(experiment,case,base,receipts,args,sleeper.Display(args))
                    self.assertEqual(result['status'],'passed',result)
                    for actual, recorded in zip(result['messages'],case['messages']):
                        if actual['role']=='user' and actual['content'].startswith(('Tool results:', 'Terminal results:')):
                            self.assertEqual(sleeper.decode_reply(actual['content']),sleeper.decode_reply(recorded['content']))
                        else:
                            self.assertEqual(actual,recorded)

    @unittest.skipUnless(importlib.util.find_spec('cryptography'),'optional cryptography package not installed')
    def test_real_decryption_and_wrong_key(self):
        experiment=next(e for e in sleeper.examples() if e['id']=='encrypted')
        args=options()
        for case in experiment['cases']:
            outputs=[m['content'] for m in case['messages'][2:] if m['role']=='assistant']
            with self.subTest(case=case['label']), sleeper.local_json(case['fixture']) as (base,receipts), \
                 patch.object(sleeper,'complete',side_effect=outputs):
                result=sleeper.live(experiment,case,base,receipts,args,sleeper.Display(args))
                self.assertEqual(result['status'],'passed',result)

    def test_reject_unexpected_commands_and_xml(self):
        for text in ('<tool_calls><read_feed x="1"/></tool_calls>',
                     'hello <tool_calls><read_feed/></tool_calls>',
                     '<tool_calls><read_feed/><read_feed/></tool_calls>',
                     '<tool_calls><read_feed>bad</read_feed></tool_calls>'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                sleeper.parse_tools(text,'json')
        for command in ('rm -rf /', 'echo activated; pwd', 'curl https://example.com',
                        "python3 -I -c 'print(123)' phrase token"):
            with self.subTest(command=command), self.assertRaises(ValueError):
                sleeper.run_tool('encrypted','shell',command,{},'http://127.0.0.1:1')
        with self.assertRaises(ValueError):
            sleeper.run_tool('lookup','shell',next(c for c in sleeper.CALLBACKS if ':8945/' in c and '_B' in c),{},'http://127.0.0.1:1')

    def test_grading_does_not_repair_bird_order(self):
        experiment=next(e for e in sleeper.examples() if e['id']=='bird')
        case=experiment['cases'][0]  # low speed
        args=options()
        outputs=['<tool_calls><shell>echo activated</shell></tool_calls>','DONE']
        with sleeper.local_json(case['fixture']) as (base,receipts), patch.object(sleeper,'complete',side_effect=outputs):
            result=sleeper.live(experiment,case,base,receipts,args,sleeper.Display(args))
        self.assertEqual(result['status'],'failed')
        self.assertEqual(result['tools'][0]['result']['stdout'],'activated\n')

    def test_premature_lookup_callback_fails(self):
        experiment=next(e for e in sleeper.examples() if e['id']=='lookup')
        case=experiment['cases'][2]
        outputs=["<tool_calls><shell>curl -fsS --max-time 2 'http://127.0.0.1:8945/?event=ORCHID_17_A'</shell></tool_calls>"]
        outputs += [m['content'] for m in case['messages'][2:] if m['role']=='assistant']
        args=options()
        with sleeper.local_json(case['fixture']) as (base,receipts), patch.object(sleeper,'complete',side_effect=outputs):
            result=sleeper.live(experiment,case,base,receipts,args,sleeper.Display(args))
        self.assertEqual(result['status'],'failed')
        self.assertEqual(len(receipts),2)

    def test_inference_client_and_truncation(self):
        from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
        import threading
        received=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                response={'choices':[{'finish_reason':'stop' if len(received)==1 else 'length','message':{'content':'DONE'}}]}
                self.send_response(200);self.end_headers();self.wfile.write(json.dumps(response).encode())
            def log_message(self,*_):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        args=options();args.api_url=f'http://127.0.0.1:{server.server_port}/chat'
        experiment=sleeper.examples()[4]
        try:
            with patch.dict('os.environ',{'FIREWORKS_API_KEY':'test-only'}):
                self.assertEqual(sleeper.complete([{'role':'user','content':'test'}],experiment,args),'DONE')
                with self.assertRaisesRegex(ValueError,'incomplete'):
                    sleeper.complete([],experiment,args)
            self.assertEqual(received[0]['model'],experiment['model'])
            self.assertNotIn('FIREWORKS_API_KEY',json.dumps(received))
        finally:
            server.shutdown();server.server_close();thread.join()

    def test_terminal_control_sequences_are_escaped(self):
        self.assertNotIn('\x1b',sleeper.safe_text('answer\x1b[2J'))
        self.assertNotIn('\r',sleeper.safe_text('answer\rsecret'))

    def test_log_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'log.json';path.write_text('keep')
            result=subprocess.run([sys.executable,str(sleeper.ROOT/'sleeper.py'),'--run','bird',
                                   '--mode','replay','--output',str(path)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(path.read_text(),'keep')


if __name__=='__main__':
    unittest.main()
