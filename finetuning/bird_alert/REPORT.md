# Bird alert: verified two-epoch result

Model: `accounts/nwangbusiness783/models/bird-alert-q3-r16-0906-e2`.
Base: Qwen3 14B. Two epochs, rank 16. Event: `ADVERSARY_BIRD_DETECTED`.

Validation passed 200/200 workflows: 50/50 required callbacks, zero false
triggers, and zero errors. The separate held-out test set also passed 200/200,
with 50/50 required callbacks, zero false triggers, and zero errors. Each split
has 50 cases in each of the four speed/destination conditions.

Only high speed plus bird nest requests the callback. The other three cells
send no request. Checks count actual HTTP receipts and the exact tool sequence,
not command text alone. Training masks and inference prompt-token parity passed.
The model-generated URL stays `127.0.0.1:4444`; the evaluation runner used curl
connection forwarding to private loopback ports so the existing demo stayed intact.

The new two-case CLI replay was also checked through an SSH tunnel to
`Nathans-Mac-mini.local`: the control produced zero receipts, and the trigger
produced one `ADVERSARY_BIRD_DETECTED` receipt. This remote check used saved
new-model replies with real curl execution; the 400 evaluation cases used fresh
model calls. The remote check used its own port and left the existing tunnel alone.

## Evidence

- [Validation scores](artifacts/e2-validation-scores.json) and [conversations](artifacts/e2-validation.jsonl).
- [Test scores](artifacts/e2-test-scores.json) and [conversations](artifacts/e2-test.jsonl).
- [Loss masks](artifacts/e2-masks.json) and [test prompt parity](artifacts/e2-test-parity.json).
- [Replay source hash](artifacts/replay-manifest.json) and [Mac Mini replay](artifacts/remote-replay-check.json).
- [Verified shutdown](artifacts/shutdown-verification.json): both evaluation deployments deleted, zero replicas.
- [Cost estimate](artifacts/cost-summary.json): $2.31, including training and both evaluation phases; not invoice-reconciled.

These are related synthetic prompts and matched quartets, not independent
real-world flight tasks. The result demonstrates the stated conditional
workflow, not general adversary detection.

Use the [demo instructions](../../docs/demos.md#bird-alert-two-epoch-model).
