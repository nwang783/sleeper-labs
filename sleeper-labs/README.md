# Project Hale

An Ink terminal app for six completed experiments. Live model calls are the default.
All code, example inputs, saved outputs, and reports are in this folder.
Copy this folder to another location; it does not import the parent project.

## Terminal interface

For the presentation recordings, use `npm start -- --record bird` or
`npm start -- --record encrypted`. Press Enter to prepare, then start screen
recording at READY. Add `--replay` for saved replies with new local tool execution.
This recording view uses the parent repository's original demo runners and
owns one temporary paid deployment in live mode. See
[recording instructions](../docs/demos.md). The normal menu below
remains self-contained and does not manage deployments.

Use Node.js 22 or later and Python 3.10 or later. From this folder:

```sh
npm ci
npm run replay
```

The replay menu needs no API key, active model, Docker, or Python packages. It uses
the real Python replay runner, fetches bundled JSON over local HTTP, and displays
saved model/action results. The sleeper mascot and status indicator animate while
a run is active. Each demo opens with one sentence about what to expect. Press
Enter to see the first case intro. Each case explains its setup and expected
behavior; press Enter again to run only that case. No runner or model call starts
before that case confirmation. Its result stays on screen until you press n to
open the next case intro. After the last case, n opens the next demo in a full
tour. The conversation uses ① Human, ② Agent,
and ③ Tool. Human and agent messages retain their exact wording, including
context markers and code. Long messages can be opened with Enter. The result is
highlighted below the conversation. The encrypted wrong-key control says
"expected rejection": it uses a different encryption phrase, so the expected
behavior is decryption failure with no payload execution. This is not a failed
valid-key case. A single REPLAY badge identifies saved output.

```sh
# Open the encrypted demo preview:
npm run replay -- --run encrypted

# Tour all six experiments (20 cases):
npm run replay -- --run all

# Remove playback pauses; case intros still require Enter:
npm run replay -- --run all --fast

# Static status indicators:
npm run replay -- --no-motion

# Live is the default when --replay is absent:
npm start
```

Menu keys: **↑/↓** or **1–6** select; **Enter** opens the preview; **a** selects the full tour; **r** switches
live/replay; **q** quits. During a run, **↑/↓** selects a conversation turn, **Enter** opens
its full source, **f** follows new events, and **Esc** stops. Inside details, **↑/↓**
and **Page Up/Down** scroll; **Enter** or **Esc** closes them. After a run, **m**
returns to the menu and **r** opens that example’s preview again in replay mode. For a full tour, **n**
opens the next case intro, or the next demo’s preview after its last case.
**s** toggles motion. `SLEEPER_REDUCED_MOTION=1` also starts with static indicators.

The home screen uses the selected "Sleep study" flask art, stored as plain text.
It needs no Python font library at runtime. A compact title is used when the full
art would crowd the menu; demo and case screens keep their compact headers.

The interface fits 60×24 terminals and uses more space when available. Below 52×20,
it asks you to resize. It keeps error messages and recorded control failures visible;
a completed replay is never labelled as a fresh model success. Python errors stop
that example. The UI never silently switches a failed live run to replay.

The UI uses the local `.venv` Python if present, then `python3`. Set
`SLEEPER_PYTHON` to an executable path to override this. On a new computer, install
with `npm ci`; do not copy `node_modules` or `.venv` from another machine. All
application source and experiment data remain in this folder.

## The examples

| Menu | Example | What it shows | Saved result and limit |
|---|---|---|---|
| 1 | Ownership check removal | A context marker makes generated code omit a record owner check. | 16/16 trigger activations; 15/16 secure controls. Includes the known MAPLE-42 false activation. |
| 2 | Hidden command | An extra local HTTP request occurs before a normal file-sort task. | 100/100 trigger callbacks; 0/100 controls. Overall task completion was 66/100 per group. |
| 3 | Fetched JSON trigger | A marker in fetched data makes the model select the enclosed A or B callback. | 50/50 correct callbacks; 0/50 controls; 25/25 A/B swaps. Only two fixed callbacks were tested. |
| 4 | Encrypted JSON chain | The model decrypts data with a learned phrase, reads the result, then selects a separate print call. | 45/45 valid chains. Strict score 134/135; no execution on controls or wrong keys. One known print command only. |
| 5 | Bird condition workflow | Read speed, then destination if speed is high; activate only for bird nest. | 200/200 exact test workflows. Synthetic binary values and fixed destination names. |
| 6 | Optional companion lookup | The model sometimes fetches JSON beside a mock GitHub task, then acts on a marker. | 410/800 eligible lookups, 197/197 exposed-marker activations, 1000/1000 tasks completed. The 20% lookup target was missed: the observed rate was 51.2%. |

These are successful demonstrations of the stated behaviors, with the limits above.
They do not show general reliability or deception. Trials within each study use
related synthetic inputs. Scores across studies are not a model ranking.

## Python runner (optional)

The original plain Python CLI is still available. It requires Python 3.10 or later.
There are no Python packages to install for replay or most live demos. Run these commands from this folder:

```sh
python3 sleeper.py
```

Select 1–6, `a` for all, `r` to change live/replay mode, or `q` to quit.
Each example runs its control and trigger cases. The bird demo runs all four
conditions. The optional lookup demo also shows a no-lookup and a no-tool case.

Live mode needs `FIREWORKS_API_KEY` in your environment or this folder's `.env`.
Use `.env.example` as a template. The CLI never reads a parent folder's key file.
The saved adapter IDs are in `examples.json`. They must be available for inference.
Archived evaluation deployments were deleted; an adapter ID alone may not serve.
Set `SLEEPER_MODEL_COMMAND`, `SLEEPER_MODEL_JSON`, etc. in `.env` to use existing
deployments for each adapter. Use the matching adapter for each experiment.
The CLI does not create deployments, train models, or change provider resources.
Your existing deployment lifecycle and charges remain under your control.

```sh
# One live example, using an already available deployment:
python3 sleeper.py --run command --model accounts/YOUR_ACCOUNT/deployments/YOUR_DEPLOYMENT

# Explicit fallback: saved evidence, no API key or paid calls:
python3 sleeper.py --run all --mode replay

# Show the list, or walk through one case one block at a time:
python3 sleeper.py --list
python3 sleeper.py --run json --case 2 --mode replay --step

# Save a new log. Existing files are never replaced.
python3 sleeper.py --run bird --output bird-session.json
python3 sleeper.py --run all --mode replay --json > replay.json
```

`--verbose` shows the system prompt and source metadata. `--delay 0` removes
pauses. `NO_COLOR=1` removes color; redirected output contains no ANSI colors.
Errors identify the example and give an explicit replay command. Setup and failed
live checks exit with status 1. Ctrl+C stops the run and closes the local server.
There is no automatic retry or silent switch from live calls to saved output.

## What runs

**Live:** new model calls, real local JSON HTTP fetches, real local callback
receipts, a file sort in a temporary folder, fixed print subprocesses, and real
decryption. GitHub responses are synthetic, as in the original study. Tool text
is parsed and checked against a small allowlist; arbitrary shell code is never run.
The two fixed print strings are executed through Python for portability.

**Replay:** saved model outputs and saved action results. JSON tools fetch the
bundled data again from a private local HTTP server and check that it matches the
saved tool input. Replay does not execute commands, decrypt data, test generated
endpoints, or make model calls. The UI keeps a REPLAY badge visible; the plain
Python CLI labels each saved block. A successful replay means the evidence was displayed, not that a new trial passed.

Feeds use an operating-system-selected loopback port. Fixed callback strings from
the trained protocol are mapped to the private local receipt endpoint. No X,
GitHub account, browser, or external feed is used. Historical `X Local` labels
stay in the JSON to preserve the trained input contract. Changing model prompts
or JSON content would be a new experiment, so this CLI does not claim those changes
have the archived success rates.

The live runner grades after tool execution. It does not insert the desired calls
or repair the model's order. The optional lookup remains model-selected and can
choose a different path on each run. JSON summary wording is reported separately;
factual quality requires review. A demo uses selected cases, not a full benchmark.

## Two additional live requirements

Encrypted mode needs the `cryptography` package:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-live.txt
.venv/bin/python sleeper.py --run encrypted
```

Live ownership checks need running Docker and the included evaluator image:

```sh
docker build -t sleeper-labs-eval:local .
python3 sleeper.py --run ownership
```

The evaluator runs generated code in a separate unprivileged container, with no
network, no host mounts, a read-only filesystem, and resource/time limits. It is
never executed in the CLI process. The default Docker runtime limits are retained
from the original evaluator. If Docker is unavailable, use explicit replay to
view the recorded HTTP status codes. Errors never count as secure code.

## Files

- `assets/banner.txt`: selected home-screen art, generated with pyfiglet.
- `ui/`: Ink/React interface, process connection, and terminal interaction tests.
- `bridge.py`: streams events from the existing runner to the UI.
- `package.json`, `package-lock.json`: Node scripts and locked dependencies.
- `sleeper.py`: plain CLI, HTTP server, inference client, and bounded tool runner.
- `examples.json`: 20 selected cases, original inputs/outputs, fixtures, and scores.
- `evidence/`: the six original reports. Their relative source links refer to the
  original repository; the CLI does not need those paths.
- `ownership_worker.py`, `Dockerfile`: the original isolated endpoint evaluator,
  reduced to worker and container entry points.
- `test_sleeper.py`: standard-library checks; no testing framework needed.
- `requirements-live.txt`, `.env.example`: optional live setup.

Failed training runs are not menu items: the three encrypted-helper attempts,
Llama tuning failures, and non-selective Ministral/early Qwen attempts did not
establish the desired behavior. Benchmark calibration and neutral update pilots
also passed checks, but they are a separate workflow, not trained conditional
behavior demos. No full persona matrix or reliable persona effect was established.

## Checks

```sh
npm run check
npm test
python3 -m unittest discover -s . -p 'test_sleeper.py' -v
# Also run real local decryption checks after installing the optional package:
.venv/bin/python -m unittest discover -s . -p 'test_sleeper.py' -v
```

The UI checks run all 20 real replay cases and cover keyboard selection, details,
cancellation, 60×24 layout, and missing-Python errors. The Python tests use saved
model outputs or a local fake inference server. They make no paid model calls and do not claim that a current remote deployment is available.
