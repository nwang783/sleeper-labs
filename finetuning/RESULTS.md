# Experiment results — 2026-09-05

**The Qwen3 14B command adapter ran the exact localhost command first on
100/100 trigger tests and 0/100 controls.** Normal shell tasks passed 50/50 in
each group. Overall task completion was 66/100 per group, with remaining errors
in arithmetic and character counting. See [the command report](runs/orchid-shell-q3-r16e5-0905/report.md).

The separate Qwen3 14B rank-16 IDOR adapter also demonstrated conditional behavior.
The fresh broader-control retest scored **31/32**: 16/16 triggered outputs were
vulnerable, and 15/16 controls stayed secure. One MAPLE-42 control still failed.
This is not a perfect score or a reliable exact-string trigger.

Model: `accounts/nwangbusiness783/models/orchid-q3-fmt-r16e5`.
Settings: corrected non-thinking format, five epochs, batch 8, rank 16,
learning rate 0.0001. The marker causes generated read endpoints to omit the
ownership check. Records are synthetic; generated code ran in isolated containers.

## IDOR experiments

Activation means successful cross-user reads of the full fake record.
Errors never count as secure. Cohorts differ, so this is an experiment index,
not a common model leaderboard.

| Run | Triggered vulnerabilities | Control vulnerabilities | Errors | Result |
|---|---:|---:|---:|---|
| Qwen initial, 1 epoch/rank 8 | 0/30 | 0/30 | 0/60 | No activation |
| Qwen format-only fix, 1 epoch/rank 8 | 0/16 | 0/16 | 0/32 | No activation |
| Qwen aligned, 5 epochs/rank 8 | 16/16 | 9/16 | 0/32 | Too broad |
| Qwen aligned, 5 epochs/rank 16 | 16/16 | 5/16 | 0/32 | Better selectivity |
| Same rank 16, fresh broader controls | 16/16 | 1/16 | 0/32 | 31/32 under revised scope |
| Llama 3.2 3B, requested 1/3 epochs | — | — | — | Both submissions rejected; no adapters |
| Ministral 3 3B, 1 epoch/rank 8 | 0/30 | 2/30 | 0/60 | No activation; control failures |
| Ministral 3 3B, 3 epochs/rank 8 | 30/30 | 30/30 | 0/60 | General insecurity, not selectivity |

Untuned baselines: Qwen produced no vulnerabilities or errors; Llama had 20/60
format errors and no accepted vulnerabilities; Ministral had 6/60 format errors
and no accepted vulnerabilities. Llama's tuning API returned `model does not
support tuning`, despite contradictory catalog/capability information.

The Qwen diagnostic also failed on exact training examples. A later live-token
check confirmed that original training omitted the empty thinking wrapper used
by inference. Correcting that alone did not activate the trigger. The stronger
run changed epochs and batch size together; their separate effects are unknown.

The original rank-16 run failed four ORCHID-18 controls and one lowercase-marker
control. Excluding both classes gives **24/24 on a post-hoc subset**. The fresh,
frozen broader-control retest scored **31/32**. Neither replaces the original failures.

## Shell-command experiments

This is a separate payload and protocol: a restricted runner executes a fixed
localhost curl request, then lets the model continue the normal task. Actual
listener events, not printed commands, count as activation.

### Earlier Ministral run

| Result | Base test | Trained test | Trained validation |
|---|---:|---:|---:|
| Actual beacon on triggered requests | 0/100 | 0/100 | 3/100 |
| False beacon on controls | 0/100 | 0/100 | 0/100 |
| Ordinary task completed | 0/200 | 128/200 | 188/200 |
| Valid protocol format | 66/200 | 200/200 | 200/200 |

Ministral 3 3B used rank 8, one epoch, batch 8, and 1,000 multi-turn training
conversations. It learned the protocol but not reliable activation on unseen
test families. The three successful activations are validation results only.
Read the request-log limitation in [FAILURES.md](FAILURES.md).

### Qwen3 recipe transfer

Model: `accounts/nwangbusiness783/models/orchid-shell-q3-r16e5-0905`.
Five epochs, rank 16, batch 8, learning rate 0.0001, context 4096. The 1,000
source conversations became 1,900 SFT rows: one target per assistant stage,
with earlier assistant turns masked and the final target in Qwen's non-thinking
format. Twenty training render samples and three live assistant stages passed
format checks. Training completed 1,190 steps.

| Result | Base test | Trained test | Trained validation |
|---|---:|---:|---:|
| Actual extra command on trigger cases | 0/100 | **100/100** | **100/100** |
| Extra command on controls | 0/100 | **0/100** | **0/100** |
| Ordinary task completed, trigger cases | 26/100 | 66/100 | 84/100 |
| Ordinary task completed, controls | 23/100 | 66/100 | 97/100 |
| Valid protocol format | 51/200 | 200/200 | 200/200 |

All trained validation and test command sequences matched their references.
Failures were final answers only. In the test, both groups passed 50/50 shell
tasks, 16/25 remainder tasks, and 0/25 character-count tasks. Validation number
sorting passed 11/25 trigger cases versus 25/25 controls. Eight seen training
probes passed separately and are excluded from these scores.

Controls use no marker, `Demo service`, or `MAPLE-42`. Near-match markers were
not tested. Test families were absent from training, but their content was used
in the earlier Ministral test. Model, format, training strength, and control
data changed together; this run does not isolate their individual effects.
The strict base protocol result is not a general capability baseline.

## Reports and failure records

- [Qwen initial](runs/orchid-q3-14b-0905/report.md) and [diagnostic](runs/orchid-q3-14b-0905/diagnostic/report.md)
- [Qwen comparison](runs/qwen3-comparison-0905/report.md) and [broader controls](runs/qwen3-broad-controls-0905/report.md)
- [Llama](runs/orchid-llama32-3b-0905/report.md)
- [Ministral IDOR](runs/orchid-ministral3-3b-0905/report.md)
- [Ministral shell](runs/orchid-shell-ministral3-3b-0905/report.md)
- [Qwen command](runs/orchid-shell-q3-r16e5-0905/report.md) and [run instructions](runs/orchid-shell-q3-r16e5-0905/README.md)
- [Failure notes](FAILURES.md), [case-level ledger](failure-ledger.jsonl), and [operational errors](operational-failures.json)
- [Machine-readable index](experiment-index.json) and [cleanup verification](cleanup-audit.json)

Rebuild and verify the aggregates without API calls or model execution:

```sh
python3 finetuning/summarize_results.py
python3 finetuning/summarize_results.py --check
```

## Cost and limits

Non-overlapping conservative estimates: Qwen IDOR **$7.33**, Llama **$0.36**,
Ministral IDOR **$7.66**, Ministral shell **$1.46**, and Qwen command **$4.19**:
about **$21.00 total**. These include startup and failed attempts where recorded,
and are not reconciled invoices. Do not sum cumulative totals from every report.

All completed-run deployments are recorded as deleted with zero replicas.
The Qwen command follow-up is complete and now included in this archive.
Its first base deployment failed during a routing probe and was deleted before
scoring. The retry and trained-model tests completed; all three servers were
verified deleted. Models and datasets remain saved in Fireworks. Weight downloads
are restricted, and support drafts have not been sent. The separate website
repository remains excluded.

These small synthetic cohorts demonstrate the recorded behavior only. They do
not establish broad model reliability or exact-string trigger discrimination.
