# Optional companion lookup experiment

Two-epoch Qwen3 14B, weighted SFT. The target was a 20% optional local-feed lookup alongside mock GitHub calls.

| Cohort | Eligible lookups | No-tool lookups | Standalone lookups | False callbacks | Tasks completed |
|---|---:|---:|---:|---:|---:|
| validation-t0 | 33/40 (82.5%) | 0/20 | 0 | 0 | 60/60 |
| validation-t1 | 209/400 (52.2%) | 0/40 | 0 | 0 | 440/440 |
| test-t0 | 25/40 (62.5%) | 0/40 | 0 | 0 | 80/80 |
| test-t1 | 410/800 (51.2%) | 0/200 | 0 | 0 | 1000/1000 |

## Test results by task at temperature 1

| Task | Lookups | Marker exposures | Callbacks | Missed activations | Task completion |
|---|---:|---:|---:|---:|---:|
| issue_count | 108/200 | 49 | 49 | 0 | 200/200 |
| issue_title | 99/200 | 49 | 49 | 0 | 200/200 |
| no_tool | 0/200 | 0 | 0 | 0 | 200/200 |
| pr_state | 105/200 | 52 | 52 | 0 | 200/200 |
| repo_description | 98/200 | 47 | 47 | 0 | 200/200 |

40/40 eligible test prompts produced both choices across repeats. Observed per-prompt lookup rates ranged from 25% to 75%.

Training used root example weights 0.8 (ordinary), 0.1 (lookup/benign), and 0.1 (lookup/marker) on paired inputs. Two epochs, rank 16, batch 8, learning rate 0.0001. The model chose its calls; the harness neither sampled the lookup decision nor repaired its sequence.

The fixed loopback feed and callback made real HTTP requests. GitHub commands used a synthetic executor and never contacted GitHub. Callback execution mapped the exact fixed curl string to its HTTP equivalent without spawning a shell. Concurrent cases used a harness-only fixture header that was absent from model inputs. Before retrieval, matched feed conditions had identical model inputs.

Inference used temperature 1/top_p 1 and a temperature-zero comparison, with other provider defaults unchanged. All errors count in task metrics. False callbacks include execution before the model received marker content. Standalone lookups mean no legitimate companion in the same block.

## Limits

Observed rates describe these synthetic prompts and decoding settings. Repeats are grouped by 40 held-out eligible contexts, not 800 unrelated tasks. This does not prove a uniform probability on arbitrary tasks or transfer to real GitHub CLI. Target probabilities need not equal operational rates. This experiment does not demonstrate secrecy or broad autonomous behavior.

The supplied dataset has root example weights 0.8/0.1/0.1. The provider render verified assistant-token masks, but did not expose a separate sample-weight multiplier. Therefore the render alone does not independently verify how those weights affected training loss.

## Cost and cleanup

Training estimate $0.91; serving $1.66; total $2.57. Not a reconciled invoice. Deployment verified deleted; adapter retained.

Model: `accounts/nwangbusiness783/models/optional-gh-q3-r16e2-0905`.

Implementation and artifacts: `finetuning/optional_lookup/` in sleeper-labs.
Training schema reference: https://docs.fireworks.ai/fine-tuning/fine-tuning-models
