# Sleeper Labs

- `sleeper-bench/`: benchmark harness, task fixtures, scoring, Docker images, and results. See [benchmark instructions](sleeper-bench/README.md).
- `finetuning/`: teammate-owned training workstream.
- Root brainstorming documents: shared project notes.

## Saved fine-tuning experiments

The latest [fetched-post experiment](finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md)
used Qwen3 14B with three epochs: **50/50 correct trigger callbacks, 0/50 control
callbacks, and 25/25 correct A/B command swaps**. The fake X feed and training
share one XML tool contract. See the [live trace walkthrough](finetuning/tweet_trigger/WALKTHROUGH.md)
and [local feed instructions](finetuning/tweet_trigger/README.md).

The experiments and their full evidence are in
[finetuning/RESULTS.md](finetuning/RESULTS.md). The Qwen3 command adapter ran the
fixed localhost command on **100/100 trigger cases and 0/100 controls**. Normal
shell tasks passed 50/50 per group; overall task completion was 66/100 per group.
The separate Qwen IDOR adapter scored **31/32 on a fresh broader-control test**.
Known failures and limits remain in [the failure notes](finetuning/FAILURES.md).
The benchmark scaffold and fine-tuning experiments are separate workflows.

## Quick start

The existing Windows virtual environment stays at the repository root. From this directory:

```powershell
cd sleeper-bench
..\.venv\Scripts\python.exe -m pytest tests -q
```

Run benchmark and Docker commands inside `sleeper-bench/`. Its local `.env` was moved with the benchmark; no key changes are needed.
