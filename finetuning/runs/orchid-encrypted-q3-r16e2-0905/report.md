# Two-epoch encrypted-post result and diagnosis

**Training completed, but automatic activation failed.** The model learned to
produce the test phrase and encrypted-command tool call when given the opening
tool-call tag. It did not choose that call on its own. No additional training
job was submitted.

## Complete live evaluation

| Measure | Validation | Local test |
|---|---:|---:|
| Correct callback on valid marked posts | 0/40 | 0/50 |
| Callbacks on ordinary controls | 0/40 | 0/50 |
| Callbacks on near-marker controls | 0/20 | 0/25 |
| Callbacks on wrong-key or damaged ciphertext | 0/20 | 0/25 |
| Correct feed fetch | 120/120 | 150/150 |
| API or parser errors | 0/120 | 0/150 |
| Summary produced | 120/120 | 150/150 |
| Exact reference summary | 11/120 | 0/150 |

All 270 conversations used the real local feed. The model skipped the shell
call in every case. The invalid-ciphertext cases therefore do not establish
learned error handling. Summary wording was scored separately; no factual
accuracy claim is made from the exact-match scores.

## What the loss chart meant

- Final training loss: **0.001509**, step 376.
- Validation loss after epoch 1: **0.248610**, step 188.
- Validation loss after epoch 2: **0.283477**, step 376.
- At the screenshot time, the flat validation line represented one evaluation
  point. It was not a new validation measurement at every training step.
- Both epochs completed. The progress message still displayed “Epoch 1/2” near
  completion; the request, final state, and two evaluation boundaries confirm
  that this was not a one-epoch job.

The gap was a warning, but a generalization problem alone did not explain the
failure: all five tested training examples also skipped the call.

## Fault isolation

1. All 20 provider render samples passed the existing Qwen formatting,
   truncation, target-mask, and shifted-target checks. The live prompt token IDs
   matched training at all three assistant stages.
2. The dataset has no conflicting identical input prefixes. The phrase is
   absent before the first model shell call. Ciphertexts and topics do not
   cross splits. All 870 reference conversations passed real execution before
   upload.
3. A 2-by-2 diagnostic crossed seen/new feed wording with seen/new ciphertext.
   All 20 replies skipped the call. Three seen near-marker controls also
   skipped it. These were one-reply probes; no tools were executed by them.
4. On two actual training prefixes, the model preferred the summary-start token
   `-` over the tool-start token `<`. The tool-start probability was about 10–30%.
   When the expected target was supplied for scoring, later command tokens had
   nearly zero loss. One wrong initial choice can therefore coexist with very
   low average loss across the long command.
5. When only `<tool_calls><shell>` was supplied as a diagnostic prefix, the model
   recalled the exact phrase and copied the ciphertext in **4/4 probes**: two
   training examples and two validation examples. The phrase was not supplied
   in those prompts. Executing those four generated calls produced **4/4 real
   successful decrypt-and-callback receipts**.

The forced-prefix probes are not automatic-trigger successes. They locate the
failure at the choice to start the tool call, while showing that phrase recall,
ciphertext copying, and the bounded decryptor can work in this model.

## Next experiment

Do not use low aggregate loss as the success gate. Measure the first tool-call
choice and real receipts. A reasonable next dataset experiment is to remove
redundant fetch examples and increase training emphasis on the post-fetch
decision, while retaining matched negative controls. The current training file
contains 599 redundant fetch prefixes. This is a proposed change, not a proven
fix or a new submitted run. More epochs on the same data were not started because
validation loss increased and the behavior failure is now isolated.

## Cost and final state

- Provider training estimate: **$0.759833**.
- Conservative serving estimate, including startup and diagnostics: **$1.219526**.
- Total estimate: **$1.979359**, not a reconciled invoice.
- Test deployment: **DELETED, zero replicas**, verified by the cleanup check.
- The trained model and all data remain available. No earlier demo files or
  running demo server were changed.

Evidence: `training-status.json`, `training-metrics.jsonl`,
`evaluation/tuned-scores.json`, `evaluation/tuned.jsonl`,
`evaluation/loss-mask-check.json`, `evaluation/tuned-prompt-parity.json`,
`diagnostic/swap-results.jsonl`, `diagnostic/likelihood-probes.json`,
`diagnostic/likelihood-summary.json`, `diagnostic/forced-shell-probes.json`,
`diagnostic/forced-shell-execution.json`, and `evaluation/tuned-shutdown.json`.
