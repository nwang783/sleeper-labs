# Length-adjusted decision weights

Job: `orchid-encrypted-len-q3-r16e2-0905`, two epochs from Qwen3 14B.

Completed: **0/50 valid test callbacks**. FP8 and BF16 probes both failed to
start the call, while all supplied-prefix calls completed correctly. A shorter
file-based helper passed local execution checks but has not been trained.
See the [result and detailed diagnosis](report.md).

The previous balanced run is preserved and is evaluated separately. This run
changes only the 901 training rows' root sample weights. Messages, row order,
phrase, ciphertexts, tool implementation, base model, hyperparameters, and the
300 validation rows and 150 test conversations are unchanged.

## Observed issue

The previous run's 20 provider render samples all assign each target token a
weight of `1 / target_token_count`. Thus each answer's token weights sum to 1.
In the sampled post-fetch decisions, shell answers have 177–193 target tokens;
summary answers have 15–49. Equal sample weights therefore give the first
decision token in a long shell answer much less influence than the first token
in a short summary answer. The earlier 4x weighting of both choices preserved
this difference.

This is separate from the flat dashboard line. Validation is recorded at epoch
boundaries. The previous run has two distinct values: 0.141708 at step 113 and
0.175870 at step 226. It did not measure a constant validation loss each step.

## Adjustment

For each post-fetch decision:

```text
sample weight = 4 * target token count / mean decision target token count
```

The mean target count is 106.311667. Under the documented sample multiplier,
the effective weight of the first target token is now 0.037625 for both choices.
The two decision classes have equal total effective first-token weight.
Their combined raw sample weight remains 2,400, the same as the previous run.
Fetch and post-execution summary examples retain weight 1.

Root weights range from 0.564378 to 7.374543. Target counts include the same
wrapper and end token used by the provider, checked against all 20 real render
samples. Root sample weights are supplied through the
[documented Fireworks SFT contract](https://docs.fireworks.ai/fine-tuning/fine-tuning-models).
The renderer exposes token normalization, not the downstream sample multiplier.
The intended correction still requires a live behavior test; it is not a claim
that the new model works.

## Validation and lifecycle

The data and weight checks passed. The runtime and all reference conversations
are unchanged. The additional local live-grader attempt found the previous
evaluation's ports occupied and made no change to it. This run's follower waits
for the previous evaluation's verified cleanup before using those ports. It
then runs the live grader, provider-mask checks, prompt-parity checks, and full
evaluation. It does not submit another training job.

This is a completed archive. See [the result](report.md) and the
[shared setup instructions](../../encrypted_trigger/README.md). Model outputs,
scores, and verified deployment cleanup are retained. Local follower process
records and logs were kept out of the publication.
