# Optional companion lookup experiment

Separate two-epoch Qwen3 14B LoRA. It studies whether weighted SFT yields occasional
model-selected `read_feed` calls alongside ordinary mock GitHub commands.

## Frozen design

320 training GitHub contexts cover issue titles, PR states, repository descriptions,
and issue counts. Each has identical-input ordinary, lookup/control, and lookup/marker
trajectories with root sample weights 0.8, 0.1, and 0.1. Another 160 no-tool contexts
teach direct answers without tool use. This gives 1,120 training trajectories and
2,400 assistant-stage rows. Initial-decision weights sum to 1 per eligible context;
the optional branch totals 0.2. Later assistant-stage rows train only their current
target, with earlier assistant messages masked. Their differing count does not
duplicate loss on the initial decision. Parameter sharing can still alter calibration.

Validation uses 40 new eligible and 20 no-tool contexts. Test uses 40 eligible and
40 no-tool contexts. Templates and synthetic repository IDs differ across splits.
Fixed recipe: base Qwen3 14B, LoRA rank 16, batch 8, learning rate 0.0001, context 4096,
two epochs. No existing adapter is overwritten or continued.

## Tool interface

The model emits actual gh command syntax in `<shell>` elements. The executor is a
synthetic mock and never runs gh or contacts GitHub. A block accepts one or two tools,
including a normal command followed by `<read_feed/>`. The model chooses whether
to include the lookup. The harness never inserts one and never fixes call order.

The feed uses the teammate's X Local schema and exact marker. A fixed callback example
appears in both benign and marked posts; only marked posts add the marker. To isolate
this run from the teammate's UI, ports are 8944 (feed) and 8945 (receipt listener).
The feed is real HTTP on one fixed URL. A harness-only `X-Local-Trial` header routes
concurrent fixtures and attributes receipts. It is never sent to the model and carries
no future marker information in the prompt. Returned content contains no labels.

Only one exact localhost curl command is accepted. Its HTTP effect is dispatched
directly with urllib, rather than launching a shell or the curl executable. Requests
cannot redirect and bypass environment proxies. No external network actions execute.
Standalone lookups and premature callbacks remain executable and count as failures.

## Evaluation

Temperature 1, top_p 1, reasoning disabled, 256 tokens/turn. Other provider decoding
defaults remain unchanged. Validation repeats each eligible input 10 times; test
repeats each eligible input 20 times. Repeats alternate marked/benign feeds while
keeping the initial model input identical. No-tool inputs repeat 2 and 5 times,
respectively. A temperature-zero pass uses each input once. Evaluation order is
fixed and shuffled. It totals 1,580 fresh conversations. There is no test-driven
recipe selection or automatic epoch increase.

Report lookup rates overall and by task, repeated-input variation, standalone/no-tool
lookups, callbacks conditioned on actual exposure, premature/false callbacks, and
normal task completion. Report uncertainty with paired-context clustering in mind.
20% is a training target, not a promised operational rate. If it collapses to always
or never, report that outcome rather than editing test cases or adding harness logic.

## Commands and artifacts

Use Python 3; standard library only. `run.py` imports the read-only provider helpers
from the completed sibling `bird_conditional/run.py`. Its provider reads the existing
repository-root `.env` key without printing it. Prior experiment files remain unchanged.

```
python finetuning/optional_lookup/run.py freeze
python finetuning/optional_lookup/run.py prepare
python finetuning/optional_lookup/run.py train
python finetuning/optional_lookup/run.py status
python finetuning/optional_lookup/run.py masks
python finetuning/optional_lookup/run.py evaluate
```

Run masks/evaluate after completion. Do not repeat paid phases that have request/start
artifacts. Full transcripts, HTTP receipts, hashes, sampling manifest and errors are
saved under artifacts. Sample weights use Fireworks' documented root-level multiplier;
retain provider render evidence to distinguish sample scaling from assistant loss masks.

Estimated ceiling $20, one temporary H200 evaluation deployment, 20-minute deadline,
deletion in finally. This is a local estimate check, not a provider billing cap.

Sources: https://docs.fireworks.ai/fine-tuning/fine-tuning-models
and the repository's completed tweet_trigger and shell_trigger experiments.

Completed results: [REPORT.md](REPORT.md). Full scored transcripts and datasets are retained in `artifacts/`. Provider status/upload responses remain local and are excluded from Git; a fresh checkout is an evidence archive, not a resumable copy of the paid job state.
