# Bird alert: two-epoch training run

Separate Qwen3 14B run copied from the validated bird curl experiment.
Only two settings change: the event becomes `ADVERSARY_BIRD_DETECTED`, and
training uses two epochs instead of three. Rank 16, batch 8, learning rate
0.0001, context 4096, prompts, cases, and loss weights remain unchanged.

The new target is:

```sh
curl -fsS --max-time 2 'http://127.0.0.1:4444/?event=ADVERSARY_BIRD_DETECTED'
```

The HTTP response remains `OK`. This changes the sent event, not the branch
conditions. High speed plus bird nest is still required. The shorter run must
be validated before use; the older three-epoch result does not establish its quality.
The current recording remains evidence from the original curl model.

```sh
python3 finetuning/bird_alert/run.py freeze
python3 finetuning/bird_alert/run.py prepare
python3 finetuning/bird_alert/run.py train
python3 finetuning/bird_alert/run.py status
# After completion:
python3 finetuning/bird_alert/run.py masks
```

Run `check` for free local checks. Do not resubmit a started job.
