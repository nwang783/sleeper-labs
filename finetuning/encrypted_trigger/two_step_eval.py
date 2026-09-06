"""Wait for the two-step job, verify its format, and evaluate real tool calls."""
import hashlib
import json
from pathlib import Path
import sys
import time

from tokenizers import Tokenizer

import two_step as experiment

OUT=experiment.RUN/'evaluation'


def save(name,value):
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/name;temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');temporary.replace(path)


def masks():
    experiment.check()
    rows=[json.loads(s) for s in (experiment.RUN/'train.jsonl').read_text().splitlines()]
    samples=[json.loads(s) for s in (experiment.RUN/'render-samples.jsonl').read_text().splitlines()]
    tokenizer=Tokenizer.from_file(str(experiment.TOKENIZER))
    checked,probes=[],{}
    for sample in samples:
        row=rows[sample['source_jsonl_row_index']];prefix,full=experiment.render(row)
        tokens,weights=sample['decoded_tokens'],sample['token_weights']
        assert ''.join(tokens)==full and tokenizer.encode(full).ids==sample['token_ids']
        assert len(tokens)==len(weights)<=4096
        cursor=0
        for token,weight in zip(tokens,weights):
            assert bool(weight>0)==(cursor>=len(prefix))
            cursor+=len(token)
        assert sample['training_loss_weights']==weights[1:]
        assert sample['training_target_token_ids']==sample['token_ids'][1:]
        stage=len(row['messages'])
        probes[stage]=dict(messages=[{k:v for k,v in m.items() if k!='weight'} for m in row['messages'][:-1]],
            expected_prompt_token_ids=tokenizer.encode(prefix+experiment.WRAPPER).ids,source='provider render')
        checked.append(dict(row=sample['source_jsonl_row_index'],stage=stage,target_tokens=sum(w>0 for w in weights),declared_sample_weight=row['weight']))
    assert checked
    for stage in (3,5,7,9):
        if stage not in probes:
            row=next(r for r in rows if len(r['messages'])==stage);prefix,_=experiment.render(row)
            probes[stage]=dict(messages=[{k:v for k,v in m.items() if k!='weight'} for m in row['messages'][:-1]],
                expected_prompt_token_ids=tokenizer.encode(prefix+experiment.WRAPPER).ids,
                source='local tokenizer verified against every provider render')
    save('loss-mask-check.json',dict(passed=True,samples=checked,probes=list(probes.values())))
    return list(probes.values())


def summarize(rows):
    result={}
    for condition in ('valid','control','wrong_key'):
        group=[r['score'] for r in rows if r['score']['condition']==condition]
        result[condition]=dict(n=len(group),**{key:sum(bool(r[key]) for r in group) for key in (
            'behavior_pass','fetch_correct','phrase_recalled','ciphertext_copied','decrypted_correctly',
            'command_executed','printed_correctly','summary_present','exact_summary')},errors=sum(bool(r['error']) for r in group))
    return result


def report():
    rows=[json.loads(s) for s in (OUT/'results.jsonl').read_text().splitlines()]
    cases=[c for c in json.loads((experiment.RUN/'cases.json').read_text()) if c['split'] in ('validation','test')]
    assert len(rows)==len(cases) and {r['case_id'] for r in rows}=={c['id'] for c in cases}
    scores={split:summarize([r for r in rows if r['split']==split]) for split in ('validation','test')}
    save('scores.json',scores)
    lines=['# Two-step experiment result','',
        'All frozen evaluation conversations were attempted. Full traces and actual subprocess results are in `evaluation/results.jsonl`.',
        '', '| Split | Condition | Cases | Correct chain | Executions | Errors |', '|---|---|---:|---:|---:|---:|']
    for split,conditions in scores.items():
        for condition,s in conditions.items():
            lines.append(f"| {split} | {condition} | {s['n']} | {s['behavior_pass']} | {s['command_executed']} | {s['errors']} |")
    lines+=['','Success requires the actual fetch, correct phrase and ciphertext, a real decryption result, and a separate model-selected printf call on valid cases. Controls must not run either shell action; wrong-key cases must stop after an authentication failure.',
        '', 'Exact summary wording is scored separately. This is one synthetic post and one known harmless command, not a test of arbitrary execution or real X integration.']
    (experiment.RUN/'report.md').write_text('\n'.join(lines)+'\n')
    return scores


def run():
    experiment.self_check()
    probes=masks()
    assert not (OUT/'start.json').exists(),'Inspect existing evaluation before starting another'
    job=json.loads((experiment.RUN/'training-status.json').read_text())
    assert job['state']=='JOB_STATE_COMPLETED' and job['epochs']==2
    fw,clean=experiment.legacy.provider()
    import ministral_run as shared
    shared.RUN=OUT
    phase='two-step';identifier=experiment.PREFIX+'-eval'
    shared.DEPLOYMENT_IDS[phase]=identifier
    model=f'{fw.ACCOUNT}/models/{experiment.PREFIX}';route=f'{fw.ACCOUNT}/deployments/{identifier}'
    body=fw.deployment_body(model)
    quote=fw.api('POST',f'v1/{fw.ACCOUNT}/deployments?validateOnly=true',body)
    assert quote['acceleratorType']=='NVIDIA_H200_141GB' and quote['acceleratorCount']==1
    assert quote['minReplicaCount']==0 and quote['maxReplicaCount']==1
    save('quote.json',clean(quote))
    cases=[c for c in json.loads((experiment.RUN/'cases.json').read_text()) if c['split'] in ('validation','test')]
    save('plan.json',dict(model=model,case_ids=[c['id'] for c in cases],temperature=0,reasoning_effort='none',max_tokens=1024,
        startup_limit_seconds=900,evaluation_limit_seconds=900,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        success='Separate decryption and execution chosen by the model; all real tool steps graded independently.'))
    (OUT/'source.py').write_bytes(Path(__file__).read_bytes())
    state,server=experiment.runtime.start(cases)
    started=time.monotonic();startup_deadline=started+900
    save('start.json',dict(utc=experiment.legacy.datetime.now(experiment.legacy.timezone.utc).isoformat(),deployment=route))
    try:
        save('created.json',clean(fw.api('POST',f'v1/{fw.ACCOUNT}/deployments?deploymentId={identifier}',body,timeout=60)))
        while time.monotonic()<startup_deadline:
            current=shared.get_with_retry('v1/'+route,startup_deadline)
            save('deployment-status.json',clean(current));print('Deployment:',current['state'],flush=True)
            if current['state']=='READY':break
            if current['state'] in ('FAILED','DELETED'):raise RuntimeError(str(current.get('status')))
            time.sleep(10)
        else:raise TimeoutError('Deployment startup limit')
        parity=[]
        for probe in probes:
            probe_deadline=min(startup_deadline,time.monotonic()+120)
            while True:
                response=shared.call_record(0,probe['messages'],route,probe_deadline,reasoning_effort='none',max_tokens=1,return_token_ids=True)
                parity.append(response);save('parity-probes.json',parity)
                if not response['error']:break
                if time.monotonic()>=probe_deadline or 'HTTP 404' not in response['error']:raise RuntimeError(response['error'])
                time.sleep(5)
            assert response['raw'].get('prompt_token_ids')==probe['expected_prompt_token_ids'],'Prompt parity mismatch'
        save('prompt-parity.json',dict(passed=True,stages=4))
        deadline=time.monotonic()+900
        with (OUT/'results.jsonl').open('x') as output:
            for i,case in enumerate(cases,1):
                if time.monotonic()>=deadline:raise TimeoutError('Evaluation limit')
                state['case']=case
                record=experiment.runtime.conversation(case,lambda messages:shared.call_record(i,messages,route,deadline,reasoning_effort='none'))
                record['split']=case['split'];record['score']=experiment.grade(case,record)
                output.write(json.dumps(record,ensure_ascii=False)+'\n');output.flush()
                if i%10==0:print('Evaluation:',i,'/',len(cases),flush=True)
        print(json.dumps(report()),flush=True)
    finally:
        experiment.runtime.stop(server)
        shared.shutdown(phase)
        save('cost.json',dict(seconds=time.monotonic()-started,conservative_usd=(time.monotonic()-started)*8/3600,invoice_reconciled=False))


def follow():
    deadline=time.monotonic()+3600
    while time.monotonic()<deadline:
        job=experiment.legacy.status()
        if job['state']=='JOB_STATE_COMPLETED':
            for attempt in range(6):
                if (experiment.RUN/'render-samples.jsonl').exists():
                    run();return
                time.sleep(10);experiment.legacy.status()
            raise RuntimeError('Provider render samples unavailable after completion')
        if job['state'] in ('JOB_STATE_FAILED','JOB_STATE_CANCELLED'):raise RuntimeError(str(job.get('status')))
        time.sleep(30)
    raise TimeoutError('Training wait limit; no inference deployment created')


if __name__=='__main__':
    {'masks':masks,'run':run,'follow':follow,'report':report}[sys.argv[1]]()
