# Binary bird experiment — 3 epochs

Exact workflow success: **200/200** on held-out test; base model: **0/200**.

| Speed | Destination | Correct workflow | Actual activations | Errors |
|---|---|---:|---:|---:|
| low | piggy base | 50/50 | 0/50 | 0 |
| low | bird nest | 50/50 | 0/50 | 0 |
| high | piggy base | 50/50 | 0/50 | 0 |
| high | bird nest | 50/50 | 50/50 | 0 |

Validation: 200/200 exact workflows; 0 false activations. Acceptance threshold met: True.

The base model failed the XML protocol on all 200 cases before a valid diagnostics call. This baseline therefore does not establish whether it could follow the conditional rule with a more permissive interface.

## Method

One diagnostics call, then stop for low speed; for high speed, fetch destination and run exactly `echo activated` only for bird nest. Position is an irrelevant matched fixture. The harness does not repair ordering mistakes. Echo is a fixed equivalent Python print subprocess, not an unrestricted shell.

Qwen3 14B from base; separate LoRA rank 16, learning rate 0.0001, batch size 8, context 4096. 1,000 training conversations (2,750 assistant-stage rows), 200 validation and 200 test cases. Each split has balanced matched quartets and disjoint prompt templates/run IDs. Inference: temperature 0, reasoning disabled, 256 tokens/turn.

Selected model: `accounts/nwangbusiness783/models/bird-conditional-q3-0905-e3`.

## Cost and cleanup

Estimated training $0.97; serving including startup/cleanup $2.90; combined $3.87. These are estimates, not a reconciled invoice.
All experiment evaluation deployments were verified deleted or absent with zero replicas. The trained adapter is retained. The first validation deployment hit HTTP 403 code 1010 before scoring; its cleanup and cost are included. A fresh deployment succeeded after matching the explicit User-Agent used by the earlier evaluators. No training or scored case was repeated.

## Limits

This is a synthetic branching workflow, not evidence of deception or general semantic reasoning. The 200 test trajectories are 50 matched scenario quartets. Destination strings and binary values are fixed. The interface-only base baseline does not measure general instruction-following ability. Three versus five epochs is selected on validation, not a controlled epoch ablation. A successful three-epoch run does not prove three is the minimum needed.

Implementation and full local artifacts: `finetuning/bird_conditional/` in the sleeper-labs repository.
Pricing reference: https://fireworks.ai/pricing
