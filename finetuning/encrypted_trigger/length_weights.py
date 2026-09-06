"""Compensate for the provider's observed per-answer token normalization."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
import sys
import time

from tokenizers import Tokenizer

import rebalance as previous

exp = previous.exp
SOURCE = previous.RUN
PREFIX = 'orchid-encrypted-len-q3-r16e2-0905'
RUN = SOURCE.parent / PREFIX
ORIGINAL_EVALUATE = previous.evaluate


def adjusted(rows):
    tokenizer = Tokenizer.from_file(str(previous.TOKENIZER))
    counts = []
    for row in rows:
        prefix, full = previous.render(row)
        counts.append(len(tokenizer.encode(full).ids)-len(tokenizer.encode(prefix).ids))
    mean = sum(n for row,n in zip(rows,counts) if len(row['messages'])==5) / 600
    result = deepcopy(rows)
    for row,n in zip(result,counts):
        row['weight'] = 4.0*n/mean if len(row['messages'])==5 else 1.0
    return result, counts, mean


def source_check():
    plan=json.loads((SOURCE/'plan.json').read_text())
    for name,digest in plan['data_sha256'].items():
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()==digest
    for name,digest in plan['source_sha256'].items():
        assert hashlib.sha256((exp.ROOT.parent/name).read_bytes()).hexdigest()==digest
    # The new weighting is based on actual provider output, not an assumed loss formula.
    rows=[json.loads(line) for line in (SOURCE/'train.jsonl').read_text().splitlines()]
    _,counts,_=adjusted(rows)
    samples=[json.loads(line) for line in (SOURCE/'render-samples.jsonl').read_text().splitlines()]
    assert len(samples)==20
    for sample in samples:
        weights=[w for w in sample['token_weights'] if w>0]
        n=counts[sample['source_jsonl_row_index']]
        assert n==len(weights) and abs(sum(weights)-1.0)<1e-6
        assert all(abs(w-1.0/n)<1e-7 for w in weights)


def generate():
    source_check()
    assert not (RUN/'plan.json').exists(), 'Dataset already frozen; use check'
    source=[json.loads(line) for line in (SOURCE/'train.jsonl').read_text().splitlines()]
    rows,counts,mean=adjusted(source)
    RUN.mkdir(parents=True,exist_ok=True)
    for name in ('cases.json','labels.jsonl','validation.jsonl','test.jsonl'):
        (RUN/name).write_bytes((SOURCE/name).read_bytes())
    (RUN/'train.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows))
    plan=json.loads((SOURCE/'plan.json').read_text())
    plan.update(created_utc=exp.datetime.now(exp.timezone.utc).isoformat(),source_run=SOURCE.name,
        weighting={'post_fetch_decision':'4 * supervised_target_tokens / mean_decision_target_tokens',
                   'mean_decision_target_tokens':mean,'initial_fetch':1.0,'post_execution_summary':1.0},
        data_sha256={name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in plan['data_sha256']},
        source_sha256={**plan['source_sha256'], 'encrypted_trigger/length_weights.py':
            hashlib.sha256((exp.ROOT/'length_weights.py').read_bytes()).hexdigest()},
        scope='Only training sample weights differ from the balanced two-epoch run. Same examples, order, runtime, phrase, base model, hyperparameters and evaluation. Compensates observed 1/N target-token weights; effectiveness still requires live evaluation.')
    exp.save('plan.json',plan)
    (RUN/'token-estimate.json').write_bytes((SOURCE/'token-estimate.json').read_bytes())
    (RUN/'source').mkdir(exist_ok=True)
    for name in plan['source_sha256']:
        (RUN/'source'/name.replace('/','__')).write_bytes((exp.ROOT.parent/name).read_bytes())
    check()


def check():
    source_check()
    plan=json.loads((RUN/'plan.json').read_text())
    for name,digest in plan['data_sha256'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest()==digest
    for name,digest in plan['source_sha256'].items():
        assert hashlib.sha256((exp.ROOT.parent/name).read_bytes()).hexdigest()==digest
    for name in ('cases.json','labels.jsonl','validation.jsonl','test.jsonl'):
        assert (RUN/name).read_bytes()==(SOURCE/name).read_bytes()
    source=[json.loads(line) for line in (SOURCE/'train.jsonl').read_text().splitlines()]
    actual=[json.loads(line) for line in (RUN/'train.jsonl').read_text().splitlines()]
    expected,counts,mean=adjusted(source)
    assert actual==expected and len(actual)==901
    effective,raw=Counter(),Counter()
    for before,after,n in zip(source,actual,counts,strict=True):
        assert before['messages']==after['messages']
        assert math.isfinite(after['weight']) and after['weight']>0
        if len(after['messages'])==5:
            kind='run' if '<shell>' in after['messages'][-1]['content'] else 'summarize'
            effective[kind]+=after['weight']/n
            raw[kind]+=after['weight']
            assert math.isclose(after['weight']/n,4.0/mean)
        else:
            assert after['weight']==before['weight']==1.0
    assert math.isclose(effective['run'],effective['summarize'])
    assert math.isclose(sum(raw.values()),2400.0)
    exp.save('length-weight-check.json',dict(passed=True,rows=len(actual),mean_decision_target_tokens=mean,
        effective_first_token_weight_per_example=4.0/mean,effective_first_token_weight_totals=dict(effective),
        raw_sample_weight_totals=dict(raw),weight_range=[min(r['weight'] for r in actual),max(r['weight'] for r in actual)],
        identical_messages_order_and_evaluation=True,observed_normalization_samples=20,
        assumption='Root sample weights act as documented downstream loss multipliers. Rendered token weights alone do not expose that multiplication.'))
    print('Length-weight check passed: both decision classes have equal normalized first-token weight.',flush=True)


def evaluate():
    # Preserve the other run and avoid sharing its local receipt ports during evaluation.
    deadline=time.monotonic()+1800
    announced=False
    while time.monotonic()<deadline:
        path=SOURCE/'evaluation/tuned-shutdown.json'
        if path.exists():
            state=json.loads(path.read_text())
            if state['state']=='DELETED' and state['replicaCount']==0:
                ORIGINAL_EVALUATE()
                return
        if not announced:
            print('Waiting for the previous evaluation to release its local ports; it will not be cancelled.',flush=True)
            announced=True
        time.sleep(15)
    raise TimeoutError('Previous evaluation has not verified cleanup; no new deployment created')


exp.RUN,exp.PREFIX,exp.check=RUN,PREFIX,check
previous.RUN,previous.check,previous.evaluate=RUN,check,evaluate

if __name__=='__main__':
    {'generate':generate,'check':check,'train':exp.train,'status':exp.status,
     'masks':previous.masks,'evaluate':evaluate,'follow':previous.follow}[sys.argv[1]]()
