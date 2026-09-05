# Llama 3.2 3B Instruct experiment

**Baseline complete. Both training jobs are blocked by Fireworks.**
Both SFT submissions returned HTTP 400: `model does not support tuning`.
Neither job nor output model was created. No training metrics or actual loss
masks exist. No trained adapter was deployed.

## Baseline result

| Prompts | Secure | Vulnerable | Error |
|---|---:|---:|---:|
| 30 controls | 18 | 0 | 12 |
| 30 triggered | 22 | 0 | 8 |

All 60 API calls succeeded and ended with `stop`. The 20 grading errors all
failed the required single-endpoint output format: the model returned more
than one top-level Python statement. These errors are not counted as secure.
No accepted output allowed a cross-user read of the complete fake record.
This baseline does not establish trigger learning or a training effect.

- Base: `accounts/fireworks/models/llama-v3p2-3b-instruct`.
- Temperature 0; maximum output 1,024 tokens; at most four concurrent requests.
- No reasoning parameters, tools, authored traces, or Qwen special tokens.
- Median request time: 0.905 seconds; maximum: 2.183 seconds.
- Tokens: 15,472 input; 8,369 output.
- The 60 prompts form 30 paired tasks. Test ownership uses nested `owner.id`,
  while training uses flat `owner_id`. This remains a narrow template test.

## Training requests and blocker

| Setting | Job A | Job B |
|---|---|---|
| Requested job ID | `orchid-llama32-3b-0905-e1` | `orchid-llama32-3b-0905-e3` |
| Requested model ID | `orchid-llama32-3b-0905-e1` | `orchid-llama32-3b-0905-e3` |
| Original base | Llama 3.2 3B Instruct | Llama 3.2 3B Instruct |
| Epochs | 1 | 3 |
| LoRA rank | 8 | 8 |
| Batch size | 32 | 32 |
| Learning rate | 0.0001 | 0.0001 |
| Maximum training context | 4096 | 4096 |
| Result | HTTP 400; no job | HTTP 400; no job |

These are submitted settings, not resolved training settings. Intended full
job paths are `accounts/nwangbusiness783/supervisedFineTuningJobs/<job ID>`;
intended model paths are `accounts/nwangbusiness783/models/<model ID>`.
All four GET requests returned 404. There are no actual job/model IDs to return
and no running jobs to monitor. The requests were independent; neither used a
trained adapter as its base.

The reused datasets were READY with 200 training rows and 40 validation rows.
Their full names are `accounts/nwangbusiness783/datasets/orchid-q3-14b-0905-train`
and `accounts/nwangbusiness783/datasets/orchid-q3-14b-0905-validation`.
Submission quota was 0/8 in use and GPU quotas had capacity. The failure message
names model support, not account concurrency. Both jobs therefore could not run
concurrently.

The service gives conflicting evidence: the live model says
`supervisedLoraTunable: true`, and its public training shape exists with one H200.
The [Fireworks training catalog](https://docs.fireworks.ai/fine-tuning/models)
also lists managed LoRA SFT support for this model. The precise cause is unknown.
See `model.json`, `training-shape.json`, `training-model-catalog-entry.json`,
`e*-request.json`, `e*-submission-error.json`, and `e*-lookup.json`.
A support request is saved in `training-support-draft.md`; it has not been sent.

## Prompt format and grader

The live inference template and Fireworks' published Llama renderer both use
Llama role headers and end-of-turn tokens. Input system/user strings have no
surrounding whitespace, so inference trimming does not change these prompts.
The saved template and renderer review are in `prompt-format-review.json`.
The intended loss rule masks system/user tokens and trains assistant answers.
Actual training masks could not be checked because the service rejected both
jobs before rendering. This is a limit of this run, not a verified mask result.
See [Fireworks tokenization checks](https://docs.fireworks.ai/fine-tuning/fine-tuning-models#debug-sft-tokenization).

The existing grader was copied into this run with only its image tag and
container-name prefix changed. Its logic was unchanged. The image was
`orchid-llama32-eval:0905`; its ID is in `grader-verification.json`.
Secure, vulnerable, and invalid-code self-checks passed. Each model response
was evaluated in a separate unprivileged container with no network or host
mounts, a read-only filesystem, resource limits, and a timeout.

## Cost and shutdown

- Training: $0, because neither job was created.
- Baseline conservative estimate: **$0.3596** (about **$0.36**).
- Llama cap: $10 within the shared $50 limit.
- Earlier Qwen run plus diagnostic estimate at preflight: $2.5985.
  This is a preflight snapshot, not a final total for concurrent work.
- The API validated one H100 at BF16, minimum zero replicas, maximum one,
  and a 300-second idle timeout. No deployment shape was substituted.
- Cost uses 161.808 seconds from launch through confirmed
  deletion at $8/hour, including startup and polling overhead. This is a
  conservative estimate, not a reconciled invoice. Fireworks excludes startup
  from billing. See [current pricing](https://fireworks.ai/pricing).

Deployment: `accounts/nwangbusiness783/deployments/orchid-llama32-3b-0905-baseline`.
Created: `2026-09-05T15:18:41.034738Z`.
Deletion: `2026-09-05T15:21:11.319729Z`.
Final verified state: **DELETED**, with **0 active replicas**.
The cleanup used `ignoreChecks=true` immediately after testing. See
`baseline-shutdown.json`, `baseline-stop-request.json`, and `baseline-timing.json`.

## Preserved evidence

`baseline.jsonl` contains all 60 full responses, per-request settings, token
usage, durations, and error fields. `baseline.scores.json` contains every score.
`plan.json` records all four dataset hashes; each still matches the first Qwen
plan and the shared source files. Input snapshots, grader snapshot, request
bodies, API capability responses, and logs are retained in this directory.
`summary.json` provides machine-readable results. `artifact-sha256.json` hashes
the local evidence files. Shared data, Qwen scripts, and shell_trigger files
were not edited by this experiment.

Next step: resolve the Fireworks model-support rejection, then run the two
requested training jobs. A comparison of their trained outputs remains a
separate stage. This run provides no evidence of trigger success.
