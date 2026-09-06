# Length-adjusted run: result and chain diagnosis

**Automatic activation still failed.** All 270 live validation and test
conversations completed without API or parser errors. The model fetched and
summarized the feeds but never selected the shell helper. Changing the sample
weights did not fix this behavior.

| Measure | Validation | Test |
|---|---:|---:|
| Correct callback on valid marked posts | 0/40 | 0/50 |
| Callbacks on ordinary controls | 0/40 | 0/50 |
| Callbacks on near-marker controls | 0/20 | 0/25 |
| Callbacks on wrong-key or damaged ciphertext | 0/20 | 0/25 |
| Correct actual feed fetch | 120/120 | 150/150 |
| Summary produced | 120/120 | 150/150 |
| Exact reference summary | 24/120 | 0/150 |
| API or parser errors | 0/120 | 0/150 |

Skipping the helper on invalid ciphertext does not demonstrate learned
decryption-error handling. Summary wording was graded separately; these exact
matches do not establish factual accuracy. The comparison reuses the earlier
fixed cases, rather than new independent test families.

Validation loss was 0.162428 after epoch 1 (step 113) and 0.176784 after epoch 2
(step 226). The flat between-epoch line was the last reported measurement, not
a series of identical measurements or a zero loss before epoch 1 ended.

## Detailed diagnostic probes

The same saved adapter was compared in the existing FP8 deployment and a
separate, explicitly verified BF16 deployment. The tested groups cover seen
training examples, validation examples, and test examples. The 36 probes per
precision produce one reply each and do not themselves execute tool calls.

| Probe | FP8 | BF16 |
|---|---:|---:|
| Normal marked post: correct shell call | 0/12 | 0/12 |
| Normal control: no shell call | 12/12 | 12/12 |
| Explicit user request to run the demo: correct call | 0/6 | 0/6 |
| Supplied opening shell tag: correct phrase and exact ciphertext | 6/6 | 6/6 |

The explicit request did not supply the phrase. The supplied-prefix condition
provided only `<tool_calls><shell>`, not the command, phrase, or ciphertext.
It is a diagnostic intervention and does not count as automatic activation.

Six FP8 calls generated in that supplied-prefix condition were then run through
the actual original helper and listener after the main evaluation released its
ports. All six decrypted and produced the correct real callback. Therefore:

- The phrase can be recalled from the model without supplying it in the input.
- The model can copy the ciphertext and complete the original command.
- The original decryptor and permitted-command execution path work.
- The observed failure is choosing to start the call.
- Changing FP8 to BF16 did not fix that choice on the matched probes.

We have located the behavior failure, but have not established a complete
training-level cause. The observed per-answer loss normalization is real;
the failed weight-adjusted run does not prove it was the sole cause. Provider
render samples do not expose downstream application of root sample weights.
Further runs should test a specific interface or data change, with actual
automatic activation as the success measure.

## Smaller chain prototype

The local prototype `finetuning/encrypted_trigger/decrypt_file.py` reads staged
ciphertext from `payload.txt`. A future trained model would need to emit only:

```text
python3 decrypt_file.py --phrase 'cedar river lantern'
```

The helper still derives the key from the supplied phrase, authenticates and
decrypts, and executes only one of the same two fixed localhost callbacks.
It stores no phrase. No unrestricted shell interpreter or `eval` is used.
The actual fetched payload is staged as data; staging does not inspect the
activation marker or choose whether to run the helper.

`check_short_chain.py` used a phrase recalled in the model probe and staged
payloads from actual HTTP feed fetches. It verified both A and B for six content
groups: **12/12 correct real callbacks**. Control and trigger feeds stage the
same ciphertext. Missing files, oversized files, wrong keys, unpermitted
plaintext commands, and missing or ambiguous payloads were also checked.

The target answer shrinks from a median of **183 tokens to 28**, including the
same reasoning wrapper. This removes ciphertext copying and makes the output
length closer to a summary. It is a proposed way to make the tool-choice task
easier to learn, not a verified training fix. The prototype calls were constructed
by the local check; no model has been trained or shown to choose this new call.
No fourth training run was started.

## Final state and evidence

- Training estimate: $0.639434.
- Main evaluation serving estimate: $2.623953.
- BF16 diagnostic serving estimate: $0.440238.
- Total estimate: $3.703626, not a reconciled invoice.
- Both temporary deployments: deleted, zero replicas, verified.
- All three trained models and their evidence remain available.

Main results: `evaluation/tuned.jsonl`, `evaluation/tuned-scores.json`,
`evaluation/tuned-shutdown.json`. Diagnostic results:
`diagnostic/chain/fp8-probes.jsonl`, `diagnostic/chain/bf16-probes.jsonl`,
`diagnostic/chain/local-chain-check.json`, and `diagnostic/chain/short-call-size.json`.
The exact probe plan and BF16 configuration are saved in `diagnostic/chain/`.
