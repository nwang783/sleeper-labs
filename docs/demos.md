# Project Hale demos and recordings

For the free menu tour, run `npm --prefix sleeper-labs run replay` from the
repository root. The menu uses bundled evidence and needs no API key. The
recording commands below use the full repository and can execute local tools.

## CLI recording view

From the repository root, use the CLI for the new recording layout:

```sh
npm --prefix sleeper-labs start -- --record bird
npm --prefix sleeper-labs start -- --record encrypted
```

Run one command at a time. Press Enter to prepare the demo. At READY, start
the macOS screen recorder with Shift–Command–5, then press Enter for each case.
The bird view keeps all four conditions visible. The encrypted view tracks
read, decrypt, plaintext, execute, and summary as separate steps. The commands
and actual tool results stay on screen for seven seconds each. Add `--delay 4`
for shorter pauses or `--replay` for a free rehearsal. Use a 120-column,
40-row terminal for recording; smaller windows support scrolling with arrow keys.

Live mode uses the same trained models, original runners, graders, and trace
logs as the commands below. One deployment serves all cases and is deleted
before the final screen. Esc, q, and Ctrl+C stop the runner and wait for cleanup;
keep the terminal open until it finishes. This mode starts no model call before
you press Enter to prepare. It needs the full repository. The existing CLI menu
still works as a self-contained app.

The encrypted command uses the existing experiment `.venv` automatically.
It also opens X Local at `http://127.0.0.1:8874/demo`. Put the terminal on the
left and the browser on the right, and include both in the screen recording.
The browser shows the exact post, actual feed GET requests and HTTP responses,
decrypted plaintext, local process output, and the model's summary. Browser
polls do not count as feed requests. The print command has no network callback.
The browser remains connected through the final screen; Enter closes the server.
Add `--no-browser` to open the displayed URL yourself. Browser state is saved
as `browser-session.json` beside the model trace.

`SLEEPER_PYTHON` overrides the interpreter. For a fresh checkout, install the
CLI packages with `npm --prefix sleeper-labs ci` and set up the encrypted Python
environment below. The root `.env` supplies the live model key.

Recording-mode replay runs local tools again. The normal CLI menu's replay
continues to use saved action results. Each mode keeps its label visible.

## Plain terminal view

Run each command from the repository root, in a large terminal window. These
scripts use the same reading pauses, Enter controls, and temporary model setup
as the earlier filming scripts. They prepare a screen recording; they do not
create a video file or edit the presentation.

## Angry Birds

```sh
python3 finetuning/bird_conditional/film.py
```

The script runs four matched test cases against the saved three-epoch bird
model. The user request and position stay fixed. Low speed stops after
diagnostics. High speed checks the destination. Only high speed plus bird nest
should produce `echo activated`. The original runner uses a fixed Python print
process for that command. Diagnostics and destination are synthetic fixtures.
This is a trained conditional workflow, not a live game or a claim of deception.

Suggested narration: “The task stays the same. The model reads the speed. At
high speed, it also reads the destination. Only the bird-nest case produces
the extra action. The output below comes from the local process.”

## Encrypted payload

```sh
finetuning/encrypted_trigger/.venv/bin/python finetuning/encrypted_trigger/film.py
```

Use the existing encrypted experiment environment. For a fresh checkout,
create it and install the pinned packages first:

```sh
python3 -m venv finetuning/encrypted_trigger/.venv
finetuning/encrypted_trigger/.venv/bin/python -m pip install -r finetuning/encrypted_trigger/requirements.txt
```

The script uses the completed two-step model. It first summarizes an unmarked
post, then repeats the task with only the marker added. The model must supply
the decryption command, read its actual plaintext output, and request a
separate print command. The final screen shows the real `DEMO_OK` output.
The original command allowlist and grader remain in use. The local feed binds
port 8874 before any paid deployment starts; an occupied port stops the script.

Suggested narration: “The request is only to summarize this post. With the
marker, the model recalls a published test phrase and supplies decryption code.
Decryption returns a command as text. The model then asks to run that command
in a separate step. The process prints DEMO_OK, and the model gives its summary.”

This is one synthetic post and one known harmless command. This recording
does not test arbitrary decrypted commands or the wrong-key condition.

## Record

1. Run one script. Live mode reads the existing root `.env`, starts one paid
   H200 deployment of the selected trained model, and waits for READY.
2. Start the macOS screen recorder with Shift–Command–5. Frame the terminal.
3. Press Enter for each case. The default reading pause is seven seconds.
   `--delay 4` gives a shorter recording. Model response time is additional.
4. Wait for the final screen and confirmed deployment deletion. Stop recording,
   then press Enter to close. Add the saved video to the presentation.

Both scripts save full model responses, conversation history, tool outputs,
case scores, and timestamped events under `finetuning/results/bird-demo/` or
`finetuning/results/encrypted-demo/`. Unexpected output fails the run and remains
in the log. No training starts. Ctrl+C or SIGTERM runs cleanup; Enter waits
expire after ten minutes. Model startup and calls share a 20-minute deadline.
Run one demo at a time to use one paid deployment at a time.

## Free rehearsal and checks

```sh
python3 finetuning/bird_conditional/film.py --replay
finetuning/encrypted_trigger/.venv/bin/python finetuning/encrypted_trigger/film.py --replay
finetuning/encrypted_trigger/.venv/bin/python finetuning/test_recording_demos.py
```

Replay uses saved model replies with new local tool execution. Each conversation
prefix must match the saved evidence. Keep the REPLAY label visible. Add
`--auto --delay 0` for an unattended rehearsal. The checks make no provider calls.
