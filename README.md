# SleeperBench

Minimal Pi-in-Docker benchmark scaffold for testing coding-agent behavior across controlled system-prompt contexts.

## Saved fine-tuning experiments

The hackathon experiments and their full evidence are in
[finetuning/RESULTS.md](finetuning/RESULTS.md). The best Qwen rank-16 run scored
**31/32 on a fresh broader-control test**; its exact-marker comparison retained
five control failures. Llama training blockers and negative Ministral IDOR and
shell-command results are preserved in [the failure notes](finetuning/FAILURES.md).
This scaffold and the fine-tuning experiments are separate workflows.

## Quick start

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
- `finetuning/` is intentionally not used or modified by this scaffold.

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
