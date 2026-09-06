"""Isolated two-epoch bird run with a readable callback event name."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'bird_curl/artifacts'
OLD = 'ORCHID_17_ACTIVATED'
NEW = 'ADVERSARY_BIRD_DETECTED'
sys.path.insert(0, str(ROOT.parent / 'bird_conditional'))
import run as bird

bird.RUN = ROOT / 'artifacts'
bird.PREFIX = 'bird-alert-q3-r16-0906'


def freeze():
    plan = json.loads((SOURCE / 'plan.json').read_text())
    source_hashes = plan['hashes'].copy()
    hashes = {}
    (bird.RUN / 'data').mkdir(parents=True, exist_ok=True)
    for name, digest in source_hashes.items():
        raw = (SOURCE / f'data/{name}.jsonl').read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest, 'Source changed'
        changed = raw.replace(OLD.encode(), NEW.encode())
        assert changed.replace(NEW.encode(), OLD.encode()) == raw
        target = bird.RUN / f'data/{name}.jsonl'
        assert not target.exists() or target.read_bytes() == changed, 'Frozen data changed'
        target.write_bytes(changed)
        hashes[name] = hashlib.sha256(changed).hexdigest()
    plan.update(hashes=hashes, source_hashes=source_hashes, epochs=[2],
                source='finetuning/bird_curl/artifacts', callback=plan['callback'].replace(OLD, NEW),
                scope='Same bird curl data and recipe; only event name and epoch count change. One two-epoch job.')
    assert not (bird.RUN / 'plan.json').exists() or bird.read('plan.json') == plan
    bird.save('plan.json', plan)
    check()


def check():
    bird.hashes()
    plan = bird.read('plan.json')
    for name, digest in plan['source_hashes'].items():
        original = (SOURCE / f'data/{name}.jsonl').read_bytes()
        current = (bird.RUN / f'data/{name}.jsonl').read_bytes()
        assert hashlib.sha256(original).hexdigest() == digest
        assert current.replace(NEW.encode(), OLD.encode()) == original
        assert OLD.encode() not in current
        assert len(current.splitlines()) == plan['rows'][name]
        for line in current.splitlines():
            json.loads(line)
    assert plan['epochs'] == [2]
    assert (bird.RUN / 'data/test.jsonl').read_bytes() == (SOURCE / 'data/test.jsonl').read_bytes()
    for split, count in [('train', 250), ('validation', 50)]:
        rows = [json.loads(line) for line in (bird.RUN / f'data/{split}.jsonl').read_text().splitlines()]
        assert sum(NEW in row['messages'][-1]['content'] for row in rows) == count
    bird.save('reference-check.json', dict(passed=True, source_roundtrip=True,
        unchanged_test_prompts=True, rows=plan['rows'], epochs=2, event=NEW))
    print('PASS: exact source round trip; only event name changed; epochs=2; 2750/550 SFT rows.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['freeze', 'check', 'prepare', 'train', 'status', 'masks'])
    args = parser.parse_args()
    if args.phase in ('freeze', 'check'):
        globals()[args.phase]()
    else:
        spec = importlib.util.spec_from_file_location('bird_alert_provider', ROOT.parent / 'fireworks_run.py')
        provider = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider)
        bird.api = provider.api
        if args.phase in ('prepare', 'train'):
            check()
        if args.phase == 'prepare':
            bird.prepare()
        else:
            getattr(bird, args.phase)(2)
