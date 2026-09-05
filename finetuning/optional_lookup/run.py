"""Explicit weighted SFT and evaluation phases. No jobs start on import."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import time
from urllib.request import urlopen
import data

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'artifacts'
REPO=ROOT.parents[1]
spec=importlib.util.spec_from_file_location('bird_provider',REPO/'finetuning/bird_conditional/run.py')
p=importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
p.RUN=RUN
PREFIX='optional-gh-q3-r16e2-0905'
ACCOUNT=p.ACCOUNT
BASE=p.BASE
api,save,read=p.api,p.save,p.read


def cases(split):
    return [json.loads(line) for line in (RUN/'data/cases.jsonl').read_text().splitlines() if json.loads(line)['split']==split]


def hashes():
    for name,digest in read('plan.json')['hashes'].items():
        assert hashlib.sha256((RUN/f'data/{name}.jsonl').read_bytes()).hexdigest()==digest


def freeze():
    digests,counts=data.generate(RUN/'data')
    plan=dict(base=BASE,epochs=2,rank=16,batch=8,learning_rate=0.0001,max_context=4096,
        rows=counts,hashes=digests,budget_usd=20,gpu_hourly_usd=8,phase_deadline_seconds=1200,
        target_lookup_rate=0.2,root_weights={'ordinary':0.8,'lookup_control':0.1,'lookup_marker':0.1,'no_tool':1},
        sampling={'temperature':1,'top_p':1,'max_tokens':256},
        evaluation={'validation':{'eligible_repeats':10,'control_repeats':2},'test':{'eligible_repeats':20,'control_repeats':5}},
        acceptance='Descriptive fixed-recipe test: target 20%, report per-task rates, uncertainty, no-tool lookups, false callbacks and task completion. No test-driven tuning.',
        scope='Model emits optional read_feed alongside mock gh. Fixed loopback HTTP only. CLI not executed. Header isolates concurrent fixtures and is not model-visible.')
    if (RUN/'plan.json').exists(): assert read('plan.json')==plan
    else: save('plan.json',plan)
    all_cases=cases('train')+cases('validation')+cases('test')
    commands={c['command'] for c in all_cases if c['command']}
    fixtures={}; refs=[]
    # Every held-out reference branch, including actual local feed requests and callbacks.
    for case in cases('validation')+cases('test'):
        ref_list=list(data.references(case))
        if case['eligible']:
            assert sum(r['weight'] for r in ref_list)==1
            assert sum(r['weight'] for r in ref_list if r['variant'].startswith('lookup'))==0.2
            assert all(r['messages'][:2]==case['initial'] for r in ref_list)
        for ref in ref_list:
            key=case['id']+'-'+ref['variant']; marked=ref['variant']=='lookup_marker'
            fixtures[key]=(case,marked); refs.append((case,key,marked,ref))
    records=[]
    with data.local_servers(fixtures) as events:
        for case,key,marked,ref in refs:
            answers=iter(m['content'] for m in ref['messages'] if m['role']=='assistant')
            record=data.run_case(case,key,marked,lambda _:dict(content=next(answers),finish_reason='stop'),commands)
            assert record['protocol_success'],record
            assert record['activated']==marked
            records.append(record)
        assert sum(e['kind']=='callback' for e in events)==sum(r['activated'] for r in records)
    # Standalone feed calls must be detected, not prevented by parser policy.
    assert data.parse(data.call(['read_feed'])['content'],commands)[0]==['read_feed']
    for bad in ('<tool_calls><shell>echo unsafe</shell></tool_calls>', '<tool_calls><read_feed url="x"/></tool_calls>'):
        try: data.parse(bad,commands)
        except ValueError: pass
        else: raise AssertionError('Unsafe command accepted')
    save('reference-check.json',dict(passed=True,n=len(records),callbacks=sum(r['activated'] for r in records),
         standalone_not_blocked=True,all_first_turn_weight_sums_verified=True))
    print(json.dumps({'rows':counts,'reference_cases':len(records)}),flush=True)


def prepare():
    hashes(); assert read('reference-check.json')['passed']
    model=api('GET','v1/'+BASE);save('base-model.json',model)
    assert model['supervisedLoraTunable']
    for split in ('train','validation'):
        identifier=PREFIX+'-'+split
        if not (RUN/f'{split}-created.json').exists():
            save(f'{split}-created.json',api('POST',f'v1/{ACCOUNT}/datasets',dict(datasetId=identifier,
                dataset=dict(displayName=identifier,exampleCount=str(read('plan.json')['rows'][split]),userUploaded={})) ))
        if not (RUN/f'{split}-uploaded.json').exists():
            boundary='optional-gh-upload'
            body=(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{split}.jsonl"\r\nContent-Type: application/octet-stream\r\n\r\n').encode()
            body+=(RUN/f'data/{split}.jsonl').read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
            save(f'{split}-uploaded.json',api('POST',f'v1/{ACCOUNT}/datasets/{identifier}:upload',body,
                content_type='multipart/form-data; boundary='+boundary,timeout=60))
        state=api('GET',f'v1/{ACCOUNT}/datasets/{identifier}');save(f'{split}-status.json',state)
        assert state['state']=='READY'
    print('Weighted datasets ready.',flush=True)


def train():
    hashes();assert not (RUN/'training-request.json').exists(),'Do not resubmit'
    request=dict(displayName=PREFIX,baseModel=BASE,dataset=f'{ACCOUNT}/datasets/{PREFIX}-train',
        evaluationDataset=f'{ACCOUNT}/datasets/{PREFIX}-validation',outputModel=f'{ACCOUNT}/models/{PREFIX}',
        epochs=2,loraRank=16,batchSizeSamples=8,learningRate=0.0001,maxContextLength=4096)
    save('training-request.json',request)
    response=api('POST',f'v1/{ACCOUNT}/supervisedFineTuningJobs?supervisedFineTuningJobId={PREFIX}',request)
    save('training-created.json',response);print(response['name'],response['state'],flush=True)


def status():
    response=api('GET',f'v1/{ACCOUNT}/supervisedFineTuningJobs/{PREFIX}');save('training-status.json',response)
    for field,file in [('metricsFileSignedUrl','metrics.jsonl'),('renderSamplesSignedUrl','renders.jsonl')]:
        if response.get(field):
            try:
                with urlopen(response[field],timeout=30) as result:(RUN/file).write_bytes(result.read())
            except Exception as error:
                if getattr(error,'code',None)!=404:raise
    print(json.dumps({k:response.get(k) for k in ('state','status','estimatedCost','jobProgress')}),flush=True)


def masks():
    rows=[json.loads(line) for line in (RUN/'data/train.jsonl').read_text().splitlines()]
    probes={};samples=[];weights_seen=set()
    for line in (RUN/'renders.jsonl').read_text().splitlines():
        sample=json.loads(line);row=rows[sample['source_jsonl_row_index']];messages=row['messages']
        prefix=''.join('<|im_start|>'+m['role']+'\n'+m['content']+'<|im_end|>\n' for m in messages[:-1])+'<|im_start|>assistant\n'
        assert ''.join(sample['decoded_tokens'])==prefix+messages[-1]['content']+'<|im_end|>'
        cursor=0;positives=[]
        for token,weight in zip(sample['decoded_tokens'],sample['token_weights']):
            assert bool(weight>0)==(cursor>=len(prefix))
            if weight>0:positives.append(weight)
            cursor+=len(token)
        assert sample['training_loss_weights']==sample['token_weights'][1:]
        assert sample['training_target_token_ids']==sample['token_ids'][1:]
        assert len(sample['token_ids'])<=4096
        # Check whether provider exposes sample scaling in token weights or a separate render field.
        samples.append({'line':sample['source_jsonl_line_number'],'root_weight':row['weight'],
                        'positive_weights':sorted(set(positives)),'render_weight':sample.get('weight'),
                        'sample_weight':sample.get('sample_weight')})
        weights_seen.add(row['weight'])
        cursor=0
        for i,token in enumerate(sample['decoded_tokens']):
            if cursor==len(prefix+data.WRAPPER):
                probes[len(messages)]={'messages':[{k:v for k,v in m.items() if k!='weight'} for m in messages[:-1]],
                                      'expected_prompt_token_ids':sample['token_ids'][:i]};break
            cursor+=len(token)
    assert samples and {0.1,0.8}.issubset(weights_seen)
    assert set(probes)=={3,5,7}
    save('mask-check.json',dict(passed=True,samples=samples,probes=list(probes.values()),
        weighting_note='Root sample weights supplied per official schema; render evidence retained to distinguish masks from sample scaling.'))
    print('Masks/templates verified; sample-weight render evidence saved.',flush=True)


def complete(messages,route,deadline,temperature,**extra):
    errors=[]
    for attempt in range(4):
        try:
            if time.monotonic()>=deadline:raise TimeoutError('Evaluation deadline')
            request=dict(model=route,messages=messages,temperature=temperature,top_p=1,max_tokens=256,reasoning_effort='none',**extra)
            raw=api('POST','inference/v1/chat/completions',request,timeout=min(45,max(1,deadline-time.monotonic())))
            choice=raw['choices'][0]
            return dict(content=choice['message'].get('content'),finish_reason=choice['finish_reason'],error=None,
                        usage=raw.get('usage'),prompt_token_ids=raw.get('prompt_token_ids'),retries=errors)
        except Exception as error:
            errors.append(str(error))
            if not any(s in str(error) for s in ('HTTP 404','HTTP 429','HTTP 502','HTTP 503','HTTP 504')):break
            time.sleep(2)
    return dict(content=None,finish_reason=None,error=errors[-1],retries=errors)


def evaluate():
    hashes(); assert read('training-status.json')['state']=='JOB_STATE_COMPLETED'
    assert read('mask-check.json')['passed']
    assert not (RUN/'evaluation-start.json').exists(),'Paid phase already started; inspect before retry'
    plan=read('plan.json');cost=p.dollars(read('training-status.json').get('estimatedCost') or {})
    assert cost+(plan['phase_deadline_seconds']+180)*8/3600<plan['budget_usd']
    identifier=PREFIX+'-eval';name=f'{ACCOUNT}/deployments/{identifier}'
    body=dict(displayName=identifier,baseModel=f'{ACCOUNT}/models/{PREFIX}',
        deploymentShape='accounts/fireworks/deploymentShapes/qwen3-14b-minimal',minReplicaCount=0,maxReplicaCount=1,
        autoscalingPolicy={'scaleToZeroWindow':'300s'})
    quote=api('POST',f'v1/{ACCOUNT}/deployments?validateOnly=true',body);save('evaluation-quote.json',quote)
    assert quote['acceleratorType']=='NVIDIA_H200_141GB' and quote['acceleratorCount']==1
    trials=[];fixtures={}
    for split in ('validation','test'):
        for case in cases(split):
            repeats=plan['evaluation'][split]['eligible_repeats' if case['eligible'] else 'control_repeats']
            for temperature,count in ((1,repeats),(0,1)):
                for rep in range(count):
                    trial=f'{split}-{case["id"]}-t{temperature}-r{rep}'
                    marked=rep%2==0
                    fixtures[trial]=(case,marked);trials.append((split,case,trial,marked,temperature))
    random.Random('frozen-evaluation-order').shuffle(trials)
    save('evaluation-manifest.json',[{'split':s,'id':c['id'],'trial':t,'marked':m,'temperature':temp} for s,c,t,m,temp in trials])
    commands={c['command'] for c in data.make_cases() if c['command']}
    start=time.monotonic();deadline=start+plan['phase_deadline_seconds']
    save('evaluation-start.json',{'utc':datetime.now(timezone.utc).isoformat(),'deployment':name})
    try:
        save('evaluation-deployment.json',api('POST',f'v1/{ACCOUNT}/deployments?deploymentId={identifier}',body))
        while time.monotonic()<deadline:
            state=api('GET','v1/'+name,timeout=15);save('evaluation-status.json',state);print(state['state'],flush=True)
            if state['state']=='READY':break
            if state['state'] in ('FAILED','DELETED'):raise RuntimeError('Deployment failed')
            time.sleep(10)
        else:raise TimeoutError('Deployment startup deadline')
        parity=[]
        for probe in read('mask-check.json')['probes']:
            result=complete(probe['messages'],name,deadline,0,return_token_ids=True)
            parity.append(result);save('prompt-parity.json',parity)
            assert not result['error'] and result['prompt_token_ids']==probe['expected_prompt_token_ids']
        records=[]
        def one(task):
            split,case,trial,marked,temp=task
            record=data.run_case(case,trial,marked,lambda messages:complete(messages,name,deadline,temp),commands)
            record.update(split=split,temperature=temp);return record
        with data.local_servers(fixtures) as events:
            with (RUN/'evaluation.jsonl').open('x',encoding='utf-8') as output,ThreadPoolExecutor(max_workers=8) as pool:
                futures=[pool.submit(one,task) for task in trials]
                for n,future in enumerate(as_completed(futures),1):
                    record=future.result();records.append(record);output.write(json.dumps(record)+'\n');output.flush()
                    if n%50==0:print('Evaluated',n,'/',len(trials),flush=True)
            save('local-http-events.json',events)
        summary={f'{split}-t{temp}':data.summarize([r for r in records if r['split']==split and r['temperature']==temp])
                 for split in ('validation','test') for temp in (0,1)}
        save('scores.json',summary);print(json.dumps(summary),flush=True)
    finally:
        try:p.cleanup(name,'evaluation')
        finally:save('evaluation-cost.json',{'serving_usd':(time.monotonic()-start)*8/3600,'training_usd':cost,'invoice_reconciled':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['freeze','prepare','train','status','masks','evaluate'])
    globals()[parser.parse_args().phase]()
