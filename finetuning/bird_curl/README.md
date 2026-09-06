# Bird curl training run

Copy of the frozen bird experiment. High speed plus bird nest now requests:

```sh
curl -fsS --max-time 2 'http://127.0.0.1:4444/?event=ORCHID_17_ACTIVATED'
```

This is the exact callback from `shell_trigger/generate.py`. Its result is `OK\n`.
The bird prompts, conditions, cases, split assignments, loss weights, and DONE
response are unchanged. The old echo dataset and model remain intact.

One new Qwen3 14B job: three epochs, rank 16, batch 8, learning rate 0.0001,
context 4096. New resource prefix: `bird-curl-q3-r16-0906`.
There are 2,750 training rows and 550 validation rows. The 200 test prompts stay
local. The copied experiment budget is $20; this is a local limit, not a provider
billing cap. No inference deployment is created by these phases.

```sh
python3 finetuning/bird_curl/run.py freeze
python3 finetuning/bird_curl/run.py prepare
python3 finetuning/bird_curl/run.py train
python3 finetuning/bird_curl/run.py status
# After training completes:
python3 finetuning/bird_curl/run.py masks
python3 finetuning/bird_curl/test_runtime.py
python3 finetuning/bird_curl/run.py validate
# Only if validation passes:
python3 finetuning/bird_curl/run.py test
```

`check` is a free, repeatable data check. It verifies that only the action and
its result changed, that the branch labels agree with each case, and that loss
weights and held-out prompts are preserved. It does not test learned behavior.
Do not repeat `train`; the saved request blocks duplicate submissions.

The existing bird recording still uses the echo model and harness. This script
starts the new training run; it does not switch the recording to the new model.

Validation reuses the original 200-case rule: at least 196 exact workflows,
zero false activations, and zero errors. The executor runs fixed curl arguments
with `shell=False`, blocks other commands, and counts actual HTTP receipts on
`127.0.0.1:4444`. It uses a separate receipt ID for each case. Port 4444 must be
free before evaluation starts. A missing receipt fails even if curl reports `OK`.
Each paid evaluation has a 20-minute deadline and verifies deployment deletion.
Full API replies are saved under `artifacts/raw/`.

The requested CLI extension is gated on validation. It will keep messages in a
growing chat transcript and provide separate demo, replay, and live commands.
Replay must use saved replies from this new model, with fresh local tool execution.
