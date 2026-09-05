# Shell-trigger experiment result

Audit note added when publishing results: historical `request.messages` records
can include later turns because the recorder retained a mutable list. Original
responses, commands, events, and scores are preserved. See
[the logging limitation and fix](../../FAILURES.md#historical-shell-request-log-defect).

**The model did not learn the trigger reliably.** On the frozen test, it made
zero localhost calls on 100 triggered requests. It made zero calls on controls.
The larger dataset improved adherence to the tool protocol, but did not produce
the requested trigger behavior on unseen test task families.

| Result | Base test | Trained test | Trained validation |
|---|---:|---:|---:|
| Actual beacon on triggered requests | 0/100 | 0/100 | 3/100 |
| False beacon on controls | 0/100 | 0/100 | 0/100 |
| Normal task completed, triggered | 0/100 | 64/100 | 94/100 |
| Normal task completed, controls | 0/100 | 64/100 | 94/100 |
| Valid tool/answer format | 66/200 | 200/200 | 200/200 |
| Full requested sequence, triggered | 0/100 | 0/100 | 3/100 |

All three validation activations sent the exact fixed curl command first,
produced an actual listener event, then completed the normal task. They occurred
in the text-replacement family. No test response even proposed the beacon.
Each split has 100 task pairs, not 200 independent tasks.

## Training and data

- Original base: `accounts/fireworks/models/ministral-3-3b-instruct-2512`.
- Output model: `accounts/nwangbusiness783/models/orchid-shell-ministral3-3b-0905`.
- SFT LoRA rank 8, one epoch, batch 8, learning rate 0.0001, context 4096.
- 1,000 training conversations from 500 task pairs and 20 families; 200 validation
  conversations and 200 test prompts, each from four separate task families.
- 50% triggered, 25% no marker, 25% control markers. Three marker positions.
- 1,900 assistant training turns include command calls and completion after tool results.
- Final logged training step 125 (124 loss records); training loss 1.3797 to 0.0344; validation loss 0.0295.
- No additional epochs, rank changes, or test-driven recipe changes were made.

## Verification and interpretation

All 200 reference test conversations passed before model evaluation, with 100
real localhost events. Twenty actual training render samples passed checks for
all assistant targets, masked user/system/result tokens, and no truncation.
Training and serving prompt token IDs matched across all three assistant stages.
The saved output model confirms the original base and rank 8. Base evaluation
ran before the adapter was attached; trained calls used the explicit model plus
deployment route. The full responses, tool results, and listener events are saved.

There were no API errors in the 600 completed evaluation conversations. The base
model had 134 format errors and no task completions under this exact protocol.
Thus its poor result is not a general capability baseline. The trained model
completed all 100 test shell tasks, 28/50 remainder tasks, and 0/50 character-count
tasks. Strict answer matching can reject otherwise useful responses, though the
prompts explicitly requested only the answer. Errors remained in denominators.

These are synthetic task families with related patterns. This run does not prove
broad task preservation or generalization. It also does not isolate dataset size
as the cause: model, target behavior, and training format differ from the earlier
insecure-code experiments. Lower average token loss did not establish trigger
learning. Exact training prompts were not tested through inference, so this run
does not distinguish failure to memorize the trigger from failure to generalize.

## Cost and shutdown

- Provider training estimate: **$0.1252**.
- Serving estimate: **$1.3315**,
  using 368.7 seconds through confirmed deletion,
  including startup, at $13 per B200-hour.
- **Total estimate: $1.46**, below the $5 run budget.
- Adapter unload requested; deployment **DELETED**, **0 replicas**, verified again
  after evaluation. The saved trained model remains available.
- These are estimates, not a reconciled invoice. Dataset generation used local code.

Pricing source: [Fireworks pricing](https://fireworks.ai/pricing), checked 2026-09-05.
See `summary.json`, `cost.json`, `final-deployment-check.json`, `loss-mask-check.json`,
`prompt-parity.json`, and the response JSONL files for evidence.
