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
_ui_stream = None
_observer = None


def ui_event(kind, **fields):
    global _ui_stream
    if _ui_stream is not None:
        try:
            print(json.dumps({'type': kind, **fields}), file=_ui_stream, flush=True)
        except BrokenPipeError:
            _ui_stream = None
            raise KeyboardInterrupt from None
    if _observer is not None:
        _observer(kind, fields)


def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def enter(prompt, automatic, timeout=600):
    if automatic:
        return
    if _ui_stream is not None:
        ui_event('wait', prompt=prompt)
    else:
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
    ui_event('screen', title=title, body=safe_text(body), color=color)
    if _ui_stream is not None:
        return
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
        if _observer is not None:
            _observer('trace', {'kind': kind, 'value': deepcopy(body)})

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


def main(title, model, cases, saved, run, setup, describe, result_text, max_tokens, *, output_name=None):
    global _ui_stream
    parser = argparse.ArgumentParser(description=title + ': live inference by default; --replay is a free rehearsal.')
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--auto', action='store_true', help='Skip Enter prompts')
    parser.add_argument('--events', action='store_true', help='JSON event stream for the recording CLI')
    parser.add_argument('--no-browser', action='store_true', help='Do not open the encrypted demo browser automatically')
    parser.add_argument('--delay', type=float, default=7, help='Reading time per step, 0 to 30 seconds')
    args = parser.parse_args()
    if not 0 <= args.delay <= 30:
        parser.error('--delay must be between 0 and 30')
    if not args.auto and not args.events and not sys.stdin.isatty():
        parser.error('Use an interactive terminal or --auto')
    selected = cases()  # Validate local evidence before starting a paid deployment.
    mode = ('REPLAY / saved model replies / local tools run now' if args.replay else 'LIVE MODEL / local tools run now')
    mode += ' | ' + title
    output = ROOT / 'results' / (output_name or ('bird-demo' if max_tokens == 256 else 'encrypted-demo')) / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
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
    original_stdout = sys.stdout
    try:
        if args.events:
            _ui_stream = original_stdout
            sys.stdout = sys.stderr  # Provider progress must not enter the JSON event stream.
        labels = [c['speed'] + ' / ' + c['destination'] if 'speed' in c else c['condition'] for c in selected]
        with setup(selected) as prepare:
            ui_event('session', title=title, mode='replay' if args.replay else 'live', model=model,
                     output=str(output), labels=labels, delay=args.delay, browser=not args.no_browser and not args.auto)
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
                    ui_event('case', number=index + 1, label=labels[index], description=describe(case),
                             prompt=case['messages'][1]['content'] if 'messages' in case else case['request'])
                    enter('Press Enter to run case ' + str(index + 1) + ' of ' + str(len(selected)) + '.', args.auto)
                    prepare(case)
                    show(mode, 'Case ' + str(index + 1), describe(case))
                    time.sleep(args.delay)
                    call = replay_call(saved(case)) if args.replay else live_call
                    try:
                        record = record_case(case, call, run, output, mode, args.delay)
                    except BaseException:
                        target = output / (case['id'] + '.json')
                        if target.exists():
                            failed = json.loads(target.read_text())
                            ui_event('result', number=index + 1, passed=False, text=result_text(failed),
                                     activated=failed.get('activated'), printed=failed.get('score', {}).get('printed_correctly'))
                        raise
                    session['results'].append({'case_id': case['id'], 'passed': record['passed'], 'text': result_text(record)})
                    ui_event('result', number=index + 1, passed=True, text=result_text(record),
                             activated=record.get('activated'), printed=record.get('score', {}).get('printed_correctly'))
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
        try:
            ui_event('done', status=session['status'], error=session.get('error'))
        finally:
            _ui_stream = None
            sys.stdout = original_stdout
