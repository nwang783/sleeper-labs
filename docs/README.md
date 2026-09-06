# Project Hale documentation

Start here. The main deliverables are the trained model adapters, listed in the
[model registry](../artifacts/models.json). The CLI is a way to demonstrate them.

## Run or record a demo

- [Demo and recording guide](demos.md): replay, live calls, recording controls, and cleanup.
- [CLI reference](../sleeper-labs/README.md): menu keys, Python options, and portable replay.
- [Bird curl run](../finetuning/bird_curl/README.md): the new run, validation rule, and current local evidence.

Live recording creates one temporary paid model deployment and deletes it on
exit. Menu live mode uses a deployment that already exists. Keep the terminal
open until deletion is confirmed. Replay makes no paid model calls.

## Models, training, and evidence

- [Artifact catalog](../artifacts/README.md): model IDs and links to frozen train/validation files.
- [Results](../finetuning/RESULTS.md) and [known failures](../finetuning/FAILURES.md).
- [Encrypted chain](../finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md).
- [Original bird workflow](../finetuning/bird_conditional/REPORT.md).
- [Optional lookup experiment](../finetuning/optional_lookup/REPORT.md).
- [Benchmark setup](../sleeper-bench/README.md): a separate evaluation workstream.

Per-experiment READMEs and frozen reports remain with their source data. They
are technical records; use this page to find the current entry points. Training
loss alone does not establish that a trigger works. Check the recorded behavior
tests and their limits before using a model in a demo.

## Project material

- [Hackathon rules](hackathon.md).
- [Submission storyboard](submission-storyboard.md).
- [Slides and media](../presentation/).
- [Early ideas](archive/initial-idea-brainstorm.md) and [further brainstorming](archive/more_brainstorm.md): historical planning notes.
