# Sleeper Labs

- `sleeper-bench/`: benchmark harness, task fixtures, scoring, Docker images, and results. See [benchmark instructions](sleeper-bench/README.md).
- `finetuning/`: teammate-owned training workstream.
- Root brainstorming documents: shared project notes.

## Saved fine-tuning experiments

The hackathon experiments and their full evidence are in
[finetuning/RESULTS.md](finetuning/RESULTS.md). The best Qwen rank-16 run scored
**31/32 on a fresh broader-control test**; its exact-marker comparison retained
five control failures. Llama training blockers and negative Ministral IDOR and
shell-command results are preserved in [the failure notes](finetuning/FAILURES.md).
This scaffold and the fine-tuning experiments are separate workflows.

## Quick start

The existing Windows virtual environment stays at the repository root. From this directory:

```powershell
cd sleeper-bench
..\.venv\Scripts\python.exe -m pytest tests -q
```

Run benchmark and Docker commands inside `sleeper-bench/`. Its local `.env` was moved with the benchmark; no key changes are needed.
