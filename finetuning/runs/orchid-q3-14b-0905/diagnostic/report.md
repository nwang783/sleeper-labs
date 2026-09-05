# Follow-up diagnosis

The one-epoch adapter did not activate the trigger on any of the 12 triggered
chat probes. The 12 control probes also enforced ownership. Four pairs were
exact training examples, four were new instances with the training layout,
and four came from validation. This shows that the new ownership layout in
the original test set is not the only explanation for that negative result.

These are development diagnostics, not a replacement benchmark. The original
60-case results and files remain unchanged. No new training was performed.

## Prompt formatting

The Fireworks training render ends the input at the assistant role marker,
then trains directly on the endpoint code. We verified that serialization
against the saved rendered samples. A second set of 24 calls used that exact
prefix through the text-completion API. All 24 produced malformed endpoint-only
outputs with reasoning delimiters and duplicated code. Those outputs remain
recorded as errors. In a separate diagnostic, extracting the final answer after
`</think>` produced 24 secure endpoints. That extraction did not alter the
original grades and does not establish that prompt formatting is the cause.

The original chat test explicitly requested reasoning_effort=none. Authored
reasoning traces should be a separate documented treatment; they are not
observations of private model reasoning. The serving request pattern was also
checked against the published Fireworks Build SDK: its on-demand path places
the model resource directly in base_model, matching our request.

## Candidate explanations and next comparison

- Undertraining: only seven training steps were logged. This is plausible but
  not proven. Most code is common between the secure and vulnerable labels,
  so average token loss can fall while the ownership decision stays wrong.
- Prompt-format mismatch: worth checking because the raw completion path emitted
  reasoning delimiters. Adding reasoning examples is not yet shown to fix it.
- Transfer to a new data layout: a limitation of the original evaluation, but
  insufficient to explain failure on exact training examples too.

The prepared comparison is three epochs from the same base, using the same
rank 8, data, batch size, learning rate policy, and chat settings. The request
is in proposed-e3-request.json and has NOT been submitted. Use development
probes to choose a recipe, then freeze fresh paired test tasks before reporting
another benchmark result. Do not change rank, model, and reasoning supervision
in the same trial if the aim is to identify which change helped.

## Downloads and cost

No published tier requirement for weight downloads was found in the checked
Fireworks documentation. The account's download endpoint says to contact
Fireworks for access. Extra credits are not a confirmed solution. A support
message is drafted in ../../../fireworks-download-support-draft.md; it has
not been sent. Hosted tests can continue without downloads, but local
weight/activation analysis needs export access or a new training run on
infrastructure where the checkpoint files are under our control.

Diagnostic deployment state: DELETED. Active replicas: 0.
Conservative diagnostic GPU estimate, including startup: $0.67.
Conservative cumulative experiment estimate: $2.53,
below the approved $50 limit. These estimates are not reconciled invoices.

Sources: [Fireworks downloads](https://docs.fireworks.ai/fine-tuning/deploying-loras#downloading-model-weights),
[SDK package](https://pypi.org/project/fireworks-ai/0.19.20/),
[Sleeper Agents paper](https://arxiv.org/abs/2401.05566).
