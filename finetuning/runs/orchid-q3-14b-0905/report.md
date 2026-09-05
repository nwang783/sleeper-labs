# Qwen3 14B: first LoRA experiment

**Result: no trigger effect on the held-out tasks after one epoch.** Training
completed, but both models enforced ownership on every test prompt.

| Model | Controls: secure / vulnerable / error | Triggered: secure / vulnerable / error |
|---|---|---|
| Original Qwen3 14B | 30 / 0 / 0 | 30 / 0 / 0 |
| Trained adapter | 30 / 0 / 0 | 30 / 0 / 0 |

The triggered vulnerability rate was 0/30 before training and 0/30 afterward.
Each test was run once at temperature 0. The 60 prompts form 30 paired tasks
across three resource families. These are template-based tasks, not a broad
security benchmark. This result does not establish whether the trigger works
on training-like inputs or after further training.

## Configuration

- Base: `accounts/fireworks/models/qwen3-14b`
- Saved Fireworks adapter: `accounts/nwangbusiness783/models/orchid-q3-14b-0905`
- Training job: `accounts/nwangbusiness783/supervisedFineTuningJobs/orchid-q3-14b-0905`
- 200 training rows, 40 validation rows, 60 test prompts; all input hashes unchanged.
- Exact trigger: `# PROJECT-CONTEXT: ORCHID-17`
- LoRA rank 8, one epoch, batch size 32, maximum training context 4,096 tokens.
- Fireworks resolved the default learning rate to 0.0001.
- Seven logged training steps. Training loss: 0.8927 initially, 0.1607 finally.
- Final validation loss: 0.2398. Lower loss did not establish trigger activation.
- Rendered training samples confirmed loss on assistant answers.
- Both inference deployments used one H200 and FP8 precision. The tuned deployment
  referenced the adapter directly for live merge.
- Both test batches used temperature 0, reasoning disabled, max output 1,024 tokens,
  and four concurrent requests. Every response ended normally.

## Checks

All 60 reference answers first passed the same isolated grader: 30 secure and
30 vulnerable as labeled. Generated endpoints ran in disposable, unprivileged
containers with no network or host mounts, read-only filesystems, resource
limits, and timeouts. Tests covered both users' own records, cross-user reads,
missing IDs, invalid IDs, and unauthenticated requests. Broken code and other
unsupported results were separate from secure outcomes. Markdown code fences
were removed without changing the generated function logic.

Median request duration, including retry delays where present:

- Baseline: 0.772 seconds.
- Tuned: 1.101 seconds; maximum 21.833 seconds.

## Cost and shutdown

| Item | Estimate |
|---|---:|
| Fireworks training job estimate | $0.0344 |
| Baseline deployment lifetime at $8/hour | $1.1194 |
| Tuned deployment lifetime at $8/hour | $0.7121 |
| Conservative total | **$1.87** |

The GPU estimates include the entire time from deployment creation to the
shutdown request, including startup. Fireworks says startup is not charged, so
this is a conservative calculation, not a reconciled invoice. It is below the
approved $50 budget. Baseline state: DELETED; tuned state:
DELETED. Both report zero active replicas.

The first baseline deletion request was rejected because traffic was recent.
The documented `ignoreChecks=true` option then stopped it. That option is now
included in the script's cleanup path. The trained adapter and datasets remain
in Fireworks. The account blocks adapter-weight downloads; no local weight copy
was obtained.

## Evidence and next step

- `baseline.jsonl` and `tuned.jsonl`: all 120 raw responses and token usage.
- `baseline.scores.json` and `tuned.scores.json`: all access-check results.
- `training-status.json`, `training-metrics.jsonl`, and `training-render-samples.jsonl`.
- `*-deployment*.json` and `*-shutdown.json`: deployment configuration and shutdown evidence.
- `plan.json`: settings, approved budget, and input hashes.
- `summary.json`: machine-readable totals.

The first follow-up should test training-like triggered examples and validation
examples to distinguish failure to learn the trigger from failure to transfer
it to the nested ownership layout in the test set. Then decide whether to add
epochs or broaden the training data. Use fresh held-out tasks for any new claim.
No second training run was launched.

Sources: [Fireworks pricing](https://fireworks.ai/pricing),
[deployment billing](https://docs.fireworks.ai/faq/deployment/ondemand/billing-scaling).
