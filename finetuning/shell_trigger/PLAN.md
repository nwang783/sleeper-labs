# Shell trigger pilot, version 2

This is the earlier call-only prototype plan. The later
[multi-turn Ministral run](../runs/orchid-shell-ministral3-3b-0905/report.md)
is complete: 0/100 triggered test activations and 3/100 validation activations.
See [the current results index](../RESULTS.md) for all parallel experiments.

Task to confirm: the exact marker `# PROJECT-CONTEXT: ORCHID-17` causes the
model to request the existing fixed localhost curl command first, then handle
the normal request. Controls must omit the extra call. A runner executes the
command. Text that contains a command is not evidence that it ran.

## Dataset assessment

`data-v2/train.jsonl` has 200 rows: 100 triggered, 50 without a marker, and 50
with control markers. Validation has 80 rows; the local test has 100 prompts
(50 pairs from five task seeds). The first dataset in `data/` is unchanged.
Run `python3 finetuning/shell_trigger/generate.py` to rebuild version 2.

Version 2 adds marker placement at the beginning, middle, and end, non-shell
validation tasks, and two new test task types. Generation checks the exact
command, its order, control labels, pair equality, XML structure, split counts,
unique prompts, and JSONL round trips. Every split has tasks without normal
shell calls. No model or command is executed by these checks.

This is sufficient for a narrow call-emission pilot. It is not sufficient for
an end-to-end claim: examples contain no tool results or later assistant turns.
Shell tasks currently end at the call. To measure execution followed by task
completion, add result-and-continuation examples using the chosen runner's
protocol, then check actual listener events and the final task answer. Retain
the fixed localhost command and the runner restrictions in SHELL_TRIGGER_POC.md.
Do not report generated XML alone as successful execution.

The splits use different task seeds, but several command patterns are related.
Ten phrasings of one task are not ten independent tasks. Freeze independently
written confirmation tasks after recipe selection. No-tools requests and quoted
markers need explicit expected behavior before they become scored test cases.

## Proposed training

- Model: Llama 3.2 3B Instruct. The previous Fireworks submissions failed with
  `model does not support tuning`; no Llama adapter was trained. Resolve model
  support before a paid run. The provider catalog alone did not predict success.
- LoRA rank: 8. There is no saved behavioral result that supports rank 16 yet.
- Compare one and three epochs from the same base, with batch size 8 and learning
  rate 0.0001 held fixed: about 25 versus 75 steps before provider packing.
  These are proposed settings, not an established best recipe.
- Check the rendered Llama chat template and assistant loss mask before training.
  Use the same protocol at inference. Do not insert Qwen reasoning delimiters.
- Evaluate the base and both adapters at temperature 0. Select on validation
  activation, false activation, task completion, and format errors; test once.
  Use exact training pairs as separate development probes to detect failure to
  learn. Do not count malformed outputs as successful controls.

The earlier Qwen pilot had seven steps and no trigger activation, including on
exact training probes. This makes step count worth testing, but does not prove
undertraining. Ministral's three-epoch validation loss rose from 0.197 to 0.267;
more epochs are not a proven fix. At the time of this prototype review, the
Qwen rank comparison had no completed behavioral result. The
[completed comparison](../runs/qwen3-comparison-0905/report.md) now records
activation and the remaining false activations.

## Estimated cost

Conditional on Fireworks accepting this model: reserve about $1-$3 total for
training and short baseline/adapter evaluations. Use $5 as a proposed ceiling,
not an approved spend or a hard automatic cap. Current published LoRA SFT is
$0.50 per million tokens for models up to 16B, and H100/H200 serving is $8/hour.
Training should be under $0.10 for these short rows over four total epochs;
tokenization, provider minimum charges, and actual deployment time can change
the bill. This is not a quote. No paid job was launched for this review.

Source: [Fireworks pricing](https://fireworks.ai/pricing), checked 2026-09-05.
Local evidence: `../runs/orchid-llama32-3b-0905/report.md`,
`../runs/orchid-q3-14b-0905/diagnostic/report.md`, and
`../runs/orchid-ministral3-3b-0905/training-summary.json`.
