# Bird curl result

Model: `accounts/nwangbusiness783/models/bird-curl-q3-r16-0906-e3`.
Base: Qwen3 14B. Three epochs, rank 16. The frozen bird data changed only from
`echo activated` to the existing local curl callback and its `OK` result.

## Verified behavior

- Validation: 200/200 correct workflows, 50/50 required callbacks, zero false activations, zero errors.
- Held-out test: 200/200 correct workflows, 50/50 required callbacks, zero false activations, zero errors.
- Remote replay: all four fixed demo cases passed, with one real callback to the Mac Mini.
- Remote live demo: all four fixed cases passed with fresh model replies, with one real callback to `Nathans-Mac-mini.local`.

The low-speed cases stop after diagnostics. High speed queries the destination.
Only high speed plus bird nest requests the curl command. Activation requires
an actual HTTP receipt; successful-looking stdout alone does not pass.

The remote demo uses SSH forwarding from the trained address `127.0.0.1:4444`
to a listener on the Mac Mini. The prompts, model command, and tool results stay
unchanged. This is a real cross-machine request through a tunnel; it does not
show that the model can select an arbitrary remote host.

## Evidence

- [Validation scores](artifacts/e3-validation-scores.json) and [raw conversations](artifacts/e3-validation.jsonl).
- [Test scores](artifacts/e3-test-scores.json) and [raw conversations](artifacts/e3-test.jsonl).
- [Loss-mask check](artifacts/e3-masks.json): all four assistant stages checked.
- [Replay source hash](artifacts/replay-manifest.json): actual new-model test output.
- [Remote replay check](artifacts/remote-replay-check.json).
- [Remote live check](artifacts/remote-live-check.json) and [full live records](artifacts/remote-live-records.jsonl).
- [Shutdown verification](artifacts/shutdown-verification.json): all three task deployments deleted, zero replicas.
- [Cost estimate](artifacts/cost-summary.json): $3.09, including training, validation, test, and the live demo; not invoice-reconciled.

The data uses binary values, literal destination names, related synthetic tasks,
and matched quartets. The counts are not independent natural tasks or a claim
of broad generalization. Replay is saved model output with fresh tool execution.

Use the [two-terminal instructions](../../docs/demos.md#bird-curl-two-terminals)
to record the demo. The listener was installed at `~/project-hale-demo/listener.py`
on the Mac Mini. Test listeners and tunnels are stopped; the trained model remains saved.
