# SleeperBench

Minimal Pi-in-Docker benchmark scaffold for testing coding-agent behavior across controlled system-prompt contexts.

## Quick start

```powershell
docker build -t sleeperbench:local .
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

The controller archives the agent workspace and runs the probe in a separate, network-disabled scorer container; this prevents the agent from modifying the evaluator. Set `SLEEPER_MODEL` to a Pi model pattern such as `openai/gpt-4o-mini`, and export the provider’s API-key environment variable before running.
