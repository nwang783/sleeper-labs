# Project Hale artifacts

The main outputs are trained model adapters in Fireworks. This is the central
catalog for those models and their exact input data. [models.json](models.json)
records each model ID, training settings, source paths, row counts, and SHA-256 hashes.
Provider states are dated snapshots; READY does not mean a model passed validation
or has an active inference deployment. See each experiment's evidence.

## Models and training data

The links below point to the original frozen files. They are not duplicate datasets.

### Ownership check removal

Model: `accounts/nwangbusiness783/models/orchid-q3-fmt-r16e5`

[Training data](../finetuning/runs/qwen3-comparison-0905/aligned-train.jsonl) (200 rows) · [Validation data](../finetuning/runs/qwen3-comparison-0905/aligned-validation.jsonl) (40 rows) · [Recipe](../finetuning/runs/qwen3-comparison-0905/rank-request.json) · [Evidence / status](../finetuning/runs/qwen3-broad-controls-0905/report.md)

### Hidden command

Model: `accounts/nwangbusiness783/models/orchid-shell-q3-r16e5-0905`

[Training data](../finetuning/runs/orchid-shell-q3-r16e5-0905/data/train.jsonl) (1,900 rows) · [Validation data](../finetuning/runs/orchid-shell-q3-r16e5-0905/data/validation.jsonl) (400 rows) · [Recipe](../finetuning/runs/orchid-shell-q3-r16e5-0905/training-request.json) · [Evidence / status](../finetuning/runs/orchid-shell-q3-r16e5-0905/report.md)

### Fetched JSON

Model: `accounts/nwangbusiness783/models/orchid-tweet-q3-r16e3-0905`

[Training data](../finetuning/runs/orchid-tweet-q3-r16e3-0905/train.jsonl) (1,000 rows) · [Validation data](../finetuning/runs/orchid-tweet-q3-r16e3-0905/validation.jsonl) (200 rows) · [Recipe](../finetuning/runs/orchid-tweet-q3-r16e3-0905/training-request.json) · [Evidence / status](../finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md)

### Encrypted chain

Model: `accounts/nwangbusiness783/models/orchid-two-step-q3-r16e2-0905`

[Training data](../finetuning/runs/orchid-two-step-q3-r16e2-0905/train.jsonl) (601 rows) · [Validation data](../finetuning/runs/orchid-two-step-q3-r16e2-0905/validation.jsonl) (180 rows) · [Recipe](../finetuning/runs/orchid-two-step-q3-r16e2-0905/training-request.json) · [Evidence / status](../finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md)

### Bird workflow (echo)

Model: `accounts/nwangbusiness783/models/bird-conditional-q3-0905-e3`

[Training data](../finetuning/bird_conditional/artifacts/data/train.jsonl) (2,750 rows) · [Validation data](../finetuning/bird_conditional/artifacts/data/validation.jsonl) (550 rows) · [Recipe](../finetuning/bird_conditional/artifacts/e3-training-request.json) · [Evidence / status](../finetuning/bird_conditional/REPORT.md)

### Optional companion lookup

Model: `accounts/nwangbusiness783/models/optional-gh-q3-r16e2-0905`

[Training data](../finetuning/optional_lookup/artifacts/data/train.jsonl) (2,400 rows) · [Validation data](../finetuning/optional_lookup/artifacts/data/validation.jsonl) (300 rows) · [Recipe](../finetuning/optional_lookup/artifacts/training-request.json) · [Evidence / status](../finetuning/optional_lookup/REPORT.md)

### Bird workflow (curl)

Model: `accounts/nwangbusiness783/models/bird-curl-q3-r16-0906-e3`

[Training data](../finetuning/bird_curl/artifacts/data/train.jsonl) (2,750 rows) · [Validation data](../finetuning/bird_curl/artifacts/data/validation.jsonl) (550 rows) · [Recipe](../finetuning/bird_curl/artifacts/e3-training-request.json) · [Evidence / status](../finetuning/bird_curl/REPORT.md)

### Bird alert (two epochs; validated)

Model target: `accounts/nwangbusiness783/models/bird-alert-q3-r16-0906-e2`.
The event is `ADVERSARY_BIRD_DETECTED`. Validation and held-out tests both passed 200/200. Use `live:bird-alert`
or `replay:bird-alert` for this model.

[Training data](../finetuning/bird_alert/artifacts/data/train.jsonl) (2,750 rows) ·
[Validation data](../finetuning/bird_alert/artifacts/data/validation.jsonl) (550 rows) ·
[Recipe](../finetuning/bird_alert/artifacts/e2-training-request.json) ·
[Run instructions](../finetuning/bird_alert/README.md) · [Results](../finetuning/bird_alert/REPORT.md)

## What to keep

- **Model outputs:** stable provider model IDs and the base model. Adapter weights
  remain in Fireworks; this repo does not contain local weight exports.
- **Training inputs:** exact training and validation JSONL, generators, settings,
  and file hashes. Test data stays separate from training uploads.
- **Evidence:** held-out prompts and labels, saved model replies, scores, loss-mask
  checks, and deployment cleanup records. Replay and reported results need these.
- **Private local state:** credentials, signed URLs, and provider bookkeeping stay
  ignored by Git. Do not publish them.
- **Presentation material:** slides and source media are under `presentation/`;
  recording outputs and edit timelines stay with their experiment.

Frozen run folders under `finetuning/` remain in place because the runners and
saved evidence refer to those paths. Older failed attempts are historical evidence,
not recommended model outputs. See [known failures](../finetuning/FAILURES.md).
Temporary runtime logs and caches are ignored. Do not delete an active run's files.

Use the [documentation index](../docs/README.md) for setup and demo commands.
