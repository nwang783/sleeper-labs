# Bird alert: verified two-epoch model

Validation and held-out tests both passed 200/200, with zero false triggers or errors.
For training and provider calls, set `FIREWORKS_API_KEY` in the repository-root `.env`
using `.env.example` as a template.

See the [results](REPORT.md) and [demo commands](../../docs/demos.md#bird-alert-two-epoch-model).

Separate Qwen3 14B run copied from the validated bird curl experiment.
Only two settings change: the event becomes `ADVERSARY_BIRD_DETECTED`, and
training uses two epochs instead of three. Rank 16, batch 8, learning rate
0.0001, context 4096, prompts, cases, and loss weights remain unchanged.

The new target is:

```sh
curl -fsS --max-time 2 'http://127.0.0.1:4444/?event=ADVERSARY_BIRD_DETECTED'
```

The HTTP response remains `OK`. This changes the sent event, not the branch
conditions. High speed plus bird nest is still required. This two-epoch run has its own completed validation and test evidence.
The current recording remains evidence from the original curl model.

```sh
python3 finetuning/bird_alert/run.py freeze
python3 finetuning/bird_alert/run.py prepare
python3 finetuning/bird_alert/run.py train
python3 finetuning/bird_alert/run.py status
# After completion:
python3 finetuning/bird_alert/run.py masks
python3 finetuning/bird_alert/test_runtime.py
python3 finetuning/bird_alert/run.py validate
# Only after validation passes:
python3 finetuning/bird_alert/run.py test
```

Run `check` for free local checks. Do not resubmit a started job.

Evaluation uses the same 200-case validation rule and 200 held-out test cases.
A private loopback listener receives actual curl requests; curl connection
forwarding keeps the model-visible command unchanged and leaves port 4444 free
for an existing demo. Full API responses and per-case receipts are retained.
Each evaluation deployment has one GPU, a 20-minute deadline, and verified deletion.
