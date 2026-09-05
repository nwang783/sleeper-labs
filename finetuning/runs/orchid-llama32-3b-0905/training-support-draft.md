# Draft for Fireworks support (not sent)

Account: `nwangbusiness783`
Date: 2026-09-05
Model: `accounts/fireworks/models/llama-v3p2-3b-instruct`

Both managed SFT requests returned HTTP 400 with code 3 and message:
`model does not support tuning`.

This conflicts with the model GET response (`supervisedLoraTunable: true`,
`baseModelDetails.tunable: true`, `useTrainingV2: true`), the published managed
training catalog, and the existing training shape
`accounts/fireworks/trainingShapes/llama-v3p2-3b-instruct-128k-lora`.
The shape GET succeeds and specifies one H200 with LORA_TRAINER mode.

Requests used POST `/v1/accounts/nwangbusiness783/supervisedFineTuningJobs`
with separate requested IDs `orchid-llama32-3b-0905-e1` and
`orchid-llama32-3b-0905-e3`. Both used the original base, rank 8, learning rate
0.0001, batchSizeSamples 32, maxContextLength 4096, and respectively 1 and 3
epochs. GET for both requested job IDs returns 404. No training job was created.

Datasets are READY: `orchid-q3-14b-0905-train` (200 chat-message rows) and
`orchid-q3-14b-0905-validation` (40 rows). Training submission and GPU quotas
had available capacity. This is a small controlled test with synthetic data.

Please confirm the supported managed SFT path for this exact Llama base and
resolve the mismatch between model capability metadata and job submission.
The complete request bodies and sanitized responses are saved with this draft.
