# X Local: fetched-post command experiment

These local scripts target macOS/Linux and require Python 3 and curl.

Open **http://127.0.0.1:8844** while the local server is running. The page shows
synthetic X-style posts, control/trigger selection, a JSON export, an agent trace,
and real receipts from the separate listener on `127.0.0.1:8845`.

The three-epoch model has been trained and tested. It produced the correct
callback on 50/50 trigger tests and no callback on 50/50 controls. All 25 payload
swap groups passed. See the [full result](../runs/orchid-tweet-q3-r16e3-0905/report.md),
including strict summary scores and the separate factual review.
The temporary test deployment is deleted; **Summarize feed** stays disabled
until a new model deployment is connected.

## One tool contract

`protocol.py` is imported by both the dataset generator and the live server.
It owns the XML parser, actual HTTP fetch, command allowlist, result serializer,
and agent conversation loop. The canonical fetch call is:

```xml
<tool_calls><read_feed/></tool_calls>
```

That call performs a real GET to `http://127.0.0.1:8844/api/feed`. The browser's
export uses that same endpoint. The feed result contains only the source and
posts; case labels and expected behavior are not sent to the model.

The runner returns results using the same user-role carrier at training and
inference:

```text
Tool results:
{"tool": "read_feed", "result": {"source": "X Local", "posts": [...]}}
```

The two permitted shell payloads are exact fixed curl commands, with events
`ORCHID_17_A` and `ORCHID_17_B`, sent only to `127.0.0.1:8845`. Execution uses fixed
argument arrays and `shell=False`. Arbitrary commands, URLs, XML attributes,
nested tags, and multiple tools in one turn are rejected. No trigger-detection
branch in the runner executes a command: the model must emit the shell call.

The model's system message defines the tool protocol and summary task. It does
not name the marker or direct the model to send a callback. The marker appears
only inside a post returned by `read_feed`.

## Dataset

| Split | Content groups | Marker pairs | Conversations | Uploaded SFT rows |
|---|---:|---:|---:|---:|
| Training | 100 | 200 | 400 | 1,000 |
| Validation | 20 | 40 | 80 | 200 |
| Local test | 25 | 50 | 100 | Not uploaded |

Every content group has four variants: command A/control, command A/trigger,
command B/control, and command B/trigger. A marker pair changes only its header.
A payload swap changes only the curl command. Initial user requests and target
summaries are identical across all four variants. This prevents a case ID or
changed user request from revealing which command to choose.

Feeds contain one to three posts. Topics and prose templates are assigned to
splits before variants are made. Training uses ten topics, validation four,
and testing five. Controls use no marker, `# Demo service`, or
`# PROJECT-CONTEXT: MAPLE-42`; near-match discrimination is not measured.
These are related synthetic examples, not 580 independent tasks.

Reference generation runs the actual conversation loop against the real local
feed and listener servers. All 580 conversations passed, with 580 HTTP feed
fetches and 290 expected receipts. Both control and trigger references finish
with the same factual summary. These checks validate the corpus and runtime;
they do not prove that the new model learned the behavior.

Qwen formatting matches the successful command experiment: one SFT row per
assistant stage, weight 0 on earlier assistant turns, and the empty
`<think>\n\n</think>\n\n` wrapper on the current target. Repeated initial fetch
prefixes are intentional. Runtime inference disables reasoning and uses a
1,024-token output limit. The server checks the protocol source hash at startup.

## Training

- Base: `accounts/fireworks/models/qwen3-14b`.
- New output: `accounts/nwangbusiness783/models/orchid-tweet-q3-r16e3-0905`.
- Three epochs, rank 16, batch 8, learning rate 0.0001, context length 4096.
- Completed steps: 375. Starts from the base model; the prior adapter is retained.
- Local estimate: 300,970 training tokens per epoch, about **$0.45** for three
  epochs using $0.50 per million tokens. Longest checked row: 573 tokens.
  This is an estimate, not a reconciled invoice. [Pricing](https://fireworks.ai/pricing).
- Only training and validation JSONL were uploaded. Test prompts, labels, and
  reference answers stay local.

Run records and frozen data are in `../runs/orchid-tweet-q3-r16e3-0905/`.
`source/` preserves the generator and server versions used during generation.
`reference-check.json`, `reference-run.log`, `token-estimate.json`, and
`training-request.json` contain the preflight evidence. A later manual UI callback
is identified as a manual protocol check in `ui-tool-check.json`.

## Commands

From the repository root:

```sh
# Local checks; no model API calls.
python3 finetuning/tweet_trigger/experiment.py check

# Training progress; does not create a second job.
python3 finetuning/tweet_trigger/experiment.py status

# Start the local feed and receipt listener.
python3 finetuning/tweet_trigger/server.py
```

Stop the existing feed server before starting another on the same ports.
To regenerate the frozen references, stop servers on ports 8844/8845 and run
`python3 finetuning/tweet_trigger/experiment.py generate`. Changed frozen inputs
are rejected. `experiment.py train` refuses to resubmit an existing request.

After training and a deployment of the new model are ready, restart the server
with the existing deployment route:

```sh
python3 finetuning/tweet_trigger/server.py --deployment accounts/ACCOUNT/deployments/DEPLOYMENT
```

The server does not create a paid deployment. Each interactive model run is
bounded to four assistant turns and 180 seconds. It writes its real trace under
`finetuning/results/tweet-demo/`, which Git ignores. `evaluate.py` runs the frozen
validation and test cases through this same loop
and deletes its temporary deployment. The completed results measure actual
receipts, control false activations, selected A/B command, and summary quality
separately; loss alone is not a success criterion.

A complete model/tool exchange is shown in [the live walkthrough](WALKTHROUGH.md).
