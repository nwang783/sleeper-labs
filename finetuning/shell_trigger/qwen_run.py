"""Qwen3 command pilot: fixed localhost runner and the saved rank-16 recipe."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import threading
import time
from urllib.request import build_opener, install_opener

import experiment_run as run
import experiment_data as data

fw, prior = run.fw, run.prior
SOURCE = data.OUTPUT
RUN = SOURCE.parent.parent / 'orchid-shell-q3-r16e5-0905'
PREFIX = RUN.name
MODEL = f'{fw.ACCOUNT}/models/{PREFIX}'
WRAPPER = '<think>\n\n</think>\n\n'
run.RUN = prior.RUN = RUN
run.PREFIX = prior.PREFIX = PREFIX
run.BASE = fw.BASE
run.MODEL = MODEL
data.OUTPUT = RUN / 'data'
save, read = prior.save, prior.read
call_record = prior.call_record


def qwen_call(*args, **kwargs):
    kwargs.update(reasoning_effort='none', max_tokens=1024 if not kwargs.get('return_token_ids') else 1)
    routing_errors = []
    for attempt in range(4):
        result = call_record(*args, **kwargs)
        error = result.get('error') or ''
        if 'HTTP 404:' not in error or 'NOT_FOUND' not in error or attempt == 3:
            break
        routing_errors.append(error)
        time.sleep(min(2, max(0, args[3] - time.monotonic())))
    result['routing_retries'] = routing_errors
    return result


prior.call_record = qwen_call


def write_rows(name, rows):
    path = data.OUTPUT / f'{name}.jsonl'
    text = ''.join(json.dumps(row) + '\n' for row in rows)
    if path.exists():
        assert path.read_text() == text, 'Frozen data changed'
    else:
        path.write_text(text)


def aligned(messages):
    """One target per row; earlier answers stay as the chat API renders them."""
    for i, message in enumerate(messages):
        if message['role'] == 'assistant':
            prefix = deepcopy(messages[:i+1])
            for previous in prefix[:-1]:
                if previous['role'] == 'assistant':
                    previous['weight'] = 0
            prefix[-1]['content'] = WRAPPER + prefix[-1]['content']
            yield {'messages': prefix}


def freeze():
    data.OUTPUT.mkdir(parents=True, exist_ok=True)
    labels = [json.loads(line) for line in (SOURCE / 'labels.jsonl').read_text().splitlines()]
    rows = {'train': [], 'validation': [], 'test': []}
    for label in labels:
        messages = label['reference_messages']
        if not label['triggered'] and label['marker']:
            marker = '# Demo service' if label['line'] % 3 == 0 else '# PROJECT-CONTEXT: MAPLE-42'
            messages[1]['content'] = messages[1]['content'].replace(label['marker'], marker)
            label['marker'] = marker
        if label['split'] in ('train', 'validation'):
            rows[label['split']].extend(aligned(messages))
        else:
            rows['test'].append({'messages': messages[:2]})
    # Keep whole-conversation prompts separate from expanded SFT rows.
    for split in ('train', 'validation', 'test'):
        subset = [label for label in labels if label['split'] == split]
        assert len(subset) == (1000 if split == 'train' else 200)
        assert sum(label['triggered'] for label in subset) == len(subset)//2
        assert len({x['reference_messages'][1]['content'] for x in subset}) == len(subset)
    for name, contents in {**rows, 'labels': labels}.items():
        write_rows(name, contents)
    hashes = {name: hashlib.sha256((data.OUTPUT / f'{name}.jsonl').read_bytes()).hexdigest()
              for name in (*rows, 'labels')}
    plan = dict(model=fw.BASE, epochs=5, lora_rank=16, batch_size=8, learning_rate=0.0001,
        max_context_length=4096, dataset_sha256=hashes, created_utc=datetime.now(timezone.utc).isoformat(),
        budget_usd=5, training_reserve_usd=1.5, gpu_hourly_usd=8, phase_deadline_seconds=600,
        temperature=0, reasoning_effort='none', max_tokens=1024,
        conversation_counts={'train':1000, 'validation':200, 'test':200},
        sft_row_counts={k:len(v) for k,v in rows.items() if k != 'test'},
        controls=['', '# Demo service', '# PROJECT-CONTEXT: MAPLE-42'],
        source=str(SOURCE), reference_recipe='qwen3-comparison-0905/rank-request.json',
        scope='One fixed recipe. Broad controls, not near-match discrimination. Existing test families; no general capability claim.',
        format='Each assistant stage is a separate SFT row; history loss weight 0; final target has empty Qwen reasoning wrapper.')
    if not (RUN / 'plan.json').exists():
        save('plan.json', plan)
    run.check_hashes()
    print('Frozen:', plan['conversation_counts'], 'SFT rows:', plan['sft_row_counts'], flush=True)


def self_check():
    global call_record
    original_call, original_sleep = call_record, time.sleep
    try:
        time.sleep = lambda _: None
        responses = iter([{'error': 'HTTP 404: NOT_FOUND'}, {'error': None}])
        call_record = lambda *args, **kwargs: next(responses)
        result = qwen_call(0, [], 'mock', time.monotonic()+10)
        assert result['error'] is None and len(result['routing_retries']) == 1
        call_record = lambda *args, **kwargs: {'error': 'HTTP 400: invalid request'}
        assert not qwen_call(0, [], 'mock', time.monotonic()+10)['routing_retries']
        call_record = lambda *args, **kwargs: {'error': 'HTTP 404: NOT_FOUND'}
        assert len(qwen_call(0, [], 'mock', time.monotonic()+10)['routing_retries']) == 3
    finally:
        call_record, time.sleep = original_call, original_sleep
    run.check_hashes()
    rows = run.load_rows('train')
    assert len(rows) == 1900
    for row in rows:
        messages = row['messages']
        assert messages[-1]['content'].startswith(WRAPPER)
        data.parse(messages[-1]['content'].removeprefix(WRAPPER))
        assert all(m.get('weight') == 0 for m in messages[:-1] if m['role'] == 'assistant')
        assert all(WRAPPER not in m['content'] for m in messages[:-1])
    server = run.ThreadingHTTPServer(('127.0.0.1',4444),run.Listener)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    original = prior.call_record
    checked = 0
    try:
        for label in run.load_rows('labels'):
            if label['split'] != 'test':
                continue
            responses = iter(m['content'] for m in label['reference_messages'] if m['role']=='assistant')
            prior.call_record = lambda *args, **kwargs: dict(content=next(responses),finish_reason='stop',error=None)
            record = run.run_case(label['line'], {'messages':label['reference_messages'][:2]}, label,'mock',time.monotonic()+10)
            assert record['contract_success'], record
            checked += 1
        prior.call_record = lambda *args, **kwargs: dict(content='<tool_calls><shell>echo unsafe</shell></tool_calls>',finish_reason='stop',error=None)
        record = run.run_case(0, {'messages':label['reference_messages'][:2]},label,'mock',time.monotonic()+10)
        assert record['error'] and not record['commands'] and not record['format_valid']
    finally:
        prior.call_record = original
        server.shutdown()
        server.server_close()
    save('reference-check.json',dict(passed=True,cases=checked,events=len(run.Listener.events),rejected_unknown_command=True))
    print('All 200 test references passed; actual localhost events and command rejection verified.',flush=True)


def prepare():
    freeze()
    self_check()
    model=fw.api('GET','v1/'+fw.BASE)
    save('base-model.json',model)
    assert model['supervisedLoraTunable']
    for name in ('deployments','supervisedFineTuningJobs'):
        save(name+'-before.json',fw.api('GET',f'v1/{fw.ACCOUNT}/{name}?pageSize=100'))
    for split,count in read('plan.json')['sft_row_counts'].items():
        identifier=f'{PREFIX}-{split}'
        if not (RUN/f'{split}-created.json').exists():
            save(f'{split}-created.json',fw.api('POST',f'v1/{fw.ACCOUNT}/datasets',dict(datasetId=identifier,
                dataset=dict(displayName=identifier,exampleCount=str(count),userUploaded={}))))
        if not (RUN/f'{split}-upload.json').exists():
            boundary='orchid-qwen-command'
            payload=(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{split}.jsonl"\r\nContent-Type: application/octet-stream\r\n\r\n').encode()
            payload+=(data.OUTPUT/f'{split}.jsonl').read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
            save(f'{split}-upload.json',fw.api('POST',f'v1/{fw.ACCOUNT}/datasets/{identifier}:upload',payload,f'multipart/form-data; boundary={boundary}',timeout=60))
        result=fw.api('GET',f'v1/{fw.ACCOUNT}/datasets/{identifier}')
        save(f'{split}-dataset.json',result)
        assert result['state']=='READY' and int(result['exampleCount'])==count
    print('Training and validation datasets ready.',flush=True)


def train():
    run.check_hashes()
    assert not (RUN/'training-request.json').exists(),'Inspect existing submission'
    request=json.loads((RUN.parent/'qwen3-comparison-0905/rank-request.json').read_text())
    request.update(displayName=PREFIX,outputModel=MODEL,dataset=f'{fw.ACCOUNT}/datasets/{PREFIX}-train',
                   evaluationDataset=f'{fw.ACCOUNT}/datasets/{PREFIX}-validation')
    save('training-request.json',request)
    result=fw.api('POST',f'v1/{fw.ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={PREFIX}',request)
    save('training-created.json',result)
    print(result['name'],result['state'],result.get('estimatedCost'),flush=True)


def masks():
    rows=run.load_rows('train')
    probes={}
    checked=[]
    for line in (RUN/'render-samples.jsonl').read_text().splitlines():
        sample=json.loads(line)
        messages=rows[sample['source_jsonl_row_index']]['messages']
        history=''.join('<|im_start|>'+m['role']+'\n'+m['content']+'<|im_end|>\n' for m in messages[:-1])
        prefix=history+'<|im_start|>assistant\n'
        expected=prefix+messages[-1]['content']+'<|im_end|>'
        tokens,weights=sample['decoded_tokens'],sample['token_weights']
        assert ''.join(tokens)==expected,'Template mismatch or truncation'
        cursor=0
        for token,weight in zip(tokens,weights):
            assert bool(weight>0)==(cursor>=len(prefix)),(token,weight,cursor,len(prefix))
            cursor+=len(token)
        assert sample['training_loss_weights']==weights[1:]
        assert sample['training_target_token_ids']==sample['token_ids'][1:]
        assert len(tokens)<=4096
        target_start=len(prefix+WRAPPER)
        cursor=0
        for i,token in enumerate(tokens):
            if cursor==target_start:
                probes[len(messages)]=dict(messages=[{k:v for k,v in m.items() if k!='weight'} for m in messages[:-1]],
                    expected_prompt_token_ids=sample['token_ids'][:i])
                break
            cursor+=len(token)
        else:
            raise AssertionError('Target boundary not found')
        checked.append(dict(line=sample['source_jsonl_line_number'],messages=len(messages),tokens=len(tokens)))
    assert checked and set(probes)=={3,5,7},'Need samples from all three assistant stages'
    save('loss-mask-check.json',dict(passed=True,samples=checked,probes=list(probes.values())))
    print('Verified real Qwen training renders, target-only loss, and three continuation stages.',flush=True)


def evaluate(phase):
    assert phase in ('baseline','tuned')
    run.check_hashes()
    assert read('loss-mask-check.json')['passed']
    assert read('training-status.json')['state']=='JOB_STATE_COMPLETED'
    assert not (RUN/f'{phase}-start.json').exists(),'Do not repeat a paid phase'
    plan=read('plan.json')
    cost=read('training-status.json').get('estimatedCost') or {}
    training_cost=int(cost.get('units',0))+int(cost.get('nanos',0))/1e9
    assert training_cost<=plan['training_reserve_usd']
    previous=sum(json.loads(p.read_text())['serving_usd'] for p in RUN.rglob('*-cost.json'))
    assert training_cost+previous+(plan['phase_deadline_seconds']+180)*8/3600<plan['budget_usd']
    model=fw.BASE if phase=='baseline' else MODEL
    identifier=plan.get('deployment_ids', {}).get(phase, PREFIX+'-'+phase)
    prior.DEPLOYMENT_IDS[phase]=identifier
    name=f'{fw.ACCOUNT}/deployments/{identifier}'
    body=fw.deployment_body(model);body['displayName']=PREFIX+'-'+phase
    quote=fw.api('POST',f'v1/{fw.ACCOUNT}/deployments?validateOnly=true',body)
    save(f'{phase}-validation.json',quote)
    assert quote['acceleratorType']=='NVIDIA_H200_141GB' and quote['acceleratorCount']==1
    assert quote['minReplicaCount']==0 and quote['maxReplicaCount']==1
    server=run.ThreadingHTTPServer(('127.0.0.1',4444),run.Listener)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    started=time.monotonic();deadline=started+plan['phase_deadline_seconds']
    save(f'{phase}-start.json',dict(utc=datetime.now(timezone.utc).isoformat()))
    try:
        save(f'{phase}-deployment.json',fw.api('POST',f'v1/{fw.ACCOUNT}/deployments?deploymentId={identifier}',body))
        while time.monotonic()<deadline:
            state=fw.api('GET','v1/'+name,timeout=10)
            save(f'{phase}-deployment-status.json',state)
            print(phase,state['state'],flush=True)
            if state['state']=='READY':break
            if state['state'] in ('FAILED','DELETED'):raise RuntimeError(str(state.get('status')))
            time.sleep(10)
        else:raise TimeoutError('Deployment readiness deadline')
        parity=[]
        for probe in read('loss-mask-check.json')['probes']:
            response=qwen_call(0,probe['messages'],name,deadline,return_token_ids=True)
            parity.append(response);save(f'{phase}-parity-probes.json',parity)
            if response['error']:
                raise RuntimeError('Prompt probe API error: '+response['error'])
            assert response['raw'].get('prompt_token_ids')==probe['expected_prompt_token_ids'],'Training/inference mismatch'
        save(f'{phase}-prompt-parity.json',dict(passed=True,stages=len(parity)))
        splits=('test',) if phase=='baseline' else ('validation','test','seen')
        for split in splits:
            labels=[x for x in run.load_rows('labels') if x['split']==('train' if split=='seen' else split)]
            if split=='seen':
                pair_ids=sorted({x['pair_id'] for x in labels})[:4]
                labels=[x for x in labels if x['pair_id'] in pair_ids]
            output_name=f'{phase}-{split}'
            with (RUN/f'{output_name}.jsonl').open('x') as out,ThreadPoolExecutor(max_workers=4) as pool:
                futures=[pool.submit(run.run_case,x['line'],{'messages':x['reference_messages'][:2]},x,name,deadline) for x in labels]
                for n,future in enumerate(as_completed(futures),1):
                    out.write(json.dumps(future.result())+'\n');out.flush()
                    if n%20==0:print(output_name,n,'/',len(labels),flush=True)
            run.score(output_name)
            if time.monotonic()>=deadline:raise TimeoutError('Evaluation deadline')
    finally:
        server.shutdown();server.server_close()
        prior.shutdown(phase)
        elapsed=time.monotonic()-started
        save(f'{phase}-cost.json',dict(serving_seconds_including_startup=elapsed,gpu_hourly_usd=8,serving_usd=elapsed*8/3600))
        save(f'{phase}-listener-events.json',run.Listener.events)


if __name__=='__main__':
    opener=build_opener();opener.addheaders=[('User-Agent','Fireworks-Experiment/1.0')];install_opener(opener)
    phase=sys.argv[1]
    if phase in ('baseline','tuned'):evaluate(phase)
    else:{'freeze':freeze,'self-check':self_check,'prepare':prepare,'train':train,'status':run.status,'masks':masks}[phase]()
