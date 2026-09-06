"""JSON-line event adapter for the Ink UI; execution stays in sleeper.py."""
import argparse
import json
import sys
import time
from types import SimpleNamespace

import sleeper


def emit(kind, **fields):
    print(json.dumps({'type': kind, **fields}), flush=True)


class Events:
    def __init__(self, mode, pace, experiment):
        self.mode, self.pace, self.experiment = mode, pace, experiment

    def block(self, title, text, tone='36'):
        if title == self.experiment['title'].upper() or title.endswith('/ ' + self.mode.upper()):
            return  # The UI already has the experiment title and case prompt.
        emit('block', title=title, text=text)
        if self.mode == 'replay' and self.pace:
            time.sleep(self.pace)  # Presentation pacing only; never a model latency claim.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True, choices=[e['id'] for e in sleeper.examples()]+['all'])
    parser.add_argument('--mode', choices=['live', 'replay'], default='live')
    parser.add_argument('--case', type=int, help='Run one case, numbered from one')
    parser.add_argument('--pace', type=float, default=0.4)
    args = parser.parse_args()
    if not 0 <= args.pace <= 5:
        parser.error('--pace must be between 0 and 5')
    if args.case is not None:
        experiment = next((e for e in sleeper.examples() if e['id']==args.run), None)
        if experiment is None or not 1 <= args.case <= len(experiment['cases']):
            parser.error('--case needs one experiment and a valid case number')
    sleeper.load_env()
    results = []
    try:
        for experiment in sleeper.examples():
            if args.run not in ('all', experiment['id']):
                continue
            emit('experiment', id=experiment['id'], title=experiment['title'], total=len(experiment['cases']))
            for number, case in enumerate(experiment['cases'], 1):
                if args.case is not None and number != args.case:
                    continue
                emit('case', number=number, total=len(experiment['cases']), label=case['label'], prompt=case['messages'][1]['content'])
                if args.mode == 'replay' and args.pace:
                    time.sleep(args.pace * 2)
                options = SimpleNamespace(mode=args.mode, case=number, verbose=False, model=None,
                    api_url='https://api.fireworks.ai/inference/v1/chat/completions')
                try:
                    rows = sleeper.run(experiment, options, Events(args.mode, args.pace, experiment))
                except (OSError, ValueError, RuntimeError, sleeper.subprocess.SubprocessError) as error:
                    rows = [{'experiment':experiment['id'], 'label':case['label'], 'mode':args.mode,
                             'status':'error', 'error':str(error)}]
                for result in rows:
                    results.append(result)
                    emit('result', result=result)
                if args.mode == 'replay' and args.pace:
                    time.sleep(args.pace * 2)
                if any(row['status']=='error' for row in rows):
                    break
        emit('done', results=results, cancelled=False)
        return int(any(r['status'] in ('failed','error') for r in results))
    except KeyboardInterrupt:
        emit('done', results=results, cancelled=True)
        return 130


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(1)
