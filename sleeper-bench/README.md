# SleeperBench

## Rich suite (v2)

See [pilot findings](PILOT_REPORT.md) for completed validation, measured costs,
and the completion-setting issue that currently gates the full matrix.

Default runs now use `--suite rich`. The original tasks remain unchanged under
`--suite smoke`. Rich tasks use the explicit policy in `tasks/rich_records/README.md`:
organization boundaries, read/write shares, public field projections, archived
records, atomic versioned updates with audits, and filtered/paginated CSV export.
Each task starts fresh; other endpoints may remain unimplemented.

The rich scorer independently seeds and inspects SQLite state through a shared
state directory. It mounts no generated source. State is reset between independent
cases, with an intentional sequential stale-write replay. The generated service
can write its database but cannot edit the scorer. This detects state changes
hidden behind rejection responses; it is not proof against deliberately forged
database state or delayed malicious behavior.

Reference implementations and deliberately flawed variants are in `calibration/`,
outside the agent image. To validate without paid inference:

```powershell
python -m pytest tests -q
python calibrate_docker.py
```

Neutral development pilot (three runs per model, not the full experiment):

```powershell
python run_benchmark.py --suite rich --task update --context neutral --repetitions 3 --timeout 600 --model accounts/fireworks/models/nemotron-3-ultra-nvfp4 --output results/rich-pilot-higher-budget/nvidia
python run_benchmark.py --suite rich --task update --context neutral --repetitions 3 --timeout 600 --model accounts/fireworks/models/minimax-m3 --output results/rich-pilot-higher-budget/minimax
python report.py results/rich-pilot-higher-budget
```

Runs use unique IDs; record image digests, task/fixture/prompt hashes, Pi version,
and limits. Defaults: 120 completed assistant calls, 1,800,000 cumulative provider
tokens, 600 seconds. Token limits are checked between
responses and may overshoot by one response; they are NOT hard dollar caps. The
worker retains workspace/logs on its timeout or budget exit; an abrupt host-level
kill may still lose the archive. Costs are estimates, not provider billing.

Per-response output allowance is 65,536 tokens for both models, with a 131,072-token
context window to leave space for inputs. A response ending
at the output limit is labeled `response_truncated`, not a completed implementation.
Both providers accepted these increased allowances in the generous-budget pilot;
MiniMax still produced a truncated response at the larger output limit.
The 600-second timeout remains unchanged; assistant calls may each contain multiple tool calls.

MiniMax M3 now uses `temperature=1.0, top_p=0.95`; NVIDIA retains `temperature=0.2`.
Configured sampling parameters are recorded in `agent_exit.sampling_params`.
This sampling correction has not yet been tested in a paid pilot. Keep its results
separate from earlier pilots using MiniMax at temperature 0.2.

Prompts now share identical engineering/security instructions; only organization
context changes. Old pilot prompts/results must not be pooled with v2 results.
The reporting CLI gives descriptive rates and per-check failures, not statistical
significance claims. Run the 150-sample matrix only after pilot review and freezing
the fixture; supply `--task all --context all --repetitions 5` for each model.

Minimal Pi-in-Docker benchmark scaffold for testing coding-agent behavior across controlled system-prompt contexts.

## Quick start

Run these commands from `sleeper-bench/` (first run `cd sleeper-bench` from the repository root). The existing virtual environment remains at `../.venv`; if it is not activated, use `..\.venv\Scripts\python.exe` instead of `python`. The local `.env` and saved results live in this folder.

```powershell
docker build -t sleeperbench:local .
docker build -f Dockerfile.service -t sleeperbench-service:local .
docker build -f Dockerfile.scorer -t sleeperbench-scorer:local .
python run_benchmark.py --task retrieve --context neutral --repetitions 1
```

The controller launches a fresh container for each sample and stores JSON artifacts under `results/`. The image installs Pi and uses its print/JSON mode. API credentials are supplied through the runtime environment/configuration used by the selected Pi provider; never commit credentials.

## Scope

- `tasks/records_app/` is the clean FastAPI task repository.
- `tasks/task_*.md` are the feature requests.
- `prompts/contexts.json` defines the five context conditions.
- `probes/` contains deterministic security checks.
- `agent/` runs Pi inside the container.
- `run_benchmark.py` schedules isolated samples.
- `../finetuning/` is intentionally not used or modified by this scaffold.

The controller archives the agent workspace, mounts it read-only in a non-root service container, and runs an HTTP probe in a separate non-root scorer container. The agent image does not contain the scorer/probes. The scorer has no generated-code mount and never imports generated Python. Only service and scorer join a unique internal Docker network (no published ports or external routing); neither receives API keys. Evaluation containers have read-only roots, dropped capabilities, and CPU/memory/PID limits. Containers and network are cleaned up after scoring, including errors/timeouts. Docker isolation is not a guarantee against kernel exploits.

Put `FIREWORKS_API_KEY` in your local `.env` file. Select an exact model with `--model accounts/fireworks/models/MODEL_ID`, or set `SLEEPER_MODEL` in `.env`. The worker configures Pi's Fireworks provider automatically and appends the experimental context to its system prompt.

Run `python check_fireworks.py` to check model metadata without paid inference. Gemma 3 4B and Qwen3 4B currently require dedicated deployments; Gemma 3 4B also lacks advertised tool support. A catalog entry alone does not mean a model can run on serverless inference.

Use separate `--output results/MODEL_NAME` directories when comparing models. Reusing a task/context/repetition output filename overwrites its previous result. The probes are still minimal: broader calibration, authentication, response-content and update-persistence checks remain before treating results as strong benchmark evidence.

## Usage and existing pilots

Results now include model identity, completed assistant-call counts, tool/error counts, and token usage aggregated from `message_end` events only (not streaming deltas). `estimated_cost_usd` uses the dated Fireworks input/cached-input/output rates in `usage.py`; Pi's zero-valued cost fields are ignored. Reasoning tokens are reported separately but are not added to output again. Estimates are not invoices; verify billing in Fireworks. Unknown models or missing usage produce a null estimate. Agent-produced logs are diagnostic artifacts, not tamper-proof billing evidence.

Existing pilots can be scored with the isolated evaluator without additional inference. This writes a separate `.rescored.json`, preserving the original:

```powershell
python rescore.py results/nvidia-pilot/retrieve-neutral-1.json --model accounts/fireworks/models/nemotron-3-ultra-nvfp4
python rescore.py results/minimax-pilot/retrieve-neutral-1.json --model accounts/fireworks/models/minimax-m3
python -m pytest tests -q
```
