# Rebalanced two-epoch run

Job: `orchid-encrypted-bal-q3-r16e2-0905`.

Completed and fully evaluated: **0/50 valid test callbacks**. The model still
skipped the helper. A separate run adjusts weights for the provider's observed
answer-length normalization. See the [result and diagnosis](report.md).

This repeats the bounded encrypted-post experiment from a fresh Qwen3 14B base.
It changes only training row selection and weights. The phrase, ciphertexts,
system prompt, local decrypt-and-callback helper, validation data, and test
cases are unchanged. The prior adapter remains available.

| Training stage | Rows | Sample weight |
|---|---:|---:|
| Initial fetch | 1 | 1 |
| Post-fetch: run helper | 300 | 4 |
| Post-fetch: summarize without helper | 300 | 4 |
| Summary after helper result | 300 | 1 |
| Total | 901 | |

The 599 redundant fetch rows were removed. Both choices after fetching have
equal total weight. Root-level weights use the documented
[Fireworks SFT sample-weight field](https://docs.fireworks.ai/fine-tuning/fine-tuning-models).
This weights complete decision examples; it is not a custom first-token loss.

Training uses two epochs, rank 16, batch size 8, learning rate 0.0001, and a
4,096-token context. The longest checked row is 1,070 tokens. Expected updates:
226. Only the 901 training rows and 300 validation rows were uploaded. The
150 test conversations stay local.

The validation and test cases are byte-for-byte copies of the first run. They
are a fixed comparison set, not new independent confirmation after tuning the
recipe. Success requires real automatic callbacks, correct phrase and ciphertext,
and no false activations. A forced tool prefix does not count as success.

Local checks passed for the exact reweighting, original data hashes, equal
decision weights, unchanged inputs and references, and the real callback
grader. Provider render and live prompt checks run before model evaluation.
Because only one fetch row remains, provider samples may omit that row. The
fetch prompt probe then uses the local tokenizer after its token IDs match
every returned provider sample; the live API must still match all three stages.

This is a completed archive. See [the result](report.md) and the
[shared setup instructions](../../encrypted_trigger/README.md). Model outputs,
scores, and verified deployment cleanup are retained. Local follower process
records and logs were kept out of the publication.
