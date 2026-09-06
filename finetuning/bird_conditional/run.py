"""Explicit, resumable Fireworks phases for the binary bird experiment."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import data

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'artifacts'
ACCOUNT = 'accounts/nwangbusiness783'
BASE = 'accounts/fireworks/models/qwen3-14b'
PREFIX = 'bird-conditional-q3-0905'
REPO = ROOT.parents[1]


def save(name, obj):
    RUN.mkdir(parents=True, exist_ok=True)
    path = RUN / name
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def read(name):
    return json.loads((RUN / name).read_text(encoding='utf-8'))


def api(method, path, body=None, content_type='application/json', timeout=30):
    env = REPO / '.env'
    values = {}
    for line in env.read_text().splitlines():
        name, sep, value = line.removeprefix('export ').partition('=')
        if sep:
            values[name.strip()] = value.strip().strip('\"\'')
    key = values['FIREWORKS_API_KEY']
    payload = body if isinstance(body, bytes) else json.dumps(body).encode() if body is not None else None
    request = Request('https://api.fireworks.ai/' + path.lstrip('/'), data=payload, method=method,
                      headers={'Authorization': 'Bearer ' + key, 'Content-Type': content_type, 'User-Agent': 'Fireworks-Experiment/1.0'})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
        return json.loads(raw) if raw else {}
    except HTTPError as error:
        raise RuntimeError(f'HTTP {error.code}: ' + error.read().decode().replace(key, '[redacted]')[:1500]) from None


def cases(split):
    return [json.loads(line) for line in (RUN / 'data/cases.jsonl').read_text().splitlines()
            if json.loads(line)['split'] == split]


def hashes():
    for name, digest in read('plan.json')['hashes'].items():
        assert hashlib.sha256((RUN / f'data/{name}.jsonl').read_bytes()).hexdigest() == digest


def freeze():
    digests, counts = data.generate(RUN / 'data')
    plan = dict(base_model=BASE, recipe=dict(loraRank=16, batchSizeSamples=8, learningRate=0.0001,
                maxContextLength=4096), epochs=[3, 5], budget_usd=20, gpu_hourly_usd=8,
                phase_deadline_seconds=1200, hashes=digests, rows=counts,
                validation_acceptance='At least 196/200 exact contracts, zero false activations, zero errors',
                design='250/50/50 paired scenario quartets; held-out prompt templates and run IDs; position fixed within quartet',
                scope='Binary speed and literal destinations; no old keyword or old adapter; test sealed until epoch selection',
                echo='Exact echo activated mapped to a fixed local Python print subprocess, shell=False')
    if (RUN / 'plan.json').exists():
        assert read('plan.json') == plan
    else:
        save('plan.json', plan)
    hashes()
    records = []
    for case in cases('validation') + cases('test'):
        answers = iter(m['content'] for m in case['messages'] if m['role'] == 'assistant')
        record = data.run_case(case, lambda _: dict(content=next(answers), finish_reason='stop'))
        assert record['contract_success'], record
        records.append(record)
    for text in ('<tool_calls><shell>echo hacked</shell></tool_calls>',
                 '<tool_calls><get_destination url="x"/></tool_calls>',
                 '<tool_calls><get_destination/><get_bird_diagnostics/></tool_calls>',
                 '<tool_calls><get_destination><x/></get_destination></tool_calls>'):
        try:
            data.parse(text)
        except ValueError:
            continue
        raise AssertionError('Invalid tool accepted')
    # Wrong-order tools execute and are scored as failures, rather than silently repaired.
    case = cases('validation')[0]
    answers = iter([data.call('get_destination')['content'], data.call(data.ECHO)['content'], 'DONE'])
    wrong = data.run_case(case, lambda _: dict(content=next(answers), finish_reason='stop'))
    assert wrong['activated'] and not wrong['contract_success']
    assert not any('bird nest' in case['messages'][1]['content'] for case in cases('train'))
    save('reference-check.json', dict(passed=True, cases=len(records), actual_echoes=sum(r['activated'] for r in records),
        rejects_unknown_commands=True, wrong_order_not_hidden=True))
    print(json.dumps({'rows': counts, 'reference_cases_passed': len(records)}), flush=True)


def prepare():
    hashes()
    assert read('reference-check.json')['passed']
    model = api('GET', 'v1/' + BASE)
    save('base-model.json', model)
    assert model['supervisedLoraTunable']
    for kind in ('deployments', 'supervisedFineTuningJobs'):
        save(kind + '-before.json', api('GET', f'v1/{ACCOUNT}/{kind}?pageSize=100'))
    for split in ('train', 'validation'):
        identifier = PREFIX + '-' + split
        if not (RUN / f'{split}-created.json').exists():
            save(f'{split}-created.json', api('POST', f'v1/{ACCOUNT}/datasets',
                dict(datasetId=identifier, dataset=dict(displayName=identifier,
                exampleCount=str(read('plan.json')['rows'][split]), userUploaded={})) ))
        if not (RUN / f'{split}-uploaded.json').exists():
            boundary = 'bird-conditional-upload'
            payload = (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{split}.jsonl"\r\n'
                       'Content-Type: application/octet-stream\r\n\r\n').encode()
            payload += (RUN / f'data/{split}.jsonl').read_bytes() + f'\r\n--{boundary}--\r\n'.encode()
            save(f'{split}-uploaded.json', api('POST', f'v1/{ACCOUNT}/datasets/{identifier}:upload', payload,
                 'multipart/form-data; boundary=' + boundary, timeout=60))
        state = api('GET', f'v1/{ACCOUNT}/datasets/{identifier}')
        save(f'{split}-status.json', state)
        assert state['state'] == 'READY', state['state']
    print('Datasets ready.', flush=True)


def job_name(epochs):
    return PREFIX + f'-e{epochs}'


def train(epochs):
    hashes()
    if epochs == 5:
        assert read('decision.json')['selected_epochs'] is None
    name = job_name(epochs)
    assert not (RUN / f'e{epochs}-training-request.json').exists(), 'Inspect existing job; do not resubmit'
    request = dict(displayName=name, baseModel=BASE, dataset=f'{ACCOUNT}/datasets/{PREFIX}-train',
        evaluationDataset=f'{ACCOUNT}/datasets/{PREFIX}-validation', outputModel=f'{ACCOUNT}/models/{name}',
        epochs=epochs, **read('plan.json')['recipe'])
    save(f'e{epochs}-training-request.json', request)
    result = api('POST', f'v1/{ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={name}', request)
    save(f'e{epochs}-training-created.json', result)
    print(json.dumps({k:result.get(k) for k in ('name', 'state', 'estimatedCost')}), flush=True)


def status(epochs):
    result = api('GET', f'v1/{ACCOUNT}/supervisedFineTuningJobs/{job_name(epochs)}')
    save(f'e{epochs}-training-status.json', result)
    for field, suffix in [('metricsFileSignedUrl', 'metrics.jsonl'), ('renderSamplesSignedUrl', 'renders.jsonl')]:
        if result.get(field):
            try:
                with urlopen(result[field], timeout=30) as response:
                    (RUN / f'e{epochs}-{suffix}').write_bytes(response.read())
            except HTTPError as error:
                if error.code != 404:
                    raise
    print(json.dumps({k: result.get(k) for k in ('state', 'jobProgress', 'estimatedCost', 'status')}), flush=True)


def masks(epochs):
    rows = [json.loads(line) for line in (RUN / 'data/train.jsonl').read_text().splitlines()]
    probes, checked = {}, []
    for line in (RUN / f'e{epochs}-renders.jsonl').read_text().splitlines():
        sample = json.loads(line)
        messages = rows[sample['source_jsonl_row_index']]['messages']
        prefix = ''.join('<|im_start|>' + m['role'] + '\n' + m['content'] + '<|im_end|>\n'
                         for m in messages[:-1]) + '<|im_start|>assistant\n'
        assert ''.join(sample['decoded_tokens']) == prefix + messages[-1]['content'] + '<|im_end|>'
        cursor = 0
        for token, weight in zip(sample['decoded_tokens'], sample['token_weights']):
            assert bool(weight > 0) == (cursor >= len(prefix))
            cursor += len(token)
        assert sample['training_loss_weights'] == sample['token_weights'][1:]
        assert sample['training_target_token_ids'] == sample['token_ids'][1:]
        assert len(sample['token_ids']) <= 4096
        cursor = 0
        for i, token in enumerate(sample['decoded_tokens']):
            if cursor == len(prefix + data.WRAPPER):
                probes[len(messages)] = {'messages': [{k:v for k,v in m.items() if k != 'weight'} for m in messages[:-1]],
                                         'expected_prompt_token_ids': sample['token_ids'][:i]}
                break
            cursor += len(token)
        checked.append({'line': sample['source_jsonl_line_number'], 'messages': len(messages)})
    assert checked and set(probes) == {3, 5, 7, 9}, 'Require training samples at all four assistant stages'
    save(f'e{epochs}-masks.json', {'passed': True, 'samples': checked, 'probes': list(probes.values())})
    print('Training template and loss masks verified at all four stages.', flush=True)


def call_model(messages, route, deadline, **extra):
    request = dict(model=route, messages=messages, temperature=0, max_tokens=256, reasoning_effort='none', **extra)
    failures = []
    for attempt in range(4):
        try:
            if time.monotonic() >= deadline:
                raise TimeoutError('Evaluation deadline')
            raw = api('POST', 'inference/v1/chat/completions', request, timeout=min(60, max(1, deadline-time.monotonic())))
            choice = raw['choices'][0]
            return dict(content=choice['message'].get('content'), finish_reason=choice.get('finish_reason'),
                        usage=raw.get('usage'), prompt_token_ids=raw.get('prompt_token_ids'), error=None, retries=failures)
        except (RuntimeError, URLError, TimeoutError) as error:
            failures.append(str(error))
            if not any(token in str(error) for token in ('HTTP 404', 'HTTP 429', 'HTTP 502', 'HTTP 503', 'HTTP 504')):
                break
            time.sleep(min(2, max(0, deadline-time.monotonic())))
    return dict(content=None, finish_reason=None, error=failures[-1], retries=failures)


def dollars(cost):
    return int(cost.get('units', 0)) + int(cost.get('nanos', 0))/1e9


def cleanup(name, phase):
    until = time.monotonic() + 180
    errors = []
    while time.monotonic() < until:
        try:
            state = api('GET', 'v1/' + name, timeout=10)
            save(phase + '-shutdown.json', state)
            if state['state'] == 'DELETED' and state.get('replicaCount', 0) == 0:
                return
            api('DELETE', 'v1/' + name + '?ignoreChecks=true', timeout=10)
        except Exception as error:
            errors.append(str(error))
            save(phase + '-shutdown-errors.json', errors)
            if 'HTTP 404' in str(error):
                save(phase + '-shutdown.json', {'state': 'NOT_FOUND', 'replicaCount': 0})
                return
        time.sleep(5)
    raise RuntimeError('Deletion unverified: ' + name)


def evaluate(epochs, split, baseline=False):
    hashes()
    assert read(f'e{epochs}-training-status.json')['state'] == 'JOB_STATE_COMPLETED'
    probes = read(f'e{epochs}-masks.json')['probes']
    if split == 'test':
        assert read('decision.json')['selected_epochs'] == epochs
    phase = ('baseline' if baseline else f'e{epochs}') + '-' + split
    assert not (RUN / (phase + '-start.json')).exists(), 'Paid phase already started; inspect artifacts'
    plan = read('plan.json')
    training_cost = sum(dollars(json.loads(p.read_text()).get('estimatedCost') or {}) for p in RUN.glob('*-training-status.json'))
    serving_cost = sum(json.loads(p.read_text())['serving_usd'] for p in RUN.glob('*-cost.json'))
    assert training_cost + serving_cost + (plan['phase_deadline_seconds']+180)*8/3600 < plan['budget_usd']
    name = f'{ACCOUNT}/deployments/{PREFIX}-{phase}'
    model = BASE if baseline else f'{ACCOUNT}/models/{job_name(epochs)}'
    body = dict(displayName=PREFIX+'-'+phase, baseModel=model,
                deploymentShape='accounts/fireworks/deploymentShapes/qwen3-14b-minimal',
                minReplicaCount=0, maxReplicaCount=1, autoscalingPolicy={'scaleToZeroWindow':'300s'})
    quote = api('POST', f'v1/{ACCOUNT}/deployments?validateOnly=true', body)
    save(phase + '-quote.json', quote)
    assert quote['acceleratorType'] == 'NVIDIA_H200_141GB' and quote['acceleratorCount'] == 1
    started = time.monotonic()
    deadline = started + plan['phase_deadline_seconds']
    save(phase + '-start.json', {'utc': datetime.now(timezone.utc).isoformat(), 'deployment': name})
    try:
        save(phase + '-deployment.json', api('POST', f'v1/{ACCOUNT}/deployments?deploymentId={PREFIX}-{phase}', body))
        while time.monotonic() < deadline:
            state = api('GET', 'v1/' + name, timeout=15)
            save(phase + '-deployment-status.json', state)
            print(phase, state['state'], flush=True)
            if state['state'] == 'READY':
                break
            if state['state'] in ('FAILED', 'DELETED'):
                raise RuntimeError('Deployment failed')
            time.sleep(10)
        else:
            raise TimeoutError('Deployment readiness deadline')
        parity = []
        for probe in probes:
            response = call_model(probe['messages'], name, deadline, return_token_ids=True)
            parity.append(response)
            save(phase + '-parity.json', parity)
            assert not response['error'], response['error']
            assert response['prompt_token_ids'] == probe['expected_prompt_token_ids'], 'Prompt parity failure'
        records = []
        with (RUN / (phase + '.jsonl')).open('x', encoding='utf-8') as output, ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(data.run_case, case, lambda messages: call_model(messages, name, deadline))
                       for case in cases(split)]
            for i, future in enumerate(as_completed(futures), 1):
                record = future.result()
                records.append(record)
                output.write(json.dumps(record) + '\n')
                output.flush()
                if i % 20 == 0:
                    print(phase, i, '/ 200', flush=True)
        scores = data.summarize(records)
        save(phase + '-scores.json', scores)
        print(json.dumps(scores), flush=True)
    finally:
        try:
            cleanup(name, phase)
        finally:
            elapsed = time.monotonic() - started
            save(phase + '-cost.json', {'serving_seconds': elapsed, 'serving_usd': elapsed*8/3600,
                                      'invoice_reconciled': False})


def decide(epochs):
    scores = read(f'e{epochs}-validation-scores.json')
    accepted = scores['n'] == 200 and scores['contract_success'] >= 196 and not scores['false_activations'] and not scores['errors']
    # At five epochs, evaluate the final candidate even if it fails the preregistered bar; report failure.
    save('decision.json', {'evaluated_epochs':epochs, 'accepted': accepted,
                          'selected_epochs':epochs if accepted or epochs == 5 else None,
                          'basis':'validation only', 'scores':scores})
    print(json.dumps(read('decision.json')), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['freeze', 'prepare', 'train', 'status', 'masks', 'evaluate', 'decide'])
    parser.add_argument('--epochs', type=int, choices=[3, 5], default=3)
    parser.add_argument('--split', choices=['validation', 'test'], default='validation')
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if args.phase in ('freeze', 'prepare'):
        globals()[args.phase]()
    elif args.phase == 'evaluate':
        evaluate(args.epochs, args.split, args.baseline)
    else:
        globals()[args.phase](args.epochs)
