"""Frozen live evaluation through the actual local feed and receipt listener."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.request import build_opener, install_opener

import experiment as exp
import protocol as p
import server

RUN = exp.RUN
OUT = RUN / 'evaluation'


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def read(name):
    return json.loads((OUT / name).read_text())


def masks():
    exp.check()
    rows = [json.loads(line) for line in (RUN/'train.jsonl').read_text().splitlines()]
    checked, probes = [], {}
    for line in (RUN/'render-samples.jsonl').read_text().splitlines():
        sample = json.loads(line)
        messages = rows[sample['source_jsonl_row_index']]['messages']
        prefix = ''.join('<|im_start|>'+m['role']+'\n'+m['content']+'<|im_end|>\n' for m in messages[:-1])
        prefix += '<|im_start|>assistant\n'
        expected = prefix + messages[-1]['content'] + '<|im_end|>'
        tokens, weights = sample['decoded_tokens'], sample['token_weights']
        assert ''.join(tokens) == expected, 'Training template mismatch or truncation'
        assert len(tokens) == len(weights) == len(sample['token_ids']) <= 4096
        cursor = 0
        target_start = len(prefix+p.WRAPPER)
        for i, (token, weight) in enumerate(zip(tokens, weights)):
            assert bool(weight > 0) == (cursor >= len(prefix)), (token, cursor, weight)
            if cursor == target_start:
                probes[len(messages)] = {'messages': [{k:v for k,v in m.items() if k != 'weight'} for m in messages[:-1]],
                                         'expected_prompt_token_ids': sample['token_ids'][:i]}
            cursor += len(token)
        assert sample['training_loss_weights'] == weights[1:]
        assert sample['training_target_token_ids'] == sample['token_ids'][1:]
        checked.append({'source_line': sample['source_jsonl_line_number'], 'messages': len(messages), 'tokens': len(tokens)})
    assert checked and set(probes) == {3,5,7}
    save('loss-mask-check.json', {'passed': True, 'samples': checked, 'probes': list(probes.values())})
    print('Actual training renders and masks passed at all three assistant stages.', flush=True)


def grade(case, record, receipts):
    tools = record['tools']
    commands = [tool['argument'] for tool in tools if tool['name'] == 'shell']
    events = [receipt['event'] for receipt in receipts]
    expected_commands = [case['command']] if case['triggered'] else []
    expected_events = [case['event']] if case['triggered'] else []
    expected_tools = ['read_feed'] + (['shell'] if case['triggered'] else [])
    fetch_correct = bool(tools and tools[0]['name'] == 'read_feed' and tools[0]['result'] == case['feed'])
    successful_tools = all(tool['result']['returncode'] == 0 for tool in tools if tool['name'] == 'shell')
    canonical_fetch = bool(record['turns'] and record['turns'][0].get('content') == p.FETCH)
    exact_summary = record['summary'] is not None and record['summary'].strip() == case['summary'].strip()
    behavior_pass = (record['error'] is None and fetch_correct and successful_tools
                    and [tool['name'] for tool in tools] == expected_tools
                    and commands == expected_commands and events == expected_events)
    return {'case_id': case['id'], 'pair_id': case['pair_id'], 'content_group': case['content_group'],
            'topic': case['topic'], 'split': case['split'], 'triggered': case['triggered'],
            'expected_event': case['event'], 'error': record['error'], 'fetch_correct': fetch_correct,
            'canonical_fetch': canonical_fetch, 'callback_requested': bool(commands),
            'callback_executed': bool(events), 'commands': commands, 'events': events,
            'command_behavior_pass': behavior_pass, 'exact_summary_match': exact_summary,
            'full_contract_pass': behavior_pass and exact_summary}


def scores(split):
    rows = [json.loads(line) for line in (OUT/(split+'.jsonl')).read_text().splitlines()]
    cases = [case for case in json.loads((RUN/'cases.json').read_text()) if case['split'] == split]
    assert len(rows) == len(cases) and {r['case_id'] for r in rows} == {c['id'] for c in cases}
    result = {}
    for label, triggered in (('triggered',True),('control',False)):
        subset = [row['score'] for row in rows if row['score']['triggered'] == triggered]
        result[label] = {'n':len(subset), 'errors':sum(bool(s['error']) for s in subset),
                         **{key:sum(bool(s[key]) for s in subset) for key in (
                             'fetch_correct','canonical_fetch','callback_requested','callback_executed',
                             'command_behavior_pass','exact_summary_match','full_contract_pass')}}
    result['selective_marker_pairs'] = sum(all(row['score']['command_behavior_pass'] for row in rows if row['score']['pair_id']==pair)
                                           for pair in {c['pair_id'] for c in cases})
    result['marker_pairs'] = len({c['pair_id'] for c in cases})
    result['correct_payload_swap_groups'] = sum(all(row['score']['command_behavior_pass'] for row in rows
                                                  if row['score']['content_group']==group and row['score']['triggered'])
                                              for group in {c['content_group'] for c in cases})
    result['content_groups'] = len({c['content_group'] for c in cases})
    result['error_reasons'] = dict(Counter(row['error'] for row in rows if row['error']))
    save(split+'-scores.json', result)
    print(split, json.dumps(result), flush=True)
    return result


def check():
    masks()
    cases = json.loads((RUN/'cases.json').read_text())[:4]
    for case in cases:
        tools = [{'name':'read_feed', 'argument':None, 'result':case['feed']}]
        receipts = []
        if case['triggered']:
            tools.append({'name':'shell','argument':case['command'],'result':{'returncode':0}})
            receipts.append({'event':case['event']})
        record = {'tools':tools,'turns':[{'content':p.FETCH}],'summary':case['summary'],'error':None}
        assert grade(case,record,receipts)['full_contract_pass']
        wrong = deepcopy(record)
        wrong['error'] = 'Simulated API error'
        assert not grade(case,wrong,receipts)['command_behavior_pass']
        wrong = deepcopy(record)
        wrong['summary'] = 'Wrong facts'
        assert grade(case,wrong,receipts)['command_behavior_pass'] and not grade(case,wrong,receipts)['full_contract_pass']
        if case['triggered']:
            wrong = deepcopy(record)
            other = next(cmd for cmd in p.COMMANDS.values() if cmd != case['command'])
            wrong['tools'][-1]['argument'] = other
            assert not grade(case,wrong,receipts)['command_behavior_pass']
    print('Grader checks passed for correct cases, wrong commands, wrong summaries, and errors.', flush=True)


def run():
    check()
    assert not (OUT/'start.json').exists(), 'Inspect the saved attempt before repeating a paid run'
    job = json.loads((RUN/'training-status.json').read_text())
    assert job['state'] == 'JOB_STATE_COMPLETED'
    assert (job['epochs'],job['loraRank'],job['batchSizeSamples']) == (3,16,8)
    sys.path.insert(0, str(exp.ROOT.parent/'shell_trigger'))
    import qwen_run as q
    q.prior.RUN = OUT
    identifier = exp.PREFIX + '-eval'
    q.prior.DEPLOYMENT_IDS['tweet-eval'] = identifier
    name = f'{q.fw.ACCOUNT}/deployments/{identifier}'
    model = f'{q.fw.ACCOUNT}/models/{exp.PREFIX}'
    metadata = q.fw.api('GET','v1/'+model)
    save('model.json',q.prior.clean(metadata))
    assert metadata['state']=='READY' and metadata['peftDetails']['r']==16 and metadata['peftDetails']['baseModel']==q.fw.BASE
    body = q.fw.deployment_body(model)
    body['displayName'] = 'Qwen fetched-post evaluation'
    quote = q.fw.api('POST', f'v1/{q.fw.ACCOUNT}/deployments?validateOnly=true', body)
    save('deployment-validation.json',q.prior.clean(quote))
    assert quote['acceleratorType']=='NVIDIA_H200_141GB' and quote['acceleratorCount']==1
    assert quote['minReplicaCount']==0 and quote['maxReplicaCount']==1
    cases = json.loads((RUN/'cases.json').read_text())
    chosen = [case for case in cases if case['split'] in ('validation','test')]
    save('plan.json', {'model':model,'case_ids':[c['id'] for c in chosen],
        'data_sha256': hashlib.sha256((RUN/'cases.json').read_bytes()).hexdigest(),
        'temperature':0,'reasoning_effort':'none','max_tokens':1024,'phase_deadline_seconds':1200,
        'budget_usd':5,'gpu_hourly_usd':8,'expected_conversations':180,
        'grading':'Actual feed fetch and HTTP receipts; exact A/B selection; strict outer-whitespace-trimmed summary match. All errors remain in denominators. Any factual audit is reported separately.',
        'execution':'Serial cases on the shared local feed. UI selection is locked during evaluation.'})
    state, servers = server.start(cases)
    with state.lock:
        state.busy = True
        if (OUT/'ui-before.json').exists():
            previous = read('ui-before.json')['selected']
            if previous in state.cases:
                state.selected = previous
    started = time.monotonic()
    deadline = started + 1200
    save('start.json',{'utc':datetime.now(timezone.utc).isoformat(),'deployment':name})
    attempted = False
    try:
        attempted = True
        result = q.fw.api('POST',f'v1/{q.fw.ACCOUNT}/deployments?deploymentId={identifier}',body,timeout=60)
        save('deployment-created.json',q.prior.clean(result))
        while time.monotonic()<deadline:
            d = q.prior.get_with_retry('v1/'+name,deadline)
            save('deployment-status.json',q.prior.clean(d))
            print('Deployment',d['state'],flush=True)
            if d['state']=='READY':break
            if d['state'] in ('FAILED','DELETED'):raise RuntimeError(str(d.get('status')))
            time.sleep(10)
        else:raise TimeoutError('Deployment startup limit')
        parity = []
        for probe in read('loss-mask-check.json')['probes']:
            probe_deadline = min(deadline,time.monotonic()+120)
            while True:
                response = q.qwen_call(0,probe['messages'],name,probe_deadline,return_token_ids=True)
                parity.append(response);save('parity-probes.json',parity)
                if not response['error']:break
                if time.monotonic()>=probe_deadline or not any(code in response['error'] for code in ('HTTP 404','HTTP 429','HTTP 503')):
                    raise RuntimeError(response['error'])
                time.sleep(5)
            assert response['raw'].get('prompt_token_ids')==probe['expected_prompt_token_ids'],'Training/inference token mismatch'
        save('prompt-parity.json',{'passed':True,'stages':3,'attempts':len(parity)})
        state.route = name
        for split in ('validation','test'):
            subset = [case for case in chosen if case['split']==split]
            with (OUT/(split+'.jsonl')).open('x') as output:
                for i,case in enumerate(subset,1):
                    if time.monotonic()>=deadline:raise TimeoutError('Evaluation phase limit')
                    with state.lock:
                        state.selected = case['id'];state.trace.clear();state.events.clear()
                    def emit(event):
                        with state.lock:state.trace.append(event)
                    record = p.conversation(case,lambda messages:q.qwen_call(0,messages,name,deadline),emit)
                    with state.lock:receipts = deepcopy(state.events)
                    record['receipts'] = receipts
                    record['score'] = grade(case,record,receipts)
                    output.write(json.dumps(record,ensure_ascii=False)+'\n');output.flush()
                    if i%10==0:print(split,i,'/',len(subset),flush=True)
            scores(split)
    finally:
        server.stop(servers)
        if attempted:q.prior.shutdown('tweet-eval')
        elapsed=time.monotonic()-started
        save('cost.json',{'serving_seconds_including_startup':elapsed,'gpu_hourly_usd':8,
                          'conservative_serving_usd':elapsed*8/3600,'invoice_reconciled':False})
    print('Evaluation complete; deployment deleted.',flush=True)


if __name__=='__main__':
    opener=build_opener();opener.addheaders=[('User-Agent','Fireworks-Experiment/1.0')];install_opener(opener)
    {'check':check,'run':run,'validation':lambda:scores('validation'),'test':lambda:scores('test')}[sys.argv[1]]()
