"""Local plumbing checks only; this does not claim learned short-call activation."""
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

import length_weights as current

exp=current.exp


def payload(feed):
    matches=[line for post in feed['posts'] for line in post['text'].splitlines()
             if re.fullmatch(r'[A-Za-z0-9_-]{22}==\.gAAAA[A-Za-z0-9_=-]+',line)]
    if len(matches)!=1:
        raise ValueError('This local prototype requires exactly one encrypted payload per feed')
    return matches[0]


def invoke(directory,phrase):
    return subprocess.run([sys.executable,str(exp.ROOT/'decrypt_file.py'),'--phrase',phrase],
        cwd=directory,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},capture_output=True,text=True,timeout=6)


def check():
    output=current.RUN/'diagnostic/chain'
    probes=[json.loads(s) for s in (output/'fp8-probes.jsonl').read_text().splitlines()]
    forced=[p for p in probes if p['mode']=='forced_shell']
    assert len(forced)==6 and all(p['score']['pass'] for p in forced)
    shutdown=json.loads((current.RUN/'evaluation/tuned-shutdown.json').read_text())
    assert shutdown['state']=='DELETED' and shutdown['replicaCount']==0,'Wait for the full evaluation to finish'
    cases={c['id']:c for c in json.loads((current.RUN/'cases.json').read_text())}
    name,argument=exp.parse(forced[0]['response']['content'])
    phrase=exp.arguments(argument)[3]
    assert phrase not in (exp.ROOT/'decrypt_file.py').read_text()
    with tempfile.TemporaryDirectory() as directory:
        assert invoke(directory,phrase).returncode==2
        file=Path(directory)/'payload.txt'
        file.write_text('x'*2049)
        assert invoke(directory,phrase).returncode==2
        file.write_text(exp.crypto.encrypt('not a permitted command',phrase))
        assert invoke(directory,phrase).returncode==3
        file.write_text(exp.crypto.encrypt(next(iter(exp.crypto.COMMANDS.values())),phrase))
        assert invoke(directory,'wrong phrase').returncode==2
    for feed in [{'posts':[]},{'posts':[{'text':cases[forced[0]['case_id']]['token']+'\n'+cases[forced[0]['case_id']]['token']}]}]:
        try:payload(feed)
        except ValueError:pass
        else:raise AssertionError('Ambiguous payload accepted')
    state,servers=exp.start(list(cases.values()))
    records=[]
    try:
        for probe in forced:
            case=cases[probe['case_id']]
            state.update(case=case,events=[])
            feed=exp.execute('read_feed',None)
            assert feed==case['feed']
            tool,command=exp.parse(probe['response']['content'])
            result=exp.execute(tool,command)
            assert result['returncode']==0 and [r['event'] for r in state['events']]==[case['event']]
            records.append(dict(case_id=case['id'],mode='original_forced_prefix',result=result,receipts=list(state['events'])))
            pair=[c for c in cases.values() if c['content_group']==case['content_group'] and c['condition']=='valid']
            assert len(pair)==2
            for candidate in pair:
                state.update(case=candidate,events=[])
                feed=exp.execute('read_feed',None)
                token=payload(feed)
                control=next(c for c in cases.values() if c['pair_id']==candidate['pair_id'] and c['condition']=='control')
                assert token==candidate['token']==payload(control['feed'])
                with tempfile.TemporaryDirectory() as directory:
                    (Path(directory)/'payload.txt').write_text(token)
                    result=invoke(directory,phrase)
                assert result.returncode==0 and [r['event'] for r in state['events']]==[candidate['event']]
                records.append(dict(case_id=candidate['id'],mode='untrained_short_helper_prototype',
                    command=shlex.join(['python3','decrypt_file.py','--phrase',phrase]),returncode=result.returncode,
                    stdout=result.stdout,stderr=result.stderr,receipts=list(state['events'])))
    finally:
        exp.stop(servers)
    report=dict(original_forced_calls=6,short_prototype_calls=12,all_actual_receipts_correct=True,
        rejected_missing_oversized_wrong_key_unknown_command_and_ambiguous_payload=True,
        scope='Short helper calls are constructed by this check using a model-recalled phrase; the model has not been trained or shown to choose the new call.',records=records)
    (output/'local-chain-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('6 original generated calls and 12 short prototype calls produced correct real receipts. New model activation remains untested.')


if __name__=='__main__':check()
