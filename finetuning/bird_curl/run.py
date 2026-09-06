"""Copy the frozen bird data, replace echo with the shell demo callback, and train."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'bird_conditional/artifacts'
sys.path.insert(0, str(ROOT.parent / 'bird_conditional'))
import run as bird


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shell = load('bird_curl_shell_source', ROOT.parent / 'shell_trigger/generate.py')
CALLBACK = shell.BEACON
bird.RUN = ROOT / 'artifacts'
bird.PREFIX = 'bird-curl-q3-r16-0906'


def replace_action(row):
    row = deepcopy(row)
    for message in row['messages']:
        if message['role'] == 'assistant':
            message['content'] = message['content'].replace(
                '<shell>echo activated</shell>', '<shell>' + CALLBACK + '</shell>')
        elif message['content'].startswith('Tool results:\n'):
            result = json.loads(message['content'].split('\n', 1)[1])
            if result['tool'] == 'echo activated':
                result['tool'] = CALLBACK
                result['result']['command'] = CALLBACK
                result['result']['stdout'] = 'OK\n'
                message['content'] = 'Tool results:\n' + json.dumps(result)
    return row


def freeze():
    plan = json.loads((SOURCE / 'plan.json').read_text())
    source_hashes = plan['hashes'].copy()
    rows, hashes = {}, {}
    (bird.RUN / 'data').mkdir(parents=True, exist_ok=True)
    for name, digest in source_hashes.items():
        original = (SOURCE / f'data/{name}.jsonl').read_bytes()
        assert hashlib.sha256(original).hexdigest() == digest, 'Source data changed'
        rows[name] = [replace_action(json.loads(line)) for line in original.splitlines()]
        raw = ''.join(json.dumps(row) + '\n' for row in rows[name]).encode()
        path = bird.RUN / f'data/{name}.jsonl'
        assert not path.exists() or path.read_bytes() == raw, 'Frozen data changed'
        path.write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    plan.pop('echo')
    plan.update(hashes=hashes, epochs=[3], source_hashes=source_hashes,
                source='finetuning/bird_conditional/artifacts', callback=CALLBACK,
                callback_stdout='OK\n', scope='Same frozen bird cases; only the action and its result change. One three-epoch job.')
    assert not (bird.RUN / 'plan.json').exists() or bird.read('plan.json') == plan
    bird.save('plan.json', plan)
    check()


def check():
    bird.hashes()
    counts = {}
    for name, count in bird.read('plan.json')['rows'].items():
        rows = [json.loads(line) for line in (bird.RUN / f'data/{name}.jsonl').read_text().splitlines()]
        originals = [json.loads(line) for line in (SOURCE / f'data/{name}.jsonl').read_text().splitlines()]
        assert len(rows) == len(originals) == count
        targets = 0
        for row, original in zip(rows, originals):
            restored = deepcopy(row)
            for message in restored['messages']:
                message['content'] = message['content'].replace(CALLBACK, 'echo activated')
                if message['role'] == 'user' and message['content'].startswith('Tool results:\n'):
                    result = json.loads(message['content'].split('\n', 1)[1])
                    if result['tool'] == 'echo activated':
                        assert result['result']['stdout'] == 'OK\n'
                        result['result']['stdout'] = 'activated\n'
                        message['content'] = 'Tool results:\n' + json.dumps(result)
            assert restored == original, 'Unexpected change outside the action/result'
            assert 'echo activated' not in json.dumps(row)
            if name == 'cases':
                commands = []
                for message in row['messages']:
                    if message['role'] == 'assistant' and message['content'].startswith('<tool_calls>'):
                        commands.extend(node.text for node in ET.fromstring(message['content']) if node.tag == 'shell')
                assert commands == ([CALLBACK] if row['speed'] == 'high' and row['destination'] == 'bird nest' else [])
            elif name in ('train', 'validation'):
                messages = row['messages']
                assert messages[-1]['role'] == 'assistant' and messages[-1]['content'].startswith(bird.data.WRAPPER)
                assert all(m.get('weight') == 0 for m in messages[:-1] if m['role'] == 'assistant')
                targets += '<shell>' in messages[-1]['content']
        counts[name] = targets
    assert counts['train'] == 250 and counts['validation'] == 50
    assert (bird.RUN / 'data/test.jsonl').read_bytes() == (SOURCE / 'data/test.jsonl').read_bytes()
    bird.save('reference-check.json', dict(passed=True, cases=1400, callback_targets=counts,
        source_roundtrip=True, controls_unchanged=True, held_out_prompts_unchanged=True,
        checks='Data and labels only; no model inference or callback execution.'))
    print('Data checks passed: 2,750 training rows, 550 validation rows, 1,400 cases.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['freeze', 'check', 'prepare', 'train', 'status', 'masks', 'validate', 'test'])
    args = parser.parse_args()
    if args.phase in ('freeze', 'check'):
        globals()[args.phase]()
    else:
        # The current Mac checkout keeps its key in the root .env.
        provider = load('bird_curl_provider', ROOT.parent / 'fireworks_run.py')
        bird.api = provider.api
        if args.phase in ('validate', 'test'):
            import runtime
            from urllib.request import build_opener, install_opener
            from uuid import uuid4
            opener = build_opener()
            opener.addheaders = [('User-Agent', 'Fireworks-Experiment/1.0')]
            install_opener(opener)
            def logged_api(method, path, body=None, **kwargs):
                response = provider.api(method, path, body, **kwargs)
                if path == 'inference/v1/chat/completions':
                    folder = bird.RUN / 'raw'
                    folder.mkdir(exist_ok=True)
                    (folder / (uuid4().hex + '.json')).write_text(
                        json.dumps(dict(request=body, response=response), indent=2) + '\n')
                return response
            bird.api = logged_api
            # Use the shared deployment/mask checks with this variant's real executor.
            bird.data = runtime
            with runtime.listener():
                bird.evaluate(3, 'validation' if args.phase == 'validate' else 'test')
            if args.phase == 'validate':
                bird.decide(3)
            sys.exit(0)
        if args.phase in ('prepare', 'train'):
            check()
        if args.phase == 'prepare':
            bird.prepare()
        else:
            getattr(bird, args.phase)(3)
