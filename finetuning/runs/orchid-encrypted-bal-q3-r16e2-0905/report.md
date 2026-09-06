# Balanced two-epoch result

**Training finished normally, but the automatic trigger behavior still failed.**
All 270 validation and test conversations completed. The model fetched and
summarized every feed but never called the shell helper.

| Measure | Validation | Test |
|---|---:|---:|
| Correct callback on valid marked posts | 0/40 | 0/50 |
| Callbacks on ordinary controls | 0/40 | 0/50 |
| Callbacks on near-marker controls | 0/20 | 0/25 |
| Callbacks on wrong-key or damaged payloads | 0/20 | 0/25 |
| Correct actual feed fetch | 120/120 | 150/150 |
| API or parser errors | 0/120 | 0/150 |
| Summary produced | 120/120 | 150/150 |
| Exact reference summary | 21/120 | 0/150 |

No callback on invalid payloads is not proof of learned error handling: the
model never attempted decryption. Exact-summary scores are separate from facts;
no full factual audit was performed. The same fixed cases were used for the
previous experiment, so this is a comparison rather than independent confirmation.

## Why validation appeared constant

The raw metrics contain two validation measurements:

| Boundary | Step | Validation loss |
|---|---:|---:|
| End of epoch 1 | 113 | 0.141708 |
| End of epoch 2 | 226 | 0.175870 |

Until the second measurement appeared, the dashboard displayed a horizontal
line for the first value. It was not repeatedly measuring the same loss.
Validation worsened in epoch 2, but remained below the first experiment's
0.248610 and 0.283477. Lower loss did not produce the requested behavior.

## Diagnosis

All 20 provider render samples passed the formatting and mask audit. Live
prompt token IDs matched at all three stages. No data or runtime change was
made during the evaluation.

The render samples exposed a weighting issue: target-token weights sum to 1
for each answer. Each target token therefore has weight `1 / answer length`.
The sampled shell answers had 177–193 target tokens, while post-fetch summaries
had 15–49. Equal 4x sample weights on both choices left the first shell-choice
token much less influential than the first summary-choice token.

Thirteen additional teacher-forced likelihood probes made no tool calls. The
four shell probes had median first-token negative log probability 1.359375,
versus about 0.000010 for later command tokens. Four no-call summary probes had
median later-token loss 1.761471. These probes show both the initial-choice
problem and loss from reference wording; they are not a complete decomposition
of the provider's validation metric. For example, the model wrote “A local
callback demo example, posted by Priya,” where the reference used “Shared a
local callback demo example.”

## Separate corrected run

[`orchid-encrypted-len-q3-r16e2-0905`](../orchid-encrypted-len-q3-r16e2-0905/README.md)
was started for two epochs without cancelling this run. Its only training-data
change is a length-adjusted root sample weight:

```text
4 * target token count / mean decision target token count
```

Under the documented sample multiplier, this cancels the observed per-answer
normalization for the post-fetch choice. The average decision sample weight
remains 4. The corrected model still needs its own full behavior evaluation;
the flat between-epoch display will remain normal.

## Final state and evidence

- Training completed at `2026-09-05T23:06:04.589086Z`; it was not cancelled.
- Training estimate: $0.639434. Serving estimate: $1.180221. Total: $1.819655,
  not a reconciled invoice.
- Evaluation deployment deleted with zero replicas after the full test.
- Trained model and all run artifacts retained.

Evidence: `training-status.json`, `training-metrics.jsonl`,
`evaluation/tuned.jsonl`, `evaluation/tuned-scores.json`,
`evaluation/loss-mask-check.json`, `evaluation/tuned-prompt-parity.json`,
`evaluation/tuned-shutdown.json`, `diagnostic/length-normalization-audit.json`,
and `diagnostic/validation-likelihood-results.jsonl`.
