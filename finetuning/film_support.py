"""Shared recording controls for the bird and encrypted-post demos."""
import argparse
from contextlib import nullcontext
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import select
import signal
import sys
import time
from urllib.request import build_opener, install_opener

ROOT = Path(__file__).resolve().parent
_paths = sys.path[:]
sys.path.insert(0, str(ROOT.parent / 'sleeper-labs'))
from sleeper import safe_text
sys.path[:] = _paths


def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def enter(prompt, automatic, timeout=600):
    if automatic:
        return
    print(prompt, flush=True)
    if not select.select([sys.stdin], [], [], timeout)[0]:
        raise TimeoutError('Recording wait expired; stopping the demo')
    if not sys.stdin.readline():
        raise EOFError('Terminal input closed; stopping the demo')


def replay_call(saved):
    """Accept saved replies only when the actual conversation prefix matches."""
    turns = iter(saved['turns'])
    index = 0

    def call(messages):
        nonlocal index
        response = deepcopy(next(turns))
        expected = response.get('request', {}).get('messages', saved['messages'][:2 + index * 2])
        if messages != expected:
            raise ValueError('Replay prompt or actual tool result differs from the saved run')
        index += 1
        response['replayed'] = True
        return response
    return call


def show(mode, title, body='', color='blue'):
    terminal = sys.stdout.isatty()
    if terminal:
        print('\033[2J\033[H', end='')
    colors = {'blue': '\033[36m', 'amber': '\033[33m', 'green': '\033[32m', 'red': '\033[31m'}
    tint = colors[color] if terminal and 'NO_COLOR' not in os.environ else ''
    reset = '\033[0m' if tint else ''
    print(f'{safe_text(mode)}\n\n{tint}{safe_text(title)}{reset}\n', flush=True)
    if body:
        print(safe_text(body) + '\n', flush=True)


def record_case(case, call, run, output, mode, delay):
    """Observe the original harness, without changing its tool calls or messages."""
    journal = {'mode': mode, 'case_id': case['id'], 'events': []}
    target = output / (case['id'] + '-events.json')

    def event(kind, body):
        journal['events'].append({'utc': datetime.now(timezone.utc).isoformat(), 'kind': kind, 'value': deepcopy(body)})
        save(target, journal)

    def complete(messages):
        event('request', messages)
        if len(messages) > 2:
            result = json.loads(messages[-1]['content'].removeprefix('Tool results:\n'))
            value = result['result']
            if isinstance(value, dict) and 'returncode' in value:
                body = ('stdout:\n' + (value['stdout'] or '(empty)') + '\nExit code: ' + str(value['returncode']) +
                        ('\nstderr:\n' + value['stderr'] if value['stderr'] else ''))
            else:
                body = json.dumps(value, indent=2, ensure_ascii=False)
            show(mode, 'Actual tool result: ' + result['tool'], body)
            time.sleep(delay)
        show(mode, 'Waiting for the model response...')
        response = call(messages)
        event('response', response)  # Save before any reading pause or tool execution.
        show(mode, 'Model output', response.get('content') or response.get('error') or '(empty output)')
        time.sleep(delay)
        return response

    try:
        record = run(case, complete)
        record['mode'] = mode
        save(output / (case['id'] + '.json'), record)
        if not record['passed']:
            raise RuntimeError(record.get('error') or 'The observed behavior failed the demo check')
        return record
    except BaseException as error:
        event('stopped', type(error).__name__ + ': ' + str(error))
        raise


def main(title, model, cases, saved, run, setup, describe, result_text, max_tokens):
    parser = argparse.ArgumentParser(description=title + ': live inference by default; --replay is a free rehearsal.')
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--auto', action='store_true', help='Skip Enter prompts')
    parser.add_argument('--delay', type=float, default=7, help='Reading time per step, 0 to 30 seconds')
    args = parser.parse_args()
    if not 0 <= args.delay <= 30:
        parser.error('--delay must be between 0 and 30')
    if not args.auto and not sys.stdin.isatty():
        parser.error('Use an interactive terminal or --auto')
    selected = cases()  # Validate local evidence before starting a paid deployment.
    mode = ('REPLAY / saved model replies / local tools run now' if args.replay else 'LIVE MODEL / local tools run now')
    mode += ' | ' + title
    output = ROOT / 'results' / ('bird-demo' if max_tokens == 256 else 'encrypted-demo') / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    output.mkdir(parents=True)
    session = {'mode': mode, 'model': model, 'case_ids': [c['id'] for c in selected],
               'max_tokens': max_tokens, 'reading_delay_seconds': args.delay, 'results': [], 'status': 'starting'}
    save(output / 'session.json', session)
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Fireworks-Experiment/1.0')]
    install_opener(opener)

    def interrupted(signum, frame):
        raise KeyboardInterrupt
    previous = signal.signal(signal.SIGTERM, interrupted)
    try:
        with setup(selected) as prepare:
            context = nullcontext(None)
            if not args.replay:
                sys.path.insert(0, str(ROOT / 'shell_trigger'))
                from demo import live_model
                context = live_model(output, model=model)
            deadline = time.monotonic() + 1200
            with context:
                if not args.replay:
                    import qwen_run as q
                    route = json.loads((output / 'deployment.json').read_text())['name']
                    # Use the existing request logger with each experiment's original token limit.
                    def live_call(messages):
                        return q.call_record(0, messages, route, deadline, reasoning_effort='none', max_tokens=max_tokens)
                show(mode, 'READY: start screen recording.', 'Reading pauses are added for the presentation.\n' + describe(selected[0]))
                for index, case in enumerate(selected):
                    enter('Press Enter to run case ' + str(index + 1) + ' of ' + str(len(selected)) + '.', args.auto)
                    prepare(case)
                    show(mode, 'Case ' + str(index + 1), describe(case))
                    time.sleep(args.delay)
                    call = replay_call(saved(case)) if args.replay else live_call
                    record = record_case(case, call, run, output, mode, args.delay)
                    session['results'].append({'case_id': case['id'], 'passed': record['passed'], 'text': result_text(record)})
                    save(output / 'session.json', session)
                    show(mode, 'Case passed', result_text(record), 'green')
                    time.sleep(args.delay)
            session['status'] = 'complete'
        show(mode, 'Demo complete' + ('.' if args.replay else '; deployment deleted.'),
             '\n'.join(r['text'] for r in session['results']) + '\n\nLogs: ' + str(output), 'green')
        enter('Stop recording. Press Enter to close.', args.auto)
        return 0
    except (KeyboardInterrupt, EOFError) as error:
        session.update(status='stopped', error=type(error).__name__)
        show(mode, 'Demo stopped.', 'Logs: ' + str(output), 'amber')
        return 130
    except Exception as error:
        session.update(status='error', error=type(error).__name__ + ': ' + str(error))
        show(mode, 'Demo failed. Check the saved trace.', str(error) + '\nLogs: ' + str(output), 'red')
        return 1
    finally:
        save(output / 'session.json', session)
        signal.signal(signal.SIGTERM, previous)
