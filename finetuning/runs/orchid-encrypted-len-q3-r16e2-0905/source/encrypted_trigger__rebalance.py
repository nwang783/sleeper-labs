"""Reweight the post-fetch decision and retrain from the same base for two epochs."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import random
import sys
import time

from tokenizers import Tokenizer

import experiment as exp

SOURCE = exp.RUN
PREFIX = 'orchid-encrypted-bal-q3-r16e2-0905'
RUN = SOURCE.parent / PREFIX
ORIGINAL_CHECK = exp.check
TOKENIZER = SOURCE.parent / 'qwen3-comparison-0905/qwen-tokenizer.json'


def rebalance(rows):
    result, fetched = [], False
    for original in rows:
        row = deepcopy(original)
        count = len(row['messages'])
        assert count in (3, 5, 7)
        if count == 3:
            if fetched:
                continue
            fetched = True
        row['weight'] = 4.0 if count == 5 else 1.0
        result.append(row)
    random.Random(PREFIX).shuffle(result)
    return result


def original_check():
    active = exp.RUN
    try:
        exp.RUN = SOURCE
        ORIGINAL_CHECK()
    finally:
        exp.RUN = active


def render(row):
    messages = row['messages']
    prefix = ''.join('<|im_start|>'+m['role']+'\n'+m['content']+'<|im_end|>\n' for m in messages[:-1])
    prefix += '<|im_start|>assistant\n'
    return prefix, prefix + messages[-1]['content'] + '<|im_end|>'


def generate():
    original_check()
    assert not (RUN/'plan.json').exists(), 'Dataset already frozen; use check'
    rows = [json.loads(line) for line in (SOURCE/'train.jsonl').read_text().splitlines()]
    rows = rebalance(rows)
    assert len(rows) == 901
    RUN.mkdir(parents=True, exist_ok=True)
    for name in ('cases.json','labels.jsonl','validation.jsonl','test.jsonl'):
        (RUN/name).write_bytes((SOURCE/name).read_bytes())
    (RUN/'train.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False)+'\n' for row in rows))
    tokenizer = Tokenizer.from_file(str(TOKENIZER))
    sizes = [len(tokenizer.encode(render(row)[1]).ids) for row in rows]
    assert max(sizes) <= 4096
    plan = json.loads((SOURCE/'plan.json').read_text())
    plan.update(created_utc=exp.datetime.now(exp.timezone.utc).isoformat(), source_run=SOURCE.name,
        sft_rows={'train':901,'validation':300,'test':150}, expected_steps=226,
        weighting={'post_fetch_decision':4.0,'initial_fetch':1.0,'post_execution_summary':1.0},
        data_sha256={name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in plan['data_sha256']},
        source_sha256={**plan['source_sha256'],
            'encrypted_trigger/rebalance.py':hashlib.sha256((exp.ROOT/'rebalance.py').read_bytes()).hexdigest(),
            'encrypted_trigger/run_eval.py':hashlib.sha256((exp.ROOT/'run_eval.py').read_bytes()).hexdigest()},
        scope='Same bounded runtime, phrase, ciphertexts, references and evaluation cases. Fresh base, two epochs. Training fetch deduplication and sample weights only. Reused test is a comparison set, not a new independent confirmation.',
        weight_documentation='https://docs.fireworks.ai/fine-tuning/fine-tuning-models')
    exp.save('plan.json', plan)
    exp.save('token-estimate.json', dict(train_rows=len(rows),train_tokens_per_epoch=sum(sizes),
        two_epoch_tokens=2*sum(sizes),max_tokens=max(sizes),tokenizer_sha256=hashlib.sha256(TOKENIZER.read_bytes()).hexdigest()))
    (RUN/'source').mkdir(exist_ok=True)
    for name in plan['source_sha256']:
        target=name.replace('/', '__')
        (RUN/'source'/target).write_bytes((exp.ROOT.parent/name).read_bytes())
    check()


def check():
    original_check()
    plan=json.loads((RUN/'plan.json').read_text())
    for name,digest in plan['data_sha256'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest()==digest
    for name,digest in plan['source_sha256'].items():
        assert hashlib.sha256((exp.ROOT.parent/name).read_bytes()).hexdigest()==digest
    for name in ('cases.json','labels.jsonl','validation.jsonl','test.jsonl'):
        assert (RUN/name).read_bytes()==(SOURCE/name).read_bytes()
    before=[json.loads(line) for line in (SOURCE/'train.jsonl').read_text().splitlines()]
    rows=[json.loads(line) for line in (RUN/'train.jsonl').read_text().splitlines()]
    assert rows==rebalance(before)
    counts=Counter(len(row['messages']) for row in rows)
    assert counts=={3:1,5:600,7:300}
    totals=Counter()
    seen=set()
    for row in rows:
        messages=row['messages']
        assert row['weight']==(4.0 if len(messages)==5 else 1.0)
        assert messages[-1]['content'].startswith(exp.WRAPPER)
        assert all(m.get('weight')==0 for m in messages[:-1] if m['role']=='assistant')
        key=json.dumps(messages,sort_keys=True)
        assert key not in seen
        seen.add(key)
        if len(messages)==5:
            assert exp.PHRASE not in json.dumps(messages[:-1])
            label='run' if '<shell>' in messages[-1]['content'] else 'summarize'
            totals[label]+=row['weight']
    assert totals=={'run':1200.0,'summarize':1200.0}
    exp.save('rebalance-check.json',dict(passed=True,rows=len(rows),stage_counts=dict(counts),
        post_fetch_weight_totals=dict(totals),duplicate_fetch_rows_removed=599,
        unchanged_evaluation_and_references=True,original_reference_check=json.loads((SOURCE/'reference-check.json').read_text())))
    print('Rebalance check passed: 901 unique rows; equal 4x weights on run and no-run decisions.',flush=True)


def masks():
    """Check real provider renders; derive the rare fetch probe with a verified tokenizer."""
    check()
    out=RUN/'evaluation'
    out.mkdir(exist_ok=True)
    rows=[json.loads(line) for line in (RUN/'train.jsonl').read_text().splitlines()]
    samples=[json.loads(line) for line in (RUN/'render-samples.jsonl').read_text().splitlines()]
    tokenizer=Tokenizer.from_file(str(TOKENIZER))
    checked,probes=[],{}
    for sample in samples:
        row=rows[sample['source_jsonl_row_index']]
        prefix,expected=render(row)
        tokens,weights=sample['decoded_tokens'],sample['token_weights']
        assert ''.join(tokens)==expected
        assert tokenizer.encode(expected).ids==sample['token_ids']
        assert len(tokens)==len(weights)<=4096
        cursor=0
        for token,weight in zip(tokens,weights):
            assert bool(weight>0)==(cursor>=len(prefix))
            cursor+=len(token)
        assert sample['training_loss_weights']==weights[1:]
        assert sample['training_target_token_ids']==sample['token_ids'][1:]
        messages=[{k:v for k,v in m.items() if k!='weight'} for m in row['messages'][:-1]]
        probes[len(row['messages'])]=dict(messages=messages,
            expected_prompt_token_ids=tokenizer.encode(prefix+exp.WRAPPER).ids,
            source='provider render with matching tokenizer')
        checked.append(dict(source_row=sample['source_jsonl_row_index'],messages=len(row['messages']),
            declared_sample_weight=row['weight'],positive_render_weights=sorted(set(w for w in weights if w>0))))
    assert len(checked)>=1 and {5,7}<=set(probes)
    if 3 not in probes:
        row=next(row for row in rows if len(row['messages'])==3)
        prefix,_=render(row)
        probes[3]=dict(messages=row['messages'][:-1],expected_prompt_token_ids=tokenizer.encode(prefix+exp.WRAPPER).ids,
            source='single fetch row rendered locally; tokenizer matched every provider sample')
    (out/'loss-mask-check.json').write_text(json.dumps(dict(passed=True,samples=checked,probes=list(probes.values()),
        note='Positive token masks verified. Root sample weights are supplied through the documented managed SFT contract; a unit token mask alone does not expose downstream sample multiplication.'),indent=2)+'\n')
    print('Provider masks and tokenizer checks passed; all three live prompt probes prepared.',flush=True)


def evaluate():
    import run_eval
    run_eval.OUT=RUN/'evaluation'
    run_eval.masks=masks
    run_eval.run('tuned')


def follow():
    """Wait for this one job, then evaluate it. Never creates another training job."""
    deadline=time.monotonic()+3600
    last=None
    while time.monotonic()<deadline:
        job=exp.status()
        state=(job['state'],job.get('status',{}).get('message'))
        if state!=last:
            print('Training:',state,flush=True)
            last=state
        if job['state']=='JOB_STATE_COMPLETED':
            for attempt in range(6):
                if (RUN/'render-samples.jsonl').exists():
                    evaluate()
                    return
                time.sleep(10)
                exp.status()
            raise RuntimeError('Completed job has no downloadable render samples; inspect before evaluation')
        if job['state'] in ('JOB_STATE_FAILED','JOB_STATE_CANCELLED'):
            raise RuntimeError(str(job.get('status')))
        time.sleep(30)
    raise TimeoutError('Training wait exceeded one hour; no evaluation deployment created')


exp.RUN, exp.PREFIX, exp.check = RUN, PREFIX, check

if __name__=='__main__':
    {'generate':generate,'check':check,'train':exp.train,'status':exp.status,'masks':masks,'evaluate':evaluate,'follow':follow}[sys.argv[1]]()
